# Docs Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bring listbee-docs content and structure to industry-grade quality, benchmarked against docs.agentmail.to and docs.zernio.com.

**Architecture:** Edit 22 existing MDX pages (add next-steps, callouts, quick-ref tables), create 3 new pages (entity-model, limitations, openapi), update docs.yml navigation, and enhance changelog format. No custom CSS, no diagrams.

**Tech Stack:** Fern docs framework, MDX, YAML

---

## Parallel Execution Map

Tasks 1–8 are fully independent and can run in parallel. Task 9 depends on Task 1 (new pages must exist before adding to navigation). Task 10 depends on all others.

```
┌──────────────────────────────────────────────────────────────┐
│  PARALLEL BATCH (Tasks 1–8, all independent)                 │
│                                                              │
│  T1: New pages (3 files)                                     │
│  T2: Welcome page overhaul                                   │
│  T3: Introduction page improvements                          │
│  T4: Errors page enhancement                                 │
│  T5: Core concept pages (5 files: listings→readiness→etc)    │
│  T6: Guide pages (4 files: auth, idempotency, etc)           │
│  T7: Integration pages (4 files: mcp, sdk, n8n, skill)       │
│  T8: Example + resource pages (5 files)                      │
└──────────────────────┬───────────────────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────────────────┐
│  T9: docs.yml + changelog (depends on T1 for new page paths) │
└──────────────────────┬───────────────────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────────────────┐
│  T10: Fern build validation                                  │
└──────────────────────────────────────────────────────────────┘
```

---

## File Reference

All paths relative to `/Users/damjan/development/listbee-dev/listbee-docs/fern/`.

**Writing standards (apply to all tasks):**
- Follow listbee-voice: direct, technical, no buzzwords
- Sentence case headers
- Every page ends with "Copy for AI assistants" code block (do not remove or reorder)
- Python + TypeScript tabs for code examples
- All examples must be runnable
- Fern callout components: `<Tip>`, `<Note>`, `<Warning>` (lowercase tag names)
- Fern card components: `<Cards>` and `<Card title="..." href="...">`

---

### Task 1: Create new pages (entity-model, limitations, openapi)

**Files:**
- Create: `docs/pages/entity-model.mdx`
- Create: `docs/pages/limitations.mdx`
- Create: `docs/pages/openapi.mdx`

- [ ] **Step 1: Create entity-model.mdx**

Create `docs/pages/entity-model.mdx` with this content:

```mdx
---
title: Entity model
description: The full ListBee entity hierarchy — accounts, listings, orders, access grants, and how they relate.
---

ListBee has six core entities. This page shows how they relate and where to find detailed documentation for each one.

---

## Hierarchy

```
Account
├── Listing
│   ├── Order
│   │   └── Access Grant
│   └── Content (file / url / text)
├── Webhook
└── API Key
```

An **account** owns everything. **Listings** are the products you sell. When a buyer pays, an **order** is created and an **access grant** delivers the content. **Webhooks** notify you of events. **API keys** authenticate your requests.

---

## Entities

| Entity | ID prefix | Description | Docs |
|--------|-----------|-------------|------|
| Account | `acc_` | Your seller account. Owns all resources. One Stripe connection per account. | [Authentication](/authentication) |
| Listing | `lst_` | A priced digital product with a hosted product page. Looked up by slug, not ID. | [Listings](/listings) |
| Order | `ord_` | Created when a buyer completes payment. Read-only — you cannot create orders via API. | [Orders & Delivery](/orders) |
| Access Grant | `ag_` | Controls content delivery after payment. Internal — not exposed in the API. | [Orders & Delivery](/orders) |
| Webhook | `wh_` | An HTTP endpoint that receives event notifications. | [Webhooks](/webhooks) |
| API Key | `lbk_` | Authentication credential. Key value has `lb_` prefix; entity ID has `lbk_` prefix. | [Authentication](/authentication) |
| Event | `evt_` | A webhook payload describing something that happened (e.g. order.paid). | [Webhooks](/webhooks) |

---

## Relationships

- An account has many listings, webhooks, and API keys.
- A listing has many orders. Each order belongs to exactly one listing.
- An order has one access grant (created automatically on payment).
- A listing has one content payload (file, URL, or text). Content is immutable after creation.
- Webhooks receive events for all resources under the account — there is no per-listing webhook scoping.

---

## ID format

All IDs follow the pattern `{prefix}_{random}`. The prefix tells you the entity type at a glance:

```
acc_r7kq2xy9m3pR5tW1   → Account
lst_r7kq2xy9m3pR5tW1   → Listing
ord_r7kq2xy9m3pR5tW1   → Order
ag_r7kq2xy9m3pR5tW1    → Access Grant
wh_r7kq2xy9m3pR5tW1    → Webhook
lbk_r7kq2xy9m3pR5tW1   → API Key (entity)
lb_r7kq2xy9m3pR5tW1    → API Key (value — used in Authorization header)
evt_r7kq2xy9m3pR5tW1   → Event
```

---

## Next steps

- [Listings](/listings) — create and manage your first product.
- [Readiness system](/readiness) — understand when a listing is ready to sell.

---

## Copy for AI assistants

<CodeBlock title="Cursor / Claude Code">
```python
# ListBee — entity model
#
# Hierarchy: Account → Listing → Order → Access Grant
#                        └→ Content (file/url/text)
#            Account → Webhook, API Key
#
# ID prefixes:
#   acc_  account
#   lst_  listing (looked up by slug, not ID)
#   ord_  order
#   ag_   access grant (internal, not in API responses)
#   wh_   webhook
#   lbk_  API key entity
#   lb_   API key value (used in Authorization: Bearer lb_...)
#   evt_  event (webhook payload)
#
# Key relationships:
#   account has many: listings, webhooks, api_keys
#   listing has many: orders
#   listing has one: content (immutable)
#   order has one: access_grant (auto-created on payment)
#   webhooks are account-scoped (receive all events, no per-listing filter)
#
# Docs: https://docs.listbee.so/entity-model
```
</CodeBlock>
```

