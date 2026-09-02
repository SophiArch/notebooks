"""Generate all AI402 (Retrieval & RAG Systems) lab notebooks."""

import json
from pathlib import Path

BASE = Path(__file__).parent.parent / "content" / "courses" / "retrieval-rag-systems"

NOTEBOOK_META = {
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python", "version": "3.11.0"},
}


def nb(cells: list) -> dict:
    return {"nbformat": 4, "nbformat_minor": 5, "metadata": NOTEBOOK_META, "cells": cells}


def code(src: str, cell_id: str, hide: bool = False) -> dict:
    meta = {"hide": True} if hide else {}
    return {
        "cell_type": "code",
        "id": cell_id,
        "metadata": meta,
        "execution_count": None,
        "outputs": [],
        "source": src.splitlines(keepends=True),
    }


def md(src: str, cell_id: str) -> dict:
    return {
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": {},
        "source": src.splitlines(keepends=True),
    }


def save(lesson_dir: str, notebook: dict) -> None:
    path = BASE / lesson_dir / "lab.ipynb"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False))
    print(f"  written: {path.relative_to(BASE.parent.parent.parent)}")


# ---------------------------------------------------------------------------
# Shared building blocks — the Nimbus Analytics product knowledge base
# ---------------------------------------------------------------------------

INSTALL = "!pip install sentence-transformers rank-bm25 faiss-cpu numpy pandas --quiet"

CORPUS_SRC = '''import numpy as np

# The Nimbus Analytics product knowledge base: (doc_id, heading_path, text)
CORPUS = [
    ("plans-overview", "Pricing > Plans",
     "Nimbus Analytics offers three subscription plans: Starter, Teams, and "
     "Enterprise. Starter includes 5 seats and community support. Teams includes "
     "50 seats, shared dashboards, and priority email support. Enterprise includes "
     "unlimited seats, priority support, and advanced security features."),
    ("sso-policy", "Pricing > Enterprise plan",
     "Single sign-on (SSO) with SAML 2.0 is available on the Enterprise plan only. "
     "The Teams plan does not include SSO. Enterprise customers can configure SSO "
     "from the admin console under Security settings."),
    ("seat-pricing", "Pricing > Seats",
     "Per-seat pricing: Starter is $12 per seat per month, Teams is $29 per seat "
     "per month, and Enterprise pricing is custom. Annual billing gives a 20 "
     "percent discount on all plans."),
    ("refund-policy", "Billing > Refunds",
     "Customers can request a full refund within 30 days of purchase. To get your "
     "money back after 30 days, contact billing support; partial refunds are "
     "prorated for annual subscriptions."),
    ("error-e4022", "Troubleshooting > Error codes",
     "Error E4022 means the API rate limit was exceeded. The Starter plan allows "
     "100 requests per minute, Teams 1,000, and Enterprise 10,000. Wait 60 seconds "
     "and retry, or upgrade the plan."),
    ("error-e5001", "Troubleshooting > Error codes",
     "Error E5001 indicates an expired API token. Rotate the token from the admin "
     "console under API settings. Tokens expire after 90 days by default."),
    ("api-export", "API > Export",
     "The export endpoint POST /v2/export creates a CSV export of dashboard data. "
     "Exports are limited to 100,000 rows on Teams and 1 million rows on "
     "Enterprise."),
    ("data-retention", "Security > Data retention",
     "Event data is retained for 13 months on all plans. Enterprise customers can "
     "configure custom retention windows up to 5 years from the admin console."),
    ("priority-support", "Support > Tiers",
     "Priority support with a 4-hour response SLA is included in Teams and "
     "Enterprise plans. Starter includes community support only."),
    ("dashboard-sharing", "Product > Dashboards",
     "Shared dashboards let teammates view and edit the same dashboard. Sharing "
     "outside your workspace requires a public link, available on Teams and "
     "Enterprise."),
    ("audit-logs", "Security > Audit logs",
     "Audit logs record sign-ins, permission changes, and data exports. Audit "
     "logs are an Enterprise-only feature and are retained for 2 years."),
    ("cancel-downgrade", "Billing > Cancellation",
     "You can cancel or downgrade at any time from the billing page. Downgrades "
     "take effect at the end of the current billing period."),
]
DOC_IDS = [d[0] for d in CORPUS]
DOC_TEXTS = [f"{d[1]}: {d[2]}" for d in CORPUS]

# Labelled evaluation queries: (query, set of relevant doc_ids)
EVAL_SET = [
    ("does the teams plan include sso", {"sso-policy"}),
    ("how do I get my money back", {"refund-policy"}),
    ("what does error E4022 mean", {"error-e4022"}),
    ("how long is event data kept", {"data-retention"}),
    ("cost per seat on the teams plan", {"seat-pricing"}),
    ("response time for priority support", {"priority-support"}),
    ("row limit for csv export", {"api-export"}),
    ("rotate an expired api token", {"error-e5001"}),
]
print(f"{len(CORPUS)} documents, {len(EVAL_SET)} labelled queries")'''

EMBED_SRC = '''from sentence_transformers import SentenceTransformer

embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def embed(texts):
    return embedder.encode(list(texts), normalize_embeddings=True)

DOC_EMB = embed(DOC_TEXTS)

def dense_search(query, k=5, doc_emb=None, doc_ids=None):
    doc_emb = DOC_EMB if doc_emb is None else doc_emb
    doc_ids = DOC_IDS if doc_ids is None else doc_ids
    scores = doc_emb @ embed([query])[0]
    order = np.argsort(scores)[::-1][:k]
    return [(doc_ids[i], float(scores[i])) for i in order]

print(dense_search("does the teams plan include sso", k=3))'''


# ---------------------------------------------------------------------------
# Lesson 02 — debug: Chunking Strategies
# ---------------------------------------------------------------------------

L02 = nb([
    code(
        "# Lab type: debug\n"
        "# Course: AI402 — Retrieval & RAG Systems\n"
        "# Lesson: Chunking Strategies: The Decision AI Tools Get Wrong\n"
        "# Task: An AI assistant wrote the ingestion pipeline below. It contains 3 bugs\n"
        "# that silently destroy retrieval quality. Find and fix each one, and write a\n"
        "# one-sentence explanation in the markdown cell after each fix.",
        "meta00001",
    ),
    md(
        "# Lab: Debugging an AI-Generated Chunking Pipeline\n\n"
        "A team asked an AI assistant to \"chunk and index our knowledge base\". The "
        "pipeline below runs without errors and most queries work — but tail queries "
        "fail, and they fail silently.\n\n"
        "**Your task:** find the 3 bugs, fix them, and verify the fix by comparing "
        "recall on the labelled query set before and after.\n\n"
        "**Outputs are cleared.** Run every cell top to bottom.",
        "intro001",
    ),
    md("## Setup", "setup001"),
    code(INSTALL, "setup002"),
    code(CORPUS_SRC, "setup003"),
    code(EMBED_SRC, "setup004"),
    md(
        "## The AI-generated ingestion pipeline\n\n"
        "Read it the way you would review a pull request. It chunks every document, "
        "embeds the chunks, and provides a search function. Three of its decisions "
        "are production defects.",
        "buggy001",
    ),
    code(
        "# --- AI-GENERATED PIPELINE (contains 3 bugs) ---\n"
        "# Review this code — is it correct?\n\n"
        "def chunk_document(text, size=120):\n"
        "    # Bug candidate area 1: how are boundaries chosen?\n"
        "    return [text[i:i + size] for i in range(0, len(text), size)]\n\n"
        "chunks = []\n"
        "for doc_id, heading, text in CORPUS:\n"
        "    # Bug candidate area 2: what does each chunk carry with it?\n"
        "    for piece in chunk_document(text):\n"
        "        chunks.append(piece)\n\n"
        "chunk_emb = embed(chunks)\n\n"
        "def chunk_search(query, k=5):\n"
        "    scores = chunk_emb @ embed([query])[0]\n"
        "    order = np.argsort(scores)[::-1][:k]\n"
        "    return [(chunks[i], float(scores[i])) for i in order]\n\n"
        "print(f\"{len(chunks)} chunks indexed\")\n"
        "for text, score in chunk_search('does the teams plan include sso', k=3):\n"
        "    print(f\"  {score:.3f}  {text[:70]!r}\")",
        "buggy002",
    ),
    md(
        "## Measure before you fix\n\n"
        "A RAG pipeline is only as good as the *facts* its chunks deliver intact. "
        "For six queries we know the exact answer-bearing span in the source "
        "document; the measurement below checks whether any retrieved chunk "
        "contains that span **unbroken**. (The pipeline returns bare text with no "
        "document identity, so span matching is also all we *can* measure — that "
        "awkwardness is itself a clue to one of the bugs.)",
        "measure001",
    ),
    code(
        "# (query, answer-bearing span that a retrieved chunk must contain intact)\n"
        "ANSWER_SPANS = [\n"
        "    (\"does the teams plan include sso\",\n"
        "     \"The Teams plan does not include SSO\"),\n"
        "    (\"how do I get my money back\",\n"
        "     \"request a full refund within 30 days\"),\n"
        "    (\"can I keep event data longer than 13 months\",\n"
        "     \"custom retention windows up to 5 years\"),\n"
        "    (\"row limit for csv export on enterprise\",\n"
        "     \"100,000 rows on Teams and 1 million rows on Enterprise\"),\n"
        "    (\"api rate limits per plan\",\n"
        "     \"100 requests per minute, Teams 1,000, and Enterprise 10,000\"),\n"
        "    (\"response time for priority support\",\n"
        "     \"4-hour response SLA\"),\n"
        "]\n\n"
        "def intact_span_rate(search_fn, k=3):\n"
        "    hits = 0\n"
        "    for query, span in ANSWER_SPANS:\n"
        "        retrieved_texts = [chunk for chunk, _ in search_fn(query, k=k)]\n"
        "        if any(span in text for text in retrieved_texts):\n"
        "            hits += 1\n"
        "        else:\n"
        "            print(f\"  MISSED intact: {span!r:.60}\")\n"
        "    return hits / len(ANSWER_SPANS)\n\n"
        "print(f\"Buggy pipeline — answer spans delivered intact @3: \"\n"
        "      f\"{intact_span_rate(chunk_search):.2f}\")",
        "measure002",
    ),
    md(
        "## Bug 1\n\n"
        "Look at `chunk_document` and at a few actual chunks (`chunks[:5]`). What do "
        "the boundaries fall in the middle of?\n\n"
        "**Explain the bug:**\n\n"
        "*(Write your diagnosis here.)*",
        "bug1_001",
    ),
    md(
        "<details>\n<summary>🔑 Reveal answer — Bug 1</summary>\n\n"
        "**The bug:** `chunk_document` splits on raw *character* positions with no "
        "overlap. Boundaries fall mid-word and mid-sentence, so facts spanning a "
        "boundary exist intact in no chunk at all.\n\n"
        "**Why it causes wrong behaviour:** a chunk like `'gle sign-on (SSO) with "
        "SAML 2.0 is availab'` embeds to a vector that no longer resembles queries "
        "about SSO availability — the content silently becomes unreachable for "
        "exactly the queries it answers.\n\n"
        "**Correct approach:** split on sentence boundaries with overlap, or — "
        "better for this corpus — keep each document's text intact per section and "
        "carry the heading path (see Bug 3 fix).\n\n</details>",
        "bug1_002",
    ),
    md(
        "## Bug 2\n\n"
        "What does each entry in `chunks` carry besides its text? Think about what "
        "you would need to (a) update the index when a document changes, (b) cite a "
        "source, (c) filter by tenant.\n\n"
        "**Explain the bug:**\n\n"
        "*(Write your diagnosis here.)*",
        "bug2_001",
    ),
    md(
        "<details>\n<summary>🔑 Reveal answer — Bug 2</summary>\n\n"
        "**The bug:** chunks are stored as bare strings — the `doc_id` and heading "
        "path are thrown away at ingestion.\n\n"
        "**Why it causes wrong behaviour:** without per-chunk metadata you cannot "
        "delete a changed document's chunks (updates), attribute an answer to a "
        "source (citations), or enforce access control (permissions). The eval "
        "harness above had to fall back to substring matching precisely because "
        "chunk→document identity was lost.\n\n"
        "**Correct approach:** store `(doc_id, heading, chunk_text)` triples (or a "
        "dict) and embed the text while keeping the identity attached.\n\n</details>",
        "bug2_002",
    ),
    md(
        "## Bug 3\n\n"
        "The corpus documents carry a heading path like `'Pricing > Enterprise "
        "plan'`. Where does that information go in the pipeline, and what happens "
        "to a chunk whose meaning depends on it?\n\n"
        "**Explain the bug:**\n\n"
        "*(Write your diagnosis here.)*",
        "bug3_001",
    ),
    md(
        "<details>\n<summary>🔑 Reveal answer — Bug 3</summary>\n\n"
        "**The bug:** the heading path is dropped — chunks are embedded without the "
        "structural context that says what they are *about*.\n\n"
        "**Why it causes wrong behaviour:** a sentence like \"...is available on "
        "the Enterprise plan only\" chunked away from its `Pricing` heading loses "
        "the vocabulary that queries actually use. Structure-aware chunking exists "
        "to carry exactly this context.\n\n"
        "**Correct approach:** prepend the heading path to each chunk's text before "
        "embedding, as the fixed pipeline below does.\n\n</details>",
        "bug3_002",
    ),
    md("## The fixed pipeline\n\nAll three fixes applied. Run it and compare recall.", "fix001"),
    code(
        "# Fix: sentence-boundary chunks + carried metadata + heading path prepended\n"
        "import re\n\n"
        "def chunk_document_fixed(text, max_sentences=2, overlap=1):\n"
        "    sentences = re.split(r\"(?<=[.!?]) +\", text)\n"
        "    step = max(1, max_sentences - overlap)\n"
        "    return [\" \".join(sentences[i:i + max_sentences])\n"
        "            for i in range(0, len(sentences), step)]\n\n"
        "fixed_chunks = []          # (doc_id, heading, chunk_text)\n"
        "for doc_id, heading, text in CORPUS:\n"
        "    for piece in chunk_document_fixed(text):\n"
        "        fixed_chunks.append((doc_id, heading, piece))\n\n"
        "fixed_emb = embed([f\"{h}: {t}\" for _, h, t in fixed_chunks])\n\n"
        "def chunk_search_fixed(query, k=5):\n"
        "    scores = fixed_emb @ embed([query])[0]\n"
        "    order = np.argsort(scores)[::-1][:k]\n"
        "    return [(fixed_chunks[i][2], float(scores[i])) for i in order]\n\n"
        "print(f\"Fixed pipeline — answer spans delivered intact @3: \"\n"
        "      f\"{intact_span_rate(chunk_search_fixed):.2f}\")\n\n"
        "# And because metadata now exists, honest doc-level recall is measurable:\n"
        "def doc_search_fixed(query, k=3):\n"
        "    scores = fixed_emb @ embed([query])[0]\n"
        "    order = np.argsort(scores)[::-1][:k]\n"
        "    return [fixed_chunks[i][0] for i in order]\n\n"
        "hits = sum(1 for q, rel in EVAL_SET if set(doc_search_fixed(q)) & rel)\n"
        "print(f\"Fixed pipeline recall@3 by doc_id (impossible before Bug 2's fix): \"\n"
        "      f\"{hits / len(EVAL_SET):.2f}\")",
        "fix002",
    ),
    md(
        "## Summary\n\n"
        "Fill in the blanks, then check your answers below.\n\n"
        "1. Character-window chunking with no overlap makes boundary-spanning facts "
        "_______ without any error surfacing.\n"
        "2. Chunk metadata (doc_id, heading path) must be captured at _______ time — "
        "afterwards it cannot be recovered from the index.\n"
        "3. Prepending the _______ to each chunk's text keeps small chunks "
        "self-describing.",
        "sum001",
    ),
    md(
        "<details>\n<summary>🔑 Reveal summary answers</summary>\n\n"
        "1. **unreachable/unretrievable** — the chunks embed away from the queries "
        "they answer.\n"
        "2. **ingestion** — updates, citations, and permissions all depend on it.\n"
        "3. **heading path** — structure-aware chunking carries the context a "
        "boundary would destroy.\n\n</details>",
        "sum002",
    ),
])


