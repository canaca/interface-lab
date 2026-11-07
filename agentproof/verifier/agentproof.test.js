import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

import {
  FORMAT_STATUS,
  SERVICE_STATUS,
  SIGNATURE_PROFILE,
  buildPayload,
  canonicalize,
  checkEvidence,
  createEvidence,
  evidenceSchema,
  exhibitStatement,
  exportPublicKey,
  generateKeyPair,
  proofDigest,
  proofSchema,
  signProof,
  undoEvidence,
  verifyProof,
} from "./agentproof.js";

const ISSUED = "2026-11-07T20:00:00.000Z";
const EXPIRES = "2026-11-07T20:15:00.000Z";
const NOW = "2026-11-07T20:01:00.000Z";
const WORDS = "Buy 1 wool blanket for 42.00 USD from Northwind Goods?";

function fields(overrides = {}) {
  return {
    proofId: `ap_${"a".repeat(32)}`,
    issuedAt: ISSUED,
    expiresAt: EXPIRES,
    confirmedAt: ISSUED,
    agentName: "Harbor Shopping Agent",
    agentReference: "agent_demo_harbor",
    displayName: "Alex Rivera",
    whatWasShown: WORDS,
    merchantName: "Northwind Goods",
    merchantReference: "shop_demo_northwind",
    platform: "unspecified",
    orderReference: "ord_demo_blanket",
    summary: "One wool blanket",
    amount: "42.00",
    currency: "USD",
    items: [{ sku: "BLANKET-WOOL", name: "Wool blanket", quantity: "1", amount: "42.00" }],
    ...overrides,
  };
}

async function minted(overrides = {}, keyPair = null) {
  const pair = keyPair ?? await generateKeyPair();
  const payload = buildPayload(fields(overrides));
  const proof = await signProof(payload, pair);
  return { pair, proof, publicKey: await exportPublicKey(pair.publicKey), payload };
}

function verify(proof, publicKey, options = {}) {
  return verifyProof(proof, {
    now: NOW,
    pinnedPublicKey: publicKey,
    merchantReference: "shop_demo_northwind",
    ...options,
  });
}

test("canonical form sorts keys, escapes strings, and rejects numbers", () => {
  assert.equal(canonicalize({ b: "x", a: "y" }), '{"a":"y","b":"x"}');
  assert.equal(canonicalize({ "a/b": "q\"\n\u0000\u20ac" }), '{"a/b":"q\\"\\n\\u0000€"}');
  assert.equal(canonicalize(["b", { z: true, a: null }]), '["b",{"a":null,"z":true}]');
  assert.throws(() => canonicalize({ n: 1 }), /Numbers are not allowed/);
  assert.throws(() => canonicalize(undefined), /cannot be canonicalized/);
});

test("a signed proof verifies only against the pinned key", async () => {
  const { proof, publicKey } = await minted();
  const result = await verify(proof, publicKey);
  assert.equal(result.ok, true);
  assert.equal(result.authorized, true);
  assert.equal(result.integrity_only, false);
  assert.equal(result.demo, true);
  assert.equal(result.pinned_key_matched, true);
  assert.equal(result.embedded_key_matched, true);
  assert.equal(result.reasons.length, 0);
  assert.equal(proof.payload.service_status, SERVICE_STATUS);
  assert.equal(proof.payload.format_status, FORMAT_STATUS);
  assert.equal(proof.signature_profile, SIGNATURE_PROFILE);
  assert.ok(result.checks.every((item) => item.ok));
});

test("the key inside the document does not authorize a purchase", async () => {
  const { proof } = await minted();
  const result = await verifyProof(proof, { now: NOW, merchantReference: "shop_demo_northwind" });
  assert.equal(result.ok, false);
  assert.equal(result.authorized, false);
  assert.equal(result.integrity_only, true);
  assert.equal(result.embedded_key_matched, true);
  assert.equal(checkById(result, "signature_pinned").ok, false);
});

test("a different signer fails the pinned key and still shows integrity only", async () => {
  const first = await minted();
  const second = await generateKeyPair();
  const resigned = await signProof(first.payload, second);
  const result = await verify(resigned, first.publicKey);
  assert.equal(result.ok, false);
  assert.equal(result.integrity_only, true);
  assert.equal(result.embedded_key_matched, true);
  assert.equal(result.pinned_key_matched, false);
  assert.match(checkById(result, "signature_embedded").detail, /not the pinned key/);
});

