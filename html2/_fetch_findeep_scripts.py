# -*- coding: utf-8 -*-
import re
import ssl
import time
import urllib.request
from pathlib import Path

CTX = ssl.create_default_context()
URL = "https://helpcosmetic.ease-dev.org/findeepSearch.es?mid=a10901000000"
OUT = Path(__file__).with_name("_findeep_live_scripts.txt")


def fetch(url, retries=5):
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                },
            )
            with urllib.request.urlopen(req, timeout=40, context=CTX) as r:
                return r.status, r.read()
        except Exception as e:
            last = e
            print("retry", i, e)
            time.sleep(1.5)
    return None, last


st, data = fetch(URL)
print("status", st, type(data))
if not isinstance(data, bytes):
    raise SystemExit(1)

html = data.decode("utf-8", "replace")
OUT.write_text(html, encoding="utf-8")
print("saved html", len(html))

print("\n=== SCRIPT SRC ===")
for m in re.finditer(r"<script([^>]*)>", html, re.I):
    attrs = m.group(1)
    src = re.search(r'src=["\']([^"\']+)["\']', attrs, re.I)
    if src:
        print(src.group(1))

print("\n=== LINK STYLESHEET ===")
for m in re.finditer(r'<link[^>]+rel=["\']stylesheet["\'][^>]*>', html, re.I):
    href = re.search(r'href=["\']([^"\']+)["\']', m.group(0), re.I)
    if href and ("findeep" in href.group(1) or "jquery" in href.group(1) or "ui" in href.group(1)):
        print(href.group(1))

# also any script src containing findeep/jquery
print("\n=== FINDEEP/JQUERY RELATED ===")
for m in re.finditer(r'(?:src|href)=["\']([^"\']*(?:findeep|jquery|d3|autocomplete|tf)[^"\']*)["\']', html, re.I):
    print(m.group(1))
