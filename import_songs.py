#!/usr/bin/env python3
"""
Basic ABC importer for your solfege tool.

- Reads abcnotation.com (or other) tune URLs
- Downloads raw ABC (using ?f=abc / &f=abc)
- Saves them into ./songs/<slug>.abc
- Updates ./songs/index.json with metadata

Usage examples:

    python import_songs.py --urls-file urls.txt
    python import_songs.py --url https://abcnotation.com/tunePage?a=users.bar/barney/wildrover/0001

urls.txt should contain one URL per line.
"""

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

import requests

SONGS_DIR = Path("songs")
INDEX_PATH = SONGS_DIR / "index.json"


def ensure_abc_url(url: str) -> str:
    """Ensure the URL requests ABC text (add f=abc if needed)."""
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    if "f" not in query:
        query["f"] = ["abc"]
    new_query = urlencode(query, doseq=True)
    return urlunparse(parsed._replace(query=new_query))


def slugify(text: str, default: str = "tune") -> str:
    """Create a safe filename slug from the title."""
    if not text:
        return default
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-+", "-", text)
    text = text.strip("-")
    return text or default


def extract_title(abc_text: str) -> str:
    """Extract the first T: line from ABC."""
    for line in abc_text.splitlines():
        line = line.strip()
        if line.startswith("T:"):
            return line[2:].strip()
    return ""


def load_index() -> dict:
    if INDEX_PATH.exists():
        with INDEX_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {"songs": []}


def save_index(index: dict) -> None:
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    with INDEX_PATH.open("w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)


def add_or_update_song(index: dict, song_meta: dict) -> None:
    """Add a song to the index, or update if id already exists."""
    for i, s in enumerate(index["songs"]):
        if s.get("id") == song_meta["id"]:
            index["songs"][i] = song_meta
            return
    index["songs"].append(song_meta)


def download_abc(url: str) -> str:
    final_url = ensure_abc_url(url)
    print(f"Fetching ABC from: {final_url}")
    resp = requests.get(final_url, timeout=15)
    resp.raise_for_status()
    return resp.text


def save_song(abc_text: str, source_url: str, default_id_prefix: str = "tune") -> dict:
    title = extract_title(abc_text)
    base_id = slugify(title, default=default_id_prefix)
    # Avoid overwriting existing files with same id by adding numeric suffix
    slug = base_id
    counter = 1
    while (SONGS_DIR / f"{slug}.abc").exists():
        counter += 1
        slug = f"{base_id}-{counter}"

    SONGS_DIR.mkdir(parents=True, exist_ok=True)
    dest = SONGS_DIR / f"{slug}.abc"
    dest.write_text(abc_text, encoding="utf-8")

    meta = {
        "id": slug,
        "title": title or slug,
        "source_url": source_url,
        "filename": str(dest),
    }
    print(f"Saved: {meta['title']} -> {dest}")
    return meta


def read_urls_from_file(path: Path) -> list[str]:
    urls = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                urls.append(line)
    return urls


def main():
    parser = argparse.ArgumentParser(description="Import ABC tunes into ./songs")
    parser.add_argument("--urls-file", type=str, help="Path to text file with one URL per line")
    parser.add_argument("--url", action="append", help="Single URL (can be repeated)")
    args = parser.parse_args()

    urls: list[str] = []

    if args.urls_file:
        urls.extend(read_urls_from_file(Path(args.urls_file)))

    if args.url:
        urls.extend(args.url)

    if not urls:
        print("No URLs given. Use --urls-file or --url.")
        return

    index = load_index()

    for i, url in enumerate(urls, start=1):
        try:
            print(f"\n[{i}/{len(urls)}] Processing: {url}")
            abc_text = download_abc(url)
            meta = save_song(abc_text, url, default_id_prefix=f"tune{i}")
            add_or_update_song(index, meta)
        except Exception as e:
            print(f"Error processing {url}: {e}")

    save_index(index)
    print(f"\nDone. Index written to {INDEX_PATH}")


if __name__ == "__main__":
    main()
