# 自我介绍

我目前在北京邮电大学读研三，所在实验室的主要方向是光网络及卫星通信相关，我在研究生期间主要的研究方向是强化学习与数据中心光网络结合的方向。今年6-8月期间在滴滴公司国际化业务技术部远程实习，主要工作是进行服务端的测试工作，涉及的主要方面是功能测试、接口测试以及自动化case的编写等。

```python
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def deleteDuplicates(self, head: ListNode) -> ListNode:
        dummy = ListNode(0)
        dummy.next = head

        pre, cur = dummy, head
        while cur and cur.next:
            if cur.val == cur.next.val:
                pre.next = cur.next
            else:
                pre = cur
            cur = cur.next

        return dummy.next
```

#  实习总结

## 项目总结

1. 俄罗斯车牌展示&车牌支持富文本
    需求背景：对俄罗斯车牌进行格式化处理，并针对不同国家的车牌可能存在的特殊样式，通过提供通用性能力解决。
  主要职责：测试接口新增字段在正常或者异常情况能否显示正确，并保证字段格式的设置与端正常交互。

2. 国际化闪送支持发多单

  需求背景：闪送用户发送完一单之后，可以返回首页继续发新的订单。

  改动点：

  1. 发单接口，发单拦截支持闪送业务发多单
  2. 在首页显示正在进行的闪送订单接口，增加闪送发多单的模板

  主要职责：测试命中发多单场景的主流程是否正常，验证各触发点的逻辑是否符合需求及异常状况下的处理。

> 测试国际化闪送支持发多单遇到的问题：
>
> 发两单闪送后取消一单，可以再发快车单，不符合不同产品线互斥的需求。
>
> 定位问题：
>
> 1. **乘客侧的cache有且仅有一条记录，cache只会保留最新的一条订单信息。**
>
>    所以取消订单后cache会清空，所以再发快车时查询到的订单信息为空，发单不会被拦截。
>
> 2. **取消订单时从订单系统查询历史订单，传的条件是order_status = 0/1/2/3/4/5，结果返回order_status = 7。**
>
>    原因是数据链路有延迟，状态未及时更新：
>    cache中order_status = 2（已到达接乘客），而订单系统中状态依然是order_status = 7（乘客抢单后取消）。
>    所以返回的状态7使得再次发快车单不被拦截。
>
> 解决方法：
>
> 1. **在取消订单代码的获取历史订单信息部分，增加一段关于产品线的逻辑判断：**
>
>    判断是否有可发多单的投放：
>
>    ​	如果不是闪送则返回空，即清空cache
>
>    ​	如果是闪送则不查cache，直接请求订单系统获取历史订单信息来返回
>
> 2. **在取消订单代码的获取历史订单信息部分，增加一段关于订单状态的过滤：**
>
>    符合查询条件时才返回，不符合的话则抛弃，返回最近的符合查询条件的订单。
>    
>    避免了由于更新不及时造成获取订单状态信息的错误。

## 学习记录

### 测试流程

QA就测试RD开发的分支代码，首先看一下代码改动点，看一下改动是否符合需求，然后看一下改动代码是否有语法错误，然后进行接口测试，测试逻辑是否合理，返回是否正确，考虑正常和异常场景，以及整体代码的覆盖度。

1. 需求评审
2. 写准入case
3. 写测试case
4. case评审(改动点、风险点)
5. 部署测试环境
6. 测试(执行测试case、提bug、回归)
7. 准出
8. 跟进上线

学业务 -> 理解需求 -> 制定测试计划 -> 写case -> 执行测试 -> 报bug -> 回归测试 -> 做测试总结

### 测试方法 & 设计测试用例

黑盒测试

* 把测试对象看做一个黑盒子，测试人员完全不考虑程序内部的逻辑结构和内部特性，只依据程序的需求规格说明书，检查程序的功能是否符合它的功能说明。
* 测试目标
  * 是否有不正确或遗漏的功能？
  * 在接口上，输入是否能正确的接受？能否输出正确的结果？
  * 是否具有数据结构错误或外部信息（例如数据文件）访问错误？
  * 性能上是否能够满足要求？
  * 是否有初始化和终止性错误？
* 测试方法
  * 等价类划分法
    * 将程序所有可能的输入数据划分为若干个等价类，然后从每个部分中选取具有代表性的数据当做测试用例；
    * 测试用例由**有效**等价类和**无效**等价类的代表数据组成。
  * 边界值分析法
    * 对程序**输入或输出的边界值**进行测试。
  * 因果图法
    * 根据输入条件的组合、约束关系和输出条件的因果关系，分析输入条件的各种组合情况，从而设计测试用例；
    * 它适合于检查程序**输入条件的各种组合**情况。

白盒测试

* 把测试对象看做一个打开的盒子，它允许测试人员利用程序内部的逻辑结构及有关信息，设计或选择测试用例，对程序所有逻辑路径进行测试，通过在不同点检查程序状态，确定实际状态是否和预期的状态一致。
* 测试目标
  * 对程序模块的所有独立的执行路径至少测试一遍
  * 对所有的逻辑判定，取“真”与取“假”的两种情况都能至少测一遍
  * 在循环的边界和运行的边界内执行循环体
  * 测试内部数据的有效性
* 测试方法
  * 程序结构分析
    * 根据源代码可以首先绘制程序的流程图，然后根据流程图分析程序的结构。
  * 逻辑覆盖
    * 根据程序的内部结构，对所有的路径进行测试，是一种穷举路径的测试方法。
  * 基本路径测试
    * 根据程序的逻辑判断，分析程序中的路径，再进行用例的设计。

**设计测试用例**

https://blog.csdn.net/qq_43669007/article/details/107347490?utm_medium=distribute.pc_relevant_t0.none-task-blog-BlogCommendFromMachineLearnPai2-1.add_param_isCf&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-BlogCommendFromMachineLearnPai2-1.add_param_isCf

测试思路：主攻功能（从正面+负面覆盖），然后覆盖非功能（包括界面、兼容性、性能、安全、易用性五个方面）。

### 接口测试

1. 接口测试流程

   ① 获取接口规范。

   ②设计接口测试功能用例（主要从用户角度出发看接口能否实现业务需求，用例设计就是黑

   盒用例那一套）。

   ③各种入参验证（正常情况，异常情况包括输入参数个数不对，类型不对，可选/必选，还

   有考虑参数有互斥或关联的情况）。

   ④ 接口返回值各种验证（符合接口文档需求）

   ⑤了解接口实现逻辑，实现逻辑覆盖（语句/条件/分支/判定/…）

   ⑥接口能并发执行吗、安全吗，性能满足要求吗?

   ⑦ 采用工具或者自写代码来验证。

   ⑧发现问题跟功能测试一样，该报bug 报bug，该跟踪状态的跟踪状态。

2. 如何设计测试用例？

接口测试一般考虑入参形式的变化和接口的业务逻辑，一般设计接口测试用例采用等价类、边界值、场景法居多。
接口测试设计测试用例的思路如下：

①是否满足前提条件

有些接口需要满足前提，才可成功获取数据。常见的，需要登录Token

逆向用例：针对是否满足前置条件（假设为n 个条件），设计0~n 条用例

②是否携带默认值参数

正向用例：带默认值的参数都不填写、不传参，必填参数都填写正确且存在的“常规”值，

其他不填写，设计1 条用例

③ 业务规则、功能需求

这里根据时间情况，结合接口参数说明，可能需要设计N 条正向用例和逆向用例

④参数是否必填

逆向用例：针对每个必填参数，都设计1 条参数值为空的逆向用例

⑤参数之间是否存在关联

有些参数彼此之间存在相互制约的关系

⑥ 参数数据类型限制

逆向用例：针对每个参数都设计1 条参数值类型不符的逆向用例

⑦参数数据类型自身的数据范围值限制

正向用例：针对所有参数，设计1 条每个参数的参数值在数据范围内为最大值的正向用例

