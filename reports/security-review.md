# 安全审查

审查日期：2026-11-27（Asia/Seoul）

## 公开范围

- Dify Workflow DSL、结构截图和接口示例。
- FastAPI 请求/响应模型及 `/health`、`/select-bands` 路由。
- 从原科研项目逐文件复制且未改写的 `base.py`、Fisher、mRMR、MVPCA、Information Entropy、Random、Uniform 模块。
- 仅使用确定性合成矩阵的演示适配器和单元测试。

## 未纳入仓库

- PaviaU 或其他数据集文件。
- 固定训练、验证和测试划分。
- SFFS、实验流水线、调参流程、检查点和实验结果。
- 本机科研项目路径、配置文件和未发表材料。
- `.env`、API Key、Token、密码、证书或私钥。

## 脱敏和边界

- Dify 知识库 ID 使用 `REBIND_KNOWLEDGE_BASE_AFTER_IMPORT`。
- DSL 的 HTTP URL 使用 `https://researchpilot-api.example.invalid/select-bands`。
- 公开 API 接受与 Dify 相同的 `PaviaU / method / k` 请求契约，但明确返回 `demo=true` 和 `data_source=synthetic`。
- 算法实现是真实可执行代码；公开接口输出来自合成数据，不是 PaviaU 实验结果。

## 扫描结果

- 新增后端和测试中没有数据文件、模型权重或实验结果文件。
- 当前文件及 13 个 Git 历史提交的高信号凭据扫描无实际凭据命中；测试文件中只存在用于检测凭据的正则表达式文本。
- 公开 DSL 中没有本地 Docker 主机名、回环地址或原知识库 ID。
- 公开文件中没有原科研项目的绝对 Windows 路径。

## 截图人工检查

- `workflow.png`：公开 Dify 工作流结构完整，HTTP 节点显示脱敏占位地址。
- `rag-trace.png`：显示真实 RAG 执行追踪及本地 Docker 联调地址 `host.docker.internal`；未显示凭据、知识库 ID 或绝对文件路径。
- `rag-result.png`：显示论文问答结果，未显示凭据或未公开实验指标。
- `fastapi-swagger-result.png`：来自真实 FastAPI Swagger 请求，响应明确标注合成数据 Demo，不描述为 Mock 或 PaviaU 运行结果。
- `Fastapi-result.png`：原始私有环境的真实 PaviaU/Fisher Swagger 200 响应；未显示凭据、训练样本内容或分类指标，README 未将其描述为 Mock 或公开 Demo。
- `Fastapi-demo.png`：Dify HTTP 分支调用原始 FastAPI 的真实执行追踪；未显示凭据，README 明确其私有环境边界。

## 功能限制

- 知识库、LLM 和部署后的 HTTP 地址仍需在目标 Dify 环境配置。
- 公开 API 用合成数据验证接口和算法调用链，不复现论文实验。
- 数据使用权、部署凭据和真实科研运行环境不属于本仓库。

