/**
 * AgentProof verifier, version 0.1.0.
 *
 * Beta format. The AgentProof service is a concept: this file does not
 * take payment, issue a live credential, or file a dispute.
 *
 * Signature profile agentproof-ed25519-jcs-0.1:
 * Ed25519 over the UTF-8 RFC 8785 canonicalization of `payload` only.
 * Numbers are rejected. Keys and signatures are base64url without padding.
 * A key inside the document is a hint. Authorization requires the merchant's
 * pinned public key.
 */

import proofSchema from "../schema/authorization-proof.schema.json" with { type: "json" };
import evidenceSchema from "../schema/order-evidence.schema.json" with { type: "json" };

export const PROOF_FORMAT = "agentproof.authorization_proof";
export const PROOF_FORMAT_VERSION = "0.1.0";
export const EVIDENCE_FORMAT = "agentproof.order_evidence";
export const EVIDENCE_FORMAT_VERSION = "0.1.0";
export const SIGNATURE_PROFILE = "agentproof-ed25519-jcs-0.1";
export const SERVICE_STATUS = "concept";
export const FORMAT_STATUS = "beta";
export const MAX_PROOF_LIFETIME_MS = 7 * 24 * 60 * 60 * 1000;
export const MIN_PROOF_LIFETIME_MS = 60 * 1000;
export const DEFAULT_SKEW_SECONDS = 120;
export const UNDO_REASONS = Object.freeze([
  "customer_requested",
  "not_as_authorized",
  "not_fulfilled",
  "merchant_declined",
]);

export { proofSchema, evidenceSchema };

const TEXT = new TextEncoder();
const DATE_TIME = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/;
const AMOUNT = /^(0|[1-9][0-9]{0,12})\.([0-9]{2})$/;
const CONTROL = /[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F\u2028\u2029]/;
const BREAKS = /[\n\t]/;

export function generateKeyPair() {
  return crypto.subtle.generateKey({ name: "Ed25519" }, true, ["sign", "verify"]);
}

export async function exportPublicKey(publicKey) {
  const jwk = await crypto.subtle.exportKey("jwk", publicKey);
  if (!jwk || jwk.kty !== "OKP" || jwk.crv !== "Ed25519" || typeof jwk.x !== "string") {
    throw new TypeError("Expected an Ed25519 public key.");
  }
  return jwk.x;
}

export function randomId(prefix) {
  const bytes = new Uint8Array(16);
  crypto.getRandomValues(bytes);
  let hex = "";
  for (const byte of bytes) hex += byte.toString(16).padStart(2, "0");
  return prefix + hex;
}

export function formatTime(value) {
  const date = value instanceof Date ? value : new Date(value);
  if (Number.isNaN(date.getTime())) throw new TypeError("Invalid time.");
  return date.toISOString();
}

export function buildPayload(input) {
  const currency = input.currency;
  const items = (input.items || []).map((item) => ({
    sku: item.sku,
    name: item.name,
    quantity: item.quantity,
    money: { amount: item.amount, currency: item.currency || currency },
  }));
  const payload = {
    proof_id: input.proofId,
    issued_at: input.issuedAt,
    expires_at: input.expiresAt,
    service_status: SERVICE_STATUS,
    format_status: FORMAT_STATUS,
    demo: input.demo !== false,
    agent: { name: input.agentName, reference: input.agentReference },
    principal: {
      display_name: input.displayName,
      confirmation: {
        confirmed_at: input.confirmedAt,
        what_was_shown: input.whatWasShown,
        method: "explicit_confirmation",
      },
    },
    merchant: {
      name: input.merchantName,
      reference: input.merchantReference,
      platform: input.platform || "unspecified",
    },
    purchase: {
      order_reference: input.orderReference,
      summary: input.summary,
      money: { amount: input.amount, currency },
      items,
    },
    constraints: {
      max_amount: { amount: input.maxAmount || input.amount, currency },
      merchant_reference: input.merchantReference,
      single_use: true,
    },
  };
  const errors = [
    ...validateDocument(payload, proofSchema.$defs.payload, proofSchema),
    ...stringProblems(payload),
  ];
  if (errors.length) throw new Error(errors.join(" "));
  return payload;
}

