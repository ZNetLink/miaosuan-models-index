# MiaoSuan Model Index

用于 MiaoSuan 网络仿真系统的“模型市场”索引仓库：

- `models/`: 基础模型清单（每模型一个 JSON）
- `packages/`: 模型包清单（可一次安装多个模型）
- `index.json`: 自动生成的快速索引（请勿直接修改）
- `schema/`: 三类 JSON 的 Schema（用于格式检查）
- `scripts/`: 生成与校验脚本

## 快速开始

- 浏览 `models/` 与 `packages/` 获取可用内容
- 通过 PR 向市场提交你的模型或模型包
- 合并到 `master` 后，`index.json` 将由 GitHub Actions 自动生成

## JSON Schema

- 模型 Schema：`schema/model.schema.json`
- 模型包 Schema：`schema/package.schema.json`
- 索引 Schema：`schema/index.schema.json`

注意：模型与模型包均新增必填字段 `repo_url`（代码仓库 URL），生成的 `index.json` 也会包含该字段。

## 贡献

请参考 [CONTRIBUTING.md](CONTRIBUTING.md) 获取提交流程、规范与示例。