- [ ] **Step 2: Create limitations.mdx**

Create `docs/pages/limitations.mdx` with this content:

```mdx
---
title: Limitations
description: What ListBee does not support — boundaries to know before you build.
---

ListBee is focused on one-time digital content sales via API. This page documents what is explicitly outside that scope, so agents and developers can plan accordingly.

---

## Not supported

| Limitation | Details |
|-----------|---------|
| **Physical goods** | Digital content only. No shipping, inventory, or fulfillment. |
| **Subscriptions** | One-time purchases only. No recurring billing, trials, or plan management. |
| **Multi-currency per listing** | Currency is set at the account level. All listings under an account use the same currency. |
| **Custom checkout UI** | Checkout is hosted by ListBee on `buy.listbee.so`. No embeddable widgets or custom payment forms. |
| **Refund API** | Refunds are processed through the Stripe dashboard directly. No ListBee API endpoint for refunds. |
| **Content updates** | The `content` field is immutable after listing creation. To change content, delete the listing and create a new one. |
| **Per-listing webhooks** | Webhooks are account-scoped. You cannot subscribe to events for a specific listing only. |
| **Buyer accounts** | Buyers do not have accounts. They pay via Stripe Checkout and receive content by email. No buyer login or purchase history. |

---

## Platform limits

| Resource | Limit |
|----------|-------|
| Listings per account | No hard limit |
| Orders per month (Free plan) | 50 |
| API keys per account | 10 |
| Webhooks per account | 10 |
| Metadata keys per listing | 50 |
| Content file size | 100 MB |
| Rate limits | See [Rate limits](/rate-limits) |

---

## Next steps

- [FAQ](/faq) — common questions about ListBee.
- [Errors](/errors) — understand error responses when you hit a boundary.

---

## Copy for AI assistants

<CodeBlock title="Cursor / Claude Code">
```python
# ListBee — limitations
#
# NOT supported:
#   - Physical goods (digital only)
#   - Subscriptions / recurring billing (one-time purchases only)
#   - Multi-currency per listing (currency is account-level)
#   - Custom checkout UI (hosted on buy.listbee.so)
#   - Refund API (use Stripe dashboard)
#   - Content updates (immutable — delete and recreate)
#   - Per-listing webhooks (account-scoped only)
#   - Buyer accounts (no login, no purchase history)
#
# Platform limits:
#   Orders/month (Free): 50
#   API keys/account:    10
#   Webhooks/account:    10
#   Metadata keys:       50
#   Content file size:   100 MB
#
# Docs: https://docs.listbee.so/limitations
```
</CodeBlock>
```

- [ ] **Step 3: Create openapi.mdx**

Create `docs/pages/openapi.mdx` with this content:

```mdx
---
title: OpenAPI spec
description: Download the ListBee OpenAPI specification for use with API tools, SDKs, and AI agents.
---

The ListBee API is fully described by an OpenAPI 3.1 specification. Use it to auto-generate clients, import into API tools, or feed directly to AI agents.

---

## Download

| Format | URL |
|--------|-----|
| OpenAPI 3.1 (JSON) | [api.listbee.so/openapi.json](https://api.listbee.so/openapi.json) |
| llms.txt | [api.listbee.so/llms.txt](https://api.listbee.so/llms.txt) |

---

## What uses the spec

The OpenAPI spec is the single source of truth for all ListBee clients and tools:

- **[MCP server](/mcp)** — tools are derived from the spec via [fastapi-mcp](https://github.com/tadata-org/fastapi-mcp)
- **[Python SDK](/python-sdk)** — type definitions and method signatures match the spec
- **[n8n node](/n8n)** — field definitions align with spec schemas
- **[API reference](/api-reference)** — auto-generated by Fern from the spec
- **Postman / Insomnia** — import the JSON URL directly
- **AI agents** — feed the spec URL or llms.txt to any LLM for full API context

---

## llms.txt

The `llms.txt` file is a condensed, plain-text summary of the API designed for LLM consumption. It includes endpoint descriptions, parameter types, and example payloads in a format optimized for context windows.

---

## Next steps

- [API reference](/api-reference) — browse the full endpoint documentation.
- [MCP server](/mcp) — connect the spec-powered MCP tools to your AI assistant.

---

## Copy for AI assistants

<CodeBlock title="Cursor / Claude Code">
```python
# ListBee — OpenAPI spec and machine-readable docs
#
# OpenAPI 3.1 spec: https://api.listbee.so/openapi.json
# llms.txt:         https://api.listbee.so/llms.txt
#
# The spec powers: MCP server, Python SDK, n8n node, API reference docs
# Import into Postman/Insomnia via the JSON URL
# Feed to any LLM for full API context
#
# Docs: https://docs.listbee.so/openapi
```
</CodeBlock>
```

