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

答：list[:]是浅拷贝，与.copy()、list(原列表)效果一样，浅拷贝的数据会共享，深的不会。深

拷贝需要deepcopy(）

## 字节跳动
6. 🔥🔥 1.简历拷打
7. 🔥🔥 对多模态的个人认识，未来的趋势
8. 🔥🔥 能介绍一下Flash Attention吗？它是怎么做到既省显存又提速的？
10. 🔥🔥 多分类损失函数 ——交叉熵；交叉熵里每一项的意义是什么？
11. 🔥🔥 你手上有哪些offer或者流程嘛现在
12. 🔥🔥 Multi-Head Attention 的作用是什么?
13. 🔥🔥 Attention如何计算?为什么除以根号下Dk?mask attention是如何实现的?
14. 🔥🔥 Transformer Decoder 的结构有哪些部分？
15. 🔥🔥 LoRA微调的原理是什么？秩 r 的选择会对模型表现产生什么影响？
16. 🔥🔥 设计模式
17. 🔥🔥 rag怎么做的（项目无关）
19. 🔥🔥 后续还有多少轮面试？
22. 🔥🔥 知道哪些损失函数
24. 🔥 Transformer 基础八股全问答
25. 🔥 从数学角度分析L1、L2正则化区别
26. 🔥 介绍一下layernorm和batchnorm的区别？
30. 🔥 详细介绍下deepspeed(三个stage结合参数回答)
31. 🔥 平常使用AI吗，都用来干嘛？如果我想使用AI，比如coding领域，你有何建议给我？
32. 🔥 你有什么想问我的？
33. 🔥 你这个 prompt 是怎么调的？
34. 🔥 聊一聊大模型的发展道路？
36. 🔥 提高模型的准确率核心是什么
37. 🔥 强化学习
38. 🔥 拷打论文、项目
39. 🔥 SFT和强化学习各自有什么优缺点，分别适用于什么场景？
40. 🔥 如何估算 LLaMA-7B 模型推理时的显存占用？
41. 🔥 介绍RAG项目
42. 🔥 DPO的原理，损失函数如何计算？
43. 🔥 分别讲一下 Dense 模型和 MoE 模型以及二者的区别
44. 🔥 3. 知道 LoRA 的原理吗， A 和 B 两个矩阵怎么初始化，有了解过其他的初始化方法吗
45. 🔥 业务详细介绍？
46. 🔥 为什么现在的LLM都是Decoder only的架构？
47. 🔥 Q5：Bert和GPT区别
48. 🔥 阐述GQA、MQA、MLA的原理分别是什么。
49. 🔥 Attention计算公式
51. 🔥 bn和ln
52. 🔥 讲一下Adam优化器的原理以及优化过程
53. 🔥 讲一下GRPO
54. 🔥 推荐怎么和大模型进行结合？
56. 🔥 谈一下最近看的论文？
57. 🔥 介绍一下function calling和MCP
58. 🔥 lora训练，怎么做的，参数，rag的流程细节。
62. 🔥 kl散度表示的是什么。
63. 🔥 4.是否了解过强化学习，讲一讲on-policy和off-policy不同和优缺点
64. 🔥 评估指标
65. 🔥 简历深挖
66. 🔥 对岗位的理解
67. 🔥 KV Cache是什么？为什么能极大地提升推理速度？
68. 🔥 你怎么处理响应速度与推理精度之间的tradeoff？是先召回再精排，还是单次生成？
69. 🔥 介绍一下RLHF流程，包括哪几步
70. 🔥 LORA和全参数微调的区别
71. 🔥 介绍一下 RAG
74. 🔥 一般你怎么去评估你的这个模型？
75. 🔥 跟各大不同部门HR语音聊3-4h以上得到的一些offer部门投递选择的有用建议：
76. 🔥 6. 能提前来实习吗
77. 🔥 你是怎么设计agent的记忆系统?
78. 🔥 PPO原理
79. 🔥 attention的计算时间复杂度
80. 🔥 微调方法了解多少？
86. 🔥 跨模态对齐的方案有哪些？为什么选择该方案
87. 业务场景题
88. 3.选择确实大于努力，有些人进去后内部转岗也需要具备良好的识别能力和眼光，有些人内部转岗才发现是从一个坑转到了另一个坑，现在不好的部门或许因为时代机遇顿时变香饽饽，现在不行不代表未来2-3年不行，因素很多，听到hr一些调侃“部门行不行看领导行不行，领导行不行看大领导行不行”，我问啥样的领导行呢？hr：能带领部门业务取得利润且赚钱的领导。重点因素：领导，大领导...
89. 有没有转正
90. 是否做过意图识别？如果要做意图识别，可以怎么实现？
91. BERT和Transformer区别
92. 介绍下self-attention，计算其时间复杂度。
93. 介绍一下 QKV 的计算？
94. bert详解，有什么缺点，bert有哪些改进模型；
95. Agent怎么评估效果？
96. 项目:如何在有限算力下做大模型微调?常用方法有哪些?
97. 介绍一下self-attention及其适用场景
103. 冷启动问题的解决方案
104. PLE和MMoE有什么区别？
105. 为什么Transformer使用Layer Normalization而不是Batch Normalization？
106. 为什么要做这个项目
107. 详细介绍快手的实习经历
108. 自己的应用模型的经历，改进经历等
109. 简单复盘总结：项目写的技术创新和深度还可以挖一挖，
110. HR都在利用信息差忽悠应届生进来，一般是语音打电话忽悠，这样方便不留下证据，可能的坑包括不限于：很坑的部门类似活多待遇低，来了跟当时说的做的东西不一样，来背部门的低绩效指标一年后out出去，其他还没有想到的...
111. 1.不能听HR的一面之词，多调研，多找人打听真实情况，最好是内部部门工作的人
112. 如何应对面试中记不住的问题
113. 你认为自己在面试中表现如何？
114. SFT中的loss是怎么做计算的？
115. GRPO的原理，损失函数如何计算？
116. 还是Transformer，自注意力。问了一个cross attention，我当时都没听说过这啥，面完赶紧补习了一下，后来百度二面也问了。
117. 生成模型了解哪些，GLM结构介绍一下
118. Lora的损失函数，优势和缺点
119. BERT的结构，比过去的文本编码器好在哪些地方？（这个确实需要好好总结一下）
120. 对rankmixer了解吗?介绍一下?
121. 长序列建模除了sim还了解哪些？
122. 主流的开源大模型结构有哪些？
123. 有没有用到类似AutoGen或LangChain的框架？为什么选这个框架？
125. 游戏ai，2道编程题，问了下岗位意愿程度
126. 要求转go语言
131. 特征重要性评估方法
132. 泊松分布和γ分布的区别（？woc开始考数学了）
133. kl散度和交叉熵的关系
134. boosting和bagging在特征方面的区别，(没做过，...
135. 为什么要在推荐系统中引入rqvae?
136. 你了解哪些生成式推荐的论文
137. 有哪些序列建模的方法和模型
138. 知道 deepspeed 和 megatron 吗，分别介绍一下
139. 真的很看运气，这次感觉把项目讲的比较详细，然后没问什么其他的，然后2道编程题，原来好的一面是1,2天后就二面....
140. 你为什么选择我们公司？
141. 这两段实习哪段体验更好
142. 具体做了什么？
143. 为什么选择前端开发
144. 如何让多个agent协同工作的？举个具体的协同机制例子。
145. 如果一个agent误判导致策略冲突，如何处理？
146. 长期记忆如何存储?如果历史记录量非常大,怎么优化查询效率?
147. 大模型灾难性遗忘是什么？怎么解决的？
148. 如果量化后理解能力下降怎么办？怎么做精度补偿？
150. 2.如何增强模型的多轮对话能力？
151. SFT和DPO的区别
157. 机器学习八股
158. 3、DIN和Transformer 的注意力机制区别
159. 为什么Transformer选用LayerNorm而不是BatchNorm？
160. 用了多少卡
161. 你为什么离开上一家公司
162. 论文模型创新细节，细到每一步运算操作，矩阵计算，我直接把向量维度说上了，实验怎么做的，评估指标
163. bert的预训练任务是什么?
164. 多模态模型怎么训练？
165. 多头和单头的情况下有什么区别
166. 如果你这个项目资源足够的话，有没有考虑过直接端到端训练？
167. 什么是agent
168. 对 RLHF 了解的多吗
169. 还有哪些交叉模型？
170. 开发一个Agent时最大的难点是什么？
171. 讲一下prompt书写的经验,如何判断prompt是否达标,如何改进prompt
173. 7.红黑树特点
177. 场景迁移学习的思路有哪些？
178. L1和L2的区别
179. 4.逻辑回归
180. 跨域问题的解决方法有哪些
181. 对llm4rec的后续迭代方向有什么见解？
182. 讲一下最近很火的onerec？你认为onerec对你工作最大的启发是啥？
183. 手推一下MSE的梯度回传？为啥01分类问题不能用MSE？
184. FP16/BF16 区别
185. 你们是怎么评估这个效果的？
186. 训练流程？
187. 一个酷似《狂飙》里蒋天的人给我讲了一堆入职之后的事就没了
188. 同学我看你都六面了啊而且面评也不错的，怎么回事啊？
189. 介绍字节实习
190. 为什么要做产品经理?
191. 你为什么选择这个岗位？
192. Self-Attention vs Cross-Attention 的区别?
193. 在 RAG+知识图谱的 Agent 系统中，知识图谱更新的机制是怎样的？是怎样保证实时性的？
194. 训练 LoRA 模型时，你是如何选择冻结层的？依据是什么？
195. 如果要做电商agent，你会选择哪些模态的信息作为输入？比如文本评论、图像、视频、购买记录？
196. LLM的评估
197. 什么是长度外推？
198. ControlNet是如何控制生成图像的？零卷积的作用？
199. 详细介绍一下Moe?优缺点各自是啥?
200. 用bert做分类任务时，输出是怎么处理的？
201. 介绍一下MHA
202. PPO的clip机制？在线强化学习和离线强化学习有什么区别？RLHF是哪一种？
203. 为什么要用reference model? 为了解决什么问题？
204. 标准RAG有什么问题？
205. 推荐系统或者NLP领域 有什么方法可以加速attention计算
206. 有没有关注目前前沿的RLHF方法？
207. 6.FlashAttention v1 和 v2 的主要改进点分别是什么？
208. Bert结构
209. 八股:Transformer encoder?为什么需要FFN?
210. 如何处理reward hacking?
214. softmax公式
215. 为什么分类用CE不用 MSE？
216. 二分类的话如果负样本过多对AUC有什么影响
217. sigmoid的平均值会怎么变
218. 二分类问题的损失函数。
219. 为什么是BCE？
220. 为什么选用DIN模型，介绍下DIN
222. 训练模型如果loss不稳定，如何解决?
223. Dropout 训练和测试的差异
224. Normalization有哪些，有什么作用
225. 什么时候用batch norm什么时候用layer norm，为什么
226. 训练和推理的时候的BN均值和方差都是怎么得到的
227. 神经网络权重初始化为全零会带来什么影响？
228. 如果要在 GPU 资源有限的条件下同时提供推理和微调服务，如何做资源分配和任务调度以保证时延和吞吐？
229. ViT的结构和原理
230. 大规模 Agent 系统在多线程/多进程场景下的资源调度策略如何设计？
231. 针对实习项目，问数据层次怎么分层
232. 针对具体实习项目，说明业务逻辑
233. 复盘之后有什么收获
234. 暑期实习有什么感受，转正了吗
235. 你在腾讯实习这个项目的收益点主要来自哪里？后续怎么继续迭代？
236. 美团项目拷打
237. 你如何评价自己的学习能力？
238. 你上一段实习现在是结束了吗？
239. 问了一下快手的工作
240. 为什么腾讯甲方要面试你
241. 如果在QQ想做什么？
242. 我问啥样的领导行呢？
243. 讲讲模型训练方面的经历？
244. 请介绍你参与过的最出色的项目并详细说明
245. 手写自注意力然后问我Q,K,V的线性变换矩阵能不能共享权重
246. 为什么÷sqrt(dk)
247. 梅尔频谱怎么来的，MFCC怎么来的，他们什么关系
248. 怎么评价生成式模型生成的音乐（我项目里有一个用diffusion生成音乐的）的好坏
249. lora原理，bert结构，截断长度token个数如何提升，rag大规模数据怎么处理，自然语言处理方面的了解程度，nlp大数据挖掘方面怎么理解，现在的大模型如何应用到搜索检索层面？
250. transformer八股，讲讲模型训练方面的经历
251. 我只说了过去word2vec窗口太小什么，还有很多其实：具体见图
252. 如果qk变成同一个矩阵会有影响吗?如果一定要变成同一个矩阵，如何解决影响?
253. 介绍下LLAMA的架构
254. 8.beamsearch 怎么做的
255. 有没有做过模型压缩？比如在车载端或低端设备上的推理加速？
256. 2．实习微调过Qwen2，你说说Qwen2的模型结构吧，Qwen2相比Qwen1做了哪些改进
257. 5．为什么有了 SFT 之后还需要 RLHF
258. 我的RM怎么训练的？
259. 加那个reward头需要什么库？
260. 怎么挖掘这些视频的标签？
261. 知不知道序列中每一个token的embedding在经过很多层self attention之后会变得相似的问题以及对应的原因？
262. 实习部分继续预训练的数据大小？
263. LLM推理的时候，如何从prompt到response？
264. 对 Agent 框架有了解吗？
265. 用过哪些大模型微调方式，LoRA微调原理
266. 有没有用rl进行策略更新？
267. 截断长度token个数如何提升？
268. rag大规模数据怎么处理？
269. 自然语言处理方面的了解程度如何？
270. nlp大数据挖掘方面怎么理解？
271. 现在的大模型如何应用到搜索检索层面？
272. decoder预测时i位置预测出来了，然后预测i+1位置，那么是用i位置的token结果还是概率结果？
273. 其他PEFT方法
274. 开放题：你在大模型训练中遇到过的困难，如何解决？
275. DPO数据如何构建
276. 大模型如何根据场景调用不同的工具类
277. 多个agent如何协作工作？
298. 手撕： transformers encoder
299. 10. static 关键字作用？
302. Java中常用的集合及其用途是什么？
303. 交叉熵loss反向链式求导过程
304. β分布和γ分布的关系
305. AUC，机器学习里样本不均衡怎么解决，二分类的话如果负样本过多对AUC有什么影响，sigmoid的平均值会怎么变
306. 抛10次硬币，4次正面，6次反面，求抛出正面的概率p的极大似然估计。
307. 二分类问题的损失函数。 为什么是BCE？表达式是什么，为什么是这个形式？
308. AUROC指标介绍一下：
309. 传统机器学习模型了解哪些，树模型，xgboost了解吗？
310. 在机器学习里，怎么处理长尾数据和多峰数据？
313. 4.如果是做生成式召回应该对模型结构怎么修改
314. 介绍多路召回策略。
315. 推荐系统#
316. 怎么去给QQ短视频里面的视频做推荐？
317. 介绍一下MMOE
318. 是先召回再精排，还是单次生成？
319. 做了哪些显存优化？
320. 训练参数？
321. 多模态学习中常见的融合方式有哪些？早期融合 vs 晚期融合 vs 中间融合的区别和适用场景？
322. 常用的不同模态数据在embedding层面对齐的方法有哪些？
323. 梅尔频谱怎么来的
324. 对测开岗位的理解
326. 3、美团实习
327. 大概问的都差不多，主要是简历的东西，剩下一点时间会问一些八股。
328. 你对这个岗位有什么期待或者说是想做的事情吗？
329. 项目中遇到的最大挑战是什么?你是如何解决模态异构性问题的?
330. 介绍agent相关项目经验
331. 对这个业务感兴趣吗？
332. 反问组里的资源和具体业务情况
333. 如何平衡学业与实习时间
334. 如果重新负责一个项目，你会有哪些优化方向？
335. 面试是否主要考察项目经验
336. 面试有哪些可以改进的地方
337. 介绍你负责的模块
338. 询问项目基本情况
339. 是否阅读过技术报告
340. Vision Transformer (ViT) 和 CNN 在图像特征提取上的优劣对比？
341. 微调时的训练数据是怎么构建的？如何保证样本多样性和质量？
342. 如何降低 Transformer 的计算复杂度？常见的稀疏注意力变体有哪些？
343. 视频大模型的长时序建模方案
344. PPO 的核心目标函数是什么？
345. 相比 PPO，GRPO 的“Group”体现在哪一步？
346. KL 散度在 RLHF 阶段出现的位置、作用以及过大/过小分别会导致什么现象？
347. Multi-Agent 场景里，Reflection 模块与 Memory 模块的输入输出各自是什么？
348. transformer计算的时间复杂度和空间复杂度，deepseek对transformer主要做了哪些改进?
349. 如何解决坍缩问题?
350. Decoder 文本生成有哪几种方法
351. 深挖多模态大模型论文用的video - llama ，讲一下大模型的结构
352. 介绍一下 ALBEF 、 BLIP
353. 用bert做下游任务时，输入有哪些embedding？
354. RAG检索召回的片段中，有一些质量差的，如果排除掉？
355. 注意力计算的计算复杂度是多少？
356. RAG的完整流程，构建向量检索库时如何处理时间衰减对召回的影响？
357. 9.大模型了解多少，强化学习了解什么
358. 10.手撕 transformer 并计算 flops 和内存开销
359. lora原理细节，为什么可以加速？什么是秩？
360. LoRA 训练和全参训练的优劣
361. 如果DPO训练的过程中发现loss不降，如何定位原因？从数据构造和训练参数两个角度分析。
362. 有没有尝试过动态prompt，训练数据如何构造，如何保证policy正确？
363. 如果想把判别式任务转化成生成式任务，学术界有哪些常用方法，哪一种效果比较好有对比过吗？
364. 如何确保分层的准确性，用大模型进行分层为什么没有尝试更大的模型？
365. CPT的数据配比是什么样的，有没有考虑CPT后通用能力的退化问题？如何检验CPT后模型的通用能力？
366. decoder部分训练和推理有什么区别？
367. 3．了解 RAG 吗， GraphRAG 的做法
368. vllm推理过程中哪些参数可以调优，结合经验来说。
369. 总结一下八股：强化学习（目前每个面试官都会问），L1 L2正则化，LoRA原理，其他PEFT方法，SFT和DPO的区别，SFT和DPO训练心得，Transformer结构，位置编码，长度外推，优化器，flash attention，分类为什么用cse而不是mse，BERT系列训练流程与各种变体，AUC指标，最近读过的论文。
370. 做注意力计算的时候softmax之前为什么要除根号d_k?
371. 微调是如何进行微调的？为什么LoRA能够work？除了LoRA外，还了解哪些微调方法？
372. 在微调 Qwen 的时候，数据是怎么构造的，有用到什么数据清洗方法吗，数据配比是怎么做的
373. 长期记忆如何存储？
374. Prompt engineering的方法？
375. SFT和DPO训练心得
376. BERT系列训练流程与各种变体
377. **reward bench** 上的reward model分哪几类？reward model如何训练的，训练目标是什么？
378. 大模型训练：数据清洗、处理、配比的方法
379. 你做Prompt优化时，是如何判断优化后的Prompt在Agent推理链路中性能提升的?
380. 你是如何利用多Agent协同来提高推理正确率的?
381. 绝对位置编码和相对位置编码的区别是什么？
382. Agent的组成部分及实现方法
383. 对比RLHF、PPO和DPO算法的技术差异、优缺点及适用场景
384. 候选人是否阅读过大模型相关的论文，特别是数据相关的论文
385. LORA的原理及低秩矩阵在参数高效微调中的作用
386. Transformer与Llama在LayerNorm实现上的区别
387. 为什么大模型有few-shot能力?
388. 介绍一下MoE和极化问题的解决方法
390. 引导：那你描述一下Epoll编程我怎么去监听一个事件？wait你要监听哪些东西，有哪些东西我其实可以不监听？（这个没答出来，对epoll的理解还是太浅了）
391. 你有一栋 100层的大楼和 2个完全相同的鸡蛋。找出临界楼层N——在这个楼层或以上扔鸡蛋，鸡蛋会碎；在这个楼层以下扔，鸡蛋不会碎。
394. 给定两个单词一个转换成另一个，只用删除，插入和替换，返回最小操作数，以及打印每一步操作
400. React项目中使用过哪些Hooks及其原理
403. 两道力扣题目
404. 常用的对比学习有哪些方法？怎么构造数据的？
405. 如果训练出来的模型在某一类任务上表现比较差，如何解决这个问题？
406. 数据的难度分层是如何做的，为什么没使用困惑度？
407. 手撕对比学习的loss计算
409. 什么是对比学习(Contrastive Learning)？InfoNCE loss 的公式和作用？
411. sparse特征和dense特征的区别
412. 正则化的基本原理和作用
413. 为什么逻辑回归中使用交叉熵损失函数而不是均方误差损失？
414. RQ-KMeans和RQ-VAE的区别是什么？
415. Uplift模型的结构和输入输出是什么
416. 知识蒸馏的方法有哪些？
418. 排序模型关注的指标是什么？
419. 双塔可以用于哪些环节？你觉得目前对双塔模型的研究还存在哪些问题？怎么优化？
420. 设计一个电商的商品召粗精链路？
421. 怎么解决模型的冷启动问题，你觉得LLM在冷启动方面能够起到什么作用？
422. 3.为什么会想在重排做生成式
423. 为什么不直接用相似度召回？而是过一遍大模型？
424. 讲一下最近很火的onerec吧？
425. 召回索引怎么优化
426. 为什么使用三路召回
428. 介绍MMOE、PLE、ESMM多任务模型
429. 大模型训练中常用的优化器有哪些？AdamW 和 Adam 的区别是什么？
430. 训练时显存占用高的瓶颈在哪？
431. AdamW 与 Adam 在权重衰减上的实现差异？
432. 梯度累积等价于 batch 扩大的严格条件是什么？
433. 为什么Adam不一定最优而SGD最优的？怎么理解分析？
434. 激活函数（sigmoid、relu）了解吗？
435. relu的缺点是啥？如何改进？
436. 其他归一化的方式还了解哪些
437. ADAM优化器相比SGD有哪些改进？
438. 离线与在线指标不一致的解决方案
439. 如果重新做一次，你会在哪些环节提前做 ablation？
440. 服务的容错，docker和k8s
441. 大模型的并行方式，多卡并行，张量并行，数据并行，流水线并行
442. 虚拟试衣技术的原理与应用

## 阿里（阿里云 / 达摩院）
1. 🔥🔥 怎么解决LLM幻觉问题
2. 🔥 human feedback是怎么被agent消化吸收的？有没有用rl进行策略更新？
4. 基本信息确认、入职时间、薪资预期、职业规划
5. 小米训练用的什么框架
6. 为什么要用位置编码?为什么要用sin_cos?
8. 有没有做记忆衰退，避免旧数据干扰新任务？
9. 了解哪些agent开发框架，例如langchain和LlamaIndex，他们核心应用场景有何不同？
10. 问数据的输入输出格式如何保证大模型输出稳定的json做了哪些工作？
11. Encoder与decoder的中Attention区别?
12. 6.RAG有哪些可优化的地方
15. 常见的对比损失有哪些
17. 询问之前实习中Agent的设计思路，以及所提创新方法的实现方式。
18. 提升推理能力和指令跟随能力哪个更难，为什么，提升指令跟随能力的优化方式和其他的比如推理有什么不一样的地方
19. 询问Agent工具的设计情况，是否采用workflow形式。
20. Attention 为什么要做scaled ，不做会怎么样，为什么用根号 d _ k
21. 说一下 Decoder 的因果注意力， QKV 分别来自哪
22. LoRA 初始化怎么做的，用的秩是多少，为什么不选其他的数
24. 为什么除以根号下Dk?
25. KV Cache显存计算方法
27. 为啥分类任务用交叉熵，不用MSE?
28. post norm和pre norm的区别？
29. 实习与学校学习/项目的区别
30. 若Agent推理API需要低延迟响应，会从哪些方面开展系统级优化工作？
31. agent调用工具不正确怎么办，采用sft或者强化学习怎么来解决？
32. 如何提高模型的推理速度
33. 说说策略模式？
35. final关键字的作用
36. 介绍下DeepFM模型
37. 提及使用DeepSpeed开展SFT训练，请说明DeepSpeed ZeRO Stage 1 - 3的不同之处，以及何种情况下使用FSDP更为合适。
38. ZeRO 的三个阶段分别是什么及其优化目标
39. 在高并发查询 Agent 系统中，你会如何优化召回和生成阶段的延迟？
40. 为什么RoPE比绝对位置编码更适合长文本？
41. MLA是怎么做的？为什么它比LoRA快？同样是低秩分解，为啥推理时LoRA慢而MLA快？
43. ppo算法为什么有reward model 又有critic model
44. 用的模型参数量有多大？
45. DAPO 改进了哪些方面？
46. 防抖和节流的原理及具体作用是什么？
47. 用两个栈实现队列
48. 如何做 Dropout
49. 你为什么选择这个方向？


## OPPO
1. 🔥🔥 了解大模型吗
2. 🔥🔥 DPO的原理
3. 🔥🔥 梯度消失和梯度爆炸怎么解决？
4. 🔥🔥 位置编码
5. 🔥 transformer相比LSLTM的优势
6. 🔥 5.了解哪些激活函数
7. transformer
8. 召回主要用哪些算法？
9. 了解模型蒸馏吗
10. 介绍第二个RAG项目
11. 反问，问部门是干什么的，说是训大模型的，不做应用
12. 介绍DIN模型


## VIVO
1. 对方说hr那边出了点情况，最近招聘是组内直接负责。
2. 分类问题的损失函数是什么，为什么不用MSE


## 京东
1. 简历项目深度拷打,多模态项目细节深挖
2. LoRA 和 Prefix Tuning 的区别？在什么场景下选择 LoRA？
3. 如果要用 LoRA 做电商推荐场景的微调，你会怎么设计数据和标签？
4. 搜索中 RAG 的向量检索会受到长尾商品影响，你会如何缓解？
5. 如果商品知识库实时更新，你怎么保证 RAG 的召回结果和库存一致？
6. Reflection 机制里，如何判断一个 Agent 的失败是由知识缺失还是工具调用错误引起的？
7. Toolformer 中通过自监督学习生成 tool call 数据，这个训练范式和 RLHF 的差别在哪里？为什么它更容易泛化？


## 其他
1. Reward Model有什么优化的方法吗？
2. 10. 4.31 模型在SFT后会出现“复读机”情况该如何debug，以及出现的原因是什么？
3. 知道Lora中的scale吗？
4. dpo 出现 chosen 和 rejected的概率都下降是为什么,怎么解决
5. LoRA中的scale参数的作用及设置方法是什么？


## 哔哩哔哩
1. 召回损失函数设计介绍一下？
2. 如何进行监督微调（SFT）
3. 7、是否了解DIN、SIM用于embedding
4. 8、从模型角度介绍特征交叉


## 小红书
1. 抖音和小红书的推荐系统在算法层面有什么核心差异？
2. 介绍一下了解的其他基于 MoE 的模型架构
3. 如果在训练 DPO 的过程中，正例和负例的 loss 都在下降，该如何解决？
4. 是否有微调经验及总结
5. dpo训练对于系统问答的优化在哪里
6. rerank 用的什么模型
7. RAG遇到模型缺失电商知识一般怎么做
8. 全参数微调 7B 需要多少显存
9. DPO、PPO、GROP之间的区别是什么？
10. LLM与推荐系统结合的可落地方案有哪些
11. 求二叉树中两个节点的最近公共祖先


## 拼多多
1. 🔥 手撕：lc143 重排链表
2. 问RLHF的流程，问到RM的训练的时候突然问RLHF的loss是什么，顺势就以为问的是RM的loss，答交叉熵，说不对？？？不是吗？后面想了一下他可能是想问PPO的loss
3. RoBERTa相比BERT有哪些改进？
4. 介绍lora，为什么lora是有效的（只需要训练更少的参数而不是训练全参数）
5. 大模型相关知识了解
6. 实现Top-p采样算法


## 携程
1. 有没有使用过ChatGPT？


## 滴滴
1. 介绍下vllm的技术点。
2. Lora 相比全参数微调可以节省多少计算量和显存？
3. 10. 4.18 讲讲attention的各个变体
4. 你觉得游戏中的智能npc会带来什么样的收益，要你设计类似逆水寒中的智能npc，你该怎么做，说说从数据收集、预处理到模型训练，系统开发该怎么做
5. 如何让模型知道代码生成的对不对（代码评估）
6. 如何计算LLM参数量
7. 训练一个智能npc你觉得需要多少数据量，模型尺寸，训练的策略该怎么选
8. 如何解决对话系统中时延问题
9. 为什么moe结构的RM，能力点没有标签
10. qwen和qwen2的区别有哪些?
11. 如何解决梯度更新噪声大（mini batch）的问题
12. triton学过吗，传统方法部署模型的流程是怎么样的


## 百度
1. MOE架构原理
2. 八股:DeepSeek R1的创新点和优化点?
3. LoRA介绍，和全参sft怎么选择？小模型的sft和大模型的LoRA效果对比会是怎么样的？sft数据集如何构建？
4. 介绍一下 beam search原理，与直接sample的区别？
5. 对一份数据在某个场景下进行分类/识别/检测，用大模型有什么方法可以做？
6. 如何对AIGC的文本进行评估？
7. ppo中kl散度的作用。
8. 如何利用大模型本身相关的方法，指标去判断数据，筛选数据
9. 如何扩展闭源的benchmark，或者如何从大量的指令数据里面提取能力项，构建扩展已有的benchmark
10. DPO的原始数据构建，如果我有一批数据格式遵循不好但是推理能力OK，另一批数据推理不行格式遵循OK，怎么构建偏好对做RLHF/DPO
11. 你用的模型有多少层
12. 大模型中常用的位置编码方案有哪些？请分别说明其优缺点及适用场景。
13. 介绍一下Bert
14. transformer相比于其他模型架构的优势
15. 数据蒸馏的方法
16. 商品塔接入多模态 encoder 后为何离线指标下滑？定位到哪个环节？
17. 生成式推荐相较于传统推荐方法的优势是什么
18. ResNet的核心思想是什么？


## 网易
1. llm如何处理长文本记忆功能
2. 词向量的原理直觉


## 美团
1. 强化学习奖励模型怎么训练的
2. 反问，组里做到餐的LLM生成餐，toC和toB，资源可能紧张
3. vllm是怎么加速的
4. LORA为什么可以实现少量的参数完成全量微调的效果
5. LORA的秩一般是如何选取的
6. SFT 使用的数据集，使用了多少张卡？ SFT 训练多久？
7. 介绍一下 ESMM(包括后续改进)
8. bert的原理
9. 模型选型问题，为什么选qwen3-8b，如何估算模型开销
10. 接触过哪些推理加速的方法。(vllm的page-attention, kv cache, prefix cachemla，flash-attention直接安排一套)
11. 基于值函数的和基于策略的有哪些模型？
12. 模型评估性能指标有哪些以及它们的定义和用途
13. 知道哪些精排模型
14. 如何评估召回系统的性能？
15. 最多做过几卡的模型训练?对deepspeed和Megatron有多少了解?
16. 项目拷打，特征怎么做的，为什么选这个模型
17. 项目：未来希望专注大模型哪个方向？（对齐 / 推理加速 / 长上下文？）为什么？
18. 大模型前沿了解哪些
19. R1的 MLA是如何节约 KV cache的?
20. 使用的 Embedding 模型结构是什么?输出向量维度是多少?
21. 长上下文压缩有哪些方法？
22. RAG常用的检索方式
23. 八股：Qwen 或 DeepSeek 技术报告中提到的关键创新点有哪些？（如 RoPE 外推、MoE）
24. Transformer中的多头注意力机制原理
25. 为什么选择DPO而不是其他强化学习算法如PPO？
26. 大模型的优缺点及个人体验
27. QLoRA是如何实现的
28. Qwen 2.5 VL中的Transformer结构与普通Transformer结构有哪些不同？
29. 召回了解的多吗？
30. 了解并介绍推荐系统中除重排之外的其他模型原理
31. 模型压缩这一块知道哪些具体的方法？
32. 八股：DeepSpeed Zero 各阶段分别做了哪些优化？
33. 项目：模型部署用了什么框架（vLLM/TGI/自研）？如何优化推理延迟和吞吐？


## 腾讯
1. 🔥🔥 7. grpo比dpo和ppo优势在哪？
2. 🔥🔥 讲解 LoRA 原理。
3. 🔥🔥 推荐系统全链路详解，电商推荐的核心难点
4. 🔥🔥 介绍AUC，AUC表达的是什么？
5. 🔥🔥 位置编码有哪几种？具体介绍了ROPE
6. 🔥🔥 讲一下你了解的优化器？
7. 🔥 reward function 如何设计的为什么这么设计？
8. 了解deepseek - R1吗，介绍一下
9. RAG过程中索引可以做哪些优化？
10. 有没有涉及到模型训练
11. 什么是旋转位置编码，解决了什么问题，为什么
12. 为什么在项目中选择GRPO而不是PPO或DPO？
13. 讲一下 RLHF 的流程，之前有用 RLHF 做过模型对齐吗
14. Attention机制的原理及应用
15. 6．在 RLHF 中，目前主流的强化学习算法有哪几个，写一下损失函数的表达式
16. 当时你用 DeepSpeed ZeRO-3 来微调 Qwen2-72B，每一张卡占用的显存大概是多少，估算一下为什么是占这么多的显存
17. 除了 DeepSpeed，还用过其他的什么优化方法吗
18. 好的，想象一个场景。我们希望打造一个产品，用户做广告不再是过去哪个先建广告组、做素材、定目标···而是交给 agent，用户只需要输入商品和基本信息，其他交给 agent 去做。那在这个过程中，main agent 发出指令，subject agent 执行。如果 subject agent 认为需要再做一个素材，这个过程应该如何流转？这个关系你会如何思考设计？
19. SFT的局限？
20. 讲DPO、PPO、RLHF什么
21. 2．讲一下大模型训练和推理的流程， SFT 和 RLHF 的作用分别是什么
22. 3．为什么探索 MoE 架构， MoE 相比 Dense 有什么好处
23. 相似度矩阵具体怎么做的
24. 结合项目讲大模型训练的几个阶段的特点和异同
25. 讲一下你对 agent 和 Workflow 的理解
26. 3.介绍MoE （混合专家）架构核心优势。
27. 4.阐述大模型训练与推理的完整流程。
28. 5. 对比 LORA 微调 Qwen 模型两种微调方式的性能表现。
29. 开放题：我看你也做了这么多 LLM 的事情，你怎么看待 LLM 的发展？
30. 4.qwen2.5和qwen3之间有什么区别你了解吗？
31. LGB只用了统计特征吗，已有embedding，为什么不用深度模型呢
32. DIN是拿哪些信息训练的
33. u2i是自己做的还是模型自动做的


## 荣耀
1. 4、softmax表达式，以及导数推导
2. 项目几个人参与、怎么与甲方沟通的、验收指标甲方评价如何
3. 介绍一下ViT、说一下多头自注意力机制的原理和应用
4. 介绍大模型项目的研究内容，ViT的原理
5. 最近有关注大模型最新的研究进展吗，介绍一下，有没有关注过生成式、Agent等等相关的
6. 为什么要使用KV Cache？
7. yolov8的算法原理、语义分割模型的算法原理、指标的计算原理等等
8. 业务？主要是用在物流场景、工业相机等，有目标检测、语义分割、视频解译等，大模型小模型多模态都会用到


## 虾皮 Shopee
1. 推荐系统的公平性优化


## 蚂蚁集团
1. 🔥 代码题：lc129 求根节点到叶节点数字之和
2. 如果召回的答案不是想要的，该怎么处理？
3. 为什么有了reward model还需要critic model？critic model作用是什么？
4. vLLM框架是怎么做推理加速的？
5. 构建 Agent 的时候，遇到过哪些瓶颈？LangChain 的 memory 默认机制在多用户并发中怎么做隔离？你是如何保证线程安全的？
6. 交叉熵和kl散度的联系和区别？PPO的kl散度可以改成交叉熵吗？分类任务可以用KL散度吗？
7. rollout数量 batchsize数量和计算资源(卡的数量)有什么关系？线性？非线性？
8. 你的 Agent 系统Prompt 是怎么设计和迭代的？有没有做过 Prompt 自动优化？当用户提出不完整的请求时，如何补全用户意图的？
9. 你做的 Agent 使用了多少个外部工具，在调用链条上如何保障故障容错和超时机制？
10. 有没有做过工具调用失败后的feedback策略设计？
11. 多轮对话上下文状态管理是如何做的？如何在高并发场景下保证一致性？
12. PPO的原理？从维护的四个model讲，再详细讲一下训练流程和损失函数各个参数含义？
13. 微调项目是如何模型选型
14. 项目:如何做微调的?直接用 PEFT 库,还是用LLama Factory做的?
15. vLLM 中使用的技术是否熟悉（如 Paged Attention 、 KV Cache )?
16. 讲一下什么场景下用SFT，什么场景下用RL
17. 有评测过吗？
18. 微调 Llama2 你是怎么选择训练样本的？清洗逻辑是什么？你有没有观察到哪些训练样本质量问题对模型行为有很大影响？举例说明。
19. DPO相比 SFT，有哪些优劣？它在 Agent 任务上效果提升明显吗？你怎么构造偏好对？构造逻辑是自动的还是人工？
20. 你说你服务部署在 vLLM 上，为何选择它？KV-cache 如何帮助推理加速？你自己做过哪些优化？
21. 有没有了解过带有时间窗口/偏移限制的对话系统？模型怎么“理解时间”？
22. Qwen2.5-vl pretrain 阶段用了哪些数据？
23. 对齐任务一般放在哪个阶段进行？
24. 你在 training 的时候long cot 能力下降了多少，有评估吗？
25. MLLM 不做对齐会有什么结果？
26. 你有考虑你的场景下做增量预训练吗？
27. 如果你用 LLM 训一个专门用来评估，和你用 sim 的评估方法有什么区别？
28. 可以当奖励模型吗？
29. MLLM 做 rl 会有提升吗？
30. 可解释性生成你是如何做的评估？
31. 给我讲一讲这几个指标以及为什么起作用。
32. 假如需要支持 Streaming 输出，但当前服务延迟又超标，你会怎么折中设计？
33. 你觉得 Agent 哪些模块最容易在真实业务中出问题？你会如何监控和定位的？
34. 给你一个场景，假设让你用 bert 或者 transformer 做一个文本分类，你能很快搭建吗
35. RAG技术原理，如何衡量RAG回答的好坏？
36. DPO的正负样本怎么构造
37. 分类任务常用的评估指标有哪些及其含义
38. CNN和Transformer的区别及适用场景


## 通用题库
1. 你觉得NLP和LLM最大的区别是什么?两者有何共同和不同之处?
2. 二面:大模型生成内容的评测方式有哪些，具体怎么操作？
3. 如何确保大模型输出内容的一致性？
4. 阐述大模型的幻觉现象及抑制方法。
5. 讲解DeepSeek R1的训练流程和基本原理。
6. 训练一个7B模型要占用多少显存？不同ZeRO阶段能节省多少显存？
7. 如果子agent回复不对怎么办？反思？跳不出去怎么办？限制次数？
8. 代码题:lc143 重排链表
9. 项目:你在项目里有没有做过 RAG 里的"召回-过滤-生成"三段式 pipeline?能不能细讲一下?
10. 如果让 agent 调用搜索引擎，如何避免无关结果影响回答？
11. RAG怎么评估,指标有哪些
12. RAG如果有噪声怎么办
13. Agent整体流程是怎么做的？包括哪些模块？
14. 项目:为什么GRPO在训练MOE时会出问题?原因是啥,怎么改进策略
15. 为什么PPO要用value baseline和GAE？它们如何让训练更稳定？
16. 项目:实习项目问的很细,数据构造,微调参数等
17. 是否自己实现过 RLHF 流程？不用框架能否手写 PPO 核心逻辑？
18. 如何确保一个 Agent 的行为是安全、可控且符合人类意图的？在 Agent 的设计中，有哪些保障对齐方法？
19. 如何证明 Agent 比人工客服更好？设计评估方案
20. Qwen3的技术原理
21. Deepseek GRPO，讲讲原理和之后的改进
22. PPO/GRPO 微调后，如何防止模型在分布外(OOD)问题上性能崩塌？
23. 项目:LLM怎么微调的,数据量多大,各数据配比多少
24. 项目:在项目中你用过 DPO 吗?和 PPO 相比,它有什么优缺点?
25. 项目:Deepseek MLA?为什么压缩?
26. 项目:GRPO的KL散度是什么?KL散度中超参数如何设计?
27. bf16 和 float16 的区别？各占多少位？训练中如何选择？
28. Q10: 解释一下混合精度的原理
29. 项目:介绍实习项目,项目中有没有做微调?
30. 请你详细介绍ROPE,对比绝对位置编码它的优劣势分别是什么?
31. 激活函数有了解吗,你知道哪些LLM常用的激活函数?为什么选用它?
32. 介绍检索做的优化,具体追问子问题分解怎么做,有没有做意图识别
33. SFT数据问题不够多样化怎么办
34. PEFT的方式,LORA论文讲一下,对比p-tuning
35. LLM训练的时候为什么warmup
36. Transformer模型中计算量(FLOPs)的分析
37. RoPE和ALiBi两种相对位置编码的原理
38. 开源框架了解过哪些？Qwen，Deepseek的论文是否有研读过，说一下其中的创新点主要体现在哪？
39. SFT 的 loss 如何只计算回答部分？(如何 ignore padding token?)
40. 八股:大模型框架了解哪些,介绍下vllm原理
41. 八股:Transformer中哪个模块的计算量最大?如何优化
42. 传统RAG有什么痛点;介绍GraphRAG,GraphRAG的难点是什么;GraphRAG如何应对增量场景
43. 介绍微调负责的工作;大模型微调最重要的是什么
44. QLoRA是怎么降低资源成本的?NF4和FP16这组组合为什么有效?
45. RAG系统在实施过程中面临哪些主要挑战？
46. 预训练和微调任务有什么区别,两者的目的
47. 代码题:lc141 环形链表
48. 对比学习中的batch size是大一些好还是小一些好(大一些,甚至可以到10k+,为了构造好的negative样本)
49. 强化学习中策略函数和值函数是什么
50. 如何量化优化效果？
51. 如何评估多模态模型的性能？除了准确率，还有哪些指标？（如 Recall@K, mAP 等）
52. 多模态学习中常见的融合方式有哪些？


## OPPO
1. 3.ChatGPT对语音助手的冲击有哪些，会从哪些方面影响到现在的语音助手
2. 4.深挖个人项目，其中涉及到Bert，Chinese-Bert-WWM，Chinese-Roberta-wwm-ext的发展演变，其中Whole Word Masking (wwm)是怎么做的，了解预训练阶段的策略吗，介绍一下
3. 3. 从文本输入开始，给我讲一下 Transformer 的流程，不考虑多头的原因，self-attention中词向量不乘QKV参数矩阵，会有什么问题？QKV 矩阵怎么产生的，为何使用多头注意力机制？参数量会变大吗
4. 显式的位置编码和训练式的位置编码哪个好？
5. 为什么会有KV Cache？为什么没有Q Cache？
6. 介绍Transformer，为什么注意力能起作用
7. 会不会C++，落地部署
8. 了解哪些数据结构并介绍链表
9. 如何处理模型过拟合问题？（如数据增强、Dropout、正则化等）
10. 为什么Sigmoid一般和交叉熵一起用，而不是和MSE一起用？
11. 4. 讲讲推荐系统里有哪些注意力
12. 对推荐系统的哪些地方感兴趣？
13. 推荐系统物品点击率的分布是啥样的？
14. 推荐系统有哪些Bias特征
15. 是否实践过图像生成模型（如GAN、Diffusion Model）？举例说明其应用场景
16. 请介绍你对多模态模型相关工作的了解


## VIVO
1. Transformer的注意力机制是什么？
2. 有三个工人(x y z)和需要完成的任务数(n), Xy z表示,每个工人可以完成的最大任务数目. 问一共有多少种分配方式,工人可以完成零个任务
3. 常见的分类模型


## 京东
1. Transformer的激活函数什么，为什么不用Sigmoid
2. 然后聊了半小时onerec，重点在多模态tokenizer和语义id
3. attention常规八股(根号dk，时间复杂度，为什么要分多头)
4. MoE模型的专家数量是如何确定的？
5. 树模型(GBDT)和深度模型(DNN)的特征重要性差异?
6. 模型融合:GBDT叶子节点接入DNN的具体实现?
7. 反问：会做生成式推荐吗
8. 点击率预估模型如何应对刷点击作弊?
9. 手写双塔模型的损失函数(Batch内负采样实现)
10. 了解目前主流多模态模型吗，扩散模型公式怎么推导的


## 其他
1. 10. 4.31 模型在SFT后会出现“复读机”情况该如何debug，以及出现的原因是什么？
2. 涉及模型训练的项目，面试官可能会提问的点
3. 给定多少token的数据,1B的模型,算力flops,计算训练时间
4. 项目经历？数据处理？模型怎么改的？训练时间？数据量？用了多少节点？下游任务SFT后怎么解决通用能力下降？
5. 如果你来参加星火大模型项目，你要做哪些事
6. 大模型能代替老师吗？怎么理解
7. 做过rag是吗？介绍graph rag？bge和gte模型怎么训练的？为什么不能直接用bert-base来做余弦相似度召回？sentence-bert和bge的原理区别？sentence-bert在训练推理阶段的区别？
8. 什么是自回归语言模型和n-gram模型？
9. 为什么BERT在第一句前会加一个[CLS]标志? BERT输出的两个函数是什么？
10. 什么是对齐税 Alignment Tax？如何缓解？
11. 10. 4.17 介绍Lora及其变体的特点
12. 10. 4.19 讲讲工业界RAG具体如何优化？
13. 对于大模型的badcase，如何迭代优化
14. 对于大模型复杂推理任务，有哪些主流方法
15. 星火大模型的了解是什么，怎么看待星火大模型
16. 大模型能解决哪些场景
17. Lora为什么在工业界这么吃香？原因是什么？
18. LLM的分布式框架了解过吗？展开讲一下它们的优缺点？
19. 大模型的训练的完整流程是什么样子的？为什么要先经过SFT微调，在RL？
20. DPO和PPO有什么区别？你更喜欢使用那种？当时浅浅回答了下，喜欢DPO，优点说明下。
21. DPO的公式给我写一下或者口述一下？当时没写出来🙄
22. DPO跟对比学习有哪些相同点和不同点？我的项目用了后者
23. 模型的幻觉问题？以及RAG的好处？如何利用RAG去缓解模型环节？
24. 看过 flash attention 源码嘛?
25. Reward Model的本质是学习同一状态下的不同动作的偏好
26. prompt和instruction的区别
27. 根据需要实现对输入法的算术表达式按照运算法则进行求值
28. 使用numpy手撕二分类交叉熵，包括train和predict的函数
29. 模型训练显存不够怎么办？gradient checkpointing原理？gradient_accumulation原理？
30. 大模型训练用到的优化器和sgd有什么不一样
31. 你了解哪些多模态encoder？


## 华为
1. 是否有过AI训练和推理框架的开发经验
2. 二面继续开挖项目，这次问的问题围绕深度学习相关的问的，主要围着项目问，问了训练中的具体调试问题
3. 关于美团的实习项目，你做的意图识别是如何实现的？
4. 面试官委婉的表达了我的方向和他们这个岗位不是特别匹配的意思
5. Function Call 工具过多导致准确率下降，你是如何解决的？
6. 什么是 RAG (Retrieval-Augmented Generation)？
7. RAG 的查询改写和混合检索是如何实现的？
8. Multi-Agent 通讯和协作的难点是什么？
9. 模型微调的训练数据构建的关键点有哪些？
10. 发散讨论，llm在运维和配置环节能做什么，然后就瞎扯了一会，比如copilot之类的。
11. 有什么建议，建议我看看模型优化这一块
12. 如何选择合适的大模型？
13. Attention机制中qkv的计算方式及意义
14. 力扣74题：搜索二维矩阵
15. 手撕LeetCode 241题：为运算表达式设计优先级
16. 如何将字符串xxxxyy转换为4x2y的格式并使用哈希表实现？
17. 检索策略是什么？


## 哔哩哔哩
1. 7、是否了解DIN、SIM用于embedding
2. 8、从模型角度介绍特征交叉
3. LoRA的原理和使用方法
4. k个有序链表合并，时间复杂度
5. 测试集如何选择？如何判断测试集和应用场景是一致的（无偏的）？模型的离在线效果差异如何解决？
6. 召回和粗排的主要作用？为什么不直接用精排？
7. 怎么评估粗排模型的好坏？粗排怎么做冷启动？
8. B站首页推荐模型可能包含哪些目标作为精排融合分的项？
9. 多路召回的融合方法是什么？
10. adam优化器和adagrad的区别
11. 之前的项目用的什么优化器
12. adagrad没答上来，只让我回答了adam怎么计算的


## 小米
1. 拷打曾经做过的项目，怎么和模型做结合的？以及未来的优化方向
2. 粗精排是否需要保持一致性
3. 从 MMoE 到 PLE ,这条路线的发展方向是什么?
4. 模型部署相关问题


## 小红书
1. 离线RL训练如何切换到在线训练？
2. 实习拷打：项目背景 指标 亮点 难点
3. 拿出自己熟悉的一个项目说说技术选型/难点/落地后评价指标
4. 三面:LLM 与推荐结合的可落地方案，小红书场景下的设计
5. DPO 训练的过程是怎么样的，正负概率怎么算
6. 意图识别LLM输出格式不好怎么优化
7. 知道哪些Embedding模型
8. 怎么防止客服LLM串台问题
9. 你说你会做上下文记忆优化，怎么做的？
10. RAG 技术的核心缺陷及优化方案
11. 小红书笔记内容理解的大模型方案设计
12. transformer吟唱
13. rag 文档怎么切分
14. rag 向量化的模型
15. 有没有微调 rerank 模型/应该怎么微调
16. 谈谈传统搜索算法和RAG的理解
17. 了解MLA吗为什么大模型结合RAG会出现AI幻觉的现象?你怎么看?怎么解决?
18. 开放场景:如果你有一个待优化的模型和一堆query,你怎么利用PPO来优化模型?
19. 讲解一下快速排序最优和最差的情况
20. 说一下你了解的分类模型和原理以及适用场景
21. 意图识别准确率如何计算或评测？
22. 介绍一下双塔模型，结构、样本
23. 召回在整个推荐链路中的作用和必要性？
24. 多路召回融合的动态权重设计，手动还是自适应调整？
25. 规则召回是怎么做的，用到哪些规则？
26. 怎么实现u-u-i的召回？
27. 如果新增一个收藏的指标，应该如何加在PLE 模型中
28. 生成式推荐的 ROI问题
29. 打分样本空间分布与精排不一致的解决方案
30. 评估OneRec和RankMixer的ROI，并分析为什么RankMixer更优
31. 图文笔记的多模态理解与检索方案


## 快手
1. 大模型在短视频推荐中的应用与实践


## 拼多多
1. 10. 反问环节，说是做RAG的，不是那你连我的LLM实习经历也不问？八股也不问RAG？
2. 项目中如何选择模型及原因
3. 4. 问Transformer encoder decoder结构上的不同
4. 6. 后面确实问了PPO的优化目标。。。
5. 如何确保模型输出的格式正确？
6. transformer中QKV的作用是什么
7. 列表和元组的区别
8. 手撕位置编码和MHA+力扣完美矩形变体
9. 给定一个流式整形输入,求中位数
10. 如何求第k大元素，使用线性复杂度的快速排序方法
11. 多目标模型的优缺点
12. 指标对比baseline提升主要来自于什么
13. 电商平台推荐系统差异比较
14. 是否了解 OneRec
15. PLE之后的多任务模型还有了解吗
16. Dropout在训练和推理时的实现方式及区别


## 携程
1. 为什么GRU行为序列建模召回比ItemCF效果更差?


## 滴滴
1. 10. 4.18 讲讲attention的各个变体
2. 最后如何评估自研的judge-LLM生成数据的质量
3. LLM中温度的意义
4. 什么是投机采样？
5. DPO训练后输出长度会变化吗？如何解决这个问题？
6. GSM8K和MATH这两个基准测试集在评估大语言模型数学能力时有哪些主要区别？
7. 预训练一般分为哪些阶段,每个阶段的特点有何区别?
8. 介绍一个传统ML模型
9. 偏好模型和对比模型（Pairwise）有什么区别？
10. Pairwise 排序模型：优化成对文档的相对顺序，主要关注文档之间的关系。
11. 偏好模型：优化用户偏好预测，主要关注用户个体对不同项的评分或偏好。
12. 推荐项目里的图检索具体是如何实现的
13. 文本很长，显卡数量不多，导致训练的batch_size太小，如何解决这个问题
14. 自适应学习率：使用具有自适应学习率的优化器（如Adam、RMSprop），这些优化器能够自动调整每个参数的学习速率，有助于缓解因小批量引起的训练不稳定。
15. deepspeed原理，如何实现zero1，2，3


## 百度
1. 性格价值观评测
2. 你在项目中做过哪些相关性优化？有没有量化结果？
3. 面完问对方能不能过，对方表示过了。
4. 一面自我介绍，项目深挖，熟悉哪个险种，百万医疗风控怎么做需要哪些步骤，怎么构建风控模型，健康险分为哪些类别，让你做健康险风控模型你会提取哪些特征，重疾险做什么样的特征工程，如何识别风险
5. 工作性质,Python用的多还是C++用的多,有无转正,是部署到车机芯片上测实车表现还是部署到测试服务里去验证性能指标?
6. 大模型微调全流程，SFT 数据构建经验
7. Prompt是如何生成的，优化目标是什么，任务是什么？
8. agent 服务高可用、稳健性是怎么保证的？
9. Transformer 各子层功能及去掉 FFN 的影响
10. RAG系统的架构，每一个模块的作用，文本截断的长度是多少？
11. lora rank 设的多大 alpha 有什么作用
12. 讲一下之前做的sft和dpo
13. 问code llm中的训练难点
14. 问简单介绍一下2中的技术，dpo sft rag等
15. GPT3和GPT3.5训练上有什么不同
16. rlhf怎么做
17. reward获取方式分别是什么
18. 反问(做文心一言coder模型预训练的)
19. 讲lora微调，如果是全量参数sft需要多长时间？
20. QWEN2的架构和训练方式
21. 在不同的项目中，都使用了DPO，有哪些区别？
22. 多模态的DPO的训练是如何做的，如果构造数据？
23. 介绍下KV Cache，GQA，MQA，MHA
24. lora的原理，lora会不会更新原来的权重，如果对embedding层也配置了lora会不会更新。
25. Bert和Transformer的decoder的区别（不清楚，不太了解Bert）
26. 为什么不用微调
27. 文案生成为什么不总BLEU指标
28. Lora sft dpo
29. self attention 计算 优缺点
30. 具体介绍一下RAG项目中的应用，如何处理文档，如何计算相似度
31. 手撕transformer模型代码，介绍模型架构，介绍交叉熵损失函数，介绍L1，L2正则化有什么区别，写下完整损失函数公式，写下transformer所有矩阵转换的数学公式，如何理解需要除根号d
32. RAG怎么用的，有没有更好的改进方法，为什么套用大模型结合BM25算法，文档怎么处理的，文档都有什么类型，如何整入数据库并提取
33. 介绍transformer，编码器解码器的作用。介绍一下损失函数，介绍qlora，说说bert以及roberta和deberta区别和联系，介绍一下bert模型都有什么任务
34. 一面，自我介绍，介绍推理框架ollama，流程化结构dify，rag原理，用到的开源闭源大模型效果如何
35. DPO对齐训练的曲线是怎么样的，正例的概率会提升嘛？
36. Deepseek-R1里面不仅推理能力很好，而且文采能力也很好，这个是个开放问题，如何让模型的文采能力也很好呢？
37. DPO 如何解决回答过长的问题，除了正则
38. 开放问题：为什么现在大家都在关注于大模型的推理能力 reasoning
39. 对于一个 base model 如何增强大模型的 reasoning 能力
40. DPO 除了长度问题还有其他的问题嘛，与问题2对应， reward hacking ？都没有奖励模型了
41. LLM是否适合用于此类方法，
42. 说一下SIMPO的原理，它是怎么解决DPO微调序列过长的问题的
43. RAG技术的性能瓶颈主要体现在哪些环节?
44. 介绍一下了解的大模型有哪些，这些模型在结构上有什么差异
45. 大模型智能体的工作原理和组成部分
46. 场景题:如何训练一个大模型以实现精确的摘要提取
47. 大模型的超长上下文是怎么实现的,比如说 KIMI
48. DeepSeek的MoA架构与MoE架构有何区别？
49. 面试中被要求讲解RAG项目时，如何应对面试官引导到模型相关技术点的提问？
50. 命名实体识别中如何处理实体嵌套问题？
51. 比较Match、DeepQA和文心一言在文本相关性及问答效果提升方面的表现
52. 岗位主要做提升文心一言的问答和检索增强任务
53. 如何评估两个文本的相似度
54. 编码：在已排序数组中用 O(log n) 实现目标值的左右边界查找
55. vector的reserve和resize区别
56. 二叉搜索树的插入、删除操作及构建方法
57. 同样是排序指标，NDCG 与 MRR 的评估视角差异在哪？
58. 损失函数：CE和对比损失
59. 如何分析训练结果并改进训练数据的构造方式？
60. XGBoost和LightGBM的区别及其并行化方法
61. 召回、排序哪个阶段最可能出问题？
62. 如何构造排序模型训练数据？如何解决正负样本不均？
63. 四塔多目标方案相较经典双塔在 CTR/跨类目召回上带来哪些可量化收益？
64. 用户塔输入特征列表中，哪些对跨类目效果拉动最大？上线后除 AUC 还重点监控哪些业务指标？
65. 是否尝试过 MMoE 等专家网络？专家数量与推理延迟增量各是多少？
66. 除了向量召回和关键词召回，还有哪些召回方式，了不了解全文召回，如何做的？
67. 向量召回，关键词召回，实体召回等不同召回链路召回的结果如何合并，哪一个优先级更高？
68. 了解的召回推荐模型
69. 为什么用精排
70. 生成式推荐与传统DLRM有什么区别？
71. MmoE的全流程,怎么确定专家数
72. 常见的量化方法有哪些及其原理
73. 讲实习中的部署优化
74. 问部署优化有什么经验（面试官希望设计算子内容，但我不会）
75. 有做什么部署优化吗
76. deepspeed 的每一段的通信比较,zero3分别是0和2的多少倍
77. 模型选型时是否做定性定量对比ab test,客观数据验证文心性能不好了吗
78. Deepspeed的zero1、zero2、zero3中混合精度的使用方式及其它显存优化方法
79. 多模态向量维度规模多大？全量推涨后提升显著的根因分析结论是什么？
80. clip训练方式？temperature的作用
81. CLIP损失函数
82. diffusion过程


## 网易
1. 2.分类模型微调前如果比较确定，但sft后可能会把概率输出变得不那么确定了，你觉得是什么导致的
2. 5.为什么sft和rl在post-train中可能需要轮着来
3. 训练时为什么要mask,推理时也需要吗?
4. 实习时用的megatron框架吗,对分布式训练框架了解多少?
5. 训练模型时用了几张卡,有遇到什么异常中断问题吗?


## 美团
1. 是否自己动手实现过一个RL智能体：答：没有
2. 你做过AI相关的开发是吧？介绍一下你在美团的agent的开发的场景和技术难点？
3. 你了解你在美团的BI系统的整个架构吗？ 原始数据从哪里来的？全部导入数据库吗？
4. 这个AI平台商用了吗？基座模型用的什么？介绍一下整个平台的架构？
5. 介绍 DeepResearch 几篇工作？主 Agent 和子 Agent 有什么区别，主要哪些子 agent？
6. 项目中的指令数据是你自己构造的吗？是否自己尝试过对指令数据做修改？
7. 有没有尝试修改项目中的prompt？prompt的准确度如何评估？
8. 项目有做过流量压测吗？单服务还是多服务部署？
9. 水平分表按什么来进行？从理论层面分析达到什么量级分表，什么量级分库，什么量级分集群？分库分表的场景和方式？
10. 找算法实习是专注于推荐领域吗？还是说有投大模型的岗位
11. 拷打实习项目，每个环节的参数选择、一个transformer decoder的输出来回问了有十分钟，压力拉满了
12. 建议：1.不能听HR的一面之词，多调研，多找人打听真实情况，最好是内部部门工作的人 2.坑很多，需要自己多掌握多方信息，别进去没多久就后悔，一半内部转岗会有时间要求，一般一年后才能转，所以因为信息差和缺乏有效调研进坑痛苦一年也划不来 3.选择确实大于努力，有些人进去后内部转岗也需要具备良好的识别能力和眼光，有些人内部转岗才发现是从一个坑转到了另一个坑，现在不好的部门或许因为时代机遇顿时变香饽饽，现在不行不代表未来2-3年不行，因素很多，听到hr一些调侃“部门行不行看领导行不行，领导行不行看大领导行不行”，我问啥样的领导行呢？hr：能带领部门业务取得利润且赚钱的领导。重点因素：领导，大领导...
13. 用 LangGraph 实现多轮对话 Agent,相比手写 prompt 流程有哪些工程和效果优势?
14. Bert如何训练的
15. 三个wise训练区别
16. 解释一下TRPO，PPO
17. llama结构
18. 什么情况用Bert模型，什么情况用LLaMA、ChatGLM类大模型?
19. 刚刚提到 MLA ，那 MLA 是怎么对 KV Cache 做优化的
20. Qwen是怎么做长度外推的
21. 在 PPO 中，如何防止模型在微调数据集以外的问题上泛化能力下降？如何防止模型收敛到单一类型的高奖励回答
22. 介绍一下 Qwen布的这几版模型，都做了哪些贡献，包括数据、模型和训练
23. DeepSeek 有了解吗， DeepSeek 用到的 MLA 注意力是怎么做的？它可以直接用 RoPE 吗？为什么不能，它做了哪些优化
24. 了解大模型的解码策略吗，简要说一说吧
25. 现有一个能力较弱的多模态模型和一个能力较强的文本模型（如 DeepSeek-R1），如何结合两者的能力来回答与多模态相关的问题？
26. 3.新结构增加的参数量
27. Reranker模型如何构造数据微调
28. MLA具体是怎么做的？可以加快推理速度吗？
29. 多模态大模型的vision encoder一般使用vit的第几层输出?
30. RL tool 的 loss 有什么区别？
31. 讲一下你对BERT模型的理解？它相较于传统深度学习模型的它的突出点是什么？
32. BERT模型相较于Transformer架构的优化是什么？
33. prompt调试有做过吗？
34. LoRA微调的框架用的什么？微调的时候是否遇到什么问题？比如收敛问题，指标不符合预期的问题？是怎么解决的？
35. LoRA微调时的优化目标是什么？用的什么LOSS？
36. Qwen 与传统的Transformer模型相比，有什么结构上的改进？
37. LLM的损失函数是什么？给你一个10w的词表，计算出事的损失值
38. GRPO为什么要做clip，直接用SFT后的模型还会不稳定吗？优势度可以怎样改进？
39. 为什么你要用GRPO？GPRO结果比之前好多少？显存开销多大？训练一个Step需要多久？奖励函数如何设置的，为什么？有没有想过为什么一开始Reward出现大幅度震荡？GRPO是否一定有效，还有什么解决方法？
40. Post-Training 的工作机制，为什么要做三阶段训练？什么情况下应该用GRPO？为什么DeepSeek用了GRPO？如何从V3到R1？
41. FLUX的工作原理，LoRA在这个地方起到了什么作用？
42. 3.RAG链路的流程。如何评估rag的效果？有哪些指标？
43. 4.讲讲微调（全量和高效）。LoRA的原理。了解多少别的变种？
44. 5.Transformer八股。讲讲自注意力机制。了解什么位置编码方式？
45. 8.讲讲PPO和GRPO
46. 谈谈大模型召回的理解？
47. transformer的normalization，为什么用layernorm不用其他的；介绍RMSnorm
48. 向量维度说上了
49. 大模型sft解决不了业务问题吗?为什么还要引入强化学习。强化学习主要解决业务中的什么问题。
50. 大模型推理加速方案在工业界的落地经验
51. LoRA为什么有效
52. bert和t5的区别
53. 微调使用的是什么框架？
54. 如何处理特别长的上下文输入？
55. Llama与原始Transformer架构的主要区别是什么？
56. SFT数据的构造方法
57. transformer中softmax的作用、问题及解决方法
58. 如何设计有效的prompt模板或规则
59. 询问大模型的基本概念和原理
60. Langchain的了解程度及工作机制
61. LoRA微调中如何选择rank值？合并adapter权重时是否遇到梯度爆炸？
62. LoRA的原理是什么？LoRA是否只能在Linear层插入？为什么不能插入在LayerNorm之后？这会对训练稳定性造成什么影响？
63. 混合检索的原理是什么？Sparse检索和Dense检索的原理及相似度度量是什么？
64. R1在SFT阶段进行冷启动的目的是什么？
65. 你们的产品是否使用大模型？如果使用，是如何训练的？是从头开始训练还是进行微调？
66. RAG的优化方法及超参数（chunk size/overlap）如何设置？是否使用rerank技术？
67. ChatGLM的结构是什么？
68. 处理长文档PDF时，采用了哪些长上下文扩展方法或技术？
69. vLLM部署中如何实现2k tokens/s的吞吐?
70. 大模型的量化方法有哪些
71. Lora的优势和缺点是什么？
72. 大模型解决了什么问题以及为什么引入大模型
73. Attention计算中有哪些显存优化策略？
74. 为什么引入 RAG?在什么场景下 RAG 比纯 SFT 更有效?
75. 你觉得当前RAG的最大瓶颈在哪?你做过哪些改进来提升Recall
76. 讲讲RAG项目中从数据清洗到检索服务上线的整个链路搭建以及chunk切分的方法
77. Transformer在训练过程中更新哪些参数？
78. 多轮对话中如何解决模型遗忘历史信息的问题
79. 大模型在美团业务中的应用场景有哪些？
80. 项目细节中的SFT数据合成、SFT/RL训练细节和奖励函数设计
81. 项目细节:证明Cold-Start SFT后再RL的模型比只RL效果好
82. Qwen 2.5 VL的图片输入处理与Loss设计
83. 八股:解释BERT的模型结构和原理
84. 大模型容易 reward hacking,如何解决?
85. VLLM prefix cache实现过吗?
86. encoder中的self-attention和decoder中的self-attention有什么区别
87. 问有没有其他方法: 最小堆，再排序O(nlogk)
88. 把自己实习模型的结构和训练流程在ide里用伪代码实现
89. 先做了两道题，一道easy，一道mid，都是链表。
90. coding：一道链表mid
91. 算法题 mid链表题（1-2-3-4-5-6的链表变成1-6-2-5-3-4）
92. TypeScript 中的泛型是什么?
93. 用过Map嘛,怎么用的,底层是如何实现的,什么结构,不同版本之间的差别,如何保证并发安全,为什么1.7有环链,为什么2的n次方容量,扩容位置变化
94. 跳表的原理及应用场景
95. 手撕排序链表
96. 强化学习中马尔可夫（MDP）中的五元组是什么？
97. 什么是强化学习的熵崩溃？怎么优化或者解决这个问题？
98. 如何确定你项目的评估指标迭代是否符合当前需求？
99. 之前本科是否有学过机器学习，深度学习，强化学习的基础知识？
100. 7.了解哪些强化学习算法？off-policy的举几个例子。
101. 机器学习相关：LR和FM，RF和GBDT区别，归一化方法，决策树特征选择
102. 如何理解强化学习中熵的概念，如何保证训练过程中熵保持在较高的水平。
103. 精确率和召回率
104. 下一个排序
105. rerank重排是不是有比准确率更好的指标？
106. 对推荐模型与机制的理解，更加愿意做什么方向的工作
107. 如果直接把这些特征输入到一个 LR 或其它简单模型做融合，和你现在的模型相比效果差距大吗？
108. 相比 LR 这样的线性模型， MMoE 的优化优势体现在哪里？
109. 对推荐系统中的重排模块了解哪些?
110. 推荐系统长期价值评估指标设计
111. 召回离线评估指标体系
112. MMOE如何解决负迁移问题
113. 多路召回策略中各策略召回文档的好坏如何评估
114. 多任务学习中如何平衡不同任务的损失函数？
115. 推荐系统离线都看什么指标,这些指标有冲突怎么办?
116. 排序模型离线指标和线上效果不一致如何处理?
117. 6.激活函数和损失函数区别
118. 优化算法知道哪些?讲-下AdamW
119. 深度学习相关：transformer结构，lstm和rnn区别
120. 模型训练的时候梯度如何传播？
121. 显存占用和哪些因素有关?
122. 6.模型训练过程中出现部分节点失活的情况,数据应该怎么处理?
123. 残差连接如何缓解梯度消失和爆炸问题？
124. 针对一个优化点，如何快速上线一个模型？
125. 如何优化系统支持更高并发？存储瓶颈和流量瓶颈？
126. 后训练用的哪个框架？你用过什么框架？如何使用deepspeed进行分布式训练？脚本是你自己写的吗？
127. 系统的状态有哪些指标
128. 性能优化指标如何获取及实现
129. 分布式训练中 Zero-2 和 Zero-3 的核心区别是什么?


## 联想
1. 问模型训练、RAG、embedding、transformer等基础八股
2. 出题：英文题目，共享屏幕用ppt画一个（设计一个）一个3D换脸的流程，网络结构，损失函数如何设计
3. 有没有端侧部署经验，或者安卓部署用过没


## 腾讯
1. 3.介绍MoE （混合专家）架构核心优势。
2. 4.阐述大模型训练与推理的完整流程。
3. 5. 对比 LORA 微调 Qwen 模型两种微调方式的性能表现。
4. 4.qwen2.5和qwen3之间有什么区别你了解吗？
5. 你知道 lovart 吗？你认为他是 agent 还是 Workflow？你怎么判断的？
6. 你觉得有代表性/有特色/有难度的是哪一个项目？
7. 项目真实部署到线上过吗？
8. 关于这个项目，我想问的问题就差不多了，看下你这边有没有一些问题想问的？
9. 问腾讯IEG这边的工作，deepresearch的deep是如何体现的（介绍了DMA的tool调用，感觉可以再了解一下多少个tool，SFT的流程
10. 聊点业务上的，目前广告产品已经有很多工具能力，生成素材、投放等工具，目前我们有两个策略：A-all in one ，B 让做多个产品。你支持什么策略？为什么？
11. 针对最后一个问题（agent 之间的关系和流程），您是怎么思考的？
12. subject agent 的设计思维考察（意图、环境、function）
13. 腾讯的实习会不会因为到岗时间偏晚而在综合排序的时候被比下去啊😭😭
14. 假设后面来这边实习，面对工作安排，你会选择直接独立去做一个项目，还是前期先做一些基础性的工作？
15. 你认为策略产品经理的核心竞争力在哪儿?
16. 你在OPPO工作期间遇到过哪些挑战，当时是如何思考和解决的？
17. 介绍实习时自动化如何实现(基于什么框架和工具实现)
18. 继续预训练怎么做的？
19. cot微调数据怎么构造的？
20. llama的特点？
21. 为什么在参数高效微调中使用低秩矩阵分解？
22. 4．有没有全量微调过
23. 8．平常有用过 RLHF 吗，简单介绍一下
24. 怎么选取大模型sft的样本
25. 当相关文本库里有和用户查询相关的内容片段，如果提高检索召回率。
26. 当文本库中不存在相关内容片段，如何提升检索召回率
27. 介绍一下nlp中不同大小的模型
28. 基于llm的智能队友中，asr-&gt;意图识别-&gt;对话生成-&gt;tts，里面需要用的模型规模以及优化方法
29. grpo 在做大模训练时，一般用全参数微调还是 lora 微调？
30. 问小米那边的工作，encoder的预训练，怎样做拼接
31. 为什么不直接把tool调用的工具输出后放到prompt里给到LLM？
32. 面试官介绍：做Excel agent，deepresearch，AI搜的研究
33. 听说过MOE吗
34. 大模型答非所问怎么办
35. 有了解Qwen3的embedding和Reranker模型吗
36. 介绍GRPO、PPO、DPO，分别需要几个模型，需要训练的是哪些
37. 如何调用不同ai模型的api，如何进行选择
38. dpo 是在其他指标都优化的情况下漏检率上升在可接受范围内，当时的话你针对这个事情是怎么调整或者说去解决并落地的？
39. 8.介绍 groupembedding 。
40. 8. 在微调 Qwen 的时候，数据是怎么构造的
41. 3.为什么现在大模型能处理动辄一两万 token 的长序列信息？
42. 6.qwen2.5- omni 个qwen3- omni 的区别和不同？
43. 7.你关于大模型理解的看法。
44. deepseek r1的训练流程 和r0 的训练流程的区别。
45. 在做对齐的时候，为什么 SFT 之后还要做 RLHF，只用 SFT 可以吗
46. 看一下你的 AI 基础。介绍一下 transformer 基本原理？解释一下注意力机制？解释一下什么是扩散模型？
47. Agent和工作流有什么区别？
48. 对prompt工程的了解程度
49. LORA一般加到哪?rank设置有没有技巧
50. rankmixer中token的交互机制是怎样的？
51. ROPE在t维度是如何实现的？
52. 大模型的实现原理是什么
53. 视频生成模型的SFT微调经验是什么？
54. 在RAG实践中选择BGE作为嵌入模型的原因及FAISS索引的构建方法
55. 使用LangGraph框架与纯Prompt方法相比有哪些核心优势？
56. 当输入文本长度超出模型的上下文窗口时，有哪些主流的处理方案或模型架构来应对？
57. 哈希表的底层实现
58. 22、算法：力扣240 搜索二维矩阵 II
59. 一面问了论文和实习项目 题目是手写cross attention
60. 冒泡排序和选择排序的时间复杂度？
61. 哈希表的其他设计方案，除了使用数组+链表
62. 上来就问我这题要考我什么，我答策略模式。后面就是自己写，没写完，但是面试官很看重细节（边界判断，特殊情况......这些才是他要考察的点）
63. private和protected区别，如何访问私有变量，不要get和set怎么访问私有属性
64. dp和贪心的区别
65. 手撕:正则表达式匹配
66. 手撕代码:有序链表去重
67. 训练时候设置的最大轮次是多少
68. 机器学习的表格数据是什么样的？正负样本比例是多少？遇到了哪些困难？
69. 强化学习状态、动作、奖励如何设置？
70. 你的推荐项目里面提到了用了腾讯广告算法的 trick 去提升模型能力，具体是什么？
71. 有了解传统精排方法吗，比如LTR
72. 7.分层召回的结构是什么？
73. 推荐系统中常用的召回方法有哪些？
74. 如何将知识图谱融入推荐系统
75. MMOE的结构及其解决的问题
76. Wide&Deep模型的原理与应用场景
77. 项目中使用了LSTM？为什么使用它，不用Transformer？LSTM的不足和优势？
78. 训练的优化器一般用什么？ Adam 跟 SGD 的显存相比哪个占比更高？
79. 什么是归一化
80. 梯度下降是局部最优还是全局最优？
81. SGD随机梯度分类器原理
82. PD分离相比传统的部署方法有什么优势？
83. 并不是所有的模型都适合PD分离部署的方式，这块有了解吗
84. 之前实习用 DeepSpeed 微调过 Qwen2-72B，于是面试官问了 ZeRO-1，ZeRO-2，ZeRO-3 三个模式的区别
85. 了解A/B实验的统计指标吗，这个没答上来
86. Deepspeed的三阶段zero是什么
87. 项目性能测试关注哪些指标?
88. 2.你都读过哪些关于多模态的技术报告


## 荣耀
1. 4、softmax表达式，以及导数推导
2. 业务（视频图像去噪处理、语言图文多模态大模型等等，感觉和图像智能解译和下游任务没啥关系）
3. 面了15分钟以后面试官开始介绍了武汉这边的业务
4. 你是哪里人、为什么想来武汉等等。。。·深圳和武汉两边的业务区别
5. 面试官表现出不耐烦的态度


## 蚂蚁集团
1. 是否使用Verl框架进行RL？详细讲解Verl框架的训练流程，并说明配置文件中rollout_batchsize、global_batch_size、micro_batch_size_per_device_for_update、rollout.n等参数的关系及其对每张显卡上样本数的影响。
2. 除了大模型，你还有做其他 NLP 的项目吗？
3. 看起来大模型是你的长板啊，那你能讲讲你学习大模型的路线吗？
4. 介绍自己的中厂实习,从业务背景,困难,解决方法,自己的产出四个维度阐述
5. KV Cache的进化之路，详细讲
6. 核心代码模式，写一下大模型预测 token 时， beam 树如何构建，如何得到最终的结果（ pytorch 简单实现了一下，主要是还是讲明白）
7. 模型量化如何做的。 gptq , qat 等等，并说明为什么选择了w8a16的量化？
8. 写一下 ppo 算法的损失函数和 GAE 优势函数。主要还是讲明白
9. PEFT的几种微调方法及其区别和优缺点
10. 训练推理一致性领域中，强化学习、flash attention分块策略和vllm框架的page attention分块策略有哪些应用？
11. 业务做啥?垂领大模型构建,KG+LLM
12. LoRA 微调秩设置的是多少
13. 实现一个包含环检测功能的链表反转的代码，如果有环，返回nullptr，如果无环返回反转后的head node
14. 手撕题hot100,中等题,合并 k 个升序链表
15. 模型蒸馏主要的两种方式。硬标签和软标签。
16. 知识蒸馏的理解，出了几个场景问我怎么衡量蒸馏的好坏
17. 训练完验证使用的是什么数据集
18. 你在模型上线做 a b 实验有什么个人体会吗
19. 对其他分布式工具是否有所了解？


## 通用题库
1. 如何设计 Agent 的灰度发布策略？
2. 多工具多Prompt下，消融实验怎么展开？
3. LangChain、LlamaIndex和AutoGen这三个框架如何选择？
4. 大模型相关岗位的典型工作场景是怎样的?
5. 我的期望薪资是**月薪40K**. 我了解到行业内这个岗位应届生的平均水平在30K,我是985硕士,研究方向是多模态大模型,有两篇一作论文,还在某大厂实习过半年,负责过RAG系统的优化,所以我认为这个薪资是合理的.
6. 什么是Scaling Laws?它揭示了模型性能、计算量和数据量之间的什么关系?这对LLM的研发有什么指导意义?
7. 当一个 Agent 需要在真实或模拟环境中（如机器人、游戏）执行任务时，它与纯粹基于软件工具的 Agent 有什么本质区别？
8. 你是怎么设计agent的记忆系统？长期记忆如何存储？如果历史记录量非常大，怎么优化查询效率？
9. 实现 Agent 任务成功率统计
10. 实现一个完整的 Mini RAG 系统
11. 手撕MQA（Multi-Query Attention）
12. 手撕RoPE（旋转位置编码）
13. 如何优化 Agent 的规划效率？
14. 推导 Contrastive Loss（CLIP）的梯度
15. 如何实现 RAG 的增量索引更新？
16. 如何为特定任务构建高质量上下文（动态打包、向量索引、信息检索）？
17. 如何评价Agent解决问题的质量？
18. LLM的参数介绍(temp topk top p等)
19. LLaMA和GLM的区别,模型架构等方面
20. Qwen模型每个版本之间的改进点
21. 怎么构建SFT数据集,数据量多少,微调方式是什么
22. self-attention求内积时为啥除以根号d
23. 解决tokens不够的问题应该怎么办
24. gpt和llama的区别(模型结构上的)
25. Deepseek中蒸馏R1是什么？是否比从零RL训练更好？
26. 请详细解释一下 Transformer 模型中的自注意力机制是如何工作的?它为什么比 RNN 更适合处理长序列?
27. 请比较一下几种常见的 LLM 架构,例如 Encoder-Only, Decoder-Only, 和 Encoder-Decoder,并说明它们各自最擅长的任务类型。
28. 在LLM的推理阶段,有哪些常见的解码策略?请解释 Greedy Search, Beam Search, Top-K Sampling 和 Nucleus Sampling (Top-P) 的原理和优缺点。
29. 什么是词元化?请比较一下 BPE 和 WordPiece 这两种主流的子词切分算法。
30. "涌现能力"是大型模型中一个备受关注的现象,请问你如何理解这个概念?它通常在模型规模达到什么程度时出现?
31. 混合专家模型（MoE）是如何在不显著增加推理成本的情况下，有效扩大模型参数规模的？请简述其工作原理。
32. 在训练一个百或千亿参数级别的 LLM 时，你会面临哪些主要的工程和算法挑战？（例如：显存、通信、训练不稳定性等）
33. 最近读过哪些LLM比较前沿的论文，聊一下它的相关方法，针对什么问题，提出了什么方法，对比实验有哪些？
34. 什么是 instruction tuning？在多模态场景下如何做？
35. 介绍RAG流程;介绍对编码模型的了解、原理、优缺点;如何评估编码模型的能力
36. 介绍一些Agent的实现框架;这些框架有什么区别;LangGraph适用于什么场景;LangGraph构建Agent的方式有哪几种
37. Self-Attention和Cross-Attention中Q、K、V的来源有何不同？
38. SFT+DPO训练怎么组织这部分数据的?是自己构造还是用公开数据?
39. RAG中知识库搭建,对知识库的文件文档进行动态增量更新,怎么来避免新旧文档的分布不一致导致的检索偏差问题?
40. A2A框架和普通Agent框架的区别在哪,挑一个最关键的不同点说明
41. Agent的自我修正机制设计与优化
42. KL散度在RLHF中的作用及公式直观理解
43. 如何评估 Agent 的规划能力?
44. DeepSeek-V3有哪些技术特点或创新点？
45. 最近读过哪些Agent方向的论文？
46. Agent的并发控制实现方法
47. 大模型相关岗位的核心定义是什么？
48. 大模型相关岗位的判断标准有哪些？
49. 设计一个支持日均百万级查询的RAG系统
50. RAG有哪些分类;多模态RAG有哪些实现框架;伪多模态RAG和多模态RAG分别怎么实现,有什么区别;CLIP可以用于哪一类多模态RAG
51. 后训练有哪些方式;微调有哪些方式;LoRA原理及参数量
52. Transformer为什么使用多头Attention?
53. SFT的核心流程、数据集构建策略以及SFT后的Post-Training方法及其目的区别是什么？
54. 旋转位置编码为什么比绝对位置编码更好
55. 为什么大模型使用GQA（Group Query Attention）
56. SwiGLU激活函数的原理
57. 不同类型的Attention机制之间有什么区别？
58. 解释一下Prompt-tuning
59. LLaMA模型在训练过程中如何处理梯度消失和梯度爆炸的问题
60. OpenAI对齐为什么要用强化学习,别的方法不行吗?
61. SFT后会出现哪些问题
62. 分类任务可以用KL散度吗？
63. 推导 Temperature Scaling 对概率分布的影响


## OPPO
1. 3.ChatGPT对语音助手的冲击有哪些，会从哪些方面影响到现在的语音助手
2. 4.深挖个人项目，其中涉及到Bert，Chinese-Bert-WWM，Chinese-Roberta-wwm-ext的发展演变，其中Whole Word Masking (wwm)是怎么做的，了解预训练阶段的策略吗，介绍一下
3. 3. 从文本输入开始，给我讲一下 Transformer 的流程，不考虑多头的原因，self-attention中词向量不乘QKV参数矩阵，会有什么问题？QKV 矩阵怎么产生的，为何使用多头注意力机制？参数量会变大吗
4. 4. 讲讲推荐系统里有哪些注意力


## 其他
1. 10. 4.31 模型在SFT后会出现“复读机”情况该如何debug，以及出现的原因是什么？
2. 10. 4.17 介绍Lora及其变体的特点
3. 10. 4.19 讲讲工业界RAG具体如何优化？


## 哔哩哔哩
1. 7、是否了解DIN、SIM用于embedding
2. 8、从模型角度介绍特征交叉


## 拼多多
1. 10. 反问环节，说是做RAG的，不是那你连我的LLM实习经历也不问？八股也不问RAG？
2. 4. 问Transformer encoder decoder结构上的不同
3. 6. 后面确实问了PPO的优化目标。。。


## 滴滴
1. 10. 4.18 讲讲attention的各个变体


## 网易
1. 2.分类模型微调前如果比较确定，但sft后可能会把概率输出变得不那么确定了，你觉得是什么导致的
2. 5.为什么sft和rl在post-train中可能需要轮着来


## 美团
1. 3.新结构增加的参数量
2. 3.RAG链路的流程。如何评估rag的效果？有哪些指标？
3. 4.讲讲微调（全量和高效）。LoRA的原理。了解多少别的变种？
4. 5.Transformer八股。讲讲自注意力机制。了解什么位置编码方式？
5. 8.讲讲PPO和GRPO
6. 7.了解哪些强化学习算法？off-policy的举几个例子。
7. 6.激活函数和损失函数区别
8. 6.模型训练过程中出现部分节点失活的情况,数据应该怎么处理?


## 腾讯
1. 3.介绍MoE （混合专家）架构核心优势。
2. 4.阐述大模型训练与推理的完整流程。
3. 5. 对比 LORA 微调 Qwen 模型两种微调方式的性能表现。
4. 4.qwen2.5和qwen3之间有什么区别你了解吗？
5. 8.介绍 groupembedding 。
6. 8. 在微调 Qwen 的时候，数据是怎么构造的
7. 3.为什么现在大模型能处理动辄一两万 token 的长序列信息？
8. 6.qwen2.5- omni 个qwen3- omni 的区别和不同？
9. 7.你关于大模型理解的看法。
10. 22、算法：力扣240 搜索二维矩阵 II
11. 7.分层召回的结构是什么？
12. 2.你都读过哪些关于多模态的技术报告


## 荣耀
1. 4、softmax表达式，以及导数推导


## OPPO
1. 3.ChatGPT对语音助手的冲击有哪些，会从哪些方面影响到现在的语音助手
2. 4.深挖个人项目，其中涉及到Bert，Chinese-Bert-WWM，Chinese-Roberta-wwm-ext的发展演变，其中Whole Word Masking (wwm)是怎么做的，了解预训练阶段的策略吗，介绍一下
3. 3. 从文本输入开始，给我讲一下 Transformer 的流程，不考虑多头的原因，self-attention中词向量不乘QKV参数矩阵，会有什么问题？QKV 矩阵怎么产生的，为何使用多头注意力机制？参数量会变大吗
4. 4. 讲讲推荐系统里有哪些注意力


## 其他
1. 10. 4.31 模型在SFT后会出现“复读机”情况该如何debug，以及出现的原因是什么？
2. 10. 4.17 介绍Lora及其变体的特点
3. 10. 4.19 讲讲工业界RAG具体如何优化？


## 哔哩哔哩
1. 7、是否了解DIN、SIM用于embedding
2. 8、从模型角度介绍特征交叉


## 拼多多
1. 10. 反问环节，说是做RAG的，不是那你连我的LLM实习经历也不问？八股也不问RAG？
2. 4. 问Transformer encoder decoder结构上的不同
3. 6. 后面确实问了PPO的优化目标。。。


## 滴滴
1. 10. 4.18 讲讲attention的各个变体


## 网易
1. 2.分类模型微调前如果比较确定，但sft后可能会把概率输出变得不那么确定了，你觉得是什么导致的
2. 5.为什么sft和rl在post-train中可能需要轮着来


## 美团
1. 3.新结构增加的参数量
2. 3.RAG链路的流程。如何评估rag的效果？有哪些指标？
3. 4.讲讲微调（全量和高效）。LoRA的原理。了解多少别的变种？
4. 5.Transformer八股。讲讲自注意力机制。了解什么位置编码方式？
5. 8.讲讲PPO和GRPO
6. 7.了解哪些强化学习算法？off-policy的举几个例子。
7. 6.激活函数和损失函数区别
8. 6.模型训练过程中出现部分节点失活的情况,数据应该怎么处理?


## 腾讯
1. 3.介绍MoE （混合专家）架构核心优势。
2. 4.阐述大模型训练与推理的完整流程。
3. 5. 对比 LORA 微调 Qwen 模型两种微调方式的性能表现。
4. 4.qwen2.5和qwen3之间有什么区别你了解吗？
5. 8.介绍 groupembedding 。
6. 8. 在微调 Qwen 的时候，数据是怎么构造的
7. 3.为什么现在大模型能处理动辄一两万 token 的长序列信息？
8. 6.qwen2.5- omni 个qwen3- omni 的区别和不同？
9. 7.你关于大模型理解的看法。
10. 22、算法：力扣240 搜索二维矩阵 II
11. 7.分层召回的结构是什么？
12. 2.你都读过哪些关于多模态的技术报告


## 荣耀
1. 4、softmax表达式，以及导数推导


## OPPO
1. 3.ChatGPT对语音助手的冲击有哪些，会从哪些方面影响到现在的语音助手
2. 4.深挖个人项目，其中涉及到Bert，Chinese-Bert-WWM，Chinese-Roberta-wwm-ext的发展演变，其中Whole Word Masking (wwm)是怎么做的，了解预训练阶段的策略吗，介绍一下
3. 3. 从文本输入开始，给我讲一下 Transformer 的流程，不考虑多头的原因，self-attention中词向量不乘QKV参数矩阵，会有什么问题？QKV 矩阵怎么产生的，为何使用多头注意力机制？参数量会变大吗
4. 4. 讲讲推荐系统里有哪些注意力


## 其他
1. 10. 4.31 模型在SFT后会出现“复读机”情况该如何debug，以及出现的原因是什么？
2. 10. 4.17 介绍Lora及其变体的特点
3. 10. 4.19 讲讲工业界RAG具体如何优化？


## 哔哩哔哩
1. 7、是否了解DIN、SIM用于embedding
2. 8、从模型角度介绍特征交叉


## 拼多多
1. 10. 反问环节，说是做RAG的，不是那你连我的LLM实习经历也不问？八股也不问RAG？
2. 4. 问Transformer encoder decoder结构上的不同
3. 6. 后面确实问了PPO的优化目标。。。


## 滴滴
1. 10. 4.18 讲讲attention的各个变体


## 网易
1. 2.分类模型微调前如果比较确定，但sft后可能会把概率输出变得不那么确定了，你觉得是什么导致的
2. 5.为什么sft和rl在post-train中可能需要轮着来


## 美团
1. 3.新结构增加的参数量
2. 3.RAG链路的流程。如何评估rag的效果？有哪些指标？
3. 4.讲讲微调（全量和高效）。LoRA的原理。了解多少别的变种？
4. 5.Transformer八股。讲讲自注意力机制。了解什么位置编码方式？
5. 8.讲讲PPO和GRPO
6. 7.了解哪些强化学习算法？off-policy的举几个例子。
7. 6.激活函数和损失函数区别
8. 6.模型训练过程中出现部分节点失活的情况,数据应该怎么处理?


## 腾讯
1. 3.介绍MoE （混合专家）架构核心优势。
2. 4.阐述大模型训练与推理的完整流程。
3. 5. 对比 LORA 微调 Qwen 模型两种微调方式的性能表现。
4. 4.qwen2.5和qwen3之间有什么区别你了解吗？
5. 8.介绍 groupembedding 。
6. 8. 在微调 Qwen 的时候，数据是怎么构造的
7. 3.为什么现在大模型能处理动辄一两万 token 的长序列信息？
8. 6.qwen2.5- omni 个qwen3- omni 的区别和不同？
9. 7.你关于大模型理解的看法。
10. 22、算法：力扣240 搜索二维矩阵 II
11. 7.分层召回的结构是什么？
12. 2.你都读过哪些关于多模态的技术报告


## 荣耀
1. 4、softmax表达式，以及导数推导
