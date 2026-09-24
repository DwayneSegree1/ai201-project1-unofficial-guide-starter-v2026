"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


def _paragraphs(text: str) -> tuple[str, list[str]]:
    """Split a document into its title line and its body paragraphs.

    Every document in this corpus is a title, a blank line, then two to four
    paragraphs. If one ever isn't, the whole text becomes the body and the
    title comes back empty, which the caller handles.
    """
    blocks = [b.strip() for b in text.strip().split("\n\n") if b.strip()]
    if len(blocks) < 2:
        return "", blocks
    return blocks[0], blocks[1:]


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Split documents at paragraph breaks, packing up to CHUNK_SIZE characters.

    My strategy for Milestone 3, chosen after measuring the corpus — the
    reasoning is in README.md under Chunking Strategy. Three rules:

      1. Never cut inside a paragraph. Paragraphs here are whole thoughts and
         the documents are short enough that there's no reason to break one.
      2. Pack paragraphs together until adding the next would pass CHUNK_SIZE.
         Most documents fit in one chunk; the long multi-topic housing ones
         come out as two.
      3. Prepend the document's title line to every chunk. A chunk that says
         "the heating is uneven" is useless without "Old Brewhouse" attached.

    A trailing chunk below MIN_CHUNK_SIZE is merged back into the previous
    one — the corpus has paragraphs as short as 36 characters, and those are
    too thin to embed on their own.
    """
    size = config.CHUNK_SIZE
    min_size = getattr(config, "MIN_CHUNK_SIZE", 0)

    chunks: list[Chunk] = []
    for doc in documents:
        title, paragraphs = _paragraphs(doc.text)
        if not paragraphs:
            continue

        # Group paragraphs into bodies of at most `size` characters.
        bodies: list[list[str]] = []
        current: list[str] = []
        current_len = 0
        for para in paragraphs:
            # +2 for the blank line joining it to what's already there.
            addition = len(para) + (2 if current else 0)
            if current and current_len + addition > size:
                bodies.append(current)
                current, current_len = [para], len(para)
            else:
                current.append(para)
                current_len += addition
        if current:
            bodies.append(current)

        def assemble(body: list[str]) -> str:
            text = "\n\n".join(body)
            return f"{title}\n\n{text}" if title else text

        # A thin tail is worse than a slightly oversized chunk. Measured on the
        # assembled chunk, title included — that's what actually gets embedded.
        if len(bodies) > 1 and len(assemble(bodies[-1])) < min_size:
            bodies[-2].extend(bodies.pop())

        for index, body in enumerate(bodies):
            text = assemble(body)
            chunks.append(
                Chunk(
                    text=text,
                    source=doc.source,
                    index=index,
                    produced_by="chunker.py::split_documents",
                )
            )

    return chunks


def split_paragraphs(documents: list[Document]) -> list[Chunk]:
    """
    Strategy B for unit 2: one paragraph per chunk, title prepended, no packing.

    This is the strategy I measured and rejected in Milestone 3. I rejected it
    because 99 of the corpus's 183 body paragraphs are under 120 characters,
    and a 90-character chunk reading "The good: the most characterful building
    on campus" is thin and, stripped of its document, doesn't say which
    building it's about.

    Half of that objection no longer holds. Prepending the title line — which
    `split_documents` does and the original paragraph experiment didn't — fixes
    the "which building" half outright. Only the "too thin to embed" half is
    still live, and that is a claim I asserted rather than tested.

    The reason to test it now is a specific measured failure, not curiosity.
    "cheapest place to live on campus" never retrieves
    `housing_morrow_house.txt`, which is the document that answers it: the
    sentence "cheapest housing tier by about $900 a year" shares a chunk with
    the building's construction date, room types and a damp problem, and the
    chunk's single vector is an average of all four. One fact per chunk is the
    direct fix for a fact that got averaged away.

    The cost is the other side of the same coin: 183 vectors instead of 91, and
    broad questions like "what is Morrow House like?" now need several chunks
    where one used to do. That trade is what the A/B in README.md measures.
    """
    chunks: list[Chunk] = []
    for doc in documents:
        title, paragraphs = _paragraphs(doc.text)
        if not paragraphs:
            continue
        for index, para in enumerate(paragraphs):
            text = f"{title}\n\n{para}" if title else para
            chunks.append(
                Chunk(
                    text=text,
                    source=doc.source,
                    index=index,
                    produced_by="chunker.py::split_paragraphs",
                )
            )
    return chunks


# The chunker each index variant is built with. `app.py index --variant NAME`
# looks the name up here, so both strategies can sit in the store at once and
# be queried against the same questions.
STRATEGIES = {
    "default": split_documents,
    "paragraph": split_paragraphs,
    "fallback": fallback_split,
}


def split_for_variant(documents: list[Document], variant: str = "default") -> list[Chunk]:
    """Chunk `documents` with whichever strategy this index variant names."""
    try:
        strategy = STRATEGIES[variant]
    except KeyError:
        raise SystemExit(
            f"No chunking strategy called {variant!r}. Known variants: "
            + ", ".join(sorted(STRATEGIES))
        ) from None
    return strategy(documents)


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
