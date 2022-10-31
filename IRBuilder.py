from IR.Corpus.corpus import Corpus
from IR.Search.boolenSearch import BoolenSearcher

class IRBuilder:

    def __init__(self):
        self.movie_corpus = Corpus(ctype="movie", preload=True)
        self.book_corpus = Corpus(ctype="book", preload=True)

        self.movie_searcher = BoolenSearcher(self.movie_corpus)
        self.book_searcher = BoolenSearcher(self.book_corpus)



if __name__ == '__main__':

    IR = IRBuilder()

    print("\033[33m"+ "*"*20 + "欢迎进入布尔检索系统"+"*"*20 + "\033[0m")
    while True:
        type = input("input your query type" +"\033[32m" + " [book or movie ]"+ "\033[0m"+ ": ")
        if type != "movie" and type != "book":
            continue

        query = input("input your query boolen expression" + "\033[32m" + " [ eg a and (b or c) ]"+ "\033[0m"+": ")
        result = None

        if type == 'movie':
            result = IR.movie_searcher.run(query)
        else:
            result = IR.movie_searcher.run(query)

        if result:
            print("The search results are in following: ")
            print_str = "\t"
            line_count = 0
            for i in result:
                print_str += i
                print_str += '\t' if line_count < 5 else '\n\t'
                line_count = 0 if line_count == 5 else line_count+1
            print("\033[34m"+print_str+"\033[0m")

        else:
            print("Can't found the related content in system!")

        next = input("continue(Y/n)? ")
        if next == 'n' or next == 'N':
            break














