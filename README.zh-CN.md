<p align="center"><img src="docs/assets/hero.svg" alt="JevLens：生成之前，先判断证据" width="100%"></p>

<p align="center"><strong>面向 Laya、Jev 和 Ollama 的本地证据决策工作台。</strong><br>让 RAG 先判断证据是否充足，再决定回答、补充证据、拒答或审查冲突。</p>
<p align="center"><a href="README.md">English</a> · <a href="#接入已有-rag-或其他项目">接入已有 RAG</a> · <a href="docs/providers.md">模型接入</a> · <a href="docs/evaluation.md">评测说明</a> · <a href="docs/api.md">API</a></p>

## 为什么做 JevLens

很多 RAG 会把检索到的前几个片段直接交给生成模型。片段包含答案时，这个流程很好理解；但如果它们只是提到同一主题、遗漏关键细节，或者两份政策互相矛盾，就很难判断生成模型是否应该回答。**检索分数表示相关性，不能直接证明证据足以回答问题。**

Jev 和 Laya 等决策模型提供了一个值得实践的思路：把“这份证据是否足够”写成明确的选择题，在生成之前判断。JevLens 将它做成可运行的本地工具：展示真实输入、保存判断、用确定的策略选择路线。开源 Laya 提供自行托管决策模型的路径，Ollama 则方便使用已经下载的本地模型。

核心特色是 **策略回放**：同一份模型判断只做一次，随后拖动支持／冲突阈值，立即查看路线如何变化，**零新增模型调用**。原回答仍属于原策略。这让开发者能先检查一项门控策略的影响，再决定是否在自己的助手里采用它。

名称中的 **Jev** 对应决策模型方向，**Lens** 对应检索与生成之间的证据观察窗口。项目独立于上游，代码和本地流程开源；托管 Jev 是可选提供方。

### 对什么人有用？

| 实际场景                                      | JevLens 提供什么                         | 原项目接下来怎么做                     |
| --------------------------------------------- | ---------------------------------------- | -------------------------------------- |
| 客服助手找到了退款政策                        | 判断它是否包含用户问的期限和办理方式     | 允许回答时，把判断过的片段交给原生成器 |
| 文档提到了 Docker，却没写 Kubernetes 部署步骤 | 显示证据不完整，便于发现检索结果中的缺口 | 补充文档、继续检索或向用户澄清         |
| 两份政策分别写 14 天和 30 天                  | 模型检测到矛盾时提示审查冲突，并展示来源 | 人工核对版本、权威性和适用条件         |
| 想调整助手的回答阈值                          | 在相同判断上回放不同策略                 | 检查路线变化，再用实际标注问题验证     |

它能在阻止回答的路线下跳过生成器，并留下可检查的理由。是否改善事实质量、减少总耗时或成本，需要在你的数据和模型上验证；决策推理本身也有开销。仓库里的少量原创样例用于集成验证，不证明通用性能提升。

![实际工作台：决策分布、证据片段和策略回放](docs/assets/studio.jpg)

_截图来自明确标注的 Demo 模式。演示分数由词法规则模拟，并非真实模型概率。_

## 已实现的功能

| 功能         | 用途                                                                |
| ------------ | ------------------------------------------------------------------- |
| 外部检索接入 | 将已有 RAG 的检索结果发给 `/api/decide`，保留原向量库、框架和生成器 |
| 四类门控     | 回答、补充证据、拒答、审查冲突；生成模型只在允许回答时调用          |
| 开源 Laya    | 接入自行托管的 `/v1/systemone`；默认平均四种循环标签顺序            |
| 本地 Ollama  | 支持已有的 `qwen3.5:4b`，用于判断和带引用的生成                     |
| 托管 Jev     | TypeSafe API Key 保存在服务端                                       |
| 策略回放     | 修改支持／冲突阈值，零模型调用查看路线变化                          |
| 完整记录     | 导出真实输入、证据、分布、策略、引用和耗时                          |
| 无模型演示   | 无需账户、密钥、向量数据库或权重下载                                |
| 本地知识库   | 上传 UTF-8 Markdown／文本，使用 BM25 和中文双字切片检索             |