3. 做接口的测试的时候测什么

   可用性测试

   根据约定的协议、方法、格式内容，传输数据到接口经处理后返回期望的结果：

    接口功能是否正确实现；

    返回值测试- 返回值除了内容要正确，类型也要正确，保证调用方能够正确地解析；

    参数值边界值、等价类测试；

   错误和异常处理测试

    输入异常值（空值、特殊字符、超过约定长度等），接口能正确处理，且按预期响应；

    输入错误的参数，接口能正确处理，并按预期响应；

    多输入、少输入参数，接口能正确处理，且按预期响应；

    错误传输数据格式（如json 格式写成form 格式）测试；

   安全性测试，主要指传输数据的安全性：

    敏感数据（如密码、秘钥）等是否加密传输；

    返回数据是否含有敏感数据，如用户密码、完整的用户银行账号信息等；

    接口是否对传入的数据做安全校验，如身份ID 加token 类似校验；

    接口是否防止恶意请求（如大量伪造请求接口致使服务器崩溃）；

   性能测试，如接口的响应时间、并发处理能力、压测处理情况：

    并发请求相同的接口（特别为POST 请求），接口的处理情况（如插入了相同的记录导致

   数据出错，引发系统故障）；

    接口响应时长在用户可忍受的范围内；

    对于请求量大的接口做压测，确定最大的瓶颈点是否满足当前业务需要；

4. 接口组成

请求地址、请求方法、请求参数（入参和出参）组成，部分接口有请求头header。

5. header请求头和入参都是发送到服务器他们有什么区别呢？

* header里存放的参数一般存放的是一些校验信息，比如cookie，它是为了校验这个请求是否有权限请求服务器，如果有，它才能请求服务器，然后把请求地址连同入参一起发送到服务器，然后服务器会根据地址和入参来返回出参。
* 也就是说，服务器是先接受header信息进行判断该请求是否有权限请求，判断有权限后，才会接受请求地址和入参的。

6. 没有接口文档如何做接口测试？

   用抓包工具把接口抓取处理，然后针对性进行测试；接口中字段信息不清楚的，找时间集中寻求开发解答。

7. 在手工接口测试或者自动化接口测试的过程中，上下游接口有数据依赖如何处理？

   用一个**全局变量**来处理依赖的数据，比如登录后返回token，其它接口都需要这个token，那就用全局变量来传token 参数。

8. 接口测试中，依赖登录状态的接口如何测试？

   依赖登录状态的接口的本质上是在每次发送请求时需要带上session 或者cookie 才能发送成功，在构建POST 请求时添加必要的session 或者cookie。

### 自动化测试

* 使用dws自动化测试框架

  * api层自动化测试框架，能支持api层的测试，包括接口返回值等各种验证。
  * 这是基于python的unittest的扩展。

* case编写

  1. 在对应的文件更新自己的测试账号；

  2. 根据接口的触发流程写入需要调用的接口；

  3. 对已存在的字段，进行替换；对未存在的字段，进行新增；

  4. 对于要校验的返回值进行断言处理。

     > 断言设置不仅要设置改动点的返回，还要设置涉及到改动点的返回是否符合预期，出问题才能定位的比较准确。
     
     
  
* pytest框架

  自动化测试脚本一般由**测试的输入、业务逻辑、测试输出和测试结果验证**几部分组成。

  * 在excel中输入请求的地址、方法、common参数、校验返回的断言等，一些私参不输入具体值，用占位符表示
  * 通过请求数据构造的服务器获得私参值
  * 在代码中使用pytest.mark.parametrize装饰器将case导入，实现测试用例的参数化，与之前获取的私参值一起通过request这个模块请求测试环境的服务器，获得接口返回
  * 校验返回的参数

  > ```python
  > @pytest.mark.parametrize(argnames, argvalues)
  > # 参数：
  > # argnames:以逗号分隔的字符串
  > # argvaluse: 参数值列表，若有多个参数，一组参数以元组形式存在，包含多组参数的所有参数
  > # 以元组列表形式存在
  > 
  > ## 如果想获得多个参数化参数的所有组合，可以通过堆叠参数化装饰器实现 ## 
  > @pytest.mark.parametrize("x",["a","b"])
  > @pytest.mark.parametrize("y",[2,3])
  > def test_foo(x,y):
  >     print("测试数据组合:x->%s,y->%s"%(x,y))
  > if __name__=="__main__":
  >     pytest.main(["-s","test_canshu.py"])
  > ```
  >
  > request模块
  >
  > ```python
  > res = requests.request(
  >  method=case['METHOD'],
  >  url=get_sim_domain(ENV) + case['URL'],
  >  params=json2dict(case['PARAMS']),
  >  # headers=json2dict(case['HEADERS']),
  >  data=json2dict(case['DATA']),
  >  json=json2dict(case['JSON'])).json()
  > ```

### 如何理解压力、负载、性能测试？

性能测试是一个较大的范围，实际上性能测试本身包含了性能、强度、压力、负载等多方面的测试内容。

压力测试是对服务器的稳定性以及负载能力等方面的测试，是一种很平常的测试。增大访问系统的用户数量、或者几个用户进行大数据量操作都是压力测试。而负载测试是压力相对较大的测试，主要是测试系统在一种或者集中极限条件下的相应能力，是性能测试的重要部分。100个用户对系统进行连续半个小时的访问可以看作压力测试，那么连续访问8个小时就可以认为负载测试，1000个用户连续访问系统1个小时也可以看作是负载测试。

相交链表

```python
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> ListNode:
        h1, h2 = headA, headB

        while h1 != h2:
            if h1:
                h1 = h1.next
            else:
                h1 = headB
            if h2:
                h2 = h2.next
            else:
                h2 = headA
        return h1
```

环形链表

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



## 定位问题

1. 某地头条用户突然不能刷是什么原因?
2. 看视频突然断网了什么原因？

## MVC 框架模式

MVC全名是**Model View Controller**，是模型(model)－视图(view)－控制器(controller)的缩写，一种软件设计典范，用于组织代码用一种**业务逻辑和数据显示分离的方法**，这个方法的假设前提是如果业务逻辑被聚集到一个部件里面，而且界面和用户围绕数据的交互能被改进和个性化定制而不需要重新编写业务逻辑。MVC被独特的发展起来**用于映射传统的输入、处理和输出功能在一个逻辑的图形化用户界面**的结构中。
MVC是一个框架模式，它**强制性的使应用程序的输入、处理和输出分开**。使用MVC应用程序被分成三个核心部件：**模型、视图、控制器**。它们各自处理自己的任务。

>   Model 是指要处理的业务逻辑和数据操作，它接收视图请求的数据并返回最终的处理结果；
>   View 视图主要是指的跟用户打交道并且显示给用户看的，用户看到并与之交互的界面；
>   Controller 看成是Model和View的桥梁，枢纽，响应请求，处理跳转，使模型和视图保持一致。





# 项目总结

## 项目介绍

**要解决的问题**：在固定网络规模（节点数、节点度）的前提下，通过使用深度强化学习来训练出优秀的模型，从而可以在面对一定流量强度下的业务时，快速的找到最优网络拓扑，以最大化的降低网络延迟。

**强化学习在项目中的应用**：在这个项目中，主要使用了强化学习的原理和算法，使用agent与它的环境（即网络）通过状态、行为、奖励这三种信号来进行交互，agent的实现就是使用强化学习算法与深度神经网络结合的框架，其目的是找到最优的行为策略（网络拓扑矩阵），以最大化奖励（即最小化网络延迟）。具体在算法中它通过使用两个深度神经网络（Acotr、Critic）来迭代地改进选择动作的策略，从而达到最大化奖励的目的。

