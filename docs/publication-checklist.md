# 发布检查表

## 必须人工确认

- [ ] 在目标 Dify 版本中成功导入公开 DSL。
- [ ] “知识检索”节点已重新绑定到可公开使用的知识库。
- [ ] 所有 LLM 节点已重新选择可用模型，且凭据只保存在 Dify 的安全配置中。
- [ ] HTTP URL 已替换为部署环境可达的 HTTPS 地址。
- [ ] FastAPI 服务、`neurospec-agent`、数据集和训练划分仍位于私有环境。
- [ ] `examples/response.example.json` 被理解为人工构造示意，不是实验结果。
- [ ] 截图已逐张检查，不含账号、知识库 ID、Token、本地路径或未发表材料。
- [ ] 用 GitHub 提交前扫描工具再次检查完整暂存区。

## 不得加入仓库

- `.env`、API Key、Token、密码、证书或私钥。
- PaviaU 或其他私有/受限数据文件。
- 训练划分、实验结果、模型权重、缓存和日志。
- `neurospec-agent` 源码或未授权算法实现。
- 未发表论文正文、图表、指标或审稿材料。

## 建议的本地 Git 步骤

```powershell
Set-Location '<本项目目录>'
git init
git status --short
git add --dry-run .
git diff --cached --check
```

确认无误后，可将该目录提交到你已有的**私有** GitHub 仓库。首次上传前仍应在 GitHub 网页确认仓库可见性为 Private。本次整理没有执行 `git push`、创建远程仓库或修改远程设置。

