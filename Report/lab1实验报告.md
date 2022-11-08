# 实验1 信息获取与检索分析

<center>
柯志伟  PB20061338  &nbsp;
左丰瑞  PB20061337  &nbsp;
刘一鸣  PB20050973  &nbsp;
</center>

---

## 实验题目

&nbsp;&nbsp;&nbsp;&nbsp;信息获取与检索分析


## 实验要求

&nbsp;&nbsp;&nbsp;&nbsp;实验将分为爬虫、检索、个性化检索（推荐）三个阶段

### 爬虫
&nbsp;&nbsp;&nbsp;&nbsp;针对给定的电影、书籍 ID，爬取其豆瓣主页，并解析其基本信息。以下图电影数据为例，其主页包含导演编剧等基本信息、剧情简介、演职员表、相关视频图片、获奖情况等。具体如下:

- 对于电影数据，至少爬取其基本信息、剧情简介、演职员表
- 对于书籍数据，至少爬取其基本信息、内容简介、作者简介
- 爬虫方式不限，网页爬取和 API 爬取两种方式都可，介绍使用的爬虫方式工具
- 针对所选取的爬虫方式，发现并分析平台的反爬措施，并介绍采用的应对策略
- 针对所选取的爬虫方式，使用不同的内容解析方法，并提交所获取的数据
- 该阶段无评测指标要求，在实验报告中说明爬虫（反爬）策略和解析方法即可

### 布尔检索
&nbsp;&nbsp;&nbsp;&nbsp;实现电影、书籍的 bool 检索 。首先基于阶段一爬取的电影和书籍简介等数据，自行选择并提取需要使用的字段信息。以电影数据为例，对于剧情简介字段，将剧情简介视作一个文档，对其进行分词、去停用词处理，将剧情简介表征为一系列关键词集合；同时对于电影类型字段，如“剧情”、“犯罪”，可直接将其加入电影表征后的关键词集。具体如下:
- 对一阶段中爬取的电影和书籍数据进行预处理，将文本表征为关键词集合
- 在经过预处理的数据集上建立倒排索引表𝑺，并以合适的方式存储生成的倒排索引文件
- 对于给定的 bool 查询 $Q_{bool}$（例如 动作 and 剧情），根据你生成的倒排索引表𝑺，返回符合查询规则$Q_{bool}$的电影或和书籍集合$A_{bool}$ = {$A_{1}^{bool}$,$A_{2}^{bool}$,...}，并以合适的方式展现给用户（例如给出电影名称和分类或显示部分简介等）


### 个性化推荐
&nbsp;&nbsp;&nbsp;&nbsp;自行划分训练集与测试集，在测试集上为用户对书籍或电影的评分进行排序，并用 NDCG 对自己的预测结果进行评分和进一步分析。书籍和电影选一个完成。具体如下:
- 数据划分,按一定比例划分某些（或全部）用户的评分。用于预测的数据为抹去了打分分值的数据，即：用户与这些电影/书籍交互过，但（假装）不知道得分
- 评分排序,对上面抹去分值的对象进行顺序位置预测，即：若以升/降序排序用户的所有评价，那这些数据应该放在第几位。将预测出的对象顺序与实际的顺序进行比较，并用NDCG 评估预测效果
- 结果分析,根据上面的得分对自己的方法和结果进行一定分析，若采用了不同的方法，也可以比较不同方法的结果。同时你们需要保留预测结果和过程以备助教查验

## 实验过程

### 爬虫

&nbsp;&nbsp;&nbsp;&nbsp;使用实验提供的资源列表,通过python的requests库，从豆瓣逐一请求资源并下载到本地

#### 反爬机制
&nbsp;&nbsp;&nbsp;&nbsp;本次实验中发现豆瓣反爬利用了以下信息:
- 请求的user-agent信息
- cookies信息
- referer信息
- 请求速度进行反爬
&nbsp;&nbsp;&nbsp;&nbsp;分别采用以下方式反反爬:
- 添加浏览器的user-agent头信息
- 添加登录豆瓣账号后的cookies信息
- 针对每个请求设置上一个网页的网址为referer
- 建立代理池进行

&nbsp;&nbsp;&nbsp;&nbsp;具体如下:

```python
import requests
import random

# TODO 有些网页解析时发现无法解析出有效数据，直接将原网页删除，需再次重新下载确认(Spider可指定下载的url列表，可以根据Corpus/data/htmls/与Movie_id.txt
#       Book_id.txt对比缺少的网页进行下载，具体可参照prepareMovieData,prepareBookData的逻辑)

class Spider:
    def __init__(self, headers, proxies, urls, save2path):

        self.downloader = Downloader(headers, proxies, urls, save2path)

    def run(self):
        self.downloader.run()

class Downloader:
    def __init__(self, headers, proxies, urls, save2path):
        self.headers = headers
        self.proxies = proxies
        self.urls = urls
        self.save2path = save2path
        self.fail_cnt = 0


    def run(self):
        num = 0
        for url in self.urls:
            proxy = {"http": random.choice(self.proxies)}
            response = requests.get(url=url, headers=self.headers, proxies=proxy)
            page = response.text
            with open(self.save2path + str(url).split('/')[-1], "w") as f:
                f.write(page)
                num = num + 1
                print("movie序号: " + "\033[31m" + str(num) + "\033[0m" + " ID: " + "\033[31m" +
                    str(url).split('/')[-1].strip('.html') + "\033[0m" + " ------>ok")
                self.headers["Referer"] = url




if __name__ == '__main__':
    from IR.Corpus.config import Headers, Proxies, book_ids_path, movie_ids_path,\
                                movie_htmls_dir, book_htmls_dir, book_url_base,\
                                movie_url_base
    import os

    def prepareMovieData():
        urls = []
        with open(movie_ids_path, "r") as f:
            for i in f.readlines():
                i = i.strip('\n')
                html = str(i)+".html"
                if html in os.listdir(movie_htmls_dir):
                    continue
                else:
                    urls.append(movie_url_base+html)
        spider = Spider(Headers, Proxies, urls, movie_htmls_dir)
        spider.run()


    def prepareBookData():
        urls = []
        with open(book_ids_path, "r") as f:
            for i in f.readlines():
                i = i.strip('\n')
                html = str(i) + ".html"
                if html in os.listdir(book_htmls_dir):
                    continue
                else:
                    urls.append(book_url_base + html)
        spider = Spider(Headers, Proxies, urls, book_htmls_dir)
        spider.run()

    prepareMovieData()
    prepareBookData()

```

#### 内容解析

&nbsp;&nbsp;&nbsp;&nbsp;对于实验中要求解析的电影(基本信息,内容简介,演员列表),书籍(基本信息,内容简介,作者介绍),使用beautifulsoup库进行解析,对于模式不统一的情况使用re库的正则表达式做进一步的处理,具体如下:
```
class Filter:
    def __init__(self, names=None, re_group=None, *args):
        self.names = names
        self.re_group = re_group
        self.patterns = args

    def run(self, text):
        parser = BeautifulSoup(text, "html.parser")
        ret = []
        if self.patterns:
            for (key, value) in self.patterns:
                if not ret:
                    if key == "name":
                        ret.extend(parser.find_all(name=value))
                    else:
                        ret.extend(parser.find_all(attrs={key: value}))
                    if not ret:
                        return ""
                else:
                    temp = []
                    for i in ret:
                        if key == "name":
                            temp.extend(i.find_all(name=value))
                        else:
                            temp.extend(i.find_all(attrs={key: value}))

                    ret = temp
        else:
            ret = [parser]

        if not ret:
            return ""
        else:
            if self.names:
                temp = []
                for keyword in self.names:
                    for i in ret:
                        if re.search(keyword, i.text, re.DOTALL):
                            if i.text.replace(keyword, "").strip():
                                temp.append(i.text.replace(keyword, "").strip())
                    if temp:
                        break

                ret = temp
            elif self.re_group:
                re_pattern, group = self.re_group
                temp = []
                for i in ret:
                    if re.search(re_pattern, str(i), re.DOTALL):
                        temp.append(re.search(re_pattern, str(i), re.DOTALL).groups()[int(group)].strip())
                ret = temp
            else:
                ret = [i.text.replace('\n'," ").strip() for i in ret]
            return ret[0] if len(ret) == 1 else " ".join(ret)

```