- [ ] **Step 4: Commit new pages**

```bash
cd /Users/damjan/development/listbee-dev/listbee-docs
git add fern/docs/pages/entity-model.mdx fern/docs/pages/limitations.mdx fern/docs/pages/openapi.mdx
git commit -m "docs: add entity model, limitations, and OpenAPI spec pages"
```

---

### Task 2: Welcome page overhaul

**Files:**
- Modify: `docs/pages/welcome.mdx`

- [ ] **Step 1: Add problem/solution framing and update cards**

Edit `docs/pages/welcome.mdx`. Replace the entire file content with:

```mdx
---
title: Welcome
description: ListBee developer documentation — one API call to sell and deliver digital content.
---

One API call to sell and deliver digital content.

ListBee is listings infrastructure for AI agents. Create a listing with a title, price, and content — get back a product page URL. Buyers visit the URL, pay via Stripe, receive the content automatically.

## The problem

- **No API for agents to sell.** Gumroad, Lemon Squeezy, and similar tools require a human in a browser. Agents can't create listings programmatically.
- **No readiness feedback.** Existing platforms give no machine-readable signal about whether a product is ready to sell. Agents can't know what action is needed next.
- **Console-only setup.** Connecting payments, configuring products, and managing content all require manual steps in a web console.

ListBee solves all three. The API is the only interface — designed for agents to operate end-to-end.

## How it works

```
Agent creates listing → ListBee hosts product page → Buyer pays → Content delivered
```

AI agents create and manage listings on behalf of sellers. Buyers are always humans who see a product page, pay via Stripe Checkout, and receive content after purchase.

## Start here

<Cards>
  <Card title="Introduction" href="/introduction">
    What ListBee is, what it solves, and how the commerce model works.
  </Card>
  <Card title="Quickstart" href="/quickstart">
    Three API calls: signup, connect Stripe, create listing.
  </Card>
  <Card title="API reference" href="/api-reference">
    Every endpoint, every parameter, try-it panel.
  </Card>
  <Card title="Readiness system" href="/readiness">
    How agents know what to do next.
  </Card>
</Cards>

## For AI agents

ListBee is built for agents to consume directly:

- **OpenAPI spec:** [api.listbee.so/openapi.json](https://api.listbee.so/openapi.json)
- **MCP server:** `npx listbee-mcp`
- **Python SDK:** `pip install listbee`
- **Machine-readable docs:** [/llms.txt](https://api.listbee.so/llms.txt)

## Support

- **GitHub:** [github.com/listbee-dev](https://github.com/listbee-dev)
- **Email:** damian@listbee.so
- **Security:** damian@listbee.so with subject `[SECURITY]`
```

- [ ] **Step 2: Commit**

```bash
cd /Users/damjan/development/listbee-dev/listbee-docs
git add fern/docs/pages/welcome.mdx
git commit -m "docs: overhaul welcome page with problem/solution framing"
```

---

### Task 3: Introduction page improvements

**Files:**
- Modify: `docs/pages/introduction.mdx`

- [ ] **Step 1: Wrap pain points in Note callouts**

In `docs/pages/introduction.mdx`, find the section:

```
**No API for agents to sell.** Gumroad, Lemon Squeezy, and similar tools are console-only. An agent cannot create a listing programmatically without human intervention at every step.

**No readiness feedback.** Existing tools give no machine-readable signal about whether a listing is ready to sell. Agents have no way to know what action is needed next.

**Console-only account setup.** Connecting a payment method typically requires a human in a browser. ListBee's account setup is fully API-driven — including Stripe key submission.
```

Replace with:

```mdx
<Note>
**No API for agents to sell.** Gumroad, Lemon Squeezy, and similar tools are console-only. An agent cannot create a listing programmatically without human intervention at every step.
</Note>

<Note>
**No readiness feedback.** Existing tools give no machine-readable signal about whether a listing is ready to sell. Agents have no way to know what action is needed next.
</Note>

<Note>
**Console-only account setup.** Connecting a payment method typically requires a human in a browser. ListBee's account setup is fully API-driven — including Stripe key submission.
</Note>
```

- [ ] **Step 2: Add next steps before AI reference block**

In `docs/pages/introduction.mdx`, find the line:

```
---

## Copy for AI assistants
```

Insert before it:

```mdx
---

## Next steps

<Cards>
  <Card title="Quickstart" href="/quickstart">
    Three API calls to go from zero to a live listing.
  </Card>
  <Card title="Entity model" href="/entity-model">
    How accounts, listings, orders, and access grants relate.
  </Card>
</Cards>

```

- [ ] **Step 3: Commit**

```bash
cd /Users/damjan/development/listbee-dev/listbee-docs
git add fern/docs/pages/introduction.mdx
git commit -m "docs: add callouts and next steps to introduction page"
```

---

### Task 4: Errors page enhancement

**Files:**
- Modify: `docs/pages/errors.mdx`

- [ ] **Step 1: Replace two-column error table with three-column resolution table**

In `docs/pages/errors.mdx`, find:

