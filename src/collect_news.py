#!/usr/bin/env python3
"""Collect a small, reproducible digest from public RSS/Atom feeds."""

from __future__ import annotations

import argparse
import html
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class Feed:
    topic: str
    url: str


FEEDS = (
    Feed("AI", "https://export.arxiv.org/rss/cs.AI"),
    Feed("量子计算", "https://export.arxiv.org/rss/quant-ph"),
    Feed("机器人", "https://export.arxiv.org/rss/cs.RO"),
    Feed("Web3 与密码学", "https://export.arxiv.org/rss/cs.CR"),
)


def text(node: ET.Element | None) -> str:
    if node is None:
        return ""
    return " ".join("".join(node.itertext()).split())


def fetch(feed: Feed, limit: int = 8) -> list[dict[str, str]]:
    request = urllib.request.Request(
        feed.url,
        headers={"User-Agent": "frontier-tech-research/1.0 (GitHub Actions)"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        root = ET.fromstring(response.read())

    entries = root.findall(".//item") or root.findall(".//{http://www.w3.org/2005/Atom}entry")
    result = []
    for entry in entries[:limit]:
        title = text(entry.find("title"))
        link_node = entry.find("link")
        link = text(link_node)
        if not link and link_node is not None:
            link = link_node.attrib.get("href", "")
        date = text(entry.find("pubDate")) or text(entry.find("{http://www.w3.org/2005/Atom}published"))
        summary = text(entry.find("description")) or text(entry.find("{http://www.w3.org/2005/Atom}summary"))
        result.append({"title": html.unescape(title), "link": link, "date": date, "summary": html.unescape(summary)[:280]})
    return result


def build_digest() -> str:
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# 前沿技术资讯摘要",
        "",
        f"> 最近生成：{generated_at}。内容来自公开 RSS/Atom 源，由 GitHub Actions 自动更新。",
        "> 该摘要用于研究线索发现，不代表项目组对内容或结论的背书。",
        "",
    ]
    for feed in FEEDS:
        lines.extend([f"## {feed.topic}", ""])
        try:
            items = fetch(feed)
        except Exception as exc:  # Keep other feeds useful when one source is unavailable.
            lines.extend([f"暂时无法读取 `{feed.url}`：`{type(exc).__name__}`。", ""])
            continue
        if not items:
            lines.extend(["本轮没有返回条目。", ""])
            continue
        for item in items:
            title = item["title"] or "无标题"
            link = item["link"] or feed.url
            lines.append(f"- [{title}]({link})")
            if item["date"]:
                lines.append(f"  - 时间：{item['date']}")
            if item["summary"]:
                lines.append(f"  - 摘要：{item['summary']}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("data/frontier-tech-news.md"))
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(build_digest(), encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
