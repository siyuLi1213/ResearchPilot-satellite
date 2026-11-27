# 截图清单

本目录只保存实际运行产生的作品集截图：

| 文件 | 内容 |
|---|---|
| `workflow.png` | Dify 10 节点、9 连线和三条任务分支 |
| `rag-trace.png` | 论文 RAG 的分类、知识检索、LLM 和输出执行追踪 |
| `rag-result.png` | RAG 根据检索上下文生成的论文问答结果 |
| `fastapi-swagger-result.png` | 公开 FastAPI Demo 的 Fisher K=10 Swagger 200 响应 |
| `Fastapi-result.png` | 原始私有科研环境的真实 PaviaU/Fisher Swagger 200 响应 |
| `Fastapi-demo.png` | Dify HTTP 分支调用原始 FastAPI 后的执行追踪和解释结果 |

`fastapi-swagger-result.png` 来自真实 FastAPI 调用，算法运行在确定性合成数据上；响应中的 `demo=true` 与 `data_source=synthetic` 用于避免与私有 PaviaU 实验结果混淆。

`Fastapi-result.png` 与 `Fastapi-demo.png` 是原始私有科研环境的历史联调证据，不是 Mock，也不能由公开仓库复现。图片未展示 OA、AA、F1 或 Kappa 等分类指标，不能据此推断模型性能。

`rag-trace.png` 中的 `host.docker.internal` 是本地 Docker 联调地址，不是公开 DSL 的配置值。全部截图均未显示 API Key、Token、密码、知识库 ID 或本地绝对文件路径。

