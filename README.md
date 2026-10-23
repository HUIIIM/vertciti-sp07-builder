# vertciti-sp07-builder

> **历史档案（已封存）**：这是商城时代的 SP-07 生产页构建工具＋机器可读商品数据（2026-09-25）。
> 商城已于 2026-09-30 全线下架（D314），**本仓库不代表任何在售产品或服务**，仅作工程档案保留。

SP-07 生产页的构建脚本与当时的机器可读商品数据，仅供 vertciti 内部工程追溯使用。

| | |
|---|---|
| 状态 | 历史档案（已封存）——2026-09 商城时代产物，商城下线后不再用于任何生产构建 |
| 类型 | 构建工具（Python 单文件脚本 `build-sp07-prod.py`）＋ `machine/` 数据快照 |
| 许可证 | 专有（vertciti clean-room engineering — proprietary，见 [LICENSE](LICENSE)） |
| 语言 | 简体中文 |
| 后继 | README 未指明后继仓库 |
| 联系 | 安全问题见 [.github/SECURITY.md](.github/SECURITY.md) · 产品：[vertciti.com](https://vertciti.com) |

## 它做什么

从 D111-safe 基准 HTML 出发，做 v1.1 logo 语法归一化（零视觉变化）＋ 6 处 SP-07 内容编辑（含 Stripe
付款链接注入），输出 `--dst-dir/index.html`。`rep()` 要求每个锚点**恰好出现 1 次**，否则 `ASSERT FAIL`
直接退出，不静默产出半成品。

架构图、演示 GIF 与截图在 [`docs/assets/`](docs/assets/)。

## 快速开始

```bash
python3 -m py_compile build-sp07-prod.py && echo BUILDER_OK
python3 build-sp07-prod.py --help
# 完整构建需自备基准 HTML（历史产物，未收录）：
python3 build-sp07-prod.py --src /path/to/base.html --dst-dir /path/to/out
```

## machine/：机器可读商品数据（2026-09-25 历史快照）

| 文件 | 内容 |
|---|---|
| `catalog.json` | 6 个标准包（SP-01~SP-06）：范围、交付物、排除项、内测价、下单方式 |
| `categories.json` | 15 个 AI 能力分类（角色/手艺/数据与基建）：定义、交付物、计价模型 |
| `manifest.json` | 总清单：阶段 `human_selected`（人选）、机器下单 `planned`（未开放） |
| `ratings.json` | 供应商评分标准 v1：维度、权重、等级映射（当时评分数据为空） |

数据自带的诚实注脚原样保留："全部为内测价，供应商数量为 0，评分为空；屏障事项明确标注 planned，不伪装成
已上线能力。"

## 状态与边界

- 构建器与数据均为 2026-09 商城时代产物；价格、阶段、评分状态均为历史快照，不代表现状。
- 没有基准 HTML 就不跑完整构建，本仓不收录构建产物。
- CI（`.github/workflows/`）：`py_compile`＋ shellcheck、CodeQL、dependency-review、gitleaks、Scorecard。

## 贡献

本仓库为 vertciti 内部工程档案，暂不接受外部 PR；发现问题请走内部渠道。

## 许可证

vertciti clean-room engineering — proprietary。详见 [LICENSE](LICENSE)。

Built by vertciti — https://vertciti.com
