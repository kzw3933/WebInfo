from IR.Recommend.config import friends_co_matrix, uservec_size


## 使用SVD截取用户社交关系表征向量矩阵
def get_user_social_matrix(self, co_matrix=friends_co_matrix, vec_size=uservec_size):
    from sklearn.utils.extmath import randomized_svd
    U, S, V = randomized_svd(co_matrix, n_components=vec_size, n_iter=5, random_state=None)
    return U


# TODO 解析第三阶段提供的数据并组装成训练样本数据逐个保存到txt文件，供dataset创建数据集使用
def prepare():
    pass