test("editing the amount without re-signing fails the signature and the cap", async () => {
  const { proof, publicKey } = await minted();
  const tampered = structuredClone(proof);
  tampered.payload.purchase.money.amount = "420.00";
  tampered.payload.purchase.items[0].money.amount = "420.00";
  const result = await verify(tampered, publicKey);
  assert.equal(result.ok, false);
  assert.equal(result.integrity_only, false);
  assert.equal(checkById(result, "signature_pinned").ok, false);
  assert.equal(checkById(result, "amount_cap").ok, false);
  assert.equal(checkById(result, "confirmation_words").ok, false);
  assert.equal(checkById(result, "line_items").ok, true);
});

test("a re-signed higher amount is a different authorization", async () => {
  const { pair, publicKey } = await minted();
  const raised = buildPayload(fields({
    amount: "420.00",
    maxAmount: "42.00",
    whatWasShown: "Buy 1 wool blanket for 420.00 USD from Northwind Goods?",
    items: [{ sku: "BLANKET-WOOL", name: "Wool blanket", quantity: "1", amount: "420.00" }],
  }));
  const proof = await signProof(raised, pair);
  const result = await verify(proof, publicKey);
  assert.equal(result.pinned_key_matched, true);
  assert.equal(result.ok, false);
  assert.equal(checkById(result, "amount_cap").ok, false);
});

test("time window, confirmation text, merchant, currency, and single use are enforced", async () => {
  const { pair, publicKey } = await minted();

  const expired = await signProof(buildPayload(fields({
    issuedAt: "2026-11-07T18:00:00.000Z",
    confirmedAt: "2026-11-07T18:00:00.000Z",
    expiresAt: "2026-11-07T18:15:00.000Z",
  })), pair);
  assert.match((await verify(expired, publicKey)).reasons.join(" "), /expired/);

  const early = await signProof(buildPayload(fields({
    issuedAt: "2026-11-07T20:10:00.000Z",
    confirmedAt: "2026-11-07T20:10:00.000Z",
    expiresAt: "2026-11-07T22:00:00.000Z",
  })), pair);
  assert.match((await verify(early, publicKey)).reasons.join(" "), /not valid yet/);

  const skewOk = await signProof(buildPayload(fields({
    issuedAt: "2026-11-07T20:02:00.000Z",
    confirmedAt: "2026-11-07T20:02:00.000Z",
    expiresAt: "2026-11-07T20:30:00.000Z",
  })), pair);
  assert.equal((await verify(skewOk, publicKey)).ok, true);

  const longLife = await signProof(buildPayload(fields({
    expiresAt: "2026-11-15T20:00:00.001Z",
  })), pair);
  assert.match((await verify(longLife, publicKey)).reasons.join(" "), /lifetime/);

  const hiddenAmount = await signProof(buildPayload(fields({
    whatWasShown: "Buy 1 wool blanket for 142.00 USD from Northwind Goods?",
  })), pair);
  assert.equal(checkById(await verify(hiddenAmount, publicKey), "confirmation_words").ok, false);

  const otherStore = await signProof(buildPayload(fields({
    merchantReference: "shop_demo_other",
    whatWasShown: WORDS,
  })), pair);
  const other = await verify(otherStore, publicKey);
  assert.equal(checkById(other, "merchant").ok, false);

  const euro = await signProof(buildPayload(fields({
    currency: "EUR",
    whatWasShown: "Buy 1 wool blanket for 42.00 EUR from Northwind Goods?",
    items: [{ sku: "BLANKET-WOOL", name: "Wool blanket", quantity: "1", amount: "42.00", currency: "USD" }],
  })), pair);
  assert.equal(checkById(await verify(euro, publicKey), "currency").ok, false);

  const once = await minted();
  const replay = await verify(once.proof, once.publicKey, { consumedProofIds: [once.proof.payload.proof_id] });
  assert.equal(checkById(replay, "single_use").ok, false);
});

test("demo proofs can be refused by a merchant checker", async () => {
  const { proof, publicKey } = await minted();
  const refused = await verify(proof, publicKey, { rejectDemo: true });
  assert.equal(checkById(refused, "demo_policy").ok, false);
  const live = await minted({ demo: false });
  const accepted = await verify(live.proof, live.publicKey, { rejectDemo: true });
  assert.equal(accepted.ok, true);
  assert.equal(accepted.demo, false);
});

test("schema failures stop verification before a signature is treated as authorization", async () => {
  const { proof, publicKey } = await minted();
  for (const key of proofSchema.$defs.payload.required) {
    const broken = structuredClone(proof);
    delete broken.payload[key];
    const result = await verify(broken, publicKey);
    assert.equal(result.ok, false);
    assert.equal(result.checks.length, 1);
    assert.equal(result.checks[0].id, "shape");
  }
  const extra = structuredClone(proof);
  extra.payload.note = "extra";
  assert.equal((await verify(extra, publicKey)).checks[0].id, "shape");
  const padded = structuredClone(proof);
  padded.payload.principal.display_name = " Alex ";
  assert.match((await verify(padded, publicKey)).reasons.join(" "), /whitespace/);
});