> **强化学习原理**
> 强化学习强调如何基于环境来选择行为，以取得最大化的预期利益。强化学习其实是在环境和机器人之间的互动，环境通过对机器人产生奖励，刺激机器人根据当前的状态和奖励产生下一个动作，整个过程以获得更高的奖励为目的，如此不断进行下去。
> 就好比你在品尝一个没有吃过的食物，吃完之后你会对这个食物有一个判断，好吃或者不好吃，这种判断就是一个奖励，决定了你下一次面对这个食物时选择吃与不吃。
>
> **KNN原理**
>
> 就是当预测一个新的值x的时候，根据它距离最近的K个点是什么类别来判断x属于哪个类别。

**实际中的实现**：通过SDN控制器交换状态、动作和奖励，SD-DCN的数据平面采用光电混合交换框架，其中机架顶部(ToR)开关采用电链路连接形成固定的环形拓扑，同时使用光链路连接到多个光电路交换(OCS)开关。通过重新配置OCS交换机，可以实现不同的互连拓扑，以满足不同应用程序的不同通信需求。SDN控制器被部署用于集中的网络控制和管理。具体来说，状态由拓扑邻接矩阵的一半组成，通过数据处理成一维矩阵的形式，动作以拓扑邻接矩阵形式表示，奖励为平均网络延迟。

## 我的贡献

1. 强化学习中训练集的设计与实现
利用算法生成了符合要求的训练集，借鉴了Google DeepMind对于解决推荐系统在大规模离散空间下训练问题的方法，采用了k近邻算法及贪婪策略进行训练集的分类与选取，并输入到神经网络进行训练；
2. 动态拓扑的设计
    在仿真初始环境中搭建全连接的网络拓扑，通过读取强化学习训练中产生的拓扑邻接矩阵来决定节点链路连接的通断以实现构建不同的网络拓扑环境；
3. 模型的训练与测试
  * 在不同流量下(25%、50%、75%...)分别训练模型，其网络时延平均值整体均随训练时间的增加呈逐步降低趋势，最后基本趋于稳定达到收敛；
  * 将训练模型分别与采用随机和贪婪策略生成拓扑的模型进行对比，在降低时延方面呈现出明显优越性；
  * 训练后的模型在面对新流量时可以一步输出相对稳定的近似最优拓扑矩阵。

# Python相关

## 数据类型

### 基本数据类型

数字int、布尔值bool、字符串str、列表list、元组tuple、字典dict等

### 列表和元组的区别

* 列表是动态数组，它们可变且可以重设长度(改变其内部元素的个数)。
* 元组是静态数组，它们不可变，且其内部数据一旦创建便无法改变。

### 数组和链表的区别

数组：连续、顺序存储

> 在Python语言中，没有直接使用数组这个概念，而是用**列表(list)**和**元组(tuple)**这两种集合，它们本质上都是对数组的封装。
>
> 其中**列表**是一个**动态可扩展**的数组，支持任意的添加、删除、修改元素；
> 而**元组**是一个**不可变**集合，一旦创建就不再支持修改。s

链表：非连续、非顺序存储

**时间复杂度**

|      | 查找 | 更新 | 插入 | 删除 |
| ---- | ---- | ---- | ---- | ---- |
| 数组 | O(1) | O(1) | O(n) | O(n) |
| 链表 | O(n) | O(1) | O(1) | O(1) |

### 可变类型和不可变类型

* 可变类型（mutable）：列表，字典
* 不可变类型（unmutable）：数字，字符串，元组

这里的可变不可变，是指**内存中的那块内容（value）是否可以被改变**。
如果是不可变类型，在对对象本身操作的时候，必须在内存中新申请一块区域(因为老区域不可变)。
如果是可变类型，对对象操作的时候，不需要再在其他地方申请内存，只需要在此对象后面连续申请(+/-)即可，也就是它的address会保持不变，但区域会变长或者变短。

不可变类型有什么好处？
如果数据是不可变类型，当我们把数据传给一个不了解的API时，可以确保我们的数据不会被修改。

### 可变参数(*args, **kargs)

* ***args**：是一个**元组**，传入的参数会被放进**元组**里。
* ***\*kwargs**：是一个**字典**，传入的参数以键值对的形式存放到**字典**里。

## is 和 == 的区别

is比较的是两个对象是否为同一个实例对象；

而==比较的是对象的值是否相等。

## 深拷贝和浅拷贝

* 深拷贝
  * 创建一个新的对象，并且递归的复制它所包含的对象（**修改其中一个，另外一个不会改变**）
* 浅拷贝
  * 创建一个新的对象，但它包含的是对原始对象中包含项的引用（如果**用引用的方式修改其中一个对象，另外一个也会修改改变**）

## 垃圾回收机制

* 对象的引用计数

  * Python内部使用引用计数，来保持追踪内存中的对象，所有对象都有引用计数，当一个对象的引用计数归零时，它将被垃圾收集机制处理掉。
    * 引用计数增加的情况：
      * 一个对象分配一个新名称
      * 将其放入一个容器中（如列表、元组或字典）

    * 引用计数减少的情况：
      * 使用del语句对对象别名显示的销毁
      * 引用超出作用域或被重新赋值

## 读写日志文件

```python
# 按行读取文件
with open('log.txt', 'r') as f:
    for line in f:
        print(line, end='')

# 转换为列表，去掉换行符，去掉行首行尾的空白字符
with open('log.txt', 'r') as f:
    content = [line.strip() for line in f]
    # f.read().splitlines() 可去掉换行符，不可去掉空白字符
    print(content)

# 按行读取文件内容并得到当前行号
'''
文件对象是可迭代的（按行迭代），使用enumerate()即可在迭代的同时，得到数字索引(行号),
enumerate()的默认数字初始值是0，如需指定1为起始，可以设置其第二个参数为1。
'''
with open('log.txt', 'r') as f:
    for number, line in enumerate(f, start=1):
        print(number, line, end='')
```

```python
'''
读取日志文件，搜索关键字，打印关键字前5行
'''
def search(lines, pattern, history=5):
    previous_lines = []
    for line in lines:
        if len(previous_lines) < history and pattern in line:
            previous_lines.append(line)
    return previous_lines

if __name__ == '__main__':
    with open('log.txt', 'r') as f:
        # 去掉换行符
        f = f.read().splitlines()
        print(search(f, 'response'))

        # 追加
        f.write('\n... and more')
        print(open('log.txt').read())
        
        
'''
读取大型日志文件，搜索关键字，打印关键字前5行
''' 
from collections import deque


# 定义一个搜索关键字的函数
def search_keyword(lines, pattern, history=5):
    """
    搜索关键字的生成器函数
    :param lines: 含有多行内容的可迭代对象
    :param pattern: 要搜索的关键字
    :param history: 保留的含有关键字的条目数
    """
    # 创建只能容纳 5 个元素的队列
    previous_lines = deque(maxlen=history)

    for line in lines:

        # 判断每行是否含有目标关键字
        if pattern in line:
            # 当每次匹配成后就把此行添加到队列中，
            # 并且返回这个队列，以便稍后打印里面的
            # 元素时可以看到其中数量的变化
            previous_lines.append(line)
            yield previous_lines


if __name__ == '__main__':
    with open(r'./some_file.txt') as f:
        for prevlines in search_keyword(f, '千锋云计算', 5):
            for pline in prevlines:
                print(pline, end='')
            print('\n', '-' * 20)
```

