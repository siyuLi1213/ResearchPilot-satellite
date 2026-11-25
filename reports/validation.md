# 验证报告

验证日期：2026-11-25（Asia/Seoul）

## 结果摘要

| 检查 | 结果 | 说明 |
|---|---|---|
| 公开 YAML 解析 | PASS | PyYAML 6.0.3 可解析 |
| 示例 JSON 解析 | PASS | 2 个 JSON 文件均可解析 |
| pytest | PASS | `4 passed in 0.14s` |
| 节点数量 | PASS | 原始与公开版本均为 10 |
| 连线数量 | PASS | 原始与公开版本均为 9 |
| 节点 ID 与连线 | PASS | ID 集合一致，无悬空端点 |
| 分类分支 | PASS | 3 个分类 ID 与 3 条分支 handle 一致 |
| Prompt 逻辑 | PASS | 所有节点的 `prompt_template` 与原始版本一致 |
| 语义差异范围 | PASS | 仅知识库 ID 与 HTTP URL 两项发生变化 |
| Fisher 固定请求 | PASS | `PaviaU / fisher / k=10` |
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

## 未执行或未验证

- 未在 Dify UI 中导入 DSL，因此导入兼容性标记为**未验证导入**。
- 未启动私有 FastAPI，也未运行真实 Fisher。当前检查环境为 Python 3.9.13，而私有 `neurospec-agent` 明确要求 Python `>=3.14,<3.15`；真实运行还依赖私有数据与固定训练划分。
- 未调用公网、收费模型 API 或远程 GitHub。
- 未生成截图。

## 人工复核项

导入后需要重新绑定知识库、模型提供商和 HTTP 服务地址，并确认目标 Dify 版本接受占位配置。发布前还需人工检查截图与 Git 暂存区。