test("verification does not mutate the proof", async () => {
  const { proof, publicKey } = await minted();
  const before = canonicalize(proof);
  await verify(proof, publicKey);
  assert.equal(canonicalize(proof), before);
});

test("acceptance, refusal, and undo produce a consistent evidence record", async () => {
  const { proof, publicKey } = await minted();
  const verification = await verify(proof, publicKey);
  await assert.rejects(
    () => createEvidence({ proof, verification: { ...verification, ok: false }, decision: "accepted", pinnedPublicKey: publicKey, now: NOW }),
    /verification failed/,
  );

  const accepted = await createEvidence({
    proof,
    verification,
    decision: "accepted",
    pinnedPublicKey: publicKey,
    now: NOW,
    recordId: `ev_${"b".repeat(32)}`,
  });
  assert.equal(accepted.decision, "accepted");
  assert.equal(accepted.undo, null);
  assert.equal(accepted.exhibit.filed, false);
  assert.equal(accepted.exhibit.predicts_outcome, false);
  assert.match(accepted.exhibit.statement, /has not been sent/);
  assert.match(accepted.exhibit.statement, /42\.00 USD/);
  assert.match(accepted.exhibit.statement, /Service status: concept/);
  assert.equal((await checkEvidence(accepted, { pinnedPublicKey: publicKey })).ok, true);
  assert.equal(evidenceSchema.properties.service_status.const, "concept");
  assert.equal(await proofDigest(accepted.proof), accepted.proof_digest);

  const refused = await createEvidence({
    proof,
    verification,
    decision: "rejected",
    note: "Out of stock in the fictional shop.",
    pinnedPublicKey: publicKey,
    now: NOW,
  });
  assert.match(refused.exhibit.statement, /refused/);
  assert.equal((await checkEvidence(refused)).ok, true);

  const undone = await undoEvidence(accepted, {
    reason: "customer_requested",
    note: "Alex asked to cancel before fulfillment.",
    now: "2026-11-07T20:05:00.000Z",
    pinnedPublicKey: publicKey,
  });
  assert.equal(undone.decision, "undone");
  assert.equal(undone.proof_digest, accepted.proof_digest);
  assert.equal(undone.recorded_at, accepted.recorded_at);
  assert.match(undone.exhibit.statement, /undone at 2026-11-07T20:05:00.000Z/);
  assert.match(exhibitStatement(undone), /customer_requested/);
  assert.equal((await checkEvidence(undone, { pinnedPublicKey: "A".repeat(43) })).ok, false);

  const edited = structuredClone(undone);
  edited.proof.payload.purchase.money.amount = "42.01";
  edited.proof_digest = await proofDigest(edited.proof);
  edited.exhibit.statement = exhibitStatement(edited);
  assert.match((await checkEvidence(edited, { pinnedPublicKey: publicKey })).reasons.join(" "), /signature/);

  await assert.rejects(
    () => undoEvidence(undone, { reason: "customer_requested", note: "Again.", now: NOW, pinnedPublicKey: publicKey }),
    /accepted/,
  );
  await assert.rejects(
    () => undoEvidence(accepted, { reason: "nope", note: "No.", now: NOW, pinnedPublicKey: publicKey }),
    /Unknown undo reason/,
  );
});

test("the published wool-blanket vector verifies inside its original window", async () => {
  const proof = JSON.parse(readFileSync(new URL("../fixtures/wool-blanket.proof.json", import.meta.url), "utf8"));
  const canonical = readFileSync(new URL("../fixtures/wool-blanket.canonical.txt", import.meta.url), "utf8");
  const evidence = JSON.parse(readFileSync(new URL("../fixtures/wool-blanket.evidence.json", import.meta.url), "utf8"));
  assert.equal(canonicalize(proof.payload), canonical);
  const result = await verifyProof(proof, {
    now: "2026-11-07T20:01:00.000Z",
    pinnedPublicKey: proof.signature.public_key,
    merchantReference: "shop_demo_northwind",
  });
  assert.equal(result.ok, true);
  assert.equal(await proofDigest(proof), evidence.proof_digest);
  assert.equal((await checkEvidence(evidence, { pinnedPublicKey: proof.signature.public_key })).ok, true);
  const later = await verifyProof(proof, {
    now: "2026-11-08T20:01:00.000Z",
    pinnedPublicKey: proof.signature.public_key,
  });
  assert.match(later.reasons.join(" "), /expired/);
});

function checkById(result, id) {
  const found = result.checks.find((item) => item.id === id);
  assert.ok(found, id);
  return found;
}