```python
'''
统计文章中频率最高的10个单词
'''
# 方法一：将wordlist的word和word的个数放入dict，排序
import re
with open('1.txt', 'r') as f:
	word_dict = {} # 用于统计 word：个数
	word_list = [] # 用于存放所有单词
	
	for line in f.readlines():
        for word in line.strip().split(" "):
            word_list.append(re.sub(r"[^a-z]+", "", word.lower()))
    word_sets = list(set(word_list))   # 确保唯一
    word_dict = {word: word_list.count(word) for word in word_sets if word}
    
result = sorted(word_dict.items(), key=lambda d: d[1], reverse=True)[:10]
print(result)

# 方法二：利用collections模块
import re
from collections import Counter
 
with open('1.txt', 'r', ) as f:
    words = f.read()                         # 将文件的内容全部读取成一个字符串
    # re.split 方法按照能够匹配的子串将字符串分割后返回列表
    count = Counter(re.split(r"\W+", words))  # 以单词为分隔
 
result = count.most_common(10)                # 统计最常使用的前10个
print(result)

'''
统计文件中的字符串数目并排序
'''
# 先读取文件，将文件中的数据抽取出来：
# 说明：这个有一个要注意的地方是文件是被”\n”,”/”两种格式分割而来的，因此需要split两次。
def getWords(filepath):
    file = open(filepath)
    wordOne = []
    while file:
        line = file.readline()
        wordOne.extend(line.split('/'))
        if not line:  # 若读取结束了
            break
    wordtwo = []
    for i in wordOne:
        wordtwo.extend(i.split())
    return wordtwo


# 然后定义一个dict，遍历数据，代码如下所示：
def getWordNum(words):
    dictWord = {}
    for i in words:
        dictWord[i] = dictWord.get(i, 0) + 1
    # 字典排序
    dictWord_order = sorted(dictWord.items(), key=lambda x: x[1], reverse=True)
    return dictWord_order


if __name__ == '__main__':
    filepath = 'log.txt'
    words = getWords(filepath)
    dictword = getWordNum(words)
    print(dictword)
```

```python
'''
替换文件中指定字符串

分析：先以只读模式打开后，对文件每一行进行readlines()操作，并保存到新的列表中。然后随之关闭。 再以'w+'方式进行读写打开，对已经保存的列表用re.sub()进行替换操作，并用f.writelines()函数写入。
'''
import re

with open('/home/wuzz/11.txt','r') as f:
	alllines=f.readlines()

with open('/home/wuzz/11.txt','w+') as f:
    for eachline in alllines:
        a=re.sub('hello','hi',eachline)
        f.writelines(a)
        
'''
将替换后的内容保存到新文件中
'''
import re
 
with open('/home/wuzz/11.txt','r+') as f1:
	with open('/home/wuzz/12.txt','w+') as f2:
        str1=r'hello'
        str2=r'hi'
        for ss in f1.readlines():
            tt=re.sub(str1,str2,ss)
            f2.write(tt)
            
'''
逐行替换超大文件中的字符串
'''
import re

#自定义正则
rex="\'0000-00-00 00:00:00\'"
new_str='now()'
old_file_path=r'C:\Users\Ths\Desktop\test.txt'
new_file_path=r'C:\Users\Ths\Desktop\newtest.txt'
def match_timestamp(repex,eachline):
    p=re.compile(repex)
    return p.findall(eachline)
    
#打开旧文件，将每一行yield后作为迭代器返回。
def old_file_yield(old_file_path):
    with open(old_file_path,'r') as  oldf:
      while True:
         line=oldf.readline()
         yield line
         if not line:
             oldf.close()
             break
#打开新文件开始逐行读取替换。     
def replace_match(old_file_path,new_file_path):
    count=0
    with open(new_file_path,"w") as newf:
        for line in old_file_yield(old_file_path):
            ifmatch=match_timestamp(rex,line)
            if not line:                    
                newf.close()
                return count
            break
            elif ifmatch:
                count+=1
                print("替换前：%s" % line)
                line=line.replace(rex,new_str)
                print("替换后：%s" % line)
                newf.write(line)
                else:
                    newf.write(line)
print('一共替换了%s行' % replace_match(old_file_path,new_file_path))
```



## lambda函数

通常是在需要一个函数，但是又不想费神去命名一个函数的场合下使用，也就是指匿名函数。

* 定义lambda函数的形式如下：

  * labmda 参数：表达式lambda函数默认返回表达式的值。

  * ```python
    # lambda [arguments]:expression
    a = lambda x,y:x+y
    ```

* lambda函数也可以赋值给一个变量。

* lambda函数可以接受任意个参数，包括可选参数，但是表达式只有一个。

## 装饰器

装饰器本质上是一个 Python 函数或类，它可以让其他函数或类在不需要做任何代码修改的前提下增加额外功能，装饰器的返回值也是一个函数/类对象。
它经常用于有切面需求的场景，比如：插入日志、性能测试、事务处理、缓存、权限校验等场景，装饰器是解决这类问题的绝佳设计。
有了装饰器，我们就可以抽离出大量与函数功能本身无关的雷同代码到装饰器中并继续重用。概括的讲，**装饰器的作用就是为已经存在的对象添加额外的功能**。

参考：

https://www.zhihu.com/question/26930016
https://www.zhihu.com/question/26930016/answer/1047233982

## yield用法

参考：

https://blog.csdn.net/mieleizhi0522/article/details/82142856/
https://www.runoob.com/w3cnote/python-yield-used-analysis.html

## 多进程 & 多线程

### 多进程

#### 进程的创建与启动步骤

```python
'''
1.导入进程包
import multiprocessing

2.通过进程类创建进程对象
sub_process = multiprocessing.Process(target=进程执行的函数名)

3.启动进程执行任务
sub_process.start()
'''
import time
import multiprocessing

# sing
def sing():
    for i in range(3):
        print("sing...")
        time.sleep(0.5)
        
# dance
def dance():
    for i in range(3):
        print("dance...")
        time.sleep(0.5)

if __name__ == '__main__':
    # 2.通过进程类创建进程对象
    sing_process = multiprocessing.Process(target=sing)
    dance_process = multiprocessing.Process(target=dance)

    # 3.启动进程执行任务
    sing_process.start()
    dance_process.start()
```

#### 进程执行带有参数的任务

```python
'''
target：进程执行的函数名
args：表示以元组的方式给函数传参
	元组的元素顺序就是任务的参数顺序
kwargs：表示以字典的方式给函数传参
	key名就是参数的名字
'''
sing_process = multiprocessing.Process(target=sing, args=(3,))
dance_process = multiprocessing.Process(target=dance, kwargs{'num': 3})

sing_process.start()
dance_process.start()
```

#### 获取进程编号

```python
'''
1.获取当前进程编号
os.getpid()

2.获取当前父进程的编号 
os.getppid()
'''
```

#### 进程的注意点

1. 正常情况下，主进程会等待所有的子进程执行结束再结束
2. 如果想主进程结束后子进程全部退出不再执行，可以**设置守护主进程**：`子进程对象.daemon = True`

```python
def work():
    # 子进程工作2s
    for i in range(5):
        print("working...")
        time.sleep(0.2)

if __name__ == '__main__':
    work_process = multiprocessing.Process(target=work)
    # 设置守护主进程
    work_process.daemon = True
    work_process.start()

    # 主进程睡眠1s
    time.sleep(0.5)
    print("main process finish...")
```

### 多线程

#### 线程的创建与启动步骤

```python
'''
1.导入线程模块
import threading

2.通过线程类创建进程对象
sub_thread = threading.Thread(target=线程执行的函数名)

3.启动线程执行任务
sub_thread.start()
'''
```

#### 线程执行带有参数的任务

```python
'''
target：线程执行的函数名
args：表示以元组的方式给函数传参
	元组的元素顺序就是任务的参数顺序
kwargs：表示以字典的方式给函数传参
	key名就是参数的名字
'''
sing_thread = threading.Thread(target=sing, args=(3,))
dance_thread = threading.Thread(target=dance, kwargs{'num': 3})

sing_thread.start()
dance_thread.start()
```

#### 线程的注意点

1. 正常情况下，主线程会等待所有的子线程执行结束再结束

2. 如果想主线程结束后子线程全部退出不再执行，可以**设置守护主线程**：

   `threading.Thread(target=sing, daemon=True)` 或

   `线程对象.setDaemon(True)`

3. 线程之间执行的顺序是无序的，是由CPU调度决定某个线程先执行的。

> 什么时候用多线程什么时候用多进程？
>
> * 多线程：io操作密集的时候
>
> * 多进程：cpu耗用过多的时候

# HTTP

HTTP 是**超文本传输协议** ，是一个在计算机世界里专门在**「两点」**之间**「传输」**文字、图片、音频、视频等**「超文本」**数据的**「约定和规范」**。

