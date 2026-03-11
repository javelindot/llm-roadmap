<nav style="background-color: #2c3e50; color: white; padding: 10px 0; margin-bottom: 20px; border-radius: 8px;">
  <ul style="list-style: none; padding: 0; margin: 0; display: flex; justify-content: center; flex-wrap: wrap;">
    <li style="margin: 0 15px; margin-bottom: 0;"><a href="../../" style="color: white; font-weight: 500; text-decoration: none; padding: 5px 10px; border-radius: 4px; transition: background-color 0.3s ease;">首页</a></li>
    <li style="margin: 0 15px; margin-bottom: 0;"><a href="../../base/" style="color: white; font-weight: 500; text-decoration: none; padding: 5px 10px; border-radius: 4px; transition: background-color 0.3s ease;">数学基础</a></li>
    <li style="margin: 0 15px; margin-bottom: 0;"><a href="../../ml/" style="color: white; font-weight: 500; text-decoration: none; padding: 5px 10px; border-radius: 4px; transition: background-color 0.3s ease;">机器学习</a></li>
    <li style="margin: 0 15px; margin-bottom: 0;"><a href="../" style="color: white; font-weight: 500; text-decoration: none; padding: 5px 10px; border-radius: 4px; transition: background-color 0.3s ease;">自然语言处理</a></li>
  </ul>
</nav>

## 2.1 概述
**文本表示**是将自然语言转化为计算机能够理解的数值形式，是绝大多数自然语言处理（NLP）任务的基础步骤。

早期的文本表示方法（如**词袋模型**）通常将整段文本编码为一个向量。这类方法实现简单、计算高效，但存在明显的局限性——表达语序和上下文语义的能力较弱。因此，现代 NLP 技术逐渐引入更加精细和表达力更强的文本表示方法，以更有效地建模语言的结构和含义。

文本表示的第一步通常是**分词**和**词表构建**，如下图所示：

<!-- 这是一张图片，ocr 内容为： -->
![](images/image_1772902934293_264933843.png)

+ **分词（Tokenization）** 是将原始文本切分为若干具有独立语义的最小单元（即token）的过程，是所有 NLP 任务的起点。
+ **词表（Vocabulary）** 是由语料库构建出的、包含模型可识别 token 的集合。词表中每个token都分配有唯一的 ID，并支持 token 与 ID 之间的双向映射。

在后续训练或预测过程中，模型会首先对输入文本进行分词，再通过词表将每个 token 映射为其对应的 ID。接着，这些 ID 会被输入嵌入层（Embedding Layer），转换为低维稠密的向量表示（即词向量），如下图所示。

<!-- 这是一张图片，ocr 内容为： -->
![](images/image_1772902934293_527914532.png)

此外，在文本生成任务中，模型的输出层会针对词表中的每个 token 生成一个概率分布，表示其作为下一个词的可能性。系统通常选取具有最大概率的ID，并通过词表查找对应的 token，从而逐步生成最终的输出文本。

## 2.2 分词
不同语言由于语言结构、词边界的差异，其分词策略和算法也不尽相同，本节将分别介绍英文与中文中常见的分词方式。

### 2.2.1 英文分词
按照分词粒度的大小，可分为词级（Word-Level）分词、字符级（Character-Level）分词和子词级（Subword-Level）分词。下面逐一介绍。

#### 词级分词
词级分词是指将文本按词语进行切分，是最传统、最直观的分词方式。在英文中，空格和标点往往是天然的分隔符。

<!-- 这是一张图片，ocr 内容为： -->
![](images/image_1772902934293_52945588.png)

词级分词虽便于理解和实现，但在实际应用中容易出现 **OOV（Out-Of-Vocabulary，未登录词）** 问题。所谓 OOV，是指在模型使用阶段，输入文本中出现了不在预先构建词表中的词语，常见的包括网络热词、专有名词、复合词及拼写变体等。由于模型无法识别这些词，通常会将其统一替换为特殊标记（如 `<UNK>`），从而导致语义信息的丢失，影响模型的理解与预测能力。

