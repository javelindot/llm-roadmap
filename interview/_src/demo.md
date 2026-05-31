## 淘天
1. AI相关的项目做过几个？分别是什么场景？

2. AI RAG项目是你参与了还是全程你自己做的？

3. AI RAG项目是基于开源项目做的吗？

4. 做AI RAG项目时的思路是怎样的？

5. 知识库上传支持什么类型的文档？

6. PDF扫描件支持吗？如果想要支持这种扫描件的话，有思路吗？

7. 上传的文档中包含图片吗？处理图片了吗？

8. 文档里的图片处理后存到哪里去了？

9. 把图片转为文字描述是怎么做的？

10. 像PDF、Word图文混排的文档怎么处理图片与文字？

11. Excel里面的图表有处理吗？

12. 文档解析完后，切片是怎么做的？

13. 召回阶段时的召回策略是怎样的？

14. 为什么选择Top10？

15. 有测过回答的准确率吗？

16. 70% 准确率你觉得能满足生产环境的要求吗？

17. 如果客户要求至少要 90% 的准确率，你有什么解决方案？

18. 有什么有效的方法能将准确率从 70% 提升到 90%？

19. 总共有几个知识库？

20. 怎么做知识库路由的？

21. 路由选择的时候有选错的情况吗？

22. 除了RAG以外，还学另外的一些AI相关的技术吗？

23. ReAct的思路是怎样的？跑过Demo吗？

24. ReAct的应用场景在哪里？

25. 了解SKILLS吗？

26. 有养龙虾吗？自己本地部署了吗？

27. 云上部署龙虾会有安全性问题吗？

28. 本地部署龙虾有什么办法可以让它安全去跑？

29. Python熟练度怎样？

30. 实际项目中用过langchain吗？



## 3.31 
一、基础技术概念类

1. 请详细介绍React框架以及自主抉择Agent的核心概念、工作原理与应用场景？
2. 项目开发过程中具体运用了哪些设计模式？
3. React、自主抉择模式、状态机、策略模式在项目中分别如何落地使用？选择使用这些技术和模式的核心原因是什么？
4. 结合项目实际，深度思考并阐述自主抉择Agent与相关技术模式的完整实现思路？

二、项目技术架构与框架选型类

5. 整个项目采用了什么技术框架？为何选择Python语言来开发RAG相关模块？
6. 你是否熟练掌握Python？若项目涉及跨语言开发需求，会采取怎样的解决方案？
7. 是否使用过VibeCoding、CC、Cursor这类开发工具？请简单介绍其使用体验与核心功能特点？
8. 项目中使用过哪些大语言模型（LLM）？不同大语言模型的核心区别是什么？各自适配什么样的业务场景？
9. 实际使用过程中若大语言模型出现异常，你会采取切换模型还是其他优化处理方式？具体解决方案是什么？

三、RAG与向量检索类

10. RAG知识查询环节有哪些方法可以提升查询结果的精准度？
11. 请解释Query重写的定义、作用，以及在RAG系统中的实现逻辑？
12. 项目中PDF文件的上传流程是怎样的？如何处理PDF中的图片内容？
13. 项目采用的向量库是什么？如何实现混合检索功能？

四、Agent工作流与工具调用类

14. FunctionCall工具调用的完整流程是什么？
15. 自主抉择Agent的工作流具体如何实现？
16. 项目中的上下文信息如何处理与管理？
17. RAG知识查询、Agent工具执行过程中出现错误该如何处理？有哪些优化策略？
18. Tools工具处理数据时是否运用相关算法？例如经纬度这类模型处理不准确的数据，如何通过Tools做算法优化处理？

五、PPT生成与状态管理类

19. 项目中PPT生成的完整流程是什么？断点恢复功能如何实现？
20. 项目中的状态数据采用何种方式存储？存储方案的设计思路是什么？
21. PPT模板在项目中如何使用？适用于哪些业务场景？是否支持用户自定义模板？

六、模型评估与优化类

22. 项目中通过什么方式评判大模型回答的准确性？具体的打分标准与评估流程是什么？
23. 模型回答评估为何采用奇数次评判的方式？核心考量是什么？



## 4.1 
1、父子分块

2、es做向量库 1亿数据怎么优化

3、上下文压缩

4、上下文压缩的大小怎么评判

5、requestbody调用ai过长了 怎么办

6、如果不用springai 调用api怎么实现agent调用

7、模型怎么评判答案是否准确

8、为什么选取top10

9、线上频繁fullgc怎么办



## **<font style="color:rgb(36, 41, 46);">志丞科技</font>**
**<font style="color:rgb(36, 41, 46);">xxx项目</font>**

**<font style="color:rgb(36, 41, 46);">1.主要负责的模块</font>**

**<font style="color:rgb(36, 41, 46);">2.控制在秒级是怎么做到的</font>**

**<font style="color:rgb(36, 41, 46);">3.模型做过微调吗？如果你要做nl2sql模型的调优你会怎么做</font>**

<font style="color:rgb(36, 41, 46);">选用强大一点的基座模型</font>

<font style="color:rgb(36, 41, 46);">对场景领域做专门调优，构建问题，sql的数据集</font>

<font style="color:rgb(36, 41, 46);"></font>

<font style="color:rgb(36, 41, 46);">xxx多智能体项目</font>

**<font style="color:rgb(36, 41, 46);">1.主要负责哪块</font>**

**<font style="color:rgb(36, 41, 46);">2.主agent和子agent的交互是怎么做？</font>**

**<font style="color:rgb(36, 41, 46);">3.sse网络波动中的断线重连的问题是怎么处理的？</font>**

<font style="color:rgb(36, 41, 46);">心跳机制：服务端定期发送空注释（:ping\n\n），检测连接是否断开</font>

<font style="color:rgb(36, 41, 46);">断线续传：为每个事件分配id，客户端重连时携带Last-Event-ID，服务端从断点补发。</font>

**<font style="color:rgb(36, 41, 46);">4.历史记录的存储和优化你是怎么处理的</font>**

**<font style="color:rgb(36, 41, 46);">5.主agent和子agent会涉及文件的交互吗？如果要做这个内容你会怎么做？</font>**

**<font style="color:rgb(36, 41, 46);">6.mcp你有了解过吗，mcp的通信协议，mcp定义的标准协议定义了哪些标准的资源类型</font>**

<font style="color:rgb(36, 41, 46);">通过标准化接口实现ai和外部资源的对接，比如工具，它有三种通信协议：streaming http、stdio、sse，主要核心就是有一个服务端提供mcp服务，客户端调用这个服务。 资源类型：model、agent、tool、session、task、resource</font>

**<font style="color:rgb(36, 41, 46);">7.skills用过吗，用过这方面的开源的coding和工具类似openclaw这样的，如果在子智能体要用skills改造这个项目你会怎么做呢</font>**

<font style="color:rgb(36, 41, 46);">skills是可复用、动态加载的专业技能包，可以通过定义结构化的流程让模型具备处理复杂任务的能力。</font>

<font style="color:rgb(36, 41, 46);">构建一个skill主要有4块内容，有一个是必须要的，就是一个skill.md的文件，这个文件里面包含两个部分，一个部分是metadata元数据，比如有name，description，可以把它当成这个文件的标题，模型执行你的指令的时候只要先加载这一小部分的内容，看是不是跟你需求是对应的，对应上的才会加载第二部分就是这个指令，也就是提示词，剩下还有reference文件这个相当于提示词的补充，还有assets文件可以提供一些图片等资源，还有一个script脚本可以当作工具用来具体处理任务的。</font>

<font style="color:rgb(36, 41, 46);">我认为skills是人工智能的一次变革吧，以前处理一个需求，用户需要通过多轮对话的形式一步一步来解决这个问题，现在只要agent能读懂你的需求，他就可以按照这个标准化的模板来执行整个流程。相当于从传统的指导agent做事到让agent读懂你的需求这方向转变。</font>

<font style="color:rgb(36, 41, 46);">skills不是给ai装上工具，因为给ai装上工具更像是mcp的功能，而skills专业手册+操作说明+业务执行模板</font>

**<font style="color:rgb(36, 41, 46);">8.遇到的最有挑战性的问题，你是怎么解决的</font>**

<font style="color:rgb(36, 41, 46);"></font>

<font style="color:rgb(36, 41, 46);"></font>

<font style="color:rgb(36, 41, 46);">强化学习怎么做的？</font>

**<font style="color:rgb(36, 41, 46);">1.ppo微调是你一个人负责的吗，还是有其他人一起的</font>**

**<font style="color:rgb(36, 41, 46);">2.数据集是怎么来的</font>**

<font style="color:rgb(36, 41, 46);">反问：</font>

## **<font style="color:rgb(36, 41, 46);">不鸣科技</font>**
**<font style="color:rgb(36, 41, 46);">1.问数：模型工具调错了，任务出现异常怎么处理</font>**

**<font style="color:rgb(36, 41, 46);">2.大模型是怎么调用工具的</font>**

<font style="color:rgb(36, 41, 46);">用户问题+工具列表→大模型→理解意图→输出结构化调用指令→外部框架执行→结果返回总结</font>

**<font style="color:rgb(36, 41, 46);">2.同步、异步</font>**

**<font style="color:rgb(36, 41, 46);">3.线程、进程、携程</font>**

**<font style="color:rgb(36, 41, 46);">4.父类的私有属性子类想调用怎么实现</font>**

**<font style="color:rgb(36, 41, 46);">5.graphrag相比传统的rag的优势</font>**

<font style="color:rgb(36, 41, 46);">支持多跳推理，能解决传统 RAG 无法处理的复杂、跨维度问题 商品-属于-品类-关联-配件</font>

**<font style="color:rgb(36, 41, 46);">6.大模型长时间没有输出结果，任务出现问题了怎么处理</font>**

## **<font style="color:rgb(36, 41, 46);">黑云科技</font>**
**<font style="color:rgb(36, 41, 46);">1.有做过用户体系吗</font>**

