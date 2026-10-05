# 游戏类型多标签数据集：GitHub 上传目录

本目录是可独立上传、下载和使用的数据集。Steam 与 IGDB 分开，保留全部记录、
原始多标签和重复描述。没有合并 taxonomy、删掉 Indie 等标签或创建建模划分。
旧文件及上传包保持不变。

| 来源 | 全部记录 | 描述与标签可用 | 原始标签数 |
|---|---:|---:|---:|
| Steam | 125,855 | 117,251 | 33 |
| IGDB | 50,000 | 50,000 | 21 |

## 文件结构

```text
data/
  raw/steam/                   # 原始 CSV 的无损 gzip 字节分片和来源说明
  raw/igdb/                    # 原始 CSV 的无损 gzip 字节分片和来源、许可
  raw/source_manifest.json     # 原始下载版本与校验和
  processed/steam/             # Parquet 存储分片，合起来就是完整 Steam 数据
  processed/igdb/              # Parquet 存储分片，合起来就是完整 IGDB 数据
  processed/steam_labels.json  # 原始 33 类的名称与多热编码顺序
  processed/igdb_labels.json   # 原始 21 类的名称与多热编码顺序
  summary/                    # 小型统计 CSV
restore_raw.py
load_data.py
raw_parts_manifest.json
manifest.json
```

所有上传文件小于 20 MiB；无须 Git LFS，也不要上传原项目的大 ZIP。
GitHub 官方文件限制：https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository
请上传本目录全部内容并保持层级。可以通过 Add file → Upload files 拖入文件夹，
或使用 GitHub Desktop/Git。GitHub 网页每次最多上传 100 个文件。

## 后续处理：直接读取 Parquet

```powershell
pip install -r requirements.txt
python load_data.py --source steam
python load_data.py --source igdb
```

```python
import pandas as pd
steam = pd.read_parquet("data/processed/steam")
igdb = pd.read_parquet("data/processed/igdb")
```

这些是文件存储分片，不是 train/validation/test 划分。每个目录直接读成一张完整表。
核心字段：game_id、name、description、genres、source。
description 是最小 HTML/实体/空白处理后的输入；description_raw 和 genres_raw
保留源字段原文。genres 是完整原始名称数组，labels 是多热向量，label_ids 是
正标签位置。Steam 33 类、IGDB 21 类编码各自独立，不能直接拼接混用。
缺失标签的编码为 null，不是全负类；training_usable 标记可用于当前监督训练的
记录，但文件没有删除其他记录。IGDB 名称缺失，ID 是源 CSV 内部记录 ID。
日期和开发商等辅助字段保持源字符串；tags/image_url 不作为主要模型输入。

小组之后需要决定目标 taxonomy 和描述分组划分；完全相同描述应留在同一个
划分内。不要对同一全量文件训练后直接报告测试性能。

## 从原始数据重新做预处理

```powershell
python restore_raw.py
# 或只还原一个来源：python restore_raw.py --source steam
```

生成 restored_raw/steam/games.csv 和 restored_raw/igdb/Dataset.csv。
还原结果与最初下载 CSV 字节完全一致，并校验 SHA256。
gzip 分片可能在字符或记录中间切开，不能把单片当作独立 CSV 读取；必须先用
restore_raw.py 按清单顺序拼接。此处理只用于规避上传大小限制，不改写源内容。
Steam 原始 CSV 的 DiscountDLC count 合并表头错误也原样保留；重新解析时应
仅在内存中把它拆为 Discount、DLC count，避免后续列错位。
还原出的超大 CSV 已被 .gitignore 排除，不需要重新提交 GitHub。

## 来源和许可

- Steam：https://huggingface.co/datasets/FronkonGames/steam-games-dataset
- IGDB 镜像：https://github.com/yuhangjiang22/video-game-genre-classificaion

来源数据卡/仓库声明 MIT；其说明文件和可获得的原许可证保存在 raw 中。
这不独立确认所有第三方描述、图片的权利。版本、文件校验和、完整记录数及
原文件未改写的验证结果见 manifest.json 与 source_manifest.json。
本目录没有额外下载图片，也没有模型预测结果。
