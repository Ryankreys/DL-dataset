# Steam + IGDB 多标签数据合并与清洗报告

原始文件、D1 分析、旧训练包不改写。本阶段只生成清洗数据；没有训练模型、向量化或划分数据集。

## 结果

原始 175,855 条；最终 159,066 条标注样本、23 类。默认最小频数 500。
最终条数是去重后的文本-标签观察数，不是已证实的唯一游戏实体数。

## 顺序清洗账目

| 阶段 | Steam | IGDB |
|---|---:|---:|
| 原始记录 | 125,855 | 50,000 |
| 移除缺失/不可读描述 | 8,464 | 9 |
| 再移除原始标签空/非法 | 141 | 0 |
| 再移除排除后标签为空 | 5,609 | 1,602 |
| 再移除缺失 ID | 0 | 0 |
| 进入重复分析 | 111,641 | 48,389 |

初次合并相同描述与相同标签集的重复训练观察：964 条。
稀有标签过滤导致全部标签丢失：0 条；过滤后标签集收敛产生的额外重复：0 条。
顺序移除原因互斥；JSON 的 independent_quality_counts 是独立检查，可重叠，不能与顺序移除数混加。

## 标签映射及排除

使用完整 Genre，忽略 random_genre。Role-playing(RPG) → RPG、Simulator → Simulation、Sport → Sports；复合名称按配置规范。保留 Action 与 Shooter、Strategy 与 Tactical/RTS/TBS、Adventure 与 Point-and-click 的区别。
清理外围空白及标签外层引号，不做语义推断。Platform 沿用原名，不擅自变成其他类型。每个源的每个观测到的标签都有 genre_mapping.csv 记录。

| 排除标签 | 原因 |
|---|---|
| Indie | Production/publishing attribute |
| Free To Play | Pricing model |
| Early Access | Release stage |
| Utilities | Software/tool category |
| Design & Illustration | Software/tool category |
| Animation & Modeling | Software/tool category |
| Education | Software/tool category |
| Video Production | Software/tool category |
| Game Development | Software/tool category |
| Audio Production | Software/tool category |
| Software Training | Software/tool category |
| Photo Editing | Software/tool category |
| Web Publishing | Software/tool category |
| Accounting | Software/tool category |
| Movie | Non-game/video category |
| Documentary | Non-game/video category |
| Episodic | Non-game/video category |
| Short | Non-game/video category |
| Tutorial | Non-game/video category |
| 360 Video | Non-game/video category |
| Violent | Content descriptor |
| Gore | Content descriptor |
| Nudity | Content descriptor |
| Sexual Content | Content descriptor |

Casual、Massively Multiplayer、Music、Quiz/Trivia、Pinball 暂定保留并标记 review，后续可通过配置或 --exclude-genre 排除。Massively Multiplayer 可能更适合作为模式描述。

## 稀有类型阈值对照

阈值基于统一、有效、非类型标签排除且重复训练观察合并后的频数。每条样本每类计一次，不是源 CSV 原始频数。
| 阈值 | 保留类型 | 移除类型 | 至少保留一类的输入样本 | 丢失全部标签 | 额外合并重复 | 最终样本 | 保留率 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 100 | 23 | 0 | 159,066 | 0 | 0 | 159,066 | 100.00% |
| 500 | 23 | 0 | 159,066 | 0 | 0 | 159,066 | 100.00% |
| 1000 | 18 | 5 | 158,268 | 798 | 10 | 158,258 | 99.49% |

阈值 1000 移除标签：Pinball, Point-and-click, Quiz/Trivia, Tactical, Visual Novel。


保留率以 merged_games.csv 为分母。先删除罕见标签，不直接删除仍有其他标签的记录。过滤可能令原本不同的标签集收敛，因此再次合并相同观察，并在需要时重新计算阈值直到稳定；500 是初始实验值，不代表最优。

## 重复处理与溯源

有效数据中相同描述组 698 个，额外描述行 1,316；
跨来源相同描述组 78 个，其中标签冲突组 64 个。
全部相同描述的标签冲突组 295 个，涉及 841 行。

