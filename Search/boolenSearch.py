
# 布尔搜索类: 对输入的语料库(包含token2id,id2token,invert_indice属性)以及布尔表达式字符串实现布尔检索


# TODO 由于目前实现的布尔表达式解析模块与布尔检索的优化密切相关(如果加入not，可以实现但如果要支持多级复杂的not表达式较为复杂(如果想支持用户各种奇怪的输入，
#      也许可以构建一个语法树做语法制导的翻译呢),需要修改较多的逻辑，同时可能实现过于复杂导致debug困难，复杂表达式比如
#  a and not (b or c and not (d)))
#  a and not not (b and c)
#  a and not not (((b)))
#  not (a or b) and c
#  ((((a or not b)))) and b
#  如果要实现not, 建议重新实现, 不再使用基于检索结果长度的优化


class BoolenSearcher:

    def __init__(self, corpus):
        self.corpus = corpus
        self.boolen_expression = None


    def run(self, boolen_expression, show_parse_pattern=True):
        self.boolen_expression = BoolenExpression.parse(boolen_expression)

        if show_parse_pattern:
            print("The formatted boolen expression is: "+"\033[31m" + self.boolen_expression + "\033[0m")

        or_items = [i.strip() for i in self.boolen_expression.split('or') if i.strip()]

        or_ret = []
        and_ret = []

        for i, or_item in enumerate(or_items):
            and_items = [j.strip() for j in or_item.split('and') if j.strip()]

            found_key = True
            for and_item in and_items:
                try:
                    _ = self.corpus.token2id[and_item]
                except KeyError:
                    found_key = False
                    break

            if not found_key:
                continue

            and_items.sort(key=lambda x: len(self.corpus.invert_indice[self.corpus.token2id[x]]))

            for j, and_item in enumerate(and_items):
                if j == 0:
                    and_ret = self.corpus.invert_indice[self.corpus.token2id[and_item]].keys()
                else:
                    if not and_ret:
                        break

                    temp_ret = []
                    temp = self.corpus.invert_indice[self.corpus.token2id[and_item]].keys()
                    for k in and_ret:
                        if k in temp:
                            temp_ret.append(k)

                    and_ret = temp_ret

            if and_ret:
                or_ret.extend(and_ret)

        return or_ret



# 布尔表达式类: 将输入的布尔表达式字符串(可包含and,or,以及任意嵌套的括号)格式化为布尔表达式与或式字符串
class BoolenExpression:

    @staticmethod
    def parse(boolen_expression):
        boolen_expression = boolen_expression.replace('(', ' ( ').replace(')', ' ) ').strip()
        split_tokens = [i.strip() for i in boolen_expression.split() if i.strip()]
        operators, items = BoolenExpression._parse2tree(split_tokens)
        return BoolenExpression._parse2str(operators, items)


    @staticmethod
    def _parse2tree(split_tokens):

        # 去掉最外层的 '()'
        paren_in_outer = True
        while paren_in_outer:
            if split_tokens[0] == '(':
                paren_level = 0
                for i, token in enumerate(split_tokens):
                    if token == '(':
                        paren_level += 1
                    elif token == ')':
                        paren_level -= 1
                        if paren_level == 0 and i == len(split_tokens) - 1:
                            split_tokens = split_tokens[1:-1]
                        elif  paren_level == 0:
                            paren_in_outer = False
                            break
            else :
                paren_in_outer = False


        operators = []
        items = []
        next_level_split_tokens = []
        paren_start = False
        paren_level = 0

        for i in split_tokens:
            if not paren_start:
                if i == '(':
                    paren_start = True
                    paren_level = 1
                elif i == 'and' or i == 'or':
                    operators.append(i)
                else:
                    items.append([i])
            else:
                if i == '(':
                    paren_level += 1
                    next_level_split_tokens.append('(')
                elif i == ')':
                    paren_level -= 1
                    if paren_level == 0:
                        paren_start = False
                        items.append(BoolenExpression._parse2tree(next_level_split_tokens))
                        next_level_split_tokens.clear()
                    else:
                        next_level_split_tokens.append(')')
                else:
                    next_level_split_tokens.append(i)

        return [operators, items]


    @staticmethod
    def _parse2str(operators, items):
        or_indexs = []
        or_items = []
        or_operators = []

        if not operators:
            return items[0][0]

        for i, item in enumerate(operators):
            if item == 'or':
                or_indexs.append(i)

        if or_indexs:
            for i, index in enumerate(or_indexs):
                if i == 0:
                    if len(items[0:or_indexs[i] + 1]) == 1:
                        or_items.append(items[0])
                    else:
                        or_items.append([['and']*(len(items[0:or_indexs[i] + 1])-1), items[0:or_indexs[i] + 1]])

                else:
                    if len(items[or_indexs[i - 1] + 1:or_indexs[i] + 1]) == 1:
                        or_items.append(items[or_indexs[i - 1] + 1])
                    else :
                        or_items.append([['and']*(len(items[or_indexs[i - 1] + 1:or_indexs[i] + 1])-1), items[or_indexs[i - 1] + 1:or_indexs[i] + 1]])

                if i == len(or_indexs) - 1:
                    if len(items[or_indexs[i] + 1:]) ==1:
                        or_items.append(items[or_indexs[i] + 1])
                    else :
                        or_items.append([['and']*(len(items[or_indexs[i] + 1:])-1), items[or_indexs[i] + 1:]])

            return BoolenExpression._parse_or_expression(or_items)
        else:
            return BoolenExpression._parse_and_expression(items)


    @staticmethod
    def _parse_and_expression(and_items):
        ret_str = ''
        for i, and_item in enumerate(and_items):
            if i == 0:
                if len(and_item) == 1:
                    ret_str += and_item[0]
                else:
                    operators, items = and_item
                    ret_str += BoolenExpression._parse2str(operators, items)

            else:
                if len(and_item) == 1:
                    split_items = [j.strip() for j in ret_str.split('or') if j.strip()]
                    for index, item in enumerate(split_items):
                        split_items[index] = item + ' and ' + and_item[0]
                    if len(split_items) == 1:
                        ret_str = str(split_items[0])
                    else:
                        ret_str = ' or '.join(split_items)
                else:
                    operators, items = and_item
                    split_items = [j.strip() for j in ret_str.split('or') if j.strip()]
                    split_items_2 = [j.strip() for j in BoolenExpression._parse2str(operators, items).split('or') if j.strip()]
                    ret_str = ''
                    for index, j in enumerate(split_items):
                        for index_2, k in enumerate(split_items_2):
                            ret_str += j+' and '+k
                            if index_2 == len(split_items_2)-1:
                                continue
                            ret_str += ' or '
                        if index == len(split_items)-1:
                            continue
                        ret_str += ' or '

        return ret_str

    @staticmethod
    def _parse_or_expression(or_items):

        ret_list = []

        for or_item in or_items:
            if len(or_item) == 1:
                ret_list.append(or_item[0])
            else:
                operators, items = or_item
                ret_list.append(BoolenExpression._parse2str(operators, items))

        return ' or '.join(ret_list)


if __name__ == '__main__':
    print(BoolenExpression.parse("(a or ((社会主义 and (注意)) and (c or d)))"))