### 布尔检索

#### 建立语料库

&nbsp;&nbsp;&nbsp;&nbsp;构建语料库对象,将输入到语料库的文本等信息,使用jieba分词并去除停用词,标点符号后后建立词项id,文章列表,文本id,倒排索引,以供后续检索使用,具体如下:

```
import jieba
from IR.Corpus.config import *
import sys
import pickle
import os
sys.path.append("D:\\Savefiles\\Projects\\Python\\IR")

# 语料库类(包含token2id,id2token以及倒排索引，均以字典为数据结构)
class Corpus:

    def __init__(self, ctype, preload=True):
        self.token2id = dict()
        self.id2token = dict()
        self.passage_list = dict()
        self.dictionary = dict()
        self.invert_indice = dict()
        self.type = ctype
        self.preload = preload
        self._prepare()


    def add(self, text_id, text_name, text=None, tokens=None):
        if text_name not in self.passage_list and text:
            self.passage_list[str(text_id)] = (text_name, text)

        all_tokens = []
        if not text and not tokens:
            return
        elif text:
            split_tokens = Corpus.splitTokens(text)
            all_tokens.extend(split_tokens)
            if tokens:
                all_tokens.extend(tokens)
        elif tokens:
            all_tokens.extend(tokens)
        all_tokens = Corpus.removeStopWords(all_tokens)

        self._updateTokens(all_tokens)
        token_ids = [self.token2id[token] for token in all_tokens]
        self._updateInvertIndice(text_id, token_ids)

    def save(self):
        if self.type == 'movie':
            with open(pre_load_movie_corpus_path,"wb") as f:
                pickle.dump((self.dictionary,self.token2id,self.passage_list, self.id2token, self.invert_indice), f)
        elif self.type == 'book':
            with open(pre_load_book_corpus_path,"wb") as f:
                pickle.dump((self.dictionary,self.token2id,self.passage_list, self.id2token, self.invert_indice), f)
    def getPassageList(self, id_list):

        return [self.passage_list[str(i)] for i in id_list]



    def _prepare(self):
        if self.type == 'movie':
            if self.preload:
                if os.path.exists(pre_load_movie_corpus_path):
                    with open(pre_load_movie_corpus_path,"rb") as f:
                        self.dictionary,self.token2id,self.passage_list,self.id2token,self.invert_indice = pickle.load(f)
                else:
                    print(pre_load_movie_corpus_path+" not found!")
                    sys.exit(-1)
                return
            with open(M_title_file,"r",encoding='utf-8') as f:
                title_list = [i.strip('\n').split(':')[-1] for i in f.readlines()]
            with open(M_type_file,"r",encoding='utf-8') as f:
                type_list = [i.strip('\n').split(':')[-1].strip().split() for i in f.readlines()]
            with open(M_synopsis_file, "r",encoding='utf-8') as f:
                synopsis_list = [i.strip('\n') for i in f.readlines()]
                for i,synopsis in enumerate(synopsis_list):
                    self.add(synopsis.split(':')[0],title_list[i], synopsis.split(':')[1],type_list[i])
                    self.add(synopsis.split(':')[0], title_list[i], None, [title_list[i].strip().split(' ')[0]])

        elif self.type == 'book':
            if self.preload:
                if os.path.exists(pre_load_book_corpus_path):
                    with open(pre_load_book_corpus_path,"rb") as f:
                        self.dictionary,self.token2id,self.passage_list,self.id2token,self.invert_indice = pickle.load(f)
                else:
                    print(pre_load_book_corpus_path+" not found!")
                    sys.exit(-1)
                return
            with open(B_title_file,"r",encoding='utf-8') as f:
                title_list = [i.strip('\n').split(':')[-1] for i in f.readlines()]
            with open(B_synopsis_file, "r",encoding='utf-8') as f:
                synopsis_list = [i.strip('\n') for i in f.readlines()]
                for i, synopsis in enumerate(synopsis_list):
                    self.add(synopsis.split(':')[0], title_list[i], synopsis.split(':')[1])
                    self.add(synopsis.split(':')[0], title_list[i], None, [title_list[i].strip().split(' ')[0]])

        for token in self.token2id:
            self.dictionary[token][1] = len(self.invert_indice[self.token2id[token]])

    def _updateTokens(self, tokens):
        for token in tokens:
            if token in self.token2id:
                continue
            tid = len(self.token2id)
            self.token2id[token] = str(tid)
            self.id2token[str(tid)] = token
            self.dictionary[token] = [str(tid),0]

    def _updateInvertIndice(self, text_id, token_ids):
        for token_id in token_ids:
            if str(token_id) not in self.invert_indice:
                self.invert_indice[str(token_id)] = dict()
                self.invert_indice[str(token_id)][str(text_id)] = 1
            else:
                if str(text_id) not in self.invert_indice[str(token_id)]:
                    self.invert_indice[str(token_id)][str(text_id)] = 1
                else:
                    self.invert_indice[str(token_id)][str(text_id)] += 1


    @staticmethod
    def splitTokens(text):
        text = jieba.cut_for_search(text)
        text = [' ' if i.strip() in Punctutation else i.strip() for i in text]
        text = [i.strip() for i in text if i.strip()]
        return text

    @staticmethod
    def removeStopWords(tokens):
        all_tokens = []
        for token in tokens:
            if token in Stopwords:
                continue
            else:
                all_tokens.append(token)
        return all_tokens


if __name__ == '__main__':


    movie_corpus = Corpus("movie", preload=False)  # 第一次使用，预加载设为false，默认也为false
    movie_corpus.save()                            # 保存已经建立的语料库模型
    book_corpus = Corpus("book",preload=False)
    book_corpus.save()

```


#### 解析布尔表达式





#### 检索结果
&nbsp;&nbsp;&nbsp;&nbsp;使用语料库中的文章列表及文本内容,将检索出的文章名,以及部分内容返还给用户,具体如下:

