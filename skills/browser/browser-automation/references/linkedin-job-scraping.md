# LinkedIn job scraping with agent-browser stealth

LinkedIn uses aggressive bot detection, but its job search endpoint (`/jobs/search/`) is **accessible without authentication** when the full stealth combo (Chrome flags + real UA + stealth extension + viewport) is applied. No sign-in wall, no CAPTCHA, no "verify you're human" challenge.

## Stealth open

```bash
agent-browser close --all
agent-browser \
  --args "--no-sandbox,--disable-gpu,--disable-dev-shm-usage,--disable-blink-features=AutomationControlled,--no-first-run,--no-default-browser-check" \
  --user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36" \
  --extension "$SKILL_DIR/assets/stealth-extension" \
  open "https://www.linkedin.com/jobs/search/?keywords=KEYWORDS&location=LOCATION&f_TPR=r604800"
sleep 4
agent-browser set viewport 1920 1080
```

URL parameters:
- `keywords` — job title or keywords (URL-encoded)
- `location` — city/state or ZIP (URL-encoded)
- `f_TPR=r604800` — last 7 days filter (r604800 = 604,800 seconds). Omit for all time.
- `distance=10` — miles radius filter (add if needed)
- `geoId` — LinkedIn's internal geo ID (optional, omit for location string matching)

## Why LinkedIn is harder than other sites

LinkedIn rotates CSS class names per session. A selector like `.job-card-container__title` that worked yesterday may not work today. Never hardcode single CSS classes — use the multi-selector fallback approach.

## Multi-CSS-selector extraction pattern

Query every known class variant + semantic attribute selectors in a single `querySelectorAll` call:

```javascript
// Step 1: Collect job card elements with broad selectors
const jobs = Array.from(document.querySelectorAll(
  '.job-card-container, .base-card, .job-search-card, ' +
  'li[class*="jobs-search-results__list-item"], ' +
  'div[class*="job-card"]'
));

// Step 2: Extract structured fields from each card
const results = jobs.map((j, i) => {
  const titleEl = j.querySelector(
    '.job-card-list__title, .base-search-card__title, ' +
    '.job-card-container__link, h3, ' +
    'a[data-anonymize="job-title"], ' +
    'a[class*="job-title"]'
  );
  const companyEl = j.querySelector(
    '.job-card-container__company-name, .base-search-card__subtitle, ' +
    '.job-card-container__primary-description, ' +
    '.base-search-card__info h4 a, ' +
    'span[class*="company-name"]'
  );
  const locationEl = j.querySelector(
    '.job-card-container__metadata-item, .base-search-card__metadata, ' +
    '.job-card-container__secondary-description, ' +
    'span[class*="location"]'
  );
  const timeEl = j.querySelector(
    '.job-card-container__listed-state, time, ' +
    '.job-search-card__listed-time, ' +
    'span[class*="listed-time"]'
  );

  return {
    index: i + 1,
    title: titleEl?.innerText.trim() || 'N/A',
    company: companyEl?.innerText.trim() || 'N/A',
    location: locationEl?.innerText.trim() || '',
    time: timeEl?.innerText.trim() || '',
    link: (titleEl?.tagName === 'A' ? titleEl : titleEl?.querySelector('a'))?.href
          || j.querySelector('a[href*="/jobs/view"]')?.href
          || ''
  };
});

// Step 3: Return as JSON for downstream parsing
JSON.stringify(results);
```

## Fallback: full page text

If structured extraction returns 0 results (classes changed entirely):

```javascript
// Bulk text dump — parse with regex
document.body.innerText

// Or extract all links with context
Array.from(document.querySelectorAll('a[href*="/jobs/view"]'))
  .map(a => ({title: a.innerText.trim(), href: a.href}))
  .filter(x => x.title)
```

## Verified behavior

- **Auth required?** No — job search results render fully without cookies/login
- **CAPTCHA encountered?** No — stealth combo bypasses it entirely
- **Rate limiting?** Not observed on moderate use (5-10 queries per session)
- **Results per page:** ~20-25 per page. Add `&start=25` for page 2, `&start=50` for page 3, etc.
- **Login-wall redirect:** LinkedIn redirects `/feed/` and profile pages to `/uas/login` for unauthenticated sessions — job search is the main endpoint that works without auth

## Job detail page extraction (salary, type, description)