```
## Common error codes

| Code | Status | Description |
|------|--------|-------------|
| `authentication_required` | 401 | No API key in the `Authorization` header. |
| `invalid_api_key` | 401 | The API key is malformed, expired, or revoked. |
| `not_found` | 404 | The requested resource does not exist. |
| `invalid_field` | 422 | A field failed validation. Check `param` for which field. |
| `missing_field` | 422 | A required field was not provided. Check `param`. |
| `unsupported_currency` | 422 | The currency code is not supported. |
| `price_too_low` | 422 | The price is below the minimum allowed amount. |
| `stripe_not_connected` | 422 | No Stripe account connected. The listing cannot sell. |
| `content_fetch_failed` | 422 | ListBee could not fetch the content URL you provided. |
| `idempotency_conflict` | 409 | Same `Idempotency-Key` was used with a different request body. |
| `rate_limit_exceeded` | 429 | Too many requests. Respect the `Retry-After` header. |
| `internal_error` | 500 | Unexpected server error. Safe to retry with exponential backoff. |
```

Replace with:

```
## Common error codes

| Code | Cause | Resolution |
|------|-------|------------|
| `authentication_required` | No API key in the `Authorization` header | Add `Authorization: Bearer lb_...` header to the request |
| `invalid_api_key` | Key is malformed, expired, or revoked | Check key format (`lb_` prefix) or create a new key via `POST /v1/api-keys` |
| `not_found` | Resource does not exist | Verify the ID or slug — listings use slug, not ID |
| `invalid_field` | A field failed validation | Check the `param` field in the error response for which field, then fix the value |
| `missing_field` | A required field was not provided | Check the `param` field, then add the missing field to the request body |
| `unsupported_currency` | The currency code is not supported | Use a supported currency — currency is set at the account level |
| `price_too_low` | Price is below Stripe's minimum | Set price to at least 50 (smallest currency unit, e.g. 50 cents) |
| `stripe_not_connected` | No Stripe account linked to this account | Call `POST /v1/account/stripe-key` with your Stripe secret key |
| `content_fetch_failed` | ListBee couldn't reach the content URL | Verify the URL is publicly accessible and returns HTTP 200 |
| `idempotency_conflict` | Same `Idempotency-Key` sent with a different request body | Generate a new UUID for the new request |
| `rate_limit_exceeded` | Too many requests for this endpoint | Wait for `Retry-After` header value (seconds), then retry |
| `internal_error` | Unexpected server error | Safe to retry with exponential backoff — if persistent, contact support |
```

- [ ] **Step 2: Add next steps before AI reference block**

In `docs/pages/errors.mdx`, find the line:

```
---

## Copy for AI assistants
```

Insert before it:

```mdx
---

## Next steps

- [Entity model](/entity-model) — see the full resource hierarchy and ID prefix reference.
- [Rate limits](/rate-limits) — understand per-endpoint limits and backoff strategies.

```

- [ ] **Step 3: Update the AI reference block to match new table format**

In `docs/pages/errors.mdx`, find the existing "Common codes" section in the AI reference block:

```
# Common codes:
#   authentication_required  401  No or invalid API key
#   invalid_api_key          401  API key malformed, expired, or revoked
#   not_found                404  Resource does not exist
#   invalid_field            422  Field failed validation — check param
#   missing_field            422  Required field absent — check param
#   unsupported_currency     422  Currency code not supported
#   price_too_low            422  Price below minimum
#   stripe_not_connected     422  No Stripe connected, listing can't sell
#   content_fetch_failed     422  Could not fetch the content URL
#   idempotency_conflict     409  Same Idempotency-Key, different body
#   rate_limit_exceeded      429  Too many requests — respect Retry-After header
#   internal_error           500  Server error — safe to retry with backoff
```

Replace with:

```
# Common codes (code → cause → resolution):
#   authentication_required  401  No API key → add Authorization: Bearer lb_... header
#   invalid_api_key          401  Key malformed/expired → check lb_ prefix or create new key
#   not_found                404  Resource missing → verify ID/slug (listings use slug)
#   invalid_field            422  Validation failed → check param field, fix value
#   missing_field            422  Required field absent → check param field, add it
#   unsupported_currency     422  Bad currency → use account-level currency
#   price_too_low            422  Below minimum → set price >= 50 (cents)
#   stripe_not_connected     422  No Stripe → POST /v1/account/stripe-key
#   content_fetch_failed     422  URL unreachable → verify URL returns 200
#   idempotency_conflict     409  Same key, diff body → generate new UUID
#   rate_limit_exceeded      429  Too many requests → wait Retry-After seconds
#   internal_error           500  Server error → retry with exponential backoff
```

- [ ] **Step 4: Commit**

```bash
cd /Users/damjan/development/listbee-dev/listbee-docs
git add fern/docs/pages/errors.mdx
git commit -m "docs: upgrade error codes to three-column resolution table"
```

---

### Task 5: Core concept pages — next steps + callouts

**Files:**
- Modify: `docs/pages/listings.mdx`
- Modify: `docs/pages/orders.mdx`
- Modify: `docs/pages/readiness.mdx`
- Modify: `docs/pages/payments.mdx`
- Modify: `docs/pages/webhooks.mdx`

For each file, insert content **before** the `## Copy for AI assistants` section (find the `---` + `## Copy for AI assistants` pattern and insert before it).