#### 字符级分词
字符级分词（Character-level Tokenization）是以单个字符为最小单位进行分词的方法，文本中的每一个字母、数字、标点甚至空格，都会被视作一个独立的 token。

<!-- 这是一张图片，ocr 内容为： -->
![](images/image_1772902934294_733724260.png)

在这种分词方式下，词表仅由所有可能出现的字符组成，因此词表规模非常小，覆盖率极高，几乎不存在 OOV 问题。无论输入中出现什么样的新词或拼写变体，只要字符在词表中，都能被表示出来。

然而，由于单个字符本身语义信息极弱，模型必须依赖更长的上下文来推断词义和结构，这显著增加了建模难度和训练成本。此外，输入序列也会变得更长，影响模型效率。

#### 子词级分词
子词级分词是一种介于词级分词与字符级分词之间的分词方法，它将词语切分为更小的单元——子词（subword），例如词根、前缀、后缀或常见词片段。与词级分词相比，子词分词可以显著缓解OOV问题；与字符级分词相比，它能更好地保留一定的语义结构。

子词分词的基本思想是：即使一个完整的词没有出现在词表中，只要它可以被拆分为词表中存在的子词单元，就可以被模型识别和表示，从而避免整体被替换为`<UNK>`。

<!-- 这是一张图片，ocr 内容为： -->
![](images/image_1772902934294_668556704.png)

常见的子词分词算法包括 **BPE（Byte Pair Encoding）**、**WordPiece** 和 **Unigram Language Model**。

其中，BPE 是最早被广泛应用的方法，其需要先从语料中学习一个子词词表，基本原理是：首先将所有词语拆分为单个字符，然后迭代地统计语料中出现频率最高的字符对，将其合并为一个新的子词，并加入词表。该过程持续进行，直到达到设定的词表大小。

然后再根据词表对新输入的文本进行分词，其基本原理是：从输入文本的第一个字符开始，优先选择词表中能够匹配的**最长子词单元**，然后继续处理剩余部分，直到完成整个序列的切分。

子词级分词已经成为现代英文 NLP 模型中的主流方法，如 BERT、GPT等模型均采用了基于子词的分词机制。

### 2.2.2 中文分词
尽管中文的语言结构与英文存在显著差异，我们仍可以借助"分词粒度"的视角，对中文的分词方式进行归类和分析。

#### 字符级分词
字符级分词是中文处理中最简单的一种方式，即将文本按照单个汉字进行切分，文本中的每一个汉字都被视为一个独立的 token。

<!-- 这是一张图片，ocr 内容为： -->
![](images/image_1772902934294_834327194.png)

由于汉字本身通常具有独立语义，因此字符级分词在中文中具备天然的可行性。相比英文中的字符分词，中文的字符分词更加"语义友好"。

#### 词级分词
词级分词是将中文文本按照完整词语进行切分的传统方法，切分结果更贴近人类阅读习惯。

<!-- 这是一张图片，ocr 内容为： -->
![](images/image_1772902934295_414143214.png)

由于中文没有空格等天然词边界，词级分词通常依赖词典、规则或模型来识别词语边界。

#### 子词级分词
虽然中文没有英文中的子词结构（如前缀、后缀、词根等），但子词分词算法（如 BPE）**仍可直接应用于中文**。它们以汉字为基本单位，通过学习语料中高频的字组合（如"自然"、"语言"、"处理"），自动构建子词词表。这种方式无需人工词典，具有较强的适应能力。

在当前主流的中文大模型（如通义千问、DeepSeek）中，子词分词已成为广泛采用的文本切分策略。

### 2.2.3 分词工具
#### 概述
目前市面上可用于中文分词的工具种类繁多，按照实现方式大致可以分为如下两类：

+ 一类是基于**词典或模型**的传统方法，主要以"词"为单位进行切分；
+ 另一类是基于**子词建模算法**（如BPE）的方式，从数据中自动学习高频字组合，构建子词词表。

