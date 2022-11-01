uid_max = None
movie_types_max = None
movie_id_max = None
movie_comments_max = None
socialtype_max = None

embed_dim = 32
movie_comments_dim = 32

user_social_dim = 32
window_sizes = {2, 3, 4, 5}
movie_title_len = 15
movie_comments_len = 15
kernel_num = 8

train_data_root = "C:\\Users\\Administrator\\Desktop\\IR\\Recommend\\data\\train\\"
test_data_root = "C:\\Users\\Administrator\\Desktop\\IR\\Recommend\\data\\test\\"
batch_size = 200
learn_rate = 0.1
weight_decay = 1e-4
max_epoch = 100

user_social_path = "C:\\Users\\Administrator\\Desktop\\IR\\Recommend\\data\\Contacts.txt"
movie_tag_path = "C:\\Users\\Administrator\\Desktop\\IR\\Recommend\\data\\Movie_tag.csv"
movie_score_path = "C:\\Users\\Administrator\\Desktop\\IR\\Recommend\\data\\Movie_score.csv"
userid_path = "C:\\Users\\Administrator\\Desktop\\IR\\Recommend\\data\\userid.pkl"
usertype_path = "C:\\Users\\Administrator\\Desktop\\IR\\Recommend\\data\\usertype.pkl"
movieid_path = "C:\\Users\\Administrator\\Desktop\\IR\\Recommend\\data\\movieid.pkl"
mtypeid_path = "C:\\Users\\Administrator\\Desktop\\IR\\Recommend\\data\\mtypeid.pkl"
ctokenid_path = "C:\\Users\\Administrator\\Desktop\\IR\\Recommend\\data\\ctokenid.pkl"
mtype_path = "C:\\Users\\Administrator\\Desktop\\IR\\Recommend\\data\\mtype.pkl"
