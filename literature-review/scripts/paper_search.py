#!/usr/bin/env python3
"""
paper_search.py — Search academic databases and validate paper URLs/DOIs.

Usage:
    python3 paper_search.py search --query "attention mechanism transformer" --limit 20
    python3 paper_search.py validate --url "https://arxiv.org/abs/1706.03762"

Output (search): JSON array of paper objects to stdout
Output (validate): "OK", "PAYWALLED", or "NOT_FOUND" to stdout

Dependencies: requests (pip install requests)
"""

import sys
import json
import argparse
import urllib.parse
import urllib.request
import urllib.error
import time

try:
    import requests
except ImportError:
    print("ERROR: requests is required. Install with: pip install requests")
    sys.exit(1)


# ── Semantic Scholar ──────────────────────────────────────────────────────────

def search_semantic_scholar(query, limit=20):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "limit": min(limit, 100),
        "fields": "title,authors,year,abstract,url,externalIds,openAccessPdf"
    }
    try:
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        data = r.json()
        papers = []
        for p in data.get("data", []):
            pdf = p.get("openAccessPdf") or {}
            paper_url = pdf.get("url") or p.get("url") or ""
            if not paper_url:
                eids = p.get("externalIds") or {}
                doi = eids.get("DOI")
                arxiv = eids.get("ArXiv")
                if arxiv:
                    paper_url = f"https://arxiv.org/abs/{arxiv}"
                elif doi:
                    paper_url = f"https://doi.org/{doi}"
            authors = p.get("authors") or []
            author_str = ", ".join(a.get("name", "") for a in authors[:5])
            if len(authors) > 5:
                author_str += " et al."
            papers.append({
                "name": p.get("title", ""),
                "url": paper_url,
                "date": str(p.get("year", "")),
                "authors": author_str,
                "abstract": (p.get("abstract") or "")[:500],
                "source": "Semantic Scholar",
                "paywalled": not bool(pdf.get("url"))
            })
        return papers
    except Exception as e:
        sys.stderr.write(f"Semantic Scholar error: {e}\n")
        return []


# ── arXiv ─────────────────────────────────────────────────────────────────────

def search_arxiv(query, limit=20):
    base = "http://export.arxiv.org/api/query"
    params = urllib.parse.urlencode({
        "search_query": f"all:{query}",
        "max_results": limit,
        "sortBy": "relevance",
        "sortOrder": "descending"
    })
    try:
        with urllib.request.urlopen(f"{base}?{params}", timeout=15) as resp:
            body = resp.read().decode("utf-8")
        papers = []
        entries = body.split("<entry>")[1:]
        for entry in entries:
            def extract(tag):
                start = entry.find(f"<{tag}")
                if start == -1:
                    return ""
                start = entry.find(">", start) + 1
                end = entry.find(f"</{tag}>", start)
                return entry[start:end].strip() if end != -1 else ""

            title = extract("title").replace("\n", " ")
            arxiv_id = extract("id").split("/abs/")[-1].strip()
            url = f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else ""
            date = extract("published")[:10]
            summary = extract("summary").replace("\n", " ")[:500]

            # Authors
            author_blocks = entry.split("<author>")[1:]
            names = []
            for ab in author_blocks:
                n = ab.split("<name>")[-1].split("</name>")[0].strip()
                if n:
                    names.append(n)
            author_str = ", ".join(names[:5])
            if len(names) > 5:
                author_str += " et al."

            if title:
                papers.append({
                    "name": title,
                    "url": url,
                    "date": date,
                    "authors": author_str,
                    "abstract": summary,
                    "source": "arXiv",
                    "paywalled": False
                })
        return papers
    except Exception as e:
        sys.stderr.write(f"arXiv error: {e}\n")
        return []


# ── PubMed ────────────────────────────────────────────────────────────────────

