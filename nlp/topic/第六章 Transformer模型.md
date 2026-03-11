# Transformer模型
## 6.1 概述
此前的Seq2Seq模型通过注意力机制取得了一定提升，但由于整体结构仍依赖 RNN，依然存在计算效率低、难以建模长距离依赖等结构性限制。

为了解决这些问题，Google在2017 年发表一篇论文《[Attention Is All You Need](https://arxiv.org/pdf/1706.03762)》，提出了一种全新的模型架构——**Transformer**。该模型完全摒弃了 RNN 结构，转而使用注意力机制直接建模序列中各位置之间的关系。通过这种方式，Transformer不仅显著提升了训练效率，也增强了模型对长距离依赖的建模能力。

<!-- 这是一张图片，ocr 内容为： -->
![](images/image_1772902934690_397602194.png)

Transformer 的提出对自然语言处理产生了深远影响。在机器翻译任务中，它首次超越了 RNN 模型的表现，并成为后续各类预训练语言模型的基础框架，如 BERT、GPT 等。这些模型推动 NLP 进入了"预训练 + 微调"的新时代，极大地提升了模型在多种任务上的通用性与性能。如今，Transformer 架构不仅广泛应用于 NLP，还扩展至语音识别、图像处理、代码生成等多个领域，成为现代深度学习中最具代表性的通用模型之一。

## 6.2 模型结构详解
### 6.2.1 核心思想
在 Seq2Seq 模型中，注意力机制的引入显著增强了模型的表达能力。它允许解码器在生成每一个目标词时，根据当前解码状态动态选择源序列中最相关的位置，并据此融合信息。这一机制有效缓解了将整句信息压缩为固定向量所带来的信息瓶颈，显著提升了翻译等任务中的建模效果。

进一步分析可以发现，注意力机制不仅是信息提取的工具，其本质是在每一个目标位置上，显式建模该位置与源序列中各位置之间的依赖关系。

与此同时，循环神经网络（RNN）作为 Seq2Seq 模型的核心结构，其作用也在于建模序列中的依赖关系。通过隐藏状态的递归传递，RNN 使当前位置的表示能够整合前文信息，从而隐式捕捉上下文依赖。从功能角度看，RNN 与注意力机制完成的是同一类任务：建立序列中不同位置之间的依赖联系。

既然注意力机制也具备建模依赖关系的能力，那么理论上，它就可以在功能上替代 RNN。

此外，相比 RNN，注意力机制在结构上具备明显优势：无需顺序计算，便于并行处理；任意位置间可直接建立联系，更适合捕捉长距离依赖。因此，它不仅具备替代的可能，也在效率与效果上表现更优。

既然如此，是否可以将 Seq2Seq 中的 RNN 结构全部替换为注意力机制？

<!-- 这是一张图片，ocr 内容为： -->
![](images/image_1772902934691_490971913.png)

**Transformer 模型正是在这一思路下诞生的**。它摒弃了传统的递归结构，仅依靠注意力机制完成输入序列和输出序列中所有位置之间的依赖建模任务。这一结构上的彻底变革，也正是论文标题 Attention is All You Need 所体现的核心理念。

### 6.2.2 整体结构
Transformer 的整体结构延续了 Seq2Seq 模型中 "编码器-解码器" 的设计理念，其中，**编码器（Encoder）**负责对输入序列进行理解和表示，而**解码器（Decoder）**则根据编码器的输出逐步生成目标序列。

与基于 RNN 的 Seq2Seq 模型一样，Transformer 的解码器采用自回归方式生成目标序列。不同之处在于，每一步的输入是此前已生成的全部词，模型会输出一个与输入长度相同的序列，但我们只取最后一个位置的结果作为当前预测。这个过程不断重复，直到生成结束标记 `<eos>`。

<!-- 这是一张图片，ocr 内容为： -->
![](images/image_1772902934691_45645008.png)

此外，Transformer 的编码器和解码器模块分别由多个结构相同的层堆叠而成。通过层层堆叠，模型能够逐步提取更深层次的语义特征，从而增强对复杂语言现象的建模能力。标准的 Transformer 模型通常包含 **6个编码器层**和**6个解码器层**。

<!-- 这是一张图片，ocr 内容为： -->
![](images/image_1772902934692_253676202.png)

## 6.3 编码器
### 6.3.1 概述
Transformer 的编码器用于**理解输入序列的语义信息，并生成每个token的上下文表示**，为解码器生成目标序列提供基础。

<!-- 这是一张图片，ocr 内容为： -->
![](images/image_1772902934693_580472454.png)

编码器由多个结构相同的**编码器层（Encoder Layer）**堆叠而成。

<!-- 这是一张图片，ocr 内容为： -->
![](images/image_1772902934693_355266995.png)

每个 Encoder Layer的主要任务都是对其输入序列进行上下文建模，使每个位置的表示都能融合来自整个序列的全局信息。每个 Encoder Layer都包含两个子层（sublayer），分别是**自注意力子层（Self-Attention Sublayer）****和****前馈神经网络子层（Feed-Forward Sublayer）**。

<!-- 这是一张图片，ocr 内容为： -->
![](images/image_1772902934694_9958482.png)

各层作用如下：

+ **Self-Attention**：用于捕捉序列中各位置之间的依赖关系。
+ **Feed-Forward**：用于对每个位置的表示进行非线性变换，从而提升模型的表达能力。

#### 自注意力层
自注意力机制（Self-Attention）是 Transformer 编码器的核心结构之一，它的作用是在序列内部建立各位置之间的依赖关系，使模型能够为每个位置生成融合全局信息的表示。

<!-- 这是一张图片，ocr 内容为： -->
![](images/image_1772902934694_191157390.png)

之所以被称为"自"注意力，是因为模型在计算每个位置的表示时，所参考的信息全部来自同一个输入序列本身，而不是来自另一个序列。

##### 自注意力计算过程
自注意力的完整计算过程如下：

**生成Query、Key、Value向量**

自注意力机制的第一步，是将输入序列中的每个位置表示映射为三个不同的向量，分别是 **查询（Query）**、**键（Key）** 和 **值（Value）**。

<!-- 这是一张图片，ocr 内容为： -->
![](images/image_1772902934694_588349181.png)

这些向量的作用如下：

+ **Query**：表示当前词的用于发起注意力匹配的向量；
+ **Key**：表示序列中每个位置的内容标识，用于与 Query 进行匹配；
+ **Value**：表示该位置携带的信息，用于加权汇总得到新的表示。

自注意力的核心思想是：每个位置用自身的 Query 向量，与整个序列中所有位置的 Key 向量进行相关性计算，从而得到注意力权重，并据此对对应的 Value 向量加权汇总，形成新的表示。

**计算位置间相关性**

完成 Query、Key、Value 向量的生成后，模型会使用每个位置的 Query 向量与所有位置的 Key 向量进行相关性评分。

<!-- 这是一张图片，ocr 内容为： -->
![](images/image_1772902934695_83940466.png)

评分函数采用向量点积形式。由于在高维空间中，点积的数值可能过大，会影响 softmax 的稳定性，因此在实际计算中对结果进行了缩放。最终的评分函数为：

$ \text{score}(Q, K) = \frac{Q \cdot K^T}{\sqrt{d_k}} $

其中 $ d_k $ 是key向量的维度，用于缩放点积的幅度。这个分数越大，表示第 i 个位置越应该关注第 j 个位置的信息。

**计算注意力权重**

在得到每个位置与所有位置之间的相关性评分后，模型会使用 softmax 函数进行归一化，确保每个位置对所有位置的关注程度之和为 1，从而形成一个有效的加权分布。

**加权汇总生成输出**

最后，模型会根据注意力权重对所有位置的 Value 向量进行加权求和，得到每个位置融合全局信息后的新表示。

综上所述，可得整个自注意力机制的完整的计算公式如下：

$ \text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V $

##### 多头自注意力计算过程
自注意力机制通过 Query、Key 和 Value 向量计算每个位置与其他位置之间的依赖关系，使模型能够有效捕捉序列中的全局信息。

然而，自然语言本身具有高度的语义复杂性，一个句子往往同时包含多种类型的语义关系。例如，句子"那只动物没有过马路，因为它太累了"中就涉及多个层面的语言关系：

+ "它"指代"那只动物"，属于跨句的代指关系；
+ "因为"连接前后两个分句，体现语义上的因果逻辑；
+ "过马路"构成动词短语，属于固定的动宾结构。

要准确理解这类句子，模型需要同时识别并建模多种层次和类型的依赖关系。但这些信息很难通过单一视角或一套注意力机制完整捕捉。

为此，Transformer 引入了**多头注意力机制（Multi-Head Attention）**。其核心思想是通过多组独立的 Query、Key、Value 投影，让不同注意力头分别专注于不同的语义关系，最后将各头的输出拼接融合。

#### 前馈神经网络层
前馈神经网络（Feed-Forward Network，简称 FFN）是 Transformer 编码器中每个子层的重要组成部分，紧接在多头注意力子层之后。它通过对每个位置的表示进行**逐位置**、**非线性**的特征变换，进一步提升模型对复杂语义的建模能力。

一个标准的 FFN 子层包含两个线性变换和一个非线性激活函数，中间通常使用 ReLU激活。其计算公式如下：

$ \text{FFN}(x) = \max(0, xW_1 + b_1)W_2 + b_2 $

### 6.3.2 残差连接与层归一化
在 Transformer 的每个编码器层中，每个子层，包括自注意力子层和前馈神经网络子层，其输出都要经过**残差连接（Residual Connection）**和**层归一化（Layer Normalization）**处理。这两者是深层神经网络中常用的结构，用于缓解模型训练中的梯度消失、收敛困难等问题，对于Transformer能够堆叠多层至关重要。

#### 残差连接
残差连接（Residual Connection，也称"跳跃连接"或"捷径连接"）最初在计算机视觉领域被提出，用于缓解深层神经网络中的梯度消失问题。其核心思想是：

将子层的输入直接与其输出相加，形成一条跨越子层的"捷径"，其数学形式为：

$ y = x + \mathcal{F}(x) $

#### 层归一化
每个子层在残差连接之后都会进行**层归一化（Layer Normalization，简称 LayerNorm）**。它的主要作用是规范输入序列中每个token的特征分布，提升模型训练的稳定性。

### 6.3.3 位置编码
Transformer 模型完全摒弃了 RNN 结构，意味着它不再按顺序处理序列，而是可以并行处理所有位置的信息。尽管这带来了显著的计算效率提升，却也引发了一个问题：Transformer 无法像 RNN 那样天然地捕捉词语之间的顺序关系。

为了解决这一问题，Transformer 引入了一个关键机制——**位置编码（Positional Encoding）**。该机制为每个词引入一个表示其位置信息的向量，并将其与对应的词向量相加，作为模型输入的一部分。

为帮助更直观地理解正余弦位置编码的构造和变化规律，可以使用以下可视化工具进行交互体验。

Transformer提出的这种编码方式不依赖任何可学习参数，数值稳定，并具备以下优势：

+ 所有值都在[-1,1]范围内，数值稳定
+ 编码方式固定、可预计算，无需训练；
+ 相同位置的编码在不同句子中保持一致；
+ 编码之间具有数学规律，便于模型在注意力机制中感知词语之间的相对位置关系。

### 6.3.4 编码器小结
Transformer 编码器通过多个结构一致的编码器层堆叠构成，每一层由两个核心子层组成：

1. **自注意力子层（Self-Attention）**：通过 Query、Key、Value 向量机制计算全序列中各位置之间的相关性，提取全局上下文信息。
2. **前馈神经网络子层（Feed-Forward Network）**：对每个位置独立进行非线性特征变换，增强模型的表示能力。

另外，在这两个子层之后，Transformer 引入了两个关键结构：

+ **残差连接（Residual Connection）**：缓解深层网络中的梯度消失问题；
+ **层归一化（Layer Normalization）**：规范向量分布，提升训练稳定性。

最后，为弥补模型并行结构下缺乏顺序感的缺陷，Transformer 使用基于正余弦函数的位置编码来提供序列中每个词的位置信息。

## 6.4 解码器
### 6.4.1 概述
Transformer 解码器的主要功能是：根据编码器的输出，逐步生成目标序列中的每一个词。其生成方式采用自回归机制（autoregressive）：每一步的输入由此前已生成的所有词组成，模型将输出一个与当前输入长度相同的序列表示。我们只取最后一个位置的输出，作为当前步的预测结果。这一过程会不断重复，直到生成特殊的结束标记 `<eos>`，表示序列生成完成。

<!-- 这是一张图片，ocr 内容为： -->
![](images/image_1772902934707_402784467.png)

编码器也由多个结构相同的**解码器层（Decoder Layer）**堆叠组成。

每个Decoder Layer都包含三个子层，分别是**Masked自注意力子层**、**编码器-解码器注意力子层（Encoder-Decoder Attention）****和****前馈神经网络子层（Feed-Forward Network）**。

各层作用如下：

+ **Masked自注意力子层（Masked Self Attention）**：用于建模当前位置与前文词之间的依赖关系。为了在训练时模拟逐词生成的过程，引入遮盖机制（Mask），限制每个位置只能关注它前面的词。
+ **编码器-解码器注意力子层（Encoder-Decoder Attention）**：用于建模当前解码位置与源序列各位置之间的依赖关系。通过注意力机制，模型能够根据当前状态从编码器的输出中提取相关上下文信息（相当于 Seq2Seq 模型中的 Attention 机制）。
+ **前馈神经网络子层（Feed-Forward Network）**：与编码器中结构完全一致，对每个位置的表示进行非线性变换，增强模型的表达能力。

### 6.4.2 Masked 自注意力子层
该子层的主要作用是：建模目标序列中当前位置与前文之间的依赖关系，为当前词的生成提供上下文语义支持。

由于 Transformer 不具备像 RNN 那样的隐藏状态传递机制，无法在序列生成过程中保留上下文信息，因此在生成每一个词时，必须将此前已生成的所有词作为输入，通过自注意力机制重新建模上下文关系，以预测下一个词。

为提升效率，Transformer 采用了**并行训练策略**：一次性输入完整目标序列，同时预测每个位置的词。

为实现这一策略，需要引入**掩码（Mask）机制**：在计算注意力时，遮挡住当前位置之后的信息，确保模型只能看到当前位置之前的内容。

## 6.5 PyTorch API使用
### 6.5.1 nn.Transformer
`nn.Transformer` 封装了完整的前向传播逻辑，其 `forward()` 方法定义了编码器→解码器的执行流程。

```python
output = transformer(
    src=src_emb,
    tgt=tgt_emb,
    src_key_padding_mask=src_pad_mask,
    tgt_key_padding_mask=tgt_pad_mask,
    tgt_mask=tgt_mask,
    memory_key_padding_mask=src_pad_mask
)
```

**参数说明：**

| 参数 | 说明 |
| --- | --- |
| src | 源序列的嵌入表示，形状为 (batch_size, src_len, d_model) |
| tgt | 目标序列的嵌入表示，形状为 (batch_size, tgt_len, d_model) |
| src_key_padding_mask | 编码器的padding掩码 |
| tgt_key_padding_mask | 解码器的padding掩码 |
| tgt_mask | 解码器的序列掩码（防止看到未来信息） |
| memory_key_padding_mask | 解码器对编码器输出的掩码 |


**输出：**

+ output：解码器输出的隐藏状态序列，形状为 (batch_size, tgt_len, d_model)

### 6.5.2 nn.TransformerEncoder
`nn.TransformerEncoder` 用于对源序列进行编码，提取上下文相关的语义表示。

```python
from torch import nn

transformer = nn.Transformer(
    d_model=512, nhead=8,
    num_encoder_layers=6, num_decoder_layers=6,
    batch_first=True
)

memory = transformer.encoder(
    src=src_emb, 
    src_key_padding_mask=src_pad_mask
)
```

### 6.5.3 nn.TransformerDecoder
`nn.TransformerDecoder` 用于基于编码器的输出和目标序列的嵌入表示，逐步生成目标序列中的各个 token。

```python
output = transformer.decoder(
    tgt=tgt_emb,
    memory=memory,
    tgt_mask=tgt_mask,
    tgt_key_padding_mask=tgt_pad_mask,
    memory_key_padding_mask=src_pad_mask
)
```

## 6.6 案例实操（中英翻译V3.0）
### 6.6.1 需求说明
本案例要求使用Transformer模型实现中英翻译任务。

### 6.6.2 需求分析
PyTorch 已提供了 `nn.Transformer` 模块，包含完整的编码器-解码器结构，因此我们可以直接使用其核心组件来搭建模型。

然而，PyTorch 并未内置位置编码（Positional Encoding）模块，而 Transformer 又不具备处理位置信息的能力，因此我们需要手动实现位置编码，并与嵌入层输出相加，作为 Transformer 的输入。

除此之外，还需要完成以下模块：

+ 源语言和目标语言的词嵌入层（nn.Embedding）
+ 输出层（nn.Linear）用于将模型输出映射为目标词表大小

### 6.6.3 完整代码
**位置编码模块**

```python
import torch
from torch import nn

class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=500):
        super().__init__()
        
        self.d_model = d_model
        self.max_len = max_len
        
        pe = torch.zeros(max_len, d_model, dtype=torch.float)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2) * (-torch.log(torch.tensor(10000.0)) / d_model))
        
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        
        self.register_buffer('pe', pe)
    
    def forward(self, x):
        seq_len = x.size(1)
        return x + self.pe[:seq_len]
```

**Transformer翻译模型**

```python
import torch
from torch import nn
import config

class TranslationModel(nn.Module):
    def __init__(self, zh_vocab_size, en_vocab_size, zh_padding_index, en_padding_index):
        super().__init__()
        
        self.src_embedding = nn.Embedding(
            num_embeddings=zh_vocab_size, 
            embedding_dim=config.DIM_MODEL,
            padding_idx=zh_padding_index
        )
        
        self.tgt_embedding = nn.Embedding(
            num_embeddings=en_vocab_size, 
            embedding_dim=config.DIM_MODEL,
            padding_idx=en_padding_index
        )
        
        self.position_encoding = PositionalEncoding(d_model=config.DIM_MODEL)
        
        self.transformer = nn.Transformer(
            d_model=config.DIM_MODEL,
            nhead=config.NUM_HEADS,
            num_encoder_layers=config.NUM_ENCODER_LAYERS,
            num_decoder_layers=config.NUM_DECODER_LAYERS,
            batch_first=True
        )
        
        self.linear = nn.Linear(config.DIM_MODEL, en_vocab_size)
    
    def encode(self, src, src_pad_mask):
        src_embed = self.src_embedding(src)
        src_embed = self.position_encoding(src_embed)
        memory = self.transformer.encoder(
            src=src_embed, 
            src_key_padding_mask=src_pad_mask
        )
        return memory
    
    def decode(self, tgt, memory, tgt_mask, tgt_pad_mask, src_pad_mask):
        tgt_embed = self.tgt_embedding(tgt)
        tgt_embed = self.position_encoding(tgt_embed)
        output = self.transformer.decoder(
            tgt=tgt_embed, 
            memory=memory, 
            tgt_mask=tgt_mask,
            tgt_key_padding_mask=tgt_pad_mask,
            memory_key_padding_mask=src_pad_mask
        )
        return self.linear(output)
    
    def forward(self, src, tgt, src_pad_mask, tgt_pad_mask, tgt_mask):
        memory = self.encode(src, src_pad_mask)
        output = self.decode(tgt, memory, tgt_mask, tgt_pad_mask, src_pad_mask)
        return output
```

**配置文件 config.py**

```python
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

MODELS_DIR = BASE_DIR / 'models'
PROCESSED_DATA_DIR = BASE_DIR / 'data' / 'processed'
RAW_DATA_DIR = BASE_DIR / 'data' / 'raw'
LOGS_DIR = BASE_DIR / 'logs'

DIM_MODEL = 256
NUM_HEADS = 8
NUM_ENCODER_LAYERS = 3
NUM_DECODER_LAYERS = 3

BATCH_SIZE = 64
SEQ_LEN = 50
LEARNING_RATE = 1e-4
EPOCHS = 30
```