<font style="color:rgb(36, 41, 46);">在cyberai智能问数助手这个项目中是没有构建用户体系的，因为这是tob的项目，针对的是企业内部的业务人员以及基于这些数据做决策的人员，综合考虑不需要用户体系和多轮对话，</font>

<font style="color:rgb(36, 41, 46);">但是在多智能体电商服务系统里面是构建用户体系的，因为要基于用户id和session id 做多轮对话。</font>

**<font style="color:rgb(36, 41, 46);">2.历史的对话信息是怎么保存的</font>**

<font style="color:rgb(36, 41, 46);">保存在数据库里面，通过用户id、session id拿到数据加到大模型提示词里面，做了上下文窗口的限制最多5轮对话，做了文本的摘要。</font>

**<font style="color:rgb(36, 41, 46);">3.task2sql的节点和流程</font>**

**<font style="color:rgb(36, 41, 46);">4.指标是什么，有什么</font>**

<font style="color:rgb(36, 41, 46);">指标比如说有gmv销售总额，aov平均单价，uv，pv，退单率，退货率，复购率，点击率这些</font>

**<font style="color:rgb(36, 41, 46);">5.响应控制时长是多久</font>**

<font style="color:rgb(36, 41, 46);">我们采用的是sse流式响应，从用户的输入到生成第一个token的延迟在毫秒级，返回最终结果得看任务的复杂度，在问数助手里面比较稳定，我们控制在秒级，一般10秒内就能看到最终的结果。</font>

**<font style="color:rgb(36, 41, 46);">6.模型是自己部署的吗，vllm的原理是什么</font>**

<font style="color:rgb(36, 41, 46);">核心原理：PagedAttention（分页注意力）</font>

<font style="color:rgb(36, 41, 46);">核心思路：</font>

<font style="color:rgb(36, 41, 46);">将 KV Cache 拆分成固定大小的page（比如 16/32 个 tokens）；</font>

<font style="color:rgb(36, 41, 46);">每个请求的 KV Cache 不再占用连续显存，而是由多个离散的page组成；</font>

<font style="color:rgb(36, 41, 46);">用一个page table记录每个请求的 KV Cache 页存在显存的哪个位置。</font>

**<font style="color:rgb(36, 41, 46);">7.qwen3的思考模式怎么开启</font>**

<font style="color:rgb(36, 41, 46);">在部署的时候有一个参数enable_thinking，你设置为true时就可以开启思考模式了。</font>

**<font style="color:rgb(36, 41, 46);">8.在langgraph里面是怎么实现sse的流式输出的</font>**

<font style="color:rgb(36, 41, 46);">graph.astream（）可以实现最终的结果的流式输出，里面有个参数stream_mode设置成了custom自定义，你在节点定义一个stream_writer，然后写write能实现自定义内容的流式输出。</font>

**<font style="color:rgb(36, 41, 46);">9.整个4b的模型是怎么微调的，上下文窗口多大</font>**

<font style="color:rgb(36, 41, 46);">全参微调，1个a800</font>

**<font style="color:rgb(36, 41, 46);">10.多智能体项目有什么难点或者亮点</font>**

<font style="color:rgb(36, 41, 46);">难点：意图识别不准确</font>

<font style="color:rgb(36, 41, 46);">亮点：架构，响应延迟的优化。</font>

**<font style="color:rgb(36, 41, 46);">11.这个有没有对业务场景做专业性的优化：</font>**

<font style="color:rgb(36, 41, 46);">集成了CyberAI 运动装备垂类知识库。</font>

<font style="color:rgb(36, 41, 46);">提示词方面的优化。</font>

**<font style="color:rgb(36, 41, 46);">12.bert和gpt区别</font>**

## 
## **<font style="color:rgb(36, 41, 46);">拼夕夕</font>**
**<font style="color:rgb(36, 41, 46);">1.问数这个项目实现方案</font>**

**<font style="color:rgb(36, 41, 46);">2.怎么去确保字段信息召回的时候是准确的</font>**

<font style="color:rgb(36, 41, 46);">元数据知识库构建的越好。</font>

<font style="color:rgb(36, 41, 46);">检索方面提高召回准确率。查询重述、多查询、假设性文档、rrf、rerank</font>

**<font style="color:rgb(36, 41, 46);">3.做查询的时候还有其他手段</font>**

**<font style="color:rgb(36, 41, 46);">4.关键字提取，意思是一样，字段是不一样的问题</font>**

**<font style="color:rgb(36, 41, 46);">5.关键词扩展这种方式你就得优势在哪里，劣势在哪里</font>**

<font style="color:rgb(36, 41, 46);">优势：关键词信息丢失的问题，提升检索召回率</font>

<font style="color:rgb(36, 41, 46);">劣势：推理延迟、专业术语很难检索</font>

**<font style="color:rgb(36, 41, 46);">6.专业名词在大模型扩展这方面是很难处理的</font>**

<font style="color:rgb(36, 41, 46);">专业词库 + 元数据注入</font>

**<font style="color:rgb(36, 41, 46);">7.处理字段取值召回es这种拆词的召回，还有没有其他的方案</font>**

<font style="color:rgb(36, 41, 46);">基于知识图谱的召回</font>

**<font style="color:rgb(36, 41, 46);">8.vllm调整过哪些参数来适配业务场景，比如qps1000+，延迟控制在5s</font>**

<font style="color:rgb(36, 41, 46);">tensor_parallel_size</font>

<font style="color:rgb(36, 41, 46);">max_num_batched_tokens</font>

<font style="color:rgb(36, 41, 46);">gpu_memory_utilization</font><font style="color:rgb(36, 41, 46);"> </font>**<font style="color:rgb(36, 41, 46);">9.vllm部署遇到的坑</font>**

<font style="color:rgb(36, 41, 46);">gpu显存占用满了</font>

**<font style="color:rgb(36, 41, 46);">10.模型量化在项目内有考虑过吗，怎么评估他精度的损失在不在你可接受的范围内</font>**

<font style="color:rgb(36, 41, 46);">显存够用就不用开，如果再后续使用的时候发现显存被占满了，可以考虑开启量化，跑量化前后的测试集</font>

**<font style="color:rgb(36, 41, 46);">11.langgraph介绍一下</font>**

## **<font style="color:rgb(36, 41, 46);">脉链集团（2人）</font>**
**<font style="color:rgb(36, 41, 46);">1.coze、dify你之前有用过吗</font>**

**<font style="color:rgb(36, 41, 46);">2.ppo跟dpo有什么区别</font>**

**<font style="color:rgb(36, 41, 46);">3.0.5b训练出来的模型出现刷分，奖励黑客的情况怎么处理</font>**

**<font style="color:rgb(36, 41, 46);">4.介绍项目</font>**

## **<font style="color:rgb(36, 41, 46);">环球老虎财经</font>**
**<font style="color:rgb(36, 41, 46);">1.transformer架构、位置编码、梯度消失与梯度爆炸怎么解决、</font>**

**<font style="color:rgb(36, 41, 46);">2.列表推导式和生成器、线程、进程、协程、线程在python中可以并行执行吗</font>**

**<font style="color:rgb(36, 41, 46);">3.对于pdf文档怎么处理、持续性的文档怎么处理的</font>**

**<font style="color:rgb(36, 41, 46);">4.skill你了解吗</font>**

## **<font style="color:rgb(36, 41, 46);">海莱云智</font>**
**<font style="color:rgb(36, 41, 46);">1.对native rag有了解吗</font>**

**<font style="color:rgb(36, 41, 46);">2.对数据下钻这种场景是怎么做的</font>**

**<font style="color:rgb(36, 41, 46);">3.数据分析类的模型你有了解吗</font>**

## **<font style="color:rgb(36, 41, 46);">云趣科技（2人）</font>**
**<font style="color:rgb(36, 41, 46);">1.主调度的agent如何决定调用哪一个专家</font>**

<font style="color:rgb(36, 41, 46);">通过提示词优化，让用户的需求和具体的专家智能体一一对应，并严格的限制它只能基于用户的提问进行意图识别，不要猜测用户的意图，通过提示词优化的手段，提高它意图识别的准确率</font>

<font style="color:rgb(36, 41, 46);">怎么调用的聊框架</font>

**<font style="color:rgb(36, 41, 46);">2.主调度智能体任务分发错误、重复调用的情况，在业务上拆分、在技术上怎么避免</font>**

<font style="color:rgb(36, 41, 46);">在业务上拆分，专家智能体拆分足够细，让它每个专家只处理它对应领域的那一部分任务，不要出现两个专家都能处理同一个任务的情况。</font>

<font style="color:rgb(36, 41, 46);">在技术上，设置唯一id，主调度 Agent 在分发任务前先检查 “任务 ID - 专家 Agent” 的映射缓存，若已存在未完成的映射则拒绝重复分发</font>

<font style="color:rgb(36, 41, 46);">设置最大交互轮数</font>

**<font style="color:rgb(36, 41, 46);">3.怎么跳出主调度智能体和子智能体的循环</font>**

<font style="color:rgb(36, 41, 46);">设置最大交互轮数，用计数器来计数，调用子智能体前查看是否达到最大上限达到就跳出</font>

**<font style="color:rgb(36, 41, 46);">4.如果任务执行失败了，怎么处理</font>**

**<font style="color:rgb(36, 41, 46);">5.agent怎么知道该调用哪一个工具，简单说一下这里面进行大模型进行交互的message类型</font>**

<font style="color:rgb(36, 41, 46);">System Message、user message 、assisant message 工具调用响应：结构化格式（如 JSON），包含 “tool_call_id”（工具调用 ID）、“tool_name”（目标工具名）、“arguments”（工具入参），用于触发具体工具执行。</font>

**<font style="color:rgb(36, 41, 46);">6.如果返回异常数据或者超时怎么处理</font>**

<font style="color:rgb(36, 41, 46);">基于规则的校正</font>

<font style="color:rgb(36, 41, 46);">心跳机制+重连/断点续传</font>

<font style="color:rgb(36, 41, 46);"></font>

## **<font style="color:rgb(36, 41, 46);">云趣科技-二面</font>**
**<font style="color:rgb(36, 41, 46);">1.为什么选择langgraph而不选择langchain</font>**

