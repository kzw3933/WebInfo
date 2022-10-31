## 实验1 信息获取与检索分析

小组成员：

柯志伟  PB20061338
左丰瑞  PB20061337
刘一鸣  PB20050973

---

#### 实验题目

```
信息获取与检索分析
```
#### 实验要求

```
针对给定的电影、书籍 ID，爬取其豆瓣主页，并解析其基本信息。以下图电影
数据为例，其主页包含导演编剧等基本信息、剧情简介、演职员表、相关视频图片、
获奖情况等

- 对于电影数据，至少爬取其基本信息、剧情简介、演职员表
- 对于书籍数据，至少爬取其基本信息、内容简介、作者简介
- 爬虫方式不限，网页爬取和 API 爬取两种方式都可，介绍使用的爬虫方式工具
- 针对所选取的爬虫方式，发现并分析平台的反爬措施，并介绍采用的应对策略
- 针对所选取的爬虫方式，使用不同的内容解析方法，并提交所获取的数据
- 该阶段无评测指标要求，在实验报告中说明爬虫（反爬）策略和解析方法即可

```

#### 实验过程

1. 爬虫策略及反爬机制

```
爬虫策略:

使用实验提供的资源列表,通过python的requests库，从豆瓣逐一请求资源并下载到本地

反爬机制:

本次实验中发现豆瓣反爬利用了以下信息：
- 请求的user-agent信息
- cookies信息
- referer信息
- 请求速度进行反爬

分别采用以下方式反反爬：
- 添加浏览器的user-agent头信息
- 添加登录豆瓣账号后的cookies信息
- 针对每个请求设置上一个网页的网址为referer
- 建立代理池进行

```




代码如下：
```python
class Spider():
    def __init__(self,downloader,parsers,idfile):
        self.headers = {
            "Referer":"https://movie.douban.com/",
            "Cookie":'ll="118183"; bid=5jNr8J7dsPc; __gads=ID=342f2d303d102c2c-22ad8273a6d6009b:T=1663595607:RT=1663595607:S=ALNI_MaI0u9Z2aUh9gVHH92DiqrhOOBkdw; \
            gr_user_id=a1529fdf-2805-4880-90d6-2f140097a75c; viewed="1084336_1046265_1046165"; _ \
            ga=GA1.1.339440865.1663597182; _ga_RXNMP372GL=GS1.1.1663686412.2.0.1663686412.60.0.0; ap_v=0,6.0; \
            __utmc=30149280; __gpi=UID=000009cec03f4993:T=1663595607:RT=1663718795:S=ALNI_MZ7Hkf2bua9XofJeggyBg-L8IN8xw; \
            dbcl2="224468347:awLw+ZstjdM"; ck=7yd2; __utma=30149280.339440865.1663597182.1663718795.1663721179.5; __utmb=30149280.0.10.1663721179;\
                __utmz=30149280.1663721179.5.2.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; push_noty_num=0; push_doumail_num=0"',
            "user-agent":"Mozilla / 5.0(X11;Linux x86_64) AppleWebKit /537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari / 537.36"
            }
        self.proxies = ["http://222.74.73.202:42055",
                        "http://122.9.101.6:8888",
                        "http://61.216.156.222:60808",
                        "http://150.109.32.166:80",
                        "http://183.247.199.215:30001",
                        "http://120.194.55.139:6969",
                        "http://120.194.55.139:6969"]

        self.downloader = downloader(self.headers,self.proxies,idfile)
        self.parsers = parsers

    def download(self):
        self.downloader()
    
    def parse(self,detail,save_to_json,parse_file):
        for parser in self.parsers:
            parser(detail,save_to_json,parse_file)


def movie_downloader(headers,proxies,moviesIdFile):
    movieBaseUrl = "https://movie.douban.com/subject/"
    movieHtmlPath="./assets/Movies/"
    actorsHtmlPath="./assets/MovieActors/"
    ids = []
    with open(moviesIdFile,"r") as f:
        ids = [id.strip('\n') for id in f.readlines()]
    def downloader():
        num = 0
        for id in ids:
            proxy = {"http": random.choice(proxies)}
            url =  movieBaseUrl + id + "/"
            response = requests.get(url=url,headers=headers,proxies=proxy)
            page = response.text
            with open(movieHtmlPath+str(id)+".html","w") as b:
                b.write(page)
                num = num+1
                print("movie序号: "+"\033[31m"+str(num)+"\033[0m"+" ID: "+"\033[31m"+str(id)+"\033[0m"+"------>ok") 
                headers["Referer"] = url
        num = 0
        for id in ids:
            proxy = {"http": random.choice(proxies)}
            headers["Referer"] = movieBaseUrl + id + "/"
            url =  movieBaseUrl + id + "/"+"celebrities"
            response = requests.get(url=url,headers=headers,proxies=proxy)
            page = response.text
            with open(actorsHtmlPath+str(id)+".html","w") as b:
                b.write(page)
                num = num+1
                print("movie序号: "+"\033[31m"+str(num)+"\033[0m"+" ID: "+"\033[31m"+str(id)+"\033[0m"+"------>ok") 
                
    return downloader

def book_downloader(headers,proxies,booksIdFile):
    bookBaseUrl = "https://book.douban.com/subject/"
    bookHtmlPath="./assets/Books/"
    ids = []
    with open(booksIdFile,"r") as f:
        ids = [id.strip('\n') for id in f.readlines()]
    def downloader():
        num = 0
        for id in ids:
            proxy = {"http": random.choice(proxies)}
            url =  bookBaseUrl+ id + "/"
            response = requests.get(url=url,headers=headers,proxies=proxy)
            page = response.text
            with open(bookHtmlPath+str(id)+".html","w") as b:
                b.write(page)
                num = num+1
                print("book序号: "+"\033[31m"+str(num)+"\033[0m"+" ID: "+"\033[31m"+str(id)+"\033[0m"+"------>ok") 
                headers["Referer"] = url
    return downloader

```


