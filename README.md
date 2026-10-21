# F20DL 第 25 组：最终多标签游戏类型数据集

本仓库提供供全组统一使用的**游戏简介 → 多标签 Genre 预测**数据。请所有组员使用相同的数据划分和标签顺序，保证传统机器学习及神经网络实验可以公平比较。

**固定版本：159,066 条文本–标签观察记录，23 个最终标签，最低保留标签频数 500，随机种子 42，按组划分 Train/Val/Test = 80/10/10。**

> 注意：159,066 是去重规则处理后的**文本–标签观察数**，不能直接称为 159,066 款唯一游戏。本仓库的数据包是**处理后的训练数据**，并不包含 Steam、IGDB 的完整原始数据集。

## 一、安装、检查和读取

需要 Python **3.10+** 和兼容的依赖。数据加载器在 Python 3.12 下测试过，实际测试使用的 pandas/numpy 版本见 `requirements-tested.txt`。

```powershell
python -m pip install -r requirements.txt
python verify_package.py
python examples/load_baseline_data.py
python -m unittest discover -s tests -v
```

若要自己实现 sklearn Baseline，可额外安装：

```powershell
python -m pip install -r requirements-baseline.txt
```

当前数据包只验证了**数据加载、标签编码和完整性**，不代表已经训练或测试过机器学习模型。

## 二、数据来源与清洗、标签处理规则

原始数据来自：

- **Steam：** https://huggingface.co/datasets/FronkonGames/steam-games-dataset
- **IGDB 镜像：** https://github.com/yuhangjiang22/video-game-genre-classificaion

最终数据在冻结之前进行了以下处理：

1. **缺失值处理：** 删除缺失或不可用游戏描述，以及没有可用目标类型标签的记录。
2. **剔除非游戏类型标签：** 例如 `Indie`（发行属性）、`Free To Play`（收费模式）、`Early Access`（发行阶段），它们不作为本项目的目标 Genre。
3. **跨数据源统一标签名称：** 例如 `RPG` 与 `Role-playing (RPG)`、`Simulation` 与 `Simulator`、`Sports` 与 `Sport` 统一到相同的目标名称。
4. **重复数据处理：** 根据既定规则处理文本–标签重复观察，并保留记录追踪与分组信息；不能把最终行数直接当成唯一游戏数。划分时保持已识别的近重复组完整。
5. **按频数筛选目标标签（阈值 500）：** 在统一后的标签体系中，**频数低于 500 的 Genre 不进入最终预测标签集合**；最终保留 23 类。这里的 500 指**某标签出现在多少条样本中**，不是游戏简介字数阈值，也不是随意删除 500 条游戏。若某条记录的标签全部被排除，它就无法作为最终监督学习样本使用。
6. **冻结数据：** 清洗、标签统一与筛选后，固定为 **159,066 条观察、23 类**。后续的 80/10/10 划分和压缩打包**没有再次清洗、删标签或删记录**。

**具体哪些旧标签被映射、合并或删除：** 请查看 `provenance/` 中的标签映射和清洗决策记录。当前上传的 README 与最终分布表并未提供完整的“被删除标签 + 原频数”明细，因此这里不臆造该清单。**500 的筛选规则针对合并后的全量数据执行一次，不是要求 train/val/test 每个集合都达到 500。**

## 三、最终保留的全部 23 个 Genre

下表为**最终 159,066 条记录**中的频数。一个游戏描述可以同时拥有多个 Genre，因此各类百分比之和可以超过 100%。

| 排名 | Genre | 样本数 | 占总样本比例 |
|---:|---|---:|---:|
| 1 | Adventure | 60,360 | 37.95% |
| 2 | Casual | 51,224 | 32.20% |
| 3 | Action | 47,074 | 29.59% |
| 4 | Simulation | 32,162 | 20.22% |
| 5 | Strategy | 31,102 | 19.55% |
| 6 | RPG | 28,251 | 17.76% |
| 7 | Sports | 10,190 | 6.41% |
| 8 | Racing | 7,302 | 4.59% |
| 9 | Shooter | 6,806 | 4.28% |
| 10 | Puzzle | 6,163 | 3.87% |
| 11 | Platform | 5,183 | 3.26% |
| 12 | Arcade | 3,306 | 2.08% |
| 13 | Massively Multiplayer | 2,576 | 1.62% |
| 14 | Fighting | 2,375 | 1.49% |
| 15 | Hack and Slash / Beat 'em Up | 1,507 | 0.95% |
| 16 | Turn-Based Strategy | 1,321 | 0.83% |
| 17 | Real-Time Strategy | 1,275 | 0.80% |
| 18 | Music | 1,132 | 0.71% |
| 19 | Point-and-click | 858 | 0.54% |
| 20 | Tactical | 855 | 0.54% |
| 21 | Quiz/Trivia | 838 | 0.53% |
| 22 | Visual Novel | 561 | 0.35% |
| 23 | Pinball | 544 | 0.34% |

