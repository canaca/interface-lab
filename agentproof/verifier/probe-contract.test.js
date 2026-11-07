import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

const root = new URL("../", import.meta.url);

function read(path) {
  return readFileSync(new URL(path, root), "utf8");
}

test("the daily probe's six files keep their contract", () => {
  assert.equal(read("status.json"), '{"status":"concept","accepting":"waitlist"}\n');

  const index = read("index.html");
  for (const href of ["llms.txt", "openapi.json", ".well-known/agent.json", "mcp.json", "status.json"]) {
    assert.ok(index.includes(`href="${href}"`), href);
  }
  assert.match(index, /Concept \/ early access, not a live service/);
  assert.match(index, /Working beta pieces/);
  assert.match(index, /href="demo\/"/);

  const openapi = JSON.parse(read("openapi.json"));
  assert.equal(typeof openapi.openapi, "string");
  assert.ok(openapi.openapi.startsWith("3.1"));
  assert.equal(openapi["x-status"], "concept");
  const posts = Object.entries(openapi.paths).filter(([, ops]) => ops && typeof ops.post === "object");
  assert.ok(posts.length >= 1);

  for (const file of [".well-known/agent.json", "mcp.json"]) {
    const doc = JSON.parse(read(file));
    assert.equal(doc["x-status"], "concept");
  }

  assert.match(read("llms.txt"), /\{"status":"concept","accepting":"waitlist"\}/);
});

test("the demo stays fictional and does not call a payment host", () => {
  const demo = read("demo/index.html");
  assert.match(demo, /from "\.\.\/verifier\/agentproof\.js"/);
  assert.match(demo, /fictional/i);
  assert.match(demo, /concept service/i);
  assert.match(demo, /No payment is collected/);
  assert.match(demo, /No dispute is filed/);
  assert.doesNotMatch(demo, /js\.stripe\.com|checkout\.stripe|paypal\.com|buy\.stripe/i);
  assert.match(read("SPEC.md"), /Service status: concept/);
  assert.match(read("SPEC.md"), /Format status: beta/);
});