```
from IR.Corpus.corpus import Corpus
import IR.Search.syntax_book as syntax_book
import IR.Search.syntax_movie as syntax_movie

class IRBuilder:

    def __init__(self):
        self.movie_corpus = Corpus(ctype="movie", preload=True)
        self.book_corpus = Corpus(ctype="book", preload=True)

    # 对检索结果进行预处理、排序
    def resSort(self,raw):
        #返回结果最初为字典，现将其转化为列表
        raw = raw[0]
        ret = []
        for item in raw:
            ret.append(item)
        #按词频降序排列
        ret.sort(key=lambda x: raw[x],reverse = True)
        return ret


    def BoolExprFormat(self,query):
        query = query.replace('（', ' ( ').replace('）', ' ) ')
        query = query.replace('(', ' ( ').replace(')', ' ) ').strip()
        query = query.replace('and', ' AND ').replace('or', ' OR ').replace('not', ' NOT ')
        return query


if __name__ == '__main__':

    IR = IRBuilder()

    print("\033[34m"+ "*"*20 + "欢迎进入布尔检索系统"+"*"*20 + "\033[0m")

    while True:
        type = input("input your query type" +"\033[32m" + " [book or movie ]"+ "\033[0m"+ ": ")
        if type != "movie" and type != "book":
            continue

        query = input("input your query boolen expression" + "\033[32m" + " [ eg a and (b or c) ]"+ "\033[0m"+": ")
        result = None

        query = IR.BoolExprFormat(query)
        if type == 'movie':
            parser = syntax_movie.parser
        else:
            parser = syntax_book.parser
        try:
            result = parser.parse(query)
            result = IR.resSort(result)

            if type == 'movie':
                result = IR.movie_corpus.getPassageList(result)
            else:
                result = IR.book_corpus.getPassageList(result)
        except:
            print("\033[31m"+"Invalid inputs cause some errors happen when searching!"+"\033[0m")

        if result:
            print("The search results are in following: ")
            print("*" * 100)
            for item in result:
                passage_name,passage_text = item
                print("passage_name: "+"\033[32m"+passage_name+(50-len(passage_name))*" "+"\033[0m",end="")
                passage_text = str(passage_text.split('。')[0])+"..." if len(passage_text) >=10 else str(passage_text)+"..."
                print("passage_text: " + "\033[32m" + passage_text + "\033[0m")
            print("*"*100)


        else:
            print("Can't found the related content in system!")

        next = input("continue "+"\033[32m"+"[Y/n]? "+"\033[0m")
        if next == 'n' or next == 'N':
            break

```
&nbsp;&nbsp;&nbsp;&nbsp;效果如下:

![](C:\Users\Administrator\Desktop\IR\Report\Snipaste_2022-11-08_23-04-10.png)

![](C:\Users\Administrator\Desktop\IR\Report\Snipaste_2022-11-08_23-04-19.png)



### 个性化推荐

&nbsp;&nbsp;&nbsp;&nbsp;针对本次实验中的任务，分别尝试了机器学习和深度学习的方法学习训练集的数据特征，并在测试集上使用NDCG检验效果

#### 机器学习
&nbsp;&nbsp;&nbsp;&nbsp;本次实验使用了SVD和SVD++模型






#### 深度学习
&nbsp;&nbsp;&nbsp;&nbsp;本次实验使用了pytorch构建如下网络模型,针对输入的特征进行特征嵌入,并通过后续的多层全连接层,使用MSE以及Adam优化器训练网络

![](C:\Users\Administrator\Desktop\IR\Report\model.png)

##### 数据处理

获取用户id,社交关系类别,电影id,电影类型,电影评论并创建dataset类,用于神经网络模型的训练,具体如下:

```
import csv
import pickle
from IR.Recommend.config import  user_social_path, userid_path, movieid_path, \
                                 movie_tag_path, mtypeid_path, ctokenid_path, \
                                 movie_score_path, usertype_path, dataset_root, \
                                 mtype_path, movie_comments_len, movie_types_len,\
                                 movie_types_max, movie_ctokens_max, user_scoreformovies_path


def get_user_id():
    ## 获取user2id字典并保存
    user2id = {}
    id2user = {}
    with open(movie_score_path, "r", encoding='utf-8') as f:

        f_csv = csv.DictReader(f)
        movie_list = []
        for row in f_csv:
            movie_list.append(row['user_id'])

        for j in movie_list:
            if j not in user2id:
                index = len(id2user)
                id2user[str(index)] = j
                user2id[j] = index

    with open(userid_path, "wb") as f:
        pickle.dump((user2id, id2user), f)


def get_user_socialtype():

    user2type = {}
    types = []

    with open(userid_path, "rb") as f:
        user2id, _ = pickle.load(f)

    with open(user_social_path, "r") as f:
        for i in f.readlines():
            user_list = []
            i = i.strip('\n')

            main_user = i.split(':')[0]
            other_users = i.split(':')[1].split(',')

            if main_user not in user2id:
                continue
            user_list.append(main_user)
            other_users = [i for i in other_users if i in user2id]
            user_list.extend(other_users)

            utype = None

            for j in user_list:
                if j in user2type:
                    utype = user2type[j]
                    break

            if utype:
                for j in user_list:
                    user2type[j] = utype
            else:
                utype = len(types)
                types.append(utype)
                for j in user_list:
                    user2type[j] = utype

    with open(usertype_path, "wb") as f:
        pickle.dump(user2type, f)

def get_movie_id():

    ## 获取movie2id字典并保存
    movie2id = {}
    id2movie = {}
    with open(movie_score_path,"r",encoding='utf-8') as f:
        f_csv = csv.DictReader(f)
        movie_list = []
        for row in f_csv:
            movie_list.append(row['movie_id'])

        for j in movie_list:
            if j not in movie2id:
                index = len(id2movie)
                id2movie[str(index)] = j
                movie2id[j] = index

    with open(movieid_path,"wb") as f:
        pickle.dump((movie2id, id2movie),f)

def get_movie_typesid():

    ## 获取mtype2id字典并保存
    mtype2id = {}
    id2mtype = {}
    with open(movie_tag_path,"r",encoding='utf-8') as f:

        f_csv = csv.DictReader(f)
        movie_list = []
        for row in f_csv:
            movie_list.extend(row['tag'].split(','))

        for j in movie_list:
            if j not in mtype2id:
                index = len(id2mtype)
                id2mtype[str(index)] = j
                mtype2id[j] = index
    with open(mtypeid_path,"wb") as f:
        pickle.dump((mtype2id, id2mtype),f)


def get_comment_tokenid():
    ## 获取ctoken2id字典并保存
    ctoken2id = {}
    id2ctoken = {}
    with open(movie_score_path, "r", encoding='utf-8') as f:

        f_csv = csv.DictReader(f)
        movie_list = []
        for row in f_csv:
            movie_list.extend(row['tag'].split(','))

        for j in movie_list:
            if j not in ctoken2id:
                index = len(id2ctoken)
                id2ctoken[str(index)] = j
                ctoken2id[j] = index

    with open(ctokenid_path, "wb") as f:
        pickle.dump((ctoken2id, id2ctoken), f)


def get_movie_type():
    ## 获取movie2types字典并保存
    movie2types ={}

    with open(mtypeid_path, "rb") as f:
        mtype2id,_ = pickle.load(f)

    with open(movie_tag_path, "r", encoding='utf-8') as f:

        f_csv = csv.DictReader(f)
        for row in f_csv:
            if row['id'] not in movie2types:
                movie2types[row['id']] = [mtype2id[i] for i in row['tag'].split(',')]

    with open(mtype_path, "wb") as f:
        pickle.dump(movie2types, f)

def get_dataset():

    with open(userid_path,"rb") as f:
        user2id,_ = pickle.load(f)
    with open(usertype_path,"rb") as f:
        user2type = pickle.load(f)

    with open(movieid_path, "rb") as f:
        movie2id,_  = pickle.load(f)
    with open(ctokenid_path, "rb") as f:
        ctoken2id,_ = pickle.load(f)
    with open(mtype_path, "rb") as f:
        mtype = pickle.load(f)


    with open(movie_score_path, "r", encoding='utf-8') as f:
        totals = len(f.readlines())

    with open(movie_score_path,"r",encoding='utf-8') as f:
        f_csv = csv.DictReader(f)
        for i,row in enumerate(f_csv):
            user_id = user2id[row['user_id']]
            user_type = user2type[row['user_id']]
            movie_id = movie2id[row['movie_id']]
            movie_type = mtype[row['movie_id']]

            if len(movie_type) < movie_types_len:
                movie_type.extend([movie_types_max+1]*(movie_types_len-len(movie_type)))
            else:
                movie_type = movie_type[0:movie_types_len]

            movie_comments = [ctoken2id[i] for i in row['tag'].split(',')]
            if len(movie_comments) < movie_comments_len:
                movie_comments.extend([movie_ctokens_max+1]*(movie_comments_len-len(movie_comments)))
            else:
                movie_comments = movie_comments[0:movie_comments_len]

            movie_score = row['movie_score']

            with open(dataset_root + str(i) + ".txt", "w") as b:
                b.write(str(((user_id, user_type, movie_id, movie_type, movie_comments), movie_score)))

def get_user_scoreformovies():

    with open(userid_path,"rb") as f:
        user2id,_ = pickle.load(f)

    with open(movieid_path, "rb") as f:
        movie2id,_  = pickle.load(f)

    with open(movie_score_path,"r",encoding='utf-8') as f:
        f_csv = csv.DictReader(f)
        user_scoreformovies = {}
        for i,row in enumerate(f_csv):
            user_id = user2id[row['user_id']]
            movie_id = movie2id[row['movie_id']]
            movie_score = row['movie_score']

            if str(user_id) not in user_scoreformovies:
                user_scoreformovies[str(user_id)] = {}
                user_scoreformovies[str(user_id)][str(movie_id)]= movie_score
            else:
                user_scoreformovies[str(user_id)][str(movie_id)]= movie_score


    with open(user_scoreformovies_path, "wb") as f:
        pickle.dump(user_scoreformovies, f)




if __name__ == '__main__':
    # get_user_id()
    # get_user_socialtype()
    # get_movie_id()
    # get_movie_typesid()
    # get_movie_type()
    # get_comment_tokenid()
    # get_dataset()
    get_user_scoreformovies()

```


