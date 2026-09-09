# SEO release — deployment runbook

For whoever deploys `pestcontrol` to **the-skystar.com**. Self-contained: you do not
need context from the work that produced it.

This release changes **how every public URL on the site resolves**. Read
[Before you start](#before-you-start) and [Rollback](#rollback) first — one setting
must be configured *before* traffic arrives, and it cannot be undone afterwards.

- **Branch:** `feature/website-template-integration`
- **Requires:** frappe v16, python 3.14
- **Downtime:** none expected; `bench migrate` is additive

---

## What this release does

| | Before | After |
|---|---|---|
| Language seen by a crawler | English only — Arabic invisible to search | `/ar/…` and `/en/…`, both indexed |
| `<title>` on `/` | `Skystar - Environmental Services` (generic default) | Per language, admin-editable |
| `<meta name="description">` | `""` — empty on every page | Real, per language |
| Canonical / hreflang | none | On every page, reciprocal |
| Structured data | none | `@graph` on every page |
| `sitemap.xml` | 30 URLs, **no landing pages** | 78 URLs with hreflang alternates |
| `robots.txt` | empty | Populated (step 4) |
| Lazy-loaded images | 0 of 57 | 56 of 57 |
| Largest image | 1499 KB | 393 KB (all photos: 8.5 MB → 2.5 MB) |
| Arabic webfont | 28 files / 497 KB | 16 files / 282 KB |

**URLs change.** `/` and `/about` now redirect to `/ar/` and `/ar/about`. Existing
document URLs (`/service/…`, `/blog/…`) keep their slugs and gain a language prefix.

---

## Before you start

### 1. The one irreversible step

**`PC Website Settings → SEO & Analytics → Default Language` must be set to `ar`
before the first visitor arrives.**

`/` issues a permanent (301) redirect to `/<default language>/`. Browsers and
crawlers cache a 301 more or less forever. If the field is empty at deploy time the
code falls back to `en`, and visitors who hit `/` in that window will keep being
sent to `/en/` from their own cache — for that site, on that browser, indefinitely.

Set it in the same maintenance window, before opening traffic.

### 2. Route audit (informational — currently clean)

This release makes `WebsiteGenerator.set_route()` run, which had never executed
before. On save it backfills empty routes and normalises any route with a leading
`/` or trailing `.`.

Audited against current content: **24 routes stable, 0 would change, 0 would be
created.** No redirects are needed. Re-run this if content changed since:

```sql
SELECT 'Website Service' dt, name, route FROM `tabWebsite Service` WHERE published=1
UNION ALL SELECT 'Website Project', name, route FROM `tabWebsite Project` WHERE published=1
UNION ALL SELECT 'Website Blog Post', name, route FROM `tabWebsite Blog Post` WHERE published=1
UNION ALL SELECT 'Website Pest', name, route FROM `tabWebsite Pest` WHERE published=1
UNION ALL SELECT 'Website Team Member', name, route FROM `tabWebsite Team Member` WHERE published=1;
```

Any row with an empty route, a leading `/`, or a trailing `.` will change on its next
save and needs a `website_redirects` entry.

### 3. Back up `/files/`

This release adds a hook that **resizes uploaded images in place**, replacing the
original. It only touches images attached to website content, and skips anything
already under 1600px — but it is destructive by design. Back up the site's
`public/files` before the first upload after deploy.

---

## Deploy

```bash
cd /path/to/bench
git -C apps/pestcontrol pull origin feature/website-template-integration

bench --site the-skystar.com migrate        # required: this release adds fields
bench --site the-skystar.com clear-cache
bench restart
```

`migrate` is not optional. It creates the `Website Article` SEO fields, the
`PC Website Settings` SEO & Analytics tab, the `Website Branch` location fields and
the `Website Opening Hours` child table.

The code tolerates running *before* migrate — image and SEO fields simply stay
inert rather than erroring — but nothing works until it has run.

---

## Configure

### `PC Website Settings` → SEO & Analytics tab

| Field | Value |
|---|---|
| **Default Language** | `ar` ← **set before traffic (see above)** |
| Canonical Base URL | `https://the-skystar.com` |
| Google Business Profile URL | *the company's Google listing* — see [Content owner](#for-the-content-owner) |
| GA4 Measurement ID | `G-…` if analytics is wanted; leave blank to emit nothing |
| Google Tag Manager ID | `GTM-…` — takes precedence over GA4; do not set both expecting both |

Canonical Base URL matters behind a proxy: without it, URLs are built from frappe's
`get_url()`, which can emit an internal hostname. A wrong canonical is worse than
none.

### `Website Settings` → `robots_txt`

Currently empty. Paste exactly:

```
User-agent: *
Disallow: /app
Disallow: /api/
Disallow: /portal
Disallow: /me
Disallow: /orders
Disallow: /invoices
Disallow: /quotations
Disallow: /account/
Disallow: /*?_lang=
Allow: /

Sitemap: https://the-skystar.com/sitemap.xml
```

This field also filters the generator sitemap, so the two stay consistent.

---

## Verify

```bash
./verify_seo.sh https://the-skystar.com      # from the app directory — expect 42/42
```

If that script is unavailable, the checks that matter:

```bash
curl -sI https://the-skystar.com/            # 301 -> /ar/
curl -sI https://the-skystar.com/about       # 301 -> /ar/about
curl -sLo /dev/null -w '%{http_code}\n' https://the-skystar.com/app     # 200 — DESK
curl -so /dev/null -w '%{http_code}\n' https://the-skystar.com/api/method/ping   # 200
# 3 alternates: ar, en, x-default. Match the <link> tags specifically -- the
# language switcher anchors also carry an hreflang attribute.
curl -s https://the-skystar.com/ar/about | grep -c '<link rel="alternate" hreflang'   # 3
curl -s https://the-skystar.com/sitemap.xml | grep -c '<loc>'            # 2 per page
```

**Check `/app` loads the desk.** It is the highest-severity failure mode and the
quickest to confirm.

Then, in Search Console: resubmit `sitemap.xml`. Expect a rise in *Page with
redirect* (normal — every old URL now redirects). **Redirect errors are not
expected.** Watch International Targeting for hreflang errors over the following
week.

---

## Rollback

**Language URLs — the whole feature, one line.**

```python
# apps/pestcontrol/pestcontrol/hooks.py — delete this line:
website_path_resolver = "pestcontrol.pc_website.router.resolve"
```
then `bench --site the-skystar.com clear-cache && bench restart`.

URLs revert to unprefixed immediately. Note that browsers which already cached the
`/` → `/ar/` redirect will keep following it until their cache expires; the
unprefixed URLs still serve correctly, so this is cosmetic rather than breaking.

**Why this line first:** frappe 16 short-circuits only `desk` before the website
hooks — there is no `/app` shortcut — so this resolver handles `/app` and `/api`
too. If the desk or the API misbehaves after deploy, remove this line before
investigating anything else.

**Other features, independently:**

| Remove from `hooks.py` | Disables |
|---|---|
| `update_website_context = …seo.build_seo_context` | all meta tags, canonical, JSON-LD |
| `doc_events = {"File": …}` | automatic image resizing on upload |

**Full rollback:** `git revert` the three commits (`2d1e712`, `9e3978d`, `e1df58d`),
then `bench migrate && bench clear-cache && bench restart`. The added fields are
additive and harmless if left in place.

---

## For the content owner

None of this needs a developer, and the structured data is thin until the first item
is done.

1. **Fill `Google Business Profile URL`** in PC Website Settings. It is the single
   highest-value field for local search — it tells Google the site and the Google
   listing are the same business.
2. **Delete the placeholder branch** named `يبليبلبل`. Its city, address and phone
   (`5555555`) are test data. It is currently prevented from being published as a
   real business location only because it has no map coordinates.
3. **Complete the Madinah branch** — set its city in the Article table. It already
   has address, phone and coordinates, so setting the city is the last thing needed
   before it appears in search as a real location.
4. Optionally fill Legal Name, CR Number, Founding Year and Price Range — each adds
   a line to the business's structured data.

### Where to write meta titles and descriptions

Per page, per language, inside the record itself:

> Open the blog post / service → scroll to the **Article** table → **click a row to
> expand it** → collapsible **SEO** section → Meta Title, Meta Description, Share Image.

The SEO fields are only visible once a row is expanded — the grid shows just
Language, Title, Subtitle and Context.

All three are optional. Left blank: Meta Title falls back to the Title, Meta
Description to the Subtitle then the body, Share Image to the record's own image.
Fill them only when the search-result wording should differ from the on-page
wording.

One behaviour: if a Meta Title **is** written it is used verbatim, without the
`| Sky Star` suffix — the assumption being the whole string was chosen deliberately.
Leave it blank and the brand is appended automatically.

---

## Not included in this release

- **Script deferral.** 17 blocking scripts and ~690 lines of inline JS remain. The
  inline blocks contain `{{ csrf_token }}` and translated strings, so they cannot
  simply move to a static file — it needs a config-object refactor touching every
  form and the accessibility toolbar.
- **Non-critical CSS** is still render-blocking.
- **Per-city landing pages.** The `LocalBusiness` machinery is in place and gated on
  data; city pages themselves were not built.