**<font style="color:rgb(36, 41, 46);">2.langgraph里面state包含哪些东西呢</font>**

**<font style="color:rgb(36, 41, 46);">3.state会太大吗，如果state太大怎么处理</font>**

<font style="color:rgb(36, 41, 46);">输入的参数设置</font>

<font style="color:rgb(36, 41, 46);">设置最大的召回数量、过滤无关信息</font>

<font style="color:rgb(36, 41, 46);">文档进行摘要总结</font>

**<font style="color:rgb(36, 41, 46);">4.基于历史对话的处理</font>**

<font style="color:rgb(36, 41, 46);">最大的交互轮数</font>

<font style="color:rgb(36, 41, 46);">摘要总结</font>

**<font style="color:rgb(36, 41, 46);">5.什么时候结束workflow</font>**

**<font style="color:rgb(36, 41, 46);">6.重试会有retry机制吗，怎么防止它无限重试</font>**

**<font style="color:rgb(36, 41, 46);">7.langgraph有重试的机制和中断的机制吗</font>**

**<font style="color:rgb(36, 41, 46);">8.chunk_size怎么选择</font>**

**<font style="color:rgb(36, 41, 46);">9.用户提的问题怎么对应是哪张表</font>**

**<font style="color:rgb(36, 41, 46);">元数据知识库的设计</font>**

**<font style="color:rgb(36, 41, 46);">问数智能体召回的准确率</font>**

**<font style="color:rgb(36, 41, 46);">10.有做检验吗</font>**

**<font style="color:rgb(36, 41, 46);">11.系统有做反馈系统</font>**

**<font style="color:rgb(36, 41, 46);">12.提示词是怎么确定，做了版本的管理吗</font>**

<font style="color:rgb(36, 41, 46);">大模型初版+提示词优化（三步）</font>

**<font style="color:rgb(36, 41, 46);">13.有端到端的系统测试吗</font>**

**<font style="color:rgb(36, 41, 46);">14.mysql的binlog日志</font>**

**<font style="color:rgb(36, 41, 46);">15.同步的搭建是你做的吗</font>**

**<font style="color:rgb(36, 41, 46);">16.验证这个sql是不是正确的是跑这个执行计划吗</font>**

**<font style="color:rgb(36, 41, 46);">17.复杂sql执行慢</font>**

## **<font style="color:rgb(36, 41, 46);">海创医疗</font>**
**<font style="color:rgb(36, 41, 46);">1.工作流流程</font>**

**<font style="color:rgb(36, 41, 46);">2.项目实现细节问题</font>**

**<font style="color:rgb(36, 41, 46);">3.意图识别不准确</font>**

**<font style="color:rgb(36, 41, 46);">4.智能体调用工具，但工具传递的参数很多会导致的问题，怎么解决</font>**

## **<font style="color:rgb(36, 41, 46);">极豆车联网</font>**
**<font style="color:rgb(36, 41, 46);">1.sft样本、做过几个上线的llm、微调的框架、训练集是哪来的、一开始提供的就是这个有标签的数据集吗</font>**

**<font style="color:rgb(36, 41, 46);">2.问数助手服务的是谁、周活多少、元数据是什么</font>**

**<font style="color:rgb(36, 41, 46);">3.召回的链路、漏召回怎么处理</font>**

**<font style="color:rgb(36, 41, 46);">4.准确率是怎么算的</font>**

**<font style="color:rgb(36, 41, 46);">5.异常警告是怎么做的</font>**

**<font style="color:rgb(36, 41, 46);">6.评论模型的目标是什么、人工标注多少条</font>**

**<font style="color:rgb(36, 41, 46);">7.ppo的稳态主要靠什么、KL散度惩罚力度太大会怎么样</font>**

**<font style="color:rgb(36, 41, 46);">8.agent与专家agent怎么路由</font>**

**<font style="color:rgb(36, 41, 46);">9.rrf是什么</font>**

**<font style="color:rgb(36, 41, 46);">10.sft微调的方式有哪些、微调过哪些模型</font>**

**<font style="color:rgb(36, 41, 46);">11.微调过多模态模型</font>**

**<font style="color:rgb(36, 41, 46);">12.用过端侧模型</font>**

**<font style="color:rgb(36, 41, 46);">13.vllm做过哪些参数调整</font>**

**<font style="color:rgb(36, 41, 46);">14.服务是通过linux部署吗、用gpu加速吗、是用docker和k8s部署吗</font>**



## <font style="color:rgb(36, 41, 46);">百康泰斯-一面</font>
**<font style="color:rgb(36, 41, 46);">1.整体流程链路，怎么从自然语言-sql-自然语言</font>**

**<font style="color:rgb(36, 41, 46);">1.这个项目做过哪些优化吗比如数据上，查询上</font>**

<font style="color:rgb(36, 41, 46);">响应的优化</font>

<font style="color:rgb(36, 41, 46);">查询准确率的优化</font>

**<font style="color:rgb(36, 41, 46);">2.多路召回的多路体现在什么地方</font>**

**<font style="color:rgb(36, 41, 46);">3.向量是怎么做的，基于kv，为什么用milvus向量索引，es做全文索引</font>**

**<font style="color:rgb(36, 41, 46);">4.es索引的是哪部分，做了哪些操作</font>**

**<font style="color:rgb(36, 41, 46);">5.动态剪枝是怎么做的，sql自修正闭环是怎么做的</font>**

**<font style="color:rgb(36, 41, 46);">6.上下文注入是做什么，agent本身是能知道时间信息的为什么还要再进行时间的注入呢</font>**

**<font style="color:rgb(36, 41, 46);">7.为什么不用react这种方式呢</font>**

**<font style="color:rgb(36, 41, 46);">8.准确率是怎么得到的，多行多列的数据是怎么正确的，</font>**

**<font style="color:rgb(36, 41, 46);">9.为什么你做数据平台为什么还要做这么toc的业务，这个项目做到多细致</font>**

<font style="color:rgb(36, 41, 46);">侧重点在于解决他们的需求么，就是商品指导缺失、咨询响应速度满。</font>

**<font style="color:rgb(36, 41, 46);">10.每个智能体是独立的环境，调用同一个大模型，怎么体现他们的区别，没有区别为什么不做一块，每一个子智能体都调用同一个大模型，就提示词不一样吗，</font>**

<font style="color:rgb(36, 41, 46);">类似主级结构</font>

**<font style="color:rgb(36, 41, 46);">11.模型的推理的速度是怎么提升的，大模型推理的优化手段</font>**

<font style="color:rgb(36, 41, 46);">量化、知识蒸馏、kvcache。</font>

**<font style="color:rgb(36, 41, 46);">12.数据脱敏是怎么做的，基于规则（正则匹配）</font>**

**<font style="color:rgb(36, 41, 46);">13.智能评论生成系统需求是什么，为什么要加KL散度，</font>**

## **<font style="color:rgb(36, 41, 46);">百康泰斯-二面</font>**
**<font style="color:rgb(36, 41, 46);">1.介绍一个项目</font>**

**<font style="color:rgb(36, 41, 46);">2.动态剪枝是怎么做的</font>**

**<font style="color:rgb(36, 41, 46);">3.有多少张表</font>**

**<font style="color:rgb(36, 41, 46);">4.用户的问题可能会对应几张表，但是提的问题可能没有显示出来的，这个是怎么处理</font>**

<font style="color:rgb(36, 41, 46);">添加额外的上下文信息，比如外键，或者描述的注入</font>

**<font style="color:rgb(36, 41, 46);">5.前端是你这边实现的吗</font>**

**<font style="color:rgb(36, 41, 46);">6.用户问的信息不准确，怎么实现进一步追问获取这个信息，类似多轮对话的形式，比如说用户想要统计全年的销售总额，但是这个全年不明确，要让模型有这个能力去反问用户是25年还24年这样。或者调用一个什么什么工具需要什么参数，但是用户提供不全，来反问用户问题得到这个参数，具体实现细节。</font>**

<font style="color:rgb(36, 41, 46);">提示词+记忆+中断</font>

**<font style="color:rgb(36, 41, 46);">7.记忆怎么设计</font>**

**<font style="color:rgb(36, 41, 46);">8.文件存储怎么设计，比如什么时候把文件放在本地，什么时候把文件放在远端。</font>**

<font style="color:rgb(36, 41, 46);">冷热处理</font>

**<font style="color:rgb(36, 41, 46);">9.openclaw内部调用是怎么使用</font>**

**<font style="color:rgb(36, 41, 46);">10.openclaw遇到这个任务本身就无解的怎么处理，本身在物理层面已经解决不了这个问题了，你怎么处理。</font>**

**<font style="color:rgb(36, 41, 46);">11.ppo里面几个模型作用</font>**

**<font style="color:rgb(36, 41, 46);">12.奖励模型的奖励是怎么设计</font>**

**<font style="color:rgb(36, 41, 46);">13.训练数据是人工标的吗，标签是怎么来的，你这个模型是qwen0.5b，为什么不考虑bert，模型的选择是怎么考虑的</font>**

**<font style="color:rgb(36, 41, 46);">14.奖励模型的指标</font>**

<font style="color:rgb(36, 41, 46);">准确率、精确率、召回率、f1分数</font>

## **<font style="color:rgb(36, 41, 46);">百康泰斯-三面</font>**
**<font style="color:rgb(36, 41, 46);">1.离职原因、公司业务是怎么样的</font>**

**<font style="color:rgb(36, 41, 46);">2.问数底层用的数据库是什么、nl2sql的流程</font>**

<font style="color:rgb(36, 41, 46);">存储元数据知识库是mysql</font>

<font style="color:rgb(36, 41, 46);">存储向量milvus、es</font>

<font style="color:rgb(36, 41, 46);">执行sql是在hive中执行的</font>

**<font style="color:rgb(36, 41, 46);">3.用户在输入的时候输入的是一个模糊的问题、比如用户在问订单时间，但是元数据里面有用户的订单时间和商家的订单时间。</font>**

