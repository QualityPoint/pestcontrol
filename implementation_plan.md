# Build CMS Admin Dashboard for Pest Control Website

## Goal

Build the **CMS layer** on top of the existing website pages at `D:\skyStar\template\pestcontrol-develop`. The HTML template files are already placed in the correct Frappe structure (`www/`, `public/website/`). Now we need:

1. **Shared Jinja includes** — eliminate 17x header/footer duplication
2. **CMS DocTypes** — admin dashboard to manage all website content
3. **Jinja templating** — make pages dynamic (read from DocTypes)
4. **Website generators** — detail pages for services, blog, team, projects
5. **Arabic / RTL support** — structural i18n baked in from Phase 1, not bolted on later

---

## What's Already Done ✅

- 16 pages in `www/` with correct Frappe routes
- Static assets in `public/website/` (CSS, JS, images, webfonts, icons)
- Skystar branding (logo, navigation, copyright `{{ year }}`)
- Slider homepage variant selected
- All asset paths rewritten to `/assets/pestcontrol/website/...`

---

## Decisions Locked In

| Question | Decision | Why |
|---|---|---|
| **Asset loading** (was open item #6 in review) | Keep pages standalone (own `<html>`/`<head>`), do **not** use `hooks.py` `web_include_css`/`web_include_js` | Those hooks only inject into pages that extend Frappe's `templates/web.html`. Our pages don't (and shouldn't) — extending it would pull in Frappe's own Bootstrap 4 + site chrome, which collides with the template's own Bootstrap 5 library. DRY-ing up CSS/JS `<link>`/`<script>` tags happens via our own shared includes instead (Phase 1), preserving the template's design exactly. |
| **Q1: Bootstrap version** | Standalone pages, template's own Bootstrap 5 stack, no Frappe base template | Same reasoning as above — this *is* the "keep it standalone" answer to Q1. |
| **Q2: Blog approach** | ~~Reuse Frappe core `Blog Post`~~ — **custom `Website Blog Post` DocType** | Originally planned to reuse core `Blog Post`/`Blog Category`/`Blogger`. Verified against the actual site (Frappe v16.30.0): **none of those doctypes exist in core anymore** — blogging was removed from Frappe core in v16. Built `Website Blog Post` in the `PC Website` module instead (title/route/blog_category/author fields/published/blog_intro/content, each with an `_ar` counterpart, plus `website_tags`). |
| **Q3: Arabic/RTL** | Yes, from the start. Structure now, translations filled in incrementally | See dedicated section below. |
| **Q4: Contact form target** | Still open — `Website Contact Message` vs. CRM `Lead` | Pending decision. |

---

## Arabic / RTL Approach (answers Q3)

Frappe's native mechanism, adapted for our standalone pages:

- **UI chrome strings** (nav, buttons, footer copy) go through `{{ _("...") }}` and get translated via `translations/ar.csv` in the app — standard Frappe translation pipeline (`bench get-untranslated` / `bench update-translations`).
- **`dir`/`lang` attributes**: Frappe's base template (`web.html`) sets these automatically, but our pages are standalone, so we set them ourselves once, in the shared includes: `<html lang="{{ lang }}" dir="{{ 'rtl' if lang == 'ar' else 'ltr' }}">`.
- **Language switching**: enable Arabic via `Website Settings.languages` (Frappe's built-in multi-language website feature — route prefixing, language switcher).
- **RTL stylesheet**: no RTL CSS ships with the template today (checked — `public/website/css/` has no `*rtl*` file). We write `skystar-rtl.css` as an additive override loaded conditionally when `dir == 'rtl'`, rather than replacing the LTR stylesheet.
- **CMS content translation** (service descriptions, blog posts, testimonials — not fixed UI strings): Frappe has no built-in field-level translation for custom DocTypes. Chosen approach: **parallel `_ar` fields** on each content DocType (e.g. `service_name` / `service_name_ar`, `short_description` / `short_description_ar`). Simple for two languages, one record per item, easy for admins to edit both languages side by side.
- **Timing**: structural pieces (dir/lang attributes, language settings wiring, `_ar` fields on new DocTypes, RTL stylesheet skeleton) are built into Phase 1 and Phase 2 now, since retrofitting them into already-built templates/doctypes later is expensive. Actually translating every string into Arabic is incremental and doesn't block shipping English-only initially.

---

## Proposed Changes

### Phase 1 — Shared Includes (Kill Duplication) + i18n Structure

Extract repeated HTML blocks into reusable Jinja includes. This touches **all 17 existing www/ files** but only removes code, replacing it with `{% include %}` tags.

#### [NEW] `pestcontrol/templates/includes/website_head.html`
The shared `<head>` block — meta, fonts, and **the template's own** CSS library (not Frappe's):
```html
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
...
<link href="/assets/pestcontrol/website/css/bootstrap.min.css" rel="stylesheet">
<link href="/assets/pestcontrol/website/css/custom.css" rel="stylesheet">
<link href="/assets/pestcontrol/website/css/skystar.css" rel="stylesheet">
{% if dir == "rtl" %}
<link href="/assets/pestcontrol/website/css/skystar-rtl.css" rel="stylesheet">
{% endif %}
```

#### [NEW] `pestcontrol/templates/includes/website_topbar.html`
Topbar with email, address, social links — ~30 lines. Will later read from `PC Website Settings`.

#### [NEW] `pestcontrol/templates/includes/website_navbar.html`
Full navigation header (logo, menu, CTA button) — ~55 lines. Will later read from `PC Website Settings`.

#### [NEW] `pestcontrol/templates/includes/website_footer.html`
Footer (about text, service links, quick links, contact, socials, copyright) — ~100 lines.

#### [NEW] `pestcontrol/templates/includes/website_scripts.html`
All `<script>` tags — the template's own library stack (jQuery 3.7.1, Bootstrap 5 JS, Swiper, GSAP, `function.js`, etc.) — ~35 lines. No Frappe `web_include_js`.

#### [NEW] `pestcontrol/templates/includes/page_header.html`
The breadcrumb + page title hero used on inner pages — ~20 lines. Accepts `page_title` variable.

#### [NEW] `pestcontrol/templates/includes/cta_section.html`
The CTA block ("Ready for a Pest-Free Life?") used on multiple pages — ~25 lines.

#### [MODIFY] All 17 `www/*.html` files
Replace duplicated header/footer/scripts with includes, and set `dir`/`lang` on `<html>`:
```html
<!DOCTYPE html>
<html lang="{{ lang }}" dir="{{ 'rtl' if lang == 'ar' else 'ltr' }}">
<head>
    {% include "pestcontrol/templates/includes/website_head.html" %}
    <title>{{ page_title }} - Skystar</title>
</head>
<body>
    {% include "pestcontrol/templates/includes/website_topbar.html" %}
    {% include "pestcontrol/templates/includes/website_navbar.html" %}

    <!-- Page-specific content stays here -->

    {% include "pestcontrol/templates/includes/website_footer.html" %}
    {% include "pestcontrol/templates/includes/website_scripts.html" %}
</body>
</html>
```

**Result:** Each page shrinks by ~250 lines. Total reduction: ~4,000 lines of duplication eliminated.

---

### Phase 2 — CMS DocTypes (Admin Dashboard)

Add a new module `PC Website` to [modules.txt](file:///d:/skyStar/template/pestcontrol-develop/pestcontrol/modules.txt).

Every translatable content field below gets a parallel `_ar` field (Data/Small Text/Text Editor matching the source field's type) per the Arabic approach above — not written out per-field in every table to keep this readable, but assume `field_name_ar` exists alongside every translatable `field_name`.

#### [NEW] `PC Website Settings` — Single DocType
The main admin control panel for global site settings:

| Field | Type | Purpose |
|---|---|---|
| **Brand** tab | | |
| `site_name` | Data | Brand name (default: "Skystar") |
| `logo` | Attach Image | Header logo |
| `footer_logo` | Attach Image | Footer logo |
| `favicon` | Attach Image | Browser favicon |
| **Contact** tab | | |
| `email` | Data | Email shown in topbar + footer |
| `phone` | Data | Phone number |
| `address` | Small Text | Address text |
| `address_ar` | Small Text | Address text (Arabic) |
| `whatsapp` | Data | WhatsApp number |
| **Social Links** tab | | |
| `instagram_url` | Data | |
| `facebook_url` | Data | |
| `twitter_url` | Data | |
| `linkedin_url` | Data | |
| **Footer** tab | | |
| `about_footer_text` | Text | Footer about paragraph |
| `about_footer_text_ar` | Text | Footer about paragraph (Arabic) |
| `copyright_text` | Data | Copyright line |
| **Languages** tab | | |
| *(uses core `Website Settings.languages`, not a custom field — enable Arabic there)* | | |
| **Counters** tab | | |
| `years_experience` | Int | "29+ Years" counter |
| `projects_completed` | Data | "2K" counter |
| `team_size` | Int | "50" counter |
| `satisfaction_rate` | Int | "98%" counter |

#### [NEW] `Website Service`

| Field | Type |
|---|---|
| `service_name` | Data (reqd, unique) |
| `service_name_ar` | Data |
| `route` | Data (auto-generated slug) |
| `icon` | Attach Image |
| `image` | Attach Image |
| `short_description` | Small Text |
| `short_description_ar` | Small Text |
| `full_description` | Text Editor |
| `full_description_ar` | Text Editor |
| `display_order` | Int |
| `published` | Check (default 1) |

**Has web view**: Yes — generates `/service/<slug>`

#### [NEW] `Website Blog Post`

Frappe v16 dropped `Blog Post`/`Blog Category`/`Blogger` from core entirely (confirmed absent from both the `frappe` and `erpnext` app sources and the live site's DocType table), so the original "reuse core Blog Post" plan is void. Built as a normal `PC Website` module doctype instead:

| Field | Type |
|---|---|
| `title` / `title_ar` | Data (reqd) |
| `route` | Data |
| `blog_category` | Data |
| `website_tags` | Small Text |
| `cover_image` | Attach Image |
| `author_name` | Data |
| `author_image` | Attach Image |
| `published` | Check |
| `published_on` | Date |
| `blog_intro` / `blog_intro_ar` | Small Text |
| `content` / `content_ar` | Text Editor |

**Has web view**: Yes — generates `/blog/<route>` (Phase 4, same as the other content doctypes).
- **[NEW] `pestcontrol/templates/generators/website_blog_post.html`** and **`pestcontrol/templates/pages/blog.html`** in Phase 4, same as the other generators — no core template overrides needed since there's no core doctype to override.

#### [NEW] `Website Team Member`

| Field | Type |
|---|---|
| `member_name` | Data (reqd) |
| `route` | Data |
| `photo` | Attach Image |
| `designation` | Data |
| `designation_ar` | Data |
| `bio` | Text Editor |
| `bio_ar` | Text Editor |
| `phone` | Data |
| `email` | Data |
| `instagram_url` | Data |
| `facebook_url` | Data |
| `twitter_url` | Data |
| `display_order` | Int |
| `published` | Check |

**Has web view**: Yes — generates `/team/<slug>`

#### [NEW] `Website Project`

| Field | Type |
|---|---|
| `project_name` | Data (reqd) |
| `project_name_ar` | Data |
| `route` | Data |
| `image` | Attach Image |
| `category` | Select (Home Pest / Commercial / Eco-Friendly / Termite & Rodent / Outdoor) |
| `short_description` | Small Text |
| `short_description_ar` | Small Text |
| `full_description` | Text Editor |
| `full_description_ar` | Text Editor |
| `client_name` | Data |
| `location` | Data |
| `duration` | Data |
| `display_order` | Int |
| `published` | Check |

**Has web view**: Yes — generates `/project/<slug>`

#### [NEW] `Website Testimonial`

| Field | Type |
|---|---|
| `client_name` | Data (reqd) |
| `client_photo` | Attach Image |
| `designation` | Data |
| `designation_ar` | Data |
| `rating` | Rating |
| `testimonial_text` | Text |
| `testimonial_text_ar` | Text |
| `display_order` | Int |
| `published` | Check |

#### [NEW] `Website Pricing Plan`

| Field | Type |
|---|---|
| `plan_name` | Data (reqd) |
| `plan_name_ar` | Data |
| `price` | Currency |
| `billing_period` | Data |
| `is_featured` | Check |
| `cta_text` | Data |
| `cta_url` | Data |
| `display_order` | Int |
| `published` | Check |
| **Child table**: `Pricing Plan Feature` | |
| — `feature_text` | Data |
| — `feature_text_ar` | Data |
| — `is_included` | Check |

#### [NEW] `Website FAQ`

| Field | Type |
|---|---|
| `question` | Data (reqd) |
| `question_ar` | Data |
| `answer` | Text Editor |
| `answer_ar` | Text Editor |
| `faq_group` | Data (e.g., "General", "Services", "Pricing") |
| `display_order` | Int |
| `published` | Check |

#### [NEW] `Website Gallery Item`

| Field | Type |
|---|---|
| `title` | Data |
| `title_ar` | Data |
| `media_type` | Select (Image / Video) |
| `image` | Attach Image |
| `video_url` | Data |
| `category` | Data |
| `display_order` | Int |
| `published` | Check |

#### [NEW] `Website Contact Message`

| Field | Type |
|---|---|
| `full_name` | Data (reqd) |
| `email` | Data (reqd) |
| `phone` | Data |
| `subject` | Data |
| `message` | Text |
| `status` | Select (New / Read / Replied) |

*(Pending Q4 — this doctype only gets built if we don't route submissions to CRM `Lead` instead.)*

#### [NEW] Workspace Sidebar: `PC Website`
Groups all CMS doctypes in one sidebar for easy admin access.

---

### Phase 3 — Make Templates Dynamic

#### [MODIFY] All `www/index.py` controllers
Replace the copy-pasted boilerplate with actual data queries, selecting the right language field based on request language:

```python
# Example: www/services/index.py
import frappe

no_cache = 1

def get_context(context):
    context.no_cache = 1
    context.lang = frappe.local.lang
    context.services = frappe.get_all(
        "Website Service",
        filters={"published": 1},
        fields=["*"],
        order_by="display_order asc"
    )
    context.settings = frappe.get_cached_doc("PC Website Settings")
    context.page_title = "Our Services"
```

#### [MODIFY] All `www/*.html` templates
Replace hardcoded content with Jinja loops and variables, picking the Arabic field when `lang == "ar"`:

```html
{% for service in services %}
<div class="col-lg-4 col-md-6">
    <div class="service-item wow fadeInUp" data-wow-delay="{{ loop.index0 * 0.2 }}s">
        <div class="service-image">
            <a href="/service/{{ service.route }}">
                <figure class="image-anime">
                    <img src="{{ service.image }}" alt="{{ service.service_name }}">
                </figure>
            </a>
        </div>
        <div class="service-body">
            <div class="icon-box">
                <img src="{{ service.icon }}" alt="">
            </div>
            <div class="service-content">
                <h3><a href="/service/{{ service.route }}">{{ service.service_name_ar if lang == "ar" and service.service_name_ar else service.service_name }}</a></h3>
                <p>{{ service.short_description_ar if lang == "ar" and service.short_description_ar else service.short_description }}</p>
            </div>
        </div>
    </div>
</div>
{% endfor %}
```

#### [MODIFY] Shared includes
Update header/footer includes to read from `PC Website Settings`:
```html
<!-- website_topbar.html -->
<li><a href="mailto:{{ settings.email }}">{{ settings.email }}</a></li>
<li>{{ settings.address_ar if lang == "ar" and settings.address_ar else settings.address }}</li>
```

---

### Phase 4 — Website Generators & Contact Form

#### [NEW] Generator templates
For DocTypes with `has_web_view = 1`, create Jinja templates in `templates/generators/`:

| Template | Route Pattern | Data Source |
|---|---|---|
| `website_service.html` | `/service/<slug>` | Website Service |
| `website_blog_post.html` | `/blog/<slug>` | Website Blog Post |
| `website_team_member.html` | `/team/<slug>` | Website Team Member |
| `website_project.html` | `/project/<slug>` | Website Project |

These replace the current static `service-single/`, `blog-single/`, etc. pages.

#### [MODIFY] [hooks.py](file:///d:/skyStar/template/pestcontrol-develop/pestcontrol/hooks.py)
```python
website_generators = ["Website Service", "Website Blog Post", "Website Team Member", "Website Project"]
```

#### [NEW] Contact form API endpoint
Pending Q4 — target doctype TBD (`Website Contact Message` vs. CRM `Lead`):
```python
@frappe.whitelist(allow_guest=True)
def submit_contact_form(full_name, email, phone, subject, message):
    doc = frappe.get_doc({
        "doctype": "Website Contact Message",  # or "Lead", pending Q4
        "full_name": full_name,
        "email": email,
        "phone": phone,
        "subject": subject,
        "message": message
    })
    doc.insert(ignore_permissions=True)
    return {"success": True}
```

#### [DELETE] Static detail pages
Remove after generators are working:
- `www/service-single/`
- `www/blog-single/`
- `www/project-single/`
- `www/team-single/`

---

### Phase 5 — Seed Data & Polish

#### [NEW] Fixtures for website content
Seed the CMS DocTypes with the content currently hardcoded in the HTML files, so the website looks identical after the migration. Seed both English and Arabic fields where Arabic copy is available; leave `_ar` fields blank otherwise (templates fall back to English when `_ar` is empty).

#### ~~[MODIFY] pyproject.toml~~
Superseded — commit `1bc5749` intentionally moved the whole repo (`pyproject.toml`, CI workflows) to `>=3.14`/`py314`. No action needed.

---

## Resolved Questions

> [!NOTE]
> **Q4: Contact form target** — Resolved: **`Website Contact Message`** (simple, standalone DocType), built in Phase 2. Not routed to CRM `Lead`.

---

## Verification Plan

### Manual Verification
1. After Phase 1: Verify all 16 pages still render identically after extracting includes; verify `dir="rtl"` applies correctly when Arabic is selected
2. After Phase 2: Verify all CMS DocTypes are accessible in the desk, create test records including `_ar` fields
3. After Phase 3: Edit a service in the desk (English and Arabic) → verify it appears correctly on `/services` in both languages
4. After Phase 4: Create a new blog post → verify `/blog/<slug>` generates and renders correctly using the overridden template
5. After Phase 5: Compare website visually with the original HTML template — should be pixel-identical in English; RTL layout verified for Arabic

### Automated Tests
```bash
bench --site test_site run-tests --app pestcontrol --module pestcontrol.pc_website
```
- Controllers return correct context with published items only
- Unpublished items excluded from listings
- Arabic fallback to English when `_ar` field is empty
- Contact form creates document
- Website generators produce correct routes
