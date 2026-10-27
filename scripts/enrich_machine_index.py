#!/usr/bin/env python3
"""Enrich a Paul's Notes JSONL index without altering its source records."""
import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote, urlsplit

TOPICS = {
    "biostatistics": ("biostatistic", "statistics", "poisson", "binomial", "regression", "survival", "kaplan", "cox", "hypothesis"),
    "machine-learning": ("machine learning", "model tuning", "feature selection", "cross validation", "neural network", "training", "calibration"),
    "genomics": ("genom", "gene", "rna", "esr1", "erbb2", "tcga", "sequencing"),
    "rust": ("rust", "cargo", "borrow", "crate"),
    "r-programming": ("r programming", "ggplot", "tidyverse", "rscript", "caret"),
    "research-governance": ("protocol", "privacy", "consent", "reproducib", "evidence", "admission", "milestone"),
}
STOP = {"about", "after", "before", "between", "could", "during", "from", "into", "other", "their", "these", "those", "through", "using", "which", "with", "would"}
WORDS = re.compile(r"[\w-]{3,}", re.UNICODE)
LINK = re.compile(r"(?<!!)\[[^\]]+\]\((<[^>]+>|[^)]+)\)")

def tokens(text):
    return {w.lower() for w in WORDS.findall(text) if w.lower() not in STOP}

def enrich(records):
    """Return sections with deterministic topics and forward/back links."""
    paths = {r["path"] for r in records}
    edges = defaultdict(set)
    for r in records:
        src = r["path"]
        for m in LINK.finditer(r["text"]):
            dest = m.group(1).strip().strip("<>").split(" ", 1)[0]
            parsed = urlsplit(dest)
            if parsed.scheme or parsed.netloc or dest.startswith(("#", "//")) or not parsed.path:
                continue
            path = str((Path(src).parent / unquote(parsed.path)).as_posix())
            from posixpath import normpath
            path = normpath(path)
            if path in paths and path != src:
                edges[src].add(path)
    reverse = defaultdict(set)
    for src, destinations in edges.items():
        for dest in destinations:
            reverse[dest].add(src)
    result = []
    for record in records:
        r = dict(record)
        # Restrict topic detection to titles and paths to avoid false positives
        # from literature bibliographies or incidental mentions in long sections.
        title = (r["path"] + " " + r["heading"]).lower()
        r["topics"] = sorted(k for k, terms in TOPICS.items() if any(term in title for term in terms))
        r["outbound_documents"] = sorted(edges[r["path"]])
        r["inbound_documents"] = sorted(reverse[r["path"]])
        r["retrieval_terms"] = sorted(tokens(r["heading"]))[:24]
        result.append(r)
    return result

def delta(previous, current):
    old = {r["section_id"]: r["content_sha256"] for r in previous}
    new = {r["section_id"]: r["content_sha256"] for r in current}
    return {"added": sorted(new.keys() - old.keys()), "removed": sorted(old.keys() - new.keys()),
            "changed": sorted(k for k in new.keys() & old.keys() if old[k] != new[k]),
            "unchanged_count": sum(old[k] == new[k] for k in new.keys() & old.keys())}

def load(path):
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--previous", type=Path)
    p.add_argument("--delta-output", type=Path)
    a = p.parse_args()
    records = load(a.input)
    required = {"path", "section_id", "content_sha256", "heading", "text"}
    if not all(required <= set(r) for r in records):
        p.error("input missing required index fields")
    if len({r["section_id"] for r in records}) != len(records):
        p.error("duplicate section IDs")
    output = enrich(records)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text("".join(json.dumps(r, sort_keys=True, ensure_ascii=False) + "\n" for r in output), encoding="utf-8")
    if a.previous:
        report = delta(load(a.previous), records)
        if a.delta_output:
            a.delta_output.parent.mkdir(parents=True, exist_ok=True)
            a.delta_output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        else:
            print(json.dumps(report, indent=2))
    print(f"Enriched {len(output)} sections across {len({r['path'] for r in output})} documents")

if __name__ == "__main__":
    main()