<font style="color:rgb(36, 41, 46);">中英文、专业术语类 ---- 大模型扩展+元数据注入</font>

<font style="color:rgb(36, 41, 46);">参数缺失类 ---- function tool + 追问</font>

<font style="color:rgb(36, 41, 46);">模糊对应（1对多）类 ---- 追问</font>

<font style="color:rgb(36, 41, 46);">复杂sql类 — 接口</font>

**<font style="color:rgb(36, 41, 46);">4.追问环节的设计</font>**

<font style="color:rgb(36, 41, 46);">提示词 + 中断返回参数前端提问设计 + 追问参数解析 + 融合之前解析的内容</font>

**<font style="color:rgb(36, 41, 46);">5.这个查询是异步的吗</font>**

<font style="color:rgb(36, 41, 46);">async 、await</font>

**<font style="color:rgb(36, 41, 46);">6.最长等待时间设置是多少</font>**

<font style="color:rgb(36, 41, 46);">1分钟</font>

**<font style="color:rgb(36, 41, 46);">7.最大的表有多少条</font>**

<font style="color:rgb(36, 41, 46);">设置最大的字段取值上限10000</font>

**<font style="color:rgb(36, 41, 46);">8.如果这个数据量很大在hive里面跑会很慢，怎么处理</font>**

<font style="color:rgb(36, 41, 46);">新增一个接口提前执行好sql，保存sql的结果 + 意图识别</font>

**<font style="color:rgb(36, 41, 46);">9.为什么执行sql不考虑在es里面检索</font>**

<font style="color:rgb(36, 41, 46);">es得考虑存不存的下，存的下性能方面会不会有很大的损失。</font>

**<font style="color:rgb(36, 41, 46);">10.多智能体电商服务系统介绍一下</font>**

**<font style="color:rgb(36, 41, 46);">11.专家智能体的构建按照什么标准来划分的</font>**

<font style="color:rgb(36, 41, 46);">任务拆的足够细，每个专家智能体只处理对应领域的那一部分任务</font>

**<font style="color:rgb(36, 41, 46);">12.专家智能体设计是独立完成的吗</font>**

**<font style="color:rgb(36, 41, 46);">13.自然语言的模型和虚拟细胞的模型串在一起</font>**

## **<font style="color:rgb(36, 41, 46);">杭州鼎智云(算法工程师3-4个)</font>**
**<font style="color:rgb(36, 41, 46);">1.最新的前沿技术你了解哪些？</font>**

**<font style="color:rgb(36, 41, 46);">2.openclaw的框架是怎么样的，这个框架有什么优势、劣势</font>**

**<font style="color:rgb(36, 41, 46);">3.详细说一下langgraph的节点和流程</font>**

**<font style="color:rgb(36, 41, 46);">4.当时技术选型是怎么样的，为什么用langgraph而不选择langchain</font>**

**<font style="color:rgb(36, 41, 46);">5.agent里面的机制</font>**

<font style="color:rgb(36, 41, 46);">agent4大方面+function tool 机制</font>

**<font style="color:rgb(36, 41, 46);">6.怎么解决agent的幻觉</font>**

<font style="color:rgb(36, 41, 46);">提示词+外挂知识库（rag/微调）</font>

**<font style="color:rgb(36, 41, 46);">7.多agent怎么做全局的状态管理</font>**

<font style="color:rgb(36, 41, 46);">说框架+agent as tool+内存的状态主从机制组偶状态管理，外部参考/共享文档+路径管理</font>

**<font style="color:rgb(36, 41, 46);">8.做ai工程化落地</font>**

## **<font style="color:rgb(36, 41, 46);">麦麦科技-一面</font>**
<font style="color:rgb(36, 41, 46);">xxx项目</font>

**<font style="color:rgb(36, 41, 46);">1.langgraph的工作流核心节点与流转</font>**

**<font style="color:rgb(36, 41, 46);">2.准确率提升是怎么做到的</font>**

<font style="color:rgb(36, 41, 46);">架构的设计</font>

<font style="color:rgb(36, 41, 46);">rag检索增加设计</font>

<font style="color:rgb(36, 41, 46);"></font>

<font style="color:rgb(36, 41, 46);">多智能体</font>

**<font style="color:rgb(36, 41, 46);">1.主调度智能体和专家智能体职责，它们之间是怎么通信的？</font>**

<font style="color:rgb(36, 41, 46);">agent as tool</font>

<font style="color:rgb(36, 41, 46);"></font>

<font style="color:rgb(36, 41, 46);">多智能体知识库</font>

**<font style="color:rgb(36, 41, 46);">1.怎么设计这个混合检索策略</font>**

<font style="color:rgb(36, 41, 46);">es做全文检索、chroma做向量检索</font>

**<font style="color:rgb(36, 41, 46);">2.数据主要是什么类型的数据</font>**

**<font style="color:rgb(36, 41, 46);">3.这个项目是已经落地了吗</font>**

**<font style="color:rgb(36, 41, 46);"></font>**

<font style="color:rgb(36, 41, 46);">知识图谱</font>

**<font style="color:rgb(36, 41, 46);">1.在项目中做了什么</font>**

**<font style="color:rgb(36, 41, 46);">2.uie模型是怎么微调</font>**

**<font style="color:rgb(36, 41, 46);">3.这个系统应用的效果是怎么样的</font>**

<font style="color:rgb(36, 41, 46);">之前的公司背景</font>

## **<font style="color:rgb(36, 41, 46);">麦麦科技-二面</font>**
### <font style="color:rgb(36, 41, 46);">基本问题</font>
**<font style="color:rgb(36, 41, 46);">1.langchain和langgraph的区别</font>**

**<font style="color:rgb(36, 41, 46);">2.rag准确率不高</font>**

**<font style="color:rgb(36, 41, 46);">3.sql自修正闭环怎么实现</font>**

**<font style="color:rgb(36, 41, 46);">4.响应延迟控制在秒级是怎么实现</font>**

**<font style="color:rgb(36, 41, 46);">5.创建连接池的参数是怎么确定的</font>**

<font style="color:rgb(36, 41, 46);">业务层面、硬件层面</font>

**<font style="color:rgb(36, 41, 46);">6.流式响应输出的实现</font>**

**<font style="color:rgb(36, 41, 46);">7.子智能体遇到故障怎么做隔离</font>**

**<font style="color:rgb(36, 41, 46);">8.rag并发怎么样，高并发怎么去优化</font>**

<font style="color:rgb(36, 41, 46);">前端限流或者分流、后端fastapi以及vllm</font>

**<font style="color:rgb(36, 41, 46);">9.降低vllm成本的方式</font>**

**<font style="color:rgb(36, 41, 46);">10.kafka做什么、还有哪些消息队列</font>**

**<font style="color:rgb(36, 41, 46);">11.coding开发工具、如果不用ai怎么开发</font>**

**<font style="color:rgb(36, 41, 46);">12.除了python以外还有用过其他的编程语言</font>**

### **<font style="color:rgb(36, 41, 46);">综合问题</font>**
**<font style="color:rgb(36, 41, 46);">1.项目背景</font>**

**<font style="color:rgb(36, 41, 46);">2.是怎么做压测的，qps、tps</font>**

<font style="color:rgb(36, 41, 46);">低并发可稳定输出 2000 tokens / 秒，端到端延迟≤400ms，高并发（200）仍能保持 1600 tokens / 秒、延迟≤700ms，完全满足电商实时问答的体验要求；</font>

**<font style="color:rgb(36, 41, 46);">3.最近关注的paper</font>**

**<font style="color:rgb(36, 41, 46);">4.你有什么要问我的吗？</font>**

**<font style="color:rgb(36, 41, 46);">5.为什么要做图谱，避免大量的表的join，因为图谱的关联关系很强。</font>**

**<font style="color:rgb(36, 41, 46);">6.什么是复杂查询</font>**

<font style="color:rgb(36, 41, 46);">业务方+数据分析师+数据团队会整理一个数据集，这个数据集就是定义的复杂sql的数据集，这个数据集三块，第一块问题，第二块sql，第三块结果，这个数据集是周期同步的，每10分钟会更新一下，数据库是实时同步+手动更新的，基于数据平台导出的操作日志，监听这个操作日志，基于它的id实现同步。</font>

<font style="color:rgb(36, 41, 46);">他们的标准是什么呢，一个简单的标准超过3张表的join就是复杂查询，但也没有那么强制，比如那种窗口函数+子查询+条件聚合的那种sql也会定义为复杂sql</font>

**<font style="color:rgb(36, 41, 46);">7.80%满足要求了吗？</font>**

<font style="color:rgb(36, 41, 46);">一开始业务方确实期望能做到 90%，这个目标主要是参考了市面上一些公开报告，很多 NL2SQL 产品宣称能达到 95% 左右的准确率。但是这是他们在一两个场景专门做微调得到的，这类高准确率基本都是在单一、标准化场景下，用大量问题‑SQL 对微调甚至直接注入样本得到的，泛化能力很弱，放到真实、多变的业务场景里根本达不到。</font>

<font style="color:rgb(36, 41, 46);">我们对比过 DataFocus、衡石 ChatBot 这类成熟产品，它们在通用场景下的复杂查询准确率，其实也就在75%~80% 这个区间。而我们的方案是基于公司内部数据平台原生集成，最终复杂查询稳定做到 80% 准确率，简单查询更高。综合对比下来，这个结果已经超过行业平均水平，也完全满足业务方的真实使用需求，最终也得到了业务认可。</font>

**<font style="color:rgb(36, 41, 46);">1.500张表，问题怎么到对应的表上</font>**

**<font style="color:rgb(36, 41, 46);">2.数据平台里面的ai助手</font>**

**<font style="color:rgb(36, 41, 46);">3.nl2sql只训练那么一两个场景，直接把sql训到模型里面，它才能再一些场景达到95。</font>**

**<font style="color:rgb(36, 41, 46);">4.哪些维度，指标 – 地区，商品，用户，订单，支付，物流。</font>**

<font style="color:rgb(36, 41, 46);">指标：uv，pv，gmv，aov，退单率，取消支付率，退货率，同比，环比，渠道引流成本，获客成本。</font>

