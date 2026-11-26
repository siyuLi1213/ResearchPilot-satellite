# 验证报告

验证日期：2026-11-26（Asia/Seoul）

## 结果摘要

| 检查 | 结果 | 说明 |
|---|---|---|
| 公开 YAML 解析 | PASS | PyYAML 可解析 |
| 本地 Dify 导入 | PASS | 10 个节点、9 条连线和三条分支完整 |
| 示例 JSON 解析 | PASS | 请求和示例响应均可解析 |
| Python 环境 | PASS | Python 3.14 隔离环境安装依赖成功，`pip check` 无冲突 |
| pytest | PASS | `16 passed in 3.00s` |
| FastAPI 健康检查 | PASS | `/health` 返回公开演示标识 |
| FastAPI 请求校验 | PASS | 合法 Fisher K=10 请求成功，非法 K 返回 422 |
| 六种算法接口 | PASS | 均返回唯一、零基、范围有效的波段索引 |
| 原始算法一致性 | PASS | 7 个基础/算法文件与科研项目源文件 SHA-256 一致 |
| Fisher 合成测试 | PASS | 可分离波段获得最高得分 |
| Random 复现性 | PASS | 固定种子得到一致结果 |
| 演示结果标记 | PASS | 响应包含 `demo=true`、`data_source=synthetic` 和非 PaviaU 声明 |
| 敏感信息扫描 | PASS | 无真实凭据、绝对科研路径、数据或结果文件 |

测试命令：

```powershell
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

测试产生一条上游 Starlette `TestClient` 弃用警告，不影响 16 项测试结果或接口行为。

## Dify 结构验证

- 本地 Dify 界面显示 10 个节点和 9 条连线。
- 论文 RAG、代码问答、波段选择三条分支完整。
- HTTP Request 节点使用脱敏占位地址。
- 验证截图：`screenshots/workflow.png`。

## 尚未覆盖

- 知识库检索和收费 LLM 调用没有进行公开环境端到端测试。
- 公开 FastAPI 没有连接 PaviaU、固定训练划分或科研结果目录。
- 没有把合成数据结果当作真实 Fisher/PaviaU 实验结果。

