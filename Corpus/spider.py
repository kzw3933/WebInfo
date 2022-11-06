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

