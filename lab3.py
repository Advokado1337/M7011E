import math
import random
import time
from matplotlib import pyplot as plt
from collections import deque

class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.parent = None

class BST:
    def __init__(self, root, c):
        self.root = root
        self.relroot = None
        self.c = c

        if c <= 0.5 or c >= 1:
            raise Exception("c must be between 0.5 and 1")

    def reorder(self, node):
        sortedList = self.inorder(node.parent, [])
        if node.parent == self.root:
            self.root = Node(sortedList[len(sortedList) // 2])
            self.relroot = self.root
        else:
            self.relroot = Node(sortedList[len(sortedList) // 2])

        self.makeNodes(sortedList, 1)

        grandparent = node.parent.parent
        if grandparent is not None:
            self.relroot.parent = grandparent
            if grandparent.val > self.relroot.val:
                grandparent.left = self.relroot
            else:
                grandparent.right = self.relroot

    def makeNodes(self, lista, t):
        if not lista:
            return
        mid = len(lista) // 2
        if t != 1:
            self.insert_rel(lista[mid])
        t += 1
        self.makeNodes(lista[:mid], t)
        self.makeNodes(lista[mid+1:], t)

    def inorder(self, root, res):
        if root:
            self.inorder(root.left, res)
            res.append(root.val)
            self.inorder(root.right, res)
        return res

    def traverse(self, node):
        parent = node.parent
        if parent is not None:
            leftSize = self.checker(parent.left)
            rightSize = self.checker(parent.right)
            combinedSize = leftSize + rightSize + 1

            balanced = (
                (rightSize <= self.c * combinedSize) and
                (leftSize <= self.c * combinedSize)
            )

            if balanced:
                self.traverse(parent)
            else:
                self.reorder(node)
                self.traverse(parent)

    def checker(self, node):
        if node is None:
            return 0
        return self.checker(node.left) + self.checker(node.right) + 1

    def insert(self, value):
        node = Node(value)
        tree = self.root
        while True:
            if node.val < tree.val:
                if tree.left is None:
                    tree.left = node
                    node.parent = tree
                    break
                else:
                    tree = tree.left
            else:
                if tree.right is None:
                    tree.right = node
                    node.parent = tree
                    break
                else:
                    tree = tree.right
        self.traverse(node)

    def insert_rel(self, value):
        node = Node(value)
        tree = self.relroot
        while True:
            if node.val < tree.val:
                if tree.left is None:
                    tree.left = node
                    node.parent = tree
                    break
                else:
                    tree = tree.left
            else:
                if tree.right is None:
                    tree.right = node
                    node.parent = tree
                    break
                else:
                    tree = tree.right

    

    def print_tree_layers(self):
        """Prints the tree with proper alignment and spacing."""
        if not self.root:
            print("Tree is empty.")
            return

        # Calculate the maximum depth of the tree
        max_depth = self.get_tree_depth(self.root)

        # Queue for level-order traversal
        queue = deque([(self.root, 0)])  # (node, depth)
        layers = []  # To store each level's nodes

        while queue:
            node, depth = queue.popleft()

            # Start a new layer if needed
            if len(layers) <= depth:
                layers.append([])

            # Add the current node to the current layer
            layers[depth].append(node)

            # Enqueue children if the node exists
            if node:
                queue.append((node.left, depth + 1))
                queue.append((node.right, depth + 1))
            else:
                # Add placeholders for missing nodes up to max_depth
                if depth + 1 < max_depth:
                    queue.append((None, depth + 1))
                    queue.append((None, depth + 1))

        # Print each layer
        for depth, layer in enumerate(layers):
            self._print_layer(layer, max_depth, depth)

    def _print_layer(self, nodes, max_depth, current_depth):
        """Helper function to print a single layer with proper alignment."""
        # Calculate the spaces before and between nodes at the current depth
        num_spaces = int((2 ** (max_depth - current_depth - 1)) - 1)
        between_spaces = int((2 ** (max_depth - current_depth)) - 1)

        # Line for the node values
        line = " " * num_spaces
        for node in nodes:
            # Fixed-width representation of node values
            line += (str(node.val).center(3) if node else "   ")  
            line += " " * between_spaces
        print(line.rstrip())

        # Line for the connectors
        if current_depth < max_depth - 1:
            connector_line = " " * num_spaces
            for node in nodes:
                if node:
                    # Dynamically determine the presence of child nodes
                    left_connector = "/" if node.left else " "
                    right_connector = "\\" if node.right else " "
                    connector_line += f"{left_connector}   {right_connector}".center(3)
                else:
                    connector_line += " " * 3
                connector_line += " " * between_spaces
            print(connector_line.rstrip())









    def get_tree_depth(self, node):
        """Helper function to calculate the depth of the tree."""
        if not node:
            return 0
        return 1 + max(self.get_tree_depth(node.left), self.get_tree_depth(node.right))




def main():
    times = []
    c = []
    array = []

    #for i in range(15):
    #    array.append(random.randint(1, 1000))
    array = [2,3,4,5,6,7,8,9,10]
    tree = BST(Node(1), 0.51)
    for value in array:
        tree.insert(value)
        print("Tree structure:"+str(tree.root.val))

        tree.print_tree_layers()
    
    print("Tree structure final:")

    tree.print_tree_layers()

    # for i in range(51, 99):
    #     c.append(i / 100)
    #     avg = 0
    #     saved = 100000
    #     start2 = time.perf_counter()
    #     for k in range(1):
    #         tree = BST(Node(10), i / 100)
    #         start = time.perf_counter()
    #         for j in range(len(array)):
    #             tree.insert(array[j])
    #         end = time.perf_counter()
    #         avg += end - start
    #     end2 = time.perf_counter()
    #     if saved > end2 - start2:
    #         saved = end2 - start2
    #     times.append(avg / 1)



main()
