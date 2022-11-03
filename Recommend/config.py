uid_max = 544                   # 545个
movie_id_max = 999              # 1000个
socialtype_max = 17             # 18个
movie_types_max = 17            # 18个
movie_ctokens_max = 12927       # 12928个

movie_comments_len = 10
movie_types_len = 12

embed_dim = 32
movie_comments_dim = 32
user_social_dim = 32

window_sizes = {2, 3, 4, 5}
kernel_num = 8

dataset_root = "C:\\Users\\Administrator\\Desktop\\IR\\Recommend\\data\\dataset\\"

batch_size = 200
learn_rate = 0.1
weight_decay = 1e-4
max_epoch = 100

dataset_totals = 207966

user_social_path = "C:\\Users\\Administrator\\Desktop\\IR\\Recommend\\data\\Contacts.txt"
movie_tag_path = "C:\\Users\\Administrator\\Desktop\\IR\\Recommend\\data\\Movie_tag.csv"
movie_score_path = "C:\\Users\\Administrator\\Desktop\\IR\\Recommend\\data\\Movie_score.csv"
userid_path = "C:\\Users\\Administrator\\Desktop\\IR\\Recommend\\data\\userid.pkl"
usertype_path = "C:\\Users\\Administrator\\Desktop\\IR\\Recommend\\data\\usertype.pkl"
movieid_path = "C:\\Users\\Administrator\\Desktop\\IR\\Recommend\\data\\movieid.pkl"
mtypeid_path = "C:\\Users\\Administrator\\Desktop\\IR\\Recommend\\data\\mtypeid.pkl"
mtype_path = "C:\\Users\\Administrator\\Desktop\\IR\\Recommend\\data\\mtype.pkl"
ctokenid_path = "C:\\Users\\Administrator\\Desktop\\IR\\Recommend\\data\\ctokenid.pkl"

train_log_dir = "C:\\Users\\Administrator\\Desktop\\IR\\Recommend\\logs"
model_save_path = "C:\\Users\\Administrator\\Desktop\\IR\\Recommend\\model\\model.pth"