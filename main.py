import csv

PATH = "base.csv"
MIN_FREQ = 2
MIN_CONF = 0.7


class Node:
    def __init__(self, key, parent):
        self.key = key
        self.next = None
        self.parent = parent
        self.Node = []


class FP_Tree:
    def __init__(self, counter, data):
        self.counter = counter
        self.data = data
        self.root = Node(None, None)
        self.build()

    def build(self):
        return


if __name__ == '__main__':
    with open(PATH, "r") as o:
        data = []
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

        print(data)
        print(counter)
        print(refined_counter)

        tree = FP_Tree(refined_counter, data)