export async function signProof(payload, keyPair) {
  if (!keyPair?.publicKey || !keyPair?.privateKey) {
    throw new TypeError("An Ed25519 key pair is required.");
  }
  const errors = [
    ...validateDocument(payload, proofSchema.$defs.payload, proofSchema),
    ...stringProblems(payload),
  ];
  if (errors.length) throw new Error(errors.join(" "));
  const bytes = TEXT.encode(canonicalize(payload));
  const signature = new Uint8Array(
    await crypto.subtle.sign({ name: "Ed25519" }, keyPair.privateKey, bytes),
  );
  return {
    proof_format: PROOF_FORMAT,
    proof_format_version: PROOF_FORMAT_VERSION,
    signature_profile: SIGNATURE_PROFILE,
    payload: plain(payload),
    signature: {
      algorithm: "ed25519",
      public_key: await exportPublicKey(keyPair.publicKey),
      value: bytesToBase64Url(signature),
    },
  };
}

export async function verifyProof(proof, options = {}) {
  const doc = plain(proof);
  const skewMs = (options.skewSeconds ?? DEFAULT_SKEW_SECONDS) * 1000;
  if (!Number.isFinite(skewMs) || skewMs < 0) throw new TypeError("skewSeconds must be a non-negative number.");
  const now = options.now === undefined ? new Date() : new Date(options.now);
  if (Number.isNaN(now.getTime())) throw new TypeError("now is invalid.");
  const consumed = options.consumedProofIds ?? [];
  if (!Array.isArray(consumed) || consumed.some((id) => typeof id !== "string")) {
    throw new TypeError("consumedProofIds must be an array of strings.");
  }
  const pinned = options.pinnedPublicKey;
  if (pinned !== undefined && typeof pinned !== "string") throw new TypeError("pinnedPublicKey must be a string.");
  if (options.merchantReference !== undefined && typeof options.merchantReference !== "string") {
    throw new TypeError("merchantReference must be a string.");
  }

  const shapeErrors = [
    ...validateDocument(doc, proofSchema),
    ...stringProblems(doc),
  ];
  if (shapeErrors.length) {
    return finish(doc, [
      check("shape", false, true, trimDetail(shapeErrors.slice(0, 4).join(" "))),
    ], {});
  }

  const checks = [check("shape", true, true, "The document matches authorization proof 0.1.0.")];
  const payload = doc.payload;
  checks.push(timeCheck(payload, now.getTime(), skewMs));
  checks.push(wordsCheck(payload));
  checks.push(amountCheck(payload));
  checks.push(lineCheck(payload));
  checks.push(merchantCheck(payload, options.merchantReference));
  checks.push(currencyCheck(payload));
  checks.push(singleUseCheck(payload, consumed));
  checks.push(demoCheck(payload, options.rejectDemo === true));

  const signedBytes = TEXT.encode(canonicalize(payload));
  const embedded = await verifyRaw(doc.signature.public_key, signedBytes, doc.signature.value);
  const pinnedResult = pinned === undefined ? null : await verifyRaw(pinned, signedBytes, doc.signature.value);
  checks.push(pinnedCheck(pinned, pinnedResult));
  checks.push(embeddedCheck(embedded, pinnedResult));
  return finish(doc, checks, {
    embeddedMatched: embedded === true,
    pinnedMatched: pinnedResult === true,
  });
}

export async function proofDigest(proof) {
  const bytes = TEXT.encode(canonicalize(plain(proof)));
  const hash = await crypto.subtle.digest("SHA-256", bytes);
  return "sha256:" + [...new Uint8Array(hash)].map((byte) => byte.toString(16).padStart(2, "0")).join("");
}