- [ ] **Step 1: Add next steps to listings.mdx**

In `docs/pages/listings.mdx`, find:

```
---

## Copy for AI assistants
```

Insert before it:

```mdx
---

## Next steps

- [Orders & Delivery](/orders) — what happens after a buyer pays.
- [Content types](/content-types) — how auto-detection works and when to override it.

```

- [ ] **Step 2: Add next steps to orders.mdx**

In `docs/pages/orders.mdx`, find:

```
---

## Copy for AI assistants
```

Insert before it:

```mdx
---

## Next steps

- [Webhooks](/webhooks) — get notified when orders are paid instead of polling.
- [Listings](/listings) — manage the products that generate orders.

```

- [ ] **Step 3: Add next steps to readiness.mdx**

In `docs/pages/readiness.mdx`, find:

```
---

## Copy for AI assistants
```

Insert before it:

```mdx
---

## Next steps

- [Agent onboarding flow](/agent-onboarding) — see the readiness system in action during a full onboarding dialogue.
- [Payments](/payments) — connect Stripe to resolve the most common readiness actions.

```

- [ ] **Step 4: Add callout and next steps to payments.mdx**

In `docs/pages/payments.mdx`, find the line:

```
There are two paths depending on whether you already have a Stripe account.
```

Insert after it:

```mdx

<Note>
Direct key submission (Path 1) is faster for agents — no browser required. Connect onboarding (Path 2) is better when the seller manages their own Stripe dashboard.
</Note>
```

Then in the same file, find:

```
---

## Copy for AI assistants
```

Insert before it:

```mdx
---

## Next steps

- [Listings](/listings) — create your first product now that Stripe is connected.
- [Readiness system](/readiness) — understand how payment status affects listing readiness.

```

- [ ] **Step 5: Add callout and next steps to webhooks.mdx**

In `docs/pages/webhooks.mdx`, find the signature verification code block section. Look for the text that discusses timing-safe comparison. Find the line that contains `hmac.compare_digest` or mentions timing-safe comparison. Add a warning callout right after the signature verification code examples and before the next `---` separator.

Specifically, find the end of the signature verification `</CodeGroup>` tag and the `---` that follows it. Insert between them:

```mdx

<Warning>
Always use timing-safe comparison for signature verification. Standard string equality (`==`) is vulnerable to timing attacks that can leak your webhook secret.
</Warning>

```

Then find:

```
---

## Copy for AI assistants
```

Insert before it:

```mdx
---

## Next steps

- [Errors](/errors) — handle webhook delivery failures and error responses.
- [Idempotency](/idempotency) — ensure your webhook handler processes events exactly once.

```

- [ ] **Step 6: Commit**

```bash
cd /Users/damjan/development/listbee-dev/listbee-docs
git add fern/docs/pages/listings.mdx fern/docs/pages/orders.mdx fern/docs/pages/readiness.mdx fern/docs/pages/payments.mdx fern/docs/pages/webhooks.mdx
git commit -m "docs: add next steps and callouts to core concept pages"
```

---

### Task 6: Guide pages — next steps + callouts

**Files:**
- Modify: `docs/pages/authentication.mdx`
- Modify: `docs/pages/idempotency.mdx`
- Modify: `docs/pages/rate-limits.mdx`
- Modify: `docs/pages/content-types.mdx`

For each file, insert content **before** the `## Copy for AI assistants` section.

- [ ] **Step 1: Add callout and next steps to authentication.mdx**

In `docs/pages/authentication.mdx`, find the section about key rotation or deleting keys. Look for text mentioning rotation strategy or deleting old keys. Insert near that section:

```mdx
<Tip>
Create a new key before revoking the old one to avoid downtime. Both keys work simultaneously until you delete the old one.
</Tip>
```

Then find:

```
---

## Copy for AI assistants
```

Insert before it:

```mdx
---

## Next steps

- [Idempotency](/idempotency) — protect against duplicate requests with idempotency keys.
- [Rate limits](/rate-limits) — understand per-endpoint rate limits for your API key.

```

- [ ] **Step 2: Add callout and next steps to idempotency.mdx**

In `docs/pages/idempotency.mdx`, find text mentioning the 24-hour cache duration or key expiry. Insert near it:

```mdx
<Note>
Idempotency keys expire after 24 hours. After expiry, the same key is treated as a new request and will execute again.
</Note>
```

Then find:

```
---

## Copy for AI assistants
```

Insert before it:

```mdx
---

## Next steps

- [Rate limits](/rate-limits) — idempotent retries hit the cache, not the rate limiter.
- [Errors](/errors) — handle `idempotency_conflict` (409) when keys are reused with different bodies.

```

- [ ] **Step 3: Add callout and next steps to rate-limits.mdx**

In `docs/pages/rate-limits.mdx`, find the section about 429 responses or the retry strategy. Insert near it:

```mdx
<Warning>
Respect the `Retry-After` header. Ignoring it and continuing to send requests may result in extended throttling.
</Warning>
```

Then find:

```
---

## Copy for AI assistants
```

Insert before it:

```mdx
---

## Next steps

- [Idempotency](/idempotency) — safe retries that don't count against rate limits.
- [Errors](/errors) — full reference for `rate_limit_exceeded` and other error codes.

```

- [ ] **Step 4: Add callout and next steps to content-types.mdx**

