# Fern Docs Improvements Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add AI search, default language, changelog format upgrade, and 4 GitHub Actions workflows to listbee-docs.

**Architecture:** All changes are configuration and static files — no application code. docs.yml gets two new top-level keys, changelog gets restructured from .md to .mdx with tags/template/overview, and .github/workflows/ gets 4 new workflow files.

**Tech Stack:** Fern docs (YAML config, MDX), GitHub Actions (YAML workflows), oasdiff

---

## File Structure

| File | Action | Responsibility |
|------|--------|---------------|
| `fern/docs.yml` | Modify | Add `ai-search` and `default-language` config |
| `fern/docs/changelog/2026-03-29.md` | Delete | Replaced by .mdx version |
| `fern/docs/changelog/2026-03-29.mdx` | Create | Converted changelog entry with tags |
| `fern/docs/changelog/overview.mdx` | Create | Changelog landing page with RSS link |
| `fern/docs/changelog/TEMPLATE.mdx` | Create | Reference template for future entries |
| `.github/workflows/check.yml` | Create | Fern validation on PR/push |
| `.github/workflows/preview-docs.yml` | Create | Preview URL generation on PRs |
| `.github/workflows/api-changelog.yml` | Create | API change detection on PRs |
| `.github/workflows/update-last-updated.yml` | Create | Auto-update frontmatter dates on PRs |

---

### Task 1: Add AI search and default language to docs.yml

**Files:**
- Modify: `fern/docs.yml` (lines 1-5, top-level config area)

- [ ] **Step 1: Add `ai-search` block after the `colors` section**

In `fern/docs.yml`, add the following block after the `colors` section (after line 12) and before `navbar-links`:

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

default-language: python
```

The file should read (top section):

```yaml
instances:
  - url: listbee-docs.docs.buildwithfern.com
    custom-domain: docs.listbee.so

title: ListBee
logo:
  light: ./docs/assets/logo-light.svg
  dark: ./docs/assets/logo-dark.svg

colors:
  accent-primary: "#F59E0B"
  background: "#FFFFFF"

ai-search:
  location: docs
  system-prompt: |
    You are the ListBee documentation assistant. Answer questions using only
    the ListBee documentation. ListBee is agent-native commerce infrastructure —
    one API call to sell and deliver digital content. Your audience includes
    both human developers and AI agent builders (MCP, n8n, Python SDK).
    If the answer isn't in the docs, say so and point to the relevant resource:
    API reference, console (console.listbee.so), or support (damian@listbee.so).

default-language: python

navbar-links:
  - type: primary
    text: Get API Key
    url: https://console.listbee.so
```

- [ ] **Step 2: Validate with fern check**

Run: `cd /Users/damjan/development/listbee-dev/listbee-docs && npx fern check`
Expected: passes with no errors (warnings about unused types are OK)

- [ ] **Step 3: Commit**

```bash
cd /Users/damjan/development/listbee-dev/listbee-docs
git add fern/docs.yml
git commit -m "feat: add AI search and default language to docs config"
```

---

### Task 2: Upgrade changelog format

**Files:**
- Delete: `fern/docs/changelog/2026-03-29.md`
- Create: `fern/docs/changelog/2026-03-29.mdx`
- Create: `fern/docs/changelog/overview.mdx`
- Create: `fern/docs/changelog/TEMPLATE.mdx`

- [ ] **Step 1: Create overview.mdx**

Create `fern/docs/changelog/overview.mdx`:

```mdx
# ListBee Changelog

