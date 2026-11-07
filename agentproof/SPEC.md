# AgentProof authorization proof 0.1.0

**Service status: concept. Format status: beta.**

This document describes a file a merchant can check. It does not describe a live AgentProof service. The page at `agentproof/` is still a concept and a waitlist. `status.json` is exactly `{"status":"concept","accepting":"waitlist"}`. `POST /authorization-proof` is not implemented. Calling it on GitHub Pages fails, and that is expected.

Version 0.1.0 signs two constants into every proof: `service_status` is `concept`, and `format_status` is `beta`. A checker cannot promote that file into a live credential.

Northwind Goods, Harbor Shopping Agent, and Alex Rivera, where they appear in the demo and fixtures, are fictional. There are no customers and no dispute results.

## What you can run

- [Authorization demo](demo/) signs one fictional purchase in the browser, checks it, and records a local accept, refuse, or undo.
- [verifier/agentproof.js](verifier/agentproof.js) is the checker. It has no dependencies. It uses Web Crypto Ed25519.
- [authorization-proof.schema.json](schema/authorization-proof.schema.json) and [order-evidence.schema.json](schema/order-evidence.schema.json) are the JSON Schemas.
- [fixtures/wool-blanket.proof.json](fixtures/wool-blanket.proof.json) is a signed fictional vector. Its public key is in the file. The private key was discarded. The vector expires at `2026-11-07T20:15:00.000Z`. Check it by passing a `now` inside that window, or expect an expiry failure.

No payment is collected. No account is created. No file is sent to a store, a processor, Shopify, Stripe, or a card network.

## Trust model

The signature covers the `payload` object. The `signature.public_key` field is a hint. It shows which key the signer put in the file.

A merchant authorizes the purchase only when the signature verifies against a public key the merchant already pinned. Pinning is an out-of-band decision: the merchant stores the key the first time they choose to trust that signer, and refuses a different key unless a person changes the pin on purpose. A key that arrives inside the same file does not authorize that file.

This matches the practical rule in the individual IETF draft for a signed marketplace catalogue (`draft-artamokhov-dawn-marketplace-discovery-03`): verify with the key you pinned, and do not treat a verified signature as proof of a legal identity. AgentProof uses a different signature profile. It is not that draft, and it is not an implementation of `/.well-known/agent-marketplace`.

What a passing check supports:

- The pinned key signed these exact purchase bytes.
- The total is within the signed cap, in one currency.
- The words recorded in the proof include that total and currency.
- The proof is inside its time window.
- The proof id is absent from the used-id list the merchant passed in.

What a passing check does not support:

- The display name is a real person, or the person controls the key.
- A bank, card network, or processor will accept the exhibit.
- The order was paid, shipped, or refunded.
- AgentProof operates a service that issued the proof.

## Authorization proof

Media type: `application/json`.

Top-level members:

| Member | Value |
| --- | --- |
| `proof_format` | `agentproof.authorization_proof` |
| `proof_format_version` | `0.1.0` |
| `signature_profile` | `agentproof-ed25519-jcs-0.1` |
| `payload` | The signed object, defined below |
| `signature` | `{ "algorithm": "ed25519", "public_key", "value" }` |

`public_key` is the raw 32-byte Ed25519 public key, base64url, no padding (43 characters). `value` is the raw 64-byte signature, base64url, no padding (86 characters).

The payload has no JSON numbers. Money and quantities are strings. Additional members are rejected.

Required payload members:

- `proof_id`: `ap_` plus 16 to 64 lowercase letters or digits. The merchant enforces single use locally. This host does not.
- `issued_at`, `expires_at`: UTC timestamps with milliseconds, such as `2026-11-07T20:00:00.000Z`. Lifetime is from 60 seconds through 7 days.
- `service_status`: `concept`.
- `format_status`: `beta`.
- `demo`: boolean. The demo always sets `true`.
- `agent.name` and `agent.reference`.
- `principal.display_name`.
- `principal.confirmation.confirmed_at`.
- `principal.confirmation.what_was_shown`: the words the person was shown. The purchase total and currency must appear in that string as their own tokens. `42.00` does not match inside `142.00`.
- `principal.confirmation.method`: `explicit_confirmation`.
- `merchant.name`, `merchant.reference`, and `merchant.platform`.
- `platform` is `unspecified`, `shopify`, or `stripe`. Those last two are labels a later exhibit might carry. They are not connections.
- `purchase.order_reference`, `purchase.summary`, `purchase.money`, and `purchase.items` (1 to 20 lines).
- `items[].money` is the line total, not a unit price. Line totals must add up to the purchase total.
- `constraints.max_amount`, `constraints.merchant_reference`, and `constraints.single_use` (`true`).

Amounts match `^(0|[1-9][0-9]{0,12})\.[0-9]{2}$`. The purchase total must be at least `0.01` and no higher than `max_amount`, in the same currency. Currency is three uppercase letters. The checker does not consult an ISO list.

Strings must not have leading or trailing whitespace, ASCII control characters, or raw line breaks. The exhibit statement is the one exception and may contain newlines.

## Signature profile `agentproof-ed25519-jcs-0.1`

Signed bytes: the UTF-8 encoding of the RFC 8785 canonicalization of `payload` only. The signature object is not covered, so a hint key can be inspected without changing the signature. In this profile the canonical document contains only objects, arrays, strings, booleans, and null. Numbers are an error, which avoids the JSON number rules in RFC 8785.

Object keys sort by UTF-16 code unit. Strings use ordinary JSON escaping. `/` is not escaped.

The verifier uses the platform Ed25519 implementation in Web Crypto and rejects keys and signatures of the wrong length before calling it. Callers should use a strict RFC 8032 implementation. A small-order or non-canonical signature that a permissive library might accept is outside this profile.

This profile is not `ed25519-pipe-2` from the marketplace-catalogue draft. The signed bytes, the canonicalization, and the base64 alphabet differ on purpose.

## Verification procedure

`verifyProof(proof, options)` returns a result. It does not throw for a bad proof. It throws if the options themselves are the wrong type.

Options:

| Option | Meaning |
| --- | --- |
| `now` | Clock for the time checks. Default is the current time. |
| `pinnedPublicKey` | Base64url Ed25519 public key the merchant pinned. |
| `merchantReference` | If set, must equal the merchant reference in the payload. |
| `consumedProofIds` | Proof ids this merchant has already decided. |
| `skewSeconds` | Future-issued tolerance. Default 120. Expiry is not extended. |
| `rejectDemo` | When true, `demo: true` fails. |

Checks, in order:

1. `shape`. Schema, then the string rules.
2. `times`. Lifetime, confirmation not after issuance (plus skew), issuance not in the future (plus skew), and `now` strictly before `expires_at`.
3. `confirmation_words`.
4. `amount_cap`.
5. `line_items`.
6. `merchant`.
7. `currency`.
8. `single_use`.
9. `demo_policy`.
10. `signature_pinned`. Required. Fails when no pinned key was provided.
11. `signature_embedded`. Not required. It reports whether the hint key matches.

`ok` and `authorized` are true only when every required check passed. `integrity_only` is true when the hint key matches and the pinned key does not. That result is not an authorization.

A shape failure stops the later checks. The result then has one check, `shape`.

## Order evidence record

`createEvidence` stores a decision for a proof that already verified (`verification.ok` must be true). `decision` is `accepted` or `rejected`. A refusal requires a note of 1 to 280 characters.

The record includes:

- `evidence_format`: `agentproof.order_evidence`, version `0.1.0`.
- `service_status`: `concept`. `format_status`: `beta`.
- `record_id`, `recorded_at`, `proof_id`.
- `proof_digest`: lowercase `sha256:` plus the SHA-256 hex of the canonical full proof, signature included.
- The embedded proof.
- The verification snapshot, including the pinned public key that was used.
- `exhibit.filed`: `false`. `exhibit.predicts_outcome`: `false`.
- A statement generated from the record. `checkEvidence` rebuilds that statement and compares it.

