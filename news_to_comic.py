#!/usr/bin/env python3
"""Simple script to fetch news, summarize, and generate a 4-panel comic."""

import re
import textwrap
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont


def fetch_article_text(url: str) -> str:
    """Fetch article text from the given URL."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    paragraphs = [p.get_text() for p in soup.find_all("p")]
    return "\n".join(paragraphs)


def simple_summarize(text: str, sentences: int = 4) -> list[str]:
    """Return the first few sentences as a crude summary."""
    cleaned = re.sub(r"\s+", " ", text)
    split = re.split(r"(?<=[.!?]) +", cleaned)
    return split[:sentences]


def make_comic(lines: list[str], output: str) -> None:
    """Create a 4-panel comic image from provided lines."""
    width, height = 800, 800
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    panel_h = height // 4
    for i, line in enumerate(lines):
        y0 = i * panel_h
        draw.rectangle([(0, y0), (width - 1, y0 + panel_h)], outline="black")
        wrapped = textwrap.fill(line, width=40)
        draw.multiline_text((10, y0 + 10), wrapped, fill="black", font=font)

    img.save(output)


def main():
    url = "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"
    feed = requests.get(url, timeout=10)
    feed.raise_for_status()
    soup = BeautifulSoup(feed.text, "xml")
    first_link = soup.find("item").find("link").get_text()
    article_text = fetch_article_text(first_link)
    summary = simple_summarize(article_text, 4)
    make_comic(summary, "comic.png")
    print("Saved comic.png")


if __name__ == "__main__":
    main()
