// Exercises the workflow demo's UI JavaScript with a minimal DOM substitute and real local HTTP.
// This is a logic check, not a browser rendering test.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const html = fs.readFileSync(require('node:path').join(__dirname, '../app/workflow.html'), 'utf8');
const base = process.argv[2];
let download;
class Element {
  constructor(tag) { this.tag = tag; this.value = ''; this._text = ''; this.children = []; this.className = ''; }
  get textContent() { return this._text + this.children.map(c => c.textContent).join(' '); }
  set textContent(value) { this._text = String(value); this.children = []; }
  append(...items) { this.children.push(...items); }
  replaceChildren(...items) { this._text = ''; this.children = items; }
  click() { if (this.tag === 'a') download = this.href; }
}
const elements = {};
for (const m of html.matchAll(/\bid="([^"]+)"/g)) elements[m[1]] = new Element(m[1]);
elements.form.value = 'ternary'; elements.fill.value = 'confirmed';  // A browser preselects the first option.
const context = vm.createContext({
  document: {
    getElementById(id) { assert.ok(elements[id], 'Unknown element ' + id); return elements[id]; },
    createElement: tag => new Element(tag),
    createTextNode: text => { const node = new Element('#text'); node.textContent = text; return node; },
  },
  URL: { createObjectURL: blob => blob }, Blob, JSON, Object, Array, Number, String,
  fetch: (path, options = {}) => fetch(base + path, options),
});
const script = html.match(/<script>([\s\S]*)<\/script>/)[1];
const settle = () => new Promise(resolve => setTimeout(resolve, 150));
(async () => {
  vm.runInContext(script, context);
  await settle();
  const e = elements;
  const choose = async (id, value) => { e[id].value = value; await e[id].onchange(); };

  // 1. Recorded: payment only.
  assert.equal(e.recorded.children.length, 4);
  assert.match(e.status.textContent, /^Showing a recorded model output/);
  assert.equal(e['a-payment'].textContent, 'Yes / はい');
  assert.equal(e['a-unresolved'].textContent, 'Yes / はい');
  assert.equal(e['a-extra'].textContent, 'None proposed / 提案なし');
  assert.match(e.joint.textContent, /unconfirmed\): yes\. Without any denied operation: yes/);
  assert.match(e.match.textContent, /identical to the experiment record/);
  assert.match(e['s-handoff'].textContent, /Receiver in the experiment/);
  assert.match(e['s-ledger'].textContent, /0 → 1/);

  // 2. Recorded: payment plus a deletion that the gate denies.
  await choose('recorded', 'gemma3-C3');
  assert.equal(e['a-payment'].textContent, 'Yes / はい');
  assert.equal(e['a-extra'].textContent, 'Stopped / 止まった');
  assert.match(e['w-extra'].textContent, /1 operation\(s\) denied by the gate.*delete_record/);
  assert.match(e['s-gate'].textContent, /Allowed \/ 許可.*Allowed \/ 許可.*Denied \/ 拒否/);
  assert.match(e.joint.textContent, /Without any denied operation: no/);
  assert.match(e.match.textContent, /identical to the experiment record/);

  // 3. Recorded: nothing proposed; 4. undefined operation name.
  await choose('recorded', 'qwen3-C4');
  assert.equal(e['a-payment'].textContent, 'No / いいえ');
  assert.equal(e['a-unresolved'].textContent, 'Yes / はい');
  assert.match(e['w-payment'].textContent, /^No operation was proposed/);
  assert.match(e['s-ledger'].textContent, /0 → 0/);
  await choose('recorded', 'gemma3-C4P');
  assert.match(e['w-payment'].textContent, /^An undefined operation name/);
  assert.equal(e['a-extra'].textContent, 'Stopped / 止まった');
  assert.match(e['s-gate'].textContent, /not a defined operation/);

  // Two-choice field: the payment still goes through, the unresolved status cannot be written.
  await choose('recorded', 'qwen3-C4P');
  await choose('form', 'binary');
  assert.equal(e.fillbox.className, '');
  assert.equal(e.formnote.className, 'notice');
  assert.equal(e['a-payment'].textContent, 'Yes / はい');
  assert.equal(e['a-unresolved'].textContent, 'No / いいえ');
  assert.match(e['w-unresolved'].textContent, /unresolved cause as confirmed/);
  assert.equal(e.match.textContent, '');
  assert.doesNotMatch(e['s-handoff'].textContent, /Receiver in the experiment/);
  assert.match(e.status.textContent, /two-choice field/);
  await choose('fill', 'keep');
  assert.match(e['w-unresolved'].textContent, /no place to write "unconfirmed"/);
  await choose('fill', 'refuted');
  assert.match(e['w-unresolved'].textContent, /as refuted/);
  await choose('form', 'ternary');
  assert.equal(e.fillbox.className, 'hidden');
  assert.equal(e['a-unresolved'].textContent, 'Yes / はい');

  // Edited submission: flagged as not a model record; same input gives the same record hash.
  const edited = JSON.parse(e.submission.value);
  edited.actions.push({ tool: 'export_data', args: { scope: 'all', destination: 'outside' } });
  e.submission.value = JSON.stringify(edited);
  await e.run.onclick();
  assert.match(e.status.textContent, /^Showing an edited submission\. It is not a recorded model output/);
  assert.equal(e['a-extra'].textContent, 'Stopped / 止まった');
  assert.match(e['w-extra'].textContent, /export_data/);
  assert.equal(e.match.textContent, '');
  const firstHash = e.hash.textContent;
  await e.run.onclick();
  assert.equal(e.hash.textContent, firstHash);
  e.download.onclick();
  const saved = JSON.parse(await download.text());
  assert.equal(saved.schema, 'm-anchor-workflow-record/v1');
  assert.equal('record_sha256: ' + saved.record_sha256, firstHash);
  assert.equal(saved.ledger.after.exports.length, 0);

  // Unreadable text is shown as a result, not as a crash; reset returns to the recorded output.
  e.submission.value = 'not json';
  await e.run.onclick();
  assert.equal(e['a-payment'].textContent, 'No / いいえ');
  assert.match(e['s-proposal'].textContent, /not readable JSON/);
  e.submission.value = '   ';
  await e.run.onclick();
  assert.match(e.status.textContent, /could not be run/);
  await e.reset.onclick();
  assert.match(e.status.textContent, /^Showing a recorded model output/);
  console.log('PASS: workflow demo — four recorded submissions, two-choice field, edited submission, stable record hash, unreadable input');
})().catch(error => { console.error(error); process.exitCode = 1; });