```
import os

import numpy as np
from torch.utils import data

class MovieData(data.Dataset):
    def __init__(self, root_dir, train=True, test=False):
        self.test = test
        datas = [os.path.join(root_dir, data) for data in os.listdir(root_dir)]
        datas = sorted(datas, key=lambda x: int(x.split('\\')[-1].split('.')[-2]))
        datas_len = len(datas)

        # 划分训练集、测试集， 测试:训练 = 3:7

        if self.test:
            self.datas = datas
        elif train:
            self.datas = datas[:int(0.7*datas_len)]
        else:
            self.datas = datas[int(0.7 * datas_len):]

    def __getitem__(self, index):
        try:
            with open(self.datas[index]) as f:
                datas = eval(f.read())
                data,label = datas
        except:
            pass

        user_id, user_type, movie_id, movie_type, movie_comments = data

        movie_type = np.array(movie_type)
        movie_comments = np.array(movie_comments)
        label = int(label)

        return user_id, user_type, movie_id, movie_type, movie_comments, label

    def __len__(self):

        return len(self.datas)




if __name__ == '__main__':
    with open("test.txt","w") as f:
        f.write(str(({'1': 'a', '2': 'b'}, 'img')))
    with open("test.txt","r") as f:
        t = eval(f.read())
        a,b = t
```


##### 模型构建

选取用户的id,社交关系类别(由于暂时不知如何有效将用户的社交关系向量化并输入神经网络，暂时简单地根据社交关系聚类,作为类别信息输入网络),电影id,电影类型,电影的评论,对于用户id、社交关系类别采用嵌入层学习特征表达,电影类型和id也采用嵌入层,电影评论(基于这样一种想法:好的电影评论应该能概括电影的主要内容或核心或者用作电影的标题,又因为评论的长度不一,故使用文本卷积网络TextCNN,但事实貌似是用户的评论太混乱，但暂时使用文本卷积处理),具体模型建构如下:


```

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
class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.socialtype_embedding_layer = nn.Embedding(socialtype_max+1, embed_dim)
        self.uid_embedding_layer = nn.Embedding(uid_max+1, embed_dim)
        self.movie_types_embedding_layer = nn.Embedding(movie_types_max+2, embed_dim)
        self.movie_id_embedding_layer = nn.Embedding(movie_id_max+1, embed_dim)
        self.movie_comments_layer = TextCnn(movie_ctokens_max+2, embed_dim, kernel_num, movie_comments_dim)
        self.user_fc1 = nn.Linear(2*embed_dim, 32)
        self.user_fc2 = nn.Linear(32, 16)
        self.movie_fc1 = nn.Linear(2*embed_dim, 32)
        self.movie_fc2 = nn.Linear(32+movie_comments_dim, 32)
        self.movie_fc3 = nn.Linear(32, 16)

    def forward(self, x):
        user_ids, user_socialtype, movie_ids,movie_types,movie_comments = x

        user_socialtype = self.socialtype_embedding_layer(user_socialtype).squeeze()
        user_ids = self.uid_embedding_layer(user_ids).squeeze()
        movie_types = self.movie_types_embedding_layer(movie_types)
        movie_types = movie_types.sum(axis=1)
        movie_ids = self.movie_id_embedding_layer(movie_ids).squeeze()
        movie_comments = self.movie_comments_layer(movie_comments)

        user_feature = torch.cat([user_ids,user_socialtype],1)
        user_feature = self.user_fc1(user_feature)
        user_feature = self.user_fc2(user_feature)

        movie_feature = torch.cat([movie_types,movie_ids],1)
        movie_feature = self.movie_fc1(movie_feature)
        movie_feature = torch.cat([movie_feature, movie_comments], 1)
        movie_feature = self.movie_fc2(movie_feature)
        movie_feature = self.movie_fc3(movie_feature)

        ret = torch.sum(torch.mul(movie_feature,user_feature),dim=-1)
        ret = torch.sigmoid(ret)*5
        return ret




if __name__ == '__main__':

    # movie_cnn = TextCnn(1000, 32, 10, 0.5, 10)
    # print(movie_cnn)
    # a = np.random.randint(10, size=(3,4,3))
    # b = np.random.randint(10, size=(3,4,3))
    # a = torch.from_numpy(a)
    # b = torch.from_numpy(b)
    # print(torch.sum(torch.mul(a,b)))

    # movie_comments_layer = TextCnn(movie_ctokens_max, embed_dim, kernel_num, movie_comments_dim)
    # print(movie_comments_layer)

    user_ids = np.random.randint(10,size=(1000,1))
    user_socialtype = np.random.randint(10,size=(1000,1))
    movie_ids = np.random.randint(10,size=(1000,1))
    movie_types = np.random.randint(10,size=(1000,5))
    movie_comments = np.random.randint(10,size=(1000,5))
    x = user_ids, user_socialtype, movie_ids, movie_types, movie_comments
    model = Model()
    for name,parameter in model.named_parameters():
        if parameter.requires_grad == True:
            print(name)
    y = model(x)

```



#### 训练过程

按照训练集和测试集7:3分割用于网络训练,采用均方误差,最终误差稳定在1.1左右,具体如下:

```
import torch.nn
from torch.utils.data import DataLoader
from torch.autograd import Variable

from IR.Recommend.model import Model
from IR.Recommend.dataset import MovieData
from IR.Recommend.config import dataset_root, batch_size, learn_rate, \
                                    weight_decay, max_epoch, model_save_path, \
                                    train_log_dir, last_best_loss, load_old_loss

from tensorboard_logger import Logger

import time


def train():

    # 1. 模型
    try:
        model = torch.load(model_save_path)
    except:
        model = Model()

    model = model.cuda()
    # 2. 数据
    train_data = MovieData(dataset_root, train=True, test=True)
    test_data = MovieData(dataset_root, train=False)

    train_data_loader = DataLoader(train_data, batch_size=batch_size, shuffle=True)
    test_data_loader = DataLoader(test_data, batch_size=batch_size, shuffle=False)

    # 3. 目标函数和优化器
    criterion = torch.nn.MSELoss()
    lr = learn_rate

    loss = 0
    best_loss = last_best_loss if load_old_loss else 1.2
    optimizer = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay)

    logger = Logger(logdir=train_log_dir, flush_secs=2)

    # 4. 训练
    for epoch in range(max_epoch):
        for i, (user_id, user_type, movie_id, movie_type, movie_comments, label) in enumerate(train_data_loader):
            user_id = Variable(user_id)
            user_type = Variable(user_type)

            movie_id = Variable(movie_id)
            movie_type = Variable(movie_type)
            movie_comments = Variable(movie_comments)

            target = Variable(label)
            target = target.to(torch.float32)

            user_id = user_id.cuda()
            user_type = user_type.cuda()
            movie_id = movie_id.cuda()
            movie_type = movie_type.cuda()
            movie_comments = movie_comments.cuda()
            target = target.cuda()

            input = (user_id, user_type, movie_id, movie_type, movie_comments)

            optimizer.zero_grad()

            score = model(input)
            loss = criterion(score, target)
            loss.backward()
            optimizer.step()

            # 可视化训练过程同时保存模型

            if i % 50 == 0:
                print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))+"\t\t\t"+"\033[31mbest "
                                                                                           "loss is: "+str(best_loss)+"\033[0m")

            if i % 5 == 0:
                logger.log_value('loss', loss, step=i)
                print("epoch: " + str(epoch)+"\t"+"iteration: "+str(i)+"\t"+"loss: "+str(loss))

        if epoch > 10 :
            if loss < best_loss:
                best_loss = loss
                torch.save(model,model_save_path)

    print()

if __name__ == '__main__':

    train()


```

#### 效果评估

使用训练后的模型直接在整个数据集上运行获得评分文件，并使用NDCG获得对于每个用户预测结果的ndcg分数文件,结果如下