In `docs/pages/content-types.mdx`, find text about auto-detection. Insert near the top of the page, after the introductory paragraph:

```mdx
<Tip>
ListBee detects content type automatically via a HEAD request to your URL. You don't need to specify the type explicitly in most cases.
</Tip>
```

Then find:

```
---

## Copy for AI assistants
```

Insert before it:

```mdx
---

## Next steps

- [Listings](/listings) — create a listing with your content attached.
- [Limitations](/limitations) — content is immutable after creation and capped at 100 MB for files.

```

- [ ] **Step 5: Commit**

```bash
cd /Users/damjan/development/listbee-dev/listbee-docs
git add fern/docs/pages/authentication.mdx fern/docs/pages/idempotency.mdx fern/docs/pages/rate-limits.mdx fern/docs/pages/content-types.mdx
git commit -m "docs: add next steps and callouts to guide pages"
```

---

### Task 7: Integration pages — quick-ref tables, common errors, limitations

**Files:**
- Modify: `docs/pages/mcp.mdx`
- Modify: `docs/pages/claude-code-skill.mdx`
- Modify: `docs/pages/python-sdk.mdx`
- Modify: `docs/pages/n8n.mdx`

- [ ] **Step 1: Add quick-ref table, errors, limitations, and next steps to mcp.mdx**

In `docs/pages/mcp.mdx`, after the frontmatter and first paragraph, insert:

```mdx

| | |
|---|---|
| **Package** | `listbee-mcp` |
| **Install** | `npx listbee-mcp` (no global install) |
| **Auth** | `LISTBEE_API_KEY` environment variable |
| **Source** | [github.com/listbee-dev/listbee](https://github.com/listbee-dev/listbee) |

```

Then, before `## Copy for AI assistants`, insert:

```mdx
---

## Common errors

| Error | Cause | Resolution |
|-------|-------|------------|
| `LISTBEE_API_KEY not set` | Environment variable missing from MCP config | Add `"LISTBEE_API_KEY": "lb_..."` to the `env` block in your MCP config |
| `Could not connect to MCP server` | `npx` failed to fetch the package | Check internet connection; run `npx listbee-mcp` manually to diagnose |
| `authentication_required` from tools | API key is invalid or expired | Verify the key starts with `lb_` and is active in [console.listbee.so](https://console.listbee.so) |
| Tools not appearing in client | Config file not in the right location or malformed JSON | Check file path per platform table above; validate JSON syntax |

## Limitations

- **No webhook management** — the MCP server does not expose webhook CRUD. Use the API directly or the Python SDK.
- **No account signup** — the server assumes an existing API key. Create accounts via the API.
- **No Stripe connection** — connecting Stripe requires the API directly. Use `POST /v1/account/stripe-key`.
- **Read-only orders** — you can list and get orders, but cannot create or modify them (orders are created by buyer checkout).

---

## Next steps

- [Claude Code skill](/claude-code-skill) — an alternative integration for Claude Code that doesn't require MCP.
- [Agent onboarding flow](/agent-onboarding) — the canonical pattern for agents selling on ListBee.

```

- [ ] **Step 2: Add quick-ref table, errors, limitations, and next steps to claude-code-skill.mdx**

In `docs/pages/claude-code-skill.mdx`, after the frontmatter and first paragraph, insert:

```mdx

| | |
|---|---|
| **Skill location** | `.claude/skills/listbee/SKILL.md` (project) or `~/.claude/skills/listbee/SKILL.md` (global) |
| **Auth** | `LISTBEE_API_KEY` environment variable |
| **Triggers** | "sell something", "create a listing", "check orders", "update listing" |

```

Then, before `## Copy for AI assistants`, insert:

```mdx
---

## Common errors

| Error | Cause | Resolution |
|-------|-------|------------|
| Skill not triggering | Skill file not in `.claude/skills/` or wrong filename | Verify path is `.claude/skills/listbee/SKILL.md` (case-sensitive) |
| `LISTBEE_API_KEY` not found | Environment variable not set in shell or `.env` | Add `export LISTBEE_API_KEY=lb_...` to shell profile or project `.env` |
| `authentication_required` | API key is invalid | Verify the key starts with `lb_` and is active |
| Claude uses generic HTTP instead of skill | Prompt didn't match skill trigger words | Use keywords like "listing", "sell", "product", or "order" |

## Limitations

- **No MCP tool calling** — the skill instructs Claude Code to run Python/httpx code directly. It does not use MCP tools.
- **No webhook management** — the skill covers listings, orders, and account operations. Webhook CRUD is not included.
- **Python-only examples** — the skill's code blocks use Python with httpx. Claude Code may adapt to TypeScript if asked, but the skill doesn't include TypeScript examples.

---

## Next steps

- [MCP server](/mcp) — an alternative integration using MCP tools instead of a skill file.
- [Python SDK](/python-sdk) — typed client with error handling, pagination, and async support.

```

- [ ] **Step 3: Add quick-ref table, errors, limitations, and next steps to python-sdk.mdx**

In `docs/pages/python-sdk.mdx`, after the frontmatter and first paragraph, insert:

```mdx

| | |
|---|---|
| **Package** | `listbee` |
| **Install** | `pip install listbee` |
| **Min Python** | 3.9+ |
| **Auth** | `ListBee(api_key="lb_...")` or `LISTBEE_API_KEY` env var |
| **Source** | [github.com/listbee-dev/listbee-python](https://github.com/listbee-dev/listbee-python) |
| **PyPI** | [pypi.org/project/listbee](https://pypi.org/project/listbee/) |

```

Then, before `## Copy for AI assistants`, insert:

```mdx
---

## Common errors

| Error | Cause | Resolution |
|-------|-------|------------|
| `AuthenticationError` | API key missing, invalid, or revoked | Pass a valid `lb_...` key to `ListBee()` or set `LISTBEE_API_KEY` env var |
| `NotFoundError` | Listing slug or order ID doesn't exist | Verify the slug/ID — listings use slug (`r7kq2xy9`), orders use ID (`ord_...`) |
| `ValidationError` | Request body failed server-side validation | Check the `param` attribute on the error for the offending field |
| `RateLimitError` | Too many requests | The SDK does not auto-retry on 429. Implement backoff using `retry_after` attribute |
| `ImportError: No module named 'listbee'` | Package not installed | Run `pip install listbee` in the correct virtual environment |

## Limitations

- **No auto-retry** — the SDK raises on 429/5xx. Implement your own retry logic.
- **No webhook signature verification** — use `hmac` directly as shown in the [Webhooks](/webhooks) guide.
- **No file upload** — the `content` field accepts URLs, not file objects. Upload to your own storage first.
- **Sync by default** — use `AsyncListBee` for async contexts. The sync and async clients have identical APIs.

---

## Next steps

- [Quickstart](/quickstart) — use the SDK to go from zero to a live listing.
- [Webhooks](/webhooks) — receive order notifications with signature verification.

```

- [ ] **Step 4: Add quick-ref table, errors, limitations, and next steps to n8n.mdx**

In `docs/pages/n8n.mdx`, after the frontmatter and first paragraph, insert:

```mdx

| | |
|---|---|
| **Package** | `n8n-nodes-listbee` |
| **Install** | Community nodes UI or `npm install n8n-nodes-listbee` |
| **Auth** | ListBee API credential (`lb_...`) |
| **Source** | [github.com/listbee-dev/n8n-nodes-listbee](https://github.com/listbee-dev/n8n-nodes-listbee) |
| **npm** | [npmjs.com/package/n8n-nodes-listbee](https://www.npmjs.com/package/n8n-nodes-listbee) |

```

Then, before `## Copy for AI assistants`, insert:

```mdx
---

## Common errors

| Error | Cause | Resolution |
|-------|-------|------------|
| Node not appearing after install | n8n needs restart to load community nodes | Restart n8n after installing via Community Nodes UI |
| `Authentication failed` | Credential has invalid or expired API key | Edit the ListBee credential in n8n and paste a valid `lb_...` key |
| `404 Not Found` on listing operations | Wrong slug in the Slug field | Verify the slug matches — use the List Listings operation to find it |
| Webhook trigger not firing | Webhook URL not registered with ListBee | Register the n8n webhook URL via `POST /v1/webhooks` with the n8n-provided URL |
| `ECONNREFUSED` on self-hosted n8n | n8n webhook URL not reachable from internet | Use a tunnel (ngrok, Cloudflare Tunnel) or ensure n8n is publicly accessible |

## Limitations

- **No Stripe connection management** — connecting/disconnecting Stripe requires the API directly.
- **No webhook CRUD in the node** — register webhooks via the API or HTTP Request node. The n8n node provides a Webhook Trigger for receiving events.
- **No content type override** — the node passes content as-is. Auto-detection handles type. To override, use the HTTP Request node.

---

## Next steps

- [Example: n8n workflow](/example-n8n) — a complete 4-node workflow that creates a listing and notifies Slack on sale.
- [Webhooks](/webhooks) — set up webhook-triggered automations.

```

- [ ] **Step 5: Commit**

```bash
cd /Users/damjan/development/listbee-dev/listbee-docs
git add fern/docs/pages/mcp.mdx fern/docs/pages/claude-code-skill.mdx fern/docs/pages/python-sdk.mdx fern/docs/pages/n8n.mdx
git commit -m "docs: add quick-ref tables, common errors, and limitations to integration pages"
```

---

### Task 8: Example + resource pages — next steps

**Files:**
- Modify: `docs/pages/agent-onboarding.mdx`
- Modify: `docs/pages/example-claude-code.mdx`
- Modify: `docs/pages/example-n8n.mdx`
- Modify: `docs/pages/example-storefront.mdx`
- Modify: `docs/pages/faq.mdx`
- Modify: `docs/pages/community.mdx`

For each file, insert before `## Copy for AI assistants`.

- [ ] **Step 1: Add next steps to agent-onboarding.mdx**

Insert before `## Copy for AI assistants`:

```mdx
---

## Next steps

- [MCP server](/mcp) — give your agent ListBee tools directly via MCP.
- [Readiness system](/readiness) — deep dive into how readiness actions work.

```

- [ ] **Step 2: Add next steps to example-claude-code.mdx**

Insert before `## Copy for AI assistants`:

```mdx
---

## Next steps

- [Example: n8n workflow](/example-n8n) — automate listing creation and order notifications.
- [Claude Code skill](/claude-code-skill) — teach Claude Code to use ListBee without explaining the API each time.

```

