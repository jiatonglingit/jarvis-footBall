#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jarvis-FootBall · Poisson + ELO 演示脚本

本脚本为教育用途，展示官网使用的核心数学模型（公开公式）。
不包含生产环境 API、数据库连接或 AI Prompt。

完整功能请访问: https://www.jarvis-ai-club.com
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
from scipy.stats import poisson

# ── 模型参数（与官网方法论一致，公开常量） ──
BASE_LAMBDA = 1.30
ALPHA = 0.18
ELO_HOME_BONUS = 55.0
LAMBDA_MIN = 0.15
LAMBDA_MAX = 6.0
MAX_GOALS = 5

WEBSITE = "https://www.jarvis-ai-club.com"


def lambda_from_elo(elo_self: float, elo_opp: float, home_bonus: float = 0.0) -> float:
    """ELO 差 → 预期进球 λ"""
    raw = BASE_LAMBDA + (ALPHA * (elo_self - elo_opp + home_bonus)) / 100.0
    return float(np.clip(raw, LAMBDA_MIN, LAMBDA_MAX))


def wdl_from_elo(elo_home: float, elo_away: float, home_bonus: float = ELO_HOME_BONUS) -> Tuple[float, float, float]:
    """对数 ELO 模型 → 胜平负概率"""
    dr = elo_home - elo_away + home_bonus
    p_home = 1.0 / (1.0 + 10 ** (-dr / 400))
    p_away = 1.0 / (1.0 + 10 ** (dr / 400))
    p_draw = 1.0 - p_home - p_away
    # 重新归一化
    total = p_home + p_draw + p_away
    return p_home / total, p_draw / total, p_away / total


def score_matrix(home_xg: float, away_xg: float) -> Dict[Tuple[int, int], float]:
    """Poisson 比分概率矩阵"""
    probs: Dict[Tuple[int, int], float] = {}
    for i in range(MAX_GOALS + 1):
        for j in range(MAX_GOALS + 1):
            probs[(i, j)] = poisson.pmf(i, home_xg) * poisson.pmf(j, away_xg)
    return probs


def predict(home_team: str, away_team: str, elo_home: float, elo_away: float, *, home_advantage: bool = True) -> dict:
    bonus = ELO_HOME_BONUS if home_advantage else 0.0
    home_xg = lambda_from_elo(elo_home, elo_away, bonus)
    away_xg = lambda_from_elo(elo_away, elo_home, -bonus if home_advantage else 0.0)

    matrix = score_matrix(home_xg, away_xg)

    p_home = sum(p for (i, j), p in matrix.items() if i > j)
    p_draw = sum(p for (i, j), p in matrix.items() if i == j)
    p_away = sum(p for (i, j), p in matrix.items() if i < j)

    top_scores = sorted(matrix.items(), key=lambda x: x[1], reverse=True)[:5]

    return {
        "home_team": home_team,
        "away_team": away_team,
        "elo_home": elo_home,
        "elo_away": elo_away,
        "elo_diff": elo_home - elo_away + bonus,
        "home_xg": round(home_xg, 2),
        "away_xg": round(away_xg, 2),
        "probabilities": {
            "home": round(p_home, 4),
            "draw": round(p_draw, 4),
            "away": round(p_away, 4),
        },
        "top_scores": [
            {"score": f"{i}-{j}", "prob": round(p, 4)}
            for (i, j), p in top_scores
        ],
    }


def bar(prob: float, width: int = 20) -> str:
    filled = int(prob * width)
    return "█" * filled + "░" * (width - filled)


def print_result(result: dict) -> None:
    print("=" * 50)
    print("  Jarvis-FootBall · Poisson + ELO Demo")
    print(f"  完整功能 → {WEBSITE}")
    print("=" * 50)
    print()
    print(f"比赛: {result['home_team']} vs {result['away_team']}")
    print(f"ELO:  {result['elo_home']} vs {result['elo_away']}  (差 {result['elo_diff']:+.0f})")
    print()
    print(f"预期进球: 主 {result['home_xg']} · 客 {result['away_xg']}")
    print()
    print("胜平负概率:")
    probs = result["probabilities"]
    labels = [("home", "主胜"), ("draw", "平局"), ("away", "客胜")]
    for key, label in labels:
        p = probs[key]
        print(f"  {label}  {p*100:5.1f}%  {bar(p)}")
    print()
    print("TOP 5 比分:")
    for i, item in enumerate(result["top_scores"], 1):
        print(f"  {i}. {item['score']}  {item['prob']*100:.1f}%")
    print()
    print(f"→ 访问官网获取 DeepSeek 深度研报与完整 104 场世界杯预测")
    print(f"  {WEBSITE}")


def load_sample_teams() -> list:
    data_path = Path(__file__).parent / "data" / "sample_teams.json"
    with open(data_path, encoding="utf-8") as f:
        return json.load(f)


def run_demo_batch() -> None:
    teams = load_sample_teams()
    print("\n📋 示例比赛批量预测\n")
    for match in teams["matches"]:
        result = predict(
            match["home"],
            match["away"],
            match["elo_home"],
            match["elo_away"],
        )
        probs = result["probabilities"]
        best = max(probs, key=probs.get)
        best_label = {"home": "主胜", "draw": "平局", "away": "客胜"}[best]
        top_score = result["top_scores"][0]["score"]
        print(f"  {match['home']} vs {match['away']}")
        print(f"    → {best_label} ({probs[best]*100:.1f}%) · 最可能比分 {top_score}")
        print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Jarvis-FootBall Poisson + ELO Demo")
    parser.add_argument("--home", type=str, help="主队名称")
    parser.add_argument("--away", type=str, help="客队名称")
    parser.add_argument("--home-elo", type=float, help="主队 ELO")
    parser.add_argument("--away-elo", type=float, help="客队 ELO")
    parser.add_argument("--batch", action="store_true", help="批量运行示例比赛")
    args = parser.parse_args()

    if args.batch:
        run_demo_batch()
        return

    if args.home and args.away and args.home_elo and args.away_elo:
        result = predict(args.home, args.away, args.home_elo, args.away_elo)
    else:
        # 默认：德国 vs 科特迪瓦（2026-06-21 命中示例）
        result = predict("Germany", "Ivory Coast", 2040, 1830)

    print_result(result)


if __name__ == "__main__":
    main()