**<font style="color:rgb(36, 41, 46);">5.数据治理的好，数据团队把很多指标融合在一个大宽表里面，这样在问数场景就很方便。</font>**

**<font style="color:rgb(36, 41, 46);">6.给业务人员，依据数据做决策的。</font>**

**<font style="color:rgb(36, 41, 46);">7.整体响应时间，tps，qps，ttft，tokens，</font>**

<font style="color:rgb(36, 41, 46);">怎么做压测的 – vllm自带的benchmark</font>

<font style="color:rgb(36, 41, 46);">输入1024token 输出512token</font>

<font style="color:rgb(36, 41, 46);">qwen8b- qps6-12，ttft一两百延迟，tokens6000</font>

<font style="color:rgb(36, 41, 46);">qwen14b- qps4-8，ttft两三百延迟，tokens4000</font>

### **<font style="color:rgb(36, 41, 46);">多智能体</font>**
**<font style="color:rgb(36, 41, 46);">1.整体响应时间</font>**

**<font style="color:rgb(36, 41, 46);">2.智能客服，前面有个分类器，检索到这类问题才会路由到这里，然后做处理。</font>**

**<font style="color:rgb(36, 41, 46);">3.有几个工具，有没有mcp的，skills</font>**

### **<font style="color:rgb(36, 41, 46);">图谱</font>**
**<font style="color:rgb(36, 41, 46);">1.多少节点，多少边，有哪些属性</font>**

<font style="color:rgb(36, 41, 46);">十几张核心表，20多万条，80万条边。</font>

**<font style="color:rgb(36, 41, 46);">2.为什么要用graphrag</font>**

<font style="color:rgb(36, 41, 46);">传统关系型数据库适合结构化、固定关联、强事务的场景，但面对多跳关系查询、灵活实体关系、语义关联检索时，SQL复杂、性能差、扩展难。</font>

**<font style="color:rgb(36, 41, 46);">3.上游是怎么调用的你这个图谱的</font>**

<font style="color:rgb(36, 41, 46);">先查节点，再沿边查关系；用实体定位起点，用关系扩展结果，全程只查局部子图，不查全图。</font>

<font style="color:rgb(36, 41, 46);">先在知识图谱中定位分类节点，再通过“属于”这条边关系，检索出所有关联的商品节点，返回商品ID给上游检索系统，最终展示商品列表</font>

### <font style="color:rgb(36, 41, 46);">评论生成</font>
<font style="color:rgb(36, 41, 46);">1.多少数据训练的，测试集7.2.1</font>

<font style="color:rgb(36, 41, 46);">2.batchsize，epoch，lr</font>

<font style="color:rgb(36, 41, 46);">3.怎么评估它的好坏，这个没有那种定量的评价标准，我们一般从2点来看这个模型训练的怎么样，第一点看模型训练的损失，尤其是奖励模型，第二点对生成的结果进行抽样检测。</font>

<font style="color:rgb(36, 41, 46);">问数模型8b+14b</font>

<font style="color:rgb(36, 41, 46);">多智能体32b</font>

<font style="color:rgb(36, 41, 46);"></font>



## 北京忆芯（B2B公司，AISSD）
1.推理怎么做的？

2.所有项目简单介绍、担任角色、人员组成

3.介绍下客服项目

4.用户意图识别怎么做的？

5.保护节点做了什么？怎么应对回退等异常情况？

6.项目开发中，有没有评估过不同模型的表达能力？

7.技术选型的思路

8. RAG的评估指标

9. RAG的耗时如何解决？

答：

切分：离线预解析；

存储：使用高速向量库；索引加速；

召回：降低召回数量；轻量化rerank；

推理：vllm或TensorRT推理加速；混合精度；流式返回；

缓存：高频问题缓存答案和结果；多级记忆；

返回：减少返回上下文，如相关性过滤、只返回摘要。

10.有没有细致测量过RAG每一步的耗时？

11.大模型推理的优化

答：标配是vllm + AWQ + FlashAttention2 + FastAPI + PD分离

（1）模型量化方法AWQ，新一代INT4量化，与GPTQ相比，保留重要权重的精度；

（2）Vllm核心是PagedAttention，将KVCache按页管理，解决内存碎片，提升GPU利用率；

（3）FlashAttention2，高性能算子，把QKV切成小块，只在高速缓存里算，不再来回搬；

（4）动态批处理，不用等整句生成完毕；

（5）3D并行，数据并行是多份模型算一份数据，张量并行是一层计算分多张卡，流水线并

行是一层计算分段执行；

（6）提示词缓存，PD分离；

（7）异步服务，FastAPI+async。

12. Transformer的原理，从用户输入到模型输出，中间经历了什么？

13. Attention公示每个字符代表什么意思？

答：Q相当于对本句的问题，K相当于本句的关键字，V相当于本句的信息。

QKT计算相似度，dk按K的维度缩放，softmax归一化得到注意力权重，×V是用权重提取重要信息。



常见实操问题（摘自连晓强）

1.哪些维度，指标

维度：地区，商品，用户，订单，支付，物流。

指标：uv，pv，gmv，aov，退单率，取消支付率，退货率，同比，环比，渠道引流成本，

获客成本。

2.问数相关

数据治理的好，数据团队把很多指标融合在一个大宽表里面，这样在问数场景就很方便。

给业务人员用，依据数据做决策的。

3.怎么做压测的？

vllm自带的benchmark

4.响应时间怎么算？

整体响应时间，tps，qps，ttft，tokens，

输入1024token输出512token

qwen8b-qps6-12，ttft一两百延迟，tokens6000

qwen14b-qps4-8，ttft两三百延迟，tokens4000

5.图谱多少节点，多少边，有哪些属性？

十几张核心表，20多万条，80万条边。

6.上游是怎么调用的你这个图谱的？

先查节点，再沿边查关系；用实体定位起点，用关系扩展结果，全程只查局部子图，不

查全图。

先在知识图谱中定位分类节点，再通过“属于”这条边关系，检索出所有关联的商品节点，返回商品ID给上游检索系统，最终展示商品列表。

。

7. vllm的原理是什么？

核心原理：PagedAttention（分页注意力）

核心思路：

将KV Cache拆分成固定大小的page（比如16/32个tokens）；

每个请求的KV Cache不再占用连续显存，而是由多个离散的page组成；

用一个page table记录每个请求的KV Cache页存在显存的哪个位置。

8. vllm调整过哪些参数来适配业务场景，比如qps1000+，延迟控制在5s？

tensor_parallel_size

max_num_batched_tokens

gpu_memory_utilization

9. vllm部署遇到的坑？

gpu显存占用满了

10.如何降低vllm成本？

与“推理优化”是同一问题



## 北京观微（遥感测绘）
1.客服项目介绍一下？

2.槽位是怎么应用的？怎么更新的？

3.业务和流程是怎么对应的？

4.知识图谱介绍一下？

5. LangGraph图流程的时间消耗？



## 北京慧博（B2B公司）
1.问数数系统90%准确率，怎么说服客户接受？毕竟已经有了成熟稳定的BI平台，问数系

统的价值在哪？

答：

一开始业务方确实期望能做到90%，这个目标主要是参考了市面上一些公开报告，很多

NL2SQL产品宣称能达到95%左右的准确率。但是这是他们在一两个场景专门做微调得到的，

这类高准确率基本都是在单一、标准化场景下，用大量问题-SQL对微调甚至直接注入样本

得到的，泛化能力很弱，放到真实、多变的业务场景里根本达不到。

我们对比过DataFocus、衡石ChatBot这类成熟产品，它们在通用场景下的复杂查询准

确率，其实也就在75%~80%这个区间。而我们的方案是基于公司内部数据平台原生集成，

最终复杂查询稳定做到80%准确率，简单查询更高。综合对比下来，这个结果已经超过行业

平均水平，也完全满足业务方的真实使用需求，最终也得到了业务认可。

问数的优势是极快的查询效率和极简的操作方法，BI平台虽然准确稳定但是也会存在误

操作和延迟回复的问题，二者优势互补。



## 联想集团（人机交互岗）（线上一面）
1.有PPT可以秀出来

2.在项目中担任什么角色？多少人？用时多久？

3.嵌入模型的选择标准？存储向量与检索向量，用的嵌入模型是否一致

注：问问题时啰嗦一堆，把我绕晕了，回头整理才发现问题其实很简单

4. Agent的Plan是怎么实现的？

5.模型微调

6.遇到的困难？如何解决？

7.人事问题

反问得到信息：联想想做AIPC，既要算法，又要交互，技术团队2



## 北京瓦特曼（机器人）
1.做过纯CV的任务吗？比如图像识别、语义分割、图像理解等。

2.文搜图这个任务，几个人开发？多大数据量？

3.你这些项目是对内对外？交付时间？

4.介绍下问数项目，包括人员和时间

5.直接让大模型生成SQL？不是先生成DSL，再解析成SQL？

6.检索阶段怎么优化RAG？

7.介绍下客服项目，包括人员和时间

8.数据来源？数据量级？

9.项目报价是多少？



## 水木东方（机器人）
1.解释下DPO、PPO、GRPO的区别

2. AB测试怎么做的？怎么衡量模型强化前后的性能提升？你这个提升30%是怎么界定的？

答：

（1）AB实验设计

蓝绿部署：其他环境一致，部署新旧版本两条系统

灰度发放：先用5%小流量放进新版本，观察稳定性，再逐步扩到20%、50%。

实验周期：保证足够样本量，一般观察1~3天，避免时段波动影响。

（2）衡量维度分两类

模型效果指标：人工评分、胜率、意图识别准确率、回答相关性。

业务/性能指标：用户停留时长、解决率、转人工率、QPS、时延。

（3）提升30%怎么界定（非常关键）

我这个30%指的是相对提升，不是绝对提升。

例：基线解决率50%，新版本65%，相对提升=(0.65-0.50)/0.50 = 30%。

3.调了个多大的模型？有没有尝试用更大的模型？

4.上线前如何确定可行？Benchmark离线评估？