def search_pubmed(query, limit=20):
    esearch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    efetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    try:
        params = {
            "db": "pubmed", "term": query, "retmax": limit,
            "retmode": "json", "sort": "relevance"
        }
        r = requests.get(esearch_url, params=params, timeout=15)
        r.raise_for_status()
        ids = r.json().get("esearchresult", {}).get("idlist", [])
        if not ids:
            return []

        time.sleep(0.4)  # NCBI rate limit

        fetch_params = {
            "db": "pubmed", "id": ",".join(ids),
            "rettype": "abstract", "retmode": "xml"
        }
        fr = requests.get(efetch_url, params=fetch_params, timeout=20)
        fr.raise_for_status()
        xml = fr.text

        papers = []
        articles = xml.split("<PubmedArticle>")[1:]
        for article in articles:
            def extract_xml(tag):
                start = article.find(f"<{tag}>")
                if start == -1:
                    return ""
                start += len(tag) + 2
                end = article.find(f"</{tag}>", start)
                return article[start:end].strip() if end != -1 else ""

            title = extract_xml("ArticleTitle")
            pmid = extract_xml("PMID")
            url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else ""
            year = extract_xml("Year")
            abstract = extract_xml("AbstractText")[:500]

            # Authors
            author_blocks = article.split("<Author ")[1:] + article.split("<Author>")[1:]
            names = []
            for ab in article.split("<LastName>")[1:]:
                last = ab.split("</LastName>")[0].strip()
                if last:
                    names.append(last)
            author_str = ", ".join(names[:5])
            if len(names) > 5:
                author_str += " et al."

            if title:
                papers.append({
                    "name": title,
                    "url": url,
                    "date": year,
                    "authors": author_str,
                    "abstract": abstract,
                    "source": "PubMed",
                    "paywalled": False
                })
        return papers
    except Exception as e:
        sys.stderr.write(f"PubMed error: {e}\n")
        return []


# ── Deduplication ─────────────────────────────────────────────────────────────

def deduplicate(papers):
    seen = set()
    result = []
    for p in papers:
        key = p["name"].lower().strip()
        if key not in seen:
            seen.add(key)
            result.append(p)
    return result


# ── Validate ──────────────────────────────────────────────────────────────────

def validate_paper(url):
    """Check if a paper URL/DOI is accessible. Returns OK, PAYWALLED, or NOT_FOUND."""
    if not url.startswith("http"):
        url = f"https://doi.org/{url}"
    try:
        r = requests.head(url, timeout=10, allow_redirects=True,
                          headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code == 200:
            # Check if final URL suggests open access
            final = r.url
            if any(x in final for x in ["arxiv.org", "pubmed", "pmc", "biorxiv",
                                          "semanticscholar", "openreview"]):
                print("OK")
                return
            print("OK")
        elif r.status_code in (401, 403, 402):
            print("PAYWALLED")
        else:
            print("NOT_FOUND")
    except Exception:
        print("NOT_FOUND")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command")

    s = sub.add_parser("search")
    s.add_argument("--query", required=True)
    s.add_argument("--limit", type=int, default=20)
    s.add_argument("--sources", default="semantic_scholar,arxiv,pubmed",
                   help="Comma-separated list of sources to query")

    v = sub.add_parser("validate")
    v.add_argument("--url", required=True)

    args = parser.parse_args()

    if args.command == "search":
        sources = [s.strip() for s in args.sources.split(",")]
        all_papers = []
        per_source = max(1, args.limit // len(sources))

        if "semantic_scholar" in sources:
            all_papers += search_semantic_scholar(args.query, per_source)
        if "arxiv" in sources:
            all_papers += search_arxiv(args.query, per_source)
        if "pubmed" in sources:
            all_papers += search_pubmed(args.query, per_source)

        papers = deduplicate(all_papers)[:args.limit]
        print(json.dumps(papers, ensure_ascii=False, indent=2))

    elif args.command == "validate":
        validate_paper(args.url)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
