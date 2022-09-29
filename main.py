import csv

PATH = "base.csv"
MIN_FREQ = 2
MIN_CONF = 0.7


class Node:
    def __init__(self, key, parent):
        self.key = key
        self.count = 0
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
        self.build()

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
        return

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
    f = csv.reader(o)
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
    print("freq data: ", processed_data)
    # print("origin counter: ", counter)
    # print("freq counter", refined_counter)
    refined_counter = rearrange_dict(refined_counter)
    print("index of freq attrs", refined_counter)
    return processed_data, refined_counter


if __name__ == '__main__':
    with open(PATH, "r") as o:
        d, c = pre_processing(o)
        tree = FP_Tree(d, c)
