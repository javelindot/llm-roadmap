<nav style="background-color: #2c3e50; color: white; padding: 10px 0; margin-bottom: 20px; border-radius: 8px;">
  <ul style="list-style: none; padding: 0; margin: 0; display: flex; justify-content: center; flex-wrap: wrap;">
    <li style="margin: 0 15px; margin-bottom: 0;"><a href="../../" style="color: white; font-weight: 500; text-decoration: none; padding: 5px 10px; border-radius: 4px; transition: background-color 0.3s ease;">首页</a></li>
    <li style="margin: 0 15px; margin-bottom: 0;"><a href="../../base/" style="color: white; font-weight: 500; text-decoration: none; padding: 5px 10px; border-radius: 4px; transition: background-color 0.3s ease;">数学基础</a></li>
    <li style="margin: 0 15px; margin-bottom: 0;"><a href="../../ml/" style="color: white; font-weight: 500; text-decoration: none; padding: 5px 10px; border-radius: 4px; transition: background-color 0.3s ease;">机器学习</a></li>
    <li style="margin: 0 15px; margin-bottom: 0;"><a href="../" style="color: white; font-weight: 500; text-decoration: none; padding: 5px 10px; border-radius: 4px; transition: background-color 0.3s ease;">自然语言处理</a></li>
  </ul>
</nav>

## 4.1 概述
传统的自然语言处理任务（如文本分类、序列标注）以**静态输出**为主，其目标是预测固定类别或标签。然而，现实中的许多应用需要模型**动态生成新的序列**，例如：

+ **机器翻译**：输入中文句子，输出对应的英文翻译。
+ **文本摘要**：输入长篇文章，生成简短的摘要。
+ **问答系统**：输入用户问题，生成自然语言回答。
+ **对话系统**：输入对话历史，生成连贯的下一条回复。

这些任务具有两个关键共同点：

+ **输入和输出均为序列**（如词、字符或子词序列）。
+ **输入与输出序列长度动态可变**（例如翻译任务中，中英文句子长度可能不同）。

为了解决这类问题，研究者提出了**Seq2Seq（Sequence to Sequence，序列到序列）模型**。

<!-- 这是一张图片，ocr 内容为： -->
![](images/image_1772902934682_3222655.png)

## 4.2 模型结构详解
Seq2Seq 模型由一个**编码器（Encoder）**和一个**解码器（Decoder）**构成。编码器负责提取输入序列的语义信息，并将其压缩为一个固定长度的上下文向量（Context Vector）；解码器则基于该向量，逐步生成目标序列。

<!-- 这是一张图片，ocr 内容为： -->
![](images/image_1772902934682_45941424.png)

### 4.2.1 编码器
编码器主要由一个循环神经网络（RNN/LSTM/GRU）构成，其任务是将输入序列的语义信息提取并压缩为一个上下文向量。

在模型处理输入序列时，循环神经网络会依次接收每个token的输入，并在每个时间步步更新隐藏状态。每个隐藏状态都携带了截止到当前位置为止的信息。随着序列推进，信息不断累积，最终会在最后一个时间步形成一个包含整句信息的隐藏状态。

这个最后的隐藏状态就会作为**上下文向量（context vector）**，传递给解码器，用于指导后续的序列生成。

<!-- 这是一张图片，ocr 内容为： -->
![](images/image_1772902934682_222840809.png)

为增强编码器的理解能力，循环网络也可以采用双向结构（结合前文与后文信息）或多层结构（提取更深的语义特征）。

### 4.2.2 解码器
解码器主要也由一个循环神经网络（RNN/LSTM/GRU）构成，其任务是基于编码器传递的上下文向量，逐步生成目标序列。

<!-- 这是一张图片，ocr 内容为： -->
![](images/image_1772902934683_691291512.png)

在生成开始时，循环神经网络以上下文向量作为初始隐藏状态，并接收一个特殊的起始标记 `<sos>`（start of sentence）作为第一个时间步的输入，用于预测第一个 token。