`undoEvidence` is allowed only from `accepted`. It sets `decision` to `undone` and adds `undo.undone_at`, `undo.reason`, and `undo.note`. The reason is one of `customer_requested`, `not_as_authorized`, `not_fulfilled`, or `merchant_declined`. The proof digest stays the same. A second undo fails.

`checkEvidence` confirms the schema, the digest, the cross-fields, the regenerated statement, and that the embedded signature still matches the pinned key stored on the record. Pass `pinnedPublicKey` from the merchant's own pin store. If it differs from the key on the record, the check fails.

Version 0.1.0 does not sign the evidence record. A person who can rewrite the merchant's storage can rewrite the record. The digest and the proof signature detect partial edits. They do not replace a system the merchant controls.

The statement is a draft exhibit. It says it was produced locally and has not been sent to a card network, a processor, Shopify, or Stripe.

## Run the checker

From a page on the same site:

```html
<script type="module">
  import { verifyProof } from "./verifier/agentproof.js";
  const result = await verifyProof(proof, {
    pinnedPublicKey: PINNED_KEY,
    merchantReference: "your-store-reference",
    consumedProofIds: alreadyDecided,
    rejectDemo: true
  });
</script>
```

Treat `result.ok` as the decision bit. Read `result.checks` for the list a person can review. With `rejectDemo: true`, fictional demo proofs fail `demo_policy`. They still carry `service_status: "concept"`.

Tests, from the repository root:

```sh
node --test agentproof/verifier/*.test.js
```

Node 22 or newer is required because the tests use the built-in Ed25519 Web Crypto implementation. No packages are installed.

## Demo

Open `agentproof/demo/` over HTTP. GitHub Pages is enough. A `file://` page will not load the module.

The demo asks for a display name, signs a 42.00 USD wool-blanket purchase, and pins the public key in that tab. The private key is not written to `localStorage`. The saved key is `il-agentproof-demo`, the same `il-` prefix as the other Interface Lab demos. Reset demo clears it.

The tamper controls are local:

- Change the total to 420.00 and keep the old signature.
- Re-sign the original purchase with a different key.
- Pretend the proof id is already on the used list.

Accept, refuse, and undo write the evidence record in the browser. Download and copy stay on the device.

## Related public work

These are separate efforts. AgentProof 0.1.0 does not implement them, is not endorsed by them, and does not send them traffic.

- **RiskBack** (riskback.com) offers merchants a decision on agent orders, an undo before delivery, dispute evidence handling, and a financial guarantee on orders it approved. This format is a local decide, undo, and draft exhibit. It has no guarantee and it files nothing.
- **Checkout Registry** (checkoutregistry.com) is a public directory of buy-side checkout APIs, with claims marked claimed, verified, failed, or unverifiable. AgentProof is not a directory and does not list providers.
- **Chargeflow** has published an agentic-commerce evidence playbook: keep the agent identity, the customer mandate, the cart that was approved, the notice, and the payment evidence. The evidence record here is a local mandate-and-cart exhibit. It does not submit a chargeback response, receive a network alert, or score an order.
- **`draft-artamokhov-dawn-marketplace-discovery-03`** defines `/.well-known/agent-marketplace`, a discovery document and a signed-catalogue profile. The pinning lesson is the same. The profile and the well-known URI are not.
- **Visa Intelligent Commerce / Trusted Agent Protocol** and **Mastercard Agent Pay** authenticate registered agents, often with HTTP message signatures and network-held keys, and they can carry payment credentials. This checker does not register agents and does not see card data.
- **Stripe and OpenAI's Agentic Commerce Protocol** defines checkout sessions, delegated payment, and order events. Shared payment tokens and delegated payment are how a purchase is actually charged. This repository does not create a checkout session or a payment token.

## Left for a later version

- A merchant signature on the evidence record, so accept and undo are tamper-evident outside the merchant's own database.
- A static merchant capability file: pinned-key location, accepted profile, and undo window. That is the discovery step, still short of a checkout directory.
- A published conformance suite and a second implementation, so a merchant can test a checker that is not this file.
