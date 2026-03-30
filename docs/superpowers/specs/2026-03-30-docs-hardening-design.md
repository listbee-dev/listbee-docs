# Fern Docs Hardening — Industry-Grade Content & Structure

Best-practices alignment pass for listbee-docs, benchmarked against docs.agentmail.to and docs.zernio.com.

**Audience priority:** AI agents/LLMs first, developers second.
**Approach:** Content + structure overhaul (Approach B). No custom CSS. Schematic diagrams only if text falls short — defer by default.

---

## 1. Welcome page overhaul

**File:** `welcome.mdx`

Add problem/solution framing before the cards:

- 3-4 pain-point statements as a concise list: "No API for agents to sell", "No readiness feedback", "Console-only setup"
- One-line solution: "ListBee: one API call to sell and deliver digital content"

Additional changes:

- Add Introduction as the first card (before Quickstart)
- Add support/community link at the bottom (email + GitHub)
- Keep existing flow diagram as text for now — upgrade to schematic image only if needed later

## 2. Introduction page improvements

**File:** `introduction.mdx`

- Wrap the three pain-point paragraphs ("No API for agents to sell", "No readiness feedback", "Console-only account setup") in Fern `<Note>` callouts for visual weight (not `<Warning>` — these are product positioning, not reader warnings)
- Add "Next steps" section before the AI reference block — link to Quickstart

No other changes. Comparison table, pricing table, and code sample are already at reference quality.

## 3. Cross-linking on every page

Add a "Next steps" section before the AI reference block on every content page. Format:

- Simple pages: 1-2 lines with inline links
- Junction pages (Quickstart, Welcome): `<Cards>` component

Reading path follows the natural progression:

- Listings → Orders & Delivery
- Orders → Webhooks
- Webhooks → Errors
- Errors → Entity Model
- Quickstart → Cards to Listings + Webhooks
- Each Guide page → next guide or back to Core Concepts
- Each Example page → next example or API Reference
- Integration pages → related guide or example

## 4. Strategic callouts

Add Fern callout components (`<Tip>`, `<Note>`, `<Warning>`) sparingly — only where they prevent mistakes or clarify decision points.

| Page | Type | Content |
|------|------|---------|
| Webhooks | `<Warning>` | Always use timing-safe comparison for signature verification |
| Authentication | `<Tip>` | Create a new key before revoking the old one to avoid downtime |
| Idempotency | `<Note>` | Keys expire after 24 hours — same key after expiry is treated as new request |
| Rate Limits | `<Warning>` | Respect the Retry-After header — ignoring it may extend throttling |
| Payments | `<Note>` | Direct key submission is faster for agents; Connect onboarding is better when sellers manage their own Stripe dashboard |
| Content Types | `<Tip>` | ListBee detects content type automatically via HEAD request — no need to specify it |

Rule: if a callout doesn't save the reader from a mistake or clarify a decision point, it doesn't go in.

## 5. Error docs enhancement

**File:** `errors.mdx`

Upgrade the "Common error codes" table from two-column (Code | Description) to three-column (Zernio pattern):

| Code | Cause | Resolution |
|------|-------|------------|
| `stripe_not_connected` | No Stripe account linked | Call `POST /v1/account/stripe-key` with your Stripe secret key |
| `content_fetch_failed` | ListBee couldn't reach the content URL | Verify the URL is publicly accessible and returns 200 |
| `price_too_low` | Price below Stripe's minimum | Set price to at least 50 (cents) |
| `idempotency_conflict` | Same key, different body | Generate a new UUID for the new request |
| `authentication_required` | No API key in Authorization header | Add `Authorization: Bearer lb_...` header |
| `invalid_api_key` | Key malformed, expired, or revoked | Check key format (lb_ prefix) or create a new key |
| `invalid_field` | Field failed validation | Check `param` field for which field, fix the value |
| `missing_field` | Required field not provided | Check `param` field, add the missing field |
| `unsupported_currency` | Currency code not supported | Use a supported currency (check account settings) |
| `rate_limit_exceeded` | Too many requests | Wait for `Retry-After` seconds, then retry |
| `not_found` | Resource does not exist | Verify the ID/slug — listings use slug, not ID |
| `internal_error` | Server error | Retry with exponential backoff |

No other structural changes to the errors page.

## 6. New pages

### 6a. Limitations

**File:** `limitations.mdx` — Resources section

Documents what ListBee explicitly does not support. Builds trust, saves agents from dead ends. Table or bullet list format:

- Physical goods (digital content only)
- Subscriptions/recurring billing (one-time purchases only)
- Multi-currency per listing (currency is account-level)
- Custom checkout UI (hosted checkout only)
- Refund API (refunds via Stripe dashboard)
- Any current platform limits (max file size, max listings, etc.)

Includes AI reference block.

### 6b. Entity model

**File:** `entity-model.mdx` — Core Concepts section (after Errors)

The "map" page showing the full entity hierarchy in one place:

```
Account → Listing → Order → Access Grant
           ↓
       Content (file/url/text)
```

Content:

