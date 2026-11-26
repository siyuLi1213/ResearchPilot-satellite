# 验证报告

验证日期：2026-11-26（Asia/Seoul）

## 结果摘要

| 检查 | 结果 | 说明 |
|---|---|---|
| 公开 YAML 解析 | PASS | PyYAML 6.0.3 可解析 |
| 本地 Dify 导入 | PASS | 公开 DSL 已在本地 Dify 界面成功导入 |
| 示例 JSON 解析 | PASS | 2 个 JSON 文件均可解析 |
| pytest | PASS | `4 passed in 0.15s` |
| 节点数量 | PASS | 原始与公开版本均为 10 |
| 连线数量 | PASS | 原始与公开版本均为 9 |
| 节点 ID 与连线 | PASS | ID 集合一致，无悬空端点 |
| 分类分支 | PASS | 3 个分类 ID 与 3 条分支 handle 一致 |
| Prompt 逻辑 | PASS | 所有节点的 `prompt_template` 与原始版本一致 |
| 语义差异范围 | PASS | 仅知识库 ID 与 HTTP URL 两项发生变化 |
| Fisher 固定请求 | PASS | `PaviaU / fisher / k=10` |
| HTTP 地址脱敏 | PASS | 截图显示保留域名占位地址 |
| 原私有绑定残留 | PASS | 原知识库 ID、原 HTTP URL 均未出现在公开 DSL |
| 本地路径与主机扫描 | PASS | 无绝对 Windows 路径或本地主机名命中 |
| 高信号密钥扫描 | PASS | 常见私钥、云密钥、GitHub Token、API Key 模式无命中 |

## 工作流结构

- 节点类型：start 1、question-classifier 1、knowledge-retrieval 1、http-request 1、llm 3、end 3。
- 论文分支：分类器 → 知识检索 → RAG LLM → 输出。
- 代码分支：分类器 → 代码问答 LLM → 输出。
- 波段分支：分类器 → HTTP Request → 结果解释 LLM → 输出。

## 可执行测试

在项目根目录执行：

```powershell
python -m pytest -q
```

测试覆盖 JSON/YAML 解析、图端点完整性、分类分支、公开占位绑定、固定 Fisher 请求和高信号敏感模式。

## Dify 导入验证

- 本地 Dify 界面显示 10 个节点完整。
- 9 条节点连线完整。
- 论文 RAG、代码问答、波段选择三条分支完整。
- HTTP Request 节点使用脱敏占位地址。
- 验证截图：`screenshots/dify-workflow-demo.png`。

以上结论只覆盖 DSL 导入和工作流结构，不代表知识库、LLM 或 HTTP/FastAPI 接口已经完成端到端运行验证。

## 未执行或未验证

- 未启动私有 FastAPI，也未运行真实 Fisher。当前检查环境为 Python 3.9.13，而私有 `neurospec-agent` 明确要求 Python `>=3.14,<3.15`；真实运行还依赖私有数据与固定训练划分。
- 未调用公网、收费模型 API 或远程 GitHub。
- 未生成截图。

## 人工复核项

在其他 Dify 环境使用时仍需重新绑定知识库、模型提供商和 HTTP 服务地址。发布前还需人工检查截图与 Git 暂存区。