这是独立应用，与上游均无隶属关系。[Jev](https://docs.typesafe.ai/introduction) 是托管决策模型；[Laya](https://github.com/NandhaKishorM/laya) 是独立开源实现；Ollama 运行生成式模型。三者效果和分布语义不能简单等同。

## 快速开始

需要 Python 3.11+ 和 [uv](https://docs.astral.sh/uv/getting-started/installation/)。适用于 PowerShell、macOS 和 Linux：

```sh
git clone https://github.com/xi029/jev-lens.git
cd jev-lens
uv sync
uv run jevlens demo
uv run jevlens serve
```

打开 **[http://127.0.0.1:8787](http://127.0.0.1:8787)**。默认是清楚标注的词法演示，任何人首次克隆都能体验。

也可以使用已有 Conda 环境，Python 须为 3.11+：

```sh
conda activate agent
python -m pip install -e .
jevlens demo
jevlens serve
```

### 使用已有的 Qwen

启动 Ollama，确认 `ollama list` 中有 `qwen3.5:4b`，无需重复下载。界面选择 **Decision → Ollama · local** 和 **Answer → Ollama · generate**。

默认启动配置可将 `.env.example` 复制为 `.env`，设置：

```dotenv
JEVLENS_PROVIDER=ollama
JEVLENS_OLLAMA_MODEL=qwen3.5:4b
```

Ollama 分数是模型自行估计的结果，**未经校准**，不会伪装成 Jev／Laya 决策头概率。

<details>
<summary>查看真实本地 Qwen 决策和生成截图</summary>

![真实 qwen3.5:4b 决策、回答和证据引用](docs/assets/ollama.jpg)

这是对原创示例资料的真实本地调用。耗时按实际记录展示，速度取决于硬件和并发请求。

</details>

### 使用开源 Laya

```sh
uv sync --extra laya
```

PowerShell 启动服务：

```powershell
$env:LAYA_HOST="127.0.0.1"
$env:LAYA_PORT="8123"
$env:LAYA_MODELS="english"
uv run --extra laya laya-serve
```

另开终端启动 JevLens，选择 **Laya · open weights**。首次需要从 Hugging Face 下载权重；CPU 安装、多语言模型和上下文配置见 [接入文档](docs/providers.md)。

## 三分钟体验

1. 加载示例知识，询问退款申请方式，查看证据和路线。
2. 将支持阈值从 70% 调到 95%，观察回放变化；原回答仍属于原策略。
3. 点击 **Missing detail**，查看价格缺失时如何建议补充资料。
4. 点击 **Add conflicting policy**，观察 14 天与 30 天政策冲突。
5. 上传自己的 `.md`／`.txt` 并导出 JSON。Ctrl／Cmd + Enter 提交。

示例是原创虚构资料。删除草案影响未来检索，旧记录保留当时的证据。

## 工作原理

![检索、决策、门控、响应和零推理回放](docs/assets/architecture.svg)

实现分为五步：

1. **检索**：独立工作台用 BM25 排序 Markdown／文本片段，英文词项和中文双字切片无需下载 embedding；接入已有项目时直接接收它检索到的片段。
2. **判断**：以“充分、部分、缺失、冲突”组成选择题。Laya 默认平均四种循环标签顺序；Jev 使用单次结构化问题；Ollama 返回经过格式验证的 JSON。
3. **门控**：纯函数按照证据、分布和阈值选择路线。空证据拒答；提供方报告上下文截断时阻止生成；随后依次检查冲突与支持阈值。
4. **响应**：工作台在允许回答时展示原文或调用 Ollama；外部接入接口只给出判断，由你的项目决定如何响应。生成引用须指向实际提交的证据 ID。
5. **回放**：保存真实输入、分布、策略和耗时；在原分布上重新计算路线，不检索、不推理、不改写原回答。

后端使用 FastAPI、Pydantic 和 SQLite；界面使用随 Python 包分发的 HTML／CSS／JavaScript，无需 Node 构建。`retrieve_more` 不自动搜索网络；`review_conflict` 不自动判断哪份政策更权威。标签轮换只缓解一种顺序偏差，不能证明分数已经校准。

## 接入已有 RAG 或其他项目

在 **原检索器 → 原生成器** 之间加入 JevLens。向 `POST /api/decide` 传入问题和已经检索到的片段，无需迁移知识库或更换框架。此接口不自行检索、不生成答案、不把片段导入文档集合；它会保存完整判断记录，供工作台查看、导出和回放。

![保留原检索器和生成器，在中间加入证据决策门控](docs/assets/integration.svg)

先运行 `uv run jevlens serve`，再运行以下完整示例，无需密钥：

```python
import httpx

response = httpx.post(
    "http://127.0.0.1:8787/api/decide",
    json={
        "question": "How do I request a refund?",
        "provider": "demo",  # 配置真实提供方后改为 laya 或 ollama。
        "evidence": [
            {
                "id": "refund-1",
                "source": "refund-policy.md",
                "text": "To request a refund, email support with the order number.",
            }
        ],
        "policy": {"support_threshold": 0.70, "conflict_threshold": 0.35},
    },
    timeout=150,
    trust_env=False,
)
response.raise_for_status()  # 门控或提供方报错时停止，不能继续生成。
trace = response.json()
print(trace["action"], trace["reason"])
# 仅当 action == "answer" 时，使用 trace["evidence"] 调用你的生成器。
```

把 `evidence` 换成原项目的向量检索、关键词搜索或框架返回结果即可。生成器应使用**返回的片段**：输入可能为了适配提供方预算被裁剪，判断仅适用于模型实际看到的内容。Demo 是词法模拟；真实使用时应选择真实提供方，并在自己的数据上验证阈值。

| 返回路线          | 你的项目应如何处理                     |
| ----------------- | -------------------------------------- |
| `answer`          | 允许原生成器根据返回的证据回答         |
| `retrieve_more`   | 补充检索、澄清问题或停止；限制重试次数 |
| `abstain`         | 返回证据不足的提示，跳过生成器         |
| `review_conflict` | 交给人工或原项目的来源核对流程         |

仓库包含[可运行接入示例](examples/external_rag.py)。用你已有的检索函数和生成函数替换其中两个回调即可：

```sh
uv run python examples/external_rag.py --provider demo
uv run python examples/external_rag.py --provider demo --question "Who won lunar chess?"
# 已配置本地提供方后：
uv run python examples/external_rag.py --provider ollama
```

示例生成器仅返回原文，方便在无额外模型时体验；门控拒答、需要更多证据、发现冲突或 HTTP 报错时，它都不会运行。需要直接嵌入 Python、不启动 HTTP 服务时，可调用 `run_decision`，见[接入指南](docs/integration.md)。该指南也说明输入限制、错误处理和记录存储。

如果需要一个独立文档助手，使用工作台和 `/api/query`：这条路径包含 BM25 检索与可选的 Ollama 生成。两条路径共用同一套提供方与门控逻辑。

## CLI、Docker 和验证

```sh
uv run jevlens ingest ./my-notes.md
uv run jevlens ask "如何申请退款？" --provider ollama --generate
docker compose up --build
```

Docker 仅向本机暴露端口。容器访问本机模型服务时，须确认服务监听地址能被 Docker 网络访问。希望全部服务只监听 loopback 时，推荐直接使用 Python。

```sh
uv sync --extra dev
uv run ruff check .
uv run ruff format --check .
uv run pytest -q
uv run python scripts/evaluate.py --provider ollama --output artifacts/ollama.json
```

八个原创样例用于路线和集成验证，**不构成通用准确率榜单**。错误和非预期路线均写入报告，见 [评测说明](docs/evaluation.md)。

引用 ID 会验证，但生成内容是否真实、引用是否在语义上支持断言，尚未自动验证。字符预算不保证符合 tokenizer 的上下文限制。项目是单人本地工作台，没有多用户认证或文档 ACL；请阅读 [安全说明](SECURITY.md)。

## 后续方向

- 常见框架的外部检索接入适配器
- 自定义标注集和风险／覆盖率曲线
- 相同证据下比较模型和问题模板
- 可检查的逐条断言支持度验证
- 记录保留期限和脱敏分享

欢迎按 [贡献指南](CONTRIBUTING.md) 提交实用改进。如果方向对你有帮助，Star 能让更多人发现它。

[Apache-2.0](LICENSE)。仓库不分发模型权重，上游各自遵循其许可证。致谢 [Laya](https://github.com/NandhaKishorM/laya)、[TypeSafe API](https://docs.typesafe.ai/api) 和 [Ollama](https://github.com/ollama/ollama)。