- Visual hierarchy (text-based, schematic image only if text is insufficient)
- ID prefixes table: `acc_`, `lst_`, `ord_`, `ag_`, `lbk_`, `wh_`, `evt_`
- Brief description of each entity (1-2 sentences)
- Links to the detailed page for each entity

Includes AI reference block.

### 6c. OpenAPI spec download

**File:** `openapi.mdx` — Resources section

Direct links to download the spec:

- JSON: `https://api.listbee.so/openapi.json`
- llms.txt: `https://api.listbee.so/llms.txt`

Brief context: spec powers the MCP server, Python SDK, and can be imported into Postman/Insomnia/n8n.

Includes AI reference block.

## 7. Integration quick-reference enhancements

Augment each existing integration page (not replacing content):

### All four pages (MCP, Claude Code Skill, Python SDK, n8n)

Add to each:

1. **Quick reference table at top** — package name, install command, min version, auth method
2. **Common errors section** — 3-5 integration-specific errors with Cause | Resolution columns
3. **Limitations** — what the integration can't do vs the raw API

### Per-page specifics

- **MCP** — which tools are available, which API operations are not exposed
- **Claude Code Skill** — skill file location, trigger patterns, what operations are covered
- **Python SDK** — sync vs async, pagination, retry behavior, error types
- **n8n** — credential setup errors, webhook trigger caveats, operations by resource

## 8. Changelog enhancement

### Format changes

- Category badges per entry: `New`, `Improved`, `Fixed`, `Breaking`
- Structured entry format: badge → one-line summary → 2-3 bullet details
- Update overview page description
- Update TEMPLATE.mdx to reflect new format

### No backfilling

New format applies going forward only. Existing entries stay as-is.

## 9. Navigation changes (docs.yml)

### Additions only

**Core Concepts** — add after Errors:
```yaml
- page: Entity Model
  slug: entity-model
  path: ./docs/pages/entity-model.mdx
```

**Resources** — add:
```yaml
- page: Limitations
  path: ./docs/pages/limitations.mdx
- page: OpenAPI Spec
  slug: openapi
  path: ./docs/pages/openapi.mdx
```

No sections added or removed. No reordering.

---

## Scope boundaries

- No custom CSS or JS
- No generated diagrams unless text is insufficient (defer by default)
- No new navigation sections
- No pricing page in docs (already in Introduction)
- No video/demo content
- No backfilling changelog entries
- AI reference blocks kept on all pages (both references do this)
- Paprika/nanobanana available for schematic diagram generation if needed later

## Files changed

| File | Action |
|------|--------|
| `fern/docs.yml` | Edit: add 3 pages to navigation |
| `fern/docs/pages/welcome.mdx` | Edit: problem/solution, Introduction card, support link |
| `fern/docs/pages/introduction.mdx` | Edit: callouts, next steps |
| `fern/docs/pages/errors.mdx` | Edit: three-column resolution table |
| `fern/docs/pages/listings.mdx` | Edit: next steps, callout if applicable |
| `fern/docs/pages/orders.mdx` | Edit: next steps |
| `fern/docs/pages/readiness.mdx` | Edit: next steps |
| `fern/docs/pages/payments.mdx` | Edit: next steps, callout |
| `fern/docs/pages/webhooks.mdx` | Edit: next steps, callout |
| `fern/docs/pages/authentication.mdx` | Edit: next steps, callout |
| `fern/docs/pages/idempotency.mdx` | Edit: next steps, callout |
| `fern/docs/pages/rate-limits.mdx` | Edit: next steps, callout |
| `fern/docs/pages/content-types.mdx` | Edit: next steps, callout |
| `fern/docs/pages/quickstart.mdx` | Edit: next steps |
| `fern/docs/pages/agent-onboarding.mdx` | Edit: next steps |
| `fern/docs/pages/mcp.mdx` | Edit: quick-ref table, common errors, limitations, next steps |
| `fern/docs/pages/claude-code-skill.mdx` | Edit: quick-ref table, common errors, limitations, next steps |
| `fern/docs/pages/python-sdk.mdx` | Edit: quick-ref table, common errors, limitations, next steps |
| `fern/docs/pages/n8n.mdx` | Edit: quick-ref table, common errors, limitations, next steps |
| `fern/docs/pages/example-claude-code.mdx` | Edit: next steps |
| `fern/docs/pages/example-n8n.mdx` | Edit: next steps |
| `fern/docs/pages/example-storefront.mdx` | Edit: next steps |
| `fern/docs/pages/faq.mdx` | Edit: next steps |
| `fern/docs/pages/community.mdx` | Edit: next steps |
| `fern/docs/pages/entity-model.mdx` | Create: entity hierarchy page |
| `fern/docs/pages/limitations.mdx` | Create: limitations page |
| `fern/docs/pages/openapi.mdx` | Create: OpenAPI spec download page |
| `fern/docs/changelog/overview.mdx` | Edit: update description |
| `fern/docs/changelog/TEMPLATE.mdx` | Edit: new format with badges |

## References

- **Primary benchmark:** https://docs.agentmail.to/welcome
- **Secondary benchmark:** https://docs.zernio.com/
- **Prior spec (infra-focused, complementary):** `2026-03-30-fern-docs-improvements-design.md`
