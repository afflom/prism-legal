// Native model corpus and unseen boundaries executed through the generated Wasm adapter.
import assert from 'node:assert/strict';
import {readFile,readdir} from 'node:fs/promises';
import {resolve,join} from 'node:path';
import {pathToFileURL} from 'node:url';
const directory=resolve(process.argv[2]),files=await readdir(directory);
const adapter=files.find(name=>name.endsWith('.js')&&name!=='app.js');
const guest=await import(pathToFileURL(join(directory,adapter)));
guest.initSync({module:await readFile(join(directory,files.find(name=>name.endsWith('_bg.wasm'))))});
const model=JSON.parse(await readFile(resolve(directory,'../../model.prism.json'),'utf8')).application;
const decoder=new TextDecoder('utf-8',{fatal:true,ignoreBOM:true});
for(const vector of model.acceptance_vectors){const input=Uint8Array.from(vector.request);if(input.byteLength>model.request_maximum)assert.throws(()=>guest.invoke_bytes(input));else assert.deepEqual(Buffer.from(guest.invoke_bytes(input)),Buffer.from(vector.response));}
const frame=(operation,values)=>Buffer.from(operation+'\x1f'+values.map(value=>Buffer.byteLength(value)+':'+value).join(''));
const invoke=(operation,values)=>JSON.parse(decoder.decode(guest.invoke_bytes(frame(operation,values))));
let state=invoke('create',['','Unicode\x1f matter']).response;
assert(state.includes('Unicode\x1f matter'));
const original='Zoë\r\n\0\x1f\u0085\u00a0\u1680\u2000\u2028\u2029\u202f\u205f\u3000\ufeff';
let result=invoke('ingest',[state,'client','Original',original]);assert.equal(result.status,'ok');state=result.response;assert(state.includes(original));
result=invoke('goal',[state,'client','Understand the source']);assert.equal(result.status,'ok');state=result.response;
result=invoke('review',[state,'client','person','Zoë']);assert.equal(result.status,'ok');state=result.response;
assert(result.details.every(text=>text.trim()&&!/[\x00-\x1f\x7f-\x9f]/.test(text)),'control-only source passages must have a valid honest display');
assert.match(result.details.join(' '),/Whitespace or control-only/);
const roundtrip=invoke('restore',[state]);assert.equal(roundtrip.status,'ok');assert.equal(roundtrip.response,state);
for(const malformed of [state+'1:x',state.slice(0,-1),'01:a','1:é']){const refused=invoke('restore',[malformed]);assert.equal(refused.status,'error');}
const refusal=invoke('ingest',[state,'client','Too long','x'.repeat(8193)]);assert.equal(refusal.status,'error');assert.equal(refusal.response,state);
assert.equal(invoke('ingest',[state,'client','Too many lines','x\n'.repeat(64)]).status,'error');
assert.equal(invoke('review',[state,'admin','fact','invented']).status,'error');
assert.equal(invoke('create',[state,'Replacement']).status,'error');
assert.equal(invoke('inspect',[state,'client','','0']).status,'error');
assert.equal(invoke('inspect',[state,'client','','1']).status,'ok');
for(const payload of ['create\x1f00:0:','create\x1f1:é','create\x1f0:1:xjunk'])assert.equal(JSON.parse(decoder.decode(guest.invoke_bytes(Buffer.from(payload)))).status,'error');
assert.throws(()=>guest.invoke_bytes(Uint8Array.of(255)));

// Learned source wording is exercised through the same byte entry used by the UI.
let learned=invoke('create',['','Receipts']).response;
learned=invoke('ingest',[learned,'client','Receipts','Payment: 50 USD.\nPayment: 75 USD.']).response;
learned=invoke('goal',[learned,'client','Understand the payments']).response;
learned=invoke('review',[learned,'client','payment.amount','50']).response;
learned=invoke('annotate',[learned,'client','payment.amount','50','claimed.amount','50']).response;
result=invoke('overview',[learned,'client']);
assert.match(result.details.join(' '),/payment.amount: 75/);
assert.match(result.details.join(' '),/claimed.amount: 75/);
result=invoke('review',[learned,'client','payment.amount','']);assert.equal(result.status,'ok');learned=result.response;
result=invoke('inspect',[learned,'client','payment.amount','1']);assert.match(result.details.join(' '),/Current interpretation: 75/);
result=invoke('withdraw',[learned,'client','claimed.amount','50']);assert.equal(result.status,'ok');learned=result.response;
result=invoke('impact',[learned,'client','1']);assert.match(result.details.join(' '),/Withdrawn/);
result=invoke('inspect',[learned,'client','claimed.amount','1']);assert.match(result.details.join(' '),/Withdrawn: 50/);
assert.equal(invoke('restore',[learned]).response,learned);

let conflicting=invoke('create',['','Conflicting interpretations']).response;
conflicting=invoke('ingest',[conflicting,'client','Receipts','Payment: 50 USD.\nPayment: 50 USD.']).response;
conflicting=invoke('goal',[conflicting,'client','Understand the payments']).response;
conflicting=invoke('review',[conflicting,'client','payment.amount','50']).response;
conflicting=invoke('annotate',[conflicting,'client','payment.amount','50','payment.amount','not confirmed']).response;
result=invoke('review',[conflicting,'client','payment.amount','']);assert.equal(result.status,'error');assert.equal(result.response,conflicting,'a blank review cannot resolve conflicting learned meanings');
result=invoke('review',[conflicting,'client','payment.amount','50']);assert.equal(result.status,'ok');

// Exercise the admitted journal count in the actual Wasm guest, not a smaller proxy.
const field=value=>Buffer.byteLength(value)+':'+value;
const command=values=>values.map(field).join('');
let full=command(['prism-legal/journal/1','Boundary matter']);
for(let revision=0;revision<512;revision++)full+=field(command(['assert',String(revision),'client','client','context',String(revision)]));
result=invoke('restore',[full]);assert.equal(result.status,'ok');assert.equal(result.response,full);
result=invoke('assertion',[full,'client','context','another']);assert.equal(result.status,'error');assert.equal(result.response,full);
assert.equal(invoke('restore',[full+field(command(['assert','512','client','client','context','extra']))]).status,'error');
console.log(`PASS: ${model.acceptance_vectors.length} source vectors plus unseen journal, Unicode, control-display, input-boundary, multiple-facet learning, withdrawal and refusal cases in generated Wasm`);