答：上线前分4步验证，全部通过才上线。

（1）离线评估Benchmark

标准数据集：MMLU、C-Eval、GSM8K等。

业务自定义评测集：构建领域内问答、意图识别、多轮对话数据集。

（2）人工对齐评估

双盲打分：相关性、有用性、安全性、流畅性。

计算胜率：新版本胜率>55%才继续推进。

（3）性能压测

压测指标：QPS、P50/P95/P99时延、GPU利用率、OOM风险。

满足业务要求才能进入线上实验。

（4）小流量AB验证

先5%流量观察监控：错误率、时延、服务稳定性。

无异常再逐步放量，确认可行后全量。

5. SFT、RM、PPO训练流程简述。

6.因为模型小就训练一轮，防止过拟合，也不追求极限？哈，可以。

7.你做的Agent工作？LangGraph项目？简单介绍下具体实现。

8.影响Agent成功率的是啥？

答：大模型基座能力、Prompt设计、工具能力、环境与反馈、流程架构、数据与评估。

9.最新的技术动向？DeepAgents？

10.什么情况需要多个子智能体？

11.文档分治会有很多问题。

答：（1）问题

上下文割裂：一个完整语义被强行切开，导致单块信息不完整。

关键信息丢失：标题、总结、逻辑关系不在同一块，检索不到。

冗余信息多：块之间重叠少了割裂，重叠多了浪费上下文、引入噪声。

边界敏感：表格、代码、列表被切坏，完全无法理解。

召回不准：小块容易语义模糊，大块又难以精准匹配。

多跳问题无法回答：需要跨多块信息聚合时，单纯分块解决不了。

（2）解决

分层分块策略（Hierarchical Chunking）

小块（512）用于精准检索

大块/章节块用于上下文理解

检索时先召回小块，再向上聚合父块

语义分块代替固定长度分块

用模型做语义分割，按段落、主题边界切分，不按固定字符硬切。

增加元信息（Metadata）

标题、章节、页码、层级结构，帮助重排与过滤。

块重叠与滑动窗口

合理设置重叠（如100~200 token），避免边界信息丢失。

重排（Rerank）优化

用bge-rerank等模型过滤低相关块，降低噪声。

复杂文档特殊处理

表格、代码单独抽取、单独建索引；

结构化数据用SQL，非结构化用RAG混合查询。

引入Agent做跨块多跳问答

规划多个检索步骤，做信息融合，解决单块无法回答的复杂问题

12.一个实际开发问题，给你一个Agent需求你该怎么做？

答：这是个很模糊的问题，所以应该先问清干什么，然后评估硬件资源，确定软件架构。这些做完，才是按Agent架构一点点确定实现细节。



世优科技（数字人）

1.实体识别怎么做的？什么BERT模型？哪一年？

2.Agent怎么做的？

3.大模型是用本地的还是商用API？

4.部署用docker还是k8s？

5.你训过或调过大模型吗？

6.调大模型是为了解决幻觉、不准确、识别速度等问题，有没有其他解决方法？

7.RAG基础知识

8.调过RAG吗？还是直接使用市面上的API？

9.模型训练完后，封装、传递给上下游使用的能力，你具备吗？

10. FastAPI、websocket、flask、socket，了解吗？

11. Transformer经典架构

12.现在的大模型还有Transformer的发挥空间吗？

13.怎么用大模型结合知识图谱做问答的呢？

14.有了ES，为什么还用Neo4j？

15.人事问题



## 致远互联（B2B公司，政务军工）
List、dict、set、tuple的区别

答：list有序可变，dict键值对，set自动去重，tuple不可变。

2.元组能否作为字典的key

答：能。字典的key要求不可变。

3.Python做一些web应用，实现接口的权限校验，用户有权限则正常调用，没有则返回

提示。如何实现？

答：校验函数

你工作怎么从大数据变更到大模型的

项目里用到的RAG优化实现细节与效果？

6.FastAPI怎么加载环境变量？WebSocket怎么实现实时调用？异步隔离？

答：load_dotenv()加载.env文件；

@app.websocket(“/ws”) async def func；

FastAPI底层是Starlette+Asyncio，自带请求级隔离。

7.平时用的什么模型？模型怎么选型？常用模型的优缺点？

8.龙虾用过吗？猜一猜架构，构想一下如何私有化实现？

9.RAG的范式？如何搭建？

10.你做的项目，如何迁移到政务军工的场景？

11.大数据、大模型，对于敏感信息的处理方案？

12.介绍下Flow配置

13.响应阶段，分段生产、全文生成的优缺点



## 中电金信（银行驻场）
1.你在项目里担任什么角色？

2. LangGraph的State有个坑，大概说一下。

答：LangGraph的State是不可变设计，不能像普通字典那样直接append、赋值修改，必须

return一个全新的状态字典来更新，否则状态不会发生任何变化。

解决：实践中分两步，一是让State类继承TypedDict，强制约束State各个属性的键值类型；

二是每个node执行完后，强制返回字典类型。

3. State是怎么初始化的？

答：State用TypedDict定义字段结构，设置init函数，传入类对象，或业务规定的默认值，

给各属性赋值，完成State初始化。

初始化完成后，调用ainvoke(State)执行流程。

在运行过程中，每个节点基于当前State计算，返回新字典覆盖更新，不会直接修改原

State。

4.（NL2SQL经典语义歧义问题）字段取值、字段、表之间往往是一对多的关系，用户输入

一个字段取值如“中信证券”，怎么确定取哪个字段、表？

答：先通过元数据向量检索缩小范围，再通过真实值校验过滤错误，最后靠大模型结合意图

做最终决策，实现从“用户输入值”到“精准表+字段”的匹配。

注：我就是按项目里做的答得，这人揪着不放，认为无法从几十张维表确定到底该用哪个，

而且这人从面试开始就很不耐烦，我也没耐心了直接打个哈哈不说话了，他也听出来了，干

脆互道再见。



## 中创实二面
1.算法题，3道，列表相关，飞行模式可使用编译器和自动提示，不能使用AI工具。

2.上机操作，2道：创建删除文件夹；显卡查看Qwen模型进程并用Docker关闭。

答：nvidia-smi查看Qwen3进程，dockerstop进程号



## 杭州寰马（数字人）
1.怎么从大数据转到大模型的？

2.客服项目里面用到的RAG知识库怎么做的？

3.文档的采集、清洗、处理具体是怎么做的？

4.为什么选择Chroma？

5.为什么不用milvus？chrom、qdrant能承载多少数据？

答：

Milvus是企业级、分布式、重架构的向量数据库。

缺点：运维复杂、开发成本高、轻量级场景没必要。

各数据库上限：

Chroma单机上限千万级向量，分布式不成熟，项目原型。

Qdrant单机上限亿级，分布式成熟，可达数亿级，中型RAG。

Milvus单机上限亿级，分布式成熟，可达百亿级，大型RAG。

选择标准：

单商家、单店铺京东客服→99%情况选Chroma完全够用

超大体量商家、多店、多品牌→Qdrant

真正需要Milvus的京东商家极少（基本只有京东官方、大服务商才用）

附：

日活咨询用户（UV）：

普通中小商家：200~1500咨询用户/天

中大型商家：2000~8000咨询用户/天

头部爆品店：1万~3万/天

每日对话轮次：

平均每用户3~6轮

每日真实query量：1000~5万条/天

京东商家客服知识库一般是（最关键）：

商品FAQ：200~800条

售后、订单、物流、退换货：200~500条

活动规则、优惠券、售后政策：100~300条

总知识库chunk数量：最多5000~2万块

向量数量：1万~3万顶天了



6. LangChain和LangGraph的使用场景有什么不同？

答：LangChain：适合线性、一次性、简单流程的RAG/调用工具。

LangGraph：适合带状态、循环、多智能体、复杂决策的对话/Agent。

7. RAG怎么提高检索准确率？

8. Self-RAG？

答：Self-Retrieval-Augmented Generation，自检索增强生成，LLM主动控制整个RAG过程。

核心4步：

Self-Retrieve，让大模型判读，要不要检索知识库，专业知识/业务问题；

Retrieve，去向量数据库召回chunks；

Self-Refine/Rank，让大模型判断，哪些有用、哪些没用；

Self-Generate，让大模型生成，并自己检查。

9. Agentic RAG与传统RAG的区别？

答：传统RAG：固定流程、无脑检索、简单问答、不会思考。

Agentic RAG：自主决策、查询优化、多步检索、反思校验、复杂问题更强。

我们用的Agentic RAG让主智能体自主判断：

是否需要检索、是否走FAQ、是否走意图、是否走图谱，

并对检索结果做校验、过滤、拒识，

还支持多轮、多跳、多工具协同，

更适合企业级复杂客服场景，更准确、更可控、更合规。

10.生产环境怎么监控评估RAG的性能？

答：生产环境我会从检索、生成、业务三层全链路监控RAG性能。

检索层监控：Recall@TopK、相似度、时延、失败率（超时报错无召回）；

生成层监控：幻觉率（无依据占比）、拒识率（无结果是否拒绝回答）、相关性、耗时；

业务层关注：问题解决率、FAQ/RAG命中占比、转人工率、用户满意度。

通过日志、监控大盘、BadCase平台、A/B测试、自动化抽检等方法持续评估。

附：

FAQ命中，能匹配到预设的标准问题。匹配不到，才会RAG检索知识库。

FAQ能命中50%~70%，RAG能命中10%~20%，系统承接60%~80%，剩下的转人工。

监控大盘，就是格里芬+普罗米修斯。

BadCase平台，必有，自动入库无召回、地相似、差评、重复问题，便于优化系统。

A/B测试，不同embedding、不同模型做对比。



11.你们RAG延迟有多少？我们做数字人追求毫秒级延迟。

答：客服RAG延迟在几百毫米到几秒。因为RAG涉及LLM生成，天生无法满足数字人。

数字人RAG降低延迟的方法：FAQ全部走缓存；

数字人RAG的首字要快，边生成边播送；

检索层优化：小嵌入模型、轻量级向量数据库、关闭重排序、只要Top1等。

