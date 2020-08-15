"""
二叉树的遍历
    深度优先遍历：前序、中序、后序
        实现方式：递归、栈(with_stack)
    广度优先遍历：层序
        实现方式：队列
"""
import collections
from queue import Queue


class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


def create_binary_tree(input_list):
    """
    构建二叉树
    :param input_list: 输入数列
    """
    """
    input_list: 3, 2, 9, None, None, 10, None, None, 8, None, 4
    
               3
          2        8
        9	 10	  N    4
      N   N N   N
    """
    if not input_list or len(input_list) == 0:
        return None
    data = input_list.pop(0)
    if not data:
        return None

    node = TreeNode(data)
    node.left = create_binary_tree(input_list)
    node.right = create_binary_tree(input_list)
    return node


def pre_order_traversal(node):
    """
    前序遍历
    :param node:二叉树节点
    """
    if not node:
        return

    print(node.data, end=' ')
    pre_order_traversal(node.left)
    pre_order_traversal(node.right)


def pre_order_traversal_with_stack(node):
    """
    前序遍历(栈实现)
    :param node:二叉树节点
    """

    """
    node: 3, 2, 9, None, None, 10, None, None, 8, None, 4
    
               3
           2        8
        9	 10	  N    4
      N   N N   N
    """
    stack = []
    # add temp for debug
    # temp = []
    while node is not None or len(stack) > 0:
        while node is not None:
            print(node.data, end=' ')
            stack.append(node)
            # temp.append(node.data)
            node = node.left
        # 当前节点没有左孩子了，开始向上回溯
        if len(stack) > 0:
            node = stack.pop()
            # temp.pop()
            node = node.right


def in_order_traversal(node):
    """
    中序遍历
    :param node: 二叉树节点
    """
    if not node:
        return

    pre_order_traversal(node.left)
    print(node.data, end=' ')
    pre_order_traversal(node.right)


def post_order_traversal(node):
    """
    后序遍历
    :param node: 二叉树节点
    """
    if not node:
        return

    pre_order_traversal(node.left)
    pre_order_traversal(node.right)
    print(node.data, end=' ')


def level_order_traversal(node):
    """
    层序遍历
    :param node: 二叉树节点
    """
    q = collections.deque()
    q.append(node)

    while q:
        cur = q.popleft()
        print(node.data, end=' ')
        if cur.left:
            q.append(cur.left)
        if cur.right:
            q.append(cur.right)


if __name__ == '__main__':
    my_input_list = list([3, 2, 9, None, None, 10, None, None, 8, None, 4])
    root = create_binary_tree(my_input_list)
    print("root:", root.data)  # 3
    print("前序遍历：")
    # pre_order_traversal(root)
    pre_order_traversal_with_stack(root)
    print("\n中序遍历：")
    in_order_traversal(root)
    print("\n后序遍历：")
    post_order_traversal(root)
    print("\n---------------")
    print("层序遍历：")
    level_order_traversal(root)
