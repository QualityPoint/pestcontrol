#!/usr/bin/env bash
# Verify the SEO work against a running site.
#   ./verify_seo.sh http://127.0.0.1:8001
BASE="${1:-http://127.0.0.1:8001}"
LANG_DEFAULT="${LANG_DEFAULT:-ar}"
SLUGS="/ /about /services /projects /team /pricing /testimonials /faqs /blog /pest-library /image-gallery /video-gallery /branches /careers /contact"
PAGES=""; for s in $SLUGS; do PAGES="$PAGES /$LANG_DEFAULT${s%/}"; done
pass=0; fail=0
ok(){ printf '  \033[32mPASS\033[0m %s\n' "$1"; pass=$((pass+1)); }
no(){ printf '  \033[31mFAIL\033[0m %s\n' "$1"; fail=$((fail+1)); }

echo "== 1. every page has title, description, canonical, exactly one h1 =="
for p in $PAGES; do
  h=$(curl -fsS "$BASE$p") || { no "$p unreachable"; continue; }
  t=$(sed -n 's:.*<title>\(.*\)</title>.*:\1:p' <<<"$(tr -d '\n' <<<"$h")")
  d=$(grep -o '<meta name="description" content="[^"]*"' <<<"$h" | head -1)
  c=$(grep -o '<link rel="canonical" href="[^"]*"' <<<"$h" | head -1)
  n=$(grep -o '<h1' <<<"$h" | wc -l)
  [ -n "$t" ] && [ -n "$d" ] && [ -n "$c" ] && [ "$n" -eq 1 ] \
    && ok "$p  h1=$n  $t" || no "$p  title='$t' desc=${d:+y} canon=${c:+y} h1=$n"
done

echo "== 2. titles are unique (duplicates are an SEO problem) =="
dupes=$(for p in $PAGES; do curl -fsS "$BASE$p" | tr -d '\n' | sed -n 's:.*<title>\(.*\)</title>.*:\1:p'; done | sort | uniq -d)
[ -z "$dupes" ] && ok "no duplicate titles" || no "duplicates: $dupes"

echo "== 3. each language has its own URL =="
en=$(curl -fsS "$BASE/en/about" | tr -d '\n' | sed -n 's:.*<title>\(.*\)</title>.*:\1:p')
ar=$(curl -fsS "$BASE/ar/about" | tr -d '\n' | sed -n 's:.*<title>\(.*\)</title>.*:\1:p')
[ "$en" != "$ar" ] && ok "en='$en'  ar='$ar'" || no "identical in both languages: $en"
curl -fsS "$BASE/ar/about" | grep -q '<html lang="ar" dir="rtl"' && ok 'ar renders dir="rtl"' || no 'missing dir="rtl"'

echo "== 3b. redirects, and paths that must NOT redirect =="
for pair in "/:/$LANG_DEFAULT/" "/about:/$LANG_DEFAULT/about" "/about?_lang=en:/en/about"; do
  src="${pair%%:*}"; want="${pair##*:}"
  got=$(curl -s -o /dev/null -w '%{redirect_url}' "$BASE$src")
  [ "$got" = "$BASE$want" ] && ok "$src -> $want" || no "$src -> ${got:-nothing} (wanted $want)"
done
for p in /api/method/ping /assets/pestcontrol/website/css/custom.css /sitemap.xml /robots.txt; do
  code=$(curl -s -o /dev/null -w '%{http_code}' "$BASE$p")
  [ "$code" = "200" ] && ok "$p not redirected ($code)" || no "$p returned $code"
done
curl -sL -o /dev/null -w '%{http_code}' "$BASE/app" | grep -q 200 && ok "/app still serves the desk" || no "/app BROKEN"

echo "== 3c. hreflang is reciprocal =="
for u in /ar/about /en/about; do
  tags=$(curl -fsS "$BASE$u" | grep -oE 'hreflang="[^"]*"' | sed 's/hreflang=//;s/"//g' | sort -u | tr '\n' ' ')
  [ "$tags" = "ar en x-default " ] && ok "$u alternates: $tags" || no "$u alternates: ${tags:-none}"
done

echo "== 4. social tags present =="
h=$(curl -fsS "$BASE/$LANG_DEFAULT/about")
for tag in 'og:title' 'og:description' 'og:url' 'og:site_name' 'og:locale' 'twitter:title' 'twitter:card'; do
  grep -q "$tag" <<<"$h" && ok "$tag" || no "$tag missing"
done

echo "== 5. keywords gone, robots present =="
grep -q 'name="keywords"' <<<"$h" && no 'stale <meta name="keywords"> still there' || ok 'no keywords tag'
grep -q 'name="robots" content="index, follow' <<<"$h" && ok 'robots index,follow' || no 'robots tag missing'
curl -fsS "$BASE/$LANG_DEFAULT/404" | grep -q 'noindex' && ok '/404 is noindex' || no '/404 not noindex'

echo "== 6. sitemap =="
s=$(curl -fsS "$BASE/sitemap.xml")
python3 -c "import sys,xml.dom.minidom as m; m.parseString(sys.stdin.read())" <<<"$s" 2>/dev/null \
  && ok "valid XML, $(grep -c '<loc>' <<<"$s") urls" || no "sitemap malformed"
grep -q "<loc>$BASE/$LANG_DEFAULT/</loc>" <<<"$s" && ok "home listed as /$LANG_DEFAULT/ (not /home)" || no "home not canonicalised"
grep -q 'xhtml:link rel="alternate"' <<<"$s" && ok "sitemap carries hreflang alternates" || no "sitemap has no alternates"
grep -q '/404\|/account/' <<<"$s" && no "private pages leaked into sitemap" || ok "404 + account excluded"

echo
echo "  passed: $pass   failed: $fail"
[ "$fail" -eq 0 ]