最高频为 Adventure（60,360 条），最低频为 Pinball（544 条），全部保留标签的频数都达到最低阈值 500。完整频数 CSV、分布图和划分统计见 `reports/`。

## 四、固定训练集、验证集、测试集

| 集合 | 样本数 | 比例 | 用途 |
|---|---:|---:|---|
| **Train** | 127,254 | 80.00075% | 训练模型、拟合 TF-IDF 等文本特征 |
| **Validation (Val)** | 15,906 | 9.99962% | 调整超参数、选择阈值和模型 |
| **Test** | 15,906 | 9.99962% | 只用于最终评价 |
| **合计** | **159,066** | **100%** | |

使用 seed=42 的**组级多标签划分**：157,509 个既有分组不可拆分，同时尽量平衡样本数、各类型频数、常见标签对与组合、Steam/IGDB 来源比例。三个集合均覆盖 23 类；已识别重复组和规范化后相同的描述没有跨集合。**但不能保证所有尚未发现的语义改写重复都不存在。**

**所有组员不得自行重新随机划分、修改标签集合或重新清洗这份冻结数据。**

## 五、文件分别放在哪里？

```text
<package root>/
├── README.md / README_中文.md
├── data/
│   ├── train/*.csv.gz         # compressed training CSV shards
│   ├── val/*.csv.gz           # compressed validation CSV shards
│   └── test/*.csv.gz          # compressed test CSV shards
├── labels.json               # authoritative 23-label order
├── load_data.py              # load split shards and encode labels
├── restore_csv.py            # reconstruct exact original CSV files
├── verify_package.py         # integrity checks
├── package_manifest.json     # file listing and SHA256 checksums
├── requirements.txt
├── requirements-baseline.txt
├── requirements-tested.txt
├── examples/load_baseline_data.py
├── tests/test_loader.py
├── metadata/split_assignments.csv.gz
├── reports/                  # frequency tables, chart, split/validation reports
└── provenance/               # source information, cleaning rules, label mapping
```

主要目录解释：

- **`data/train/`、`data/val/`、`data/test/`：** 训练、验证、测试数据的压缩 CSV 分片；**不是多个可任选的数据集**，同一集合的所有分片都需要一起读取。
- **`labels.json`：** 全组统一的 23 类标签名称及顺序，模型输出列顺序必须与其一致。
- **`reports/`：** 23 类频数及图表、划分统计、验证报告等。
- **`provenance/`：** 原始数据来源、许可证资料、标签映射、清洗和去重决策等。
- **`metadata/`：** 样本和既有分组的归属信息，方便复核数据划分。
- **`package_manifest.json`：** 数据分片和文件完整性校验信息。

### 推荐：直接通过加载器读取

```python
from load_data import load_split, encode_targets, CLASSES

train = load_split("train")
val = load_split("val")
# test 留到最终评价时再读取。

X_train = train["description"].tolist()
y_train = encode_targets(train)  # (127254, 23) 的多热标签矩阵
X_val = val["description"].tolist()
y_val = encode_targets(val)
```

每条记录保留五列：`source`、`game_id`、`title`、`description`、`genres`。其中 `genres` 是 **JSON 标签数组**，一条记录可有多个 Genre；`game_id` 保持字符串，部分 IGDB 的 `title` 为空。模型主要输入是 `description`，不能把真实 `genres`、ID 等作为预测特征。不要自己重新排列标签，也不要使用旧版 9/20 类或原始 33/21 类的编码。

### 如果需要普通的 train.csv / val.csv / test.csv

```powershell
python restore_csv.py
```

脚本会在 `restored_splits/` 中恢复：

```text
restored_splits/train.csv
restored_splits/val.csv
restored_splits/test.csv
```

并通过 SHA256 检查恢复结果是否与原始冻结 CSV 完全一致。此目录已在 `.gitignore` 中排除，**不要把恢复后的大 CSV 再上传到 GitHub**。



## 七、版权与数据包范围

原始数据源链接见第二节，来源卡片和可用许可证资料见 `provenance/`。上游仓库声明 MIT 不必然意味着所有第三方游戏简介或图片都具有同样的再分发许可，应遵循原始来源的使用条款。

**本数据包只包含处理后的固定训练数据、元数据、加载/校验脚本和实验说明