前者的代表工具包括 [jieba](https://github.com/fxsjy/jieba)、[HanLP](https://github.com/hankcs/HanLP)等，这些工具广泛应用于传统 NLP 任务中。

后者的代表工具包括 [Hugging Face Tokenizer](https://github.com/huggingface/tokenizers)、[SentencePiece](https://github.com/google/sentencepiece)、[tiktoken](https://github.com/openai/tiktoken)等，常用于大规模预训练语言模型中。

#### jieba分词器
##### 概述
jieba 是中文分词领域中应用广泛的开源工具之一，具有接口简洁、模式灵活、词典可扩展等特点，在各类传统 NLP 任务中依然具备良好的实用价值。

##### 安装
```bash
pip install jieba
```

##### 分词模式
jieba分词器提供了多种分词模式，以适应不同的应用场景。

**精确模式（默认）**

试图将句子最精确地切开，适合文本分析。分词效果如下：

```plain
小明毕业于北京大学计算机系
↓
[小明|毕业|于|北京大学|计算机系]
```

精确模式分词可使用`jieba.cut`或者`jieba.lcut`方法，前者返回一个生成器对象，后者返回一个list。具体代码如下：

```python
import jieba

text = "小明毕业于北京大学计算机系"

words_generator = jieba.cut(text)  # 返回一个生成器
for word in words_generator:
    print(word)

words_list = jieba.lcut(text)  # 返回一个列表
print(words_list)
```

**全模式**

把句子中所有的可以成词的词语都扫描出来，分词效果如下：

```plain
小明毕业于北京大学计算机系
↓
[小|明|毕业|于|北京|北京大学|大学|计算|计算机|计算机系|算机|系]
```

全模式分词可使用`jieba.cut`或者`jieba.lcut`，并将`cut_all`参数设置为True，具体代码如下：

```python
import jieba

text = "小明毕业于北京大学计算机系"

words_generator = jieba.cut(text, cut_all=True)  # 返回一个生成器
for word in words_generator:
    print(word)

words_list = jieba.lcut(text, cut_all=True)  # 返回一个列表
print(words_list)
```

**搜索引擎模式**

在精确模式基础上，对长词进一步切分，适合用于搜索引擎分词，分词效果如下：

```plain
小明毕业于北京大学计算机系
↓
[小明|毕业|于|北京|大学|北京大学|计算|算机|计算机|计算机系]
```

可使用`jieba.cut_for_search`或者`jieba.lcut_for_search`，具体代码如下：

```python
import jieba

text = "小明毕业于北京大学计算机系"

words_generator = jieba.cut_for_search(text)  # 返回一个生成器
for word in words_generator:
    print(word)

words_list = jieba.lcut_for_search(text)  # 返回一个列表
print(words_list)
```

**自定义词典**

jieba支持用户自定义词典，以便包含 jieba 词库里没有的词，用于增强特定领域词汇的识别能力。

自定义词典的格式为：一个词占一行，每一行分三部分：词语、词频（可省略，词频决定某个词在分词时的优先级。词频越高被优先切分出来的概率越大）、词性标签（可省略，不影响分词结果），用空格隔开，顺序不可颠倒。例如：

```plain
云计算
云原生 5
大模型 10 n
```

可使用`jieba.load_userdict(file_name)`加载词典文件，也可以使用`jieba.add_word(word, freq=None, tag=None)`与`jieba.del_word(word)`动态修改词典。

```python
import jieba

jieba.load_userdict('dict.txt')

words_list = jieba.lcut("随着云计算技术的普及，越来越多企业开始采用云原生架构来部署服务，并借助大模型能力提升智能化水平，实现业务流程的自动化与智能决策。")
print(words_list)
```

## 2.3 词表示
### 2.3.1 概述
在分词完成之后，文本被转换为一系列的 token（词、子词或字符）。然而，这些符号本身对计算机而言是不可计算的。因此，为了让模型能够理解和处理文本，必须将这些 token 转换为计算机可以识别和操作的数值形式，这一步就是所谓的**词表示（word representation）**。

词表示的发展经历了从稀疏的**one-hot编码**，到稠密的**语义化词向量**，再到近年来的**上下文相关的词表示**。不同的词表示方法在表达能力、语义建模、上下文适应性等方面存在显著差异。

### 2.3.2 One-hot编码
最早期的词向量表示方式是 **One-hot 编码**：它将词汇表中的每个词映射为一个稀疏向量，向量的长度等于整个词表的大小。该词在对应的位置为 1，其他位置为 0。

<!-- 这是一张图片，ocr 内容为： -->
![](images/image_1772902934295_553008103.png)

one-hot 虽然实现简单、直观易懂，但它无法体现词与词之间的语义关系，且随着词表规模的扩大，向量维度会迅速膨胀，导致计算效率低下。因此，在实际自然语言处理任务中，one-hot 表示已经很少被直接使用。

### 2.3.3 语义化词向量
传统的one-hot表示虽然结构简单，但它无法反映词语之间的语义关系，也无法衡量词与词之间的相似度。为了解决这个问题，研究者提出了**Word2Vec**模型，它通过对大规模语料的学习，为每个词生成一个具有语义意义的**稠密向量**表示。这些向量能够在连续空间中表达词与词之间的关系，使得"意思相近"的词在空间中距离更近。

<!-- 这是一张图片，ocr 内容为： -->
![](images/image_1772902934295_806000133.png)

#### Word2Vec概述
Word2Vec的设计理念源自"**分布假设**"——即**一个词的含义由它周围的词决定**。

<!-- 这是一张图片，ocr 内容为： -->
![](images/image_1772902934295_857039642.png)

基于这一假设，Word2Vec构建了一个简洁的神经网络模型，通过学习词与上下文之间的关系，自动为每个词生成一个能够反映语义特征的向量表示。

Word2Vec提供了两种典型的模型结构，用于实现对词向量的学习：

+ **CBOW（Continuous Bag-of-Words）模型**输入是一个词的上下文（即前后若干个词），模型的目标是预测中间的目标词。<!-- 这是一张图片，ocr 内容为： -->
![](images/image_1772902934296_861548995.png)
+ **Skip-gram 模型**输入是一个中心词，模型的目标是预测其上下文中的所有词（即前后若干个词）。<!-- 这是一张图片，ocr 内容为： -->
![](images/image_1772902934296_256564888.png)

只要按照上述目标训练模型，就能得到语义化的词向量。

#### Word2Vec原理
##### 数据集
Word2Vec 不依赖人工标注，而是直接利用大规模原始文本（如书籍、新闻、网页等）作为数据源，从中自动构造训练样本。

由于两种模型的输入和输出都是词语，因此首先需要对原始文本进行分词，将连续文本转换为 token 序列。

此外，模型无法直接处理文本符号，训练时仍需将词语转换为 one-hot 编码，以便作为模型的输入和输出进行计算。

<!-- 这是一张图片，ocr 内容为： -->
![](images/image_1772902934296_689572832.png)

##### Skip-Gram
**训练数据集**

Skip-Gram的目标是根据中间词预测上下文，所以其训练样本为：

<!-- 这是一张图片，ocr 内容为： -->
![](images/image_1772902934297_695924432.png)

**模型结构**

Skip-Gram模型结构如下图所示：

<!-- 这是一张图片，ocr 内容为： -->
![](images/image_1772902934297_171088953.png)

Skip-Gram模型损失值的计算图如下图所示：

<!-- 这是一张图片，ocr 内容为： -->
![](images/image_1772902934297_251725656.png)

**前向传播过程如下：**

1. **输入中心词（地铁）**"地铁"用 one-hot 向量表示
2. **查找词向量**与参数矩阵相乘，取出"地铁"对应的词向量。（实际上就是词向量矩阵，每一行表示一个词的向量）
3. **预测上下文**将中心词向量与参数矩阵相乘，得到对整个词表的预测得分。
4. **Softmax 输出**得分通过 Softmax 转为概率分布，表示各词作为上下文的可能性。
5. **计算损失**与真实上下文词"乘坐"、"上班"进行比对，计算交叉熵损失并求和，得到总损失。

之后在进行反向传播时，参数矩阵中的"地铁"对应的词向量就会被更新，模型通过这个过程不断的进行学习，最终便能得到具有语义的词向量。

##### CBOW
**训练样本**

CBOW的目标是根据上下文预测中间词，所以其训练样本为：

<!-- 这是一张图片，ocr 内容为： -->
![](images/image_1772902934298_848117196.png)

**模型结构**

CBOW模型的结构如下图所示：

<!-- 这是一张图片，ocr 内容为： -->
![](images/image_1772902934298_492129075.png)

CBOW模型损失值的计算图如下图所示：

<!-- 这是一张图片，ocr 内容为： -->
![](images/image_1772902934298_328542226.png)

**CBOW 模型的前向传播过程如下：**

1. **输入上下文词（乘坐、上班）**每个词用 one-hot 向量表示。
2. **查找词向量**每个 one-hot 向量与参数矩阵相乘，查出对应的词向量。
3. **平均上下文向量**将多个上下文词向量取平均，得到一个整体的上下文表示。
4. **预测中心词**将平均后的上下文向量与参数矩阵相乘，得到对整个词表的预测得分。
5. **Softmax 输出**将得分输入Softmax，得到每个词作为中心词的概率分布。
6. **计算损失**将预测结果与真实中心词"地铁"的one-hot向量进行比对，计算交叉熵损失。

之后在进行反向传播时，参数矩阵中"乘坐"和"上班"对应的词向量就会被更新。模型通过不断训练，逐步优化这些向量，最终便能得到具有语义的词向量。

#### 获取Word2Vec词向量
词向量的获取通常有两种方式：一种是直接使用他人公开发布的词向量，另一种是在特定语料上自行训练。

在实际工作中，无论是加载已有模型还是从零训练，都可借助[Gensim](https://radimrehurek.com/gensim/)来完成，它提供了便捷的接口来加载 Word2Vec 格式的词向量，也支持基于自有语料训练属于自己的词向量模型。

可执行以下命令安装Gensim：

```bash
pip install gensim
```

##### 使用公开词向量
公开的中文词向量，可从[https://github.com/Embedding/Chinese-Word-Vectors](https://github.com/Embedding/Chinese-Word-Vectors)下载，其提供了基于多个数据集训练得到的词向量。

词向量文件的格式为：第一行记录基本信息，包括两个整数，分别表示总词数和词向量维度。从第二行起，每一行表示一个词及其对应的词向量，格式为：词 + 向量的各个维度值。所有内容通过空格分隔，该格式已成为自然语言处理领域中广泛接受的约定俗成的通用格式。具体格式如下：

```plain
<词汇总数> <向量维度>
word1 val11 val12 ... val1N
word2 val21 val22 ... val2N
...
```

可使用`KeyedVectors.load_word2vec_format()`加载上述词向量文件，具体代码如下：

```python
from gensim.models import KeyedVectors

model_path = 'sgns.weibo.word.bz2'
model = KeyedVectors.load_word2vec_format(model_path)
```

词向量加载完后，便可使用如下API查询词向量：

```python
# 查看词向量维度
print(model.vector_size)

# 查看某个词的向量
print(model['地铁'])

# 查看两个向量的相似度
similarity = model.similarity('地铁', '公交')
print('地铁 vs 公交 相似度：', similarity)
```

`model.similarity`计算的是两个词向量的余弦相似度，计算公式如下：

```plain
similarity = cos(θ) = (A · B) / (|A| × |B|)
```

返回值介于[-1,1]。接近1表示高度相似，语义接近；接近0表示无明显相关；接近-1表示方向完全相反，极度不相似。

```python
# 找出与某个词最相似的词
similar_words = model.most_similar(positive=["上班"], topn=5)
print(similar_words)

# 词语类比推理
result = model.most_similar(positive=["爸爸", "女性"], negative=["男性"], topn=3)
print(result)
```

##### 自行训练词向量
**准备语料**

Word2Vec的训练语料需要是已分词的文本序列，格式为：

```python
sentences = [
    ['我', '每天', '乘坐', '地铁', '上班'],
    ['我', '每天', '乘坐', '公交', '上班']
]
```

**训练模型**

gensim提供了十分方便的训练词向量的API——Word2Vec：

```python
from gensim.models import Word2Vec

model = Word2Vec(
    sentences,           # 已分词的句子序列
    vector_size=100,     # 词向量维度
    window=5,            # 上下文窗口大小
    min_count=2,         # 最小词频（低于将被忽略）
    sg=1,                # 1:Skip-Gram，0:CBOW
    workers=4            # 并行训练线程数
)
```

**保存词向量**

```python
model.wv.save_word2vec_format('my_vectors.kv')
```

**加载词向量**

```python
from gensim.models import KeyedVectors
my_model = KeyedVectors.load_word2vec_format('my_vectors.kv')
```

##### 应用Word2Vec词向量
将训练好的词向量应用于PyTorch框架的神经网络中，示例代码如下：

```python
import torch
import torch.nn as nn

# 1. 加载词向量
model = KeyedVectors.load_word2vec_format('my_vectors.kv')

# 2. 构建词表和词向量矩阵
word2index = {word: idx for idx, word in enumerate(model.key_to_index.keys())}
num_embeddings = len(word2index)
embedding_dim = model.vector_size

embedding_matrix = torch.zeros(num_embeddings, embedding_dim)  # 构造词向量矩阵,形状为(词表大小, 词向量维度大小)
for word, idx in word2index.items():
    embedding_matrix[idx] = torch.tensor(model[word])

# 3. 构建 PyTorch 的嵌入层
embedding_layer = nn.Embedding.from_pretrained(
    embedding_matrix,  # 词向量矩阵，形状为(num_embeddings, embedding_dim)
    freeze=False        # 是否冻结词向量
)

# 4. 示例：将词索引转换为向量
input_words = ["我", "喜欢", "乘坐", "地铁"]  # 分词后的句子
input_indices = [word2index[word] for word in input_words]  # token转为索引
input_tensor = torch.tensor([input_indices])  # 构造嵌入层输入张量

# 5. 查询嵌入（即词向量查找）
output = embedding_layer(input_tensor)  # 通过嵌入层查找预训练词向量
print(output.shape)  # 例如 torch.Size([1, 4, 100])
```

### 2.3.4 上下文相关词表示（ELMo）
虽然像Word2Vec这样的模型已经能够为词语提供具有语义的向量表示，但是它只为每个词分配一个**固定的向量表示**，不论它在句中出现的语境如何。这种表示被称为**静态词向量（static embeddings）**。

然而，语言的表达极其灵活，一个词在不同上下文中可能有完全不同的含义。例如：

<!-- 这是一张图片，ocr 内容为： -->
![](images/image_1772902934299_635535186.png)

这时，使用同一个静态词向量去表示"苹果"，显然无法区分这两种语义。这就推动了上下文相关的词表示的发展。

**上下文相关词表示（Contextual Word Representations）**，是指词语的向量表示会根据它所在的句子上下文动态变化，从而更好地捕捉其语义。一个具有代表性的模型是——[ELMo](https://arxiv.org/abs/1802.05365)。

该模型全称为 Embeddings from Language Models，发表于2018年2月。其基于LSTM 语言模型，使用上下文**动态**生成每个词的表示，每个词的向量由其前文和后文共同决定，是第一个被广泛应用于下游任务的上下文词向量模型。

<!-- 这是一张图片，ocr 内容为： -->
![](images/image_1772902934299_833102243.png)

