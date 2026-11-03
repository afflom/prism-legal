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

// Multiple reviewed slots may change together; no fixed source value is copied.
let joint=invoke('create',['','Dated receipts']).response;
joint=invoke('ingest',[joint,'client','Records','Amount: 50; day: Monday.\nAmount: 75; day: Tuesday.']).response;
joint=invoke('goal',[joint,'client','Understand both receipt fields']).response;
joint=invoke('review',[joint,'client','amount','50']).response;
joint=invoke('annotate',[joint,'client','amount','50','day','Monday']).response;
result=invoke('overview',[joint,'client']);assert.match(result.details.join(' '),/amount: 75/);assert.match(result.details.join(' '),/day: Tuesday/);
result=invoke('review',[joint,'client','amount','']);assert.equal(result.status,'ok');joint=result.response;
assert.equal(result.message,'Review another aspect of this passage');
assert.match(result.request,/^review\u001f/);assert.match(result.request,/Tuesday/);
const pendingDay=joint;
result=invoke('review',[joint,'client','day','Tuesday']);assert.equal(result.status,'ok');joint=result.response;
assert.equal(result.message,'Confirm the governing jurisdiction');
assert.notEqual(joint,pendingDay);
result=invoke('withdraw',[joint,'client','day','Tuesday']);assert.equal(result.status,'ok');joint=result.response;
assert.equal(result.message,'Confirm the governing jurisdiction');
result=invoke('inspect',[joint,'client','amount','1']);assert.match(result.details.join(' '),/Current interpretation: 75/);
assert.equal(invoke('restore',[joint]).response,joint);

// A role change changes permission, never the focused source passage.
let roleMatter=invoke('annotate',[pendingDay,'lawyer','amount','50','authority','Monday']).response;
const clientFocus=invoke('overview',[roleMatter,'client']),lawyerFocus=invoke('overview',[roleMatter,'lawyer']);
assert.equal(clientFocus.message,'Lawyer review: another aspect');assert.equal(clientFocus.request,'');
assert.match(clientFocus.details.join(' '),/Records · line 2/);assert.match(lawyerFocus.details.join(' '),/Records · line 2/);
assert.equal(clientFocus.response,roleMatter);assert.equal(lawyerFocus.response,roleMatter);
result=invoke('review',[roleMatter,'client','','']);assert.equal(result.status,'error');assert.equal(result.response,roleMatter);
result=invoke('review',[roleMatter,'lawyer','authority','Tuesday']);assert.equal(result.status,'ok');roleMatter=result.response;
assert.match(invoke('inspect',[roleMatter,'lawyer','authority','1']).details.join(' '),/Current interpretation: Tuesday/);

// Equal values on distinct passages remain separately reviewable through the focused action.
let repeated=invoke('create',['','Repeated receipts']).response;
repeated=invoke('ingest',[repeated,'client','Records','Amount: 50; day: Monday.\nAmount: 75; day: Tuesday.\nAmount: 75; day: Tuesday.']).response;
repeated=invoke('goal',[repeated,'client','Review each receipt']).response;
repeated=invoke('review',[repeated,'client','amount','50']).response;
repeated=invoke('annotate',[repeated,'client','amount','50','day','Monday']).response;
repeated=invoke('review',[repeated,'client','amount','75']).response;
repeated=invoke('review',[repeated,'client','amount','75']).response;
result=invoke('overview',[repeated,'client']);assert.match(result.details.join(' '),/Records · line 2/);
result=invoke('review',[repeated,'client','different.aspect','']);assert.equal(result.status,'error');assert.equal(result.response,repeated);
result=invoke('review',[repeated,'client','day','']);assert.equal(result.status,'ok');repeated=result.response;
assert.match(result.details.join(' '),/Records · line 3/);
result=invoke('review',[repeated,'client','day','']);assert.equal(result.status,'ok');repeated=result.response;
assert.equal(result.message,'Confirm the governing jurisdiction');
assert.equal(invoke('restore',[repeated]).response,repeated);

for (const next of ['Payment: 50 USD.','Payment: 75 USD.']) {
let conflicting=invoke('create',['','Conflicting interpretations']).response;
conflicting=invoke('ingest',[conflicting,'client','Receipts','Payment: 50 USD.\n'+next]).response;
conflicting=invoke('goal',[conflicting,'client','Understand the payments']).response;
conflicting=invoke('review',[conflicting,'client','payment.amount','50']).response;
conflicting=invoke('annotate',[conflicting,'client','payment.amount','50','payment.amount','not confirmed']).response;
result=invoke('review',[conflicting,'client','payment.amount','']);assert.equal(result.status,'error');assert.equal(result.response,conflicting,'a blank review cannot resolve conflicting learned meanings');
result=invoke('review',[conflicting,'client','payment.amount','50']);assert.equal(result.status,'ok');
}
let unanchored=invoke('create',['','Unanchored facets']).response;
unanchored=invoke('ingest',[unanchored,'client','Notes','50\nunrelated wording']).response;
unanchored=invoke('goal',[unanchored,'client','Understand the notes']).response;
unanchored=invoke('review',[unanchored,'client','amount','50']).response;
unanchored=invoke('annotate',[unanchored,'client','amount','50','claimed.amount','50']).response;
result=invoke('overview',[unanchored,'client']);assert.equal(result.response,unanchored);
assert.doesNotMatch(result.details.join(' '),/(?:amount|claimed.amount): unrelated wording/,'unanchored aliases cannot teach a meaning transfer');


// Exercise the admitted journal count in the actual Wasm guest, not a smaller proxy.
const field=value=>Buffer.byteLength(value)+':'+value;
const command=values=>values.map(field).join('');
let full=command(['prism-legal/journal/1','Boundary matter']);
for(let revision=0;revision<512;revision++)full+=field(command(['assert',String(revision),'client','client','context',String(revision)]));
result=invoke('restore',[full]);assert.equal(result.status,'ok');assert.equal(result.response,full);
result=invoke('assertion',[full,'client','context','another']);assert.equal(result.status,'error');assert.equal(result.response,full);
assert.equal(invoke('restore',[full+field(command(['assert','512','client','client','context','extra']))]).status,'error');
console.log(`PASS: ${model.acceptance_vectors.length} source vectors plus unseen journal, Unicode, control-display, input-boundary, multiple-facet and joint-slot learning, withdrawal and refusal cases in generated Wasm`);
