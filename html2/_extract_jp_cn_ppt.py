# -*- coding: utf-8 -*-
from __future__ import annotations

import re
import shutil
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET
from html import unescape

ROOT = Path(__file__).resolve().parent
BASE = ROOT / "5개국 도식화(최종)_261023" / "5개국 도식화(최종)_261023"


def find_pptx(folder_name: str) -> Path:
    d = BASE / folder_name
    cands = list(d.glob("*.pptx"))
    if not cands:
        raise SystemExit(f"No pptx in {d}")
    return cands[0]


def extract_hlinks(pptx: Path) -> list[tuple[int, str, str, str]]:
    """Return list of (slide, rid, url, anchors_joined)."""
    td = Path(tempfile.mkdtemp())
    rows = []
    try:
        with zipfile.ZipFile(pptx) as z:
            z.extractall(td)
        slides = sorted(
            (td / "ppt" / "slides").glob("slide*.xml"),
            key=lambda p: int(re.search(r"(\d+)", p.name).group(1)),
        )
        for s in slides:
            n = int(re.search(r"(\d+)", s.name).group(1))
            rels = td / "ppt" / "slides" / "_rels" / f"{s.name}.rels"
            rid_url = {}
            if rels.exists():
                root = ET.parse(rels).getroot()
                for rel in root:
                    typ = (rel.get("Type") or "").lower()
                    if "hyperlink" in typ and rel.get("TargetMode") == "External":
                        rid_url[rel.get("Id")] = rel.get("Target")
            xml = s.read_text(encoding="utf-8")
            for rid, url in rid_url.items():
                anchors = []
                for rm in re.finditer(r"<a:r[\s>][\s\S]*?</a:r>", xml):
                    block = rm.group(0)
                    if f'r:id="{rid}"' in block:
                        t = "".join(re.findall(r"<a:t[^>]*>([^<]*)</a:t>", block))
                        if t.strip():
                            anchors.append(unescape(t))
                # also check br with hlink
                on_br = bool(re.search(rf'<a:br>[\s\S]*?r:id="{rid}"', xml))
                anchor = " | ".join(dict.fromkeys(anchors)) if anchors else ("(LINEBREAK/EMPTY)" if on_br else "(no visible text)")
                rows.append((n, rid, url, anchor))

        # comments mentioning 첨부
        comment_hits = []
        cdir = td / "ppt" / "comments"
        if cdir.exists():
            for p in sorted(cdir.glob("modernComment_*.xml")):
                # which slides point here?
                slides_for = []
                for rels in (td / "ppt" / "slides" / "_rels").glob("slide*.xml.rels"):
                    t = rels.read_text(encoding="utf-8")
                    if p.name in t:
                        slides_for.append(int(re.search(r"slide(\d+)", rels.name).group(1)))
                texts = []
                for el in ET.parse(p).getroot().iter():
                    if el.text and el.text.strip():
                        texts.append(el.text.strip())
                att = [t for t in texts if "첨부" in t or re.search(r"\d-\d", t)]
                if att or any("첨부" in t for t in texts):
                    comment_hits.append((slides_for, p.name, texts))
        return rows, comment_hits, td
    except Exception:
        shutil.rmtree(td, ignore_errors=True)
        raise


def list_attachments(folder_name: str) -> list[str]:
    d = BASE / folder_name / "첨부자료"
    if not d.exists():
        # try alternate
        alts = list((BASE / folder_name).rglob("*"))
        return [f"[no 첨부자료 dir] entries={len(alts)}"]
    out = []
    for p in sorted(d.rglob("*")):
        if p.is_file():
            out.append(str(p.relative_to(d)))
    return out


def dump_country(code: str, folder: str, out_name: str) -> None:
    pptx = find_pptx(folder)
    rows, comments, td = extract_hlinks(pptx)
    lines = [
        f"# {code} PPT extract",
        f"PPTX: {pptx.name}",
        "",
        "## Hyperlinks",
    ]
    seen = set()
    for n, rid, url, anchor in rows:
        lines.append(f"- S{n} {rid}: {anchor}")
        lines.append(f"  {url}")
        seen.add(url)
    lines.append("")
    lines.append(f"## Unique URLs ({len(seen)})")
    for u in sorted(seen):
        lines.append(f"- {u}")
    lines.append("")
    lines.append("## Comments (첨부-related snippets)")
    for slides_for, name, texts in comments:
        lines.append(f"### slides {slides_for} / {name}")
        for t in texts:
            if "첨부" in t or re.search(r"\d-\d|\d\.", t) or len(t) < 80:
                lines.append(f"- {t}")
    lines.append("")
    lines.append("## Attachment folder files")
    for f in list_attachments(folder):
        lines.append(f"- {f}")

    # also raw slide text for link-ish words? skip for size
    shutil.rmtree(td, ignore_errors=True)
    out = ROOT / out_name
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out} ({len(rows)} hlinks, {len(seen)} unique)")


dump_country("JP", "일본", "_ppt_jp_extract.txt")
dump_country("CN", "중국", "_ppt_cn_extract.txt")
