# v0.1.0-demo

首个公开 Demo 版本，用于 GitHub 引流与技术展示。

## 包含内容

- **推广 README**：项目介绍、界面预览、命中率展示、官网链接
- **Poisson + ELO 演示脚本**（`demo/predict.py`）：可本地运行，展示核心数学模型
- **公开方法论**（`docs/METHODOLOGY.md`）：与官网一致的公式说明
- **GitHub Pages 落地页**（`docs/index.html`）：自动跳转官网

## 快速开始

```bash
git clone https://github.com/jiatonglingit/jarvis-footBall.git
cd jarvis-footBall
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python demo/predict.py
```

## 与官网的差异

| 功能 | Demo | 官网 |
|------|------|------|
| Poisson + ELO | ✅ | ✅ |
| DeepSeek AI 研报 | ❌ | ✅ |
| 104 场世界杯 | ❌ | ✅ |
| Monte Carlo 模拟 | ❌ | ✅ |
| 命中历史验证 | ❌ | ✅ |

## 在线体验

👉 [https://www.jarvis-ai-club.com](https://www.jarvis-ai-club.com)

## 声明

本仓库仅供学术研究与技术展示，不构成任何形式的投注建议。
