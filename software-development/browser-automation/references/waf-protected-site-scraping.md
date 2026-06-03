# WAF-protected site scraping with agent-browser stealth

Concrete patterns for extracting content from Cloudflare/Akamai-protected sites that blocked curl and headless Chrome. The stealth extension + Chrome flags combo has been verified against multiple WAF-protected domains including job aggregators, AI model pricing pages, and SaaS documentation portals.

## When to use this

Sites behind Cloudflare, Akamai, or DataDome typically block standard headless Chrome by detecting `navigator.webdriver`, missing plugin arrays, and other automation fingerprints. The stealth extension patches these vectors at `document_start` — before the page's own scripts run. Use this BEFORE falling back to alternative extraction methods.

## Prerequisites: stealth extension loaded

Always use the full stealth combo before hitting job aggregators:

```bash
agent-browser close --all
agent-browser \
  --args "--no-sandbox,--disable-gpu,--disable-dev-shm-usage,--disable-blink-features=AutomationControlled,--no-first-run,--no-default-browser-check" \
  --user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36" \
  --extension "$SKILL_DIR/assets/stealth-extension" \
  open "https://www.indeed.com/jobs?q=KEYWORDS&l=LOCATION&sort=date"
sleep 4
agent-browser set viewport 1920 1080
```

Verify stealth before trusting page content:
```bash
agent-browser eval "JSON.stringify({webdriver: navigator.webdriver})"
# Expected: {"webdriver":false}
```

If webdriver is `true`, Cloudflare detected automation — the stealth extension isn't loading (check path, `--extension` syntax).

## General extraction approach

Once the stealth session is established:

```javascript
// Full page text dump (bulk extraction)
document.body.innerText.substring(0, 8000)

// Extract all links with text
Array.from(document.querySelectorAll('a[href]'))
  .map(a => ({text: a.textContent.trim(), href: a.href}))
  .filter(x => x.text)

// Extract structured data from JSON-LD
const ld = document.querySelector('script[type="application/ld+json"]');
ld ? JSON.parse(ld.textContent) : null

// Extract table data
Array.from(document.querySelectorAll('table tbody tr'))
  .map(row => Array.from(row.querySelectorAll('td')).map(td => td.textContent.trim()))
```

## Real-world use cases

### AI model pricing & capabilities pages
Many AI/ML provider pages (OpenAI, Anthropic, Google AI) use Cloudflare on their documentation and pricing sections:
```javascript
// Extract model pricing table
document.body.innerText
```

### SaaS documentation behind WAF
Cloudflare-protected docs sites can be scraped for API references, changelogs, and feature comparisons:
```bash
agent-browser eval "Array.from(document.querySelectorAll('article, main, .content, .docs')).map(el => el.innerText).join('\\n')"
```

### E-commerce product pages
Major retailers and marketplaces often use bot protection on product listings:
```javascript
// Extract product names and prices
Array.from(document.querySelectorAll('[class*=\"product\" i], [class*=\"price\" i], [class*=\"title\" i], [data-testid*=\"product\" i]'))
  .map(e => e.textContent.trim()).filter(Boolean).slice(0, 30)
```

### Web application E2E testing
Login flows, form submissions, and dashboard interactions on WAF-protected apps:
```bash
agent-browser --args "--no-sandbox,--disable-gpu,--disable-blink-features=AutomationControlled" \
  --user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
  --extension "$SKILL_DIR/assets/stealth-extension" \
  open "https://app.example.com/login"
agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "password"
agent-browser click @e3
```

## Employer-direct fallback

If an aggregator or job board remains blocked despite the stealth combo, go direct to the organization's own application portal. These (BambooHR, Paylocity, Workday, ADP) rarely have the same level of bot protection. See `references/employer-direct-job-scraping.md` for patterns covering:
- BambooHR — JSON-LD structured data extraction
- Paylocity — table-based listing extraction
- Workday — JS-rendered portal extraction