## Get 和 Post 的区别

- `Get` 方法的含义是请求**从服务器获取资源**，这个资源可以是静态的文本、页面、图片视频等。
  
> 比如，你打开一篇文章，浏览器就会发送 GET 请求给服务器，服务器就会返回文章的所有文字及资源。

- `POST` 方法则是相反操作，它**向 `URI` 指定的资源提交数据**，数据就放在报文的 body 里。

  > 比如，你在一篇文章底部，敲入了留言后点击「提交」，浏览器就会执行一次 POST 请求，把你的留言文字放进了报文 body 里，然后拼接好 POST 请求头，通过 TCP 协议发送给服务器。

基本区别

1. GET请求通过URL（请求行）**提交数据**，在URL中可以看到所传参数；
   POST通过Request body（请求体）**传递数据**，参数不会在url中显示。
2. GET请求提交的数据有长度限制，POST请求没有限制。
3. GET对数据进行查询，POST主要对数据进行增删改！简单说，**GET是只读，POST是写**。
4. **GET比POST更不安全**，因为参数直接暴露在URL上，所以不能用来传递敏感信息。

## 状态码

| 状态码 | 类别                             | 含义                       |
| ------ | -------------------------------- | -------------------------- |
| 1XX    | Informational（信息性状态码）    | 接收的请求正在处理         |
| 2XX    | Success（成功状态码）            | 请求正常处理完毕           |
| 3XX    | Redirection（重定向状态码）      | 需要进行附加操作以完成请求 |
| 4XX    | Client Error（客户端错误状态码） | 服务器无法处理请求         |
| 5XX    | Server Error（服务器错误状态码） | 服务器处理请求出错         |

> 常见错误码：
>
> 「**400 Bad Request**」表示客户端请求的报文有错误，但只是个笼统的错误。
>
> 「**403 Forbidden**」表示服务器禁止访问资源，并不是客户端的请求出错。
>
> 「**404 Not Found**」表示请求的资源在服务器上不存在或未找到，所以无法提供给客户端。
>
> ---
>
> 「**500 Internal Server Error**」与 400 类型，是个笼统通用的错误码，服务器发生了什么错误，我们并不知道。
>
> 「**501 Not Implemented**」表示客户端请求的功能还不支持，类似“即将开业，敬请期待”的意思。
>
> 「**502 Bad Gateway**」通常是服务器作为网关或代理时返回的错误码，表示服务器自身工作正常，访问后端服务器发生了错误。
>
> 「**503 Service Unavailable**」表示服务器当前很忙，暂时无法响应服务器，类似“网络服务正忙，请稍后重试”的意思。

## HTTP与HTTPS

HTTP 有以下安全性问题：

- 使用明文进行通信，内容可能会被窃听；
- 不验证通信方的身份，通信方的身份有可能遭遇伪装；
- 无法证明报文的完整性，报文有可能遭篡改。

HTTPS 并不是新协议，而是让 HTTP 先和 SSL（Secure Sockets Layer）通信，再由 SSL 和 TCP 通信，也就是说 HTTPS 使用了隧道进行通信。

通过使用 SSL，HTTPS 具有了**加密（防窃听）**、**认证（防伪装）**和**完整性保护（防篡改）**。

<img src="https://tva1.sinaimg.cn/large/007S8ZIlly1gh00tknagnj30un09l0uo.jpg" alt="img" style="zoom:50%;" />

> HTTP端口 80
> HTTPS端口443

### HTTP/HTTPS区别

1. 建立连接时候：https 比 http多了 TLS 的握手过程；
2. 传输内容的时候：https 会把数据进行加密，通常是对称加密数据；

### 加密

- 使用非对称密钥加密方式，传输对称密钥加密方式所需要的 Secret Key，从而保证安全性;

- 获取到 Secret Key 后，再使用对称密钥加密方式进行通信，从而保证效率。（下图中的 Session Key 就是 Secret Key）

  <img src="https://tva1.sinaimg.cn/large/007S8ZIlly1gh00y6wxjlj30u02650vm.jpg" alt="img" style="zoom: 25%;" />

### 认证

通过使用 **证书** 来对通信方进行认证。

数字证书认证机构（CA，Certificate Authority）是客户端与服务器双方都可信赖的第三方机构。

服务器的运营人员向 CA 提出公开密钥的申请，CA 在判明提出申请者的身份之后，会对已申请的公开密钥做数字签名，然后分配这个已签名的公开密钥，并将该公开密钥放入公开密钥证书后绑定在一起。

进行 HTTPS 通信时，服务器会把证书发送给客户端。客户端取得其中的公开密钥之后，先使用数字签名进行验证，如果验证通过，就可以开始通信了。

<img src="https://tva1.sinaimg.cn/large/007S8ZIlly1gh02s7vdgtj30m80gjdgw.jpg" alt="img" style="zoom:60%;" />

### 完整性保护

SSL 提供报文**摘要功能**来进行完整性保护。

## 输入一个网址到显示网页的过程

1. 在客户端浏览器中输入网址URL；
2. 发送到DNS(域名服务器)获得域名对应的WEB服务器的IP地址；
3. 客户端浏览器与WEB服务器建立TCP(传输控制协议)连接；
4. 客户端浏览器向对应IP地址的WEB服务器发送相应的HTTP或HTTPS请求；
5. WEB服务器响应请求，返回指定的URL数据或错误信息；
6. 客户端浏览器下载数据，解析HTML源文件，解析完成后，在浏览器中显示基础的页面；
7. 分析页面中的超链接，显示在当前页面，重复以上过程直至没有超链接需要发送，完成页面的全部显示。

<img src="https://tva1.sinaimg.cn/large/007S8ZIlly1gh02j2a8v6j30fy0cidjh.jpg" alt="image-20200722212545866" style="zoom: 80%;" />

### DNS域名系统工作原理

1. 查询浏览器、操作系统**缓存**；
2. 请求**本地域名服务器**；
3. 本地域名服务器未命中缓存，其请求**根域名服务器**；
4. 根域名服务器返回所查询域的**主域名服务器**（主域名、顶级域名，如com、cn）；
5. 本地域名服务器请求主域名服务器，获取该域名的 **名称服务器**（域名注册商的服务器）；
6. 本地域名服务器向 名称服务器 请求 **域名-IP 映射**；
7. 缓存解析结果。

### 客户端向服务器发起http请求时的请求信息

1. 请求方法URI协议/版本
2. 请求头(有关的客户端环境和请求正文的有用信息)
3. 请求正文(客户提交的查询字符串信息：)

##Cookie、Session

* Cookie保存在**客户端浏览器**中，而Session保存在**服务器**上。
* Cookie机制是通过检查客户身上的**“通行证”**来确定客户身份，Session机制是通过检查服务器上的**“客户明细表”**来确认客户身份。

## 短连接、长连接

* 短连接
  * 连接->传输数据->关闭连接 
  * HTTP是无状态的的短链接，浏览器和服务器每进行一次HTTP操作，就建立一次连接，但任务结束就中断连接。 
* 长连接
  * 连接->传输数据->保持连接 -> 传输数据-> ...........->直到一方关闭连接
  * 多是客户端关闭连接

# MySQL

## 终端连接数据库

1. mysql数据库安装在本机，则直接敲入命bai令mysql -u root -p即可。
2. mysql数据库不是安装在本机，则需要加参数，常用参数如下：
   * -h，指定目标ip地址
   * -u，指定登录用户名
   * -p，指定密码，密码可以接在-p后面输入mysql -uroot -p123456。也可以mysql -uroot -p回车等提示输入密码时输入，这样输入密码没有回显。

## 使用的索引

* Hash索引
  
  * 底层原理：哈希表
