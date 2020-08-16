# 二叉树专题

## BFS(层序遍历)框架

BFS 的核心思想就是把一些问题抽象成图，从一个点开始，向四周开始扩散。一般来说，我们写 BFS 算法都是用**「队列」**这种数据结构，每次将每个还没有搜索到的点依次放入队列，然后再弹出队列的头部元素当做当前遍历点。

BFS 相对 DFS 的最主要的区别是：**BFS 找到的路径一定是最短的，但代价就是空间复杂度比 DFS 大很多**。

BFS 出现的常见场景，问题的本质就是让你在一幅「图」中找到**从起点 `start`到终点`target`的最近距离**。

框架如下：

```python
# 计算从起点 start 到终点 target 的最近距离
def BFS(start, target):
    q = collections.deque()		# 核心数据结构
    visited = set()		# 避免走回头路(set集合保证visit中的元素唯一)

    q.append(start)		# 将起点加入队列
    visited.add(start)
    step = 0		# 记录扩散的步数

    while q:
  		sz = len(q)
        # 将每个还没有搜索到的点依次放入队列，再弹出队列的头部元素当做当前遍历点 
        # for 节点 in cur的所有相邻节点:
        #    if 该节点有效且未被访问过:
        #		 		queue.append(该节点)
        for _ in range(sz):
            cur = q.popleft()
            # 划重点：这里判断是否到达终点
            if cur == target:
                return step
            # 将 cur 的相邻节点加入队列
  					if cur.left and cur.left not in visited: 
  						q.append(cur.left)
						  visited.add(cur.left)
  					if cur.right and cur.right not in visited: 
  						q.append(cur.right)
						  visited.add(cur.right)
        # 划重点：更新步数在这里
        step += 1
```

> 像一般的二叉树结构，没有子节点到父节点的指针，不会走回头路就不需要 `visited`。

### [111. 二叉树的最小深度](https://leetcode-cn.com/problems/minimum-depth-of-binary-tree/)

首先明确一下起点 `start` 和终点 `target` 是什么，怎么判断到达了终点？

显然**起点就是`root`根节点，终点就是最靠近根节点的那个「叶子节点」**，叶子节点就是两个子节点都是 `None` 的节点：

```python
if not cur.left and not cur.right:
  # 到达叶子节点
```

那么，按照我们上述的框架稍加改造来写解法即可：

```python
class Solution:
    def minDepth(self, root: TreeNode) -> int:
        if not root: return 0
        q = collections.deque()
        q.append(root)
        depth = 1

        while q:
            sz = len(q)
            # 将每个还没有搜索到的点依次放入队列，再弹出队列的头部元素当做当前遍历点 
            for i in range(sz):
                cur = q.popleft()
                # 判断是否到达终点
                if not cur.left and not cur.right:
                    return depth
                # 将 cur 的相邻节点加入队列
                if cur.left: q.append(cur.left)
                if cur.right: q.append(cur.right)
            # 这里增加步数
            depth += 1
        return depth
```

### [102. 二叉树的层序遍历](https:#leetcode-cn.com/problems/binary-tree-level-order-traversal/)

```python
class Solution:
    def levelOrder(self, root: TreeNode) -> List[List[int]]:
        queue = collections.deque()
        queue.append(root)
        res = []
        while queue:
            size = len(queue)
            level = []
            for _ in range(size):
                cur = queue.popleft()
                if not cur:
                    continue
                level.append(cur.val)
                queue.append(cur.left)
                queue.append(cur.right)
            if level:
                res.append(level)
        return res
```

### [752. 打开转盘锁](https://leetcode-cn.com/problems/open-the-lock/)

```python
class Solution:
    def openLock(self, deadends: List[str], target: str) -> int:
        # 记录需要跳过的死亡密码
        deads = set()
        for s in deadends:
            deads.add(s)
        # 记录已经穷举过的密码，防止走回头路
        visited = set()
        q = collections.deque()
        # 从起点开始启动广度优先搜索
        step = 0
        q.append("0000")
        visited.add("0000")

        while q:
            sz = len(q)
            # 将当前队列中的所有节点向周围扩散
            for _ in range(sz):
                cur = q.popleft()
                # 判断是否到达终点
                if cur in deads:
                    continue
                if cur == target:
                    return step
                # 将一个节点的未遍历相邻节点加入队列
                for i in range(4):
                    up = self.plusOne(cur, i)
                    if up not in visited:
                        q.append(up)
                        visited.add(up)
                    down = self.minusOne(cur, i)
                    if down not in visited:
                        q.append(down)
                        visited.add(down)
            step += 1
        return -1

    # 将 s[j] 向上拨动一次
    def plusOne(self, s, j):
        s = [str(c) for c in s]
        if s[j] == '9':
            s[j] = '0'
        else:
            s[j] = int(s[j])
            s[j] += 1
            s[j] = str(s[j])
        return "".join(s)        
    
    # 将 s[i] 向下拨动一次
    def minusOne(self, s, j):
        s = [str(c) for c in s]
        if s[j] == '0':
            s[j] = '9'
        else:
            s[j] = int(s[j])
            s[j] -= 1
            s[j] = str(s[j])
        return "".join(s)
```





