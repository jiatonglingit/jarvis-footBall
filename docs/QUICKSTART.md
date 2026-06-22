# 快速开始

## 在线体验（推荐）

访问 [https://www.jarvis-ai-club.com](https://www.jarvis-ai-club.com) 获取完整功能，无需安装。

---

## 本地 Demo

本仓库 Demo 展示 **ELO + Poisson** 核心数学模型，不含 AI 研报与数据库。

### 环境要求

- Python 3.10+
- pip

### 安装步骤

```bash
git clone https://github.com/jiatonglingit/jarvis-footBall.git
cd jarvis-footBall

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 运行

**默认比赛（德国 vs 科特迪瓦）：**

```bash
python demo/predict.py
```

**自定义比赛：**

```bash
python demo/predict.py \
  --home "Argentina" \
  --away "Mexico" \
  --home-elo 2140 \
  --away-elo 1880
```

**批量示例：**

```bash
python demo/predict.py --batch
```

---

## 与官网的差异

| 功能 | 本地 Demo | 官网 |
|------|----------|------|
| Poisson + ELO 预测 | ✅ | ✅ |
| DeepSeek AI 研报 | ❌ | ✅ |
| 104 场世界杯赛程 | ❌ | ✅ |
| Monte Carlo 模拟 | ❌ | ✅ |
| 命中历史验证 | ❌ | ✅ |
| 会员 / 积分体系 | ❌ | ✅ |

---

## 常见问题

**Q: 为什么本地结果与官网不完全一致？**  
A: Demo 使用简化模型与示例 ELO，官网使用实时 ELO + 有效 ELO 修正 + 更多特征。

**Q: 可以接入真实 API 吗？**  
A: 本仓库 intentionally 不包含 API 密钥与数据库连接。完整功能请使用官网。

**Q: 如何贡献？**  
A: 欢迎提交 Issue 建议功能，或 PR 改进 Demo 文档。核心产品代码不在本仓库维护。