Latest API and SDK updates. [Subscribe via RSS](https://docs.listbee.so/changelog.rss)
```

- [ ] **Step 2: Create TEMPLATE.mdx**

Create `fern/docs/changelog/TEMPLATE.mdx`:

```mdx
---
tags: ["area-tag", "type-tag"]
---

# Title

Summary (2-3 sentences, benefit-focused).

## What's new

- `METHOD /path` — description

## Breaking changes

Migration steps with code examples.
```

- [ ] **Step 3: Convert existing changelog entry to .mdx with tags**

Create `fern/docs/changelog/2026-03-29.mdx` with the content from the existing `.md` file, adding tags:

```mdx
---
title: "Agent-native infrastructure"
date: 2026-03-29
tags: ["api", "new-feature"]
---

## New endpoints

- `POST /v1/account/signup` + `POST /v1/account/verify` — agent-initiated account creation with email OTP
- `GET/POST/DELETE /v1/api-keys` — API key management
- `PUT /v1/listings/{slug}` — listing updates (content immutable)
- `POST /v1/account/stripe-key` — direct Stripe key input
- `POST /v1/account/stripe/connect` — Stripe Connect via API
- `DELETE /v1/account/stripe` — disconnect Stripe

## Readiness evolution

- `blockers` → `actions` with `kind` (api/human) and `next` pointer
- Agents now know what to call and whether they can do it autonomously

## Agent discovery

- `/llms.txt` endpoint for agent discovery
- `Idempotency-Key` header on all POST endpoints
```

- [ ] **Step 4: Delete the old .md file**

```bash
cd /Users/damjan/development/listbee-dev/listbee-docs
rm fern/docs/changelog/2026-03-29.md
```

- [ ] **Step 5: Validate with fern check**

Run: `cd /Users/damjan/development/listbee-dev/listbee-docs && npx fern check`
Expected: passes with no errors

- [ ] **Step 6: Commit**

```bash
cd /Users/damjan/development/listbee-dev/listbee-docs
git add fern/docs/changelog/
git commit -m "feat: upgrade changelog to mdx with tags, template, and overview"
```

---

### Task 3: Add Fern check workflow

**Files:**
- Create: `.github/workflows/check.yml`

- [ ] **Step 1: Create the workflow file**

Create `.github/workflows/check.yml`:

```yaml
name: Fern Check

on:
  pull_request:
  push:
    branches:
      - main

jobs:
  fern-check:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Install Fern
        run: npm install -g fern-api

      - name: Check API is valid
        run: fern check
```

- [ ] **Step 2: Commit**

```bash
cd /Users/damjan/development/listbee-dev/listbee-docs
git add .github/workflows/check.yml
git commit -m "ci: add Fern validation workflow"
```

---

### Task 4: Add preview docs workflow

**Files:**
- Create: `.github/workflows/preview-docs.yml`

- [ ] **Step 1: Create the workflow file**

Create `.github/workflows/preview-docs.yml`:

```yaml
name: Preview Docs

on: pull_request

jobs:
  preview:
    runs-on: ubuntu-latest
    permissions: write-all
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Install Fern
        run: npm install -g fern-api

      - name: Generate preview URL
        id: generate-docs
        env:
          FERN_TOKEN: ${{ secrets.FERN_TOKEN }}
        run: |
          OUTPUT=$(fern generate --docs --preview --log-level debug 2>&1) || true
          echo "$OUTPUT"
          URL=$(echo "$OUTPUT" | grep -oP 'Published docs to \K.*(?= \()')
          echo "Preview URL: $URL"
          echo "preview_url=$URL" >> $GITHUB_OUTPUT

      - name: Comment URL in PR
        uses: actions/github-script@v7
        with:
          script: |
            const url = '${{ steps.generate-docs.outputs.preview_url }}';
            if (url) {
              await github.rest.issues.createComment({
                issue_number: context.issue.number,
                owner: context.repo.owner,
                repo: context.repo.repo,
                body: `🌿 Preview your docs: ${url}`
              });
            }
```

Note: This workflow requires a `FERN_TOKEN` secret to be configured in the repository settings. The implementer should remind the user to add this secret.

- [ ] **Step 2: Commit**

```bash
cd /Users/damjan/development/listbee-dev/listbee-docs
git add .github/workflows/preview-docs.yml
git commit -m "ci: add docs preview URL workflow for PRs"
```

---

### Task 5: Add API changelog automation workflow

**Files:**
- Create: `.github/workflows/api-changelog.yml`

- [ ] **Step 1: Create the workflow file**

Create `.github/workflows/api-changelog.yml`:

```yaml
name: API Changelog Automation

on:
  pull_request:
    paths:
      - 'fern/openapi/**'
  workflow_dispatch:

jobs:
  generate-diff:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write

    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Get base OpenAPI spec
        run: |
          git show ${{ github.event.pull_request.base.sha }}:fern/openapi/openapi.json > base-openapi.json || echo '{}' > base-openapi.json

      - name: Copy current OpenAPI spec
        run: |
          cp fern/openapi/openapi.json current-openapi.json

      - name: Run oasdiff changelog
        id: oasdiff
        uses: oasdiff/oasdiff-action/changelog@main
        with:
          base: base-openapi.json
          revision: current-openapi.json
          format: markdown
          fail-on-diff: false
        continue-on-error: true

      - name: Check if changes detected
        id: check_changes
        env:
          CHANGELOG: ${{ steps.oasdiff.outputs.changelog }}
          BREAKING: ${{ steps.oasdiff.outputs.breaking }}
        run: |
          if [ -n "$CHANGELOG" ]; then
            echo "has_changes=true" >> $GITHUB_OUTPUT
            echo "breaking_count=${BREAKING:-0}" >> $GITHUB_OUTPUT
          else
            echo "has_changes=false" >> $GITHUB_OUTPUT
            echo "breaking_count=0" >> $GITHUB_OUTPUT
          fi

      - name: Upload changelog diff artifact
        if: steps.check_changes.outputs.has_changes == 'true'
        env:
          CHANGELOG_DIFF: ${{ steps.oasdiff.outputs.changelog }}
        run: |
          node -e "require('fs').writeFileSync('changelog-diff.md', process.env.CHANGELOG_DIFF || '')"

      - name: Upload artifact
        if: steps.check_changes.outputs.has_changes == 'true'
        uses: actions/upload-artifact@v4
        with:
          name: api-changelog-diff
          path: changelog-diff.md
          retention-days: 7

      - name: Comment on PR with diff
        if: steps.check_changes.outputs.has_changes == 'true' && github.event_name == 'pull_request'
        env:
          CHANGELOG_DIFF: ${{ steps.oasdiff.outputs.changelog }}
          BREAKING_COUNT: ${{ steps.check_changes.outputs.breaking_count || 0 }}
        uses: actions/github-script@v7
        with:
          script: |
            const diff = process.env.CHANGELOG_DIFF || '';
            const breaking = (Number(process.env.BREAKING_COUNT) || 0) > 0;
            const safeDiff = diff.replace(/\`\`\`/g, '\\`\\`\\`');
            const body = [
              `## ${breaking ? '🚨 Breaking' : '✨'} API Changes`,
              '',
              '```markdown',
              safeDiff,
              '```',
              '',
              '💡 Download `api-changelog-diff` artifact for the full diff.'
            ].join('\n');
            await github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body
            });
