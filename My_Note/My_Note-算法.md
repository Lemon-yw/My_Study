# 排序

## 快速排序

基本思想：通过一趟排序将待排记录分隔成独立的两部分，其中一部分记录的关键字均比另一部分的关键字小，则可分别对这两部分记录继续进行排序，以达到整个序列有序。

### 算法描述

1. 从数列中挑出一个元素，称为 “基准”（pivot）；
2. 重新排序数列，所有元素比基准值小的摆放在基准前面，所有元素比基准值大的摆在基准的后面（相同的数可以到任一边）。在这个分区退出之后，该基准就处于数列的正确位置。这个称为分区（partition）操作；
3. 递归地（recursive）把小于基准值元素的子数列和大于基准值元素的子数列排序。

### 代码实现

```python
def quick_sort(start_index, end_index, array):
    # 递归的结束条件
    if start_index >= end_index:
        return
    # 得到基准元素的位置
    pivot_index = partition_v1(start_index, end_index, array)
    # 根据基准元素位置，分成两部分进行排序
    quick_sort(start_index, pivot_index-1, array)
    quick_sort(pivot_index+1, end_index, array)


def partition_v1(start_index, end_index, array):
    # 取第一个元素作为基准元素
    pivot = array[start_index]
    left = start_index
    right = end_index

    while left != right:
        # 控制right指针比较并左移
        while left < right and array[right] > pivot:
            right -= 1
        # 控制left指针比较并右移
        while left < right and array[left] <= pivot:
            left += 1
        # 交换left和right指向的元素
        if left < right:
            array[left], array[right] = array[right], array[left]
    # pivot和指针重合点交换(注意不能直接用pivot的值进行交换，改变pivot的值没有意义)
    array[start_index], array[left] = array[left], array[start_index]
    return left
```

**注意**

1. **指针移动的先后顺序**：**指针要从基准元素的另一方向指针开始移动**，即从右指针开始移动，由于基准元素从左侧开始（若基准元素从右侧开始则先移动左指针），若从左指针开始移动，执行顺序会以左指针的位置为主，左指针会先停下，然后限制右指针的移动，而由于左指针最后停下的位置一定是left+1之后大于pivot时停下，也就是说此时左指针停下位置的元素值是大于pivot的，不符合预期，所以要先从右指针开始移动，保证了先停下的指针位置的值是小于等于pivot的。
2. **等号的归属**：**等号要从基准元素侧的指针开始**，即等号从左指针开始，由于基准元素从左侧开始（若基准元素从右侧开始则等号从右指针开始），为了防止pivot位置被移动，即避免左指针一直停留在pivot位置时被换位，所以在相等时要往后移一位。



## 归并排序

基本思想：先使每个子序列有序，再使子序列段间有序。是递归的思想。

### 算法描述

1. 把长度为n的输入序列分成两个长度为n/2的子序列；
2. 对这两个子序列分别采用归并排序；
3. 将两个排序好的子序列合并成一个最终的排序序列。

### 代码实现

```python
def merge_sort(array):
    length = len(array)
    if length < 2:
        return array

    middle = length // 2
    left, right = array[0: middle], array[middle:]
    return merge(merge_sort(left), merge_sort(right))


def merge(left, right):
    result = []
    while left and right:
        if left[0] <= right[0]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))

    while left:
        result.append(left.pop(0))
    while right:
        result.append(right.pop(0))
    return result
```



## 堆排序

基本思想：堆排序（Heapsort）是指利用堆这种数据结构所设计的一种排序算法。堆积是一个近似完全二叉树的结构，并同时满足堆积的性质：即子结点的键值或索引总是小于（或者大于）它的父节点。

### 算法描述

### 代码实现



## 各排序复杂度 & 稳定性

<img src="https://tva1.sinaimg.cn/large/007S8ZIlly1gi1scxqyh3j310g0ow471.jpg" alt="image-20200824122521381" style="zoom:50%;" />



# 栈实现队列 | 队列实现栈

## [232. 用栈实现队列](https://leetcode-cn.com/problems/implement-queue-using-stacks/)

我们使用两个栈 `s1, s2` 就能实现一个队列的功能：

<img src="https://tva1.sinaimg.cn/large/007S8ZIlly1gi14322ur9j30te0ewh0a.jpg" alt="image-20200823222525052" style="zoom: 43%;" />

当调用 `push` 让元素入队时，只要把元素压入 `s1` 即可，比如说 `push` 进 3 个元素分别是 1,2,3，那么底层结构就是这样：

<img src="https://tva1.sinaimg.cn/large/007S8ZIlly1gi144fofscj30tc0eqnc3.jpg" alt="image-20200823222649489" style="zoom:43%;" />

那么如果这时候使用 `peek` 查看队头的元素怎么办呢？按道理队头元素应该是 1，但是在 `s1` 中 1 被压在栈底，现在就要轮到 `s2` 起到一个中转的作用了：当 `s2` 为空时，可以把 `s1` 的所有元素取出再添加进 `s2`，**这时候** **`s2`** **中元素就是先进先出顺序了**。

<img src="https://tva1.sinaimg.cn/large/007S8ZIlly1gi1461vcdxj30t00ewtnn.jpg" alt="image-20200823222822595" style="zoom:43%;" />

完整思路：

1. 初始化两个栈结构，stack1为主栈，stack2为辅助栈
2. push往stack1末尾添加元素，利用append即可实现
3. pop时候，先将stack1元素向stack2转移，知道stack1只剩下一个元素时候（这就是我们要返回的队列首部元素），然后我们再把stack2中的元素转移回stack1中即可
4. 类似于步骤（3）的操作，唯一不同是这里我们需要将elenment先添加回stack2，然后再将stack2的元素转移回stack1中，因为peek操作不需要删除队列首部元素
5. empty判断stack1尺寸即可

完整代码：

```python
class MyQueue:

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.stack1 = []     # 主栈
        self.stack2 = []     # 辅助栈

    def push(self, x: int) -> None:
        """
        Push element x to the back of queue.
        """
        self.stack1.append(x)

    def pop(self) -> int:
        """
        Removes the element from in front of queue and returns that element.
        """
        while len(self.stack1) > 1:
            self.stack2.append(self.stack1.pop())
        element = self.stack1.pop()
        while len(self.stack2) > 0:
            self.stack1.append(self.stack2.pop())
        return element

    def peek(self) -> int:
        """
        Get the front element.
        """
        while len(self.stack1) > 1:
            self.stack2.append(self.stack1.pop())
        element = self.stack1.pop()
        self.stack2.append(element)
        while len(self.stack2) > 0:
            self.stack1.append(self.stack2.pop())
        return element

    def empty(self) -> bool:
        """
        Returns whether the queue is empty.
        """
        return len(self.stack1) == 0
```

## [225. 用队列实现栈](https://leetcode-cn.com/problems/implement-stack-using-queues/)

```python
class MyStack:

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.queue = []


    def push(self, x: int) -> None:
        """
        Push element x onto stack.
        """
        self.queue.append(x)
        queue_len = len(self.queue)
        while queue_len > 1:
            #反转前n-1个元素，栈顶元素始终保留在队首
            self.queue.append(self.queue.pop(0))
            queue_len -= 1


    def pop(self) -> int:
        """
        Removes the element on top of the stack and returns that element.
        """
        return self.queue.pop(0)


    def top(self) -> int:
        """
        Get the top element.
        """
        return self.queue[0]


    def empty(self) -> bool:
        """
        Returns whether the stack is empty.
        """
        return len(self.queue) == 0
```



# 反转链表

## 反转整个链表

### [206. 反转链表](https://leetcode-cn.com/problems/reverse-linked-list/)

先看代码：

```python
class Solution:
    def reverseList(self, head: ListNode) -> ListNode:
        # 递归
        if not head or not head.next:
            return head
        
        last_node = self.reverseList(head.next)
        head.next.next = head
        head.next = None
        return last_node
```

**对于递归算法，最重要的就是明确递归函数的定义**。具体来说，我们的 `reverse` 函数定义是这样的：

输入一个节点`head`，将「以`head`为起点」的链表反转，并返回反转之后的头结点。

明白了函数的定义，在来看这个问题。比如说我们想反转这个链表：

<img src="https://tva1.sinaimg.cn/large/007S8ZIlly1gi160qju4dj31380bqncg.jpg" alt="image-20200823233228072" style="zoom:45%;" />

那么输入 `self.reverseList(head)` 后，会在这里进行递归：

```python
last_node = self.reverseList(head.next)
```

不要跳进递归（你的脑袋能压几个栈呀？），而是要根据刚才的函数定义，来弄清楚这段代码会产生什么结果：

<img src="https://tva1.sinaimg.cn/large/007S8ZIlly1gi163b58izj314e09e15z.jpg" alt="image-20200823233456524" style="zoom:50%;" />

这个 `self.reverseList(head.next)`执行完成后，整个链表就成了这样：

<img src="https://tva1.sinaimg.cn/large/007S8ZIlly1gi164ww2m8j31200bs4dt.jpg" alt="image-20200823233629072" style="zoom:50%;" />

并且根据函数定义，`reverseList` 函数会返回反转之后的头结点，我们用变量 `last_node` 接收了。

现在再来看下面的代码：

```python
head.next.next = head
```

<img src="https://tva1.sinaimg.cn/large/007S8ZIlly1gi16661zn2j30zc0fa4hd.jpg" alt="image-20200823233741464" style="zoom:50%;" />

接下来：

```python
head.next = None
return last_node
```

<img src="https://tva1.sinaimg.cn/large/007S8ZIlly1gi167m5a70j314i0g61eq.jpg" alt="image-20200823233904831" style="zoom:35%;" />

这样整个链表就反转过来了！不过其中有两个地方需要注意：

1. 递归函数要有 base case，也就是这句：

```python
if not head.next: return head
```

意思是如果链表只有一个节点的时候反转也是它自己，直接返回即可。

2. 当链表递归反转之后，新的头结点是 `last_node`，而之前的 `head` 变成了最后一个节点，别忘了链表的末尾要指向 None：

```python
head.next = None
```

另外也可以迭代实现：

```python
class Solution:
    def reverseList(self, head: ListNode) -> ListNode:
        # 迭代
        pre = None
        cur = head

        while cur:
            temp = cur.next
            cur.next = pre
            pre = cur
            cur = temp
        return pre
```



## 反转链表前n个节点

比如说对于下图链表，执行 `reverseN(head, 3)`：

<img src="https://tva1.sinaimg.cn/large/007S8ZIlly1gi16lj9htyj312o0kohcn.jpg" alt="image-20200823235227739" style="zoom: 40%;" />

解决思路和反转整个链表差不多，只要稍加修改即可：

1. base case 变为 `n == 1`，反转一个元素，就是它本身，同时**要记录后驱节点**。
2. 刚才我们直接把 `head.next` 设置为 None，因为整个链表反转后原来的 `head` 变成了整个链表的最后一个节点。但现在 `head` 节点在递归反转之后不一定是最后一个节点了，所以要记录后驱 `successor`（第 n + 1 个节点），反转之后将 `head` 连接上。

<img src="https://tva1.sinaimg.cn/large/007S8ZIlly1gi16n3d6k9j315q0dywxf.jpg" alt="image-20200823235357029" style="zoom:40%;" />

