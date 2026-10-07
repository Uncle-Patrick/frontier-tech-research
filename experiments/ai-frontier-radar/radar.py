#!/usr/bin/env python3
"""A tiny, explainable baseline for ranking frontier-tech research signals."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


KEYWORDS = {
    "AI": ("transformer", "agent", "multimodal", "reasoning", "llm", "diffusion"),
    "Web3": ("zero-knowledge", "zk", "blockchain", "smart contract", "decentralized"),
    "量子计算": ("quantum", "qubit", "error correction", "量子"),
    "机器人": ("robot", "embodied", "manipulation", "autonomous", "机器人"),
}


def score(title: str, summary: str) -> list[tuple[str, int]]:
    haystack = f"{title} {summary}".lower()
    results = []
    for topic, keywords in KEYWORDS.items():
        hits = sum(len(re.findall(re.escape(keyword.lower()), haystack)) for keyword in keywords)
        if hits:
            results.append((topic, hits))
    return sorted(results, key=lambda item: (-item[1], item[0]))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("text", nargs="?", default="data/frontier-tech-news.md")
    args = parser.parse_args()
    content = Path(args.text).read_text(encoding="utf-8")
    print("Frontier-tech radar baseline")
    for line in content.splitlines():
        if line.startswith("- ["):
            title = line.split("](", 1)[0].removeprefix("- [")
            tags = score(title, line)
            if tags:
                print(f"{title} :: {', '.join(f'{topic}={points}' for topic, points in tags)}")


if __name__ == "__main__":
    main()