推理加速：TensorRT-LLM、vllm等，首包延迟压到100ms以下。

微调怎么避免过拟合？

13. RAG架构有哪些模块？

14. SFT和RLHF的适用场景？

15.有没有Agent的记忆系统？

答：短期滑动窗口记忆、结构化工作记忆、向量长期记忆、用户持久化记忆。

16. Agent运行的安全问题？

答：输入安全，输入校验+注入拦截；

工具安全，工具白名单；

数据安全，数据权限最小化；

行为安全，调用工具之前必须经过校验；

输出安全，答案脱敏+合规审查；

流程安全，限制思考步数，防止死循环；

全链路日志与审计。

17.分布式部署？vllm和TensorRT有什么不同？

答：常用框架：

TensorRT-LLM，英伟达官方，速度最快，高吞吐低延迟，企业级大模型推理首选。

CTranslate2，轻量级、超小体积、速度快，适合边缘计算。

（TGI，哈根菲斯官方，部署简单，适合快速上线、云原生。

LightLLM，国产，比vllm更快、更省显存，适合Qwen、Llama、百川。

ONNX Runtime，通用模，可跨平台，适合小模型。）

选择标准：

高并发、低延迟场景用TensorRT-LLM；

快速迭代、多模型兼容、高吞吐量场景用vLLM；

小模型用CTranslate2。

18.单张显卡，怎么分配，才能多跑几个模型或任务？

答：3D并行，数据、张量、流水线；

Zero3，将优化器状态、梯度、参数进行切片，不需切模型；

模型量化；

给每个任务设置最大显存；

动态加载、分时复用；

小模型如嵌入、重拍，放到小显存或者CPU；适用支持动态批处理、多任务复用的推理引擎。

。

19.资源有限的情况，不能让一个vllm把资源吃完。

20.上家薪资，期望薪资，到岗时间？还有其他问题吗？

中创实（矿业公司）

1.多表多跳的RAG情景。有三张SQL表，AB公用一个字段，BC公用一个字段。怎么从A快

速找到C？至少有3种技术可以实现。

答：图谱；NL2SQL；向量库+元数据过滤；SQL方法，如提前合并成宽表。

2.有一本txt格式的专业教程，有很详细的目录，对这本教程设计RAG，不能用向量数据

库，不能用嵌入模型。

答：基于目录的结构化分块，设置PageIndex给每个目录块分配固定编号，构建全文索引。

可以用ES做。

3.多Agent系统，怎么设置失败回滚机制？大概4、5个方面。

答：5层保障

状态快照：每步执行前保存完整状态；

写前日志：记录所有操作，可追踪可恢复；

补偿事务：对已执行操作做反向撤销；

重试与降级：短暂失败自动重试，严重失败回滚；

原子步骤：保证要么全成功，要么全回滚。

4.多Agent系统，容易彼此调用和质疑，如何监测和打破死循环

大概5种。

答：监测方法4种：

步数计数；状态哈希检测；对话相似度检测；超时监测。

打破方法5种：

强制步数熔断；

主Agent仲裁；

随机选择+降级退出；

给子Agent设置信任权重，低权重不许质疑；

任务中断，转人工。

5. LLM Ops了解吗？公司代码挪到现场部署会有各种问题，就算用Docker，之前也要做一

件事，防止逆向工程，顺带做一个加速处理。还有一个新出来的Agent Ops。

答：

一、LLM Ops，大模型全生命周期管理。4步。

（1）模型工程化，包括量化、导出、加速、加密（防逆向的那件事）；

（2）部署与调度，包括Docker容器化、K8S编排、多Agent调度、资源隔离、蓝绿部署（同时部署新旧版本）、灰度发布（一点点给新版本放流量）、AB测试（新旧版本对比）、离

线私有化部署、内网环境适配；

（3）监控与运维，包括时延、吞吐、QPS（每秒请求数）、P99（最慢的1%有多慢）、显

存/CPU/GPU监控、自动重启、扩缩容、日志、问题追踪；

（4）安全与治理，包括Prompt注入防护、安全审核、权限控制、隐私脱敏、模型防盗、

防篡改、防拷贝。

二、Agent Ops，Agent全生命周期管理，是LLM Ops的下一代。6步。

（1）执行状态监控

（2）死循环监测熔断

（3）失败重试与回滚

（4）行为安全审计

（5）多Agent调度

（6）Bad Case自动迭代

6.多Agent并发调用同一工具或数据库时，如何处理争抢问题？

答：并发队列；全局互斥锁；并发度控制；读写锁分离；连接池。

7.多Agent场景，如何处理共享记忆与私有记忆隔离？子Agent的记忆隔离，用什么实现？

答：独立State；独立CheckPoint，记忆前缀；独立对话历史，独立上下文

8.如何解决记忆遗忘问题？主要是早期重要信息被挤出上下文的问题。

答：关键信息抽取，结构化保存；历史对话摘要压缩；向量化，长期记忆。

9.每天TB级数据，怎么剔除假数据？比如非凸离散数据，怎么得到真实数据？实际都是现

场传感器数据，因为缺少维护，出现了很多假值、非凸，显得很离谱的数。

答：降维；非凸问题转为凸优化问题。

10.上下文膨胀问题和压缩策略？

答：上下文膨胀，是对话越聊越长，导致Prompt越来越大。

压缩策略：

滑动窗口压缩（只保留最近N轮）；

结构化压缩（关键信息抽取）；

摘要压缩（LLM提取摘要）；

递归摘要压缩（超大文本，分块提取摘要，再把摘要再摘要）；

召回式压缩（向量化保存）；

选择性保留（业务规则打分）。

附：Agent设计准则，尽量少调用LLM



## 软通动力 - 外包公司
1. LangChain和LangGraph的区别？

2.理解节点的命令分哪几种？是以什么形式输出的？

答：

（1）命令类型：

- Flow相关: StartFlowCommand, CancelFlowCommand

-回答相关: KnowledgeAnswerCommand,

ChitChatAnswerCommand, CannotHandleCommand

-槽位相关: SetSlotCommand

-会话相关: SessionStartCommand, ClarifyCommand

-系统相关: ErrorCommand, HumanHandoffCommand

（2）以“DSL/领域特定语言/文本格式”输出，让命令解析器，解析DSL，得到Command

对象，传入策略节点。

3.理解节点的提示词是怎么约束的？

答：6部分。

任务说明：分析当前对话和上下文，生成系统命令。

可用命令清单：Flow控制的命令、回答控制的~、槽位收集的命令、会话控制的~

命令生成规

则：启动Flow的规则、设置槽位的~、知识检索的规则、通用规则

决策规则表：输入的条件，与执行命令相对应

槽位更新规则：根据当前对话状态，确定是否更新槽位，更新规则细节和示例

例

4.理解节点提示词需要哪些变量？

答：可用Flow、当前状态、历史对话

5.怎么处理对话中断？

答：3种情况。核心组件“对话栈”是一个类对象，维护了一个栈帧列表。

（1）用户插入新消息。把未完成对话保存到对话历史，保留对话栈不清空，压栈新命令。

（2）用户取消Flow。解析得到取消命令，对话栈弹栈当前命令。

（3）无法理解用户意图，系统降级处理，对话栈压栈闲聊命令。

6.怎么处理对话嵌套？

答：连续压栈。

7.（嵌套问题变体）用户一次输入多个不相干任务，是否要创建新的对话栈？

答：可以创建新的，但本项目没有。一次图流程，创建一个State，读取持久化的Tracker信

息，将解析出来的多个命令逐个压栈，逐个处理。添加栈深变量，监控栈深不要过长。

8.怎么处理对话回退

答：用户发送/back命令或LLM生成back命令，对话栈弹栈。

9.怎么决策是压栈还是弹栈？

答：大模型解析用户输入，如果是新消息，就压栈；如果是取消命令，就弹栈；如果无法理

解，就降级。

10.怎么判断会话是连续的还是重启的？

答：主要看TrackerStore中是否存在该sender_id的DialogueStateTracker实例。

（1）连续会话：如果store中已有该sender_id的tracker，说明是连续对话，会加载之前的

状态（包括对话历史、对话栈、槽位值等）。

（2）重启会话：有两种情况

隐式重启：sender_id第一次出现，store中没有对应的tracker，会创建新的空白tracker

显式重启：用户发送/restart命令或LLM生成restart命令，调用tracker.restart()，清空所有

状态

（3）持久化支持：系统支持多种TrackerStore实现（内存、数据库等），生产环境可以实

现跨进程/跨服务器的会话状态共享。

11.怎么判断有没有关联的上下文信息？

答：Tracker保存着。

12.介绍下DPO、PPO

13.交叉熵损失和KL散度有什么区别？

答：（1）交叉熵衡量两组样本之间的距离，主要用于损失函数。

（2）KL散度/相对熵衡量两个概率分布的差异，主要作为正则化项。

14.具体实现用了哪些框架？Accelarate底层用的什么？

答：（1）Transformer加载模型、Accelarate分布式训练、DeepSpeed训练加速、vLLM推理

部署、LoRA微调、QLoRA微调；

（2）Accelerate是Hugging Face推 出 的 分 布 式 训 练 封 装 库 ， 底 层 依 赖PyTorch的

torch.distributed，默认使用DDP+NCCL实现多卡加速，同时支持DeepSpeed作为扩展后端，

让一套代码无缝运行在不同硬件环境上。

15.怎么实现NL2SQL的？

16.什么时候用元数据表？

17.怎么校验？

18. RAG优化？

19.是否使用代码专用模型？

20. Chroma的检索原理？

21. FastAPI vs Flask？

答：Flask，老牌轻量Web框架，简单灵活，但性能一般、异步弱。

FastAPI，现代高性能Web框架，天生异步、自动文档、速度接近Go，是大模型部署首选。

22.关于CPT的工作？

23. Neo4j的实体抽取怎么做的？

24.项目里的异步编程？实现并发？



## 中恒博瑞（电器公司）
1.自我介绍

2.前司介绍

3.视觉模型有哪些了解？