export async function createEvidence(input) {
  const decision = input.decision;
  if (decision !== "accepted" && decision !== "rejected") {
    throw new TypeError("decision must be accepted or rejected.");
  }
  if (!input.verification || typeof input.verification.ok !== "boolean") {
    throw new TypeError("verification result is required.");
  }
  if (!input.verification.ok) {
    throw new Error("Refusing to store an evidence record when verification failed.");
  }
  if (typeof input.pinnedPublicKey !== "string") throw new TypeError("pinnedPublicKey is required.");
  const now = formatTime(input.now ?? new Date());
  const proof = plain(input.proof);
  const note = input.note ?? null;
  if (decision === "rejected") {
    assertNote(note, "A refusal note");
  } else if (note !== null) {
    throw new TypeError("An acceptance does not take a refusal note.");
  }
  const record = {
    evidence_format: EVIDENCE_FORMAT,
    evidence_format_version: EVIDENCE_FORMAT_VERSION,
    record_id: input.recordId || randomId("ev_"),
    recorded_at: now,
    service_status: SERVICE_STATUS,
    format_status: FORMAT_STATUS,
    demo: proof?.payload?.demo === true,
    decision,
    refusal_note: decision === "rejected" ? note : null,
    undo: null,
    verification: snapshot(input.verification, now, input.pinnedPublicKey),
    proof_id: proof?.payload?.proof_id,
    proof_digest: await proofDigest(proof),
    proof,
    exhibit: {
      title: "Draft dispute exhibit",
      filed: false,
      predicts_outcome: false,
      statement: "",
    },
  };
  record.exhibit.statement = exhibitStatement(record);
  await assertRecord(record);
  return record;
}

export async function undoEvidence(record, input) {
  const inspected = await checkEvidence(record, { pinnedPublicKey: input.pinnedPublicKey });
  if (!inspected.ok) throw new Error(inspected.reasons.join(" "));
  if (record.decision !== "accepted") throw new Error("Only an accepted record can be undone.");
  if (!UNDO_REASONS.includes(input.reason)) throw new TypeError("Unknown undo reason.");
  assertNote(input.note, "An undo note");
  const next = plain(record);
  next.decision = "undone";
  next.undo = {
    undone_at: formatTime(input.now ?? new Date()),
    reason: input.reason,
    note: input.note,
  };
  next.exhibit.statement = exhibitStatement(next);
  await assertRecord(next);
  if (next.proof_digest !== record.proof_digest) throw new Error("Undo changed the proof digest.");
  return next;
}

export async function checkEvidence(record, options = {}) {
  const doc = plain(record);
  const reasons = [];
  const schemaErrors = validateDocument(doc, evidenceSchema);
  if (schemaErrors.length) reasons.push(trimDetail(schemaErrors.slice(0, 4).join(" ")));
  else reasons.push(...stringProblems(doc));
  if (!reasons.length && doc.proof) {
    const proofErrors = [...validateDocument(doc.proof, proofSchema), ...stringProblems(doc.proof)];
    if (proofErrors.length) reasons.push(trimDetail(proofErrors.slice(0, 4).join(" ")));
  }
  if (!reasons.length) {
    const digest = await proofDigest(doc.proof);
    if (digest !== doc.proof_digest) reasons.push("The proof digest does not match the embedded proof.");
    if (doc.proof_id !== doc.proof?.payload?.proof_id) reasons.push("The record proof id does not match the embedded proof.");
    if (doc.demo !== doc.proof?.payload?.demo) reasons.push("The demo flag does not match the embedded proof.");
    if (doc.service_status !== doc.proof?.payload?.service_status) reasons.push("Service status does not match the embedded proof.");
    const statement = exhibitStatement(doc);
    if (doc.exhibit?.statement !== statement) reasons.push("The exhibit statement does not match the record.");
    if (doc.decision === "undone") {
      if (!doc.undo) reasons.push("An undone record needs an undo object.");
    } else if (doc.undo !== null) {
      reasons.push("Only an undone record has an undo object.");
    }
    if (doc.decision === "rejected" && typeof doc.refusal_note !== "string") reasons.push("A refused record needs a refusal note.");
    if (doc.decision !== "rejected" && doc.refusal_note !== null) reasons.push("Only a refused record has a refusal note.");
    if (doc.verification?.result !== "valid" || doc.verification?.pinned_key_matched !== true) {
      reasons.push("The record needs a verification that matched the pinned key.");
    }
    const signedBytes = doc.proof?.payload ? TEXT.encode(canonicalize(doc.proof.payload)) : null;
    const recordedKey = doc.verification?.pinned_public_key;
    const matched = signedBytes && recordedKey
      ? await verifyRaw(recordedKey, signedBytes, doc.proof.signature?.value)
      : false;
    if (matched !== true) reasons.push("The embedded proof signature does not match the public key stored on this record.");
    if (options.pinnedPublicKey !== undefined && options.pinnedPublicKey !== recordedKey) {
      reasons.push("The public key on this record is not the key this checker has pinned.");
    }
  }
  return { ok: reasons.length === 0, reasons };
}