```python
successor = None # 后驱节点

# 反转以 head 为起点的 n 个节点，返回新的头结点
def reverseN(head, n):
    if n == 1:
        successor = head.next	# 记录第 n + 1 个节点
        return head
    # 以 head.next 为起点，需要反转前 n - 1 个节点
    last = reverseN(head.next, n - 1)
	# 反转 head 节点
    head.next.next = head
    # 让反转之后的 head 节点和后面的节点连起来
    head.next = successor
    return last
```



## 反转链表的一部分

### [92. 反转链表 II](https://leetcode-cn.com/problems/reverse-linked-list-ii/)

首先，如果 `m == 1`，就相当于反转链表开头的 `n` 个元素，也就是我们刚才实现的功能；

如果 `m != 1` 怎么办？如果我们把 `head` 的索引视为 1，那么我们是想从第 `m` 个元素开始反转；如果把 `head.next` 的索引视为 1 呢？那么相对于 `head.next`，反转的区间应该是从第 `m - 1` 个元素开始的；那么对于 `head.next.next` 呢……

区别于迭代思想，这就是递归思想，所以我们可以完成代码：

```python
class Solution:
    def reverseBetween(self, head: ListNode, m: int, n: int) -> ListNode:
        # 反转以 head 为起点的 n 个节点，返回新的头结点
        def reverseN(head, n):
            if n == 1:
                successor = head.next # 拿到后继(第 n+1 个)节点
                return head, successor
            # 以 head.next 为起点，需要反转前 n - 1 个节点
            last, successor = reverseN(head.next, n-1)

            # 反转 head 节点
            head.next.next = head
            # 让反转之后的 head 节点和后继节点连起来
            head.next = successor
            return last, successor

        if m == 1: # 递归终止条件
            res, _ = reverseN(head, n)
            return res
        # 如果不是第一个，那么以下一个为头结点开始递归，直到触发条件
        head.next = self.reverseBetween(head.next, m-1, n-1)
        return head
```



# 二叉树专题

## BFS(层序遍历)框架

BFS 的核心思想就是把一些问题抽象成图，从一个点开始，向四周开始扩散。

**BFS 算法框架步骤：**

1. 用**「队列」**这种数据结构
2. 每次将每个还没有搜索到的点依次放入队列
3. 然后再弹出队列的头部元素当做当前遍历点

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
        #		 	queue.append(该节点)
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
            for _ in range(sz):
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

3. #### [101. 对称二叉树](https://leetcode-cn.com/problems/symmetric-tree/)

   ```python
   # Definition for a binary tree node.
   # class TreeNode:
   #     def __init__(self, x):
   #         self.val = x
   #         self.left = None
   #         self.right = None
   
   class Solution:
       def isSymmetric(self, root: TreeNode) -> bool:
           def isSame(left, right):
               if not left and not right:
                   return True
               if not left or not right:
                   return False
               if left.val != right.val:
                   return False           
               return isSame(left.left, right.right) and isSame(left.right, right.left)
           
           if not root:
               return True
           return isSame(root.left, root.right)
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

### 二叉树算法的设计框架总结

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



# 回溯算法专题

**解决一个回溯问题，实际上就是一个决策树的遍历过程**。你只需要思考 3 个问题：

1. 路径：也就是已经做出的选择。

2. 选择列表：也就是你当前可以做的选择。

3. 结束条件：也就是到达决策树底层，无法再做选择的条件。

代码方面，回溯算法的框架：

```python
def trackback(选择列表, 路径):
    if 满足结束条件:
        res.append(路径)
        return

    for 选择 in 选择列表:
        路径.append(选择) # 做选择
        trackback(路径, 选择列表)	# 进入下一层决策树
        路径.pop() # 撤销选择
res = []
trackBack(nums, [])
return res
```

**其核心就是 for 循环里面的递归，在递归调用之前「做选择」，在递归调用之后「撤销选择」**。

## [46. 全排列](https://leetcode-cn.com/problems/permutations/)

<img src="https://tva1.sinaimg.cn/large/007S8ZIlly1ghxc0fmdqsj31360l21kx.jpg" alt="image-20200820155728193" style="zoom: 33%;" />

只要从根遍历这棵树，记录路径上的数字，其实就是所有的全排列。**我们不妨把这棵树称为回溯算法的「决策树」**。

**为啥说这是决策树呢，因为你在每个节点上其实都在做决策**。比如说你站在上图的红色节点上：

你现在就在做决策，可以选择 1 那条树枝，也可以选择 3 那条树枝。为啥只能在 1 和 3 之中选择呢？
因为 2 这个树枝在你身后，这个选择你之前做过了，而全排列是不允许重复使用数字的。

**现在可以解答开头的几个名词：`[2]`就是「路径」，记录你已经做过的选择；`[1,3]`就是「选择列表」，表示你当前可以做出的选择；「结束条件」就是遍历到树的底层，在这里就是选择列表为空的时候**。

如果明白了这几个名词，**可以把「路径」和「选择」列表作为决策树上每个节点的属性**，比如下图列出了几个节点的属性：

<img src="https://tva1.sinaimg.cn/large/007S8ZIlly1ghxc4akmz8j313k0ne7wh.jpg" alt="image-20200820160113667" style="zoom:33%;" />

**我们定义的** **`backtrack`** **函数其实就像一个指针，在这棵树上游走，同时要正确维护每个节点的属性，每当走到树的底层，其「路径」就是一个全排列**。

再进一步，如何遍历一棵树？各种搜索问题其实都是树的遍历问题，而多叉树的遍历框架就是这样：

```python
def traverse(root):
    for (TreeNode child : root.childern)
        # 前序遍历需要的操作
        traverse(child)
        # 后序遍历需要的操作
```

而所谓的前序遍历和后序遍历，他们只是两个很有用的时间点，如图：

<img src="https://tva1.sinaimg.cn/large/007S8ZIlly1ghxeeyhsx8j30ui0iqx0e.jpg" alt="image-20200820172039951" style="zoom:40%;" />

**前序遍历的代码在进入某一个节点之前的那个时间点执行，后序遍历代码在离开某个节点之后的那个时间点执行**。

「路径」和「选择」是每个节点的属性，函数在树上游走要正确维护节点的属性，那么就要在这两个特殊时间点搞点动作：

<img src="https://tva1.sinaimg.cn/large/007S8ZIlly1ghxegdc39mj312o0l64qp.jpg" alt="image-20200820172201371" style="zoom:33%;" />

现在再来看回溯算法的这段核心框架：

```python
def trackback(选择列表, 路径):
    if 满足结束条件:
        res.append(路径)
        return

    for 选择 in 选择列表:
        路径.append(选择) # 做选择
        trackback(路径, 选择列表)	# 进入下一层决策树
        路径.pop() # 撤销选择
res = []
trackBack(nums, [])
return res
```

**我们只要在递归之前做出选择，在递归之后撤销刚才的选择**，就能正确得到每个节点的选择列表和路径。

下面，直接看全排列代码：

```python
class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        # 路径：选择的元素记录在 track 中
        # 选择列表：nums 中不存在于 track 的那些元素
        # 结束条件：nums 中的元素全都在 track 中出现
        def trackBack(nums, track):
            # 触发结束条件
            if len(track) == len(nums):
                res.append(track[:])   # 需要传递下track的拷贝，否则对track的修改会影响到结果
                return
            for i in nums:
                # 排除不合法的选择
                if i in track:
                    continue
                track.append(i)   # 做选择
                trackBack(nums, track)   # 进入下一层决策树
                track.pop()   # 取消选择
        res = []
        trackBack(nums, [])
        return res
```

## [77. 组合](https://leetcode-cn.com/problems/combinations/)

这就是典型的回溯算法，`k` 限制了树的高度，`n` 限制了树的宽度，直接套回溯算法模板框架就行了：

```python
class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        def trackback(start, track):
            # 到达树的底部
            if k == len(track):
                res.append(track[:])
                return
            # 注意 i 从 start 开始递增
            for i in range(start, n+1):
                # if i in track:	# 注意这里不需要再判断，因为 i 每次都是从 i+1 开始，
                #    continue		# 所以track每次append的 i 值都不一样
                track.append(i)	# 做选择
                trackback(i+1, track)
                track.pop()	 # 撤销选择   
        res = []
        trackback(1, [])
        return res
```

## [78. 子集](https://leetcode-cn.com/problems/subsets/)

```python
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        def trackback(start, track):
            res.append(track[:])
            for i in range(start, len(nums)):
                track.append(nums[i])
                trackback(i+1, track)
                track.pop()
        res = []
        trackback(0, [])
        return res
```

与排列问题不同，组合问题和子集问题都不能有重复元素，故回溯时都从当前位置的下一个位置开始。



# 双指针 & 滑动窗口专题

## 快慢指针

主要解决链表中的问题，比如典型的判定链表中是否包含环。

**快慢指针一般都初始化指向链表的头结点 head，前进时快指针 fast 在前，慢指针 slow 在后，巧妙解决一些链表中的问题。**

### [876. 链表的中间结点](https://leetcode-cn.com/problems/middle-of-the-linked-list/)

让快指针一次前进两步，慢指针一次前进一步，当快指针到达链表尽头时，慢指针就处于链表的中间位置。

```python
class Solution:
    def middleNode(self, head: ListNode) -> ListNode:
        slow, fast = head, head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow
```

### [141. 环形链表](https://leetcode-cn.com/problems/linked-list-cycle/)

分析：单链表的特点是每个节点只知道下一个节点，所以一个指针的话无法判断链表中是否含有环的。

如果链表中不含环：这个指针最终会遇到空指针`None`表示链表到头了，可以判断该链表不含环。
如果链表中含有环：这个指针就会陷入死循环，因为环形数组中没有`None`指针作为尾部节点。

**经典解法就是用两个指针，一个每次前进两步，一个每次前进一步。**
如果不含有环，跑得快的那个指针最终会遇到 `None`，说明链表不含环；
如果含有环，快指针最终会超慢指针一圈，和慢指针相遇，说明链表含有环。

```python
class Solution:
    def hasCycle(self, head: ListNode) -> bool:
        slow, fast = head, head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                return True
        return False
```

### [142. 环形链表 II](https://leetcode-cn.com/problems/linked-list-cycle-ii/)

分析：第一次相遇时，假设慢指针 slow 走了 k 步，那么快指针 fast 一定走了 2k 步，也就是说比 slow 多走了 k 步（也就是环的长度）。

<img src="https://mmbiz.qpic.cn/mmbiz_png/map09icNxZ4lFDturGXicxrn2F0wKQPgocMTLbYubOMnV8BG7fkHKw7cIKV43yOlzzuNOwvFW7eVsPbgC30FG2rQ/640?wx_fmt=png&amp;wxfrom=5&amp;wx_lazy=1&amp;wx_co=1" alt="img" style="zoom: 50%;" />

设相遇点距环的起点的距离为 m，那么环的起点距头结点 head 的距离为 k - m，也就是说如果从 head 前进 k - m 步就能到达环起点。
巧的是，如果从相遇点继续前进 k - m 步，也恰好到达环起点。

<img src="https://mmbiz.qpic.cn/mmbiz_png/map09icNxZ4lFDturGXicxrn2F0wKQPgocgdhvrjrUt8ibD3PXJomkhSBk5CPubhUQCxiaw2bwJwKP7Y3ODBZc5xag/640?wx_fmt=png&amp;wxfrom=5&amp;wx_lazy=1&amp;wx_co=1" alt="img" style="zoom:50%;" />

所以，只要相遇后我们把快慢指针中的任一个重新指向 head，然后两个指针同速前进，k - m 步后就会相遇，相遇之处就是环的起点了。

```python
class Solution:
    def detectCycle(self, head: ListNode) -> ListNode:
        slow, fast = head, head
        while True:
            if not (fast and fast.next): 
                return
            slow = slow.next
            fast = fast.next.next
            if fast == slow: 
                break
        slow = head
        while slow != fast:
            slow = slow.next
            fast = fast.next
        return slow