# ---------------------------------------------------------------------------
# Lesson 03 — review: Hybrid Retrieval
# ---------------------------------------------------------------------------

L03 = nb([
    code(
        "# Lab type: review\n"
        "# Course: AI402 — Retrieval & RAG Systems\n"
        "# Lesson: Hybrid Retrieval: BM25 + Dense Fusion and RRF\n"
        "# Task: A working hybrid retriever is below. Run it, then answer the\n"
        "# judgment questions about its design choices — several are defensible,\n"
        "# at least two are defects you should be able to name and fix.",
        "meta00001",
    ),
    md(
        "# Lab: Reviewing a Hybrid Retriever\n\n"
        "This retriever runs and produces plausible results. Your job is judgment: "
        "for each design choice, decide whether it is sound, and if not, what "
        "breaks and for which queries.\n\n"
        "**Outputs are cleared.** Run every cell top to bottom.",
        "intro001",
    ),
    md("## Setup", "setup001"),
    code(INSTALL, "setup002"),
    code(CORPUS_SRC, "setup003"),
    code(EMBED_SRC, "setup004"),
    md("## The retriever under review", "rev001"),
    code(
        "from rank_bm25 import BM25Okapi\n\n"
        "# Index-time tokenisation: lowercase, strip punctuation\n"
        "def tokenize(text):\n"
        "    return [t.strip('.,:;()$').lower() for t in text.split()]\n\n"
        "bm25 = BM25Okapi([tokenize(t) for t in DOC_TEXTS])\n\n"
        "def bm25_search(query, k=5):\n"
        "    # NOTE the tokenisation used here\n"
        "    scores = bm25.get_scores(query.split())\n"
        "    order = np.argsort(scores)[::-1][:k]\n"
        "    return [(DOC_IDS[i], float(scores[i])) for i in order]\n\n"
        "def hybrid_weighted(query, k=5, w=0.5):\n"
        "    # Combine the two retrievers with a weighted score sum\n"
        "    combined = {}\n"
        "    for doc_id, s in dense_search(query, k=10):\n"
        "        combined[doc_id] = w * s\n"
        "    for doc_id, s in bm25_search(query, k=10):\n"
        "        combined[doc_id] = combined.get(doc_id, 0.0) + (1 - w) * s\n"
        "    ranked = sorted(combined, key=combined.get, reverse=True)\n"
        "    return ranked[:k]\n\n"
        "for q in [\"does the teams plan include sso\", \"what does error E4022 mean\"]:\n"
        "    print(q)\n"
        "    print(\"  dense :\", [d for d, _ in dense_search(q, k=3)])\n"
        "    print(\"  bm25  :\", [d for d, _ in bm25_search(q, k=3)])\n"
        "    print(\"  hybrid:\", hybrid_weighted(q, k=3))",
        "rev002",
    ),
    md(
        "**Question 1.** Print the actual score ranges of the two arms for a few "
        "queries. What does `w=0.5` actually weight in `hybrid_weighted`, given "
        "those ranges? Which arm dominates the sum, and would changing `w` to 0.9 "
        "fix it?",
        "q1_001",
    ),
    md(
        "<details>\n<summary>🔑 Reveal answer — Question 1</summary>\n\n"
        "Dense cosine scores live in roughly 0.3–0.8; BM25 scores on this corpus "
        "reach several points and are unbounded. The weighted sum is dominated by "
        "BM25 almost regardless of `w` — the weights are decorative because the "
        "scales are incompatible. Re-weighting cannot fix a comparison that is "
        "meaningless by construction; fusing by *rank* (RRF, Question 3) is the "
        "correct repair.\n\n</details>",
        "q1_002",
    ),
    md(
        "**Question 2.** Compare the tokenisation at index time (`tokenize`) with "
        "the tokenisation at query time inside `bm25_search`. Construct a query "
        "where the mismatch matters and demonstrate it.",
        "q2_001",
    ),
    md(
        "<details>\n<summary>🔑 Reveal answer — Question 2</summary>\n\n"
        "The index lowercases and strips punctuation; queries are split raw. "
        "`bm25_search(\"What does Error E4022 mean?\")` queries the terms "
        "`['What', 'does', 'Error', 'E4022', 'mean?']` — `Error` (capitalised) and "
        "`mean?` (punctuation attached) miss the index vocabulary, and on longer "
        "identifier queries the damage compounds. The lexical arm silently "
        "underperforms on exactly the identifier-style traffic it exists for. Fix: "
        "`bm25.get_scores(tokenize(query))` — index and query must share one "
        "tokeniser.\n\n</details>",
        "q2_002",
    ),
    md(
        "**Question 3.** Implement RRF fusion over the two arms' rankings "
        "(`score = Σ 1/(60 + rank)`) and compare its output with `hybrid_weighted` "
        "on the eval set. Which queries change, and why?",
        "q3_001",
    ),
    code(
        "# Work here: implement rrf_fuse(rankings, k=60) and compare\n"
        "# recall@3 of hybrid_weighted vs your RRF fusion over EVAL_SET.\n",
        "q3_002",
    ),
    md(
        "<details>\n<summary>🔑 Reveal answer — Question 3</summary>\n\n"
        "```python\n"
        "def rrf_fuse(rankings, k=60):\n"
        "    scores = {}\n"
        "    for ranking in rankings:\n"
        "        for rank, doc_id in enumerate(ranking, start=1):\n"
        "            scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + rank)\n"
        "    return sorted(scores, key=scores.get, reverse=True)\n\n"
        "def hybrid_rrf(query, k=5):\n"
        "    dense_ids = [d for d, _ in dense_search(query, k=10)]\n"
        "    bm25_ids = [d for d, _ in bm25_search(query, k=10)]\n"
        "    return rrf_fuse([dense_ids, bm25_ids])[:k]\n\n"
        "for fn in (hybrid_weighted, hybrid_rrf):\n"
        "    hits = sum(1 for q, rel in EVAL_SET if set(fn(q, k=3)) & rel)\n"
        "    print(fn.__name__, hits / len(EVAL_SET))\n"
        "```\n\n"
        "On a 12-document corpus both fusions can reach the same recall@3 — the "
        "corpus is too small for top-3 to miss much, which is itself a lesson in "
        "why demos hide fusion defects. The difference is visible in the *scores*: "
        "print `hybrid_weighted`'s combined dict for a paraphrase query and note "
        "the dense contribution is numerically irrelevant next to BM25's scale, "
        "then look at a query where the arms disagree (the E4022 query, where the "
        "raw-token BM25 arm misranks) and see RRF settle it by consensus instead "
        "of by whichever scale is bigger. At production corpus sizes that "
        "difference is recall, not just margins.\n\n</details>",
        "q3_003",
    ),
    md(
        "**Question 4.** This corpus has 12 documents and the demo works either "
        "way. Name the two query populations from the lesson that decide whether "
        "hybrid retrieval is worth a second index in production, and say how you "
        "would measure whether *this* system needs it.",
        "q4_001",
    ),
    md(
        "<details>\n<summary>🔑 Reveal answer — Question 4</summary>\n\n"
        "Identifier-style queries (error codes, part numbers, function names) — "
        "where BM25 uniquely wins — and paraphrase queries — where dense uniquely "
        "wins. Measure by running the labelled query set through each arm "
        "*separately*: if one arm alone matches the fused recall, skip the second "
        "index; if each arm uniquely wins a meaningful slice, hybrid is buying "
        "exactly that slice.\n\n</details>",
        "q4_002",
    ),
    md(
        "## Summary\n\n"
        "1. Weighted sums over incompatible score scales are _______, whatever the "
        "weights.\n"
        "2. Index-time and query-time _______ must match for the lexical arm to "
        "work.\n"
        "3. RRF fuses _______, rewarding documents both retrievers agree on.",
        "sum001",
    ),
    md(
        "<details>\n<summary>🔑 Reveal summary answers</summary>\n\n"
        "1. **meaningless/decorative** — one scale dominates regardless.\n"
        "2. **tokenisation** — a silent mismatch starves BM25 of matches.\n"
        "3. **rank positions** — consensus beats confidence within one arm.\n\n</details>",
        "sum002",
    ),
])

print("Generating AI402 lab notebooks ...")
save("02-chunking-strategies", L02)
save("03-hybrid-retrieval", L03)


# ---------------------------------------------------------------------------
# Lesson 04 — extend: Query Rewriting
# ---------------------------------------------------------------------------