export function exhibitStatement(record) {
  const payload = record.proof.payload;
  const items = payload.purchase.items
    .map((item) => `${item.name} × ${item.quantity}, line total ${item.money.amount} ${item.money.currency} (${item.sku})`)
    .join("; ");
  const decision = record.decision === "accepted"
    ? `Merchant decision: accepted at ${record.recorded_at}.`
    : record.decision === "rejected"
      ? `Merchant decision: refused at ${record.recorded_at}. Note: ${record.refusal_note}`
      : `Merchant decision: undone at ${record.undo.undone_at}. Reason: ${record.undo.reason}. Note: ${record.undo.note}`;
  return [
    "Draft dispute exhibit. This file was produced locally. It has not been sent to a card network, a processor, Shopify, or Stripe. It does not predict a dispute outcome.",
    `Service status: ${record.service_status}. Format status: ${record.format_status}. Demo data: ${record.demo ? "yes" : "no"}.`,
    `Proof id: ${record.proof_id}.`,
    `Person: ${payload.principal.display_name}.`,
    `Confirmed at ${payload.principal.confirmation.confirmed_at}. Words shown: "${payload.principal.confirmation.what_was_shown}"`,
    `Purchase: ${payload.purchase.summary}. Total: ${payload.purchase.money.amount} ${payload.purchase.money.currency}. Order reference: ${payload.purchase.order_reference}.`,
    `Items: ${items}.`,
    `Merchant: ${payload.merchant.name} (${payload.merchant.reference}). Platform label: ${payload.merchant.platform}.`,
    `Agent: ${payload.agent.name} (${payload.agent.reference}).`,
    `Pinned key matched at check time: ${record.verification.pinned_key_matched ? "yes" : "no"}.`,
    decision,
  ].join("\n");
}

export function canonicalize(value) {
  return encodeValue(value);
}

export function validateDocument(value, schema, root = schema) {
  const errors = [];
  visit(value, schema, root, "#", errors, 0);
  return errors;
}

function finish(doc, checks, flags) {
  const reasons = checks.filter((item) => item.required && !item.ok).map((item) => item.detail);
  const ok = reasons.length === 0;
  return {
    ok,
    authorized: ok,
    integrity_only: flags.embeddedMatched === true && flags.pinnedMatched !== true,
    demo: doc?.payload?.demo === true,
    proof_id: typeof doc?.payload?.proof_id === "string" ? doc.payload.proof_id : null,
    pinned_key_matched: flags.pinnedMatched === true,
    embedded_key_matched: flags.embeddedMatched === true,
    checks,
    reasons,
  };
}

function check(id, ok, required, detail) {
  return { id, ok, required, detail };
}

function timeCheck(payload, nowMs, skewMs) {
  const issued = Date.parse(payload.issued_at);
  const expires = Date.parse(payload.expires_at);
  const confirmed = Date.parse(payload.principal.confirmation.confirmed_at);
  const problems = [];
  const life = expires - issued;
  if (life < MIN_PROOF_LIFETIME_MS || life > MAX_PROOF_LIFETIME_MS) {
    problems.push("The proof lifetime must be from 60 seconds through 7 days.");
  }
  if (confirmed > issued + skewMs) problems.push("Confirmation is later than the proof was issued.");
  if (confirmed >= expires) problems.push("Confirmation is not inside the proof lifetime.");
  if (issued > nowMs + skewMs) problems.push("The proof is not valid yet.");
  if (nowMs >= expires) problems.push("The proof is expired.");
  return check(
    "times",
    problems.length === 0,
    true,
    problems.length ? problems.join(" ") : "Issued, confirmed, and expiry times are inside the window.",
  );
}

function wordsCheck(payload) {
  const words = payload.principal.confirmation.what_was_shown;
  const money = payload.purchase.money;
  const amountOk = containsToken(words, money.amount, /[0-9.]/);
  const currencyOk = containsToken(words, money.currency, /[A-Za-z]/);
  const ok = amountOk && currencyOk;
  return check(
    "confirmation_words",
    ok,
    true,
    ok
      ? "The words that were shown include the purchase total and currency."
      : "The words that were shown must include the purchase total and currency as separate tokens.",
  );
}

