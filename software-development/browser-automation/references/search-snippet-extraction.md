# Search Snippet Extraction (WAF/CAPTCHA Workaround)

When a target site uses aggressive anti-bot protection (DataDome, Cloudflare Turnstile, etc.) that blocks all direct access including headless Chrome and curl, but Google still indexes its pages, use Google search snippets as a data extraction fallback.

## When to use

- `agent-browser` shows a CAPTCHA iframe (DataDome) or blank page (Cloudflare)
- curl/wget also blocked or challenged
- Google search results still show the target domain with descriptive snippets

## How it works

Google indexes page content including job descriptions, skills sections, and meta descriptions. These appear in search result snippets. By constructing targeted site searches, you can extract structured data from the snippets alone.

## Technique

```python
from hermes_tools import web_search

# Target the site with relevant query terms
results = web_search("site:targetdomain.com/jobs required skills", limit=50)

# Extract data from search result descriptions
for r in results.get('data', {}).get('web', []):
    title = r.get('title', '')
    description = r.get('description', '')
    url = r.get('url', '')
    # Process description text for skills, requirements, etc.
```

## Query strategy

| Goal | Query Pattern | Notes |
|------|--------------|-------|
| Broad corpus | `site:domain.com/jobs` | Returns everything, but snippets may not contain skills section |
| Skills-focused | `site:domain.com/jobs "required skills"` | Targets pages with explicit skills sections |
| Category filter | `site:domain.com/jobs engineer "required skills"` | Narrow by job category |
| Qualifications | `site:domain.com/jobs qualifications experience` | Alternative to skills keyword |

## Limitations

- Snippets are ~200 characters — full job descriptions are not captured
- Biased toward jobs that explicitly mention "required skills" or "qualifications" in the indexed text
- Skills listed deeper in descriptions (after the snippet cut-off) are missed — undercounts cloud/infra/generic skills
- Suitable for **aggregate/corpus analysis** (top skills across 100+ postings, trend direction) but NOT for individual job detail
- Multiple search queries needed to hit 100+ unique results (use deduplication by URL)

## Confirmed use case

Extracting top skills from Wellfound.com (DataDome-protected) across ~100 job postings:
- Multiple queries with `site:wellfound.com/jobs` + skill-related keywords
- Deduplicated by URL
- Extracted skill mentions via regex pattern matching on title + description
- Produced directional frequency data (AI/LLM 13%, React 4%, Python 3% of postings)