```

### [剑指 Offer 22. 链表中倒数第k个节点](https://leetcode-cn.com/problems/lian-biao-zhong-dao-shu-di-kge-jie-dian-lcof/)

思路还是使用快慢指针：让快指针先走 k 步，然后快慢指针开始同速前进。
这样当快指针走到链表末尾 null 时，慢指针所在的位置就是倒数第 k 个链表节点：

```python
class Solution:
    def getKthFromEnd(self, head: ListNode, k: int) -> ListNode:
        slow, fast = head, head
        while k != 0:
            fast = fast.next
            k -= 1
        while fast:
            slow = slow.next
            fast = fast.next
        return slow
```

## 左右指针

主要解决数组（或者字符串）中的问题，比如二分查找。

**左右指针在数组中实际是指两个索引值，一般初始化为 `left = 0`, `right = nums.length - 1`**

### 二分查找

#### 二分查找框架

对于寻找左右边界的二分搜索，常见的手法是使用左闭右开的「搜索区间」，**根据逻辑将「搜索区间」全都统一成两端都闭，便于记忆，只要修改两处即可变化出三种写法：**

```python
# 寻找一个数（基本的二分搜索）
def binary_search(nums, target):
    left, right = 0, len(nums) - 1 
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] < target:
            left = mid + 1
        elif nums[mid] > target:
            right = mid - 1
        elif nums[mid] == target:
            # 直接返回
            return mid
    # 直接返回
    return -1

# 寻找左侧边界的二分搜索
def left_bound(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] < target:
            left = mid + 1
        elif nums[mid] > target:
            right = mid - 1
        elif nums[mid] == target:
            # 别返回，锁定左侧边界
            right = mid - 1
    # 最后要检查 left 越界的情况
    if left >= len(nums) or nums[left] != target:
        return -1
    return left

# 寻找右侧边界的二分搜索
def right_bound(nums, target):        
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] < target:
            left = mid + 1
        elif nums[mid] > target:
            right = mid - 1
        elif nums[mid] == target:
            # 别返回，锁定右侧边界
            left = mid + 1
    # 最后要检查 right 越界的情况
    if right < 0 or nums[right] != target:
        return -1
    return right
```

#### [704. 二分查找](https://leetcode-cn.com/problems/binary-search/)

```python
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums)-1

        while left <= right:
            mid = (left+right) // 2
            if target < nums[mid] :
                right = mid - 1
            elif target > nums[mid]:
                left = mid + 1
            else:
                return mid
        return -1