L04 = nb([
    code(
        "# Lab type: extend\n"
        "# Course: AI402 — Retrieval & RAG Systems\n"
        "# Lesson: Query Rewriting: HyDE, Multi-Query, and Decomposition\n"
        "# Task: A baseline dense retriever is provided, along with canned LLM\n"
        "# rewrite outputs (no API key needed). Extend the pipeline with multi-query\n"
        "# fusion and decomposition, and measure what each buys.",
        "meta00001",
    ),
    md(
        "# Lab: Extending a Retriever with Query Rewriting\n\n"
        "The rewrites an LLM would produce are supplied as canned strings so the "
        "lab runs without API calls — in production these come from a versioned "
        "rewrite prompt.\n\n"
        "**Outputs are cleared.** Run every cell top to bottom.",
        "intro001",
    ),
    md("## Setup: baseline retriever", "setup001"),
    code(INSTALL, "setup002"),
    code(CORPUS_SRC, "setup003"),
    code(EMBED_SRC, "setup004"),
    code(
        "def rrf_fuse(rankings, k=60):\n"
        "    scores = {}\n"
        "    for ranking in rankings:\n"
        "        for rank, doc_id in enumerate(ranking, start=1):\n"
        "            scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + rank)\n"
        "    return sorted(scores, key=scores.get, reverse=True)\n\n"
        "def recall_at_k(search_fn, k=3):\n"
        "    hits = sum(1 for q, rel in EVAL_SET\n"
        "               if set(search_fn(q)[:k]) & rel)\n"
        "    return hits / len(EVAL_SET)\n\n"
        "baseline = lambda q: [d for d, _ in dense_search(q, k=5)]\n"
        "print(f\"Baseline dense recall@3: {recall_at_k(baseline):.2f}\")",
        "setup005",
    ),
    md(
        "## Canned LLM rewrites\n\n"
        "For three ambiguous eval queries, here is what a rewrite prompt returned.",
        "canned001",
    ),
    code(
        "MULTI_QUERY_REWRITES = {\n"
        "    \"how do I get my money back\": [\n"
        "        \"refund policy\",\n"
        "        \"request a refund for a subscription\",\n"
        "        \"cancel my plan and get reimbursed\",\n"
        "        \"billing refund window\",\n"
        "    ],\n"
        "    \"how long is event data kept\": [\n"
        "        \"data retention period\",\n"
        "        \"how many months is analytics data stored\",\n"
        "        \"retention window configuration\",\n"
        "    ],\n"
        "    \"response time for priority support\": [\n"
        "        \"priority support SLA\",\n"
        "        \"support tier response times\",\n"
        "        \"how fast does support reply on paid plans\",\n"
        "    ],\n"
        "}\n\n"
        "COMPOUND_QUESTION = (\n"
        "    \"which plan should we pick if we need SSO and priority support \"\n"
        "    \"but only have budget for 20 seats\"\n"
        ")\n"
        "DECOMPOSITION = [\n"
        "    \"which plans include SSO\",\n"
        "    \"which plans include priority support\",\n"
        "    \"per seat pricing for each plan\",\n"
        "]",
        "canned002",
    ),
    md(
        "## Extension 1: multi-query fusion\n\n"
        "Implement `multi_query_search(query)`: retrieve for the original query "
        "*and* its rewrites (when available), fuse with RRF, and return ranked doc "
        "IDs. Then compare recall@3 against the baseline.",
        "ext1_001",
    ),
    code(
        "def multi_query_search(query, k_per_arm=5):\n"
        "    # TODO: build the list of queries: the ORIGINAL plus any rewrites\n"
        "    # TODO: run dense_search for each, collect doc-id rankings\n"
        "    # TODO: return rrf_fuse(rankings)\n"
        "    pass\n",
        "ext1_002",
    ),
    md(
        "<details>\n<summary>🔑 Reveal model answer — Extension 1</summary>\n\n"
        "```python\n"
        "def multi_query_search(query, k_per_arm=5):\n"
        "    queries = [query] + MULTI_QUERY_REWRITES.get(query, [])\n"
        "    rankings = [[d for d, _ in dense_search(q, k=k_per_arm)]\n"
        "                for q in queries]\n"
        "    return rrf_fuse(rankings)\n\n"
        "print(f\"Multi-query recall@3: {recall_at_k(multi_query_search):.2f}\")\n"
        "```\n\n"
        "Keeping the original query in the list is not optional: a rewrite that "
        "drifts from the user's intent would otherwise be able to push the right "
        "documents out entirely.\n\n</details>",
        "ext1_003",
    ),
    md(
        "## Extension 2: decomposition\n\n"
        "Implement `decomposed_search(sub_questions)`: retrieve top-2 documents per "
        "sub-question and return them *grouped by sub-question* (a dict), not fused "
        "— generation needs to know which evidence answers which part.",
        "ext2_001",
    ),
    code(
        "def decomposed_search(sub_questions, k=2):\n"
        "    # TODO: return {sub_question: [doc_id, ...]} for each sub-question\n"
        "    pass\n\n"
        "# When done: decomposed_search(DECOMPOSITION)\n",
        "ext2_002",
    ),
    md(
        "<details>\n<summary>🔑 Reveal model answer — Extension 2</summary>\n\n"
        "```python\n"
        "def decomposed_search(sub_questions, k=2):\n"
        "    return {sq: [d for d, _ in dense_search(sq, k=k)]\n"
        "            for sq in sub_questions}\n\n"
        "for sq, docs in decomposed_search(DECOMPOSITION).items():\n"
        "    print(f\"{sq!r:.55} -> {docs}\")\n"
        "```\n\n"
        "Compare with `dense_search(COMPOUND_QUESTION, k=3)`: the single-shot "
        "query averages three information needs into one vector and typically "
        "misses at least one of `sso-policy` / `priority-support` / "
        "`seat-pricing`; the decomposed version retrieves each fact "
        "independently.\n\n</details>",
        "ext2_003",
    ),
    md(
        "## Extension 3: the cost column\n\n"
        "Each rewrite pattern adds LLM calls and extra retrievals. For each of "
        "baseline, multi-query (assume 1 rewrite call + N retrievals) and "
        "decomposition (1 call + M retrievals), tally: LLM calls before retrieval, "
        "retrieval operations, and whether latency is added *before* the first "
        "retrieval. Write your table in the markdown cell below.",
        "ext3_001",
    ),
    md("*(Your cost table here.)*", "ext3_002"),
    md(
        "<details>\n<summary>🔑 Reveal model answer — Extension 3</summary>\n\n"
        "| pipeline | LLM calls pre-retrieval | retrievals | latency before 1st retrieval |\n"
        "|---|---|---|---|\n"
        "| baseline | 0 | 1 | none |\n"
        "| multi-query | 1 | 1 + #rewrites (parallelisable) | one LLM round-trip |\n"
        "| decomposition | 1 | #sub-questions | one LLM round-trip |\n\n"
        "The rewrite call usually costs more latency than retrieval itself — which "
        "is why rewriting is applied selectively (ambiguous/compound traffic), not "
        "unconditionally.\n\n</details>",
        "ext3_003",
    ),
    md(
        "## Summary\n\n"
        "1. Multi-query fuses the original plus rewrites with _______.\n"
        "2. Decomposition returns evidence _______ by sub-question, not fused.\n"
        "3. Every rewrite pattern inserts an _______ call in front of retrieval — "
        "cost, latency, and stochasticity.",
        "sum001",
    ),
    md(
        "<details>\n<summary>🔑 Reveal summary answers</summary>\n\n"
        "1. **RRF (reciprocal rank fusion)**\n"
        "2. **grouped**\n"
        "3. **LLM**\n\n</details>",
        "sum002",
    ),
])


# ---------------------------------------------------------------------------
# Lesson 05 — review: Cross-Encoder Re-Ranking
# ---------------------------------------------------------------------------

L05 = nb([
    code(
        "# Lab type: review\n"
        "# Course: AI402 — Retrieval & RAG Systems\n"
        "# Lesson: Re-Ranking with Cross-Encoders at Production Scale\n"
        "# Task: A two-stage retrieval service is below. Run it, then answer the\n"
        "# judgment questions — one design choice nullifies the re-ranker entirely.",
        "meta00001",
    ),
    md(
        "# Lab: Reviewing a Re-Ranking Service\n\n"
        "**Outputs are cleared.** Run every cell top to bottom. The cross-encoder "
        "model (~90 MB) downloads on first use.",
        "intro001",
    ),
    md("## Setup", "setup001"),
    code(INSTALL, "setup002"),
    code(CORPUS_SRC, "setup003"),
    code(EMBED_SRC, "setup004"),
    md("## The service under review", "rev001"),
    code(
        "from sentence_transformers import CrossEncoder\n\n"
        "reranker = CrossEncoder(\"cross-encoder/ms-marco-MiniLM-L-6-v2\")\n\n"
        "def rerank(query, candidate_ids, top_k=3):\n"
        "    texts = {d: t for d, t in zip(DOC_IDS, DOC_TEXTS)}\n"
        "    pairs = [(query, texts[c]) for c in candidate_ids]\n"
        "    scores = reranker.predict(pairs)\n"
        "    order = np.argsort(scores)[::-1][:top_k]\n"
        "    return [(candidate_ids[i], float(scores[i])) for i in order]\n\n"
        "def retrieve_and_rerank(query, top_k=3):\n"
        "    candidates = [d for d, _ in dense_search(query, k=top_k)]\n"
        "    return rerank(query, candidates, top_k=top_k)\n\n"
        "for q, rel in EVAL_SET[:3]:\n"
        "    out = retrieve_and_rerank(q)\n"
        "    print(f\"{q!r:45} -> {[d for d, _ in out]}  (relevant: {sorted(rel)})\")",
        "rev002",
    ),
    md(
        "**Question 1.** Compare `retrieve_and_rerank`'s output with plain "
        "`dense_search` at the same `top_k` across the whole eval set. How often "
        "does the re-ranker change *which documents* are returned (not just their "
        "order)? Explain why, pointing at one line of code.",
        "q1_001",
    ),
    md(
        "<details>\n<summary>🔑 Reveal answer — Question 1</summary>\n\n"
        "Never. Stage one retrieves `k=top_k` candidates, so the re-ranker can "
        "only permute the same three documents — the funnel has no wide end. The "
        "offending line is `dense_search(query, k=top_k)`: the candidate set's "
        "*composition* is fixed entirely by the weaker bi-encoder, and the "
        "cross-encoder's accuracy is spent shuffling it. Re-ranking recovers "
        "ranking errors, never recall errors.\n\n</details>",
        "q1_002",
    ),
    md(
        "**Question 2.** Fix the funnel: retrieve a wider candidate set (try "
        "k=8) and re-rank down to 3. Measure recall@3 before and after on "
        "EVAL_SET. What is the ratio between stage-one k and final top_k here, and "
        "what does the lesson recommend?",
        "q2_001",
    ),
    code(
        "# Work here: widen stage one, re-rank to top 3, compare recall@3.\n",
        "q2_002",
    ),
    md(
        "<details>\n<summary>🔑 Reveal answer — Question 2</summary>\n\n"
        "```python\n"
        "def funnel(query, top_k=3, depth=8):\n"
        "    candidates = [d for d, _ in dense_search(query, k=depth)]\n"
        "    return [d for d, _ in rerank(query, candidates, top_k=top_k)]\n\n"
        "for fn in (lambda q: [d for d, _ in retrieve_and_rerank(q)], funnel):\n"
        "    hits = sum(1 for q, rel in EVAL_SET if set(fn(q)) & rel)\n"
        "    print(hits / len(EVAL_SET))\n"
        "```\n\n"
        "Here depth/top_k ≈ 2.7× because the corpus has only 12 documents; the "
        "lesson's production guidance is 10–40× (e.g. 50–200 candidates for a "
        "top-5), with the right depth found where measured ranking quality "
        "plateaus.\n\n</details>",
        "q2_002a",
    ),
    md(
        "**Question 3.** Run the widened funnel on the query "
        "`\"can I export my dashboards to powerpoint\"` (the corpus has no such "
        "feature) and print the re-ranker's scores. Compare them with the scores "
        "for an answerable query. What capability does this give the pipeline that "
        "cosine similarity alone cannot?",
        "q3_001",
    ),
    md(
        "<details>\n<summary>🔑 Reveal answer — Question 3</summary>\n\n"
        "The cross-encoder's scores for the unanswerable query sit far below the "
        "scores it gives genuine answers (for this model, well into negative "
        "logits), while cosine similarity still dutifully produces a \"best\" "
        "match. A calibrated score floor lets the pipeline return *nothing* and "
        "say so — the honest no-answer — instead of feeding known-irrelevant "
        "context to generation. Stage one alone cannot tell you this.\n\n</details>",
        "q3_002",
    ),
    md(
        "**Question 4.** This service re-ranks with one forward pass per "
        "candidate per query. Name the two knobs from the lesson that control "
        "re-ranking latency at production traffic, and state what each trades "
        "away.",
        "q4_001",
    ),
    md(
        "<details>\n<summary>🔑 Reveal answer — Question 4</summary>\n\n"
        "**Candidate depth** — capping it caps compute linearly but lowers the "
        "recall ceiling the re-ranker can exploit; set it where measured quality "
        "plateaus. **Model size** — a smaller distilled re-ranker (this 6-layer "
        "MiniLM is already the workhorse class) cuts per-pair cost at some "
        "accuracy loss. Batching the pairs is free speed with no trade; skipping "
        "re-ranking when stage-one scores are already well separated trades a "
        "little quality on ambiguous queries for a large average saving.\n\n</details>",
        "q4_002",
    ),
    md(
        "## Summary\n\n"
        "1. Stage one owns _______; stage two owns precision at the top.\n"
        "2. A funnel whose stage-one k equals its final top_k gives the re-ranker "
        "_______ to do.\n"
        "3. A calibrated cross-encoder score floor enables the honest _______.",
        "sum001",
    ),
    md(
        "<details>\n<summary>🔑 Reveal summary answers</summary>\n\n"
        "1. **recall**\n"
        "2. **nothing (except reordering the same set)**\n"
        "3. **no-answer** — returning no context when nothing is relevant.\n\n</details>",
        "sum002",
    ),
])