随后，在每一个时间步，模型都会根据前一时刻的隐藏状态和上一步生成的 token，预测当前的输出。这种"将前一步的输出作为下一步输入"的方式被称为**自回归生成（Autoregressive Generation）**，它确保了生成结果的连贯性。

生成过程会持续进行，直到模型生成了一个特殊的结束标记 `<eos>`（end of sentence），表示句子生成完成。

**说明**：起始标记和结束标记会在训练数据中显式添加，模型会在训练中学会何时开始、如何续写，以及何时结束，从而掌握完整的生成流程。

## 4.3 模型训练和推理机制
### 4.3.1 模型训练
Seq2Seq 模型的训练目标，是在给定输入序列的条件下，逐步生成完整且准确的目标序列。下面以一个中–英机器翻译样本为例，说明训练过程的各个环节。

假设某个训练样本为：

+ 中文输入："我喜欢你。"
+ 英文输出："I like you."

#### 数据准备
为了让模型明确目标序列的起点和终点，通常在目标句前添加 `<sos>`（start of sequence），句末添加 `<eos>`（end of sequence）：

"I like you." → " I like you. "

这两个特殊标记帮助模型学会从哪里开始生成，以及何时停止生成。

#### 前向传播
模型由编码器和解码器两部分组成：

**编码器**

编码器接收源语言序列"我喜欢你。"，通过嵌入层和循环神经网络（RNN/LSTM/GRU）的逐步处理，将整句编码为上下文向量。

**解码器**

解码器使用该上下文向量初始化其隐藏状态，然后逐步生成目标序列。

**需要特别注意的是，训练阶段与推理阶段的解码策略是不同的：**

在推理阶段，解码器采用**自回归生成**方式：每一步的输入是模型自己上一步的预测结果。

而在训练阶段，通常使用一种称为 **Teacher Forcing** 的策略，即：

解码器每一步的输入不是模型上一步的预测结果，而是目标序列中真实的前一个token。如图下图所示：

<!-- 这是一张图片，ocr 内容为： -->
![](images/image_1772902934683_288296789.png)

这种做法带来了两个明显好处：

+ 训练更快，误差不会累积；
+ 梯度传播更稳定，有利于优化收敛。

#### 计算损失
解码器每一步输出一个token的概率分布，我们通过交叉熵损失函数衡量模型对真实词的预测质量。训练过程中，每一个时间步都会产生一个损失值。该样本的总损失，就是所有时间步的损失值逐步累加的结果。

<!-- 这是一张图片，ocr 内容为： -->
![](images/image_1772902934684_942278985.png)

#### 反向传播
在 PyTorch 中，调用 `loss.backward()` 即可自动完成梯度的反向传播。系统会沿时间维度展开计算图，自动完成所有参数的梯度计算，无需手动推导，实现简洁高效。

### 4.3.2 模型推理
模型推理是Seq2Seq模型在实际任务中生成目标序列的过程，通常包括以下几个环节：

#### 编码器处理
推理阶段的编码器处理流程与训练时完全一致。

输入序列会经过分词、嵌入和循环神经网络的逐步处理，最终生成一个表示整句语义的上下文向量，该向量将作为解码器的初始隐藏状态，为生成过程提供语义基础。

#### 解码器处理
解码器是推理过程的核心，其生成方式采用**自回归生成（Autoregressive Generation）**：每一步的输出会作为下一步的输入，逐步构造完整句子。

**自回归生成流程**

1. 第一步，解码器接收起始标记 `<sos>`，生成第一个词；
2. 第二步，将上一步生成的词作为当前输入，再预测第二个词；
3. 持续重复以上过程，直到模型生成 `<eos>`，或达到设定的最大生成步数。

**词选择策略**

每个时间步，解码器输出的是一个词概率分布。我们需要从中选择一个具体词作为本时间步的输出，选择方式即为生成策略。常见策略包括：

