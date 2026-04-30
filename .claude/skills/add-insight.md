---
name: add-insight
description: Capture a new insight into the DevelopmentGuide system. Accepts a URL, pasted text, local file path, PDF, or verbal description. Creates a raw insight file and drafts a structured rule for review.
---

# add-insight

Capture an insight into `insights/` and draft a corresponding rule in `rules/`.

## Step 1 — Identify input type

Examine what the user provided:
- **URL**: a link to a web page, GitHub repo, YouTube video, or social post
- **Local file path**: an absolute or relative path to a file on disk (`.md`, `.txt`, `.pdf`, code files, etc.)
- **PDF**: a path to a PDF file (may be the same as a local file path — detected by `.pdf` extension)
- **Pasted text**: raw content copied from an article, post, or document
- **Verbal**: the user described something in their own words

## Step 2 — Fetch content (URL and local files)

**For URLs** — use WebFetch based on the domain:

| Domain | Fetch strategy |
|--------|---------------|
| `github.com` | Fetch the repo root URL; extract README content. If a CLAUDE.md or docs/ directory is mentioned, fetch those too. |
| `youtube.com` / `youtu.be` | Fetch the page; extract video title, description, and any auto-transcript content visible in the page source. |
| `linkedin.com`, `twitter.com`, `x.com` | Fetch the URL. Note: these platforms often restrict unauthenticated content — save whatever is available and note the limitation in the insight file. |
| `reddit.com` | Fetch the post page; extract post body and visible top-level comments. |
| All other URLs | Standard WebFetch of the page content. |

**For local files** — use the Read tool:

| File type | Read strategy |
|-----------|--------------|
| `.pdf` | Use Read with the `pages` parameter if large (>10 pages). Extract key sections — skip front matter, tables of contents, and indexes unless they contain substance. |
| `.md`, `.txt` | Read the full file. |
| Code files (`.py`, `.ts`, `.go`, etc.) | Read the file; focus on comments, docstrings, and structural patterns rather than implementation details. |
| Large files (>500 lines) | Read in relevant sections — ask the user which part contains the insight if unclear. |

## Step 3 — Determine source_project

Ask the user which project this insight is associated with, OR infer it from the current working directory if obvious. If none applies, use `"none"`.

## Step 4 — Create the insight file

File path: `insights/YYYY-MM-DD-{slug}.md`

- `YYYY-MM-DD`: today's date
- `{slug}`: 2–5 word kebab-case summary of the topic

Frontmatter:
```yaml
---
date: YYYY-MM-DD
source: <URL | "paste" | "verbal">
source_type: <web | github | youtube | social-linkedin | social-twitter | social-reddit | pdf | local-file | paste | verbal>
source_project: <project name or "none">
status: raw
tags: []
---
```

Body: the raw content — full text, fetched page content, or the user's verbal description written out clearly.

## Step 5 — Draft the rule file

File path: `rules/{slug}.md`

Use the same slug as the insight file.

Frontmatter:
```yaml
---
name: {slug}
applies_when: []
promotes_to: CLAUDE.md
source_insight: insights/YYYY-MM-DD-{slug}.md
source_project: <project name or "none">
---
```

Body: distill the insight into a concise, actionable rule. One short paragraph. Write it as a direct instruction (e.g. "When X, do Y. Reason: Z.").

If `applies_when` is not clear from the content, leave it as `[]` and flag it in your report.

## Step 6 — Report

Tell the user:
- Paths of both files created
- Any frontmatter fields left blank that need human review (especially `applies_when` and `tags`)
- Any fetch limitations encountered (e.g. auth wall on social platforms)