save("04-query-rewriting", L04)
save("05-cross-encoder-reranking", L05)


# ---------------------------------------------------------------------------
# Lesson 06 — debug: Retrieval Metrics
# ---------------------------------------------------------------------------

L06 = nb([
    code(
        "# Lab type: debug\n"
        "# Course: AI402 — Retrieval & RAG Systems\n"
        "# Lesson: Retrieval Metrics: Recall@k, MRR, and nDCG\n"
        "# Task: The evaluation harness below prints a flattering report. It\n"
        "# contains 3 bugs — none of them crash. Find and fix each one, and write\n"
        "# a one-sentence explanation after each fix.",
        "meta00001",
    ),
    md(
        "# Lab: Debugging an Evaluation Harness\n\n"
        "Evaluation bugs don't raise exceptions — they publish wrong numbers with "
        "confident names. The harness below was AI-generated to \"measure our "
        "retriever\". Every number it prints is wrong.\n\n"
        "**Outputs are cleared.** Run every cell top to bottom.",
        "intro001",
    ),
    md("## Setup", "setup001"),
    code(INSTALL, "setup002"),
    code(CORPUS_SRC, "setup003"),
    code(EMBED_SRC, "setup004"),
    md("## The harness under audit", "buggy001"),
    code(
        "# --- AI-GENERATED EVALUATION HARNESS (contains 3 bugs) ---\n"
        "# Review this code — is it correct?\n\n"
        "def evaluate_recall(search_fn, eval_set, k=5):\n"
        "    hits = 0\n"
        "    for query, relevant in eval_set:\n"
        "        results = [d for d, _ in search_fn(query, k=k)]\n"
        "        if results[0] in relevant:            # <- look closely\n"
        "            hits += 1\n"
        "    return hits / len(eval_set)\n\n"
        "def evaluate_mrr(search_fn, eval_set, k=5):\n"
        "    reciprocal_ranks = []\n"
        "    for query, relevant in eval_set:\n"
        "        results = [d for d, _ in search_fn(query, k=k)]\n"
        "        for i, doc in enumerate(results, start=1):\n"
        "            if doc in relevant:\n"
        "                reciprocal_ranks.append(1.0 / i)\n"
        "                break\n"
        "    # 'avoid division issues when a query has no hits'\n"
        "    return sum(reciprocal_ranks) / len(reciprocal_ranks)\n\n"
        "# 'we didn't have labelled queries, so we generated them from the docs'\n"
        "DOC_DERIVED_EVAL_SET = [(t[:60], {d}) for d, h, t in CORPUS[:8]]\n\n"
        "# The team's real labelled set, which has drifted: one labelled source\n"
        "# document ('integrations-guide') was deleted from the corpus last month.\n"
        "TEAM_EVAL_SET = EVAL_SET + [\n"
        "    (\"does nimbus integrate with salesforce\", {\"integrations-guide\"}),\n"
        "]\n\n"
        "print(f\"recall@5: {evaluate_recall(dense_search, DOC_DERIVED_EVAL_SET):.2f}\")\n"
        "print(f\"MRR:      {evaluate_mrr(dense_search, TEAM_EVAL_SET):.2f}\")",
        "buggy002",
    ),
    md(
        "## Bug 1: what does `evaluate_recall` actually compute?\n\n"
        "Trace it by hand for one query. What metric is it, and what should "
        "recall@5 check?\n\n"
        "**Explain the bug:**\n\n"
        "*(Write your diagnosis here.)*",
        "bug1_001",
    ),
    md(
        "<details>\n<summary>🔑 Reveal answer — Bug 1</summary>\n\n"
        "**The bug:** only `results[0]` is ever checked, so the function computes "
        "hit-rate@1 and labels it recall@5.\n\n"
        "**Why it causes wrong behaviour:** every number in the report describes a "
        "stricter, different metric — comparisons against any recall@5 target or "
        "another system's recall are meaningless.\n\n"
        "**Correct approach:**\n"
        "```python\n"
        "def recall_at_k(search_fn, eval_set, k=5):\n"
        "    total = 0.0\n"
        "    for query, relevant in eval_set:\n"
        "        results = [d for d, _ in search_fn(query, k=k)]\n"
        "        total += len(set(results[:k]) & relevant) / len(relevant)\n"
        "    return total / len(eval_set)\n"
        "```\n\n</details>",
        "bug1_002",
    ),
    md(
        "## Bug 2: the MRR average\n\n"
        "`TEAM_EVAL_SET` contains a query whose labelled source document no "
        "longer exists in the corpus — a realistic labelled-set drift. Trace what "
        "`evaluate_mrr` does with that query. Which population disappears from "
        "the average, and in which direction does the reported MRR move?\n\n"
        "**Explain the bug:**\n\n"
        "*(Write your diagnosis here.)*",
        "bug2_001",
    ),
    md(
        "<details>\n<summary>🔑 Reveal answer — Bug 2</summary>\n\n"
        "**The bug:** a query with no relevant document in the top k appends "
        "nothing to `reciprocal_ranks`, so the mean is taken over successful "
        "queries only — the salesforce query silently vanishes and the reported "
        "MRR is unchanged by a total retrieval failure.\n\n"
        "**Why it causes wrong behaviour:** the dropped zeros are exactly the "
        "retrieval failures — the population you most need to see. The reported "
        "MRR answers 'how well do we rank, when we succeed?' and inflates as the "
        "system fails more. A query with no relevant result scores 0 by "
        "definition; there is no division issue to avoid — count it as `0.0` "
        "(equivalently: divide the sum by `len(eval_set)`).\n\n</details>",
        "bug2_002",
    ),
    md(
        "## Bug 3: where did the eval queries come from?\n\n"
        "Look at `DOC_DERIVED_EVAL_SET`. What is being 'asked', and what will "
        "*any* retriever score on it? Compare with the phrasings in `EVAL_SET`.\n\n"
        "**Explain the bug:**\n\n"
        "*(Write your diagnosis here.)*",
        "bug3_001",
    ),
    md(
        "<details>\n<summary>🔑 Reveal answer — Bug 3</summary>\n\n"
        "**The bug:** each eval 'query' is the first 60 characters of the "
        "document's own text — a verbatim fragment of exactly what was embedded. "
        "This is the retrieval-evaluation analogue of evaluating on the training "
        "set: any retriever scores near-perfectly, and the number says nothing "
        "about real traffic.\n\n"
        "**Why it causes wrong behaviour:** real users ask in their own words "
        "(\"how do I get my money back\"), which is precisely the "
        "vocabulary-mismatch problem retrieval must solve. Label real (or "
        "realistic) user phrasings, as `EVAL_SET` does.\n\n</details>",
        "bug3_002",
    ),
    md("## The fixed harness\n\nApply all three fixes and re-measure on the honest query set.", "fix001"),
    code(
        "# Fix for Bugs 1-3: correct recall, zeros kept in MRR, real query phrasings\n"
        "def recall_at_k(search_fn, eval_set, k=5):\n"
        "    total = 0.0\n"
        "    for query, relevant in eval_set:\n"
        "        results = [d for d, _ in search_fn(query, k=k)]\n"
        "        total += len(set(results[:k]) & relevant) / len(relevant)\n"
        "    return total / len(eval_set)\n\n"
        "def mrr(search_fn, eval_set, k=5):\n"
        "    total = 0.0\n"
        "    for query, relevant in eval_set:\n"
        "        results = [d for d, _ in search_fn(query, k=k)]\n"
        "        rr = 0.0\n"
        "        for i, doc in enumerate(results, start=1):\n"
        "            if doc in relevant:\n"
        "                rr = 1.0 / i\n"
        "                break\n"
        "        total += rr\n"
        "    return total / len(eval_set)\n\n"
        "print(\"Bug 2 made visible — same retriever, same queries:\")\n"
        "print(f\"  buggy MRR (drops the failed query): \"\n"
        "      f\"{evaluate_mrr(dense_search, TEAM_EVAL_SET):.2f}\")\n"
        "print(f\"  fixed MRR (counts it as zero):      \"\n"
        "      f\"{mrr(dense_search, TEAM_EVAL_SET):.2f}\")\n"
        "print()\n"
        "print(\"Bug 3 made visible — doc-derived vs real phrasings:\")\n"
        "print(f\"  doc-derived recall@5: {recall_at_k(dense_search, DOC_DERIVED_EVAL_SET):.2f}\"\n"
        "      \"   <- flattering by construction\")\n"
        "print(f\"  real-query recall@5:  {recall_at_k(dense_search, EVAL_SET):.2f}\")\n"
        "print(f\"  real-query recall@1:  {recall_at_k(dense_search, EVAL_SET, k=1):.2f}\"\n"
        "      \"   <- with recall@5, localises ranking-vs-retrieval faults\")",
        "fix002",
    ),
    md(
        "## Summary\n\n"
        "1. The buggy 'recall@5' was actually _______.\n"
        "2. Dropping zero-scoring queries from MRR makes the metric measure only "
        "the queries where retrieval _______.\n"
        "3. Eval queries derived from document titles are the retrieval analogue "
        "of evaluating on the _______.",
        "sum001",
    ),
    md(
        "<details>\n<summary>🔑 Reveal summary answers</summary>\n\n"
        "1. **hit-rate@1**\n"
        "2. **succeeded**\n"
        "3. **training set**\n\n</details>",
        "sum002",
    ),
])


# ---------------------------------------------------------------------------
# Lesson 07 — extend: RAG Evals (faithfulness, citations)
# ---------------------------------------------------------------------------

