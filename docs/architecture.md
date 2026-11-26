# 系统架构与边界

```mermaid
flowchart LR
    U[浏览器 / Dify UI] --> S[用户输入]
    S --> C{问题分类器}
    C -->|论文问题| K[Dify 知识检索]
    K --> R[论文 RAG LLM]
    C -->|代码问题| Q[代码问答 LLM]
    C -->|波段选择任务| H[HTTP Request]
    H --> A[FastAPI /select-bands]
    A --> P[波段选择服务适配层]
    P --> N[neurospec-agent]
    N --> D[(授权数据与固定训练划分)]
    A --> B[结果解释 LLM]
    R --> O[输出]
    Q --> O
    B --> O

    subgraph Public[可公开展示范围]
      U
      S
      C
      K
      R
      Q
      H
      B
      O
    end

    subgraph Compute[科研计算服务]
      A
      P
      N
      D
    end
```

## 职责边界

- 浏览器与 Dify 负责交互和确定性工作流编排。
- Dify 知识检索节点负责从重新绑定的论文知识库召回上下文；公开仓库不含知识库内容和真实 ID。
- LLM 节点负责分类、论文回答、代码回答和接口结果解释；模型凭据由部署者在 Dify 中配置。
- FastAPI 只暴露受控请求模型和算法调用入口，服务适配层提供 `/health` 与 `POST /select-bands`。
- `neurospec-agent` 与服务适配代码可以在完成授权和安全复核后发布；数据文件、凭据和未发表实验材料仍不纳入本仓库。

## 波段选择数据流

公开 DSL 的 HTTP 节点固定发送 `dataset=PaviaU`、`method=fisher`、`k=10`。FastAPI 校验请求后调用波段选择服务适配层，再返回索引和运行元数据。示例响应不来自现场执行，不代表任何论文指标。

## 可迁移性说明

公开 DSL 使用保留域名 `researchpilot-api.example.invalid`，避免泄露或误连本地服务。知识库 ID 使用显式占位值。两者均需在导入后的 Dify UI 中重新绑定。虽然 YAML 和图结构已检查，当前尚未在目标 Dify 版本中完成导入验证。

