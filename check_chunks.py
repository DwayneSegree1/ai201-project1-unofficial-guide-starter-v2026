#!/usr/bin/env python3
"""
Criterion 4: do chunks end where thoughts end?

    python3 check_chunks.py            three samples of 10, seeds 0/1/2
    python3 check_chunks.py --n 10 --seeds 0 1 2

`run_eval.py` measures criteria 1, 2, 3 and 5 by asking questions. Criterion 4
is about the index, not about any question, so nothing in the eval touches it.
This does: it draws a random sample of chunks and checks both edges.

A chunk's first line is its document's title, which is a heading and carries no
terminal punctuation — that's a clean start, not a cut, so the start test asks
whether the chunk opens a line rather than whether it opens a sentence. The end
test is the strict one: a chunk that stops mid-sentence ends on a lowercase
letter or a comma, and that's what it catches.
"""

import argparse
import random

from ingest import load_documents
from chunker import split_for_variant

END_MARKS = ".?!\"'”’)"
START_MARKS = "\"'“‘"


def check(chunk) -> tuple[bool, bool]:
    """(starts cleanly, ends cleanly) for one chunk, as it is actually indexed."""
    text = chunk.text.strip()
    first, last = text[0], text[-1]
    return (first.isupper() or first.isdigit() or first in START_MARKS), (last in END_MARKS)


def sample_boundaries(corpus: str | None = None, n: int = 10, seed: int = 0,
                      variant: str = "default"):
    """Draw `n` chunks at random and report which edges are clean."""
    chunks = split_for_variant(load_documents(corpus), variant)
    sample = random.Random(seed).sample(chunks, n)

    clean = 0
    print(f"\nSeed {seed} — {n} chunks drawn at random from {len(chunks)} "
          f"(variant {variant})")
    for c in sample:
        starts_ok, ends_ok = check(c)
        ok = starts_ok and ends_ok
        clean += ok
        text = c.text.strip()
        print(f"  {'ok  ' if ok else 'CUT '} {c.label:<44} "
              f"start={text[0]!r} end={text[-1]!r}")
        if not ok:
            print(f"        head: {text[:70]!r}")
            print(f"        tail: {text[-70:]!r}")
    print(f"  -> {clean} of {n} clean at both edges")
    return clean


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", default=None)
    parser.add_argument("--n", type=int, default=10, help="chunks per sample")
    parser.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    parser.add_argument("--variant", default="default",
                        help="which chunking strategy to check (see chunker.STRATEGIES)")
    args = parser.parse_args()

    for seed in args.seeds:
        sample_boundaries(corpus=args.corpus, n=args.n, seed=seed,
                          variant=args.variant)


if __name__ == "__main__":
    main()