L07 = nb([
    code(
        "# Lab type: extend\n"
        "# Course: AI402 — Retrieval & RAG Systems\n"
        "# Lesson: RAG Evals: Faithfulness, Groundedness, and Citations\n"
        "# Task: Canned claim-decomposition and judge outputs are provided (no API\n"
        "# key needed). Extend the harness: compute faithfulness, then build the\n"
        "# citation-support checker the naive version gets wrong.",
        "meta00001",
    ),
    md(
        "# Lab: Extending a RAG Eval with Faithfulness and Citation Checks\n\n"
        "In production, claim extraction and support verdicts come from versioned "
        "LLM judge prompts. Here they are supplied as canned data so the lab runs "
        "offline — the *logic* you build around them is exactly the production "
        "logic.\n\n"
        "**Outputs are cleared.** Run every cell top to bottom.",
        "intro001",
    ),
    md("## Setup: one answer, its context, and the judge's raw output", "setup001"),
    code(INSTALL, "setup002"),
    code(CORPUS_SRC, "setup003"),
    code(
        "# The pipeline retrieved these chunks (with stable IDs) ...\n"
        "RETRIEVED = {\n"
        "    1: (\"sso-policy\", \"Single sign-on (SSO) with SAML 2.0 is available on \"\n"
        "        \"the Enterprise plan only. The Teams plan does not include SSO.\"),\n"
        "    2: (\"plans-overview\", \"Teams includes 50 seats, shared dashboards, and \"\n"
        "        \"priority email support.\"),\n"
        "    3: (\"seat-pricing\", \"Per-seat pricing: Starter is $12 per seat per month, \"\n"
        "        \"Teams is $29 per seat per month, and Enterprise pricing is custom.\"),\n"
        "}\n\n"
        "# ... and generation produced this answer:\n"
        "ANSWER = (\n"
        "    \"The Teams plan costs $29 per seat per month [3] and includes shared \"\n"
        "    \"dashboards [2]. It also includes SSO via SAML 2.0 [1], and all plans \"\n"
        "    \"come with a 14-day free trial [2].\"\n"
        ")\n\n"
        "# Canned output of the claim-decomposition prompt:\n"
        "CLAIMS = [\n"
        "    (\"The Teams plan costs $29 per seat per month\", [3]),\n"
        "    (\"The Teams plan includes shared dashboards\", [2]),\n"
        "    (\"The Teams plan includes SSO via SAML 2.0\", [1]),\n"
        "    (\"All plans come with a 14-day free trial\", [2]),\n"
        "]\n\n"
        "# Canned per-claim verdicts from the judge prompt (claim checked against\n"
        "# the retrieved context ONLY — never against world knowledge):\n"
        "JUDGE_VERDICTS = [\"SUPPORTED\", \"SUPPORTED\", \"NOT_SUPPORTED\", \"NOT_SUPPORTED\"]\n"
        "print(f\"{len(CLAIMS)} claims, verdicts: {JUDGE_VERDICTS}\")",
        "setup004",
    ),
    md(
        "## Extension 1: the faithfulness score\n\n"
        "Implement `faithfulness(verdicts)` returning the supported fraction, and "
        "print each claim with its verdict. Note which claims failed and why the "
        "third one fails even though its sentence *cites* chunk [1].",
        "ext1_001",
    ),
    code(
        "def faithfulness(verdicts):\n"
        "    # TODO: fraction of claims judged SUPPORTED\n"
        "    pass\n",
        "ext1_002",
    ),
    md(
        "<details>\n<summary>🔑 Reveal model answer — Extension 1</summary>\n\n"
        "```python\n"
        "def faithfulness(verdicts):\n"
        "    return verdicts.count(\"SUPPORTED\") / len(verdicts)\n\n"
        "for (claim, cites), v in zip(CLAIMS, JUDGE_VERDICTS):\n"
        "    print(f\"  [{v:13}] {claim}\")\n"
        "print(f\"faithfulness = {faithfulness(JUDGE_VERDICTS):.2f}\")\n"
        "```\n\n"
        "Score: 0.50. Claim 3 contradicts chunk 1 (SSO is Enterprise-only; the "
        "answer says Teams has it) — a citation was attached to a claim its source "
        "*refutes*. Claim 4 (free trial) appears in no retrieved chunk at all: it "
        "may even be true in the world, but faithfulness is measured against the "
        "context only.\n\n</details>",
        "ext1_003",
    ),
    md(
        "## Extension 2: the naive citation checker — and yours\n\n"
        "Below is the citation checker the AI assistant originally wrote. Run it, "
        "observe that it passes the answer, then extend it: a correct checker "
        "verifies each citation points at a chunk that *supports* the citing "
        "claim, using the judge verdicts.",
        "ext2_001",
    ),
    code(
        "import re\n\n"
        "def naive_citation_check(answer, retrieved):\n"
        "    cited = [int(c) for c in re.findall(r\"\\[(\\d+)\\]\", answer)]\n"
        "    return all(c in retrieved for c in cited)\n\n"
        "print(f\"naive checker passes: {naive_citation_check(ANSWER, RETRIEVED)}\")\n\n"
        "def citation_support_check(claims, verdicts, retrieved):\n"
        "    # TODO: return a list of (claim, ok) where ok is True only when the\n"
        "    # claim's citations exist in `retrieved` AND its verdict is SUPPORTED\n"
        "    pass\n",
        "ext2_002",
    ),
    md(
        "<details>\n<summary>🔑 Reveal model answer — Extension 2</summary>\n\n"
        "```python\n"
        "def citation_support_check(claims, verdicts, retrieved):\n"
        "    results = []\n"
        "    for (claim, cites), verdict in zip(claims, verdicts):\n"
        "        ok = all(c in retrieved for c in cites) and verdict == \"SUPPORTED\"\n"
        "        results.append((claim, ok))\n"
        "    return results\n\n"
        "for claim, ok in citation_support_check(CLAIMS, JUDGE_VERDICTS, RETRIEVED):\n"
        "    print(f\"  [{'ok' if ok else 'FAIL'}] {claim}\")\n"
        "```\n\n"
        "The naive checker validates citation *existence* — every `[n]` points at "
        "a real chunk, so it blesses an answer whose key claim is refuted by its "
        "own source. Citation presence is not citation correctness.\n\n</details>",
        "ext2_003",
    ),
    md(
        "## Extension 3: the triad, read together\n\n"
        "Suppose this pipeline's eval run reports retrieval recall@5 = 0.95, "
        "faithfulness = 0.50 (as computed above), answer relevance = 0.9. In the "
        "markdown cell below: name the broken stage, justify it from the score "
        "combination, and say what the *dangerous* combination from the lesson "
        "would look like instead.",
        "ext3_001",
    ),
    md("*(Your diagnosis here.)*", "ext3_002"),
    md(
        "<details>\n<summary>🔑 Reveal model answer — Extension 3</summary>\n\n"
        "Recall is high and relevance is high, but half the claims aren't "
        "grounded: **generation is inventing** (and mis-citing) — fix prompting or "
        "the model, not retrieval. The dangerous combination is the mirror image: "
        "recall *low* with faithfulness and relevance *high* — the model faithfully "
        "and fluently answers from the wrong context, every per-answer signal "
        "looks green, and only the retrieval metric exposes it.\n\n</details>",
        "ext3_003",
    ),
    md(
        "## Summary\n\n"
        "1. Faithfulness is measured per _______, against the retrieved context "
        "only.\n"
        "2. A citation checker must verify _______, not existence.\n"
        "3. The triad (retrieval, faithfulness, relevance) is diagnostic because "
        "each score isolates a pipeline _______.",
        "sum001",
    ),
    md(
        "<details>\n<summary>🔑 Reveal summary answers</summary>\n\n"
        "1. **claim** — per-claim verdicts stop one fabrication being averaged "
        "away.\n"
        "2. **support**\n"
        "3. **stage**\n\n</details>",
        "sum002",
    ),
])


# ---------------------------------------------------------------------------
# Lesson 08 — review: Index Maintenance
# ---------------------------------------------------------------------------

L08 = nb([
    code(
        "# Lab type: review\n"
        "# Course: AI402 — Retrieval & RAG Systems\n"
        "# Lesson: Index Maintenance: Freshness, Updates, and Embedding Drift\n"
        "# Task: The document-update handler below runs a live demonstration of\n"
        "# its own defect. Run it, watch the orphan appear, and answer the\n"
        "# judgment questions.",
        "meta00001",
    ),
    md(
        "# Lab: Reviewing an Index Update Path\n\n"
        "We use FAISS with an ID-mapped index so vectors can be added and removed "
        "by chunk ID — the same mechanics as a production vector database, small "
        "enough to inspect.\n\n"
        "**Outputs are cleared.** Run every cell top to bottom.",
        "intro001",
    ),
    md("## Setup", "setup001"),
    code(INSTALL, "setup002"),
    code(CORPUS_SRC, "setup003"),
    code(EMBED_SRC, "setup004"),
    code(
        "import faiss\n\n"
        "DIM = DOC_EMB.shape[1]\n"
        "index = faiss.IndexIDMap(faiss.IndexFlatIP(DIM))\n\n"
        "# chunk registry: numeric id -> (doc_id, chunk_no, text)\n"
        "registry = {}\n"
        "next_id = 0\n\n"
        "def add_chunks(doc_id, chunk_texts):\n"
        "    global next_id\n"
        "    vecs = embed(chunk_texts)\n"
        "    ids = np.arange(next_id, next_id + len(chunk_texts))\n"
        "    index.add_with_ids(np.asarray(vecs, dtype=\"float32\"), ids)\n"
        "    for i, (cid, text) in enumerate(zip(ids, chunk_texts)):\n"
        "        registry[int(cid)] = (doc_id, i, text)\n"
        "    next_id += len(chunk_texts)\n\n"
        "# Index the refund policy as 3 chunks (v1 of the document)\n"
        "V1_CHUNKS = [\n"
        "    \"Billing > Refunds: full refund within 30 days of purchase.\",\n"
        "    \"Billing > Refunds: after 30 days contact billing support.\",\n"
        "    \"Billing > Refunds: annual subscriptions get prorated partial refunds.\",\n"
        "]\n"
        "add_chunks(\"refund-policy\", V1_CHUNKS)\n"
        "print(f\"index size: {index.ntotal}, registry: {len(registry)}\")",
        "setup005",
    ),
    md("## The update handler under review", "rev001"),
    code(
        "# --- THE UPDATE HANDLER (review this code — is it correct?) ---\n"
        "def update_document(doc_id, new_chunk_texts):\n"
        "    \"\"\"Re-chunk and upsert a changed document.\"\"\"\n"
        "    vecs = embed(new_chunk_texts)\n"
        "    # overwrite chunk i of this doc with new chunk i\n"
        "    ids = [cid for cid, (d, i, t) in sorted(registry.items())\n"
        "           if d == doc_id][:len(new_chunk_texts)]\n"
        "    index.remove_ids(np.array(ids, dtype=\"int64\"))\n"
        "    index.add_with_ids(np.asarray(vecs, dtype=\"float32\"),\n"
        "                       np.array(ids, dtype=\"int64\"))\n"
        "    for cid, text in zip(ids, new_chunk_texts):\n"
        "        registry[cid] = (doc_id, registry[cid][1], text)\n\n"
        "# v2 of the policy: the 30-day window became 14 days, and the policy is\n"
        "# now SHORTER — it re-chunks to 2 chunks, not 3.\n"
        "V2_CHUNKS = [\n"
        "    \"Billing > Refunds: full refund within 14 days of purchase.\",\n"
        "    \"Billing > Refunds: no partial refunds for annual subscriptions.\",\n"
        "]\n"
        "update_document(\"refund-policy\", V2_CHUNKS)\n"
        "print(f\"index size after update: {index.ntotal}\")\n\n"
        "def search_chunks(query, k=3):\n"
        "    scores, ids = index.search(\n"
        "        np.asarray(embed([query]), dtype=\"float32\"), k)\n"
        "    return [(registry[int(i)][2], float(s))\n"
        "            for s, i in zip(scores[0], ids[0]) if i != -1]\n\n"
        "for text, score in search_chunks(\"do annual subscriptions get partial refunds\"):\n"
        "    print(f\"  {score:.3f}  {text}\")",
        "rev002",
    ),
    md(
        "**Question 1.** The search above asked about partial refunds for annual "
        "subscriptions. v2 of the policy says there are none — yet look at what "
        "ranked highly. Which chunk is it, which document version does it belong "
        "to, and exactly which line(s) of `update_document` let it survive?",
        "q1_001",
    ),
    md(
        "<details>\n<summary>🔑 Reveal answer — Question 1</summary>\n\n"
        "The v1 chunk \"annual subscriptions get prorated partial refunds\" is "
        "still in the index — the exact *opposite* of current policy. "
        "`update_document` slices the doc's chunk IDs to "
        "`[:len(new_chunk_texts)]` (2 of the 3) and replaces only those; v1's "
        "third chunk is never touched. This is the orphan defect: chunk-count "
        "changes on re-publish leave the old tail retrievable forever, and both "
        "policy versions now answer queries. The correct shape is "
        "**delete-everything-for-doc_id first** (`remove_ids` over *all* the "
        "doc's chunks, then add the new ones under fresh IDs).\n\n</details>",
        "q1_002",
    ),
    md(
        "**Question 2.** Write the corrected `update_document_fixed` "
        "(delete-then-insert by document), apply it (re-run the v2 update), and "
        "show the stale chunk is gone from the same search.",
        "q2_001",
    ),
    code(
        "# Work here: implement update_document_fixed(doc_id, new_chunk_texts)\n"
        "# then re-run the search from above.\n",
        "q2_002",
    ),
    md(
        "<details>\n<summary>🔑 Reveal answer — Question 2</summary>\n\n"
        "```python\n"
        "def update_document_fixed(doc_id, new_chunk_texts):\n"
        "    stale = [cid for cid, (d, i, t) in registry.items() if d == doc_id]\n"
        "    index.remove_ids(np.array(stale, dtype=\"int64\"))\n"
        "    for cid in stale:\n"
        "        del registry[cid]\n"
        "    add_chunks(doc_id, new_chunk_texts)\n\n"
        "update_document_fixed(\"refund-policy\", V2_CHUNKS)\n"
        "print(f\"index size: {index.ntotal}\")   # 2 — v1 fully gone\n"
        "for text, score in search_chunks(\"do annual subscriptions get partial refunds\"):\n"
        "    print(f\"  {score:.3f}  {text}\")\n"
        "```\n\n"
        "In production this delete-then-insert should also be atomic (or hidden "
        "behind a version field) so queries mid-update don't see a half-updated "
        "document.\n\n</details>",
        "q2_003",
    ),
    md(
        "**Question 3.** Nothing in this notebook pins which embedding model "
        "built the index. Describe the failure sequence if the query side upgrades "
        "to a different embedding model while these stored vectors remain, and the "
        "one-line assertion from the lesson that converts it into a loud error.",
        "q3_001",
    ),
    md(
        "<details>\n<summary>🔑 Reveal answer — Question 3</summary>\n\n"
        "Query vectors from model v2 are compared against document vectors from "
        "v1 — different embedding spaces — so similarity scores become noise and "
        "recall decays diffusely with no exception anywhere (dimensions often "
        "match, so nothing crashes). The guard: store "
        "`embedding_model` in the index metadata and assert at query time that "
        "the query-side model matches it — turning a silent quality collapse into "
        "a deployment error. A model upgrade then means a scheduled full-corpus "
        "re-embed.\n\n</details>",
        "q3_002",
    ),
    md(
        "**Question 4.** This lab's evals would not have caught the stale-chunk "
        "defect if the eval set had been labelled before the policy changed. Name "
        "the index-level monitors from the lesson that catch freshness failures "
        "answer-level evals cannot see.",
        "q4_001",
    ),
    md(
        "<details>\n<summary>🔑 Reveal answer — Question 4</summary>\n\n"
        "Ingestion lag (newest indexed change vs newest corpus change), "
        "per-document index age, orphan and tombstone counts, and — highest "
        "signal — a canary set of recently *edited* documents whose new content "
        "is verified retrievable (and old content verified gone) after each "
        "ingestion cycle.\n\n</details>",
        "q4_002",
    ),
    md(
        "## Summary\n\n"
        "1. Updates must be delete-then-insert keyed by _______, because "
        "re-chunking changes chunk counts.\n"
        "2. An orphaned chunk keeps _______ forever, with no error.\n"
        "3. An embedding model upgrade invalidates _______ stored vector.",
        "sum001",
    ),
    md(
        "<details>\n<summary>🔑 Reveal summary answers</summary>\n\n"
        "1. **document (doc_id)**\n"
        "2. **answering queries / being retrievable**\n"
        "3. **every**\n\n</details>",
        "sum002",
    ),
])

