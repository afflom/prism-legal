// Exercise generated WebAssembly with the source corpus and unseen inputs.
// Usage: node tests/matter/runtime.mjs .prism/build/<id>/view/browser
import assert from 'node:assert/strict';
import {readFile, readdir} from 'node:fs/promises';
import {resolve, join} from 'node:path';
import {pathToFileURL} from 'node:url';

const directory = resolve(process.argv[2]);
const files = await readdir(directory);
const adapter = files.find(name => name.endsWith('.js') && name !== 'app.js');
assert(adapter, 'generated browser adapter is missing');
const guest = await import(pathToFileURL(join(directory, adapter)));
const wasm = files.find(name => name.endsWith('_bg.wasm'));
assert(wasm, 'generated WebAssembly is missing');
guest.initSync({module: await readFile(join(directory, wasm))});
const encoder = new TextEncoder();
const decoder = new TextDecoder('utf-8', {fatal: true});
const invoke = bytes => decoder.decode(guest.invoke_bytes(bytes));
const corpus = JSON.parse(await readFile(new URL('./acceptance.json', import.meta.url), 'utf8'));
let assertions = 0;
for (const vector of corpus) {
  const bytes = Buffer.from(vector.request_hex, 'hex');
  let validUtf8 = true;
  try { decoder.decode(bytes); } catch { validUtf8 = false; }
  if (bytes.length > 32768 || !validUtf8) {
    assert.throws(() => invoke(bytes), undefined, vector.name);
  } else {
    assert.equal(invoke(bytes), vector.response, vector.name);
  }
  assertions++;
}
function review(content, quotation = '', facet = '', interpretation = '', audience = 'client') {
  return JSON.parse(invoke(encoder.encode(['review', content, quotation, facet, interpretation, audience].join('\x1f'))));
}
const unicode = 'Déclaration: "No notice" — 支払いなし. <script>alert(1)</script> \\';
assert.equal(review(unicode).cells[2], unicode);
assert.equal(review('There was no notice.').cells[1], 'Unassigned');
assert.equal(review('notice received\nnotice disputed', 'notice received', 'Notice').cells[1], 'Notice');
const corrected = review('notice received\nnotice disputed', 'notice received', 'Notice', 'payment completed');
assert.equal(corrected.cells[1], 'Unassigned', 'correction must recompute dependent suggestions');
assert(corrected.details.some(item => item.includes('payment completed')));
const lawyer = review('\nZoë\r\nnot received', '', '', '', 'lawyer');
assert.equal(lawyer.cells[0], 'Line 2');
assert(lawyer.details.includes('Source 1, revision 1, UTF-8 bytes 1..6'));
assert(!lawyer.details.includes('Source 1, revision 1, UTF-8 bytes 7..19'), 'unrelated passages stay out of the focused view');
assert.equal(lawyer.details.length, 1);
assert.equal(review(Array.from({length: 64}, (_, i) => `passage ${i}`).join('\n')).status, 'ok');
assert.equal(review('x\n'.repeat(64)).error, 'source');
assert.equal(review('x'.repeat(8193)).error, 'source');
assert.equal(review('x'.repeat(8192)).cells[2], 'x'.repeat(8192));
assert.equal(review('\0'.repeat(8192)).cells[2], '\0'.repeat(8192));
assert.equal(review('x', 'x', 'f'.repeat(129)).error, 'review-limit');
assert.equal(review('x', 'x', 'Fact', 'y'.repeat(8193)).error, 'review-limit');
assert.equal(review('x', '', '', '', 'admin').error, 'audience');
assert.equal(review('same\nsame', 'same', 'Fact').error, 'review');
assert.equal(review('actual source', 'invented source', 'Fact').error, 'review');
assert.equal(review('x', '', 'Fact').error, 'review');
assert.equal(review('x\nx\nx', 'x', 'Fact').cells.length, 0);
console.log(`PASS: ${assertions} corpus vectors plus unseen and boundary inputs against generated WebAssembly`);
