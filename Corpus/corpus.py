import jieba
from IR.Corpus.config import Stopwords, Punctutation, movie_parse_data_path, book_parse_data_path, pre_load_book_corpus_path, pre_load_movie_corpus_path
import sys
import json, pickle
import os
sys.path.append("D:\\Savefiles\\Projects\\Python\\IR")


# 语料库类(包含token2id,id2token以及倒排索引，均以字典为数据结构)
class Corpus:

    def __init__(self, ctype, preload=True):
        self.token2id = dict()
        self.id2token = dict()
        self.corpus_passage_list = []
        self.invert_indice = dict()
        self.type = ctype
        self.preload = preload
        self._prepare()



    def add(self, text_id, text=None, tokens=None):
        all_tokens = []
        if self.corpus_passage_list and text_id in self.corpus_passage_list:
            if not tokens:
                return
            else:
                all_tokens.extend(tokens)
                all_tokens = Corpus.removeStopWords(all_tokens)
                self._updateTokens(all_tokens)
                token_ids = [self.token2id[token] for token in all_tokens]
                self._updateInvertIndice(text_id, token_ids)
        else:
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

            self.corpus_passage_list.append(text_id)

    def save(self):
        if self.type == 'movie':
            with open(pre_load_movie_corpus_path,"wb") as f:
                pickle.dump((self.token2id, self.id2token, self.invert_indice, self.corpus_passage_list), f)
        elif self.type == 'book':
            with open(pre_load_book_corpus_path,"wb") as f:
                pickle.dump((self.token2id, self.id2token, self.invert_indice, self.corpus_passage_list), f)

    # TODO 暂时只加入了内容简介的内容进入语料库，电影类型(或者其他的内容模仿)内容简介的方式添加进语料库,对于添加进语料库的文档,
    #      text仅支持添加一次(默认第一次需要添加text，否则后续只能以添加tokens形式添加)，但可以tokens形式添加新的词项进入
    #      语料库(具体见add函数)，以此方式防止文章内容重复添加并同时支持对文章内容的增量添加

    def _prepare(self):
        if self.type == 'movie':
            if self.preload:
                if os.path.exists(pre_load_movie_corpus_path):
                    with open(pre_load_movie_corpus_path,"rb") as f:
                        self.token2id, self.id2token, self.invert_indice, self.corpus_passage_list = pickle.load(f)
                else:
                    print(pre_load_movie_corpus_path+" not found!")
                    sys.exit(-1)
                return
            with open(movie_parse_data_path, "r") as f:
                movies = json.load(f)
                for key, value in movies.items():
                    self.add(key, value)
        elif self.type == 'book':
            if self.preload:
                if os.path.exists(pre_load_book_corpus_path):
                    with open(pre_load_book_corpus_path,"rb") as f:
                        self.token2id,self.id2token,self.invert_indice, self.corpus_passage_list = pickle.load(f)
                else:
                    print(pre_load_book_corpus_path+" not found!")
                    sys.exit(-1)
                return
            with open(book_parse_data_path, "r") as f:
                books = json.load(f)
                for key, value in books.items():
                    self.add(key, value)



    def _updateTokens(self, tokens):
        for token in tokens:
            if token in self.token2id:
                continue
            tid = len(self.token2id)
            self.token2id[token] = str(tid)
            self.id2token[str(tid)] = token

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