save("06-retrieval-metrics", L06)
save("07-rag-evals-faithfulness", L07)
save("08-index-maintenance-freshness", L08)


# ---------------------------------------------------------------------------
# Lesson 09 — debug: Permission-Aware Retrieval
# ---------------------------------------------------------------------------

L09 = nb([
    code(
        "# Lab type: debug\n"
        "# Course: AI402 — Retrieval & RAG Systems\n"
        "# Lesson: Permission-Aware and Multi-Tenant Retrieval\n"
        "# Task: The multi-tenant retrieval service below contains 3 bugs — one\n"
        "# recall bug, one leak, and one authorisation-staleness bug. Find and fix\n"
        "# each one; the demo queries make each visible if you look.",
        "meta00001",
    ),
    md(
        "# Lab: Debugging a Multi-Tenant Retriever\n\n"
        "Two tenants share an index: **acme** (2 documents) and **globex** (10 "
        "documents). Tenant size matters — one of the bugs only hurts the small "
        "tenant.\n\n"
        "**Outputs are cleared.** Run every cell top to bottom.",
        "intro001",
    ),
    md("## Setup: a two-tenant corpus", "setup001"),
    code(INSTALL, "setup002"),
    code(CORPUS_SRC, "setup003"),
    code(EMBED_SRC, "setup004"),
    code(
        "# acme's private docs (2) and globex's private docs (10, reusing the KB)\n"
        "TENANT_DOCS = [\n"
        "    (\"acme-contract\", \"acme\",\n"
        "     \"Contracts > Acme: Acme Corp's enterprise contract renews on March 1 \"\n"
        "     \"with a 15 percent negotiated discount and a 99.9 percent SLA.\"),\n"
        "    (\"acme-tickets\", \"acme\",\n"
        "     \"Support > Acme: Acme reported an SSO outage last quarter, resolved \"\n"
        "     \"by rotating the SAML certificate.\"),\n"
        "] + [(d, \"globex\", f\"{h}: {t}\") for d, h, t in CORPUS[:10]]\n\n"
        "T_IDS = [d for d, _, _ in TENANT_DOCS]\n"
        "T_TENANT = {d: ten for d, ten, _ in TENANT_DOCS}\n"
        "T_TEXTS = [t for _, _, t in TENANT_DOCS]\n"
        "T_EMB = embed(T_TEXTS)\n"
        "print(f\"{len(TENANT_DOCS)} docs: \"\n"
        "      f\"{sum(1 for d in T_IDS if T_TENANT[d]=='acme')} acme, \"\n"
        "      f\"{sum(1 for d in T_IDS if T_TENANT[d]=='globex')} globex\")",
        "setup005",
    ),
    md("## The service (contains 3 bugs)", "buggy001"),
    code(
        "# --- AI-GENERATED MULTI-TENANT RETRIEVAL SERVICE ---\n"
        "# Review this code — is it correct?\n"
        "query_cache = {}\n\n"
        "def search_for_tenant(query, tenant, k=3):\n"
        "    # cache retrievals to save embedding calls\n"
        "    if query in query_cache:                     # (bug candidate)\n"
        "        return query_cache[query]\n"
        "    scores = T_EMB @ embed([query])[0]\n"
        "    order = np.argsort(scores)[::-1][:k]         # (bug candidate)\n"
        "    results = [T_IDS[i] for i in order]\n"
        "    allowed = [d for d in results\n"
        "               if T_TENANT[d] == tenant]          # (bug candidate)\n"
        "    query_cache[query] = allowed\n"
        "    return allowed\n\n"
        "print(\"acme asks about its own contract:\")\n"
        "print(\"  \", search_for_tenant(\"when does our contract renew\", \"acme\"))\n"
        "print(\"globex asks the same question:\")\n"
        "print(\"  \", search_for_tenant(\"when does our contract renew\", \"globex\"))\n"
        "print(\"acme asks a generic product question:\")\n"
        "print(\"  \", search_for_tenant(\"how long is event data kept\", \"acme\"))",
        "buggy002",
    ),
    md(
        "## Bug 1: the second print\n\n"
        "globex asked about *its* contract and got acme's contract doc (or acme's "
        "cached results). Which line leaks across tenants, and why is this worse "
        "than a wrong answer?\n\n"
        "**Explain the bug:**\n\n"
        "*(Write your diagnosis here.)*",
        "bug1_001",
    ),
    md(
        "<details>\n<summary>🔑 Reveal answer — Bug 1</summary>\n\n"
        "**The bug:** `query_cache` is keyed on the query alone — no tenant in "
        "the key. globex's identical query returns acme's cached result list.\n\n"
        "**Why it causes wrong behaviour:** this is a cross-tenant data leak, not "
        "a relevance bug: acme's private doc IDs (and whatever is fetched with "
        "them downstream) are served to globex. It is also exactly the class of "
        "defect post-filter architectures invite — state between search and "
        "filter that doesn't carry the authorisation context.\n\n"
        "**Correct approach:** key the cache on `(tenant, query)` — or drop the "
        "cache entirely until the filter placement is fixed (Bug 3).\n\n</details>",
        "bug1_002",
    ),
    md(
        "## Bug 2: the third print\n\n"
        "acme asked a generic product question. The corpus has a perfectly good "
        "answer (`data-retention`) — why did acme get nothing (or nearly "
        "nothing), and which tenant will *never* notice this bug?\n\n"
        "**Explain the bug:**\n\n"
        "*(Write your diagnosis here.)*",
        "bug2_001",
    ),
    md(
        "<details>\n<summary>🔑 Reveal answer — Bug 2</summary>\n\n"
        "**The bug:** the search takes the global top-k *first* "
        "(`np.argsort(scores)[::-1][:k]` over all tenants' docs) and filters "
        "afterwards.\n\n"
        "**Why it causes wrong behaviour:** the candidate budget is spent on "
        "chunks acme cannot see. Wait — here the leak-filter keeps only acme docs "
        "out of a top-3 dominated by globex's larger corpus, so acme (2 of 12 "
        "docs) gets starved. globex, owning most of the corpus, never notices — "
        "which is why post-filtering looks like a \"small tenant relevance "
        "problem\" in production and gets mis-fixed by raising k.\n\n"
        "**Correct approach:** pre-filter — restrict the score computation (or "
        "the index itself, via per-tenant namespaces) to the tenant's own "
        "documents *before* taking top-k.\n\n</details>",
        "bug2_002",
    ),
    md(
        "## Bug 3: what nobody asked yet\n\n"
        "Suppose acme's contractor loses access, or a doc moves from `globex` to "
        "a restricted tenant. Where does this service's authorisation state live, "
        "and what is wrong with that?\n\n"
        "**Explain the bug:**\n\n"
        "*(Write your diagnosis here.)*",
        "bug3_001",
    ),
    md(
        "<details>\n<summary>🔑 Reveal answer — Bug 3</summary>\n\n"
        "**The bug:** `T_TENANT` was captured once at ingestion and — worse — "
        "results already sit in `query_cache` beyond any permission check at "
        "all: a revocation changes nothing already cached.\n\n"
        "**Why it causes wrong behaviour:** permission staleness is measured in "
        "exposure, not relevance. Cached result lists and ingestion-time ACL "
        "snapshots keep serving access that has been revoked.\n\n"
        "**Correct approach:** fast-path permission changes through the index "
        "update pipeline (ahead of content edits), keep volatile ACLs out of "
        "long-lived caches, and resolve fine-grained permissions against the live "
        "authorisation service at query time (as defence in depth on top of the "
        "tenant pre-filter).\n\n</details>",
        "bug3_002",
    ),
    md("## The fixed service + a leak regression test", "fix001"),
    code(
        "# Fix for Bugs 1-3: tenant-scoped pre-filter, tenant-keyed (minimal)\n"
        "# cache, and a cross-tenant leak test to gate regressions.\n"
        "def search_for_tenant_fixed(query, tenant, k=3):\n"
        "    mask = np.array([T_TENANT[d] == tenant for d in T_IDS])\n"
        "    idx = np.where(mask)[0]                    # tenant's docs only\n"
        "    scores = T_EMB[idx] @ embed([query])[0]    # pre-filtered search\n"
        "    order = idx[np.argsort(scores)[::-1][:k]]\n"
        "    return [T_IDS[i] for i in order]\n\n"
        "print(\"acme, generic question, full recall now:\")\n"
        "print(\"  \", search_for_tenant_fixed(\"how long is event data kept\", \"acme\"))\n"
        "print(\"globex, contract question, no acme docs:\")\n"
        "print(\"  \", search_for_tenant_fixed(\"when does our contract renew\", \"globex\"))\n\n"
        "def leak_test():\n"
        "    probes = [\"when does our contract renew\", \"sso outage\",\n"
        "              \"negotiated discount\", \"acme SLA\"]\n"
        "    for q in probes:\n"
        "        for d in search_for_tenant_fixed(q, \"globex\", k=5):\n"
        "            assert T_TENANT[d] == \"globex\", f\"LEAK: {d} via {q!r}\"\n"
        "    return \"leak test passed: no acme doc reachable from globex\"\n\n"
        "print(leak_test())",
        "fix002",
    ),
    md(
        "## Summary\n\n"
        "1. Post-filtering spends the candidate budget on chunks the tenant "
        "_______.\n"
        "2. The leak was a cache keyed on _______ alone.\n"
        "3. A leak is a retrieval result, so it is _______ like one — add the "
        "cross-tenant test to the regression gate.",
        "sum001",
    ),
    md(
        "<details>\n<summary>🔑 Reveal summary answers</summary>\n\n"
        "1. **cannot see** — small tenants starve, large tenants never notice.\n"
        "2. **the query** — no tenant in the key.\n"
        "3. **testable**\n\n</details>",
        "sum002",
    ),
])


