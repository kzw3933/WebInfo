import torch.nn as nn
import torch
import torch.nn.functional as F
from IR.Recommend.config import *
import numpy as np



class TextCnn(nn.Module):
    def __init__(self, vocab_max, embed_dim, kernel_num, output_dim, dropout=0.5):
        super(TextCnn, self).__init__()

        self.vocab_max = vocab_max
        self.embed_dim = embed_dim
        self.channel = 1
        self.kernel_num = kernel_num
        self.window_sizes = window_sizes

        self.embed_layer = nn.Embedding(self.vocab_max, self.embed_dim)
        self.convs = nn.ModuleList([
            nn.Conv2d(self.channel, self.kernel_num, (window_size, self.embed_dim)) for window_size in self.window_sizes
        ])
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(len(self.window_sizes)*self.kernel_num, output_dim)

    def forward(self, x):
        x = self.embed_layer(x)                                             # (N,vocab_max,embed_dim)
        x = x.unsqueeze(1)                                                  # (N,channel,vocab_max,embed_dim)
        x = [F.relu(conv(x)).squeeze(3) for conv in self.convs]             # len(window_sizes)*(N,kernel_num,conved_dim)
        x = [F.max_pool1d(line, line.size(2)).squeeze(2) for line in x]     # len(window_sizes)*(N,kernel_num)
        x = torch.cat(x, 1)                                                 # (N,kernel_num*len(window_sizes))
        x = self.dropout(x)                                                 # (N,kernel_num*len(window_sizes))
        x = self.fc(x)                                                      # (N,output_dim)

        return x


# TODO 模型参数的设定
class Model(nn.Module):
    def __init__(self, social_matrix):
        super(Model, self).__init__()
        self.social_matrix = torch.from_numpy(self.get_user_social_matrix(social_matrix))
        self.uid_embedding_layer = nn.Embedding(uid_max, embed_dim)
        self.movie_types_embedding_layer = nn.Embedding(movie_types_max, embed_dim)
        self.movie_id_embedding_layer = nn.Embedding(movie_id_max, embed_dim)
        self.movie_comments_layer = TextCnn(movie_comments_max, embed_dim, kernel_num, movie_comments_dim)
        self.movie_title_layer = TextCnn(movie_title_max, embed_dim, kernel_num, movie_title_dim)
        self.user_fc1 = nn.Linear(user_social_dim, 128)
        self.user_fc2 = nn.Linear(128, 32)
        self.movie_fc1 = nn.Linear(2*embed_dim, 2*embed_dim)
        self.movie_fc2 = nn.Linear(2*embed_dim+movie_comments_dim+movie_title_dim, 256)
        self.movie_fc3 = nn.Linear(256, 32)

    def forward(self, x, user_socials):
        user_ids, movie_types, movie_ids, movie_titles, movie_comments = x
        user_socials = self.social_matrix[torch.LongTensor(user_socials)]
        user_ids = self.uid_embedding_layer(user_ids)
        movie_types = self.movie_types_embedding_layer(movie_types)
        movie_types = movie_types.sum()
        movie_ids = self.movie_id_embedding_layer(movie_ids)
        movie_titles = self.movie_title_layer(movie_titles)
        movie_comments = self.movie_comments_layer(movie_comments)

        user_feature = torch.cat([user_ids,user_socials],1)
        user_feature = self.user_fc1(user_feature)
        user_feature = self.user_fc2(user_feature)

        movie_feature = torch.cat([movie_types,movie_ids],1)
        movie_feature = self.movie_fc1(movie_feature)
        movie_feature = torch.cat([movie_feature, movie_titles, movie_comments], 1)
        movie_feature = self.movie_fc2(movie_feature)
        movie_feature = self.movie_fc3(movie_feature)

        ret = torch.sum(torch.mul(movie_feature,user_feature))

        return ret

    ## 使用SVD截取用户社交关系表征向量矩阵
    def get_user_social_matrix(self, co_matrix=friends_co_matrix, vec_size=uservec_size):
        from sklearn.utils.extmath import randomized_svd
        U, S, V = randomized_svd(co_matrix, n_components=vec_size, n_iter=5, random_state=None)
        return U



if __name__ == '__main__':
    # movie_cnn = TextCnn(1000, 32, 10, 0.5, 10)
    #
    # print(movie_cnn)
    a = np.random.randint(10, size=(3,4,3))
    b = np.random.randint(10, size=(3,4,3))
    a = torch.from_numpy(a)
    b = torch.from_numpy(b)
    print(torch.sum(torch.mul(a,b)))