+ **贪心解码（Greedy Decoding）**每一步都选择概率最高的词。优点：简单高效缺点：容易陷入局部最优，生成不够多样。
+ **束搜索（Beam Search）**每一步保留多个候选词序列（如 beam size = 3），并在扩展后选择得分最高的完整句子。优点：全局考虑，生成质量高缺点：计算开销大

## 4.4 案例实操（中英翻译V1.0）
### 4.4.1 需求说明
本案例的目标是实现一个简易的中→英翻译模型，输入为中文句子（如"我喜欢你。"），输出为英文翻译结果（如"I like you."）。

### 4.4.2 需求分析
#### 数据处理
本案例使用的数据集来自[阿里云天池平台](https://tianchi.aliyun.com/dataset/174937)，共包含 29,155 对中英文平行语句。原始文件为 TSV 格式，每行包含一对中文句子和对应的英文翻译，结构如下图所示：

<!-- 这是一张图片，ocr 内容为： -->
![](images/image_1772902934685_659965403.png)

在本案例中，仅使用前两列数据：中文句子作为模型输入（源语言），英文句子作为模型输出（目标语言）。

需要注意的是，输入和输出序列需要单独分词和构建词表，其中中文按照字粒度分词，英文使用[NLTK](https://www.nltk.org/howto/tokenize.html)分词工具。

#### 模型设计
模型采用经典的 Seq2Seq 架构，由编码器（Encoder）与解码器（Decoder）两部分构成，具体结构如下：

**编码器**

编码器由两层组成：

+ 嵌入层（Embedding Layer）：将中文 token 序列映射为稠密向量。
+ 循环神经网络层（GRU）：为更好的提取输入序列的语义信息，采用双向GRU，最终拼接前向与后向的隐藏状态，作为上下文向量传递给解码器。

**解码器**

解码器由三层组成：

+ 嵌入层（Embedding Layer）：将目标序列中的token 转换为稠密向量。
+ 循环神经网络层（GRU）：结合前一步的词向量和隐藏状态，生成当前的隐藏状态。
+ 全连接层（Linear Layer）：将当前隐藏状态映射为词表大小的概率分布，用于预测下一个词。

#### 训练方案
+ 训练策略：采用 Teacher Forcing，即每一步使用目标序列中真实的前一个词作为解码器输入。
+ 损失函数：使用 CrossEntropyLoss。
+ 优化器：使用 Adam 优化器进行参数更新。

#### 推理方案
推理阶段采用自回归生成策略（Autoregressive Generation）。

词选择策略使用贪心解码（Greedy Decoding）。

#### 评估方案
在机器翻译任务中，**BLEU（Bilingual Evaluation Understudy）** 是一种常用的自动评估指标，用于衡量模型生成的翻译与人工参考译文之间的相似程度。其核心思想是：

+ **n-gram 匹配**：统计预测译文中有多少 n-gram（词或短语）同时出现在参考译文中，用于衡量翻译内容的准确性。
+ **精确率计算**：将匹配到的 n-gram 数量除以预测译文中 n-gram 的总数，反映生成译文中"正确部分"的比例。

此外，BLEU 还引入长度惩罚机制，防止模型通过生成过短句子获得不合理的高分。

最终得到的 BLEU 分数越高，说明生成译文与参考译文越接近。

本案例中，使用 Python 的 NLTK 库 中的 [bleu_score](https://www.nltk.org/api/nltk.translate.bleu_score.html) 模块，对模型在测试集上的翻译结果进行评估，主要参考BLEU-4 的得分情况，作为翻译质量的衡量依据。

### 4.4.3 需求实现
#### 项目结构
```plain
project/
├── config.py              # 配置文件
├── process.py             # 数据预处理
├── tokenizer.py           # 自定义分词器
├── dataset.py             # 自定义数据集
├── model.py               # 模型定义
├── train.py               # 训练脚本
├── predict.py             # 预测脚本
└── evaluate.py            # 评估脚本
```

#### 完整代码
**数据预处理 process.py**

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from tokenizer import ChineseTokenizer, EnglishTokenizer
import config

def process():
    """
    数据预处理主函数。
    """
    print('开始处理数据')
    
    # 读取原始数据文件
    df = pd.read_csv(
        config.RAW_DATA_DIR / 'cmn.txt',
        sep='\t',
        header=None,
        usecols=[0, 1],
        names=['en', 'zh']
    )
    
    # 数据清洗：去除空值和空字符串
    df = df.dropna()
    df = df[df['en'].str.strip().ne('') & df['zh'].str.strip().ne('')]
    
    # 划分训练集和测试集
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
    
    # 构建词表并保存
    EnglishTokenizer.build_vocab(train_df['en'].tolist(), config.PROCESSED_DATA_DIR / 'en_vocab.txt')
    ChineseTokenizer.build_vocab(train_df['zh'].tolist(), config.PROCESSED_DATA_DIR / 'zh_vocab.txt')
    
    # 加载词表
    en_tokenizer = EnglishTokenizer.from_vocab(config.PROCESSED_DATA_DIR / 'en_vocab.txt')
    zh_tokenizer = ChineseTokenizer.from_vocab(config.PROCESSED_DATA_DIR / 'zh_vocab.txt')
    
    # 编码并保存训练集
    train_df['en'] = train_df['en'].apply(
        lambda x: en_tokenizer.encode(x, seq_len=config.SEQ_LEN, add_sos_eos=True)
    )
    train_df['zh'] = train_df['zh'].apply(
        lambda x: zh_tokenizer.encode(x, seq_len=config.SEQ_LEN, add_sos_eos=False)
    )
    train_df.to_json(
        config.PROCESSED_DATA_DIR / 'indexed_train.jsonl',
        orient='records',
        lines=True
    )
    
    # 编码并保存测试集
    test_df['en'] = test_df['en'].apply(
        lambda x: en_tokenizer.encode(x, seq_len=config.SEQ_LEN, add_sos_eos=True)
    )
    test_df['zh'] = test_df['zh'].apply(
        lambda x: zh_tokenizer.encode(x, seq_len=config.SEQ_LEN, add_sos_eos=False)
    )
    test_df.to_json(
        config.PROCESSED_DATA_DIR / 'indexed_test.jsonl',
        orient='records',
        lines=True
    )
    
    print('数据处理完成')

if __name__ == '__main__':
    process()
```

**自定义分词器 tokenizer.py**

```python
from abc import abstractmethod
from nltk import word_tokenize, TreebankWordDetokenizer
from tqdm import tqdm

class BaseTokenizer:
    """
    分词器基类，支持词表构建、编码、索引映射等功能。
    """
    unk_token = '<unk>'
    pad_token = '<pad>'
    sos_token = '<sos>'
    eos_token = '<eos>'
    
    @staticmethod
    @abstractmethod
    def tokenize(sentence):
        pass
    
    @abstractmethod
    def decode(self, indexes):
        pass
    
    @classmethod
    def build_vocab(cls, sentences, vocab_file):
        unique_words = set()
        for sentence in tqdm(sentences, desc='分词'):
            for word in cls.tokenize(sentence):
                unique_words.add(word)
        
        vocab_list = [cls.pad_token, cls.unk_token, cls.sos_token, cls.eos_token] + list(unique_words)
        with open(vocab_file, 'w', encoding='utf-8') as f:
            for word in vocab_list:
                f.write(word + '\n')
    
    def __init__(self, vocab_list):
        self.vocab_list = vocab_list
        self.vocab_size = len(vocab_list)
        self.word2index = {word: index for index, word in enumerate(vocab_list)}
        self.index2word = {index: word for index, word in enumerate(vocab_list)}
        self.unk_token_index = self.word2index[self.unk_token]
        self.pad_token_index = self.word2index[self.pad_token]
        self.sos_token_index = self.word2index[self.sos_token]
        self.eos_token_index = self.word2index[self.eos_token]
    
    @classmethod
    def from_vocab(cls, vocab_file):
        with open(vocab_file, 'r', encoding='utf-8') as f:
            vocab_list = [line.strip() for line in f.readlines()]
        return cls(vocab_list)
    
    def encode(self, sentence, seq_len, add_sos_eos=False):
        tokens = self.tokenize(sentence)
        indexes = [self.word2index.get(token, self.unk_token_index) for token in tokens]
        
        if add_sos_eos:
            indexes = indexes[:seq_len - 2]
            indexes = [self.sos_token_index] + indexes + [self.eos_token_index]
        else:
            indexes = indexes[:seq_len]
        
        if len(indexes) < seq_len:
            indexes += [self.pad_token_index] * (seq_len - len(indexes))
        
        return indexes

class ChineseTokenizer(BaseTokenizer):
    @staticmethod
    def tokenize(sentence):
        return list(sentence)
    
    def decode(self, indexes):
        return "".join([self.index2word[index] for index in indexes])

class EnglishTokenizer(BaseTokenizer):
    @staticmethod
    def tokenize(sentence):
        return word_tokenize(sentence)
    
    def decode(self, indexes):
        tokens = [self.index2word[index] for index in indexes]
        return TreebankWordDetokenizer().detokenize(tokens)
```

**自定义数据集 dataset.py**

```python
import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
import config

class TranslationDataset(Dataset):
    def __init__(self, data_path):
        self.data = pd.read_json(data_path, lines=True).to_dict(orient='records')
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, index):
        input_tensor = torch.tensor(self.data[index]['zh'], dtype=torch.long)
        target_tensor = torch.tensor(self.data[index]['en'], dtype=torch.long)
        return input_tensor, target_tensor

def get_dataloader(train=True):
    data_path = config.PROCESSED_DATA_DIR / ('indexed_train.jsonl' if train else 'indexed_test.jsonl')
    dataset = TranslationDataset(data_path)
    return DataLoader(dataset, batch_size=config.BATCH_SIZE, shuffle=True)
```

**模型定义 model.py**

```python
import torch
from torch import nn
from torchinfo import summary
import config

class TranslationEncoder(nn.Module):
    """
    翻译模型编码器，基于双向 GRU。
    """
    def __init__(self, vocab_size, padding_index):
        super().__init__()
        
        self.embedding = nn.Embedding(
            num_embeddings=vocab_size,
            embedding_dim=config.EMBEDDING_DIM,
            padding_idx=padding_index
        )
        
        self.rnn = nn.GRU(
            input_size=config.EMBEDDING_DIM,
            hidden_size=config.ENCODER_HIDDEN_DIM,
            num_layers=config.ENCODER_LAYERS,
            batch_first=True,
            bidirectional=True
        )
    
    def forward(self, src):
        embedded = self.embedding(src)
        output, hidden = self.rnn(embedded)
        return output, hidden

class TranslationDecoder(nn.Module):
    """
    翻译模型解码器，基于单向 GRU。
    """
    def __init__(self, vocab_size, padding_index):
        super().__init__()
        
        self.embedding = nn.Embedding(
            num_embeddings=vocab_size,
            embedding_dim=config.EMBEDDING_DIM,
            padding_idx=padding_index
        )
        
        self.rnn = nn.GRU(
            input_size=config.EMBEDDING_DIM,
            hidden_size=config.DECODER_HIDDEN_DIM,
            batch_first=True
        )
        
        self.linear = nn.Linear(
            in_features=config.DECODER_HIDDEN_DIM,
            out_features=vocab_size
        )
    
    def forward(self, tgt, hidden):
        embedded = self.embedding(tgt)
        output, hidden = self.rnn(embedded, hidden)
        output = self.linear(output)
        return output, hidden
```

**训练脚本 train.py**

```python
import time
from itertools import chain
import torch
from torch.nn import CrossEntropyLoss
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm
from dataset import get_dataloader
from tokenizer import ChineseTokenizer, EnglishTokenizer
import config
from model import TranslationEncoder, TranslationDecoder

def train_one_epoch(dataloader, encoder, decoder, loss_function, optimizer, device):
    encoder.train()
    decoder.train()
    total_loss = 0
    
    for src, tgt in tqdm(dataloader, desc='训练'):
        src = src.to(device)
        tgt = tgt.to(device)
        
        optimizer.zero_grad()
        
        _, encoder_hidden = encoder(src)
        
        forward_hidden = encoder_hidden[-2]
        backward_hidden = encoder_hidden[-1]
        context_vector = torch.cat([forward_hidden, backward_hidden], dim=1)
        
        decoder_input = tgt[:, 0:1]
        decoder_hidden = context_vector.unsqueeze(0)
        decoder_outputs = []
        
        for step in range(1, config.SEQ_LEN):
            decoder_output, decoder_hidden = decoder(decoder_input, decoder_hidden)
            decoder_outputs.append(decoder_output)
            decoder_input = tgt[:, step:step+1]
        
        decoder_outputs = torch.cat(decoder_outputs, dim=1)
        decoder_targets = tgt[:, 1:]
        
        loss = loss_function(
            decoder_outputs.reshape(-1, decoder_outputs.shape[-1]),
            decoder_targets.reshape(-1)
        )
        
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    
    return total_loss / len(dataloader)

def train():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    dataloader = get_dataloader()
    
    zh_tokenizer = ChineseTokenizer.from_vocab(config.PROCESSED_DATA_DIR / 'zh_vocab.txt')
    en_tokenizer = EnglishTokenizer.from_vocab(config.PROCESSED_DATA_DIR / 'en_vocab.txt')
    
    encoder = TranslationEncoder(
        vocab_size=zh_tokenizer.vocab_size,
        padding_index=zh_tokenizer.pad_token_index
    ).to(device)
    
    decoder = TranslationDecoder(
        vocab_size=en_tokenizer.vocab_size,
        padding_index=en_tokenizer.pad_token_index
    ).to(device)
    
    loss_function = CrossEntropyLoss(ignore_index=en_tokenizer.pad_token_index)
    optimizer = torch.optim.Adam(chain(encoder.parameters(), decoder.parameters()), lr=config.LEARNING_RATE)
    
    writer = SummaryWriter(log_dir=config.LOGS_DIR / time.strftime('%Y-%m-%d_%H-%M-%S'))
    best_loss = float('inf')
    
    for epoch in range(1, config.EPOCHS + 1):
        print(f'========== Epoch {epoch} ==========')
        avg_loss = train_one_epoch(dataloader, encoder, decoder, loss_function, optimizer, device)
        print(f'平均损失: {avg_loss:.4f}')
        writer.add_scalar('Loss', avg_loss, epoch)
        
        if avg_loss < best_loss:
            best_loss = avg_loss
            torch.save(encoder.state_dict(), config.MODELS_DIR / 'encoder.pt')
            torch.save(decoder.state_dict(), config.MODELS_DIR / 'decoder.pt')
            print('已保存模型')

if __name__ == '__main__':
    train()
```

**预测脚本 predict.py**

```python
import torch
from tokenizer import ChineseTokenizer, EnglishTokenizer
from model import TranslationEncoder, TranslationDecoder
import config

def predict_batch(input_tensor, encoder, decoder, en_tokenizer, device):
    encoder.eval()
    decoder.eval()
    
    with torch.no_grad():
        encoder_output, encoder_hidden = encoder(input_tensor)
        context_vector = torch.cat([encoder_hidden[-2], encoder_hidden[-1]], dim=1)
        
        batch_size = input_tensor.shape[0]
        decoder_input = torch.full(
            size=(batch_size, 1),
            fill_value=en_tokenizer.sos_token_index,
            device=device
        )
        decoder_hidden = context_vector.unsqueeze(0)
        
        generated = [[] for _ in range(batch_size)]
        finished = [False for _ in range(batch_size)]
        
        for step in range(1, config.SEQ_LEN):
            decoder_output, decoder_hidden = decoder(decoder_input, decoder_hidden)
            predict_indexes = decoder_output.argmax(dim=-1)
            
            for i in range(batch_size):
                if finished[i]:
                    continue
                token_id = predict_indexes[i].item()
                if token_id == en_tokenizer.eos_token_index:
                    finished[i] = True
                    continue
                generated[i].append(token_id)
            
            if all(finished):
                break
            
            decoder_input = predict_indexes
        
        return generated

def predict(zh_sentence, encoder, decoder, zh_tokenizer, en_tokenizer, device):
    input_ids = zh_tokenizer.encode(zh_sentence, seq_len=config.SEQ_LEN, add_sos_eos=False)
    input_tensor = torch.tensor([input_ids], device=device)
    
    generated = predict_batch(input_tensor, encoder, decoder, en_tokenizer, device)
    en_indexes = generated[0]
    en_sentence = en_tokenizer.decode(en_indexes)
    
    return en_sentence
```

**评估脚本 evaluate.py**

```python
import torch
from nltk.translate.bleu_score import corpus_bleu
from tqdm import tqdm
import config
from tokenizer import ChineseTokenizer, EnglishTokenizer
from model import TranslationEncoder, TranslationDecoder
from dataset import get_dataloader
from predict import predict_batch

def evaluate(dataloader, encoder, decoder, zh_tokenizer, en_tokenizer, device):
    all_references = []
    all_predictions = []
    
    special_tokens = [
        zh_tokenizer.pad_token_index,
        zh_tokenizer.eos_token_index,
        zh_tokenizer.sos_token_index
    ]
    
    for src, tgt in tqdm(dataloader, desc="评估"):
        src = src.to(device)
        tgt = tgt.tolist()
        
        predict_indexes = predict_batch(src, encoder, decoder, en_tokenizer, device)
        all_predictions.extend(predict_indexes)
        
        for indexes in tgt:
            indexes = [index for index in indexes if index not in special_tokens]
            all_references.append([indexes])
    
    bleu = corpus_bleu(all_references, all_predictions)
    return bleu
```

**配置文件 config.py**

```python
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

MODELS_DIR = BASE_DIR / 'models'
PROCESSED_DATA_DIR = BASE_DIR / 'data' / 'processed'
RAW_DATA_DIR = BASE_DIR / 'data' / 'raw'
LOGS_DIR = BASE_DIR / 'logs'

EMBEDDING_DIM = 128
ENCODER_HIDDEN_DIM = 512
DECODER_HIDDEN_DIM = 2 * ENCODER_HIDDEN_DIM
ENCODER_LAYERS = 1

BATCH_SIZE = 128
SEQ_LEN = 30
LEARNING_RATE = 1e-3
EPOCHS = 30
```

## 4.5 存在问题
在上述 Seq2Seq 架构中，编码器会将整个源句压缩为一个固定长度的上下文向量，并将其作为解码器生成目标序列的唯一参考。这种"压缩再解压"的方式虽然结构简洁，但在实际任务中暴露出两个核心问题：

### 4.5.1 信息压缩困难，语义表达受限
对于编码器而言，用一个定长向量去表达任意复杂的句子，是一项非常困难的任务。尤其在面对长句时，信息很容易在压缩过程中丢失，导致语义表达不完整。

这种"信息瓶颈"限制了模型在处理长文本或复杂语义结构时的表现。

### 4.5.2 缺乏动态感知，解码难以精准生成
解码器始终只能基于同一个上下文向量进行生成。

但在实际生成过程中，不同位置的目标词，往往依赖源句中不同的关键信息：

+ 生成主语时，可能更依赖源句的开头；
+ 生成谓语或宾语时，可能需要参考句中或句末内容。

然而在固定表示下，解码器无法"有选择地关注"输入序列的不同部分，只能一视同仁地处理所有信息，从而降低了生成的准确性与灵活性。