2. 解析方法
```
针对电影(基本信息、剧情简介、演职员表),图书(基本信息、内容简介、作者简介)，分别使用
beautifulsoup设置出元素的选择器并获取出其信息，对于特殊的情况使用re模块进一步解析

```
代码如下：

```python

## 基本信息(作者，编剧，主演，类型，制片国家，上映时间，片长，别名，IMDb)
def movie_baseinfo_parser(detail=True,save_to_json=True,parse_file=None):
    movieHtmlPath="./assets/Movies/"
    movieJsonPath = "./assets/movies_baseinfo.json"
    num = 0
    allmovies = {}
    files = []
    infos = None
    if not parse_file:
        files = os.listdir(movieHtmlPath)
    else:
        files = [parse_file+".html"]
    for file in files:
        with open(movieHtmlPath+file,"r") as f:
            movie_id = file.split(".")[0]
            soup = BeautifulSoup(f.read(),"html.parser") 
            info = soup.find(attrs={"id":"info"})
            if(info):
                infos = info.text.strip("\n").split("\n")
                if(detail):
                    print("baseinfo:(划分前)",end="")
                    print(infos) 
                temps = []
                for i in infos:
                    i = i.split(":")
                    if(len(i) == 2):
                        temps.append(i[0])
                        temps.append(i[1])
                    else :
                        temps.append(i[0])
                        temps.append(":".join(i[1:]))
                    infos = [i.strip() for i in temps if(i.strip())]
                    keys =[infos[i] for i in range(len(infos)) if i&0b1 == 0]
                    values = [infos[i] for i in range(len(infos)) if i&0b1 ==1]
                    infos = dict(zip(keys,values))
                allmovies[movie_id] = infos             
            else :
                allmovies[movie_id] = None
            if(detail):
                print("baseinfo:(划分后)",end="")
                print(infos) 
            num = num+1
            print("movie序号: "+"\033[31m"+str(num)+"\033[0m"+" ID: "+"\033[31m"+str(movie_id)+"\033[0m"+"------>ok")
    if(save_to_json and not parse_file):
        with open(movieJsonPath,"w") as f:
                json.dump(allmovies,f)


## 内容简介
def movie_synopsis_parser(detail=True,save_to_json=True,parse_file=None):
    movieHtmlPath="./assets/Movies/"
    movieJsonPath = "./assets/movies_synopsis.json"
    num = 0
    allmovies = {}
    files = []
    if not parse_file:
        files = os.listdir(movieHtmlPath)
    else:
        files = [parse_file+".html"]
    for file in files:
        with open(movieHtmlPath+file,"r") as f:
            movie_id = file.split(".")[0]
            soup = BeautifulSoup(f.read(),"html.parser")
            synopsis = soup.find(attrs={"id":"link-report"})
            temps = None
            if synopsis :
                temps = synopsis.find(attrs={"property":"v:summary"}).text
                temps = re.search(r'.*\s+(.*)\s+.*', temps)
                if (temps): 
                    temps = temps.groups()[0]
            synopsis = temps
            allmovies[movie_id] = synopsis
            if(detail):
                print("synopsis:",end="")
                print(synopsis)
            num = num+1
            print("movie序号: "+"\033[31m"+str(num)+"\033[0m"+" ID: "+"\033[31m"+str(movie_id)+"\033[0m"+"------>ok")
    if(save_to_json and not parse_file):
        with open(movieJsonPath,"w") as f:
                json.dump(allmovies,f)


## 演员列表
def movie_actor_parser(detail=True,save_to_json=True,parse_file=None):
    actorsHtmlPath="./assets/MovieActors/"
    movieJsonPath = "./assets/movies_actors.json"
    num = 0
    allmovies = {}
    files = []
    if not parse_file:
        files = os.listdir(actorsHtmlPath)
    else:
        files = [parse_file+".html"]
    for file in files:
        with open(actorsHtmlPath+file,"r") as f:
            movie_id = file.split(".")[0]
            soup = BeautifulSoup(f.read(),"html.parser")
            actorsList = []
            for actor in soup.find_all(name="div",attrs={"class","info"}):
                name = actor.find(attrs={"class","name"})
                role = actor.find(attrs={"class","role"})
                if(role):
                    actorsList.append(name.text+"-->"+role.text)
            allmovies[movie_id] = actorsList
            if(detail):
                print("actors:",end="")
                print(actorsList)
            num = num +1
            print("movie序号: "+"\033[31m"+str(num)+"\033[0m"+" ID: "+"\033[31m"+str(movie_id)+"\033[0m"+"------>ok")
    if(save_to_json and not parse_file):
        with open(movieJsonPath,"w") as f:
                json.dump(allmovies,f)


# 基本信息(作者，出版社，原作名，译者，出版年，页数，定价，装帧，丛书,ISBN)
def book_baseinfo_parser(detail=True,save_to_json=True,parse_file=None):
    bookHtmlPath="./assets/Books/"
    bookJsonPath = "./assets/books_baseinfo.json"
    allbooks = {}
    num = 0
    files = []
    if not parse_file:
        files = os.listdir(bookHtmlPath)
    else:
        files = [parse_file+".html"]
    for file in files:
        with open(bookHtmlPath+file,"r") as f:
            book_id = file.split(".")[0]
            soup = BeautifulSoup(f.read(),"html.parser")
            info = soup.find(attrs={"id":"info"})
            keys = []
            values = []
            infos = None
            combine = False
            if(info):
                infos = info.text.strip("\n").split("\n")
                infos = [i.replace("\n","").replace("\xa0"," ").strip() for i in infos if i.replace("\n","").replace("\xa0"," ").strip()]
                if(detail):
                    print("baseinfo:(划分前)",end="")
                    print(infos) 
                temps = []
                for i in infos:
                    temp = i.split(":")
                    if(len(temp)>2):
                        temps.append(temp[0])
                        temps.append(":".join(temp[1:]))
                    elif(len(temp)==2):
                        temps.append(temp[0])
                        temps.append(temp[1])
                    else:
                        temps.append(temp[0])
                infos = [i.strip() for i in temps if i.strip()]
                for i in infos:
                    if(combine):
                        values[-1] = values[-1] + i
                        combine = False
                    elif("]" in i and len(i) == i.index("]")+1):
                        values.append(i)
                        combine = True
                    elif("/" == i):
                        values[-1] = values[-1] + ' '
                        combine = True
                    elif(len(keys) == len(values)):
                        keys.append(i)
                        combine = False
                    else:
                        values.append(i)
                        combine = False
                keys = [key.strip("/").strip() for key in keys]
                values = [value.strip("/").strip() for value in values]
                infos = dict(zip(keys,values))
                allbooks[book_id] = infos
            else:
                infos = None
                allbooks[book_id] = infos
            if(detail):
                print("baseinfo(划分后):",end="")
                print(infos)     
            num = num +1
            print("book序号: "+"\033[31m"+str(num)+"\033[0m"+" ID: "+"\033[31m"+str(book_id)+"\033[0m"+"------>ok")

    if(save_to_json and not parse_file):
        with open(bookJsonPath,"w") as f:
            json.dump(allbooks,f)          

def book_synopsis_parser(detail=True,save_to_json=True,parse_file=None):
    bookHtmlPath="./assets/Books/"
    bookJsonPath = "./assets/books_synopsis.json"
    allbooks = {}
    num = 0
    files = []
    if not parse_file:
        files = os.listdir(bookHtmlPath)
    else:
        files = [parse_file+".html"]
    for file in files:
        with open(bookHtmlPath+file,"r") as f:
            book_id = file.split(".")[0]
            soup = BeautifulSoup(f.read(),"html.parser")
            synopsis= soup.find(attrs={"id":"link-report"})
            temps = None
            if(synopsis):
                temps = ""
                for p in synopsis.find(attrs={"class":"intro"}).find_all(name="p"):
                    temps = temps + p.text.strip().strip('\n').strip() + "\n"     
            synopsis = temps
            allbooks[book_id] = synopsis
            if(detail):
                print("synopsis:",end="")
                print(synopsis)
            num = num +1
            print("book序号: "+"\033[31m"+str(num)+"\033[0m"+" ID: "+"\033[31m"+str(book_id)+"\033[0m"+"------>ok")
            
    if(save_to_json and not parse_file):
        with open(bookJsonPath,"w") as f:
            json.dump(allbooks,f)  
               
                    
def book_writer_parser(detail=True,save_to_json=True,parse_file=None):
    bookHtmlPath="./assets/Books/"
    bookJsonPath = "./assets/books_writer.json"
    allbooks = {}
    num = 0
    files = []
    if not parse_file:
        files = os.listdir(bookHtmlPath)
    else:
        files = [parse_file+".html"]
    for file in files:
        with open(bookHtmlPath+file,"r") as f:
            contents = f.read()
            book_id = file.split(".")[0]
            soup = BeautifulSoup(contents,"html.parser")
            writer_exist = re.search("作者简介",contents)
            temps = None
            if(writer_exist):
                temps = soup.find_all(attrs={"class":"intro"})
                if(temps):
                    temps = temps[-1].find(name="p").text
            writer = temps
            allbooks[book_id] = writer
            if(detail):
                print("作者简介:",end="")
                print(writer)
            num = num +1
            print("book序号: "+"\033[31m"+str(num)+"\033[0m"+" ID: "+"\033[31m"+str(book_id)+"\033[0m"+"------>ok")
            
    if(save_to_json and not parse_file):
        with open(bookJsonPath,"w") as f:
            json.dump(allbooks,f)  

```