# ---------------------------------------------------------------------------
# Lesson 10 — extend: RAG Observability and Cost
# ---------------------------------------------------------------------------

L10 = nb([
    code(
        "# Lab type: extend\n"
        "# Course: AI402 — Retrieval & RAG Systems\n"
        "# Lesson: RAG Observability and Cost\n"
        "# Task: A working two-stage pipeline is provided with NO instrumentation.\n"
        "# Extend it with a per-stage trace and a per-query cost model, then use\n"
        "# your own instruments to answer two questions with data.",
        "meta00001",
    ),
    md(
        "# Lab: Instrumenting a RAG Pipeline\n\n"
        "**Outputs are cleared.** Run every cell top to bottom.",
        "intro001",
    ),
    md("## Setup: the uninstrumented pipeline", "setup001"),
    code(INSTALL, "setup002"),
    code(CORPUS_SRC, "setup003"),
    code(EMBED_SRC, "setup004"),
    code(
        "from rank_bm25 import BM25Okapi\n\n"
        "def tokenize(text):\n"
        "    return [t.strip('.,:;()$').lower() for t in text.split()]\n\n"
        "bm25 = BM25Okapi([tokenize(t) for t in DOC_TEXTS])\n\n"
        "def rrf_fuse(rankings, k=60):\n"
        "    scores = {}\n"
        "    for ranking in rankings:\n"
        "        for rank, doc_id in enumerate(ranking, start=1):\n"
        "            scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + rank)\n"
        "    return sorted(scores, key=scores.get, reverse=True)\n\n"
        "INDEX_META = {\"index_version\": \"2026-09-02\", \"embedding_model\":\n"
        "              \"sentence-transformers/all-MiniLM-L6-v2\"}\n\n"
        "def rag_answer(query, top_k=3):\n"
        "    dense_ids = [d for d, _ in dense_search(query, k=8)]\n"
        "    bm25_scores = bm25.get_scores(tokenize(query))\n"
        "    bm25_ids = [DOC_IDS[i] for i in np.argsort(bm25_scores)[::-1][:8]]\n"
        "    fused = rrf_fuse([dense_ids, bm25_ids])[:top_k]\n"
        "    texts = {d: t for d, t in zip(DOC_IDS, DOC_TEXTS)}\n"
        "    context = \"\\n\\n\".join(texts[d] for d in fused)\n"
        "    prompt = f\"Context:\\n{context}\\n\\nQuestion: {query}\"\n"
        "    return prompt  # (generation call omitted — we instrument up to it)\n\n"
        "print(rag_answer(\"does the teams plan include sso\")[:200], \"...\")",
        "setup005",
    ),
    md(
        "## Extension 1: the per-stage trace\n\n"
        "Rewrite the pipeline as `rag_answer_traced(query)` returning "
        "`(prompt, trace)` where `trace` records: the raw query, each arm's "
        "ranked doc IDs, the fused list, the assembled context's doc IDs, the "
        "index metadata from `INDEX_META`, and a token estimate for the prompt "
        "(`len(prompt) // 4`). Record chunk/doc **IDs**, never full text — why?",
        "ext1_001",
    ),
    code(
        "def rag_answer_traced(query, top_k=3):\n"
        "    # TODO: same pipeline, plus a trace dict per the spec above\n"
        "    pass\n",
        "ext1_002",
    ),
    md(
        "<details>\n<summary>🔑 Reveal model answer — Extension 1</summary>\n\n"
        "```python\n"
        "def rag_answer_traced(query, top_k=3):\n"
        "    dense_ids = [d for d, _ in dense_search(query, k=8)]\n"
        "    bm25_scores = bm25.get_scores(tokenize(query))\n"
        "    bm25_ids = [DOC_IDS[i] for i in np.argsort(bm25_scores)[::-1][:8]]\n"
        "    fused = rrf_fuse([dense_ids, bm25_ids])[:top_k]\n"
        "    texts = {d: t for d, t in zip(DOC_IDS, DOC_TEXTS)}\n"
        "    context = \"\\n\\n\".join(texts[d] for d in fused)\n"
        "    prompt = f\"Context:\\n{context}\\n\\nQuestion: {query}\"\n"
        "    trace = {\n"
        "        \"query_raw\": query,\n"
        "        \"retrieval\": {\"dense\": dense_ids, \"bm25\": bm25_ids,\n"
        "                      **INDEX_META},\n"
        "        \"fused\": fused,\n"
        "        \"context_docs\": fused,\n"
        "        \"prompt_tokens_est\": len(prompt) // 4,\n"
        "    }\n"
        "    return prompt, trace\n"
        "```\n\n"
        "IDs, not text: a trace store holding full retrieved content is a second "
        "copy of the corpus outside its access controls — log readers, caches "
        "and retention schedules don't respect tenant boundaries. IDs keep the "
        "trace joinable to content under proper authorisation.\n\n</details>",
        "ext1_003",
    ),
    md(
        "## Extension 2: attribute a planted failure\n\n"
        "The query `\"how fast is priority support\"` should retrieve "
        "`priority-support`. Use *only your trace* (not the corpus) to determine: "
        "was it in the dense arm's list? the BM25 arm's? the fused top-3? the "
        "context? Write one sentence attributing the failure (or success) to a "
        "stage.",
        "ext2_001",
    ),
    code(
        "# Work here: run rag_answer_traced on the query and inspect the trace.\n",
        "ext2_002",
    ),
    md(
        "<details>\n<summary>🔑 Reveal model answer — Extension 2</summary>\n\n"
        "```python\n"
        "_, tr = rag_answer_traced(\"how fast is priority support\")\n"
        "for stage in (\"dense\", \"bm25\"):\n"
        "    print(stage, \"priority-support\" in tr[\"retrieval\"][stage],\n"
        "          tr[\"retrieval\"][stage])\n"
        "print(\"fused top-3:\", tr[\"fused\"])\n"
        "```\n\n"
        "Typical finding: both arms retrieve `priority-support` and it survives "
        "fusion — the stage-by-stage walk that took one dict lookup here is "
        "exactly the walk that is *impossible* when only the final prompt is "
        "logged. If it had been missing from the fused list but present in an "
        "arm, the attribution would be \"fusion/ranking\", and so on up the "
        "funnel.\n\n</details>",
        "ext2_003",
    ),
    md(
        "## Extension 3: the cost model\n\n"
        "Assume: generation input $3.00 per million tokens; query embedding "
        "$0.02 per million tokens (~queries are tiny); ignore vector-DB read "
        "cost. Using `prompt_tokens_est` averaged over all EVAL_SET queries, "
        "compute monthly cost at 1M queries/month for top_k=3 vs top_k=8. Then "
        "answer: which single number in this lab is the biggest billing knob?",
        "ext3_001",
    ),
    code(
        "# Work here: average prompt_tokens_est over EVAL_SET for top_k=3 and 8,\n"
        "# then monthly_cost = avg_tokens / 1e6 * 3.00 * 1_000_000 queries.\n",
        "ext3_002",
    ),
    md(
        "<details>\n<summary>🔑 Reveal model answer — Extension 3</summary>\n\n"
        "```python\n"
        "for k in (3, 8):\n"
        "    toks = [rag_answer_traced(q, top_k=k)[1][\"prompt_tokens_est\"]\n"
        "            for q, _ in EVAL_SET]\n"
        "    avg = sum(toks) / len(toks)\n"
        "    monthly = avg / 1e6 * 3.00 * 1_000_000\n"
        "    print(f\"top_k={k}: avg {avg:.0f} input tokens/query -> \"\n"
        "          f\"${monthly:,.0f}/month at 1M queries\")\n"
        "```\n\n"
        "The retrieved-context size — `top_k` × chunk length — is the dominant "
        "knob: every retrieved chunk is billed again as generation input on "
        "every query, and it scales linearly with both. This is why \"just "
        "retrieve more\" has a precise monthly price, and why prompt caching "
        "can't rescue it (retrieved context differs per query).\n\n</details>",
        "ext3_003",
    ),
    md(
        "## Summary\n\n"
        "1. Traces record chunk _______, never full text.\n"
        "2. Failure attribution = checking each stage's recorded output for the "
        "expected doc, from _______ backwards.\n"
        "3. The dominant RAG cost line is retrieved context billed as _______.",
        "sum001",
    ),
    md(
        "<details>\n<summary>🔑 Reveal summary answers</summary>\n\n"
        "1. **IDs**\n"
        "2. **generation/context assembly** (the last stage)\n"
        "3. **generation input tokens**\n\n</details>",
        "sum002",
    ),
])

save("09-permission-aware-retrieval", L09)
save("10-rag-observability-cost", L10)


# ---------------------------------------------------------------------------
# Lesson 11 — review: Agentic and Iterative Retrieval
# ---------------------------------------------------------------------------

