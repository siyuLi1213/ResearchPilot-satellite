# ResearchPilot-satellite

ResearchPilot-satellite 是一个面向科研辅助场景的 Dify Workflow 作品集。项目通过问题分类编排论文 RAG、代码问答和高光谱波段选择，并使用 FastAPI HTTP Tool Calling 连接公开演示后端。

本仓库展示工作流设计、RAG 编排、接口契约、传统波段选择算法和发布前安全处理。仓库不包含 PaviaU 数据、固定训练划分、凭据或未发表实验结果。

## 三条工作流

1. **论文 RAG**：检索 Dify 知识库，将召回上下文交给 LLM 生成论文相关回答。
2. **代码问答**：代码类问题进入独立 LLM 节点，用于解释、调试和优化建议。
3. **波段选择**：Dify 以 `PaviaU / fisher / k=10` 调用 FastAPI `/select-bands`，再由 LLM 解释结构化响应。

公开 DSL 保留 10 个节点、9 条连线和三条任务分支。知识库 ID 与 HTTP 地址使用待重新绑定的安全占位值。

## 公开后端与算法

`backend/neurospec/baselines/` 原样收录科研项目中实际使用的七个基础文件，包括公共校验协议和六种传统波段选择实现：

- Fisher Score
- mRMR
- MVPCA
- Information Entropy
- seeded Random
- Uniform spacing

算法文件保留原文件名和实现，没有重新编写。`backend/selector_registry.py` 只负责把 FastAPI 请求分派到这些原始模块。算法接收二维训练矩阵并返回零基原始波段索引。公开 FastAPI 演示为了避免发布科研数据，会在确定性合成数据上运行上述真实算法。响应始终包含：

```json
{
  "demo": true,
  "data_source": "synthetic",
  "note": "...not a PaviaU experiment result."
}
```

因此公开接口可以验证算法调用链和返回契约，但其波段索引不是 PaviaU 实验结果。

## 本地运行

建议使用 Python 3.11 或 3.12：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
uvicorn backend.main:app --reload
```

打开 `http://127.0.0.1:8000/docs` 查看 OpenAPI 页面。运行测试：

```powershell
python -m pytest -q
```

接口示例：

```json
{
  "dataset": "PaviaU",
  "method": "fisher",
  "k": 10
}
```

## 技术栈

- **Dify Workflow**：分类、分支编排、知识检索、HTTP 调用和结果生成
- **RAG**：论文资料召回；知识库内容和真实 ID 不进入仓库
- **FastAPI + Pydantic**：请求校验、OpenAPI 和结构化响应
- **NumPy + scikit-learn**：传统波段选择算法
- **pytest + GitHub Actions**：合成数据单元测试与持续集成

## 仓库结构

```text
ResearchPilot-satellite/
├─ backend/
│  ├─ neurospec/baselines/
│  ├─ main.py
│  ├─ mock_selector.py
│  ├─ selector_registry.py
│  ├─ schemas.py
│  └─ requirements.txt
├─ tests/
│  ├─ test_backend_algorithms.py
│  ├─ test_backend_api.py
│  └─ test_public_artifacts.py
├─ workflow/ResearchPilot-Public.yml
├─ screenshots/workflow.png
├─ examples/
├─ docs/
├─ reports/
├─ requirements-dev.txt
└─ .github/workflows/tests.yml
```

## Dify 导入验证

公开 DSL 已在本地 Dify 界面成功导入。截图可核对 10 个节点、9 条连线，以及论文 RAG、代码问答、波段选择三条完整分支。

![Dify Workflow 导入验证](screenshots/workflow.png)

该截图验证 DSL 导入和工作流结构。知识库、LLM 与部署后的 HTTP 服务仍需在目标环境重新配置和运行验证。

## 导入后设置

1. 在 Dify 导入 `workflow/ResearchPilot-Public.yml`。
2. 在知识检索节点重新绑定有权使用的知识库。
3. 为分类器和 LLM 节点配置模型提供商及凭据。
4. 将 HTTP Request 节点的占位 URL 改为已部署 FastAPI 服务地址。
5. 使用 `/health` 和 `/docs` 检查服务，再执行端到端验证。