- 在去重之前写出 duplicate_analysis.json、duplicate_groups.jsonl 和重复 ID 报告。
- 只合并清洗描述完全相同且规范后标签集完全相同的重复训练观察；并不认定它们必然是同一游戏。
- 代表记录按 Steam 优先、可用标题、数字/字符串 ID、原始行号确定。所有原始成员通过 record_lineage.csv 保留。
- 相同描述但不同标签集保留为不同观察，不强行取并集、不认定一个来源更正确；这是必须由小组审核的标注差异。
- source 与 game_id 共同标识源记录；IGDB 标题为缺失，不推断游戏名。若有同源 ID 冲突，不擅自覆盖，详见 ID 报告。
- genre_frequency_comparison.csv 是初次重复观察合并后的频数，按代表记录来源归属；steam_count + igdb_count = combined_count。跨源代表记录的其他成员仍见溯源，不应把代表来源比例当作原始来源覆盖率。

## 最终频数

| 类型 | 样本数 |
|---|---:|
| Adventure | 60,360 |
| Casual | 51,224 |
| Action | 47,074 |
| Simulation | 32,162 |
| Strategy | 31,102 |
| RPG | 28,251 |
| Sports | 10,190 |
| Racing | 7,302 |
| Shooter | 6,806 |
| Puzzle | 6,163 |
| Platform | 5,183 |
| Arcade | 3,306 |
| Massively Multiplayer | 2,576 |
| Fighting | 2,375 |
| Hack and Slash / Beat 'em Up | 1,507 |
| Turn-Based Strategy | 1,321 |
| Real-Time Strategy | 1,275 |
| Music | 1,132 |
| Point-and-click | 858 |
| Tactical | 855 |
| Quiz/Trivia | 838 |
| Visual Novel | 561 |
| Pinball | 544 |

## 来源保留情况

| 来源 | 最终代表行 | 代表行 / 原始 | 被代表的原始行 | 原始行覆盖率 |
|---|---:|---:|---:|---:|
| steam | 111,114 | 88.29% | 111,641 | 88.71% |
| igdb | 47,952 | 95.90% | 48,389 | 96.78% |

## 文本与已知限制

HTML/实体/空白清理复用 D1 工具；另排除 null-like 占位符和没有任何字母/数字（含 Unicode）的不可读文本。不设任意长度门槛，不删除停用词、不词干化，保留有用标点和原意；类型词仍在描述中。
split_groups.csv 只提供未来分组依据，没有分配 train/test。忽略大小写、标点、空格的等价描述会在同组，另对共享长前缀/后缀且字符相似度 ≥ 配置值的候选作保守分组；大共享块只分组、不删行。
近重复候选连接数 854，保守大块 1。
该候选检查不是全量语义或实体匹配，仍可能漏掉改写描述，不能宣称已杜绝所有未来泄漏。之后划分必须使用组字段并补充更广泛的近重复审核。标签间覆盖不一致、原始错标、同一游戏不同描述、不同游戏共享模板等风险仍在。
原始 D1 的 619/656 是按忽略大小写的全部可读描述统计，本次重复账目使用有效标签子集和精确文本，分母与定义不同，不能混作相同游戏数量。

## 文件与复现

主数据 schema：source, game_id, title, description, genres。CSV genres 为 JSON 数组，读取时用 json.loads；ID 用字符串读取。
merged_games.csv 是去重后、稀有过滤前的有效记录；cleaned_games.csv 是所选阈值结果。record_lineage.csv 对每个原始行给出处理结果与代表 UID，duplicate_groups.jsonl 保留冲突细节。
```powershell
python scripts/merge_and_clean.py --min-genre-frequency 500
python -m unittest discover -s tests -p test_merge_and_clean.py -v
# 再运行到新目录，避免覆盖旧结果：
python scripts/merge_and_clean.py --min-genre-frequency 1000 --output-dir data/processed/merged_multilabel_1000
```
原始输入 SHA256 前后相同。artifact_checksums.json 可用于比较同一配置重跑的内容；CSV/JSON/Markdown 按确定性顺序生成，不写时间戳。未自动 commit 或 push。