Search result cards show only title, company, and location — **not salary, employment type, or seniority level**. These live on the individual job detail page (`/jobs/view/{id}`). To get them, open each job's URL directly.

### Navigating to a detail page

Each job card's link from the multi-selector extraction points to a URL like `https://www.linkedin.com/jobs/view/{job-title}-at-{company}-{numeric-id}`. Navigate to it with a fresh stealth session:

```bash
agent-browser close --all
agent-browser \
  --args "--no-sandbox,--disable-gpu,--disable-dev-shm-usage,--disable-blink-features=AutomationControlled,--no-first-run,--no-default-browser-check" \
  --user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36" \
  --extension "$SKILL_DIR/assets/stealth-extension" \
  open "https://www.linkedin.com/jobs/view/office-receptionist-at-serenity-healthcare-4424232194"
sleep 3
```

**Important:** `--extension`, `--args`, and `--user-agent` flags are **ignored if a daemon is already running**. Always `close --all` before opening a new detail page with the stealth combo.

### Extracting salary, type, and metadata

The detail page's `<main>` element contains a plain-text dump with structured fields. Extract them by filtering for known labels:

```bash
agent-browser eval "
const text = document.querySelector('main')?.innerText || '';
const lines = text.split('\\\\n').filter(l => {
  const t = l.trim();
  return t.includes('Employment type') || t.includes('Salary') ||
         t.includes('\$') || t.includes('hour') ||
         t.includes('Part-time') || t.includes('Full-time') ||
         t.includes('Seniority') || t.includes('Job function') ||
         t.includes('Industries');
});
JSON.stringify(lines);
"
```

Expected output shape (each present field shows on its own line):
```
["Employment type", "Full-time", "Seniority level", "Entry level", "Industries", "IT Services and IT Consulting"]
```

### Full page text dump

For complete job description, summary stats, and all metadata:

```bash
agent-browser eval "document.querySelector('main')?.innerText?.substring(0, 3000)"
```

This returns everything: title, company, location, time posted, salary range (if provided), employment type, seniority level, job function, industries, and the full description body.

### What fields are typically available

| Field | Example | Notes |
|---|---|---|
| Employment type | `Full-time` / `Part-time` | Usually present |
| Salary range | `$18.00/hr - $24.00/hr` or `$23.28 - $34.98 Hourly` | ~40% of postings include it |
| Seniority level | `Entry level` / `Mid-Senior level` | Usually present |
| Job function | `Administrative`, `Customer Service` | Usually present |
| Industries | `IT Services and IT Consulting` | Company-level metadata |
| Pay range disclaimer | `Base pay range` / `Provided by {company}` | Indicates employer-provided salary |
| FT/PT status | `FT / PT Status – Full-Time` | Sometimes in description header |

### Known salary format patterns

```javascript
// Employer-provided pay ranges — found near top of description
"Base pay range\\n$18.00/hr - $24.00/hr"

// Inline at top of description (state/municipal jobs)
"FT / PT Status – Full-Time Salary – $23.28 - $34.98 Hourly"

// Scattered in perks/bullet section
"Competitive compensation package starting at $16 per hour"
"TIME COMMITMENT: 15 hours per week"
"SALARY: $17.00 - $18.00/hour"
```

### Sign-in overlay dismissal

Sometimes clicking a job card or opening a detail page triggers a LinkedIn sign-in overlay ("Sign in to view more jobs" or "Sign in to tailor your resume"). It has a dismiss button:

```bash
# Dismiss the sign-in overlay
agent-browser click @e1   # ref=e1 is always "Dismiss" button
sleep 2
# Reload the main content
agent-browser eval "document.querySelector('main')?.innerText?.substring(0, 1000)"
```

If `@e1` doesn't work, check the snapshot for any button containing "Dismiss" or "Close".

### Batch extraction strategy

To enrich a list of search results with salary/type data:

1. Extract job URLs from search results (multi-selector pattern above)
2. For each URL, `close --all` then load with full stealth combo
3. Extract detail fields via the eval pattern above
4. Merge back into the results table (title → append type + salary columns)

Target the most promising jobs first (by recency, location fit, title match) — not all 19+ listings need detail extraction.

## Applying this across sessions

When LinkedIn changes its DOM structure (every few months), add the new class names to each `querySelectorAll` call rather than replacing the existing ones. Keeping all historical selectors ensures resilience against rolling class changes where some users see old classes and others see new ones.
