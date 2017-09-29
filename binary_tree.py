class Node:
    def __init__(self, data, error=None, left=None, right=None):
        self.data = data
        self.error = error
        self.left = left
        self.right = right
        self.parent = None
        self.prediction = None

    def getPrediction(self):
        return self.prediction

    def setPrediction(self, value):
        self.prediction = value

    def getParent(self):
        return self.Parent

    def setParent(self, value):
        self.Parent = value

    def getLeftChild(self):
        return self.left

    def getRightChild(self):
        return self.right

    def getData(self):
        return self.data

    def getError(self):
        return self.error

    def setData(self, value):
        if self.data is not None:
            self.data = value
        else:
            return None

    def setError(self, value):
        if self.error is not None:
            self.error = value
        else:
            return None

    def insert_left(self, new_data):
        self.left = new_data

    def insert_right(self, new_data):
        self.right = new_data

    def is_leaf(self):
        return self.right is None and self.left is None

    def is_node(self):
        return self.right is not None or self.left is not None

    def delete(self):
        par = self.parent
        if par is None:
            return
        if par.left.data == self.data:
            par.left = None
        else:
            par.right = None


def count_leaves(self):
    if self.is_leaf():
        return 1
    count = 0
    if self.right is not None:
        count += count_leaves(self.right)
    if self.left is not None:
        count += count_leaves(self.left)
    return count


def getLeafNode(node, count):
    if node.is_leaf():
        count.append(node)
        # return self
    # count = []
    if node.right is not None:
        getLeafNode(node.right, count)  # count.append(
    if node.left is not None:
        getLeafNode(node.left, count)  # count.append(
        # return count


def count(root):
    if root is None:
        return 0
    else:
        if root.left is None and root.right is None:
            return 1
        else:
            return 1 + (count(root.left) + count(root.right))


def total_depth(tree, avg_depth):
    if tree is None:
        return 0
    return avg_depth + total_depth(tree.left, avg_depth + 1) + total_depth(tree.right, avg_depth + 1)