* B+树索引
  
  * 底层原理：多路平衡查找树
  
  * 为什么使用B+树
  
    数据库使用B+树肯定是为了提升查找效率。
  
    但是具体如何提升查找效率呢？
  
    查找数据，最简单的方式是顺序查找。但是对于几十万上百万，甚至上亿的数据库查询就很慢了。
  
    所以要对查找的方式进行优化，熟悉的二分查找，二叉树可以把速度提升到O(log(n,2))，查询的瓶颈在于树的深度，最坏的情况要查找到二叉树的最深层，由于，每查找深一层，就要访问更深一层的索引文件。在多达数G的索引文件中，这将是很大的开销。所以，尽量把数据结构设计的更为‘矮胖’一点就可以减少访问的层数。在众多的解决方案中，B-/B+树很好的适合。B-树定义具体可以查阅，简而言之就是中间节点可以多余两个子节点，而且中间的元素可以是一个域。相比B-树，B+树的父节点也必须存在于子节点中，是其中最大或者最小元素，B+树的节点只存储索引key值，具体信息的地址存在于叶子节点的地址中。这就使以页为单位的索引中可以存放更多的节点。减少更多的I/O支出。因此，B+树成为了数据库比较优秀的数据结构，MySQL中MyIsAM和InnoDB都是采用的B+树结构。不同的是前者是非聚集索引，后者主键是聚集索引，所谓聚集索引是物理地址连续存放的索引，在取区间的时候，查找速度非常快，但同样的，插入的速度也会受到影响而降低。聚集索引的物理位置使用链表来进行存储。

## 事务

### 定义

一个最小的不可再分的工作单元；通常一个事务对应一个完整的业务(例如银行账户转账业务)。

### 事务四大特征(ACID)

* 原子性(A)：事务是最小单位，不可再分。
* 一致性(C)：事务要求所有的DML语句操作的时候，必须保证同时成功或者同时失败。
* 隔离性(I)：事务A和事务B之间具有隔离性。
* 持久性(D)：是事务的保证，事务终结的标志(内存的数据持久到硬盘文件中)。

### 事务提交

`commit;`(让虚拟的效果真实产生)

### 事务手动回滚

`rollback;`（让虚拟的效果撤销）

### 事务的隔离性

* read uncommitted
  * 读未提交的
  * A事务已执行，但未提交；B事务查询到A事务的更新后数据；A事务回滚；---出现脏数据
* read committed
  * 读已经提交的
  * A事务执行更新；B事务查询；A事务又执行更新；B事务再次查询时，前后两次数据不一致；---不可重复读
* repeatable read
  * 可重复读
  * A事务无论执行多少次，只要不提交，B事务查询值都不变；B事务仅查询B事务开始时那一瞬间的数据快照。
* serializable
  * 串行化
  * 不允许读写并发操作，写执行时，读必须等待。

> mysql默认隔离级别是repeatable read

## 三大设计范式

* 第一范式：数据中所有字段都是不可分割的原子值。
* 第二范式：必须满足第一范式的前提下，除主键外的每一列都必须完全依赖于主键。
* 第三范式：必须满足第二范式，除主键列外的其他列之间不能有传递依赖关系。

> 数据库主键，指的是一个列或多列的组合，其值能唯一地标识表中的每一行，通过它可强制表的实体完整性。
> 主键主要是用与其他表的外键关联，以及本记录的修改与删除。

## 查询

### 连接查询