```

Key adaptation from agentmail: We use `git show` to extract the base OpenAPI spec from the PR base commit, rather than checking out the base and running `fern export`. This is simpler because we store the OpenAPI spec directly as JSON.

- [ ] **Step 2: Commit**

```bash
cd /Users/damjan/development/listbee-dev/listbee-docs
git add .github/workflows/api-changelog.yml
git commit -m "ci: add API changelog automation for PRs"
```

---

### Task 6: Add update-last-updated workflow

**Files:**
- Create: `.github/workflows/update-last-updated.yml`

- [ ] **Step 1: Create the workflow file**

Create `.github/workflows/update-last-updated.yml`:

```yaml
name: Update last updated date

on:
  pull_request:
    types: [opened, synchronize]
    branches:
      - main

jobs:
  update-last-updated:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          ref: ${{ github.head_ref }}
          fetch-depth: 0
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Get changed MDX files
        id: changed-files
        uses: tj-actions/changed-files@v45
        with:
          files: |
            **/*.mdx

      - name: Update last-updated frontmatter
        if: steps.changed-files.outputs.any_changed == 'true'
        run: |
          CURRENT_DATE=$(date +"%B %-d, %Y")
          echo "Current date: $CURRENT_DATE"

          for file in ${{ steps.changed-files.outputs.all_changed_files }}; do
            echo "Processing: $file"

            if [ ! -f "$file" ]; then
              echo "File not found, skipping: $file"
              continue
            fi

            if ! head -1 "$file" | grep -q "^---"; then
              echo "No frontmatter found, skipping: $file"
              continue
            elif grep -q "^last-updated:" "$file"; then
              echo "Updating existing last-updated field"
              sed -i "s/^last-updated:.*$/last-updated: $CURRENT_DATE/" "$file"
            else
              echo "Adding last-updated field to existing frontmatter"
              awk -v date="$CURRENT_DATE" '
                BEGIN { in_frontmatter=0; added=0 }
                NR==1 && /^---$/ { in_frontmatter=1; print; next }
                in_frontmatter && /^---$/ && !added { print "last-updated: " date; added=1; print; in_frontmatter=0; next }
                { print }
              ' "$file" > "${file}.tmp" && mv "${file}.tmp" "$file"
            fi
          done

      - name: Commit changes
        if: steps.changed-files.outputs.any_changed == 'true'
        run: |
          git config --local user.email "github-actions[bot]@users.noreply.github.com"
          git config --local user.name "github-actions[bot]"
          git add -A
          if git diff --staged --quiet; then
            echo "No changes to commit"
          else
            git commit -m "chore: update last-updated date in MDX files"
            git push
          fi
```

- [ ] **Step 2: Commit**

```bash
cd /Users/damjan/development/listbee-dev/listbee-docs
git add .github/workflows/update-last-updated.yml
git commit -m "ci: add auto-update last-updated date workflow"
```

---

## Post-implementation reminders

- Add `FERN_TOKEN` secret to the listbee-docs GitHub repository settings (required for preview-docs workflow)
- Run `make preview` locally to verify AI search and changelog render correctly before deploying