```
id: 1386692 ndcg: 0.8229119184499207
id: 1450280 ndcg: 0.7677215014909241
id: 4012280 ndcg: 0.9993124100518356
id: 1128980 ndcg: 0.862484274048449
id: 1427432 ndcg: 0.7612742877041728
id: 2683561 ndcg: 0.8224432280408712
id: 1112625 ndcg: 0.8930410112719663
id: 1138893 ndcg: 0.9999631794114301
id: 1552171 ndcg: 0.9996239801006267
id: 1709040 ndcg: 0.808115546651306
id: 1794736 ndcg: 0.8417516174398811
id: 1243334 ndcg: 0.9057461198522639
id: 1476533 ndcg: 0.8851841304003693
id: 1382659 ndcg: 0.9601964393032381
id: 1402283 ndcg: 0.9751800258819728
id: 1055487 ndcg: 0.9999078563093102
id: 1932734 ndcg: 1.0
id: 1906915 ndcg: 0.841456369946024
id: 2269768 ndcg: 0.8327877201529084
id: 2871839 ndcg: 0.9998365018568336
id: 1888200 ndcg: 0.9999916316713874
id: 1339996 ndcg: 0.7690288658505715
id: 1283467 ndcg: 0.9693213044787752
id: 2286127 ndcg: 0.8616651623915044
id: 1880026 ndcg: 0.99999869514617
id: 1018854 ndcg: 0.9996363478861651
id: 2211893 ndcg: 0.8700339247478579
id: 1003740 ndcg: 0.9937841681236944
id: 1184689 ndcg: 0.9830160449957056
id: 1168414 ndcg: 0.9969563250482826
id: 1230447 ndcg: 0.9997801701498935
id: 1295915 ndcg: 0.8334285882258506
id: 2458162 ndcg: 0.999933958080956
id: 1002057 ndcg: 0.999997019227385
id: 2221636 ndcg: 0.9482002125825707
id: 2188785 ndcg: 1.0
id: 1114759 ndcg: 0.9812006280545397
id: 1072216 ndcg: 0.8190325650178403
id: 1459556 ndcg: 0.9131319663011996
id: 1818818 ndcg: 0.8814810429162904
id: 1671513 ndcg: 0.7810167204290405
id: 1803018 ndcg: 0.8560422801939959
id: 1079373 ndcg: 0.9884444567049311
id: 2851211 ndcg: 0.9999982535818007
id: 1127622 ndcg: 1.0
id: 2733661 ndcg: 0.9915539861224103
id: 1237534 ndcg: 0.9756848409492436
id: 1164201 ndcg: 1.0
id: 4114001 ndcg: 0.9985381750285764
id: 1240378 ndcg: 0.9825347924196881
id: 1985929 ndcg: 0.9999971086950982
id: 1379502 ndcg: 0.9829605902982504
id: 1380001 ndcg: 0.9965477838937866
id: 1352838 ndcg: 0.8354123124874621
id: 1604609 ndcg: 0.9997609819547558
id: 1227360 ndcg: 0.9638442275577636
id: 1167468 ndcg: 0.7954330368136383
id: 1419678 ndcg: 0.9778963968086193
id: 1120021 ndcg: 0.8707632816329202
id: 1083069 ndcg: 0.9996259202691968
id: 1668909 ndcg: 0.5910002849554069
id: 4243064 ndcg: 0.6507288313254515
id: 4390089 ndcg: 0.8675061865471169
id: 2718960 ndcg: 0.976007545167503
id: 1623509 ndcg: 0.9177109845770469
id: 2548540 ndcg: 0.959476136114354
id: 1409472 ndcg: 0.9924336276633544
id: 1012873 ndcg: 0.999951262658578
id: 1235021 ndcg: 0.9971991086193706
id: 2034976 ndcg: 0.8984631975606417
id: 1206987 ndcg: 0.9749601717633781
id: 3110829 ndcg: 0.5105993880202527
id: 1354970 ndcg: 0.6431825104321328
id: 2329743 ndcg: 1.0
id: 1216489 ndcg: 0.7174923850723418
id: 3565317 ndcg: 0.9962337855030754
id: 1128221 ndcg: 0.8651639999267419
id: 1462934 ndcg: 0.5833667147484943
id: 1664850 ndcg: 0.9870813794099901
id: 1104439 ndcg: 0.9998672575499205
id: 2116489 ndcg: 0.8812985804365983
id: 1418881 ndcg: 0.9967490761222485
id: 3265640 ndcg: 0.9986587394784759
id: 2866549 ndcg: 0.993961668239234
id: 1348695 ndcg: 0.9993437620709832
id: 1706717 ndcg: 0.9990910483035533
id: 1207216 ndcg: 0.9868198798914563
id: 1113171 ndcg: 0.6412413995945143
id: 43828497 ndcg: 0.7361707216441713
id: 1546732 ndcg: 0.971668021307101
id: 1945834 ndcg: 0.9214905991156227
id: 2279590 ndcg: 0.8351685027985134
id: 2114111 ndcg: 0.8931884204275587
id: 1149214 ndcg: 0.9988358332062803
id: 1233505 ndcg: 0.9876017407782414
id: 1454018 ndcg: 0.999003846368788
id: 2831524 ndcg: 0.9497856979407469
id: 1380928 ndcg: 0.9999726559052933
id: 1433566 ndcg: 0.6421235825835121
id: 1191238 ndcg: 1.0
id: 1968007 ndcg: 0.9998883977883689
id: 2737574 ndcg: 1.0
id: 1321067 ndcg: 0.9996029497083677
id: 1083177 ndcg: 0.9026026995899606
id: 1219568 ndcg: 0.8737093348298597
id: 2790785 ndcg: 0.8767873301568588
id: 2166874 ndcg: 0.9991363531507622
id: 1082140 ndcg: 0.8267393148668634
id: 1841712 ndcg: 0.9999234108362034
id: 1458339 ndcg: 0.9999974527331984
id: 2601165 ndcg: 0.9975587403468119
id: 4104534 ndcg: 0.8911967267917906
id: 1769763 ndcg: 0.99902817089185
id: 1078544 ndcg: 0.5697851818691614
id: 1917438 ndcg: 0.7905026862511858
id: 2158763 ndcg: 0.9999982987335699
id: 1064298 ndcg: 0.9999997478112579
id: 1216008 ndcg: 0.9806301905140078
id: 2297669 ndcg: 0.9997973448548892
id: 1443719 ndcg: 0.9999910352248522
id: 2272694 ndcg: 0.9992237586545265
id: 1514785 ndcg: 0.9996227279012294
id: 1302560 ndcg: 0.9934432736002288
id: 1056656 ndcg: 0.997404594181816
id: 1772323 ndcg: 0.7968220442516457
id: 1075526 ndcg: 0.9994510741583099
id: 1553185 ndcg: 0.9814143298348309
id: 1018267 ndcg: 0.8717463154029731
id: 2290115 ndcg: 0.999499889650549
id: 1683450 ndcg: 1.0
id: 1021985 ndcg: 0.9923750472851977
id: 1320395 ndcg: 0.9609349846945884
id: 1142233 ndcg: 0.9995866804172533
id: 1770641 ndcg: 0.8969048133236612
id: 1449801 ndcg: 0.8201198631241211
id: 2420609 ndcg: 0.9996449667084016
id: 1484972 ndcg: 0.8009205708556243
id: 1413054 ndcg: 0.9999801991717319
id: 2391083 ndcg: 0.9999974681941801
id: 42444500 ndcg: 0.9816111872765232
id: 1136972 ndcg: 0.9602280849077267
id: 1286081 ndcg: 0.8896666194627558
id: 1387637 ndcg: 0.8963609965640214
id: 1005928 ndcg: 0.7907535895555862
id: 1494167 ndcg: 0.9938367734329003
id: 1482639 ndcg: 0.8961592126395109
id: 1064685 ndcg: 1.0
id: 1178055 ndcg: 0.9555186606828493
id: 27900917 ndcg: 0.9909905261314497
id: 1032565 ndcg: 0.8068209305579375
id: 1024221 ndcg: 0.8719670265480468
id: 1157049 ndcg: 1.0
id: 1725202 ndcg: 0.7785067077076724
id: 1243811 ndcg: 0.9145740368623538
id: 2163599 ndcg: 1.0
id: 2188175 ndcg: 1.0
id: 1649784 ndcg: 0.26348119701112965
id: 45337884 ndcg: 0.9454518144281836
id: 2580197 ndcg: 0.9286982599231606
id: 1067865 ndcg: 0.9992958177605464
id: 2467021 ndcg: 1.0
id: 2272136 ndcg: 0.5769097021305736
id: 2057913 ndcg: 0.9308661952999523
id: 1623515 ndcg: 1.0
id: 2317472 ndcg: 0.7967664776211869
id: 2348857 ndcg: 0.7631868246546926
id: 1223030 ndcg: 0.9767235471195397
id: 1065754 ndcg: 0.9071114434685329
id: 3483674 ndcg: 0.795454581938286
id: 1956989 ndcg: 0.9987613905519364
id: 1135968 ndcg: 1.0
id: 1064727 ndcg: 0.9977255532371583
id: 1035406 ndcg: 0.9963978063703199
id: 3718831 ndcg: 0.9999997252213355
id: 1931533 ndcg: 0.8833129653373863
id: 3997105 ndcg: 0.8911445836635506
id: 1025084 ndcg: 0.969608602778701
id: 1691787 ndcg: 0.9985795819201225
id: 1823170 ndcg: 1.0
id: 1989241 ndcg: 0.884791791436046
id: 1385999 ndcg: 0.9505345247736355
id: 1562832 ndcg: 0.9990845580683227
id: 1935228 ndcg: 0.995146943450428
id: 1359809 ndcg: 0.9994556775756593
id: 1559766 ndcg: 0.9994827433743142
id: 1084392 ndcg: 0.7481523258963233
id: 1201356 ndcg: 0.9997505430896879
id: 1527440 ndcg: 0.7560328512947626
id: 1997615 ndcg: 0.5493428764483628
id: 2108133 ndcg: 1.0
id: 2221312 ndcg: 0.6203822396334459
id: 1140220 ndcg: 0.8594202416825067
id: 1464973 ndcg: 0.9893008492419973
id: 4783264 ndcg: 0.850682862290076
id: 2887092 ndcg: 0.8955364699332982
id: 1017464 ndcg: 0.827260825555583
id: 1158473 ndcg: 0.9764574846895463
id: 1256052 ndcg: 0.9997755716100756
id: 3835874 ndcg: 0.9795674532996008
id: 2788465 ndcg: 0.8606000717654535
id: 1096479 ndcg: 1.0
id: 2150874 ndcg: 0.8632135157364625
id: 3377711 ndcg: 0.9995616339359419
id: 4504171 ndcg: 0.9990011148967511
id: 1306299 ndcg: 0.9999972044612193
id: 1178038 ndcg: 0.9999965636064387
id: 1683981 ndcg: 0.8017708494543134
id: 1292181 ndcg: 0.9997233400862016
id: 1077373 ndcg: 0.6525573821246221
id: 2789379 ndcg: 1.0
id: 1828154 ndcg: 0.9191932857425839
id: 1793566 ndcg: 0.99935770394066
id: 2174195 ndcg: 0.9923677284340137
id: 2371597 ndcg: 0.9710192640802282
id: 1400056 ndcg: 0.6843216537078857
id: 1580264 ndcg: 0.8607069818790337
id: 1242406 ndcg: 0.8349355945979433
id: 1177306 ndcg: 0.999998498244149
id: 2226027 ndcg: 0.9764736824482418
id: 2398175 ndcg: 0.971275052842962
id: 2623840 ndcg: 0.8185242925065092
id: 1524768 ndcg: 0.17997320452520357
id: 4480774 ndcg: 0.9999962366975259
id: 45987769 ndcg: 1.0
id: 1796366 ndcg: 0.980399385446197
id: 1849659 ndcg: 0.9786320989614694
id: 2109890 ndcg: 0.9998571273132215
id: 1371393 ndcg: 0.7622443127525173
id: 1215272 ndcg: 0.9997228665959006
id: 2287590 ndcg: 0.9883676214418993
id: 3308317 ndcg: 0.9997280087247347
id: 1083626 ndcg: 0.8168511511137891
id: 1424151 ndcg: 0.9061384318756093
id: 2177125 ndcg: 0.854542829877184
id: 1233620 ndcg: 0.7716884017359752
id: 2864932 ndcg: 0.9995135536769868
id: 3576498 ndcg: 1.0
id: 4210333 ndcg: 0.846079017086303
id: 1099336 ndcg: 0.8906474965965377
id: 2085736 ndcg: 0.985451035761754
id: 2433862 ndcg: 0.8665902988939808
id: 1166776 ndcg: 0.9704602039298484
id: 2154163 ndcg: 0.56877348546877
id: 1197222 ndcg: 0.9972402871168984
id: 1222124 ndcg: 0.9700445592986748
id: 2362932 ndcg: 0.8174376693019925
id: 2470009 ndcg: 0.8653478926479106
id: 1636770 ndcg: 0.8773138264773709
id: 2650181 ndcg: 0.8404744949287306
id: 1162388 ndcg: 0.8540561512450745
id: 1210614 ndcg: 0.8212758445555444
id: 1870973 ndcg: 0.8899719958538861
id: 1433354 ndcg: 0.9423653975639198
id: 2282183 ndcg: 0.8521467584682804
id: 4020382 ndcg: 0.977892050139305
id: 1023392 ndcg: 0.9993792394954428
id: 2576305 ndcg: 0
id: 1332401 ndcg: 0.9998929041072777
id: 2531459 ndcg: 1.0
id: 2180956 ndcg: 0.9480596371220217
id: 1532168 ndcg: 0.9999142069875582
id: 2586116 ndcg: 0.6800326217312226
id: 2095456 ndcg: 0.9805666623424044
id: 2665497 ndcg: 0.8734978782319811
id: 1010302 ndcg: 1.0
id: 3029054 ndcg: 0.9969054277315553
id: 1089465 ndcg: 0.7813295076228874
id: 2090959 ndcg: 0.9385461277150124
id: 1781603 ndcg: 0.8835693281034738
id: 1524701 ndcg: 0.9995941209175975
id: 1601045 ndcg: 0.9968264153873554
id: 1507030 ndcg: 1.0
id: 1109192 ndcg: 0.9971847530970193
id: 1348926 ndcg: 0.8503074465623057
id: 1389804 ndcg: 1.0
id: 1000905 ndcg: 0.99991754166746
id: 1341263 ndcg: 0.9997594634789827
id: 1859205 ndcg: 0.9990986741305106
id: 1281917 ndcg: 0.6889890126631711
id: 1289379 ndcg: 0.9898958485103208
id: 2489892 ndcg: 0.9706869855506712
id: 2502133 ndcg: 0.9855364192097299
id: 1167773 ndcg: 0.9999979438727997
id: 1466340 ndcg: 0.9999390408958648
id: 1015534 ndcg: 0.8706635211070154
id: 1283582 ndcg: 0.742932491407952
id: 1791144 ndcg: 0.9998361521965419
id: 1218518 ndcg: 0.8722051486506491
id: 1984919 ndcg: 0.9768728192124452
id: 1090084 ndcg: 0.996797159842872
id: 1994511 ndcg: 0.9777545413453049
id: 1068205 ndcg: 0.6211868091252305
id: 1598721 ndcg: 0.20386797286864397
id: 1293083 ndcg: 0.8952028934960191
id: 4204517 ndcg: 0.8958403807645229
id: 2163500 ndcg: 0.958515111733809
id: 1252895 ndcg: 0.9986963624324044
id: 1456761 ndcg: 0.9977204995995703
id: 1076256 ndcg: 0.8142048466946186
id: 36855984 ndcg: 0.9991372132004515
id: 1738814 ndcg: 0.9937328611645115
id: 1569517 ndcg: 0.9990049142431289
id: 3441020 ndcg: 0.9994458056285165
id: 1600164 ndcg: 0.9860641936990766
id: 4459843 ndcg: 0.96278086558804
id: 3924193 ndcg: 0.9963422516724763
id: 1757555 ndcg: 0.7967461907107073
id: 1761738 ndcg: 0.8925067796550763
id: 2583379 ndcg: 0.884893315751577
id: 1190081 ndcg: 0.9501937569639258
id: 2402677 ndcg: 0.9999569135837736
id: 2056903 ndcg: 0.8911060725302191
id: 1789875 ndcg: 0.9127384652986613
id: 1473794 ndcg: 0.8703077373127175
id: 2046829 ndcg: 0.9849296942950392
id: 2363647 ndcg: 0.9999827168625126
id: 2060100 ndcg: 0.8912692301861771
id: 1017425 ndcg: 0.7236224193031876
id: 3146327 ndcg: 0.6283942214683884
id: 1043408 ndcg: 0.9913791123056009
id: 1428232 ndcg: 0.9996585613244605
id: 3196945 ndcg: 0.9955229739111711
id: 1447979 ndcg: 0.8368255718588845
id: 1065448 ndcg: 0.9875678063159764
id: 2456521 ndcg: 0.8706771227402046
id: 1086596 ndcg: 0.8148137763270478
id: 2367249 ndcg: 0.9732924321263102
id: 1515955 ndcg: 0.999828846858785
id: 1117271 ndcg: 0.9997055018342589
id: 1326807 ndcg: 0.9246509784967164
id: 1799854 ndcg: 0.9998783707191428
id: 1987990 ndcg: 0.9992351218486952
id: 1365772 ndcg: 0.8566004460644523
id: 1294931 ndcg: 0.9389847199729308
id: 10032764 ndcg: 0.8896259103200775
id: 4573673 ndcg: 0.9989611514787875
id: 1154663 ndcg: 0.9543887383009813
id: 1268461 ndcg: 0.8138805201982996
id: 4266578 ndcg: 0.9532221024811695
id: 1101456 ndcg: 1.0
id: 3494904 ndcg: 0.9792051161162048
id: 1681567 ndcg: 0.9843025417915667
id: 1286613 ndcg: 0.16592658312552244
id: 1054440 ndcg: 0.9771731510798548
id: 1658018 ndcg: 0.8768207854061193
id: 4187528 ndcg: 0.8856083092471969
id: 3275026 ndcg: 0.8103341405433728
id: 3257743 ndcg: 0.9502253743300484
id: 1553487 ndcg: 0.9988463360817207
id: 4321056 ndcg: 0.9844752955731418
id: 2380813 ndcg: 0.9939528629673611
id: 2621589 ndcg: 0.9828513531713277
id: 1024471 ndcg: 1.0
id: 1247727 ndcg: 0.7434648583499501
id: 2161685 ndcg: 1.0
id: 1142799 ndcg: 0.9999945850060216
id: 1116761 ndcg: 1.0
id: 1885452 ndcg: 0.8487505882608603
id: 1233734 ndcg: 0.7702181015279022
id: 1210604 ndcg: 0.8199461964978638
id: 4584061 ndcg: 0.9999761682637298
id: 1311864 ndcg: 0.8977922098052624
id: 4344558 ndcg: 0
id: 1980404 ndcg: 0.969064150301607
id: 1120768 ndcg: 1.0
id: 1507714 ndcg: 0.9994962160505928
id: 1042606 ndcg: 0.9997431845694547
id: 1531287 ndcg: 0.9593196380486959
id: 1101697 ndcg: 0.8798792167846652
id: 4058423 ndcg: 0.983045645889995
id: 1462744 ndcg: 0.8676300471055587
id: 1391511 ndcg: 0.8424485959972907
id: 1128567 ndcg: 0.977612041176148
id: 2185606 ndcg: 0.8971289707028223
id: 1324439 ndcg: 0.8922476521594424
id: 2458731 ndcg: 0.9995094796081735
id: 1381120 ndcg: 0.8881916007064159
id: 2320897 ndcg: 0.9951686915101305
id: 1404062 ndcg: 0.8654118402525589
id: 2187640 ndcg: 0.8457387522780534
id: 2478751 ndcg: 0.8192227990759109
id: 1184811 ndcg: 0.8657537826233894
id: 1265100 ndcg: 0.999977728540358
id: 1900220 ndcg: 1.0
id: 1143289 ndcg: 0.9928084419054958
id: 1564473 ndcg: 0.7804096375808017
id: 1907423 ndcg: 0.8226437601909296
id: 1417075 ndcg: 1.0
id: 4328538 ndcg: 0.8700671196759103
id: 2126601 ndcg: 0.999993624925692
id: 1462422 ndcg: 0.8697716110751701
id: 3872317 ndcg: 0.9996332491671893
id: 1117550 ndcg: 1.0
id: 1224197 ndcg: 0.997509037577185
id: 1267105 ndcg: 0.9934962654918053
id: 1416960 ndcg: 0.8891246437565286
id: 1013185 ndcg: 0.8196982318026874
id: 1308599 ndcg: 0.8408985349643936
id: 1486607 ndcg: 0.9998421528406659
id: 1264887 ndcg: 0.9595782409293415
id: 1321096 ndcg: 0.8705254067657446
id: 1191558 ndcg: 0.9934176849279129
id: 1253159 ndcg: 0.8548514227202444
id: 1231114 ndcg: 0.6694344590181371
id: 4419732 ndcg: 0.6471595143162588
id: 1127772 ndcg: 0.9999992233186988
id: 1145553 ndcg: 0.8275725850726707
id: 1184528 ndcg: 0.9322929681739419
id: 1229607 ndcg: 0.9994992423464437
id: 4432234 ndcg: 0.9468588446202936
id: 1256388 ndcg: 0.8295801662442269
id: 1120366 ndcg: 0.9840468944594827
id: 1334746 ndcg: 0.9621092612528676
id: 1087393 ndcg: 0.4820745476983899
id: 1080398 ndcg: 1.0
id: 2312968 ndcg: 0.8709734161467242
id: 4869982 ndcg: 0.9905255084863862
id: 27612232 ndcg: 0.9999123546926585
id: 1247621 ndcg: 0.9580813423823858
id: 2317706 ndcg: 0.8567571354332075
id: 1371498 ndcg: 0.8890951864997563
id: 2007121 ndcg: 0.972110718892401
id: 3310238 ndcg: 0.9652455690061258
id: 1163240 ndcg: 0.18316925091363362
id: 1966717 ndcg: 1.0
id: 1458288 ndcg: 1.0
id: 1468297 ndcg: 0.9221862756535766
id: 1003080 ndcg: 0.82082174942931
id: 1684291 ndcg: 1.0
id: 1415418 ndcg: 0.9231377858455759
id: 1611177 ndcg: 0.8881936182532606
id: 1717315 ndcg: 1.0
id: 1022965 ndcg: 0.9679631876136907
id: 1999864 ndcg: 0.928520481285707
id: 37829070 ndcg: 0.7879677681225813
id: 2195332 ndcg: 0.8911083934562174
id: 2923991 ndcg: 0.992651144880669
id: 1496247 ndcg: 0.8195249705850437
id: 1048262 ndcg: 0.9925850613521926
id: 1133770 ndcg: 0.9999762371571713
id: 1125189 ndcg: 0.942306090219832
id: 1216758 ndcg: 0.9998585914902111
id: 1665012 ndcg: 0.8881811328467084
id: 1997642 ndcg: 0.9745838533355241
id: 1212789 ndcg: 0.9962287358917868
id: 1275416 ndcg: 0.9999950934348621
id: 1301150 ndcg: 1.0
id: 1311301 ndcg: 0.9016645329599852
id: 1215476 ndcg: 0.7598627399393623
id: 3106355 ndcg: 1.0
id: 2244978 ndcg: 0.990333413761957
id: 1243741 ndcg: 0.9957366969257365
id: 1004613 ndcg: 0.8871545228859871
id: 48190738 ndcg: 0
id: 1435341 ndcg: 0.7984675365077335
id: 2532481 ndcg: 1.0
id: 1201152 ndcg: 0.8251652711807531
id: 1551538 ndcg: 0.8561985665523985
id: 2254558 ndcg: 0.9726004354643455
id: 3298656 ndcg: 0.9048530563255431
id: 1923547 ndcg: 0.873691996415699
id: 2192275 ndcg: 0.9924196929070203
id: 1593734 ndcg: 0.44934327597036994
id: 2283414 ndcg: 0.9921296949116247
id: 2614823 ndcg: 0.8873591240280336
id: 1943775 ndcg: 1.0
id: 2501452 ndcg: 0.7935916038788693
id: 1248504 ndcg: 0.9714231827946723
id: 1588635 ndcg: 0.8802546727780476
id: 1032989 ndcg: 0.9585659400928109
id: 1381050 ndcg: 0.8448424652404601
id: 2318815 ndcg: 0.7957398342773722
id: 2728851 ndcg: 0.860091908593631
id: 1994744 ndcg: 0.8463711446837512
id: 2155349 ndcg: 0.9760587043222488
id: 1106259 ndcg: 0.9993232442746404
id: 1073676 ndcg: 0.6228034276894238
id: 3756896 ndcg: 1.0
id: 2423171 ndcg: 0.6356578325530482
id: 1635105 ndcg: 0.8929848269120391
id: 1407245 ndcg: 0.8950814551755311
id: 1067265 ndcg: 0.9784245679867986
id: 1840823 ndcg: 0.9996244817960225
id: 1198902 ndcg: 1.0
id: 1322790 ndcg: 0.8197340320870203
id: 2164427 ndcg: 0.8500362219230343
id: 1391951 ndcg: 0.9871170444158556
id: 2447160 ndcg: 0.8993399243026599
id: 1384560 ndcg: 0.9839056234429677
id: 2504060 ndcg: 0.9999826024468658
id: 1464407 ndcg: 0.9997918234465097
id: 2672224 ndcg: 0.9611597619873088
id: 1607518 ndcg: 0.9999922745297788
id: 1095381 ndcg: 0.9999878329854601
id: 2473833 ndcg: 0.8695953890190122
id: 1043499 ndcg: 0.9960539213830905
id: 3659732 ndcg: 0.9956473746022876
id: 1763584 ndcg: 0.8909311365363556
id: 1113569 ndcg: 0.8466590293789136
id: 3571728 ndcg: 0.9999704732663263
id: 1242190 ndcg: 0.7311118564384862
id: 44605628 ndcg: 0.9996891127200644
id: 1849412 ndcg: 0.87582763351821
id: 1444698 ndcg: 0.9998315438704786
id: 1590891 ndcg: 0.8249960622130889
id: 1325628 ndcg: 0.891956861799545
id: 1793602 ndcg: 0.889312919197926
id: 1674014 ndcg: 0.8038990638870899
id: 1028845 ndcg: 0.9999508910182978
id: 1117043 ndcg: 0.9598108100499457
id: 2035973 ndcg: 0.9561136841136422
id: 1902672 ndcg: 0.9988871365761662
id: 2133129 ndcg: 0.9999998128576546
id: 1115174 ndcg: 0.9998386145459657
id: 1049746 ndcg: 1.0
id: 1707961 ndcg: 0.47381489358184814
id: 1462547 ndcg: 0.847443869001291
id: 1053836 ndcg: 1.0
id: 1477408 ndcg: 0.8398613968111568
id: 3507246 ndcg: 0.9988281790993969
id: 1431372 ndcg: 0.8679637791172665
id: 2532423 ndcg: 0.9317368372892133
id: 2931632 ndcg: 0.9578115410068364
id: 1009991 ndcg: 0.9130894974843612
id: 2700495 ndcg: 0.7841687142438417
id: 1091489 ndcg: 0.975884552723522
id: 2129120 ndcg: 0.9996608854718639
id: 1337199 ndcg: 0.9993642751239985
id: 1509119 ndcg: 0.9953418145851743
id: 1468293 ndcg: 0.42249253535790904
id: 1146587 ndcg: 0.9999879270868477
id: 1229156 ndcg: 0.951107316677793
id: 1453980 ndcg: 0.976259008591658
id: 1156490 ndcg: 0.8863100483170759
id: 2352275 ndcg: 0.9684389169540181
id: 2603819 ndcg: 0.9747288001911607
id: 2037426 ndcg: 0.8644694689155966
id: 1386404 ndcg: 0.8268802896925131
id: 1220523 ndcg: 0.9998147292955166
id: 1577739 ndcg: 0.9796344514249536
id: 1182135 ndcg: 0.970323904687301
id: 1504223 ndcg: 0.9444794302303822
id: 1085884 ndcg: 0.9993755669327833
id: 2126832 ndcg: 0.8739103870529346
id: 1468660 ndcg: 0.9984973722203858

```













