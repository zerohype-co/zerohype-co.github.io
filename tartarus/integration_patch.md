# Tartarus integration patch (zerohype-co/guides)

This document describes how to wire the Tartarus page into the existing
zerohypelab.com site. Do not run a `git push` from this session: the target
repositories use a different auth context. Apply these edits in a separate
commit.

---

## 1. Serving path and existing files

The page currently lives at:

- **Files:** `tartarus/index.html`, `tartarus/index.md`
- **Served at:** `https://zerohypelab.com/tartarus/`
- **Markdown twin:** `https://zerohypelab.com/tartarus/index.md` (the site
  serves `/tartarus/index.md`, matching the `/product/index.md` convention used
  by the eleven existing product pages)

The page is fully self-contained: inline CSS, inline JS, no backend, no
client-side dependencies. It reuses the site's self-hosted fonts at `/fonts/`
and the site favicon.

---

## 2. Insert into `/sitemap.xml`

Add the following `<url>` block. Place it in the "Free tools" group (after
`/bullshit-detector/` or near the other free tools) so it groups with the rest
of the diagnostics.

```xml
  <!-- Free tools -->
  <url>
    <loc>https://zerohypelab.com/tartarus/</loc>
    <lastmod>2026-08-15</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
```

---

## 3. Insert into `/llms.txt`

The file uses heading `## Free Tools` for the free diagnostic tools. Add a
dedicated `## Tools` section (this is the convention requested for Tartarus)
after the free tools block and before the `## Full document` section:

```markdown
## Tools

### Tartarus
**URL:** https://zerohypelab.com/tartarus/
Prompt: codebase diagnostic. Paste a GitHub repo URL, pick a tech stack, get a
Context Readiness Score 0-100 across code structure, dependency clarity,
documentation coverage, and AI-readiness. Heuristic scan, not a full audit.
Built on top of GRAFT, the open-source MIT-licensed context graph engine.
Free. No backend. The repo URL is not stored.
```

Note: choose this heading literally (`## Tools`) per spec, even though the
existing file names its free group `## Free Tools`. If you prefer strict
consistency with the rest of the file, you may instead add a `### Tartarus`
entry under the existing `## Free Tools` list with the same body.

---

## 4. Insert into `/llms-full.txt`

Identical content to llms.txt, in the corresponding "Free Tools / Tools"
region (the full file keeps `## Free Tools` at the top of the body). Insert
the same `## Tools` section (or the `### Tartarus` entry) there.

---

## 5. Make the page reachable from the parent site

The primary nav (`index.html`) exposes: Manifesto, Method, Guides, Substack
Newsletter. Free tools are not in the primary nav today. Two options, in order
of preference:

### Option A (recommended): add a footer link

Add one small link to the footer of `index.html`. The footer already links
pages and tools; append:

```html
<li><a href="https://zerohypelab.com/tartarus/">Tartarus</a></li>
```

Low friction, does not crowd the primary nav, and matches how utility pages
are surfaced. Works well with section 2 so search engines and LLM crawlers
both find it.

### Option B: add a "Tools" or "Diagnostics" link to the primary nav

Add a link in `index.html` `<ul class="nav-links">`. If a single tool is not
enough, introduce a `/tools/` or `/diagnostics/` hub later and link that. For
now a single primary-nav item labeled `Tools` pointing to Tartarus is the
lightest option:

```html
<li><a href="https://zerohypelab.com/tartarus/">Tools</a></li>
```

### Option C: rely on the `/scores/` leaderboard pattern

The `/scores/` page is its own dedicated page reachable from the sitemap and
llms.txt rather than the primary nav. Tartarus already follows that pattern
(own repo folder, own markdown twin, sitemap entry, llms.txt entry). If you
prefer not to touch the nav at all, this is the path that requires zero
changes to existing pages. Recommend pairing it with Option A when time allows.

Recommendation: use **Option A** now (footer link plus sitemap plus llms.txt)
and revisit **Option B** when there are two or more free tools to justify a
`/tools/` hub.

---

## 6. Not in scope (do not run here)

- Do **not** push to `github.com/zerohype-co/guides` from this session.
- Do **not** touch the Stripe placeholder URL
  (`https://buy.stripe.com/placeholder_tartarus`) until real checkout is
  wired. The page already labels it "integration coming soon".
- Contact for the page: `zerohype@proton.me`. ZeroHype Lab is an anonymous
  brand; no real-name identities appear anywhere in the page or this patch.
