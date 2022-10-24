import csv
import os
import time
import tracemalloc
from datetime import datetime

PATH = "DataSetA.csv"
MIN_FREQ = 1000
MIN_CONF = 0.9


class Node:
    def __init__(self, key, parent):
        self.key = key
        self.count = 1
        self.next = None
        # self.prev = None
        self.parent = parent
        self.children = {}


class FP_Tree:
    def __init__(self, data, counter, sitems):
        self.counter = counter
        self.data = data
        self.root = Node(None, None)
        self.dict = {}
        self.prefix_path = {}
        self.build()
        self.get_prefix_path()
        self.sitems = sitems

    def build(self):
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

    def get_mined_tree(self):
        return self.mine(self.sitems, [], [], self.prefix_path)

    def mine(self, item_lis, xiao, da, prefix):
        for item in item_lis:
            lis = xiao.copy()
            lis.append(item)
            da.append(lis)
            d = prefix_to_d(item, prefix)
            data, c, a = pre_processing(d)
            tree = FP_Tree(data, c, a)
            if a is not None:
                self.mine(a, lis, da, tree.prefix_path)
        return da


def prefix_to_d(key, prefix):
    lis = []
    lis1 = []
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
    return lis


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
    for row in o:
        for prop in row:
            value = counter.get(prop)
            if value is None:
                counter[prop] = 1
            else:
                counter[prop] = value + 1
        data.append(row)
    for key in counter:
        value = counter[key]
        if value >= MIN_FREQ and key != '':
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
    # print("d:freq data : ", processed_data)
    # print("origin counter: ", counter)
    # print("freq counter", refined_counter)
    refined_counter = rearrange_dict(refined_counter)
    a = [v[0] for v in sorted(refined_counter.items(), key=lambda p: p[1], reverse=True)]
    # print("c:index of freq attrs", refined_counter)
    # example: {'r': 4, 'z': 0, 'y': 2, 'x': 1, 't': 5, 's': 3}
    # but the order of same value is random, which will change the structure of FP Tree
    return processed_data, refined_counter, a


class Tracer:
    def __init__(self, time, mem, result):
        self.log_path = "log/" + PATH[0:-4] + "_" + str(datetime.now())[0:19] + ".txt"
        self.log_path = self.log_path.replace(':', '-')
        self.info = {"dataset": PATH, "MIN_FREQ": MIN_FREQ, "MIN_CONF": MIN_CONF, "time_cons": time, "mem_cons": mem,
                     "result": result}

    def output(self):
        print(self.info["result"])
        print("total time consumption:", self.info["time_cons"])
        print("total storage consumption:", self.info["mem_cons"])
        l = os.listdir()
        if "log" not in l:
            os.mkdir("log")
        with open(self.log_path, 'w', encoding='utf-8') as o:
            for i in self.info:
                if i == "result":
                    o.write(i + ": " + '\n')
                    for j in range(len(self.info[i])):
                        o.write(str(self.info[i][j]) + '\n')
                else:
                    o.write(i + ": " + str(self.info[i]) + '\n')


if __name__ == '__main__':
    start = time.time()
    tracemalloc.start()
    info = {}
    with open(PATH, "r") as o:
        f = csv.reader(o)
        d, c, a = pre_processing(f)
        tree = FP_Tree(d, c, a)
        result = tree.get_mined_tree()
    end = time.time()
    # The used time for mem trace shouldn't be included
    total = end - start
    mem_snapshot = tracemalloc.take_snapshot()
    stat = mem_snapshot.statistics('filename')
    sum = 0
    for s in stat:
        sum = sum + s.size
    Tracer(str(total) + " s", str(sum / 1024) + " KB", result).output()