答：

分类：ResNet、MobileNet、EfficientNet、ConvNeXt

检测：YOLOv5/v8、Faster R-CNN、RT-DETR

分割：U-Net、Mask R-CNN、MobileSAM、Segment Anything

多模态：Qwen-VL、LLaVA、InternVL、LayoutLM、Donut

OCR：DBNet+CRNN、PP-OCR、MMOCR

应用：布局分析、表格识别、图纸结构提取、文本检测

4. PDF文档如何处理？表格如何提取？图像如何提取？

答：

PDF解析：PyMuPDF、pdfplumber、PDFMiner、unstructured

表格提取：

规则式：pdfplumber、Camelot

模型式：LayoutLM + TableTransformer、TableMaster

多模态：Donut、Qwen-VL

图像提取：PyMuPDF直接提取Pixmap，保存为高清图，再做OCR/布局分析

5.对视觉模型有没有微调经验？

答：

YOLO微调：检测电气元件、图标、标注区域

轻量分割微调：U-Net/MobileSAM做管线、拓扑分割

多模态微调：LLaVA/Qwen-VL做领域指令微调

工具：TorchVision、Transformers、PEFT（LoRA）

6.处理过的最大分辨率的图像？PDF里的图像分辨率很大，包含很多复杂管线，还有水印

数字文字信息，用什么办法去理解这种大图的语义信息？前提资源不能无限扩张。

答：核心：分层分治，不喂整张图

矢量优先：PDF提取文字、线段，减少像素处理

水印去除：FFT频域滤波+形态学，轻量UNet

分级图像：全局小图看结构，局部高清块读文字

轻量模型：YOLO检测元件，PP-OCR读标注

拓扑结构化：输出三元组（设备-连接-设备）

多模态只做最后融合，不处理大图

资源可控、精度高。

7.如果切块再向量化，会不会丢失语义信息？如何从向量化完整恢复成图片？

答：会丢，切块破坏全局拓扑，所以必须分层chunk+父块回溯+重排来弥补。

向量是压缩特征，无法完整恢复原图，只能存原图+元数据+向量索引。

8.微调模型的数据集怎么创建？

答：

采集：业务图纸、PDF、标注数据

清洗：去重、去模糊、滤除噪声

标注：检测用LabelStudio；分割用SAM辅助；多模态用对话格式

增强：旋转、缩放、对比度、噪声

格式：COCO、JSONL、ShareGPT

9.对于电气行业的这种大分辨率图像，怎么微调一个视觉模型？

答：

基座选轻量：YOLOv8-tiny、MobileSAM、Qwen-VL-Tiny

用LoRA低成本微调，冻结主干

数据做分级采样：大图切块+全局图一起训

任务：元件检测、拓扑分割、图标OCR、多模态问答

评估：mAP、召回率、准确率、人工评测

10. RAG会用哪些模型？

答：

嵌入：bge-small/base、text2vec、m3e

重排：bge-rerank

生成：Qwen、Llama、InternLM

多模态：Qwen-VL、InternVL

11.常用的嵌入模型？有什么区别？

答：

BGE：综合强，中文好，M3版最新最强

GTE：阿里通义，中文比BGE还强

Nomic-embed：长本文专用，8k上下文无压力

区别：维度、上下文长度、MTEB分数、速度、领域适配性。

12.文档向量化时，怎么设置chunk？

答：

固定chunk+重叠：通用文本

语义chunk：按段落/主题切

分层chunk：父块+子块，适合大图/长文档

图纸：按元件/区域做语义块

13.怎么提高RAG的召回率？

14.国产显卡的推理加速有没有做过？不让用N卡。

答：适配昇腾、沐曦、摩尔线程等国产显卡的方法：

框架：MindSpore、Transformers++、定制runtime

加速：图编译、算子融合、INT4/INT8

引擎：定制TRT类似加速栈、vLLM移植版

部署：FastAPI+国产runtime，保证QPS与时延

15.每个项目的周期？最近的项目的人员配置、项目周期？

16.怎么处理大模型的幻觉？

答：

RAG增强检索，提供证据

指令约束：“只根据文档回答，不知道就说不知道”

验证器模型二次校验

高质量SFT+DPO

引用溯源，展示来源片段

17.有没有方案寻优？

答：有，从多维度做方案对比：

模型大小、量化等级；

chunk策略、检索方式；

多模态/纯文本；

国产卡/N卡部署成本；

时延、QPS、准确率、成本；

最终输出最优技术方案。

18.人事问题

19.大数据工作



## 北京朗杰（培训公司）
1.自我介绍

2.介绍一下客服系统

3.项目背景、人员、岗位职责

4.优化提示词调模型属于比较简单的，什么情况下不太好处理？或者说，用户先问订单再

临时插问物流，该怎么处理？

5.怎么保存查询结果、上下文？

6.历史对话越来越长，会不会撑爆内存？

答：会。解决方法很多，

设置保留最大轮次如10轮；

用LLM将历史对话压缩成一段摘要，只保留用户信息、核心问题、关键槽位；

提取关键信息，做成JSON给子Agent；

历史对话直接存数据库，用RAG技术检索上下文。

7.介绍一下Tracker。

答：（1）Tracker是类对象，封装了对话业务状态。包含的内容有：

SessionID、槽位字典、最大轮次等基础信息；

对话历史列表、当前对话；

对话栈类对象，核心是栈帧列表。

（2）通过TrackerStore基类及其子类，Tracker可以持久化到不同的存储介质，如内存/数据

库/文件系统，支持跨会话调用业务信息。

（3）Tracker类对象，是State字典的一个元素。

8.介绍一下State。

答：（1）State是LangGraph的传递状态。包含的内容有：

追踪器Tracker、Flow列表、领域（包括槽位和固定响应）、

输入输出数据、中间结果缓存、

最大动作次数限制、当前动作次数、节点执行信息等等。

（2）State仅在一次图流程中有效，是临时变量，不需要序列化。

（3）State是字典对象，其中一个元素是Tracker

9.怎么处理对话嵌套？

10.主Agent和子Agent怎么划分边界？除了提示词，还有其他方法吗？

答：

1.结构化调度，主Agent只输出结构化指令，子Agent只接收固定格式。边界

由代码锁死，不可能越权；

2.独立入口，每个子Agent是一个独立的微服务，不共享内存、不共享上下文；

3.工具白名单，每个子Agent单独绑定工具；

4.设置数据权限，每个子Agent只能访问特定数据库；

5.上下文隔离，分发任务时只给子Agent必要的最小的上下文；

6.独立微调，强化每个子Agent的垂域边界。

11.（如果答的好会追问）为什么要严格划分边界答：

企业服务必须可控；

如果涉及敏感信息，Agent权限必须最小化；

防止单Agent出错影响全局；

便于迭代、排查问题；

满足法务合规要求。

12.子Agent有并发/并行场景吗？怎么处理的？

答：

并发场景：

多用户同时请求系统；

用户一次输入多个问题，解析后调用不同Agent同时处理；

用户输入一个复杂问题，拆解成并行子任务，多跳或多知识源的。

并发的问题：

资源争抢、上下文混乱、结果返回顺序错乱、调用超出时间限制、死锁

并发控制：

子Agent异步并发+主Agent统一等待；

给子Agent设置并发上限，如订单Agent最多同时跑10个，超时则排队；

SessionID隔离会话，保证会话的上下文、返回结果不乱套；

子Agent之间不许通信，只跟主Agent通信；

并发超时，直接降级回答。

13.标题注入防止语义丢失，具体怎么操作的

14.标题注入是否会带来噪声？

答：会，但是噪声可控。

首先，标题长度远低于chunk长度，还能设置正文权重大于标题权重；

还可以，只注入必要层级，尽量保留名词性内容，去除修饰词和长难句；

如果过长，还能提取摘要。

15.还有哪些方法减少语义丢失？

答：

语义边界切分，最新的切分方式，SemanticChunker，对句子向量化，计算相邻句子的

相似度，相似度低的句子之间就切开。

递归字符切分，最常用，切分时允许重叠10%；

结构层次切分，按文档的H1H2H3切分，并注入层级路径；

每个chunk生成极短摘要，放在chunk最前面。

16. NL2SQL为什么要构建元数据知识库？

17. SQL可执行率是怎么提升的？

18. NL2SQL安全边界怎么考虑？

答：7层设计

只给select权限；

只允许生成轻量级SQL，禁止嵌套过深、Join过多、union过多等；

给每个生成的SQL强制添加UserID，只允许用户查自己的；

只给白名单库表；

SQL校验，不止检查正确性，更要检查合规性，禁止危险操作、SQL注入、敏感字段，

必须添加limit和where，禁止全盘扫描；

禁止自然语言直接生成SQL，要先提取关键字，构建Prompt或填充预定义SQL模板；

监控SQL日志。

19.知识图谱+向量检索+全文检索，什么情况需要这么复杂的混合查询？

答：

三者综合使用场景：

用户的问法极度不一致，有关键词查询、有口语化查询；

含有大量多跳、关联的问题；

既有结构化数据，又有非结构化文档；

要求召回率较高，跟钱有关的；

同时存在复杂逻辑、自由问答。

三者使用场景不同可以互相补充：

知识图谱，擅长多跳、逻辑推理、关联查询；

向量检索，擅长口语化、相似度查询；

全文检索，擅长关键词匹配、精确匹配。

20.图谱的使用场景？

21.查询路径比较长的情况，也适用图谱吗？如用户问题从系统到服务、从文档到变更。

答：非常适合！查询路径越长、关联越深，越适合图谱。

图谱三大要素：实体+关系+属性。

变更记录、版本、历史、操作轨迹，完全可以保存在图谱。

22. FastAPI接口换成Jsink/DataFrame，会不会更快？

答：FastAPI底层是异步非阻塞的，本身非常快；Jsink/DF是批处理架构，适合离线、流处理。

23. Python深浅拷贝

答：list[:]是浅拷贝，与.copy()、list(原列表)效果一样，浅拷贝的数据会共享，深的不会。深

拷贝需要deepcopy(）
