# Employer-Direct Job Scraping

When job aggregators (Indeed, LinkedIn, ZipRecruiter, SimplyHired) block headless Chrome behind Cloudflare/WAF, go directly to the employer's own career page. Employer-hosted ATS portals (BambooHR, Paylocity, Workday, ADP, Taleo, iCIMS) rarely block automation.

## Workflow

### 1. Find the employer career page

Usually `{company}.com/careers` or `careers.{company}.com`. For well-known employers in a region, search:

```
web_search("{company name} careers job openings")
```

### 2. Open with anti-detection flags

Always use the full Cloudflare bypass combo:

```bash
agent-browser close --all
agent-browser --args "--no-sandbox,--disable-gpu,--disable-dev-shm-usage,--disable-blink-features=AutomationControlled" \
  --user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36" \
  open "https://{company}.com/careers"
```

Then set viewport before interacting:

```bash
agent-browser set viewport 1920 1080
```

### 3. Find all job links via eval

Use JavaScript to extract links, filtering for relevant titles:

```bash
agent-browser eval "Array.from(document.querySelectorAll('a')).map(a => ({text: a.textContent.trim(), href: a.href})).filter(x => x.text.includes('keyword') || x.text.includes('keyword'))"
```

For Paylocity portals, links are in tables — extract full text:

```bash
agent-browser eval "document.body.innerText"
```

### 4. Open individual listing

Navigate to the specific job detail page and extract full description:

```bash
agent-browser open "https://{ats-portal-url}/jobs/details/{id}"
agent-browser eval "document.body.innerText"
```

Paylocity detail pages have structured JSON-LD with salary, location, and description — check for it:

```bash
agent-browser eval "document.querySelector('script[type=\"application/ld+json\"]')?.textContent"
```

### 5. Apply link

Send the direct apply URL to the user for them to open on their own device.

## ATS Portal Patterns

| ATS | URL Pattern | Extraction Method |
|-----|------------|-------------------|
| **BambooHR** | `{company}.bamboohr.com/careers/{id}` | JSON-LD script tag + body text |
| **Paylocity** | `recruiting.paylocity.com/Recruiting/Jobs/Details/{id}` | body text (JS-rendered, eval works) |
| **Workday** | `{company}.wd1{num}.myworkdayjobs.com/...` | body text (complex JS, may need snapshot) |
| **ADP** | `recruiting.adp.com/...` | body text |
| **Greenhouse** | `boards.greenhouse.io/{company}/jobs/{id}` | body text, often easy to scrape |
| **Lever** | `jobs.lever.co/{company}/{id}` | body text, simple layout |
| **iCIMS** | `careers-{company}.icims.com/jobs/{id}` | body text |

## Example: Paylocity Portal

```bash
# Step 1: Find job listings page (use the employer's Paylocity URL)
agent-browser --args "..." --user-agent "..." open \
  "https://recruiting.paylocity.com/recruiting/jobs/All/{org-id}/{ORG-NAME}"

# Step 2: Extract all listings
agent-browser eval "document.body.innerText"

# Step 3: Open specific listing
agent-browser open \
  "https://recruiting.paylocity.com/Recruiting/Jobs/Details/{job-id}"

# Step 4: Get full description
agent-browser eval "document.body.innerText"
```

## Example: BambooHR Portal

```bash
# Step 1: Open jobs listing page (BambooHR doesn't block — no anti-detection needed)
agent-browser open "https://{company}.bamboohr.com/careers"

# Step 2: Find links for relevant positions
agent-browser eval "Array.from(document.querySelectorAll('a')).filter(a => a.textContent.includes('keyword')).map(a => ({text: a.textContent.trim(), href: a.href}))"

# Step 3: Open specific listing
agent-browser open "https://{company}.bamboohr.com/careers/{id}"

# Step 4: Extract details — BambooHR has JSON-LD structured data
agent-browser eval "document.querySelector('script[type=\"application/ld+json\"]')?.textContent"

# Step 5: Get full readable description
agent-browser eval "document.body.innerText"
```

## Pitfalls

- **Session reuse**: Always `agent-browser close --all` between different sites to clear cookies and avoid cross-site state issues.
- **Dynamic ref IDs**: Don't rely on snapshot ref IDs across sessions — they change each time. Use eval with CSS selectors instead.
- **Job is stale**: Listings posted >30 days ago may be filled but not taken down. Check the `datePosted` in JSON-LD or the posting date in the table.
- **Paylocity rendering**: Paylocity uses client-side JS. `snapshot -i` may show limited content. Always use `eval "document.body.innerText"` for full extraction.
- **Workday complexity**: Workday portals are heavy JS apps. If `eval` returns nothing useful, try `snapshot` and scroll first before extracting.
