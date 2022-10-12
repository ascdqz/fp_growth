# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import csv

# an example from https://blog.csdn.net/weixin_43317943/article/details/122094461?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_baidulandingword~default-1-122094461-blog-60132224.pc_relevant_default&spm=1001.2101.3001.4242.2&utm_relevant_index=3
PATH = "base.csv"
MIN_FREQ = 3
MIN_CONF = 0.7


class Node:
    def __init__(self, key, parent):
        self.key = key
        self.count = 1
        self.next = None
        # self.prev = None
        self.parent = parent
        self.children = {}


class FP_Tree:
    def __init__(self, data, counter):
        self.counter = counter
        self.data = data
        self.root = Node(None, None)
        self.dict = {}
        self.prefix_path = {}
        self.build()
        self.get_prefix_path()
        self.frequant_itemlist=[]
        return

    def build(self):
        # todo
        for d in self.data:
            # if not rearrange, use this
            # not stable
            # d.sort(key=self.counter.get, reverse=True)
            d.sort(key=self.counter.get)
            pointer = self.root
            for i in d:
                val = pointer.children.get(i)

                if val is None:
                    child = Node(i, pointer)
                    pointer.children[i] = child
                    pointer = child
                    self.add_new_node(child)
                else:
                    val.count += 1
                    pointer = val

    def add_new_node(self, node):
        val = self.dict.get(node.key)
        if val is None:
            self.dict[node.key] = node
        else:
            prev = val
            cur = val.next
            while cur is not None:
                prev = cur
                cur = cur.next
            prev.next = node

    def get_prefix_path(self):

        for i in self.dict:
            # entry node
            val = self.dict[i]
            pointer = val
            cur_prefix_path = []
            while pointer is not None:
                count = pointer.count
                l = []
                current = pointer.parent
                while current != self.root:
                    l.append(current.key)
                    current = current.parent
                result = (count, l)
                cur_prefix_path.append(result)
                pointer = pointer.next
            self.prefix_path[i] = cur_prefix_path

    def minedtree(self):
        xiao=[]
        da=[]
        self.frequant_itemlist=minetree(self.root,self.dict,xiao,da,self.prefix_path)
        return self.frequant_itemlist





def prefix_to_d(key, prefix):
    lis = []
    lis1 = []
    lis2 = []
    for item in prefix[key]:
        count = item[0]
        for temp in item[1]:
            lis1.append(temp)
        lis2 = lis1.copy()
        lis.append(lis2)
        while count != 1:
            lis.append(lis2)
            count -= 1
        lis1.clear()
    lis2='nb'

    return lis

def minetree(root,dict,xiao,da,prefix):
    tempdic={}

    for key in dict:
        tempdic[key]=dict[key].count
    templis=[them[0] for them in sorted(tempdic.items(),key=lambda p:p[1])]

    for item in templis:
        lis=xiao.copy()
        lis.append(item)
        da.append(xiao)
        d=prefix_to_d(key,prefix)
        data,c=pre_processing(d)
        tree=FP_Tree(data,c)
        contree=tree.root
        dic_p=tree.dict
        prefi=tree.prefix_path
        if dic_p!=None:
            minetree(contree,dic_p,lis,da,prefi)

    return da

def rearrange_dict(dic):
    val = list(dic.values())
    val.sort(reverse=True)

    refined_dic = {}
    for i in dic:
        index = val.index(dic[i])

        refined_dic[i] = index
        val[index] = 'x'

    return refined_dic


def pre_processing(o):
    data = []
    processed_data = []
    counter = {}
    refined_counter = {}

    # header = next(f)
    for row in f:
        for prop in row:
            value = counter.get(prop)

            if value is None:
                counter[prop] = 1
            else:
                counter[prop] = value + 1
        data.append(row)
    for key in counter:
        value = counter[key]
        if value >= MIN_FREQ:
            refined_counter[key] = value
    for i in data:
        attr = []
        for j in i:
            value = refined_counter.get(j)
            if value is not None:
                attr.append(j)
        if len(attr) == 0:
            continue
        processed_data.append(attr)

    # print("origin data: ", data)
    #print("d:freq data : ", processed_data)
    #print("origin counter: ", counter)
    #print("freq counter", refined_counter)
    refined_counter = rearrange_dict(refined_counter)
    #print("c:index of freq attrs", refined_counter)
    # example: {'r': 4, 'z': 0, 'y': 2, 'x': 1, 't': 5, 's': 3}
    # but the order of same value is random, which will change the structure of FP Tree
    return processed_data, refined_counter


if __name__ == '__main__':
    with open(PATH, "r") as o:
        f = csv.reader(o)
        d, c = pre_processing(f)
        tree = FP_Tree(d, c)
        frequant_item_list=tree.minedtree()
        print(frequant_item_list)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