```

#### [34. 在排序数组中查找元素的第一个和最后一个位置](https://leetcode-cn.com/problems/find-first-and-last-position-of-element-in-sorted-array/)

```python
class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        if not nums or len(nums) == 0:
            return [-1, -1]
        left, right = -1, -1

        # left bounder
        start, end = 0, len(nums) - 1
        while start <= end:
            mid = start + ((end - start) // 2)
            if target < nums[mid]:
                end = mid - 1
            elif target > nums[mid]:
                start = mid + 1
            else:
                end = mid - 1
        left = end + 1
        if left >= len(nums) or nums[left] != target:
            return [-1, -1]

        # right bounder
        start, end = 0, len(nums) - 1
        while start <= end:
            mid = start + ((end - start) // 2)
            if target > nums[mid]:
                start = mid + 1
            elif target < nums[mid]:
                end = mid - 1
            else:
                start = mid + 1
        right = start - 1
        if right < 0 or nums[right] != target:
            return [-1, -1]

        return [left, right]
```



### [167. 两数之和 II - 输入有序数组](https://leetcode-cn.com/problems/two-sum-ii-input-array-is-sorted/)

**只要数组有序，就应该想到双指针技巧。这道题的解法有点类似二分查找，通过调节 left 和 right 可以调整 sum 的大小**

```python
class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        left, right = 0, len(numbers)-1
        while left < right:
            sum_val = numbers[left] + numbers[right]
            if sum_val == target:
                return [left+1, right+1]
            elif sum_val < target:
                left += 1
            else:
                right -= 1
```

### 滑动窗口算法

这个算法技巧的思路就是维护一个窗口，不断滑动，然后更新答案。该算法的大致逻辑如下：

```python
window = {}
left = right = 0, 0

while right < len(s):
    # 增大窗口
	window[s[right]] = window.get(s[right], 0) + 1
	right += 1
    while (window needs shrink):
        # 缩小窗口
        window[s[left]] -= 1
        left += 1
```

**滑动窗口算法框架**

```python
def slidingWindow(s, t):
    need, window = {}, {}
    for c in t:
    	need[c] = need.get(c, 0) + 1

    left, right = 0, 0
    valid = 0
    while right < len(s):
        # c 是将移入窗口的字符
        c = s[right]
        # 右移窗口
        right += 1
        # 进行窗口内数据的一系列更新
        ...

        # 判断左侧窗口是否要收缩
        while (window needs shrink):
            # d 是将移出窗口的字符
            d = s[left]
            # 左移窗口
            left += 1
            # 进行窗口内数据的一系列更新
            ...
```

**其中两处`...`表示的更新窗口数据的地方，到时候你直接往里面填就行了**。

而且，这两个`...`处的操作分别是右移和左移窗口更新操作，它们操作是完全对称的。

#### [76. 最小覆盖子串](https://leetcode-cn.com/problems/minimum-window-substring/)

**滑动窗口算法思路：**

1. 我们在字符串`S`中使用双指针中的左右指针技巧，初始化`left = right = 0`，**把索引左闭右开区间`[left, right)`称为一个「窗口」**。

2. 我们先不断地增加`right`指针扩大窗口`[left, right)`，直到窗口中的字符串符合要求（包含了`T`中的所有字符）。

3. 此时，我们停止增加`right`，转而不断增加`left`指针缩小窗口`[left, right)`，直到窗口中的字符串不再符合要求（不包含`T`中的所有字符了）。同时，每次增加`left`，我们都要更新一轮结果。

4. 重复第 2 和第 3 步，直到`right`到达字符串`S`的尽头。

> **第 2 步相当于在寻找一个「可行解」，然后第 3 步在优化这个「可行解」，最终找到最优解，**也就是最短的覆盖子串。左右指针轮流前进，窗口大小增增减减，窗口不断向右滑动，这就是「滑动窗口」这个名字的来历。

下面画图理解一下，`needs`和`window`相当于计数器，分别记录`T`中字符出现次数和「窗口」中的相应字符的出现次数。

*初始状态：*

<img src="https://mmbiz.qpic.cn/sz_mmbiz_png/gibkIz0MVqdGQlBxOlAet1AXGPoibCzEow6FwvAvsZKyCTCtrmLcvKDxhYAJEqI36cAZxfoIWLFibEhmz9IfHf24Q/640?wx_fmt=png&amp;wxfrom=5&amp;wx_lazy=1&amp;wx_co=1" alt="img" style="zoom: 50%;" />

*增加`right`，直到窗口`[left, right)`包含了`T`中所有字符：*

<img src="https://mmbiz.qpic.cn/sz_mmbiz_png/gibkIz0MVqdGQlBxOlAet1AXGPoibCzEowCyAS47jbjAGEfqUVRzkKDWbT6Y8JiarUicPMVR2yI72X3X6hjBGj4bGw/640?wx_fmt=png&amp;wxfrom=5&amp;wx_lazy=1&amp;wx_co=1" alt="img" style="zoom:50%;" />

*现在开始增加`left`，缩小窗口`[left, right)`：*

<img src="https://mmbiz.qpic.cn/sz_mmbiz_png/gibkIz0MVqdGQlBxOlAet1AXGPoibCzEowoE6BjdgVFKZwEb1q6VibCzIsNuoYmHuNicVdlDibQrQD6lRJbibjkBxO4A/640?wx_fmt=png&amp;wxfrom=5&amp;wx_lazy=1&amp;wx_co=1" alt="img" style="zoom:50%;" />

*直到窗口中的字符串不再符合要求，`left`不再继续移动：*

<img src="https://mmbiz.qpic.cn/sz_mmbiz_png/gibkIz0MVqdGQlBxOlAet1AXGPoibCzEowZQrqU81dPoEicq1J93aicY0A70IdicorFC5kfhJKa66CibKQTJxY4A60jA/640?wx_fmt=png&amp;wxfrom=5&amp;wx_lazy=1&amp;wx_co=1" alt="img" style="zoom:50%;" />

之后重复上述过程，先移动`right`，再移动`left`…… 直到`right`指针到达字符串`S`的末端，算法结束。

**现在我们来看看这个滑动窗口代码框架怎么用：**

首先，初始化`window`和`need`两个哈希表（字典），记录窗口中的字符和需要凑齐的字符：

```python
need, window = {}, {}
for c in t:
    need[c] = need.get(c, 0) + 1
# 或者直接用：need = Counter(t)
```

然后，使用`left`和`right`变量初始化窗口的两端，注意区间`[left, right)`是左闭右开的，所以初始情况下窗口没有包含任何元素：

```python
left, right = 0, 0
valid = 0
while right < len(s):
    # 开始滑动
```

**其中`valid`变量表示窗口中满足`need`条件的字符个数**，如果`valid`和`len(need)`的大小相同，则说明窗口已满足条件，已经完全覆盖了串`T`。

**现在开始套模板，只需要思考以下四个问题**：

1. 当移动`right`扩大窗口，即加入字符时，应该更新哪些数据？
2. 当移动`left`缩小窗口，即移出字符时，应该更新哪些数据？
3. 什么条件下，窗口应该暂停扩大，开始移动`left`缩小窗口？
4. 我们要的结果应该在扩大窗口时还是缩小窗口时进行更新？

**回答：**

1. 如果一个字符进入窗口，应该增加`window`计数器；
2. 如果一个字符将移出窗口的时候，应该减少`window`计数器；
3. 当`valid`满足`need`时应该收缩窗口；
4. 应该在收缩窗口的时候更新最终结果。

完整代码：

```python
class Solution:
    def minWindow(self, s: str, t: str) -> str:
        need, window = {}, {}
        for c in t:
            need[c] = need.get(c, 0) + 1

        left, right = 0, 0
        valid = 0	# 表示窗口中满足 need 条件的字符个数
        # 记录最小覆盖子串的起始索引及长度
        start = 0
        valid_len = float('inf')
        while right < len(s):
            c = s[right]	# c 是将移入窗口的字符
            right += 1		# 右移窗口
            # 进行窗口内数据的一系列更新
            if c in need:
                window[c] = window.get(c, 0) + 1
                # 验证包含字符的数量
                if window[c] == need[c]:
                    valid += 1

            # 判断左侧窗口是否要收缩
            while valid == len(need):
                # 在这里更新最小覆盖子串
                if right - left < valid_len:
                    start = left
                    valid_len = right - left
                d = s[left]	  # d 是将移出窗口的字符
                left += 1	# 左移窗口
                # 进行窗口内数据的一系列更新
                if d in need:
                    if window[d] == need[d]:
                        valid -= 1	# 为了停止收缩
                    window[d] -= 1	# 移出多余的包含字符
        # 返回最小覆盖子串
        if valid_len == float('inf'):
            return ""
       	else:
            return s[start:start+valid_len]
```

需要注意的是：

1. 当我们发现某个字符在`window`的数量满足了`need`的需要，就要更新`valid`，表示有一个字符已经满足要求。而且两次对窗口内数据的更新操作是完全对称的。
2. 当`valid == len(need)`时，说明`T`中所有字符已经被覆盖，已经得到一个可行的覆盖子串，现在应该开始收缩窗口了，以便得到「最小覆盖子串」。
3. 移动`left`收缩窗口时，窗口内的字符都是可行解，所以应该在收缩窗口的阶段进行最小覆盖子串的更新，以便从可行解中找到长度最短的最终结果。

#### [567. 字符串的排列](https://leetcode-cn.com/problems/permutation-in-string/)

对于这道题的解法代码，基本上和最小覆盖子串一模一样，只需要改变两个地方：

1. 本题移动`left`缩小窗口的时机是窗口大小大于`len(s2)`时，因为排列嘛，显然长度应该是一样的。
2. 当发现`valid == len(need)`时，就说明窗口中就是一个合法的排列，所以立即返回`True`。

至于如何处理窗口的扩大和缩小，和最小覆盖子串完全相同。

```python
class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        need = Counter(s1)
        window = {}

        left, right = 0, 0
        valid = 0

        while right < len(s2):
            c = s2[right]
            right += 1
            if c in need:
                window[c] = window.get(c, 0) + 1
                if window[c] == need[c]:
                    valid += 1

            while right-left >= len(s1):
                if valid == len(need):
                    return True
                d = s2[left]
                left += 1
                if d in need:
                    if window[d] == need[d]:
                        valid -= 1
                    window[d] -= 1
        return False
```

#### [438. 找到字符串中所有字母异位词](https://leetcode-cn.com/problems/find-all-anagrams-in-a-string/)

```python
def findAnagrams(self, s: str, p: str) -> List[int]:  
        need = Counter(p)
        window = {}

        left, right = 0, 0
        valid = 0
        res = []

        while right < len(s):
            c = s[right]
            right += 1
            if c in need:
                window[c] = window.get(c, 0) + 1
                if window[c] == need[c]:
                    valid += 1
            while right-left >= len(p):
                if valid == len(need):
                    res.append(left)
                d = s[left]
                left += 1
                if d in need:
                    if window[d] == need[d]:
                        valid -= 1
                    window[d] -= 1
        return res
```

#### [3. 无重复字符的最长子串](https://leetcode-cn.com/problems/longest-substring-without-repeating-characters/)

这次不需要`need`和`valid`，而且更新窗口内数据也只需要简单的更新计数器`window`即可。

当`window[c]`值大于 1 时，说明窗口中存在重复字符，不符合条件，就该移动`left`缩小窗口了。

唯一需要注意的是，在哪里更新结果`res`呢？我们要的是最长无重复子串，哪一个阶段可以保证窗口中的字符串是没有重复的呢？

这里和之前不一样，**要在收缩窗口完成后更新`res`**，因为窗口收缩的 while 条件是存在重复元素，换句话说收缩完成后一定保证窗口中没有重复。

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        window = {}
        left, right = 0, 0
        res = 0

        while right < len(s):
            c = s[right]
            right += 1
            window[c] = window.get(c, 0) + 1
            # 收缩左侧窗口
            while window[c] > 1:
                d = s[left]
                left += 1
                window[d] -= 1
            res = max(res, right-left)
        return res
```



# 动态规划专题

动态规划问题的一般形式就是**求最值**。求解动态规划的核心问题是**穷举**。

首先，动态规划的穷举有点特别，因为这类问题**存在「重叠子问题」**，如果暴力穷举的话效率会极其低下，所以需要**「备忘录」**或者**「DP table」**来优化穷举过程，避免不必要的计算。

> **优化穷举的前提：存在「重叠子问题」**
>
> **优化穷举的方法：「备忘录」、「DP table」**

而且，动态规划问题一定会**具备「最优子结构」**，才能通过子问题的最值得到原问题的最值。

> **进行穷举的前提：具备「最优子结构」**

另外，虽然动态规划的核心思想就是穷举求最值，但是问题可以千变万化，穷举所有可行解其实并不是一件容易的事，只有列出**正确的「状态转移方程」**才能**正确地穷举**。

> **正确穷举的方法：「状态转移方程」**

以上提到的**重叠子问题、最优子结构、状态转移方程**就是动态规划三要素。在实际的算法问题中，**写出状态转移方程是最困难的**，这里提供一个思维框架，辅助思考状态转移方程：

**明确 base case -> 明确「状态」-> 明确「选择」 -> 定义 dp 数组/函数的含义**。

```python
# 初始化 base case
dp[0][0][...] = base
# 进行状态转移
for 状态1 in 状态1的所有取值：
    for 状态2 in 状态2的所有取值：
        for ...
            dp[状态1][状态2][...] = 求最值(选择1，选择2...)
```

## 509. [斐波那契数](https://leetcode-cn.com/problems/fibonacci-number/)

```python
class Solution:
    def fib(self, N: int) -> int:
        if N < 1:
            return 0
        if N < 2:
            return 1            
        dp = [0] * (N+1)
        # base case
        dp[1] = dp[2] = 1
        for i in range(3, N+1):
            dp[i] = dp[i - 1] + dp[i - 2]
        return dp[N]
```

「**状态压缩**」：如果我们发现每次状态转移只需要 DP table 中的一部分，那么可以尝试用状态压缩来缩小 DP table 的大小，只记录必要的数据。

根据斐波那契数列的状态转移方程，当前状态只和之前的两个状态有关，其实并不需要那么长的一个 DP table 来存储所有的状态，只要想办法存储之前的两个状态就行了。所以，可以进一步优化，把DP table 的大小从 `n` 缩小到 2，把空间复杂度降为 O(1)：

```python
class Solution:
    def fib(self, N: int) -> int:
        if N < 1:
            return 0
        if N < 2:
            return 1
        pre, cur = 1, 1
        for _ in range(3, N+1):
            sum_val = pre + cur
            pre = cur
            cur = sum_val
        return cur
```

斐波那契数列的例子严格来说不算动态规划，因为没有涉及求最值，以上旨在说明重叠子问题的消除方法，演示得到最优解法逐步求精的过程。下面，看第二个例子，凑零钱问题。

## [322. 零钱兑换](https://leetcode-cn.com/problems/coin-change/)

首先，这个问题是动态规划问题，因为它具有「最优子结构」。**要符合「最优子结构」，子问题间必须互相独立**。

比如你想求 `amount = 11` 时的最少硬币数（原问题），如果你知道凑出 `amount = 10` 的最少硬币数（子问题），你只需要把子问题的答案加一（再选一枚面值为 1 的硬币）就是原问题的答案。因为硬币的数量是没有限制的，所以子问题之间没有相互制，是互相独立的。

那么，既然知道了这是个动态规划问题，就要思考**如何列出正确的状态转移方程**？

1、**确定 base case：**显然目标金额 `amount` 为 0 时算法返回 0，因为不需要任何硬币就已经凑出目标金额了。

2、**确定「状态」：也就是原问题和子问题中会变化的变量**。由于硬币数量无限，硬币的面额也是题目给定的，只有目标金额会不断地向 base case 靠近，所以唯一的「状态」就是目标金额 `amount`。

3、**确定「选择」：也就是导致「状态」产生变化的行为**。目标金额为什么变化呢，因为你在选择硬币，你每选择一枚硬币，就相当于减少了目标金额。所以说所有硬币的面值，就是你的「选择」。

4、**明确 `dp` 函数/数组的定义**：我们自底向上使用 dp table 来消除重叠子问题。

* 一般来说数组的索引就是状态转移中会变化的量，也就是上面说到的「状态」；
* 数组索引值就是题目要求我们计算的量，即凑出目标金额所需的最少硬币数量。

就本题来说，状态只有一个，即「目标金额」，题目要求我们计算凑出目标金额所需的最少硬币数量。所以`dp`数组的定义把「状态」，也就是目标金额作为变量。：

**`dp`数组的定义：当目标金额为 `i` 时，至少需要`dp[i]` 枚硬币凑出。**

根据开头给出的动态规划代码框架可以写出如下解法：

```python
class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        # 数组大小为 amount + 1，初始值也为 amount + 1
        dp = [amount + 1] * (amount + 1)
        # base case
        dp[0] = 0
        # 外层 for 循环在遍历所有状态的所有取值
        for i in range(len(dp)):
            # 内层 for 循环在求所有选择的最小值
            for coin in coins:
                # 子问题无解，跳过
                if i - coin < 0:
                    continue
                dp[i] = min(dp[i], 1 + dp[i - coin])
        if dp[amount] == amount + 1:
            return -1
        else:
            return dp[amount]
```

## [300. 最长上升子序列](https://leetcode-cn.com/problems/longest-increasing-subsequence/) 

**动态规划的核心设计思想是「数学归纳法」**

我们设计动态规划算法，不是需要一个 dp 数组吗？我们可以**假设 dp[0...i−1] 都已经被算出来了，然后想：怎么通过这些结果算出dp[i] ?**

直接拿最长递增子序列这个问题举例你就明白了。不过，**首先要定义清楚 dp 数组的含义，即 dp[i] 的值到底代表着什么？**

1. 我们的定义是这样的：**dp[i] 表示以 nums[i] 这个数结尾的最长递增子序列的长度。**

根据这个定义，我们的最终结果（子序列的最大长度）应该是 dp 数组中的最大值：`max(dp)`

2. 我们应该怎么设计算法逻辑来正确计算每个 dp[i] 呢？这就是动态规划的重头戏了，要思考如何进行状态转移，这里就可以使用数学归纳的思想：

<img src="https://tva1.sinaimg.cn/large/007S8ZIlly1ghtnc2j7ejj30lc0du40d.jpg" alt="image-20200817112658844" style="zoom: 50%;" />

比如我们已经知道了 dp[0...4] 的所有结果，我们如何通过这些已知结果推出 dp[5]呢？

根据刚才我们对 dp 数组的定义，现在想求 dp[5] 的值，也就是想求以 nums[5] 为结尾的最长递增子序列。

nums[5] = 3，既然是递增子序列，我们只要找到前面那些结尾比 3 小的子序列，然后把 3 接到最后，就可以形成一个新的递增子序列，而且这个新的子序列长度加 1。

当然，可能形成很多种新的子序列，但是我们只要最长的，把最长子序列的长度作为 dp[5] 的值即可。

```python
for j in range(i):
  	if nums[j] < nums[i]:
        dp[i] = max(dp[i], dp[j] + 1)
```

3. 这段代码的逻辑就可以算出 dp[5]。到这里，这道算法题我们就基本做完了。类似数学归纳法，你已经可以通过 dp[0...4] 算出 dp[5] 了，那么任意 dp[i] 你肯定都可以算出来：

```python
for i in range(len(dp)):
    for j in range(i):
  		if nums[j] < nums[i]:
        	dp[i] = max(dp[i], dp[j] + 1)
```

4. 还有一个细节问题，就是 base case。dp 数组应该全部初始化为 1，因为子序列最少也要包含自己，所以长度最小为 1。下面我们看一下完整代码：

```python
class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        length = len(nums)
        if length == 0:
            return length
        dp = [1] * length

        for i in range(length):
            for j in range(i):
                if nums[j] < nums [i]:
                    dp[i] = max(dp[i], dp[j]+1)
        return max(dp)
```

至此，这道题就解决了，时间复杂度 O(N^2)。

**如何设计dp数组小结**

1. 首先明确 dp 数组所存数据的含义。这步很重要，如果不得当或者不够清晰，会阻碍之后的步骤。

2. 然后根据 dp 数组的定义，运用数学归纳法的思想，假设 dp[0...i−1] 都已知，想办法求出 dp[i]，

   一旦这一步完成，整个题目基本就解决了。但如果无法完成这一步，很可能就是 dp 数组的定义不够恰当，需要重新定义 dp 数组的含义；或者可能是 dp 数组存储的信息还不够，不足以推出下一步的答案，需要把 dp 数组扩大成二维数组甚至三维数组。

## [53. 最大子序和](https://leetcode-cn.com/problems/maximum-subarray/)

其实第一次看到这道题，首先可能想到的是滑动窗口算法，因为滑动窗口算法就是专门处理子串/子数组问题的，这里不就是子数组问题么？但是，稍加分析就发现，**这道题还不能用滑动窗口算法，因为数组中的数字可以是负数**。

滑动窗口算法无非就是双指针形成的窗口扫描整个数组/子串，但关键是，你得清楚地知道什么时候应该移动右侧指针来扩大窗口，什么时候移动左侧指针来减小窗口。

而对于这道题目，你想想，当窗口扩大的时候可能遇到负数，窗口中的值也就可能增加也可能减少，这种情况下不知道什么时机去收缩左侧窗口，也就无法求出「最大子数组和」。

解决这个问题需要动态规划技巧，但是 `dp` 数组的定义比较特殊。按照我们常规的动态规划思路，一般是这样定义 `dp` 数组：

**`nums[0..i]`中的「最大的子数组和」为`dp[i]`**。

如果这样定义的话，整个 `nums` 数组的「最大子数组和」就是 `dp[n-1]`。如何找状态转移方程呢？按照数学归纳法，假设我们知道了 `dp[i-1]`，如何推导出 `dp[i]` 呢？

如下图，按照我们刚才对 `dp` 数组的定义，`dp[i] = 5` ，也就是等于 `nums[0..i]` 中的最大子数组和：

<img src="https://tva1.sinaimg.cn/large/007S8ZIlly1ghtowfxb84j30tk0dm14i.jpg" alt="image-20200817122112008" style="zoom:33%;" />

那么在上图这种情况中，利用数学归纳法，你能用 `dp[i]` 推出 `dp[i+1]` 吗？

**实际上是不行的，因为子数组一定是连续的，按照我们当前** **`dp`** **数组定义，并不能保证** **`nums[0..i]`** **中的最大子数组与** **`nums[i+1]`** **是相邻的**，也就没办法从 `dp[i]` 推导出 `dp[i+1]`。

所以说我们这样定义 `dp` 数组是不正确的，无法得到合适的状态转移方程。对于这类子数组问题，我们就要重新定义 `dp` 数组的含义：

1. **以`nums[i]`为结尾的「最大子数组和」为`dp[i]`。**

这种定义之下，想得到整个 `nums` 数组的「最大子数组和」，不能直接返回 `dp[n-1]`，而要返回整个 `dp` 数组的最大值：`max(dp)`

接下来依然使用数学归纳法来找状态转移关系：假设我们已经算出了 `dp[i-1]`，如何推导出 `dp[i]` 呢？

可以做到，`dp[i]` 有两种「选择」，要么与前面的相邻子数组连接，形成一个和更大的子数组；要么不与前面的子数组连接，自成一派，自己作为一个子数组。

2. 如何选择？既然要求「最大子数组和」，当然选择结果更大的那个啦：

```python
# 要么自成一派，要么和前面的子数组合并
dp[i] = max(nums[i], nums[i] + dp[i - 1])
```

综上，我们已经写出了状态转移方程，就可以直接写出解法了：

```python
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        length = len(nums)
        if length == 0:
            return 0
       
        dp = [float('-inf')] * length
        # base case
        # 第一个元素前面没有子数组
        dp[0] = nums[0]
        # 状态转移方程
        for i in range(1, length):
            dp[i] = max(nums[i], nums[i]+dp[i-1])
        return max(dp)
```

以上解法时间复杂度是 O(N)，空间复杂度也是 O(N)，不过**注意到** **`dp[i]`** **仅仅和** **`dp[i-1]`** **的状态有关**，那么我们可以进行「状态压缩」，将空间复杂度降低：

```python
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        length = len(nums)
        if length == 0:
            return 0
        
        # base case
        res = dp_0 = nums[0]
        dp_1 = 0
        for i in range(1, length):
            # dp[i] = max(nums[i], nums[i] + dp[i-1])
            dp_1 = max(nums[i], nums[i] + dp_0)
            dp_0 = dp_1
            # 顺便计算最大的结果
            res = max(res, dp_1)
        return res
```

今天这道「最大子数组和」就和「最长递增子序列」非常类似，`dp` 数组的定义是**「以 `nums[i]` 为结尾的最大子数组和/最长递增子序列为 `dp[i]`」**。因为只有这样定义才能将 `dp[i+1]` 和 `dp[i]` 建立起联系，利用数学归纳法写出状态转移方程。



## 动态规划流程框架总结(0-1背包问题)

> 以经典0-1背包问题为例，描述：
>
> 给你一个可装载重量为 `W` 的背包和 `N` 个物品，每个物品有重量和价值两个属性。其中第 `i` 个物品的重量为 `wt[i]`，价值为 `val[i]`，现在让你用这个背包装物品，最多能装的价值是多少？

1. 要明确两点：**「状态」和「选择」**

   * **状态**：如何才能描述一个问题局面？只要给定几个可选物品和一个背包的容量限制，就形成了一个背包问题。
     * 所以状态有两个，就是：**「背包的容量」和「可选择的物品」**。
   * **选择**：对于每件物品，你能选择什么？
     * 选择就是：**「装进背包」或者「不装进背包」**。

   明白了状态和选择，动态规划问题基本上就解决了，只要往这个框架套就完事儿了：
   
   ```python
   for 状态1 in 状态1的所有取值:
       for 状态2 in 状态2的所有取值:
           for ...
               dp[状态1][状态2][...] = 择优(选择1，选择2...)
   ```
   
2. 要明确：**`dp`数组的定义**

   `dp`数组是什么？其实就是描述问题局面的一个数组。换句话说，我们刚才明确问题有什么「状态」，现在需要**用`dp`数组把状态表示出来**。

   首先看看刚才找到的「状态」，有两个，也就是说我们需要一个二维`dp`数组，一维表示可选择的物品，一维表示背包的重量。

   **`dp[i][w]`的定义如下：对于前`i`个物品，当前背包的容量为`w`，这种情况下可以装的最大价值是`dp[i][w]`。**

   比如说，如果 `dp[3][5]= 6`，其含义为：对于给定的一系列物品中，若只对前 3 个物品进行选择，当背包重量为 5 时，最多可以装下的价值为 6。

   PS：为什么要这么定义？便于状态转移，或者说这就是套路，记下来就行了。

   根据这个定义，**我们想求的最终答案就是`dp[N][W]`**。**base case 就是`dp[0][..] = dp[..][0] = 0`**，因为没有物品或者背包没有空间的时候，能装的最大价值就是 0。

   细化上面的框架：
   
   ```python
   dp[N+1][W+1]
   dp[0][..] = 0
   dp[..][0] = 0
   
   for i in range(1, N+1):
       for w in range(1, W+1):
           dp[i][w] = max(把物品 i 装进背包, 不把物品 i 装进背包)
   return dp[N][W]
   ```
   
3. **根据「选择」，思考状态转移的逻辑**

   简单说就是，上面伪码中「把物品`i`装进背包」和「不把物品`i`装进背包」怎么用代码体现出来呢？

   这一步要结合对`dp`数组的定义和我们的算法逻辑来分析：

   先重申一下刚才我们的`dp`数组的定义：

   `dp[i][w]`表示：对于前`i`个物品，当前背包的容量为`w`时，这种情况下可以装下的最大价值是`dp[i][w]`。

   **如果你没有把这第`i`个物品装入背包：**那么最大价值`dp[i][w]`应该等于`dp[i-1][w]`。你不装嘛，那就继承之前的结果。

   **如果你把这第`i`个物品装入了背包：**那么`dp[i][w]`应该等于`dp[i-1][w-wt[i-1]] + val[i-1]`。

   **首先，由于`i`是从 1 开始的，所以对`val`和`wt`的取值是`i-1`。**

   而**`dp[i-1][w-wt[i-1]]`**也很好理解：你如果想装第`i`个物品，你怎么计算这时候的最大价值？换句话说，**在装第`i`个物品的前提下，背包能装的最大价值是多少？**

   显然，你应该**寻求剩余容量`w-wt[i-1]`限制下能装的最大价值，加上第`i`个物品的价值`val[i-1]`，这就是装第`i`个物品的前提下，背包可以装的最大价值**。

   综上就是两种选择，我们都已经分析完毕，也就是写出来了状态转移方程，可以进一步细化代码：
   
   ```python
   for i in range(1, N+1):
       for w in range(1, W+1):
           dp[i][w] = max(dp[i-1][w], dp[i-1][w - wt[i-1]] + val[i-1])
   return dp[N][W]
   ```
   
4. **把伪码翻译成代码，处理一些边界情况**

   ```python
   def knapsack(W, N, wt, val):
       # 初始化，先全部赋值为0，这样至少体积为0或者不选任何物品的时候是满足要求 
       dp = [[0]*(W+1) for j in range(N+1)]
       for i in range(1, N+1):
       	for w in range(1, W+1):
               # 当前背包容量装不下，只能选择不装入背包
               if wt[i-1] > w :
                   dp[i][w] = dp[i - 1][w]
               else:
                   # 装入或者不装入背包，择优
                   dp[i][w] = max(dp[i - 1][w - wt[i-1]] + val[i-1], dp[i - 1][w])
       return dp[N][W]
   ```

## [416. 分割等和子集](https://leetcode-cn.com/problems/partition-equal-subset-sum/)

> 对于这个问题，我们可以先对集合求和，得出 `sum`，把问题转化为背包问题：
>
> 给一个可装载重量为`sum / 2`的背包和`N`个物品，每个物品的重量为`nums[i]`。现在让你装物品，是否存在一种装法，能够恰好将背包装满？
>
> 其实这就是背包问题的模型，下面我们就直接转换成背包问题，开始套前文讲过的背包问题框架即可。

1. 「状态」和「选择」

   * **状态**：子集和（背包容量）、数组中的元素（可选择的物品）
   * **选择**：选元素（装进背包）、不选元素（不装进背包）

2. `dp`数组的定义

   按照背包问题的套路，可以给出如下定义：

   `dp[i][j] = x` 表示，对于前 `i` 个物品，当前背包的容量为 `j` 时，若 `x` 为 `true`，则说明可以恰好将背包装满，若 `x` 为 `false`，则说明不能恰好将背包装满。

   比如说，如果 `dp[4][9] = true`，其含义为：对于容量为 9 的背包，若只是用前 4 个物品，可以有一种方法把背包恰好装满。

   对于本题，含义是**对于给定的集合中，若只对前 4 个数字进行选择，存在一个子集的和可以恰好凑出 9**。

   根据这个定义，我们想求的**最终答案就是 `dp[N][sum/2]`**

   **base case 就是 `dp[..][0] = true` 和 `dp[0][..] = false`**，因为背包没有空间的时候，就相当于装满了；而当没有物品可选择的时候，肯定没办法装满背包。

3. 状态转移方程

   回想刚才的 `dp` 数组含义，可以根据「选择」对 `dp[i][j]` 得到以下状态转移：

   如果不把 `nums[i]` 算入子集，或者说你**不把这第`i`个物品装入背包**，那么是否能够恰好装满背包，取决于上一个状态 `dp[i-1][j]`，继承之前的结果。

   如果把 `nums[i]` 算入子集，或者说你**把这第`i`个物品装入了背包**，那么是否能够恰好装满背包，取决于状态 `dp[i-1][j-nums[i-1]]`。

   **首先，由于 `i` 是从 1 开始的，而数组索引是从 0 开始的，所以第 `i` 个物品的重量应该是 `nums[i-1]`，这一点不要搞混。**

   `dp[i-1][j-nums[i-1]]` 也很好理解：你如果装了第 `i` 个物品，就要看背包的剩余重量 `j - nums[i-1]` 限制下是否能够被恰好装满。

   换句话说，如果 `j - nums[i-1]` 的重量可以被恰好装满，那么只要把第 `i` 个物品装进去，也可恰好装满 `j` 的重量；否则的话，重量 `j` 肯定是装不满的。

4. 完整代码

   ```python
   class Solution:
       def canPartition(self, nums: List[int]) -> bool:
           sum_val = sum(nums)
           if sum_val % 2 == 1:
               return False
   
           target = sum_val // 2
           length = len(nums)
           dp = [[False] * (target + 1) for _ in range(length + 1)]
   
           for i in range(length + 1):
               dp[i][0] = True
   
           for i in range(1, length + 1):
               for j in range(1, target + 1):
                   if j - nums[i - 1] < 0:
                       # 背包容量不足，不能装入第 i 个物品
                       dp[i][j] = dp[i - 1][j]
                   else:
                       # 装入或不装入背包
                       dp[i][j] = dp[i - 1][j] or dp[i - 1][j - nums[i - 1]]
           return dp[-1][-1]
   ```

5. 代码优化（状态压缩）

   再进一步，是否可以优化这个代码呢？**注意到** **`dp[i][j]`** **都是通过上一行** **`dp[i-1][..]`** **转移过来的**，之前的数据都不会再使用了。所以，我们可以进行状态压缩，将二维 `dp` 数组压缩为一维，节约空间复杂度：

   ```python
   class Solution:
       def canPartition(self, nums: List[int]) -> bool:
           sum_val = sum(nums)
           if sum_val % 2 == 1:
               return False
   
           length = len(nums)
           target = sum_val // 2
           dp = [False]*(target+1)
   
           # base case
           dp[0] = True
   
           for i in range(length):
               for j in range(target, -1, -1):
                   if j >= nums[i]:
                       dp[j] = dp[j] or dp[j - nums[i]]
           return dp[-1]
   ```

   这就是状态压缩，其实这段代码和之前的解法思路完全相同，只在一行 `dp` 数组上操作，`i` 每进行一轮迭代，`dp[j]` 其实就相当于 `dp[i-1][j]`，所以只需要一维数组就够用了。

   **唯一需要注意的是** **`j`** **应该从后往前反向遍历，因为每个物品（或者说数字）只能用一次，以免之前的结果影响其他的结果**。

## [518. 零钱兑换 II](https://leetcode-cn.com/problems/coin-change-2/)

> **我们可以把这个问题转化为背包问题的描述形式**：
>
> 有一个背包，最大容量为 `amount`，有一系列物品 `coins`，每个物品的重量为 `coins[i]`，**每个物品的数量无限**。请问有多少种方法，能够把背包恰好装满？
>
> 这个问题和我们前面讲过的两个背包问题，有一个最大的区别就是，每个物品的数量是无限的，这也就是传说中的「**完全背包问题**」，没啥高大上的，无非就是状态转移方程有一点变化而已。
>
> 下面就以背包问题的描述形式，继续按照流程来分析。

1. 「状态」和「选择」

   状态：「背包的容量」和「可选择的物品」

   选择：「装进背包」或者「不装进背包」

   明白了状态和选择，动态规划问题基本上就解决了，只要往这个框架套就完事儿了：

   ```python
   for 状态1 in 状态1的所有取值：
       for 状态2 in 状态2的所有取值：
           for ...
               dp[状态1][状态2][...] = 计算(选择1，选择2...)
   ```

2. `dp`数组的定义

   「状态」有两个，也就是说我们需要一个二维 `dp` 数组。

   `dp[i][j]` 的定义如下：

   若只使用前 `i` 个物品，当背包容量为 `j` 时，有 `dp[i][j]` 种方法可以装满背包。

   换句话说，翻译回我们题目的意思就是：

   **若只使用`coins`中的前`i`个硬币的面值，若想凑出金额`j`，有`dp[i][j]`种凑法**。

   经过以上的定义，可以得到：**base case 为 `dp[0][..] = 0， dp[..][0] = 1`**。

   因为如果不使用任何硬币面值，就无法凑出任何金额；如果凑出的目标金额为 0，那么“无为而治”就是唯一的一种凑法。

   我们最终想得到的答案就是 `dp[N][amount]`，其中 `N` 为 `coins` 数组的大小。

   大致的伪码思路如下：
   
   ```python
   dp[N+1][amount+1]
   dp[0][..] = 0
   dp[..][0] = 1
   
   for i in [1..N]:
       for j in [1..amount]:
           把物品 i 装进背包,
           不把物品 i 装进背包
   return dp[N][amount]
   ```
   
3. 状态转移方程

   注意，我们这个问题的特殊点在于物品的数量是**无限**的，所以这里和之前写的背包问题文章有所不同。

   **如果你不把这第`i`个物品装入背包**，也就是说你不使用`coins[i]`这个面值的硬币，那么凑出面额 `j` 的方法数 `dp[i][j]` 应该等于 `dp[i-1][j]`，继承之前的结果。

   **如果你把这第`i`个物品装入了背包**，也就是说你使用`coins[i]`这个面值的硬币，那么`dp[i][j]`应该等于`dp[i][j-coins[i-1]]`

   > **首先由于 `i` 是从 1 开始的，所以 `coins` 的索引是 `i-1` 时表示第 `i` 个硬币的面值。**
   >
   > **`dp[i][j-coins[i-1]]`** 也不难理解，如果你决定使用这个面值的硬币，那么就应该关注如何凑出金额 `j - coins[i-1]`。
   >
   > 比如说，你想用面值为 2 的硬币凑出金额 5，那么如果你知道了凑出金额 3 的方法，再加上一枚面额为 2 的硬币，就可以凑出 5 。
   
      **综上就是两种选择，而我们想求的`dp[i][j]`是「共有多少种凑法」，所以`dp[i][j]`的值应该是以上两种选择的结果之和**：
   
   ```python
   for i in range(1, length+1):
               for j in range(1, amount+1):
                   if j >= coins[i-1]:
                       dp[i][j] = dp[i-1][j] + dp[i][j-coins[i-1]]
   ```

4. 完整代码

   ```python
   class Solution:
       def change(self, amount: int, coins: List[int]) -> int:
           length = len(coins)
           dp = [[0]*(amount+1) for _ in range(length+1)]
           # base case
           for i in range(length+1):
               dp[i][0] = 1
   
           for i in range(1, length+1):
               for j in range(1, amount+1):
                   if j < coins[i-1]:
                       dp[i][j] = dp[i-1][j]
                   else:
                       dp[i][j] = dp[i-1][j] + dp[i][j-coins[i-1]]
           return dp[-1][-1]
   ```

5. 代码优化（状态压缩）

   我们通过观察可以发现，`dp`数组的转移只和 dp[i][..]`和`dp[i-1][..]`有关，所以可以压缩状态，降低算法的空间复杂度：

   ```python
   class Solution:
       def change(self, amount: int, coins: List[int]) -> int:
           length = len(coins)
           dp = [0]*(amount+1)
           # base case
           dp[0] = 1
   
           for i in range(length):
               for j in range(1, amount+1):
                   if j >= coins[i]:
                       dp[j] = dp[j] + dp[j-coins[i]]
           return dp[-1]
   ```

   

## [1143. 最长公共子序列](https://leetcode-cn.com/problems/longest-common-subsequence/)

**只要涉及子序列问题，十有八九都需要动态规划来解决**，往这方面考虑就对了。

1. `dp`数组的定义

   对于两个字符串的动态规划问题，套路是通用的。比如说对于字符串 `s1` 和 `s2`，一般来说都要构造一个这样的 DP table：

<img src="https://tva1.sinaimg.cn/large/007S8ZIlly1ghv2zseq9bj314m0oi413.jpg" alt="image-20200818171420579" style="zoom:28%;" />

​	为了方便理解此表，我们暂时认为索引是从 1 开始的，待会的代码中只要稍作调整即可。

​	其中，**`dp[i][j]` 的含义是：对于 `s1[1..i]` 和 `s2[1..j]`，它们的 LCS 长度是 `dp[i][j]`**。
​	比如上图的例子，`d[2][4]`的含义就是：对于 `"ac"` 和 `"babc"`，它们的 LCS 长度是 2。我们最终想得到的答案应该是 `dp[3][6]`。

2. 定义base case

   **我们专门让索引为 0 的行和列表示空串，`dp[0][..]` 和 `dp[..][0]` 都应该初始化为 0，这就是 base case。**

   比如说，按照刚才 dp 数组的定义，`dp[0][3]=0` 的含义是：对于字符串 `""` 和 `"bab"`，其 LCS 的长度为 0。因为有一个字符串是空串，它们的最长公共子序列的长度显然应该是 0。

3. 状态转移方程

   这是动态规划最难的一步，不过好在这种字符串问题的套路都差不多，权且借这道题来聊聊处理这类问题的思路。

   **状态转移说简单些就是做选择。**比如说这个问题，是求 `s1` 和 `s2` 的最长公共子序列，不妨称这个子序列为 `lcs`。那么对于 `s1` 和 `s2` 中的每个字符，有什么选择？很简单，**两种选择，要么在 `lcs` 中，要么不在**。

   <img src="https://tva1.sinaimg.cn/large/007S8ZIlly1ghv4jz9t5vj313y0mwgn4.jpg" alt="image-20200818180822608" style="zoom: 25%;" />

   这个「在」和「不在」就是选择，关键是，应该如何选择呢？这个需要动点脑筋：如果某个字符应该在 `lcs` 中，那么这个字符肯定同时存在于 `s1` 和 `s2` 中，因为 `lcs` 是最长**公共**子序列嘛。所以本题的思路是这样：

   **用两个指针 `i` 和 `j` 从后往前遍历 `s1` 和 `s2`，如果 `s1[i]==s2[j]`，那么这个字符一定在 `lcs` 中；否则的话，`s1[i]` 和 `s2[j]` 这两个字符至少有一个不在 `lcs` 中，需要丢弃一个。**

4. 完整代码

   ```python
   class Solution:
       def longestCommonSubsequence(self, text1: str, text2: str) -> int:
           m, n = len(text1), len(text2)
           # 构建 DP table 和 base case
           dp = [[0] * (n+1) for _ in range(m+1)]
           # 进行状态转移
           for i in range(1, m + 1):
               for j in range(1, n + 1):
                   if text1[i-1] == text2[j-1]:
                       # 找到一个 lcs 中的字符
                       dp[i][j] = 1 + dp[i-1][j-1]
                   else:
                       # 谁能让 lcs 最长，就听谁的
                       dp[i][j] = max(dp[i-1][j], dp[i][j-1])
           return dp[-1][-1]
   ```

**疑难解答**

对于 `s1[i]` 和 `s2[j]` 不相等的情况，**至少有一个**字符不在 `lcs` 中，会不会两个字符都不在呢？比如下面这种情况：

<img src="https://tva1.sinaimg.cn/large/007S8ZIlly1ghv4zeqcx8j31400i475f.jpg" alt="image-20200818182311919" style="zoom: 30%;" />

所以代码是不是应该考虑这种情况，改成这样：

```python
if str1[i-1] == str2[j-1]:
    # ...
else:
    dp[i][j] = max(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
```

其实可以这样改，也能得到正确答案，但是多此一举，因为 `dp[i-1][j-1]` 永远是三者中最小的，max 根本不可能取到它。

原因在于我们对 dp 数组的定义：对于 `s1[1..i]` 和 `s2[1..j]`，它们的 LCS 长度是 `dp[i][j]`。

<img src="https://tva1.sinaimg.cn/large/007S8ZIlly1ghv50ukwx9j30rm0tqwfv.jpg" alt="image-20200818182435646" style="zoom:33%;" />

这样一看，显然 `dp[i-1][j-1]` 对应的 `lcs` 长度不可能比前两种情况大，所以没有必要参与比较。

## 两个字符串的动态规划问题总结

对于两个字符串的动态规划问题，一般来说都是像本文一样定义 **DP table：**

**对于 `s1[1..i]` 和 `s2[1..j]`，它们的 LCS 长度是 `dp[i][j]`**

因为这样定义有一个好处，就是容易写出状态转移方程，`dp[i][j]` 的状态可以通过之前的状态推导出来：

<img src="https://tva1.sinaimg.cn/large/007S8ZIlly1ghv52ofqh1j30lu0juq41.jpg" alt="image-20200818182621220" style="zoom:33%;" />

**找状态转移方程的方法是：思考每个状态有哪些「选择」，只要我们能用正确的逻辑做出正确的选择，算法就能够正确运行。**

## 子序列解题模板（最长回文子序列）

子序列问题的套路，**其实就有两种模板，相关问题只要往这两种思路上想，十拿九稳。**

一般来说，这类问题都是让你求一个**最长子序列**，一旦涉及到**子序列**和**最值**，那几乎可以肯定，**考察的是动态规划技巧，时间复杂度一般都是 O(n^2)**。

### 1. 一个一维的 dp 数组（最长上升子序列）

``` python
n = len(array)
dp = [1] * (n)

for i in range(n):
    for j in range(i):
        dp[i] = 最值(dp[i], dp[j] + ...)
```

在[最长上升子序列](#[300. 最长上升子序列](https://leetcode-cn.com/problems/longest-increasing-subsequence/) )中，`dp` 数组的定义是：

**在子数组`array[0..i]`中，以`array[i]`结尾的目标子序列（最长递增子序列）的长度是`dp[i]`。**

为啥最长递增子序列需要这种思路呢？因为这样符合归纳法，可以找到状态转移的关系。

### 2. 一个二维的 dp 数组

```python
n = len(arr)
dp = [[n] * n for _ in range(n)]

for i in range(n):
    for j in range(n)
        if arr[i] == arr[j]:
            dp[i][j] = dp[i][j] + ...
        else:
            dp[i][j] = 最值(...)
```

这种思路运用相对更多一些，尤其是涉及两个字符串/数组的子序列。

本思路中 dp 数组含义又分为「只涉及一个字符串」和「涉及两个字符串」两种情况。

#### 2.1涉及两个字符串/数组时（最长公共子序列）

在[最长公共子序列](#[1143. 最长公共子序列](https://leetcode-cn.com/problems/longest-common-subsequence/))中，`dp` 数组的含义如下：

**在子数组`arr1[0..i]`和子数组`arr2[0..j]`中，我们要求的子序列（最长公共子序列）长度为`dp[i][j]`**。

#### 2.2 只涉及一个字符串/数组时（最长回文子序列）

在[最长回文子序列](#[516. 最长回文子序列](https://leetcode-cn.com/problems/longest-palindromic-subsequence/) )中，`dp` 数组的含义如下：

**在子数组`array[i..j]`中，我们要求的子序列（最长回文子序列）的长度为`dp[i][j]`**。

### [516. 最长回文子序列](https://leetcode-cn.com/problems/longest-palindromic-subsequence/) 

1. `dp`数组的定义

   这个问题对`dp`数组的定义是：**在子串`s[i..j]`中，最长回文子序列的长度为`dp[i][j]`**。一定要记住这个定义才能理解算法。

   为啥这个问题要这样定义二维的 dp 数组呢？我们前文多次提到，**找状态转移需要归纳思维，说白了就是如何从已知的结果推出未知的部分**，这样定义容易归纳，容易发现状态转移关系。

2. 状态转移方程

   具体来说，如果我们想求`dp[i][j]`，假设你知道了子问题`dp[i+1][j-1]`的结果（`s[i+1..j-1]`中最长回文子序列的长度），你是否能想办法算出`dp[i][j]`的值（`s[i..j]`中，最长回文子序列的长度）呢？

<img src="https://tva1.sinaimg.cn/large/007S8ZIlly1ghv7lrlyq7j30qo0c6n24.jpg" alt="image-20200818195353856" style="zoom:33%;" />

​	可以！**这取决于`s[i]`和`s[j]`的字符**：

​	**如果它俩相等**，那么它俩加上`s[i+1..j-1]`中的最长回文子序列就是`s[i..j]`的最长回文子序列：

<img src="https://tva1.sinaimg.cn/large/007S8ZIlly1ghv7mhgljzj30q00b6q7v.jpg" alt="image-20200818195434929" style="zoom:33%;" />

​	**如果它俩不相等**，说明它俩**不可能同时**出现在`s[i..j]`的最长回文子序列中，那么把它俩**分别**加入`s[i+1..j-1]`中，看	看哪个子串产生的回文子序列更长即可：

<img src="https://tva1.sinaimg.cn/large/007S8ZIlly1ghv7nboibfj30q80f80zg.jpg" alt="image-20200818195523363" style="zoom:33%;" />

​	以上两种情况写成代码就是这样：

```python
if s[i] == s[j]:
    # 它俩一定在最长回文子序列中
    dp[i][j] = dp[i + 1][j - 1] + 2;
else:
    # s[i+1..j] 和 s[i..j-1] 谁的回文子序列更长？
    dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
```

​	至此，状态转移方程就写出来了，根据 dp 数组的定义，我们要求的就是`dp[0][n - 1]`，也就是整个`s`的最长回文子序	列的长度。

3. 定义base case

   明确一下 base case，如果只有一个字符，显然最长回文子序列长度是 1，也就是`dp[i][j] = 1(i == j)`。

   因为`i`肯定小于等于`j`，所以对于那些`i > j`的位置，根本不存在什么子序列，应该初始化为 0。

4. 代码实现

   另外，看看刚才写的状态转移方程，想求`dp[i][j]`需要知道`dp[i+1][j-1]`，`dp[i+1][j]`，`dp[i][j-1]`这三个位置；再看看我们确定的 base case，填入 dp 数组之后是这样：

<img src="https://tva1.sinaimg.cn/large/007S8ZIlly1ghv7uh6pvij30wo0iytj9.jpg" alt="image-20200818200215825" style="zoom:30%;" />

​	**为了保证每次计算`dp[i][j]`，左、下、左下三个方向的位置已经被计算出来，只能斜着遍历或者反着遍历**：

<img src="https://tva1.sinaimg.cn/large/007S8ZIlly1ghv7v70q7cj310y0i8qje.jpg" alt="image-20200818200257058" style="zoom:33%;" />

​	我选择反着遍历，代码如下：

```python
class Solution:
    def longestPalindromeSubseq(self, s: str) -> int:
        n = len(s)
        # dp 数组全部初始化为 0
        dp = [[0] * n for _ in range(n)]
        # base case
        for i in range(n):
            dp[i][i] = 1
        # 反着遍历保证正确的状态转移
        for i in range(n-1, -1, -1):
            for j in range(i+1, n):
                # 状态转移方程
                if s[i] == s[j]:
                    dp[i][j] = dp[i + 1][j - 1] + 2
                else:
                    dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
        # 整个 s 的最长回文子串长度
        return dp[0][n - 1]
```

至此，最长回文子序列的问题就解决了。

**主要还是正确定义 dp 数组含义，遇到子序列问题，首先想到两种动态规划思路，然后根据实际问题看哪种思路容易找到状态转移关系。**

**另外，找到状态转移和 base case 之后，一定要观察 DP table，看看怎么遍历才能保证通过已计算出来的结果解决新的问题**



## 股票买买问题合集

### 一、穷举框架

首先，还是一样的思路：如何穷举？

**利用「状态」进行穷举**。我们具体到每一天，看看总共有几种可能的「状态」，再找出每个「状态」对应的「选择」。
我们要穷举所有「状态」，穷举的目的是根据对应的「选择」更新状态。听起来抽象，你只要记住**「状态」**和**「选择」**两个词就行。

```python
for 状态1 in 状态1的所有取值：
    for 状态2 in 状态2的所有取值：
        for ...
            dp[状态1][状态2][...] = 择优(选择1，选择2...)
```

比如说这个问题，**每天都有三种「选择」**：买入、卖出、无操作，我们用 buy, sell, rest 表示这三种选择。
但问题是，并不是每天都可以任意选择这三种选择的，因为 sell 必须在 buy 之后，buy 必须在 sell 之后。那么 rest 操作还应该分两种状态，一种是 buy 之后的 rest（持有了股票），一种是 sell 之后的 rest（没有持有股票）。而且别忘了，我们还有交易次数 k 的限制，就是说你 buy 还只能在 k > 0 的前提下操作。

> 这里以**买入股票(buy)**来记录交易次数k。因为交易是成对出现的(买入、卖出)，所以只要记录其中一种的操作变化即可。
> 即**买入股票(buy)时 -> k-1**

**这个问题的「状态」有三个**：天数、允许交易的最大次数、当前的持有状态（即之前说的 rest 的状态，我们不妨用 1 表示持有，0 表示没有持有）。然后我们用一个三维数组就可以装下这几种状态的全部组合：

```python
dp[i][k][0 or 1]
# 0 <= i <= n-1, 1 <= k <= K
# n 为天数，大 K 为最多交易数
# 此问题共 n × K × 2 种状态，全部穷举就能搞定。

for i in range(n):
    for k in range(1, K+1):
        for s in {0, 1}:
            dp[i][k][s] = max(buy, sell, rest)
```

我们可以用自然语言描述出每一个状态的含义：
*  `dp[2][3][0]` 的含义：今天是第二天，我现在手上没有持有股票，至今最多进行 3 次交易。
*  `dp[3][2][1]` 的含义就是：今天是第三天，我现在手上持有着股票，至今最多进行 2 次交易。

我们想求的最终答案是 `dp[n-1][K][0]`，即最后一天，最多允许 K 次交易，最多获得多少利润。

> 为什么不是`dp[n-1][K][1]`？
> 因为 [1] 代表手上还持有股票，[0] 表示手上的股票已经卖出去了，很显然后者得到的利润一定大于前者。
>
> 如何解释「状态」？
> 一旦觉得哪里不好理解，把它翻译成自然语言就容易理解了。

### 二、状态转移框架

现在，我们完成了「状态」的穷举，我们开始思考每种「状态」有哪些「选择」，应该如何更新「状态」。可以画个状态转移图：

<img src="https://tva1.sinaimg.cn/large/007S8ZIlly1ghw56wd42yj31360qmafv.jpg" alt="image-20200819151555420" style="zoom: 25%;" />

通过这个图可以很清楚地看到，每种状态（0 和 1）是如何转移而来的。根据这个图，写出**状态转移方程**：

```python
"""
未持有状态：今天我没有持有股票，有两种可能：
要么是我昨天就没有持有，然后今天选择 rest，所以我今天还是没有持有；
要么是我昨天持有股票，但是今天我 sell 了，所以我今天没有持有股票了。
"""
dp[i][k][0] = max(dp[i-1][k][0], dp[i-1][k][1] + prices[i])
              max(   选择 rest  ,           选择 sell      )
"""
持有状态：今天我持有着股票，有两种可能：
要么我昨天就持有着股票，然后今天选择 rest，所以我今天还持有着股票；
要么我昨天本没有持有，但今天我选择 buy，所以今天我就持有股票了。
"""
dp[i][k][1] = max(dp[i-1][k][1], dp[i-1][k-1][0] - prices[i])
              max(   选择 rest  ,           选择 buy         )
```

如果 buy，就要从利润中减去`prices[i]`；如果 sell，就要给利润增加`prices[i]`。
今天的最大利润就是这两种可能选择中较大的那个。而且注意 k 的限制，我们在选择 buy 的时候，把 k 减小了 1。

**定义 base case**，即最简单的情况：

```python
# 因为 i 是从 0 开始的，所以 i = -1 意味着还没有开始，这时候的利润当然是 0 
dp[-1][k][0] = 0
# 还没开始的时候，是不可能持有股票的，用负无穷表示这种不可能
dp[-1][k][1] = float('-inf')
# 因为 k 是从 1 开始的，所以 k = 0 意味着根本不允许交易，这时候利润当然是 0 
dp[i][0][0] = 0
# 不允许交易的情况下，是不可能持有股票的，用负无穷表示这种不可能
dp[i][0][1] = float('-inf')
```

### 三、解题

#### 1. [121. 买卖股票的最佳时机](https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock/)

即 **k = 1**的情况：
直接套状态转移方程，根据 base case，可以做一些化简：

```python
dp[i][1][0] = max(dp[i-1][1][0], dp[i-1][1][1] + prices[i])
dp[i][1][1] = max(dp[i-1][1][1], dp[i-1][0][0] - prices[i]) 
            = max(dp[i-1][1][1], -prices[i])	# 根据上面 k = 0 时的 base case，dp[i-1][0][0] = 0

# 现在发现 k 都是 1，不会改变，即 k 对状态转移已经没有影响了。可以进行进一步化简去掉所有 k ：
dp[i][0] = max(dp[i-1][0], dp[i-1][1] + prices[i])
dp[i][1] = max(dp[i-1][1], -prices[i])
```

写出代码：

```python
# k = 1
def maxProfit(prices):
    n = len(prices)
    if n == 0: 
        return 0
    dp = [[0] * 2 for _ in range(n)]
    # 定义base case (i=0)     
    # dp[i][0] = max(dp[-1][0], dp[-1][1] + prices[i])
    #          = max(0, float('-inf') + prices[i]) = 0
    # dp[0][0] = 0

    # dp[i][1] = max(dp[-1][1], dp[-1][0] - prices[i])
    #          = max(float('-inf'), 0 - prices[i]) = -prices[i]       
    dp[0][1] = -prices[0]

    for i in range(1, n):
        dp[i][0] = max(dp[i-1][0], dp[i-1][1] + prices[i])
        dp[i][1] = max(dp[i-1][1], - prices[i])
    return dp[n-1][0]
```

> 对`-prices[i]`的思考：
>
> 正常可能第一下想到的是`dp[i-1][0] - prices[i]`，表示的意义是第 i - 1 天无持有，第 i 天买入。
> 注意这里的 k = 1，也就是只能进行一次交易（买入一次+卖出一次），
> 在买入后必定伴随着卖出（为了利润最大，最后手里买入的股票都要卖出去），
> 所以在买入时就会消耗掉一次也是唯一的一次交易机会，故在任何时候的买入前都不会有利润（只能有一次买入），
> 所以对于第 i - 1 天无持有，第 i 天买入的状态，在第 i 天之前的利润一定都是 0 ，
> 即在此状态下`dp[i-1][0]`一定为 0（别的状态不一定），所以这里只能是`-prices[i]`而不能是`dp[i-1][0] - prices[i]`

状态压缩：

注意状态转移方程，新状态只和相邻的一个状态有关，所以只需要一个变量储存相邻的那个状态就够了，这样就把空间复杂度降到 O(1)：

```python
# k == 1
def maxProfit_k_1(prices):
    n = len(prices)
    # base case: dp[-1][0] = 0, dp[-1][1] = float('-inf')
    dp_i_0, dp_i_1 = 0, float('-inf')
    for i in range(n):
        # dp[i][0] = max(dp[i-1][0], dp[i-1][1] + prices[i])
        dp_i_0 = max(dp_i_0, dp_i_1 + prices[i])
        # dp[i][1] = max(dp[i-1][1], -prices[i])
        dp_i_1 = max(dp_i_1, -prices[i])
    return dp_i_0
```



#### 2. [122. 买卖股票的最佳时机 II](https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock-ii/)

即 **k = inf** 的情况：
如果 k 为正无穷，那么就可以认为 k 和 k - 1 是一样的。可以这样改写框架：

```python
dp[i][k][0] = max(dp[i-1][k][0], dp[i-1][k][1] + prices[i])
dp[i][k][1] = max(dp[i-1][k][1], dp[i-1][k-1][0] - prices[i])
            = max(dp[i-1][k][1], dp[i-1][k][0] - prices[i])

# 我们发现数组中的 k 已经不会改变了，也就是说不需要记录 k 这个状态了：
dp[i][0] = max(dp[i-1][0], dp[i-1][1] + prices[i])
dp[i][1] = max(dp[i-1][1], dp[i-1][0] - prices[i])
```

写出代码：

```python
# k = inf
def maxProfit(prices):
    n = len(prices)
    if n == 0: 
        return 0
    dp = [[0] * 2 for _ in range(n)]
    # dp[0][0] = 0   
    dp[0][1] = -prices[0]

    for i in range(1, n):
        dp[i][0] = max(dp[i-1][0], dp[i-1][1] + prices[i])
        dp[i][1] = max(dp[i-1][1], dp[i-1][0] - prices[i])
    return dp[n-1][0]
```

> 根据对 k = 1时`-prices[i]`的思考，现在 k = inf ，买入和卖出的次数不再受限，
> 所以`dp[i-1][0] - prices[i]`状态时的`dp[i-1][0]`的值不一定一直为 0 （买卖次数不限），故这里应该加上。

状态压缩：


```python
# k == inf
def maxProfit_k_1(prices):
    n = len(prices)
    dp_i_0, dp_i_1 = 0, float('-inf')
    for i in range(n):
        temp = dp_i_0
        dp_i_0 = max(dp_i_0, dp_i_1 + prices[i])
        dp_i_1 = max(dp_i_1, temp - prices[i])
    return dp_i_0
```

> 其实根据题目的意思，当天卖出以后，当天还可以买入。所以算法还可以直接简化为只要今天比昨天大，就卖出。
>
> ```python
> def maxProfit(prices):
>         if len(prices) == 0:
>             return 0
>         total = 0
>         for i in range(1, len(prices)):
>             if prices[i] > prices[i-1]:
>                 total += prices[i] - prices[i-1]
>         return total
> ```



# 面试题记录

## [88. 合并两个有序数组](https://leetcode-cn.com/problems/merge-sorted-array/)

```python
class Solution:    
    def merge(self, A: List[int], m: int, B: List[int], n: int) -> None:
        res = []
        i, j = 0, 0
        while i < len(A) and j < len(B):
            if A[i] < B[j]:
                res.append(A[i])
                i += 1
            else:
                res.append(B[j])
                j += 1
        if i < j:
            res.extend(A[i:])
        if i > j:
            res.extend(B[j:])
        return res
```

**优化：不申请额外空间**

```python
class Solution:
    def merge(self, A: List[int], m: int, B: List[int], n: int) -> None:
        """
        Do not return anything, modify A in-place instead.
        """
        index_a = m - 1	 # 对 A 中元素倒序遍历，指针从最后元素位置开始 
        cur = m + n - 1  # 添加 cur 指针追踪位置，从 A 列表末尾开始追踪
        while index_a > -1:
            if B and A[index_a] < B[-1]:
                A[cur] = B.pop()
                cur -= 1
            else:
                A[cur] = A[index_a]
                cur -= 1
                index_a -= 1
        if B:
            A[:len(B)] = B  # 比较完B还有剩下的，全填到A前面即可
        return A
```

## [905. 按奇偶排序数组](https://leetcode-cn.com/problems/sort-array-by-parity/)

```python
class Solution:
    def sortArrayByParity(self, A: List[int]) -> List[int]:
        res1 = []
        res2 = []      
        for i in range(len(A)):
            if A[i] % 2 == 0:
                res1.append(A[i])
            else:
                res2.append(A[i])
        res1.extend(res2)
        return res1
```

**优化1：不申请额外空间**

```python
# 左右指针
class Solution:
    def sortArrayByParity(self, A: List[int]) -> List[int]:
        i, j = 0, len(A) - 1
        while i < j:
            if A[i] % 2 == 1 and A[j] % 2 == 0:
                A[i], A[j] = A[j], A[i]
                i += 1
                j -= 1
            elif A[i] % 2 == 0:
                i += 1
            elif A[j] % 2 == 1:
                j -= 1
        return A
```

**优化2：不改变相对顺序**

```python
# 快慢指针
class Solution:
    def sortArrayByParity(self, A: List[int]) -> List[int]:
        i = 0
        for j in range(len(A)):
            if A[j] % 2 == 0:
                A[i], A[j] = A[j], A[i]
                i += 1
        return A
```

## [236. 二叉树的最近公共祖先](https://leetcode-cn.com/problems/lowest-common-ancestor-of-a-binary-tree/)

```python
class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        if not root or root == p or root == q: 
            return root
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)
        # 1.当 left 和 right 同时为空:说明 root 的左 / 右子树中都不包含 p,q，返回 None
        if not left and not right: 
            return
        # 3.当 left 为空，right 不为空：p,q 都不在 root 的左子树中，直接返回 right
        if not left:
            return right 
        if not right: 
            return left # 4. 与 3 同理
        return root # 2. if left and right:
```

