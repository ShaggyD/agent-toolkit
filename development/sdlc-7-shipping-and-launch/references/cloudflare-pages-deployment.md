# Cloudflare Pages Deployment

Static site deployment through Cloudflare Pages, with a GitHub repo and domain managed at Cloudflare.

## When This Applies

- Deploying a static site (HTML, JS, CSS, or framework output) to Cloudflare Pages
- Domain already registered at Cloudflare (auto-DNS for Pages)
- GitHub as the source of truth for the code

## Prerequisites

- Cloudflare account (with the domain)
- GitHub repo with the site code
- No local API credentials needed — setup is done in dashboard

## Setup Walkthrough

### Step 1: Prepare the Repo

Create the GitHub repo first (see `github-repo-management` skill). The repo should have the site code on the `main` branch — Cloudflare Pages auto-deploys from it.

**Common build output dirs by framework:**
| Framework | Build command | Output dir |
|-----------|--------------|------------|
| Plain HTML/JS/CSS | (none) | . (root) |
| Hugo | `hugo` | `public/` |
| Next.js (static) | `next build && next export` | `out/` |
| React/Vite | `npm run build` | `dist/` |
| Astro | `npm run build` | `dist/` |

### Step 2: Connect to Cloudflare Pages (Dashboard)

1. Go to **Cloudflare Dashboard → Workers & Pages → Create → Pages → Connect to Git**
2. Authorize GitHub if prompted
3. Select the repo
4. **Build settings:**
   - Framework preset: pick from dropdown (or "None" for plain HTML)
   - Build command: as needed (empty for plain HTML)
   - Build output directory: as needed (`.` for root, `dist/`, `public/`, etc.)
5. **Environment variables** — add any needed during build (set later via Pages dashboard if missed)
6. Click **Save and Deploy**

### Step 3: Domain Setup

Because the domain is **already at Cloudflare**, Pages auto-suggests it:

1. In the Pages project → **Custom domains → Set up a custom domain**
2. Type `codegrit.dev` (or your domain)
3. Cloudflare creates the `CNAME` DNS record automatically
4. SSL certificate provisions automatically (Cloudflare edge cert)

**No manual DNS changes needed** — this is the advantage of buying the domain at Cloudflare.

### Step 4: Auto-Deploy

After the first deploy, every `git push` to main triggers a new build and deploy:

```bash
git add .
git commit -m "your changes"
git push origin main
# Cloudflare Pages picks this up automatically
```

## Manual Deploy (via wrangler CLI)

Optional — if `wrangler` is installed and authenticated:

```bash
# Install wrangler
npm install -g wrangler

# Auth
wrangler login

# Deploy from project root
wrangler pages deploy ./dist --project-name=codegrit-dev

# Or set up with a config file
npx wrangler pages project create
```

## Post-Deploy Checklist

- [ ] Site loads at the custom domain (not just the `*.pages.dev` URL)
- [ ] SSL working (HTTPS, padlock)
- [ ] All routes work (no 404s on SPA routes — add a `_redirects` or `_headers` file if needed)
- [ ] CDN cache warming: Cloudflare caches at the edge automatically
- [ ] Branch previews: Cloudflare Pages creates preview deployments for PRs (useful for review)

## Common Pitfalls

- **`_headers` and `_redirects` files** go in the **build output directory**, not the repo root. For plain HTML sites, they go at the repo root (because the output = root).
- **SPA fallback**: For single-page apps, create `_redirects` with `/* /index.html 200` in the output dir so client-side routing works.
- **Build failures**: Check the Cloudflare Pages build logs in the dashboard. Common causes: missing `NODE_VERSION` env var, missing build deps, wrong output directory.
- **First deploy takes ~2 minutes**, subsequent deploys are faster (cache).
- **Custom domain propagation** is instant for Cloudflare domains — no waiting on DNS.