L11 = nb([
    code(
        "# Lab type: review\n"
        "# Course: AI402 — Retrieval & RAG Systems\n"
        "# Lesson: Agentic and Iterative Retrieval\n"
        "# Task: A scripted agentic retrieval loop is below (the 'model' is a\n"
        "# deterministic stand-in, so no API key is needed). Run it and judge the\n"
        "# orchestration: what is enforced, what is merely hoped for.",
        "meta00001",
    ),
    md(
        "# Lab: Reviewing an Agentic Retrieval Loop\n\n"
        "The `scripted_model` below plays the LLM's role with a fixed policy so "
        "the loop's *orchestration* can be studied deterministically: it answers "
        "a multi-hop question by first finding a customer, then searching for "
        "that customer's renewal.\n\n"
        "**Outputs are cleared.** Run every cell top to bottom.",
        "intro001",
    ),
    md("## Setup", "setup001"),
    code(INSTALL, "setup002"),
    code(CORPUS_SRC, "setup003"),
    code(EMBED_SRC, "setup004"),
    code(
        "# Extra docs that make the question multi-hop\n"
        "AGENT_DOCS = CORPUS + [\n"
        "    (\"ticket-stats\", \"Support > Quarterly stats\",\n"
        "     \"Acme Corp filed 41 support tickets last quarter, the most of any \"\n"
        "     \"customer. Globex filed 12.\"),\n"
        "    (\"acme-renewal\", \"Contracts > Acme\",\n"
        "     \"Acme Corp renewed its Enterprise contract on March 1 for two years.\"),\n"
        "]\n"
        "A_IDS = [d[0] for d in AGENT_DOCS]\n"
        "A_TEXTS = [f\"{d[1]}: {d[2]}\" for d in AGENT_DOCS]\n"
        "A_EMB = embed(A_TEXTS)\n\n"
        "def search_kb(query, k=2):\n"
        "    \"\"\"The tool: the same funnel every lab has used (dense here).\"\"\"\n"
        "    scores = A_EMB @ embed([query])[0]\n"
        "    order = np.argsort(scores)[::-1][:k]\n"
        "    return [(A_IDS[i], A_TEXTS[i], float(scores[i])) for i in order]\n\n"
        "QUESTION = \"did the customer who filed the most tickets last quarter renew?\"",
        "setup005",
    ),
    md("## The loop under review", "rev001"),
    code(
        "# --- THE ORCHESTRATION LOOP (review this code — is it correct?) ---\n"
        "def scripted_model(question, observations):\n"
        "    \"\"\"Deterministic stand-in for the LLM's tool-use decisions.\"\"\"\n"
        "    seen = \" \".join(t for _, t, _ in observations)\n"
        "    if \"most of any customer\" not in seen:\n"
        "        return (\"search\", \"which customer filed the most support tickets last quarter\")\n"
        "    if \"renewed\" not in seen:\n"
        "        return (\"search\", \"did Acme Corp renew its contract\")\n"
        "    return (\"answer\", \"Yes — Acme Corp (most tickets: 41) renewed on March 1.\")\n\n"
        "def agentic_answer(question):\n"
        "    observations = []\n"
        "    while True:                                   # <- look closely\n"
        "        action, payload = scripted_model(question, observations)\n"
        "        if action == \"answer\":\n"
        "            return payload, observations\n"
        "        observations += search_kb(payload)         # <- and here\n\n"
        "answer, obs = agentic_answer(QUESTION)\n"
        "print(\"answer:\", answer)\n"
        "print(f\"hops: {len(obs) // 2}, observations: {[d for d, _, _ in obs]}\")",
        "rev002",
    ),
    md(
        "**Question 1.** Single-shot retrieval cannot answer QUESTION well — "
        "demonstrate it: run `search_kb(QUESTION, k=3)` and explain, from the "
        "results, why the second hop's query could not have been written up "
        "front.",
        "q1_001",
    ),
    md(
        "<details>\n<summary>🔑 Reveal answer — Question 1</summary>\n\n"
        "Single-shot retrieval finds `ticket-stats` (the question's vocabulary "
        "matches it) but has no reason to rank `acme-renewal` highly — the "
        "question never mentions Acme. \"Acme\" only enters the picture after "
        "reading the first hop's result; the second query is *derived from the "
        "first answer*, which no up-front rewrite or decomposition can know. "
        "That dependency is the definition of a multi-hop question.\n\n</details>",
        "q1_002",
    ),
    md(
        "**Question 2.** The loop works on this happy path. List what bounds it: "
        "iteration cap? token budget? latency budget? What happens if "
        "`scripted_model` is replaced by a real LLM that keeps choosing "
        "\"search\" — and whose job is it to prevent that?",
        "q2_001",
    ),
    md(
        "<details>\n<summary>🔑 Reveal answer — Question 2</summary>\n\n"
        "Nothing bounds it: `while True` with no iteration cap, no token budget, "
        "no latency budget. A real model that never reaches an \"answer\" state "
        "spins until something external breaks, accumulating context (and cost) "
        "each hop. Enforcement belongs to the **orchestrator** — a hard cap on "
        "search calls (3–5 typical), per-request token/latency budgets checked "
        "in the loop — because the model does not reliably know when to stop. "
        "Telling it to \"search within reason\" is a hope, not a control.\n\n</details>",
        "q2_002",
    ),
    md(
        "**Question 3.** Add the guards: rewrite `agentic_answer` with "
        "`max_searches=3` and a `token_budget` (estimate tokens as "
        "`len(text) // 4` accumulated over observations); on breach, return the "
        "honest failure `(\"budget exhausted\", observations)`. Verify the happy "
        "path still completes in 2 hops.",
        "q3_001",
    ),
    code(
        "# Work here: bounded agentic_answer with max_searches and token_budget.\n",
        "q3_002",
    ),
    md(
        "<details>\n<summary>🔑 Reveal answer — Question 3</summary>\n\n"
        "```python\n"
        "def agentic_answer_bounded(question, max_searches=3, token_budget=2000):\n"
        "    observations, searches, tokens = [], 0, 0\n"
        "    while True:\n"
        "        action, payload = scripted_model(question, observations)\n"
        "        if action == \"answer\":\n"
        "            return payload, observations\n"
        "        if searches >= max_searches or tokens > token_budget:\n"
        "            return \"budget exhausted\", observations\n"
        "        results = search_kb(payload)\n"
        "        observations += results\n"
        "        searches += 1\n"
        "        tokens += sum(len(t) // 4 for _, t, _ in results)\n\n"
        "print(agentic_answer_bounded(QUESTION)[0])   # completes in 2 hops\n"
        "```\n\n"
        "The budget check lives in the loop, not in the model's prompt — the "
        "orchestrator owns the guarantee.\n\n</details>",
        "q3_003",
    ),
    md(
        "**Question 4.** The final answer above is correct. Explain why a "
        "final-answer-only eval would still under-specify this system, and what "
        "the lesson says a multi-hop eval set must label.",
        "q4_001",
    ),
    md(
        "<details>\n<summary>🔑 Reveal answer — Question 4</summary>\n\n"
        "A correct final answer can be reached by lucky wandering — querying the "
        "wrong customer and stumbling onto the right doc scores identically to a "
        "sound trajectory. Multi-hop eval sets label the *intermediate* answers "
        "(here: hop 1 must identify Acme via `ticket-stats`; hop 2 must retrieve "
        "`acme-renewal`), so per-hop retrieval quality, convergence, and "
        "stopping behaviour are all measurable — trajectory evaluation on top of "
        "answer evaluation.\n\n</details>",
        "q4_002",
    ),
    md(
        "## Summary\n\n"
        "1. Agentic retrieval enables _______ questions, where the next query "
        "depends on the last result.\n"
        "2. Loop bounds are enforced by the _______, never the model.\n"
        "3. Trajectory evals need labelled _______ answers, not just final ones.",
        "sum001",
    ),
    md(
        "<details>\n<summary>🔑 Reveal summary answers</summary>\n\n"
        "1. **multi-hop**\n"
        "2. **orchestrator**\n"
        "3. **intermediate**\n\n</details>",
        "sum002",
    ),
])


# ---------------------------------------------------------------------------
# Lesson 12 — prompt: Capstone audit
# ---------------------------------------------------------------------------

L12 = nb([
    code(
        "# Lab type: prompt\n"
        "# Course: AI402 — Retrieval & RAG Systems\n"
        "# Lesson: Auditing an AI-Built RAG Pipeline: Capstone\n"
        "# Task: Direct an AI assistant to build a RAG pipeline for the Nimbus\n"
        "# corpus twice (naive prompt, then directive prompt), paste each output\n"
        "# below unmodified, and audit both against the 7-point protocol.",
        "meta00001",
    ),
    md(
        "# Capstone: Direct, Then Audit\n\n"
        "This is the course's judgment–direction–verification loop run end to "
        "end. You will prompt an AI assistant (any current one) to build a RAG "
        "pipeline, paste its output here **unmodified**, and audit it "
        "stage-by-stage. Wrong or defective AI output is not a problem — it is "
        "the point: the audit is where the learning happens.\n\n"
        "**Outputs are cleared.** Run the setup, then work top to bottom.",
        "intro001",
    ),
    md("## Setup: the corpus the pipeline must serve", "setup001"),
    code(INSTALL, "setup002"),
    code(CORPUS_SRC, "setup003"),
    md(
        "## The task (give this scenario to the AI)\n\n"
        "> Build a production RAG pipeline in Python for a product knowledge "
        "base of ~1,000 Markdown documents with headings and tables, serving "
        "three customer tenants. Documents are edited daily. Query traffic "
        "mixes error-code lookups and natural-language questions. Include "
        "ingestion, indexing, retrieval, and an evaluation harness.\n\n"
        "You will prompt twice:\n\n"
        "- **Round 1 (naive):** ask in one sentence, e.g. *\"Build me a RAG "
        "pipeline in Python for a Markdown knowledge base.\"*\n"
        "- **Round 2 (directive):** specify what this course taught you to "
        "specify — chunking strategy for structured Markdown, hybrid retrieval "
        "with RRF fusion, a widened funnel with re-ranking, delete-then-insert "
        "updates keyed by document, tenant pre-filtering inside the search, and "
        "an eval harness with named metrics at named k values (zeros kept in "
        "averages).",
        "task001",
    ),
    md(
        "## Your prompts\n\n"
        "**Round 1 prompt:**\n\n*(paste here)*\n\n"
        "**Round 2 prompt:**\n\n*(paste here)*",
        "prompts001",
    ),
    md("## Round 1 output — paste the assistant's code, unmodified", "r1_001"),
    code(
        "# PASTE the AI assistant's Round 1 code here, unmodified.\n"
        "# Do not fix anything — the audit below is where defects get recorded.\n",
        "r1_002",
    ),
    md(
        "## The audit protocol\n\n"
        "Audit each round against these 7 checks, in pipeline order. Each check "
        "is testable by inspection — cite the line(s) of pasted code that pass "
        "or fail it.\n\n"
        "1. **Chunking**: boundaries respect document structure (headings/"
        "tables); every chunk carries doc_id + heading path + tenant metadata.\n"
        "2. **Update path**: document changes are delete-then-insert keyed by "
        "doc_id (no chunk-ID upserts that orphan old tails); embedding model "
        "version pinned and asserted.\n"
        "3. **Retrieval**: hybrid where traffic warrants (error codes ⇒ yes "
        "here); fusion by RRF over ranks, never weighted score sums; one "
        "tokeniser at index and query time.\n"
        "4. **Funnel**: stage-one k meaningfully wider than final top-k; "
        "re-ranking present; a relevance floor for the honest no-answer.\n"
        "5. **Evaluation**: recall@k / MRR computed correctly, at the k "
        "production uses, zero-scoring queries kept; eval queries are realistic "
        "phrasings, not document titles.\n"
        "6. **Permissions**: tenant filter inside the search (or per-tenant "
        "namespaces), never after it; no cross-tenant cache keys.\n"
        "7. **Observability & cost**: per-stage trace with chunk IDs (not "
        "text); someone did the input-token arithmetic for top-k × chunk size.",
        "audit001",
    ),
    code(
        "audit_round_1 = {\n"
        "    \"1 chunking\":        \"PASS/FAIL — evidence: ...\",\n"
        "    \"2 update path\":     \"PASS/FAIL — evidence: ...\",\n"
        "    \"3 retrieval/fusion\": \"PASS/FAIL — evidence: ...\",\n"
        "    \"4 funnel\":          \"PASS/FAIL — evidence: ...\",\n"
        "    \"5 evaluation\":      \"PASS/FAIL — evidence: ...\",\n"
        "    \"6 permissions\":     \"PASS/FAIL — evidence: ...\",\n"
        "    \"7 observability\":   \"PASS/FAIL — evidence: ...\",\n"
        "}\n"
        "for k, v in audit_round_1.items():\n"
        "    print(f\"{k:20} {v}\")",
        "audit002",
    ),
    md("## Round 2 output — paste the assistant's code, unmodified", "r2_001"),
    code(
        "# PASTE the AI assistant's Round 2 code here, unmodified.\n",
        "r2_002",
    ),
    code(
        "audit_round_2 = {\n"
        "    \"1 chunking\":        \"PASS/FAIL — evidence: ...\",\n"
        "    \"2 update path\":     \"PASS/FAIL — evidence: ...\",\n"
        "    \"3 retrieval/fusion\": \"PASS/FAIL — evidence: ...\",\n"
        "    \"4 funnel\":          \"PASS/FAIL — evidence: ...\",\n"
        "    \"5 evaluation\":      \"PASS/FAIL — evidence: ...\",\n"
        "    \"6 permissions\":     \"PASS/FAIL — evidence: ...\",\n"
        "    \"7 observability\":   \"PASS/FAIL — evidence: ...\",\n"
        "}\n"
        "for k, v in audit_round_2.items():\n"
        "    print(f\"{k:20} {v}\")",
        "audit003",
    ),
    md(
        "## Reflection\n\n"
        "1. Which checks did direction fix between Round 1 and Round 2?\n"
        "2. Which defect survived the directive prompt — and was it in something "
        "you specified, or something you left unspecified?\n"
        "3. If you could add one sentence to your Round 2 prompt, what would it "
        "be?\n\n"
        "*(Write your reflection here.)*",
        "reflect001",
    ),
    md(
        "**Instructor note — expected failure modes.** Round 1 outputs "
        "typically fail checks 1 (fixed-size character chunks, no metadata), 2 "
        "(no update path at all, or chunk-ID upsert), 4 (retrieve k = final k, "
        "no re-ranker), 5 (no eval harness, or accuracy-style hit@1 mislabelled), "
        "6 (single-tenant assumption or post-filter), and 7 (no tracing). Round "
        "2 outputs usually pass the named checks but fail in the unspecified "
        "remainder — most often check 2's atomicity/model-version pinning, check "
        "4's relevance floor, and check 7's ID-only trace discipline (full chunk "
        "text logged). If a student's Round 2 audit shows all 7 passing, ask "
        "them to find the silent default the assistant chose that they never "
        "specified (chunk size numbers, k values, cache keys, tokeniser choice) "
        "— there is always at least one.",
        "instr001",
    ),
])

save("11-agentic-iterative-retrieval", L11)
save("12-auditing-ai-built-rag-capstone", L12)
print("Done.")