function amountCheck(payload) {
  const total = cents(payload.purchase.money.amount);
  const cap = cents(payload.constraints.max_amount.amount);
  const same = payload.purchase.money.currency === payload.constraints.max_amount.currency;
  const ok = same && total !== null && cap !== null && total >= 1 && total <= cap;
  return check(
    "amount_cap",
    ok,
    true,
    ok
      ? "The purchase total is within the signed cap."
      : "The purchase total must be at least 0.01 and no higher than the signed cap, in the same currency.",
  );
}

function lineCheck(payload) {
  let sum = 0;
  let ok = true;
  for (const item of payload.purchase.items) {
    const line = cents(item.money.amount);
    if (line === null || line < 1 || item.money.currency !== payload.purchase.money.currency) ok = false;
    else sum += line;
  }
  if (sum !== cents(payload.purchase.money.amount)) ok = false;
  return check(
    "line_items",
    ok,
    true,
    ok
      ? "Line totals add up to the purchase total."
      : "Each line total must use the purchase currency, and the lines must add up to the purchase total.",
  );
}

function merchantCheck(payload, expected) {
  const reference = payload.merchant.reference;
  const bound = payload.constraints.merchant_reference;
  const matchesOption = expected === undefined || expected === reference;
  const ok = reference === bound && matchesOption;
  return check(
    "merchant",
    ok,
    true,
    ok
      ? "The merchant reference matches the signed constraint."
      : "The merchant reference does not match the signed constraint or the reference this checker expected.",
  );
}

function currencyCheck(payload) {
  const code = payload.purchase.money.currency;
  const values = [
    payload.constraints.max_amount.currency,
    ...payload.purchase.items.map((item) => item.money.currency),
  ];
  const ok = values.every((value) => value === code);
  return check(
    "currency",
    ok,
    true,
    ok ? "Every amount uses the same currency." : "The purchase, the cap, and every line must use one currency.",
  );
}

function singleUseCheck(payload, consumed) {
  const used = consumed.includes(payload.proof_id);
  return check(
    "single_use",
    !used,
    true,
    used
      ? "This proof id is already in the merchant's local used list."
      : "This proof id is absent from the used list passed to the checker.",
  );
}

function demoCheck(payload, rejectDemo) {
  const refused = rejectDemo && payload.demo === true;
  return check(
    "demo_policy",
    !refused,
    true,
    refused
      ? "This checker is set to refuse demo proofs."
      : payload.demo
        ? "The proof is marked demo."
        : "The proof is not marked demo.",
  );
}

function pinnedCheck(pinned, pinnedResult) {
  if (pinned === undefined) {
    return check("signature_pinned", false, true, "No pinned public key was provided. A key inside the document does not authorize the purchase.");
  }
  if (pinnedResult === "bad-key") {
    return check("signature_pinned", false, true, "The pinned public key is not a 32-byte Ed25519 key.");
  }
  if (pinnedResult !== true) {
    return check("signature_pinned", false, true, "The signature does not match the pinned public key.");
  }
  return check("signature_pinned", true, true, "The signature matches the pinned public key.");
}

function embeddedCheck(embedded, pinnedResult) {
  const ok = embedded === true;
  let detail = ok
    ? "The signature matches the key published inside the document."
    : "The signature does not match the key published inside the document.";
  if (ok && pinnedResult === false) {
    detail = "The signature matches the key inside the document, and that key is not the pinned key.";
  }
  return check("signature_embedded", ok, false, detail);
}

async function verifyRaw(publicKey, bytes, signature) {
  const rawKey = base64UrlToBytes(publicKey);
  const rawSig = base64UrlToBytes(signature);
  if (!rawKey || rawKey.length !== 32) return "bad-key";
  if (!rawSig || rawSig.length !== 64) return "bad-sig";
  try {
    const key = await crypto.subtle.importKey(
      "raw",
      rawKey,
      { name: "Ed25519" },
      false,
      ["verify"],
    );
    return await crypto.subtle.verify({ name: "Ed25519" }, key, rawSig, bytes);
  } catch {
    return "bad-key";
  }
}

