---
name: add-insight
description: Capture a new insight into the DevelopmentGuide system. Accepts one or more sources (URLs, pasted text, local files, PDFs, or verbal descriptions). Creates a raw insight file and drafts one rule file per distinct actionable rule found.
---

# add-insight

Capture an insight into `insights/` and draft one rule file per distinct actionable rule found in the content.

## Step 1 — Identify all sources

The user may provide one or more sources in a single invocation. Collect all of them before fetching anything.

Each source is one of:
- **URL**: a web page, GitHub repo, YouTube video, or social post
- **Local file path**: an absolute or relative path to a file on disk (`.md`, `.txt`, `.pdf`, code files, etc.)
- **Pasted text**: raw content copied from an article, post, or document
- **Verbal**: the user described something in their own words

If multiple sources are provided, they are treated as co-sources of a single insight — all fetched and combined into one insight file.

## Step 2 — Fetch all sources

Fetch every source before proceeding. For each:

**URLs** — use WebFetch based on the domain:

| Domain | Fetch strategy |
|--------|---------------|
| `github.com` | Fetch the repo root URL; extract README content. If a CLAUDE.md or docs/ directory is mentioned, fetch those too. |
| `youtube.com` / `youtu.be` | Fetch the page; extract video title, description, and any auto-transcript content visible in the page source. |
| `linkedin.com`, `twitter.com`, `x.com` | Fetch the URL. Note: these platforms often restrict unauthenticated content — save whatever is available and note the limitation in the insight file. |
| `reddit.com` | Fetch the post page; extract post body and visible top-level comments. |
| All other URLs | Standard WebFetch of the page content. |

**Local files** — use the Read tool:

| File type | Read strategy |
|-----------|--------------|
| `.pdf` | Use Read with the `pages` parameter if large (>10 pages). Extract key sections — skip front matter, tables of contents, and indexes unless they contain substance. |
| `.md`, `.txt` | Read the full file. |
| Code files (`.py`, `.ts`, `.go`, etc.) | Read the file; focus on comments, docstrings, and structural patterns rather than implementation details. |
| Large files (>500 lines) | Read in relevant sections — ask the user which part contains the insight if unclear. |

## Step 3 — Determine source_project

Ask the user which project this insight is associated with, OR infer it from the current working directory if obvious. If none applies, use `"none"`.

## Step 4 — Create the insight file

One insight file covers all co-sources.

File path: `insights/YYYY-MM-DD-{slug}.md`

- `YYYY-MM-DD`: today's date
- `{slug}`: 2–5 word kebab-case summary of the overall topic

Frontmatter:
```yaml
---
date: YYYY-MM-DD
sources:
  - url: <URL | "paste" | "verbal">
    type: <web | github | youtube | social-linkedin | social-twitter | social-reddit | pdf | local-file | paste | verbal>
source_project: <project name or "none">
status: raw
tags: []
---
```

For a single source, `sources` is still a list with one entry. For multiple co-sources, list each with its own `url` and `type`.

Body: the combined content from all sources — clearly labeled per source if multiple. Note any fetch limitations (e.g. auth wall on YouTube).

## Step 5 — Identify distinct rules

Before drafting, analyze the combined insight content and identify every distinct actionable rule it contains. A distinct rule is one that:
- Addresses a different behavior, workflow, or decision pattern
- Could stand alone without the others
- Would have a different `applies_when` profile than its siblings

There may be one rule or several. Do not force everything into one rule — capture the true granularity of the insight.

List the rules you intend to draft and their proposed slugs before writing files. If a rule is unclear, note it.

## Step 6 — Draft one rule file per distinct rule

For each rule identified in Step 5, create a separate file.

File path: `rules/{descriptive-slug}.md`

Use a descriptive slug specific to that rule — not the insight slug. If two rules come from the same insight, they get different, meaningful names (e.g. `codex-rescue-subagent.md` and `codex-adversarial-review.md`).

Frontmatter:
```yaml
---
name: {descriptive-slug}
applies_when: []
promotes_to: CLAUDE.md
source_insight: insights/YYYY-MM-DD-{insight-slug}.md
source_project: <project name or "none">
---
```

Body: one short paragraph. Direct instruction ("When X, do Y. Reason: Z."). Under 100 words.

If `applies_when` is not clear from the content, leave it as `[]` and flag it in the report.

## Step 7 — Update index

Invoke `/update-index` to rebuild `rules/index.md`. New rules will be excluded until refined, but this keeps the index consistent.

## Step 8 — Report

Tell the user:
- Path of the insight file created and how many sources it captured
- List of all rule files drafted with a one-line summary of each
- Any frontmatter fields left blank that need human review (especially `applies_when` and `tags`)
- Any fetch limitations encountered (e.g. auth wall on social platforms)
