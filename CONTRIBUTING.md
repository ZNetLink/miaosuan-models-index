# 贡献指南（模型/模型包提交流程）

非常欢迎向 MiaoSuan Model Index 提交模型与模型包！请按照下面流程与规范进行：

## 仓库结构

- `models/`: 单个基础模型的清单文件（每个模型一个 JSON 文件，文件名即模型 `slug`）
- `packages/`: 模型包的清单文件（一次安装多个模型，文件名即包 `slug`）
- `index.json`: 自动生成的索引，便于快速展示与检索（请勿直接修改）
- `schema/`: 三类 JSON 的 JSON Schema（用于格式校验）
- `scripts/`: 辅助脚本（本地校验与生成索引）

## 命名与文件规范

- 文件名（不含扩展名）作为 `slug`，应仅包含小写字母、数字、`-`、`_`：例如 `udp.json`、`basic.json`
- 请不要直接修改 `index.json`，它会在合并到 `master` 后由 GitHub Action 自动生成

## 模型文件（models/*.json）

请参考 `schema/model.schema.json`。关键字段：

- `name`: 人类可读名称（如 "UDP Model"）
- `author`: 作者信息对象 `{ name, email?, url? }`
- `description`: 模型描述
- `license`: 许可证（建议使用 SPDX 标识）
- `labels`: 标签数组（去重）
- `versions`: 版本数组（至少一个），每项包含：
  - `version`: 语义化版本（如 `1.0.0`）
  - `url`: 可下载地址（例如 release 归档）
  - `checksum`: 包校验和（支持 `sha256:<64hex>` 或 64 位 hex）
  - `date`: 发布日期（YYYY-MM-DD）
  - `notes`: 备注（可选）

示例（`models/udp.json`）：

```json
{
  "name": "UDP Model",
  "author": { "name": "ZNetLink", "email": "dev@example.com" },
  "description": "Standard UDP Model",
  "labels": ["UDP", "TCP/IP"],
  "license": "GPL-3.0",
  "versions": [
    {
      "version": "1.0.0",
      "checksum": "sha256:...64hex...",
      "url": "https://.../v1.0.0.zip",
      "date": "2024-06-01",
      "notes": "Initial release of the UDP model."
    }
  ]
}
```

## 模型包文件（packages/*.json）

请参考 `schema/package.schema.json`。关键字段：

- `name`: 人类可读名称
- `author`: 作者信息对象 `{ name, email?, url? }`
- `description`: 包描述
- `labels`: 标签数组（去重）
- `models`: 引用的模型清单数组，元素为：
  - `name`: 模型 `slug`（即 `models/<slug>.json` 的 `<slug>`）
  - `version`: 期望的模型版本（可选，语义化版本）

示例（`packages/basic.json`）：

```json
{
  "name": "Basics",
  "author": { "name": "ZNetLink" },
  "description": "Basic models for testing purposes",
  "labels": ["testing", "basic"],
  "models": [
    { "name": "udp", "version": "1.0.0" }
  ]
}
```

> 说明：当前仅进行“格式校验”，不强制要求引用模型一定存在；合并时由维护者综合判断。

## 开发者本地检查

可选但推荐：

1. 安装 Python 3.9+，并安装依赖：`pip install jsonschema`
2. 运行校验：`python scripts/validate_json.py`

## 提交流程（PR）

1. Fork 本仓库，创建分支
2. 在 `models/` 或 `packages/` 下新增或修改 JSON 文件，遵循上述规范与 Schema
3. 切勿修改 `index.json`
4. 提交 PR；CI 会自动进行 JSON Schema 校验，若 `index.json` 被修改将直接失败

## 合并与索引生成

- PR 合并进入 `master` 后，GitHub Action 会自动扫描 `models/` 和 `packages/` 生成新的 `index.json`

感谢你的贡献！