## BST(二叉搜索树)框架

**二叉树算法的设计的总路线：明确一个节点要做的事情，然后剩下的事抛给框架。**

```python
def traverse(root):
    # root 需要做什么？在这做。
    # 其他的不用 root 操心，抛给框架
    traverse(root.left)
    traverse(root.right)
```

举例

1. 如何把二叉树所有的节点中的值加一？

   ```python
   def plusOne(root) {
       if not root: return
       root.val += 1
   
       plusOne(root.left)
       plusOne(root.right)
   ```

2. 如何判断两棵二叉树是否完全相同？

   ```python
   def isSameTree(root1, root2)
       # 都为空的话，显然相同
       if not root1 and not root2: return True
       # 一个为空，一个非空，显然不同
       if not root1 or not root2: return False
       # 两个都非空，但 val 不一样也不行
       if root1.val != root2.val: return False
   
       # root1 和 root2 该比的都比完了
       return isSameTree(root1.left, root2.left)
           and isSameTree(root1.right, root2.right);
   ```

### 验证BST

>  **注意：**root 需要做的不只是和左右子节点比较，而是要整个左子树和右子树所有节点比较。
>
> 这种情况，我们可以**使用辅助函数，增加函数参数列表，在参数中携带额外信息。**

二叉搜索树的两个特征：

1. 节点的左子树只包含小于当前节点的数。
2. 节点的右子树只包含大于当前节点的数。

这两句话可以理解为：

1. 当前节点的值是其左子树的值的**上界**(最大值)
2. 当前节点的值是其右子树的值的**下界**(最小值)

#### [98. 验证二叉搜索树](https:#leetcode-cn.com/problems/validate-binary-search-tree/)

将整个判断过程抽象成递归代码。

写递归代码必需的两个要素：

1. 终止条件
2. 深入递归的递归方程

首先来看在这道题中的终止两种终止条件：

1. 当当前节点为空时，表示这个节点已经是叶子节点，这个节点没有子节点，可以返回 True
2. 当当前节点不在 [ min_value,max_value ] 的区间时，这个节点不能同时符合二叉搜索树的两个特征，返回 False

然后看看递归方程，由于节点有两个子树，所以我们有两个递归方程要执行(注意绿色剪头)：

1. 对左子树：isBST(root.left, min_val, root.val) 	解释：当前节点是左子树的上界(可以粗略地理解为最大值)
2. 对右子树：isBST(root.right, root.val, max_val)  解释同上

```python
class Solution:
    def isValidBST(self, root: TreeNode) -> bool:
        if not root:
            return True
        return self.isBST(root, float('-inf'), float('inf'))

    def isBST(self, root, min_val, max_val):
        # root：当前节点，min_val：允许最小值(下界)，max_val：允许最大值(上界)
        if not root:    # 如果当前节点为空，证明已经递归到叶子节点，返回True
            return True
        if root.val <= min_val or root.val >= max_val:	# 不符合二叉搜索树的特征，返回False
            return False
        # 对左子树进行递归，此时最大值应该为当前节点值
        # 对右子树进行递归，此时最小值应该为当前节点值
        return self.isBST(root.left, min_val, root.val) and 
      					self.isBST(root.right, root.val, max_val)
```

因为二叉搜索树中序遍历是递增的，所以我们可以中序遍历判断前一数是否小于后一个数。

```python
class Solution:
    def isValidBST(self, root: TreeNode) -> bool:
        res = []
        def helper(root):
            if not root:
                return 
            helper(root.left)
            res.append(root.val)
            helper(root.right)
        helper(root)
        # 判断res是否为升序且无重复元素
        return res == sorted(res) and len(set(res)) == len(res)
```

### BST的遍历框架

在 BST 中查找一个数是否存在，根据二叉树算法，我们可以写出：

