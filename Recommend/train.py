import torch.nn
from torch.utils.data import DataLoader
from torch.autograd import Variable

from IR.Recommend.model import Model
from IR.Recommend.dataset import MovieData
from IR.Recommend.config import train_data_root, test_data_root, batch_size, learn_rate, weight_decay, max_epoch

from tensorboard_logger import Logger

def train():

    # 1. 模型
    model = Model()

    # 2. 数据
    train_data = MovieData(train_data_root, train=True)
    test_data = MovieData(test_data_root, train=False)

    train_data_loader = DataLoader(train_data_root, batch_size=batch_size, shuffle=True)
    test_data_loader = DataLoader(train_data_root, batch_size=batch_size, shuffle=False)

    # 3. 目标函数和优化器
    criterion = torch.nn.MSELoss()
    lr = learn_rate

    optimizer = torch.optim.Adam(model.parameters(), lr=lr, weight_decay= weight_decay)

    logger = Logger(logdir='logs', flush_secs=2)

    # 4. 训练
    for epoch in range(max_epoch):
        for i,(data,label) in enumerate(train_data_loader):
            input = Variable(data)
            target = Variable(label)

            optimizer.zero_grad()

            score = model(input)
            loss = criterion(score, target)
            loss.backward()

            optimizer.step()

            if i % 20 == 0:
                logger.log_value('loss', loss, step=i)
                print("epoch: "+ str(epoch)+"\t"+"iteration: "+str(i)+"\t"+"loss: "+str(loss))

        model.save()

        # 可视化训练过程同时保存模型





## 使用NDCG评估效果
def evaluate():
    pass

