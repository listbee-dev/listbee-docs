# Fern Docs Improvements

Spec for 5 improvements to listbee-docs, inspired by agentmail-docs patterns.

## 1. AI Search

Add AI-powered search to docs with a custom system prompt scoped to ListBee content.

**Config addition** (top-level in `docs.yml`):

```yaml
ai-search:
  location: docs
  system-prompt: |
    You are the ListBee documentation assistant. Answer questions using only
    the ListBee documentation. ListBee is agent-native commerce infrastructure —
    one API call to sell and deliver digital content. Your audience includes
    both human developers and AI agent builders (MCP, n8n, Python SDK).
    If the answer isn't in the docs, say so and point to the relevant resource:
    API reference, console (console.listbee.so), or support (damian@listbee.so).
```

## 2. Default Language

Set Python as the default code snippet language.

**Config addition** (top-level in `docs.yml`):

```yaml
default-language: python
```

## 3. Changelog Format Upgrade

Convert the changelog from bare `.md` files to structured `.mdx` with tags, a template, and an overview page.

### Tag taxonomy

- **Area:** `api`, `console`, `checkout`, `webhooks`, `mcp`, `sdk`, `n8n`, `docs`
- **Type:** `new-feature`, `improvement`, `breaking-change`, `fix`, `deprecation`

### Files to create/modify

**`fern/docs/changelog/overview.mdx`** (landing page):

```mdx
# ListBee Changelog

Latest API and SDK updates. [Subscribe via RSS](https://docs.listbee.so/changelog.rss)
```

**`fern/docs/changelog/TEMPLATE.mdx`** (not rendered, reference only):

```mdx
---
tags: ["area-tag", "type-tag"]
---

# Title

Summary (2-3 sentences, benefit-focused).

## What's new

- `METHOD /path` — description

## Breaking changes

Migration steps with code examples using `<CodeBlocks>`.
```

**`fern/docs/changelog/2026-03-29.mdx`** (convert existing entry):

Rename from `.md` to `.mdx`. Add tags `["api", "new-feature"]` to frontmatter. Keep existing content unchanged.

## 4. GitHub Actions Workflows

Create `.github/workflows/` with 4 workflow files. No `.github/` directory exists yet.

### 4a. `check.yml` — Fern validation

- **Triggers:** `pull_request` + `push` to `main`
- **Steps:** checkout, install fern, run `fern check`
- **Purpose:** block merges on invalid API definitions

### 4b. `preview-docs.yml` — Preview URL on PRs

- **Triggers:** `pull_request`
- **Steps:** checkout, install fern, `fern generate --docs --preview`, comment URL on PR
- **Secrets needed:** `FERN_TOKEN`
- **Purpose:** reviewers can see rendered docs before merge

### 4c. `api-changelog.yml` — API change detection

- **Triggers:** `pull_request` when `fern/openapi/**` changes
- **Steps:** checkout with full history, run `oasdiff` comparing base vs head `openapi.json`, comment diff on PR, upload artifact
- **Adaptation:** agentmail triggers on `fern/definition/**/*.yml` and uses `fern export` to generate specs. We trigger on `fern/openapi/**` and diff the JSON directly since we use OpenAPI as source of truth.
- **Purpose:** surface API changes (especially breaking) in PR review

### 4d. `update-last-updated.yml` — Auto-update frontmatter dates

- **Triggers:** `pull_request` (opened, synchronize) against `main`
- **Steps:** checkout PR branch, detect changed `.mdx` files, update/add `last-updated` frontmatter with current date, commit back to PR
- **Date format:** `"Month Day, Year"` (e.g. "March 30, 2026")
- **Purpose:** keep "last updated" dates accurate without manual effort

## Scope boundaries

- No custom CSS or JS
- No Knowledge Base tab (not enough content yet)
- No redirects (no URL migrations needed)
- No SDK generation workflows (we hand-craft SDKs)
- Changelog content stays as-is — only format/structure changes

## Files changed

| File | Action |
|------|--------|
| `fern/docs.yml` | Edit: add `ai-search`, `default-language` |
| `fern/docs/changelog/2026-03-29.md` | Delete (replaced by .mdx) |
| `fern/docs/changelog/2026-03-29.mdx` | Create: converted entry with tags |
| `fern/docs/changelog/overview.mdx` | Create: landing page |
| `fern/docs/changelog/TEMPLATE.mdx` | Create: reference template |
| `.github/workflows/check.yml` | Create |
| `.github/workflows/preview-docs.yml` | Create |
| `.github/workflows/api-changelog.yml` | Create |
| `.github/workflows/update-last-updated.yml` | Create |