function snapshot(verification, checkedAt, pinnedPublicKey) {
  return {
    checked_at: checkedAt,
    result: verification.ok ? "valid" : "invalid",
    pinned_public_key: pinnedPublicKey,
    pinned_key_matched: verification.pinned_key_matched === true,
    embedded_key_matched: verification.embedded_key_matched === true,
    checks: verification.checks.map((item) => ({
      id: item.id,
      ok: item.ok,
      required: item.required,
      detail: item.detail,
    })),
    reasons: verification.reasons.slice(),
  };
}

function assertNote(note, label) {
  if (typeof note !== "string" || note.length < 1 || note.length > 280 || note !== note.trim() || CONTROL.test(note) || BREAKS.test(note)) {
    throw new TypeError(`${label} must be 1 to 280 characters, without surrounding whitespace or control characters.`);
  }
}

async function assertRecord(record) {
  const errors = validateDocument(record, evidenceSchema);
  if (errors.length) throw new Error(`Evidence record failed its schema: ${errors.join(" ")}`);
  const inspected = await checkEvidence(record);
  if (!inspected.ok) throw new Error(`Evidence record is inconsistent: ${inspected.reasons.join(" ")}`);
}

function cents(amount) {
  const match = AMOUNT.exec(amount);
  if (!match) return null;
  return Number(match[1]) * 100 + Number(match[2]);
}

function containsToken(text, token, neighbor) {
  let from = 0;
  while (from <= text.length) {
    const at = text.indexOf(token, from);
    if (at < 0) return false;
    const before = at === 0 ? "" : text[at - 1];
    const after = text[at + token.length] ?? "";
    if (!neighbor.test(before) && !neighbor.test(after)) return true;
    from = at + 1;
  }
  return false;
}

function trimDetail(text) {
  return text.length > 400 ? `${text.slice(0, 397)}...` : text;
}

function stringProblems(value, path = "#", out = []) {
  if (typeof value === "string") {
    if (value !== value.trim() || CONTROL.test(value)) out.push(`${path} has surrounding whitespace or a control character`);
    if (BREAKS.test(value) && path !== "#/exhibit/statement") out.push(`${path} contains a line break`);
    return out;
  }
  if (Array.isArray(value)) {
    value.forEach((item, index) => stringProblems(item, `${path}/${index}`, out));
    return out;
  }
  if (value && typeof value === "object") {
    for (const key of Object.keys(value)) stringProblems(value[key], `${path}/${escapePath(key)}`, out);
  }
  return out;
}

function encodeValue(value) {
  if (value === null) return "null";
  if (typeof value === "string") return JSON.stringify(value);
  if (typeof value === "boolean") return value ? "true" : "false";
  if (typeof value === "number") throw new TypeError("Numbers are not allowed in this signature profile.");
  if (Array.isArray(value)) return `[${value.map((item) => encodeValue(item)).join(",")}]`;
  if (typeof value === "object") {
    const proto = Object.getPrototypeOf(value);
    if (proto !== Object.prototype && proto !== null) throw new TypeError("Only plain objects can be canonicalized.");
    const keys = Object.keys(value).sort(compareUtf16);
    return `{${keys.map((key) => `${JSON.stringify(key)}:${encodeValue(value[key])}`).join(",")}}`;
  }
  throw new TypeError("This value cannot be canonicalized.");
}

function compareUtf16(left, right) {
  if (left < right) return -1;
  if (left > right) return 1;
  return 0;
}

function plain(value) {
  if (Array.isArray(value)) return value.map((item) => plain(item));
  if (value && typeof value === "object") {
    const copy = Object.create(null);
    for (const key of Object.keys(value)) copy[key] = plain(value[key]);
    return copy;
  }
  return value;
}

function bytesToBase64Url(bytes) {
  let binary = "";
  for (const byte of bytes) binary += String.fromCharCode(byte);
  return btoa(binary).replaceAll("+", "-").replaceAll("/", "_").replace(/=+$/u, "");
}