3. 信息保存
```
本次实验将解析的信息先保存到json文件中，后又保存到xls文件中
```

代码如下：
```python

def movies_to_xls():
    moviesIdFile = "./assets/Movie_id.txt"
    moviesFile = ["./assets/movies_baseinfo.json","./assets/movies_synopsis.json","./assets/movies_actors.json"]
    book = xlwt.Workbook(encoding="utf-8",style_compression=0)
    sheet = book.add_sheet('豆瓣电影',cell_overwrite_ok= True)
    col_movie = ("ID","导演","编剧","主演","类型","制片国家/地区","语言","上映日期","片长","又名","IMDb","首播","季数","集数","单集片长","官方网站/小站","剧情简介","演职员表")
    find_movie_pos={"ID":0,"导演":1,"编剧":2,"主演":3,"类型":4,"制片国家/地区":5,"语言":6,"上映日期":7,"片长":8,"又名":9,"IMDb":10,"首播":11,"季数":12,"集数":13,"单集片长":14,"官方网站":15,"官方小站":15,"剧情简介":16,"演职员表":17}
    unuseList=[]
    for i in range(0, 18):
        sheet.write(0, i, col_movie[i])
    def save_movie_data(info,value,line):
        sheet.write(line + 1, find_movie_pos[info], value)
    with open(moviesIdFile,"r") as b:             
        num = 0
        for line in b.readlines():
            line = line.strip('\n')
            f1 = open(moviesFile[0], "r")
            f2 = open(moviesFile[1], "r")
            f3 = open(moviesFile[2], "r")
            baseinfo = json.load(f1)
            synopsis = json.load(f2)
            actors = json.load(f3)

            if(baseinfo[line]):
                for key,value in baseinfo[line].items():
                    save_movie_data(key, value, num)
            else:
                unuseList.append(line+"\n")
                continue
            save_movie_data('剧情简介', synopsis[line], num)
            save_movie_data('演职员表', actors[line], num)
            save_movie_data('ID',line,num)
            num += 1
            print(str(num)+" is ok!")
    book.save('豆瓣电影.xls')
    if unuseList:
        with open("./assets/movie_id.txt","w") as f:
            for line in unuseList:
                f.write(line)
    else:
        os.remove("./assets/movie_id.txt")

def books_to_xls():
    booksIdFile = "./assets/Book_id.txt"
    booksFile = ["./assets/books_baseinfo.json","./assets/books_synopsis.json","./assets/books_writer.json"]
    book = xlwt.Workbook(encoding="utf-8",style_compression=0)
    sheet = book.add_sheet('豆瓣书籍',cell_overwrite_ok= True)
    col_book =("ID","作者","出版社","原作名","副标题","译者","校注","出版年","统一书号","页数","定价","装帧","丛书","ISBN","出品方","内容简介","作者简介")
    find_book_pos={"ID":0,"作者":1,"出版社":2,"原作名":3,"副标题":4,"译者":5,"校注":6,"出版年":7,"统一书号":8,"页数":9,"定价":10,"装帧":11,"丛书":11,"ISBN":13,"出品方":14,"内容简介":15,"作者简介":16}
    unuseList=[]
    for i in range(0, 17):
        sheet.write(0, i, col_book[i])
    def save_book_data(info,value,line):
        if info in find_book_pos.keys():
            sheet.write(line + 1, find_book_pos[info], value)
    with open(booksIdFile,"r") as b:
        num = 0
        for line in b.readlines():
            line = line.strip('\n')
            f1 = open(booksFile[0], "r")
            f2 = open(booksFile[1], "r")
            f3 = open(booksFile[2], "r")
            baseinfo = json.load(f1) 
            synopsis = json.load(f2) 
            writer = json.load(f3)
            if(baseinfo[line]):
                for key,value in baseinfo[line].items():
                    save_book_data(key, value, num)
            else:
                unuseList.append(line+"\n")
                continue
            save_book_data('内容简介', synopsis[line], num)
            save_book_data('作者简介', writer[line], num)
            save_book_data('ID',line,num)
            num += 1
            print(str(num)+" is ok!")
    book.save('豆瓣书籍.xls')

    if unuseList:
        with open("./assets/book_id.txt","w") as f:
            for line in unuseList:
                f.write(line)
    else:
        os.remove("./assets/book_id.txt")

```



