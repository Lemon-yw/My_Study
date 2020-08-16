import collections


class Solution:
    def openLock(self, deadends, target):
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
        s = list(s)
        if s[j] == '9':
            s[j] = '0'
        else:
            s[j] = int(s[j])
            s[j] += 1
            s[j] = str(s[j])
        return ''.join(s)

    # 将 s[i] 向下拨动一次
    def minusOne(self, s, j):
        s = list(s)
        if s[j] == '0':
            s[j] = '9'
        else:
            s[j] = int(s[j])
            s[j] -= 1
            s[j] = str(s[j])
        return ''.join(s)


deadends = ["8887", "8889", "8878", "8898", "8788", "8988", "7888", "9888"]
target = "8888"
solution = Solution()
print(solution.openLock(deadends, target))
