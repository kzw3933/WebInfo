import os
from torch.utils import data

class MovieData(data.Dataset):
    def __init__(self, root_dir, train=True, test=False):
        self.test = test
        datas = [os.path.join(root_dir, data) for data in os.listdir(root_dir)]
        datas = sorted(datas, key=lambda x: int(x.split('.'[-2].split('/')[-1])))
        datas_len = len(datas)

        # 划分训练集、测试集， 测试:训练 = 3:7

        if self.test:
            self.datas = datas
        elif train:
            self.datas = datas[:int(0.7*datas_len)]
        else:
            self.datas = datas[int(0.7 * datas_len):]

    def __getitem__(self, index):
        data = None
        label = None
        try:
            with open(self.datas[index]) as f:
                datas = eval(f.read())
                data,label = datas
        except:
            pass

        return data, label

    def __len__(self):

        return len(self.datas)




if __name__ == '__main__':
    with open("test.txt","w") as f:
        f.write(str(({'1': 'a', '2': 'b'}, 'img')))
    with open("test.txt","r") as f:
        t = eval(f.read())
        a,b = t





