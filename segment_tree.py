import math


class SegmentTree:
    ROOT_INDEX = 0

    class Node:
        def __init__(self, interval):
            self.inclusive_interval = interval
            self.value = 0

        def get(self):
            return self.value

        def set(self, value):
            self.value = value

        def is_complete_overlap(self, interval):
            return self.inclusive_interval[0] >= interval[0] and self.inclusive_interval[1] <= interval[1]

        def is_null_overlap(self, interval):
            return interval[0] > self.inclusive_interval[1] or interval[1] < self.inclusive_interval[0]

    def __init__(self, data, segment_func, leaf_func):
        self.segment_func = segment_func
        self.leaf_func = leaf_func
        self.tree = [None] * SegmentTree.tree_size(len(data))
        self.compute_tree(data, SegmentTree.ROOT_INDEX, 0, len(data) - 1)

    def update(self, index, value):
        self._update(index, value, SegmentTree.ROOT_INDEX)

    def _update(self, index, value, node_index):
        node = self.tree[node_index]
        if node.inclusive_interval[0] == index and node.inclusive_interval[1] == index:
            prev_value = node.get()
            node.set(self.leaf_func(value))
            return node.get()
        elif node.is_null_overlap((index, index)):
            return node.get()
        else:
            left_value = self._update(index, value, SegmentTree.left(node_index))
            right_value = self._update(index, value, SegmentTree.right(node_index))
            node.set(self.segment_func(left_value, right_value))
            return node.get()

    def compute_tree(self, data, root, f_index, t_index):
        # print("{} {} {}".format(root, f_index, t_index))
        self.tree[root] = SegmentTree.Node((f_index, t_index))
        if t_index == f_index:
            self.tree[root].set(self.leaf_func(data[f_index]))
            return self.tree[root].get()
        elif f_index > t_index:
            return 0

        half = f_index + (t_index - f_index) // 2
        left_subtree_val = self.compute_tree(data, SegmentTree.left(root), f_index, half)
        right_subtree_val = self.compute_tree(data, SegmentTree.right(root), half + 1, t_index)
        self.tree[root].set(self.segment_func(left_subtree_val, right_subtree_val))
        return self.tree[root].get()

    def calc_segment(self, left, right):
        return self.get((left, right), SegmentTree.ROOT_INDEX)

    def get(self, interval, node_index):
        if self.tree[node_index].is_complete_overlap(interval):
            return self.tree[node_index].get()
        elif self.tree[node_index].is_null_overlap(interval):
            return 0
        else:
            return self.get(interval, SegmentTree.left(node_index)) + self.get(interval, SegmentTree.right(node_index))

    def find(self, index, left_right, result):
        left, right = left_right

        if index == left and index == right:
            return result

        half = left + (right - index) // 2
        if index <= half:
            return self.find(index, left, half, SegmentTree.left(result))
        else:
            return self.find(index, half + 1, SegmentTree.right(result))

    @staticmethod
    def mid_index(current_interval):
        return current_interval[0] + (current_interval[1] - current_interval[0]) // 2

    @staticmethod
    def tree_size(data_size):
        return 2 * 2 ** math.ceil(math.log2(data_size)) - 1

    @staticmethod
    def left(index):
        return 2 * index + 1

    @staticmethod
    def right(index):
        return 2 * index + 2

    @staticmethod
    def parent(index):
        return (index - 1) // 2