- [ ] **Step 3: Add next steps to example-n8n.mdx**

Insert before `## Copy for AI assistants`:

```mdx
---

## Next steps

- [Example: storefront script](/example-storefront) — bulk-create listings from a JSON catalog.
- [n8n node](/n8n) — full reference for the ListBee community node.

```

- [ ] **Step 4: Add next steps to example-storefront.mdx**

Insert before `## Copy for AI assistants`:

```mdx
---

## Next steps

- [API reference](/api-reference) — explore every endpoint in detail.
- [Webhooks](/webhooks) — get notified on orders instead of polling.

```

- [ ] **Step 5: Add next steps to faq.mdx**

Insert before `## Copy for AI assistants`:

```mdx
---

## Next steps

- [Limitations](/limitations) — explicit boundaries and platform limits.
- [Community](/community) — get help or report issues.

```

- [ ] **Step 6: Add next steps to community.mdx**

Insert before `## Copy for AI assistants`:

```mdx
---

## Next steps

- [FAQ](/faq) — common questions about ListBee.
- [OpenAPI spec](/openapi) — download the spec for your tools.

```

- [ ] **Step 7: Commit**

```bash
cd /Users/damjan/development/listbee-dev/listbee-docs
git add fern/docs/pages/agent-onboarding.mdx fern/docs/pages/example-claude-code.mdx fern/docs/pages/example-n8n.mdx fern/docs/pages/example-storefront.mdx fern/docs/pages/faq.mdx fern/docs/pages/community.mdx
git commit -m "docs: add next steps to example and resource pages"
```

---

### Task 9: docs.yml navigation + changelog enhancement

**Files:**
- Modify: `docs.yml`
- Modify: `docs/changelog/overview.mdx`
- Modify: `docs/changelog/TEMPLATE.mdx`

**Depends on:** Task 1 (new page files must exist)

- [ ] **Step 1: Add new pages to docs.yml navigation**

In `docs.yml`, find the Core Concepts section. After the Errors entry:

```yaml
          - page: Errors
            path: ./docs/pages/errors.mdx
```

Add:

```yaml
          - page: Entity Model
            slug: entity-model
            path: ./docs/pages/entity-model.mdx
```

Then find the Resources section:

```yaml
      - section: Resources
        skip-slug: true
        contents:
          - page: FAQ
            path: ./docs/pages/faq.mdx
          - page: Community
            path: ./docs/pages/community.mdx
```

Replace with:

```yaml
      - section: Resources
        skip-slug: true
        contents:
          - page: FAQ
            path: ./docs/pages/faq.mdx
          - page: Limitations
            path: ./docs/pages/limitations.mdx
          - page: OpenAPI Spec
            slug: openapi
            path: ./docs/pages/openapi.mdx
          - page: Community
            path: ./docs/pages/community.mdx
```

- [ ] **Step 2: Update changelog overview**

Replace the entire content of `docs/changelog/overview.mdx` with:

```mdx
# ListBee Changelog

API, SDK, and platform updates. Each entry is tagged by type: **New**, **Improved**, **Fixed**, or **Breaking**.

[Subscribe via RSS](https://docs.listbee.so/changelog.rss)
```

- [ ] **Step 3: Update changelog template**

Replace the entire content of `docs/changelog/TEMPLATE.mdx` with:

```mdx
---
tags: ["area-tag", "type-tag"]
---

# Title

<!-- Tag taxonomy:
  Area: api, console, checkout, webhooks, mcp, sdk, n8n, docs
  Type: new-feature, improvement, breaking-change, fix
-->

Summary (2-3 sentences, benefit-focused).

## What changed

- **New:** description of new feature or endpoint
- **Improved:** description of enhancement
- **Fixed:** description of bug fix
- **Breaking:** description of breaking change + migration steps

## Migration (if breaking)

Before:

```python
# old pattern
```

After:

```python
# new pattern
```
```

- [ ] **Step 4: Commit**

```bash
cd /Users/damjan/development/listbee-dev/listbee-docs
git add fern/docs.yml fern/docs/changelog/overview.mdx fern/docs/changelog/TEMPLATE.mdx
git commit -m "docs: update navigation with new pages, enhance changelog format"
```

---

### Task 10: Fern build validation

**Depends on:** All previous tasks

- [ ] **Step 1: Run fern check**

```bash
cd /Users/damjan/development/listbee-dev/listbee-docs
npx fern check
```

Expected: no errors. Warnings about unused definitions are acceptable.

- [ ] **Step 2: Run fern build preview**

```bash
cd /Users/damjan/development/listbee-dev/listbee-docs
make preview
```

Expected: local preview server starts. Spot-check:
- Welcome page has problem/solution section and 4 cards
- Introduction page has Note callouts around pain points
- Entity model page renders with hierarchy and table
- Limitations page renders with both tables
- OpenAPI spec page renders with download links
- Errors page has three-column table
- Each page has "Next steps" above "Copy for AI assistants"
- Integration pages have quick-ref tables and common errors sections
- Changelog overview shows updated description

- [ ] **Step 3: Commit any fixes if needed**

If fern check reports errors, fix them and commit:

```bash
cd /Users/damjan/development/listbee-dev/listbee-docs
git add -A
git commit -m "docs: fix fern validation issues"
```