* 内连接

  * inner join 或者 join
  * 两张表中的数据，通过某个字段相等，查询出相关记录数据，用 on… 表示条件。

  ![在这里插入图片描述](https://tva1.sinaimg.cn/large/007S8ZIlly1gh0088pu9mj30640340sj.jpg)

* 外连接

  * 左连接：left join

    * 会把左边表里面的所有数据取出来，而右边表数据如果有相等的，就显示出来，如果没有，就补 NULL。

      ![在这里插入图片描述](https://tva1.sinaimg.cn/large/007S8ZIlly1gh008kq78sj307l032744.jpg)

  * 右连接：right join

    * 会把右边表里面的所有数据取出来，而左边表数据如果有相等的，就显示出来，如果没有，就补 NULL。

    ![在这里插入图片描述](https://tva1.sinaimg.cn/large/007S8ZIlly1gh008oukaej306g0393yb.jpg)

### 查询语句的执行顺序

* 查询语句书写顺序：select-from-where-group by-having-order by-limit

* 查询语句执行顺序：from-where-group by-having-select-order by-limit

> from：决定从哪儿获取数据
> where，group by，having：决定决定显示那几行
> select：决定显示的列
> order by：对列进行排序
> limit：决定获取哪些数据

### 面试题

- 学生表student(id,name)
- 课程表course(id,name)
- 学生课程表student_course(sid,cid,score)

1. 查询student表中重名的学生，结果包含id和name，按name,id升序。

   * 需要查询某一列重复的行，一般通过**group by**(有重复的列)然后取**count>1**的值。 

   * **order by** 默认升序排列

     ```mysql
     select id, name from student where name in (
       select name from student group by name	# 分组
     having count(*) > 1	#条件
     ) order by name;
     ```
     

   > count(*)
   > 返回表中的记录数(包括所有列)，相当于**统计表的行数**(不会忽略列值为NULL的记录)
   >
   > count(1)
   > 忽略所有列，1表示一个固定值，也可以用count(2)、count(3)代替(不会忽略列值为NULL的记录)
   >
   > count(列名)
   > 返回列名指定列的记录数，列值为NULL的记录不统计在内。
   >
   > count(distinct 列名)
   > 只包括列名指定列，返回指定列的**不同值**的记录数，列值为NULL的记录不统计在内。

   

2. 在student_course表中查询平均分不及格的学生，列出学生id和平均分。

   * **where子句中不能用聚合函数作为条件表达式，但是having短语可以**；

      > where后面之所以不能使用聚合函数是因为**where的执行顺序在聚合函数之前**：
      >
      > ```mysql
      > select sum(score) from student group by student.sex where sum(student.age)>100;  # wrong
      > ```
      >
      > **having是对查出来的结果进行过滤**，那么就不能对没有查出来的值使用having： 
      >
      > ```mysql
      > select student.id,student.name from student having student.score >90; 	# wrong
      > ```

   * **where只能写在group by前边，要想在后边加限制条件，应该使用having关键字。**

      ```mysql
     select sid, avg(score) as avg_score from student_course group by sid 
     	having avg_score < 60;
     ```

   > **聚合函数是用来做纵向运算的函数**
   >
   > count()：统计指定列不为null的记录行数。
   > max()：  计算指定列的最大值
   > min()：  计算指定列的最小值
   > sum()： 计算指定列的数值和
   > avg()：  计算指定列的平均值
   >
   > **注：凡是和聚合函数同时出现的列名，则一定要写在group by之后。**

   

3. 在student_course表中查询每门课成绩都不低于80的学生id。

   * ```mysql
     select distinct sid from student_cource where sid in(
       select sid from student_cource where score > 80);
     ```

4. 总成绩最高的学生，结果列出学生id和总成绩。

   * **order by、limit**

     ```mysql
     select sid, sum(score) as sum_score from student_cource group by sid 
     	order by sum_score desc limit 1;
     ```

   > limit用来限制查询结果的起始行，以及总行数.

   

5. 在student_course表查询课程1成绩第2高的学生，如果第2高的不止一个则列出所有的学生。

   * 查询 **第N大数** 的问题

     ```mysql
     select * from student_course where cid = 1 and score = (
       # 查出第2高的成绩
       select score from student_course where cid = 1 group by score order by score desc limit 1, 1);
     ```

6. 一条SQL语句查出每个班的及格人数和不及格人数。

   表class_score，有字段name(学生姓名)、class(所在班级ID)、score(分数)

   如何用一条SQL语句查询出每个班的及格人数和不及格人数（score>=60及格），显示格式为：班级ID，及格人数，不及格人数

   ```mysql
   SELECT 
   	class as 班级ID,
   	sum(case when score >= 60 then 1 else 0 end) as 及格人数,
   	sum(case when score < 60 then 1 else 0 end) as 不及格人数
   FROM
   	class_score
   GROUP BY
   	class;
   ```

## 更新

```mysql
# MySQL-UPDATE语法：

UPDATE table_name 
SET 
    column_name1 = expr1,
    column_name2 = expr2,
    ...
WHERE
    condition;
    
# 举例：更新了员工编号1056的姓氏和电子邮件列

UPDATE employees 
SET 
    lastname = 'Hill',
    email = 'mary.hill@yiibai.com'
WHERE
    employeeNumber = 1056;
```

在上面`UPDATE`语句中：

1. 在`UPDATE`关键字后面指定要更新数据的表名。

2. `SET`子句指定要修改的列和新值。要更新多个列，请使用以逗号分隔的列表。

3. 使用WHERE语句中的条件指定要更新的行。

   `  WHERE`子句是可选的。 如果省略`WHERE`子句，则`UPDATE`语句将更新表中的所有行。

## MySQL与Redis的区别

* 类型上
  * 从类型上来说，mysql是关系型数据库，redis是缓存数据库。

* 作用上
  * mysql用于持久化的存储数据到**硬盘**，功能强大，但是读取速度较慢。
  * redis用于存储使用较为频繁的数据到**缓存**中，读取速度快。

# 计算机网络

## 计算机网络体系结构

<img src="https://tva1.sinaimg.cn/large/007S8ZIlly1gh02rwaro2j30k60gi0tc.jpg" alt="img" style="zoom:50%;" />

* 每一层的作用：
  * 物理层：通过媒介传输比特，确定机械及电气规范（比特Bit）（中继器，集线器，网关）
  * 数据链路层：将比特封装成帧和点到点的传递（帧Frame）（网桥，交换机）
  * 网络层：负责数据包从源到宿的传递和网际互连（包PackeT）（路由器）
    * 协议：IP、ICMP、ARP、RARP、OSPF、IPX、RIP、IGRP
  * 传输层：提供端到端的可靠报文传递和错误恢复（段Segment）
    * 协议：TCP、UDP
  * 应用层：允许访问OSI环境的手段（应用协议数据单元APDU）
    * 协议：FTP、DNS、Telnet、SMTP、HTTP、WWW、NFS

## TCP三次握手

### 过程

假设 A 为客户端，B 为服务器端。

1. 首先 B 处于 LISTEN（监听）状态，等待客户的连接请求；
2. A 向 B 发送连接请求报文；
3. B 收到连接请求报文，如果同意建立连接，则向 A 发送连接确认报文；
4. A 收到 B 的连接确认报文后，还要向 B 发出确认；
5. B 收到 A 的确认后，连接建立。

### 三次握手的原因

第三次握手是为了防止失效的连接请求到达服务器，让服务器错误打开连接。

客户端发送的连接请求如果在网络中滞留，那么就会隔很长一段时间才能收到服务器端发回的连接确认。客户端等待一个超时重传时间之后，就会重新请求连接。但是这个滞留的连接请求最后还是会到达服务器，如果不进行三次握手，那么服务器就会打开两个连接。如果有第三次握手，客户端会忽略服务器之后发送的对滞留连接请求的连接确认，不进行第三次握手，因此就不会再次打开连接。

## TCP四次挥手

### 过程

1. A 发送连接释放报文；
2. B 收到之后发出确认，此时 TCP 属于半关闭状态，B 能向 A 发送数据但是 A 不能向 B 发送数据。
3. 当 B 不再需要连接时，发送连接释放报文；
4. A 收到后发出确认，进入 TIME-WAIT 状态，等待 2 MSL（最大报文存活时间）后释放连接；
5. B 收到 A 的确认后释放连接。

### 四次挥手的原因

客户端发送了连接释放报文之后，服务器收到了这个报文，就进入了 CLOSE-WAIT 状态。这个状态是为了让服务器端发送还未传送完毕的数据，传送完毕之后，服务器会发送 FIN 连接释放报文。

#### 为什么要TIME_WAIT

- 确保最后一个确认报文能够到达。如果 B 没收到 A 发送来的确认报文，那么就会重新发送连接释放请求报文，A 等待一段时间就是为了处理这种情况的发生。
- 等待一段时间是为了让本连接持续时间内所产生的所有报文都从网络中消失，使得下一个新的连接不会出现旧的连接请求报文。

## TCP和UDP的区别

1. TCP面向连接，UDP无连接；
2. TCP开销比UDP小；
3. TCP提供可靠的服务，UDP不保证可靠交付；
4. 每一条TCP连接只能是点到点的，UDP支持一对一，一对多，多对一和多对多的交互通信。

## TCP如何保证数据的可靠传输

4种拥塞控制算法：慢启动，拥塞避免，快速重传和快速恢复。

1. 针对数据包丢失或者出现的定时器**超时重传**机制；
2. 针对数据包到达接收端主机顺序乱掉的顺序控制、对失序**数据进行重新排序**，然后才交给应用层；
3. 针对高效传输数据包的**流动窗口控制**；
4. 针对避免网络拥堵时候的**流量控制**；
5. 针对刚开始启动的时候避免一下子发送大量数据包而导致网络瘫痪的**慢启动算法**和**拥塞控制**。

# 操作系统

## 进程间通信的方式

* 消息传递（管道、消息队列、FIFO）
* 同步（互斥量、条件变量、读写锁、文件和写记录锁、信号量）
* 共享内存（匿名的和具名的，eg:channel）
* 远程过程调用(RPC)

## 进程和线程

- 进程是具有一定独立功能的程序关于某个数据集合上的一次运行活动，**进程是系统进行资源分配和调度的一个独立单位**。
- **线程是进程的一个实体，是CPU调度和分派的基本单位**，它是比进程更小的能独立运行的基本单位。

### 进程和线程的关系

- 一个线程只能属于一个进程，而一个进程可以有多个线程，但至少有一个线程。**线程是操作系统可识别的最小执行和调度单位**。
- 资源分配给**进程**，同一进程的所有线程**共享**该进程的所有资源。
- 真正在处理机上运行的是**线程**。
- 线程在执行过程中，需要协作同步。不同进程的线程间要利用**消息通信**的办法实现同步。

### 进程和线程的区别

- 进程有自己的独立**地址空间**，线程没有；
- 进程是**资源分配**的最小单位，线程是**CPU调度**的最小单位；
- 进程和线程通信方式不同；
  - **同一进程下的线程共享数据**(比如全局变量，静态变量)，线程通过这些数据来通信；
  - 而进程之间的通信只能通过**进程通信**的方式进行。
- 进程上下文切换**开销大**，线程**开销小**；
- 一个进程挂掉了**不会影响**其他进程，而线程挂掉了**会影响**其他线程；

### 进程和线程的优缺点：

* 进程：
  * 优点：可以使用多核
  * 缺点：资源开销大
* 线程
  * 优点：资源开销小
  * 缺点：不能使用多核

## 死锁

* 死锁概念及产生原理
  * 概念：多个并发进程因争夺系统资源而产生相互等待的现象。
  * 原理：当一组进程中的每个进程都在等待某个事件发生，而只有这组进程中的其他进程才能触发该事件，这就称这组进程发生了死锁。

   **本质原因：**

​	1）系统资源有限。

​	2）进程推进顺序不合理。

* 死锁产生的4个必要条件

  1. 互斥：某种资源一次只允许一个进程访问，即该资源一旦分配给某个进程，其他进程就不能再访问，直到该进程访问结束。
  2. 占有且等待：一个进程本身占有资源(一种或多种)，同时还有资源未得到满足，正在等待其他进程释放该资源。
  3. 不可抢占：别人已经占有了某项资源，你不能因为自己也需要该资源，就去把别人的资源抢过来。
  4. 循环等待：存在一个进程链，使得每个进程都占有下一个进程所需的至少一种资源。

## 并行 & 并发

* 并发（Concurrent），在操作系统中，是指**一个时间段中**有几个程序都处于已启动运行到运行完毕之间，且这几个程序都是在同一个处理机上运行。

* 并行（Parallel），当系统有一个以上CPU时，当一个CPU执行一个进程时，另一个CPU可以执行另一个进程，两个进程互不抢占CPU资源，可以**同时**进行，这种方式我们称之为并行(Parallel)。

> 并发的关键是你有处理多个任务的能力，不一定要同时。
> 并行的关键是你有同时处理多个任务的能力。
>
> 所以我认为它们最关键的点就是：是否是**『同时』**。

![img](https://img2018.cnblogs.com/blog/1628624/201905/1628624-20190505161932608-1136050215.jpg)

## 内存溢出 & 内存泄漏

* 内存泄漏memory leak :是指程序在申请内存后，无法释放已申请的内存空间，一次内存泄漏似乎不会有大的影响，但内存泄漏堆积后的后果就是内存溢出。 
* 内存溢出 out of memory :指程序申请内存时，没有足够的内存供申请者使用，或者说，给了你一块存储int类型数据的存储空间，但是你却存储long类型的数据，那么结果就是内存不够用，此时就会报错OOM,即所谓的内存溢出。

# Linux

## 查看

### 查看端口状态

* 查看哪些端口被打开：`netstat -anp`

* 关闭某个端口：`kill -9 PID` (PID：进程号)

  ```sh
  # 例如要关闭22号端口：
  
  $ netstat -anp | grep :22
  # 返回
  tcp 0  0 0.0.0.0:22   0.0.0.0:*  LISTEN  988/sshd
  
  # 如此，知道了22号端口对应的进程ID 988，只要kill掉该进程即可关闭该端口：
  $ kill 988
  ```

### 查看进程

`ps`：当前进程情况

`top：`实时查看进程

### **查看文件的前 n 行或者后 n 行**

```shell
 head -n 	# 查看前 n 行，将 n 替换为需要看的行数
 tail -n 	# 查后 n 行，将 n 替换为需要看的行数
 head -n file | tail -1		# 获取到文件的第 n 行
```

## 查找

### 查找文件

1. 命令格式
find [查找目录] [查找规则] [查找完后的操作]
即：find pathname -option [-print -exec -ok …]

2. 命令功能
用于在文件树中查找文件，并做相应的处理，(有可能访问磁盘)。

3. 命令参数
    （1）pathname：表示所要查找的目录路径,例如”.”表示当前目录，”/”表示根目录。
    （2）-print：将find找到的文件输出到标准输出。
    （3）-exec：对找到的文件执行exec这个参数所指定的shell命令，相应的形式为：-exec command {} \; 

  ​					  将查到的文件进行command操作，”{}”就代替查到的文件。

```shell
find . -name My_Work
```

4. 递归目录查找以.txt结尾的文件并删除

find dir -name "*.txt" | xargs rm -rf

### 查找关键字

参考：https://linux.cn/article-1672-1.html

## 修改

### 修改权限

`chmod`

`chmod 777`：所有用户都可读可写可执行

### 修改文件内容

```shell
# 将log.txt中的response替换成request
sed -i "" 's/response/request/g' log.txt
```

# 补充

## Nginx

### 什么是Nginx?

Nginx是一个web服务器和反向代理服务器，用于HTTP、HTTPS、SMTP、POP3和IMAP协议。

### 反向代理服务器是什么?

我们访问互联网上的服务时，大多数时，客户端并不是直接访问到服务端的，而是客户端首先请求到反向代理，反向代理再转发到服务端实现服务访问，通过反向代理实现路由/负载均衡等策略。这样在服务端拿到的客户端IP将是反向代理IP，而不是真实客户端IP，因此需要nginx反向代理实现获取用户真实ip

```nginx
# 客户端访问服务端的数据流走向
client(172.25.0.1) --> ADSL(192.168.0.1)--> cdn(10.0.0.1) --> SLB(反向代理)11.0.0.1 --> server(nginx)12.0.0.1
```

**反向代理服务器可以隐藏源服务器的存在和特征。它充当互联网云和web服务器之间的中间层，提高了安全性。**

### Nginx如何处理HTTP请求？

Nginx使用反应器模式。主事件循环等待操作系统发出准备事件的信号，这样数据就可以从套接字读取，在该实例中读取到缓冲区并进行处理。单个线程可以提供数万个并发连接。

# 面试模拟

1. 自我介绍

2. 介绍一下实习的项目，你都做了什么？

3. 介绍一下实验室的项目，你都做了什么？

4. 测试流程、测试方法？

5. 自动化测试的流程、case如何编写？

   ...

---

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

将待排序的序列构造成一个大顶堆。此时，整个序列的最大值就是堆顶的根节点。将它移走(其实就是将其与堆数组的末尾元素交换，此时末尾元素就是最大值)，然后将剩余的n-1个序列重新构造成一个堆，这样就会得到n个元素中的次最大值。如此反复执行，就能得到一个有序序列了。这个过程其实就是先构建一个最大/最小二叉堆，然后不停的取出最大/最小元素（头结点），插入到新的队列中，以此达到排序的目的。

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

不要跳进递归（你的脑袋能压几个栈呀？），而是要根据刚才函数定义，来弄清楚这段代码会产生什么结果：

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

如果 `m != 1` 怎么办？如果我们把 `head` 的索引视为 1，那么我们是想从第 `m` 个元素开始反转；
如果把 `head.next` 的索引视为 1 呢？那么相对于 `head.next`，反转的区间应该是从第 `m - 1` 个元素开始的；
那么对于 `head.next.next` 呢？区别于迭代思想，这就是递归思想，所以我们可以完成代码：

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
        queue, res = [root], []
        while queue:
            level = []
            for _ in range(len(queue)):
                cur = queue.pop(0)
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

而对于这道题目，当窗口扩大的时候可能遇到负数，窗口中的值也就可能增加也可能减少，这种情况下不知道什么时机去收缩左侧窗口，也就无法求出「最大子数组和」。

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

一般来说，这类问题都是让你求一个**最长**子序列，一旦涉及到子序列和最值，那几乎可以肯定，**考察的是动态规划技巧，时间复杂度一般都是 O(n^2)**。

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

为啥最长递增子序列需要这种思路呢？因为这样符合归纳法，可以找到状态转移的关系，这里就不具体展开了。

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

从10万个数中找10个最大的数

我们首先取10万个元素中的前10个元素来建立由10个元素组成的最小堆。这样堆顶元素便是当前已知元素的第10大的数；然后依次读取剩下的99990个元素，若读取的元素比堆顶元素大，则将堆顶元素和当前元素替换，并自堆顶至下调整堆；这样读取完所有元素后，堆中的10个元素即为这10万个数最大的10个数，同时堆顶元素为这10万个元素第10大元素。
时间复杂度：
设从N个数中找M个最大数
每次重新恢复堆的时间复杂都为O(logM),最多供进行了（N-M）次恢复堆操作，顾时间复杂度为O(NlogM)。



给40亿个不重复的unsigned int的整数，没排过序的，然后再给几个数，如何快速判断这几个数是否在那40亿个数当中?
unsigned int 的取值范围是0到2^32-1。我们可以申请连续的2^32/8=512M的内存，用每一个bit对应一个unsigned int数字。首先将512M内存都初始化为0，然后每处理一个数字就将其对应的bit设置为1。当需要查询时，直接找到对应bit，看其值是0还是1即可。



#### [26. 删除排序数组中的重复项](https://leetcode-cn.com/problems/remove-duplicates-from-sorted-array/)

```python
def removeDuplicates(self, nums: List[int]) -> int:
        i, j = 0, 1
        while j < len(nums):
            if nums[i] == nums[j]:
                j += 1
            else:
                i += 1
                nums[i] = nums[j]
        return i + 1
```

#### [27. 移除元素](https://leetcode-cn.com/problems/remove-element/)

```python
def removeElement(self, nums: List[int], val: int) -> int:
        length = len(nums)
        i, j = 0, 0
        while j < length:
            if nums[j] != val:
                nums[i] = nums[j]
                i += 1
                j += 1
            else:
                j += 1

        return i
```