function base64UrlToBytes(value) {
  if (typeof value !== "string" || !/^[A-Za-z0-9_-]+$/u.test(value)) return null;
  const padded = value + "=".repeat((4 - (value.length % 4)) % 4);
  try {
    const binary = atob(padded.replaceAll("-", "+").replaceAll("_", "/"));
    const bytes = new Uint8Array(binary.length);
    for (let index = 0; index < binary.length; index += 1) bytes[index] = binary.charCodeAt(index);
    return bytes;
  } catch {
    return null;
  }
}

function visit(value, schema, root, path, errors, depth) {
  if (depth > 32) {
    errors.push(`${path} schema is too deep`);
    return;
  }
  if (schema.$ref) {
    visit(value, resolveRef(schema.$ref, root), root, path, errors, depth + 1);
    return;
  }
  if (schema.anyOf) {
    const group = schema.anyOf.map(() => []);
    schema.anyOf.forEach((option, index) => visit(value, option, root, path, group[index], depth + 1));
    if (group.some((item) => item.length === 0)) return;
    const best = group.reduce((left, right) => (right.length < left.length ? right : left));
    errors.push(...best);
    return;
  }
  if (schema.type) {
    if (!typeOk(value, schema.type)) {
      errors.push(`${path} must be ${schema.type}`);
      return;
    }
  }
  if (Object.hasOwn(schema, "const") && !same(value, schema.const)) {
    errors.push(`${path} must be ${JSON.stringify(schema.const)}`);
    return;
  }
  if (schema.enum && !schema.enum.some((item) => same(value, item))) {
    errors.push(`${path} must be one of ${schema.enum.map((item) => JSON.stringify(item)).join(", ")}`);
    return;
  }
  if (typeof value === "string") {
    if (schema.minLength !== undefined && value.length < schema.minLength) errors.push(`${path} is too short`);
    if (schema.maxLength !== undefined && value.length > schema.maxLength) errors.push(`${path} is too long`);
    if (schema.pattern && !new RegExp(schema.pattern, "u").test(value)) errors.push(`${path} does not match ${schema.pattern}`);
    if (schema.format === "date-time" && !isDateTime(value)) errors.push(`${path} must be a UTC timestamp with milliseconds`);
  }
  if (Array.isArray(value)) {
    if (schema.minItems !== undefined && value.length < schema.minItems) errors.push(`${path} has too few items`);
    if (schema.maxItems !== undefined && value.length > schema.maxItems) errors.push(`${path} has too many items`);
    if (schema.items) value.forEach((item, index) => visit(item, schema.items, root, `${path}/${index}`, errors, depth + 1));
  }
  if (isObject(value) && schema.properties) {
    const known = new Set(Object.keys(schema.properties));
    if (schema.required) {
      for (const key of schema.required) {
        if (!Object.hasOwn(value, key)) errors.push(`${path}/${escapePath(key)} is required`);
      }
    }
    if (schema.additionalProperties === false) {
      for (const key of Object.keys(value)) {
        if (!known.has(key)) errors.push(`${path}/${escapePath(key)} is not allowed`);
      }
    }
    for (const key of Object.keys(schema.properties)) {
      if (Object.hasOwn(value, key)) visit(value[key], schema.properties[key], root, `${path}/${escapePath(key)}`, errors, depth + 1);
    }
  }
}

function resolveRef(ref, root) {
  if (!ref.startsWith("#/$defs/")) throw new Error(`Unsupported schema reference ${ref}`);
  let node = root;
  for (const part of ref.slice(2).split("/")) {
    node = node?.[part];
  }
  if (!node) throw new Error(`Missing schema reference ${ref}`);
  return node;
}

function typeOk(value, type) {
  if (type === "object") return isObject(value);
  if (type === "array") return Array.isArray(value);
  if (type === "string") return typeof value === "string";
  if (type === "boolean") return typeof value === "boolean";
  if (type === "null") return value === null;
  throw new Error(`Unsupported schema type ${type}`);
}

function isObject(value) {
  return Boolean(value) && typeof value === "object" && !Array.isArray(value);
}

function isDateTime(value) {
  if (!DATE_TIME.test(value)) return false;
  const parsed = Date.parse(value);
  return !Number.isNaN(parsed) && new Date(parsed).toISOString() === value;
}

function same(left, right) {
  return JSON.stringify(left) === JSON.stringify(right);
}

function escapePath(key) {
  return key.replaceAll("~", "~0").replaceAll("/", "~1");
}
