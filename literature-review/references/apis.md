# Academic API Reference

Reference for the three databases used by `paper_search.py`. Read this file when debugging search failures or adjusting query strategies.

## Semantic Scholar

**Endpoint:** `GET https://api.semanticscholar.org/graph/v1/paper/search`

**Key params:**
- `query` — free-text search
- `limit` — max 100 per request
- `fields` — comma-separated: `title,authors,year,abstract,url,externalIds,openAccessPdf`

**Response fields:**
- `data[].title` — paper title
- `data[].authors[].name` — author names
- `data[].year` — publication year
- `data[].abstract` — abstract text
- `data[].url` — Semantic Scholar page URL
- `data[].openAccessPdf.url` — direct PDF URL (null if paywalled)
- `data[].externalIds.DOI`, `.ArXiv` — external IDs

**Rate limit:** ~100 req/5 min without API key. No key needed for basic search.

**Tip:** Semantic Scholar has the broadest coverage across CS, ML, and biomedical fields. Prioritize it for general queries.

---

## arXiv

**Endpoint:** `GET http://export.arxiv.org/api/query`

**Key params:**
- `search_query` — e.g. `all:attention mechanism`, `ti:transformer`, `au:Vaswani`
- `max_results` — default 10, max 2000
- `sortBy` — `relevance` | `lastUpdatedDate` | `submittedDate`
- `sortOrder` — `descending` | `ascending`

**Field prefixes for search_query:**
- `ti:` — title
- `au:` — author
- `abs:` — abstract
- `all:` — all fields

**Response:** Atom XML. Each `<entry>` has `<title>`, `<id>` (URL), `<published>`, `<summary>`, `<author><name>`.

**Paper URL format:** `https://arxiv.org/abs/{arxiv_id}`

**Rate limit:** 3 req/sec. No key needed.

**Tip:** Best for ML, physics, math, CS preprints. Papers are always open access.

---

## PubMed (NCBI E-utilities)

**Step 1 — ESearch** (get IDs):
`GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi`
- `db=pubmed`, `term=<query>`, `retmax=<limit>`, `retmode=json`, `sort=relevance`

**Step 2 — EFetch** (get metadata):
`GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi`
- `db=pubmed`, `id=<comma-separated PMIDs>`, `rettype=abstract`, `retmode=xml`

**Response XML fields:**
- `<ArticleTitle>` — title
- `<PMID>` — PubMed ID → URL: `https://pubmed.ncbi.nlm.nih.gov/{PMID}/`
- `<Year>` inside `<PubDate>` — year
- `<AbstractText>` — abstract
- `<LastName>` inside `<Author>` — author surnames

**Rate limit:** 3 req/sec without API key. Add `&api_key=<key>` for 10 req/sec.

**Tip:** Best for biomedical, clinical, and life sciences literature.

---

## DOI Resolution

For paywalled papers detected by `paper_search.py --validate`:
- Try `https://doi.org/{DOI}` — redirects to publisher page
- Check `https://unpaywall.org/api/v2/{DOI}?email=test@test.com` for open-access versions
- Suggest Sci-Hub or Unpaywall to the user; do not automate access to paywalled content

---

## Query Tips

| Goal | Strategy |
|---|---|
| Find papers on a specific topic | Use broad query in Semantic Scholar first |
| Find papers by a specific author | Use `au:Surname` in arXiv or `Author[au]` in PubMed |
| Find papers from a specific year | Add year range in Semantic Scholar `year` filter |
| Biomedical topics | Prefer PubMed |
| ML/AI topics | Prefer Semantic Scholar + arXiv |
| Missing results | Try synonym terms or split into two narrower searches |