```python
def isInBST(root, target):
    if not root: return False
    if root.val == target: return True
    return isInBST(root.left, target) or isInBST(root.right, target)
```

根据BST “左小右大”的特性，其实我们不需要递归地搜索两边，类似二分查找思想，根据 target 和 root.val 的大小比较，就能排除一边。我们把二叉树算法框架的思路稍稍改动：

```python
def isInBST(root, target):
    if not root: return False
    if root.val == target: return True
    if root.val < target:
        return isInBST(root.right, target)
    if root.val > target:
        return isInBST(root.left, target)
    # root 该做的事做完了，顺带把框架也完成了
```

于是，我们对原始框架进行改造，抽象出一套**针对 BST 的遍历框架**：

```python
def BST(root, target)
    if root.val == target:
        # 找到目标，做点什么
    if root.val < target:
        BST(root.right, target)
    if root.val > target:
        BST(root.left, target)
```

### 在 BST 中插入一个数

对数据结构的操作无非**遍历 + 访问**，**遍历就是“找”，访问就是“改”**。具体到这个问题，插入一个数，就是先找到插入位置，然后进行插入操作。

上一个问题，我们总结了 BST 中的遍历框架，就是“找”的问题。直接套框架，加上“改”的操作即可。**一旦涉及“改”，函数就要返回 TreeNode 类型，并且对递归调用的返回值进行接收。**

```python
def insertIntoBST(root, val):
    # 找到空位置插入新节点
    if not root:
      root = TreeNode(val)
      return root
    if root.val < val:
        root.right = insertIntoBST(root.right, val)
    if root.val > val:
        root.left = insertIntoBST(root.left, val)
    return root
```

### 在 BST 中删除一个数

跟插入操作类似，先“找”再“改”，先把框架写出来：

```python
def deleteNode(root, key):
    if root.val == key:
        # 找到啦，进行删除
    elif root.val > key:
        root.left = deleteNode(root.left, key)
    elif root.val < key:
        root.right = deleteNode(root.right, key)
    return root
```

找到目标节点之后，比方说是节点 A，如何删除这个节点，这是难点。因为删除节点的同时不能破坏 BST 的性质。有三种情况：

1. A 恰好是末端节点，两个子节点都为空，直接删除：

   ```python
   if not root.left and not root.right:
       return None
   ```

2. A 只有一个非空子节点，那么它要让这个孩子接替自己的位置：

   ```python
   # 排除了情况 1 之后
   if not root.left: return root.right
   if not root.right: return root.left
   ```

3. A 有两个子节点，麻烦了，为了不破坏 BST 的性质，A 必须找到左子树中最大的那个节点，或者右子树中最小的那个节点来接替自己。我们以第二种方式讲解：

   ```python
   if root.left and root.right:
       # 找到右子树的最小节点
       minNode = getMin(root.right)
       # 把 root 改成 minNode
       root.val = minNode.val
       # 转而去删除 minNode
       root.right = deleteNode(root.right, minNode.val)
   ```

三种情况分析完毕，填入框架，简化一下代码：

#### [450. 删除二叉搜索树中的节点](https://leetcode-cn.com/problems/delete-node-in-a-bst/)

```python
def deleteNode(self, root: TreeNode, key: int) -> TreeNode:
        if not root: return None
        if key == root.val:
            # key 两个子节点都为空 or 只有一个非空子节点
            if not root.left: return root.right
            if not root.right: return root.left
            # key 有两个子节点
            # 找到右子树的最小节点
            min_node = self.getMin(root.right)
            # 把 root 改成 min_node
            root.val = min_node.val
            # 转而去删除 min_node
            root.right = self.deleteNode(root.right, min_node.val)
        elif key < root.val:
            root.left = self.deleteNode(root.left, key)
        else:
            root.right = self.deleteNode(root.right, key)
        return root

    def getMin(self, root):
        while root.left:
            root = root.left
        return root
```

### 小结

1. 二叉树算法设计的总路线：**把当前节点要做的事做好，其他的交给递归框架，不用当前节点操心。**

2. **如果当前节点会对下面的子节点有整体影响，可以通过辅助函数增长参数列表，借助参数传递信息。**

3. 在二叉树框架之上，扩展出一套 **BST 遍历框架**：

   ```python
   def BST(root, target)
       if root.val == target:
           # 找到目标，做点什么
       if root.val < target:
           BST(root.right, target)
       if root.val > target:
           BST(root.left, target)
   ```

   