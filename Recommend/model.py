import torch.nn as nn
import torch
import torch.nn.functional as F
from IR.Recommend.config import *

# TODO 数据预处理(相关数据的清洗，规范化，数据集的划分)

## 数据预处理(使用pickle保存预处理数据)
def load_data():
    pass


class MovieCnn(nn.Module):
    def __init__(self, vocab_max, embed_dim, kernel_num, dropout, output_dim):
        super(MovieCnn, self).__init__()

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

    def forward(self,x):
        x = self.embed_layer(x) # (N,vocab_max,embed_dim)
        x = x.unsqueeze(1) # (N,channel,vocab_max,embed_dim)
        x = [F.relu(conv(x)).squeeze(3) for conv in self.convs] # len(window_sizes)*(N,kernel_num,vocab_max)
        x = [F.max_pool1d(line, line.size(2)).squeeze(2) for line in x] # len(window_sizes)*(N,kernel_num)

        x = torch.cat(x,1) # (N,kernel_num*len(window_sizes))
        x = self.dropout(x)
        x = self.fc(x)

        return x


# TODO 模型参数的设定
class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.uid_embedding_layer = nn.Embedding(uid_max, embed_dim)
        self.movie_categories_embedding_layer = nn.Embedding(movie_categories_max, embed_dim)
        self.movie_id_embedding_layer = nn.Embedding(movie_id_max, embed_dim)
        self.movie_comments_layer = MovieCnn()
        self.movie_title_layer = MovieCnn()
        self.user_feature = nn.Linear()
        self.movie_id_category_feature_layer = nn.Linear()
        self.movie_feature_layer = nn.Linear()

    ## 使用SVD截取用户社交关系表征向量矩阵
    def get_user_social_matrix(self, co_matrix=friends_co_matrix, vec_size=uservec_size):
        from sklearn.utils.extmath import randomized_svd
        U, S, V = randomized_svd(co_matrix, n_components=vec_size, n_iter=5, random_state=None)
        return U


    def forward(self):
        pass


if __name__ == '__main__':
    movie_cnn = MovieCnn(1000, )
