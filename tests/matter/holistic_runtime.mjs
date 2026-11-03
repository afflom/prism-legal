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


// Equal interpretations are selected by their visible source location.
let located=invoke('create',['','Separate receipt corrections']).response;
for(const [operation, fields] of [
 ['ingest',['client','Records','Zoë: 75\r\nZoë: 75']],
 ['goal',['client','Review both receipts']],
 ['review',['client','amount','75']],
 ['review',['client','amount','75']]]){
 result=invoke(operation,[located,...fields]);assert.equal(result.status,'ok');located=result.response;
}
result=invoke('inspect',[located,'client','amount','1']);
assert.match(result.details.join(' '),/Source location: Records · line 1/);
assert.match(result.details.join(' '),/Source location: Records · line 2/);
for(const location of ['', 'Records · line 3']){
 result=invoke('edit',[located,'client','amount','75','80',location]);
 assert.equal(result.status,'error');assert.equal(result.response,located);
}
result=invoke('annotate',[located,'client','amount','75','disputed.amount','75','Records · line 2']);
assert.equal(result.status,'ok');located=result.response;
result=invoke('edit',[located,'client','amount','75','80','Records · line 2']);
assert.equal(result.status,'ok');located=result.response;
result=invoke('inspect',[located,'client','amount','1']);
assert.match(result.details.join(' '),/Current interpretation: 75 — Source location: Records · line 1/);
assert.match(result.details.join(' '),/Current interpretation: 80 — Source location: Records · line 2/);
result=invoke('withdraw',[located,'client','amount','75','Records · line 1']);
assert.equal(result.status,'ok');located=result.response;
result=invoke('inspect',[located,'client','amount','1']);
assert.match(result.details.join(' '),/Withdrawn: 75 — Source location: Records · line 1/);
assert.match(result.details.join(' '),/Current interpretation: 80 — Source location: Records · line 2/);
assert.equal(invoke('restore',[located]).response,located);
result=invoke('replace-source',[located,'client','Records','Replacement heading\n75']);assert.equal(result.status,'ok');located=result.response;
result=invoke('inspect',[located,'client','amount','1']);
assert.match(result.details.join(' '),/Needs review: 80 — Source location: Records · earlier version 1 · line 2/);
result=invoke('edit',[located,'client','amount','80','85','Records · earlier version 1 · line 2']);
assert.equal(result.status,'error');assert.equal(result.response,located);


// Reviewed date meanings drive chronology; corrections and disputes change the view.
let dated=invoke('create',['','Notice chronology']).response;
for(const [operation,fields] of [
 ['ingest',['client','Notices','Notice dated 2024-03-01.\nNotice dated 2024-02-29.']],
 ['goal',['client','Understand the sequence']],
 ['review',['client','notice.date','2024-03-01']],
 ['review',['client','notice.date','']]]){
 result=invoke(operation,[dated,...fields]);assert.equal(result.status,'ok');dated=result.response;
}
result=invoke('timeline',[dated,'client','notice.date','1']);assert.equal(result.status,'ok');assert.equal(result.response,dated);
assert.equal(result.message,'Chronology: notice.date');assert.match(result.details[0],/Current dates: 2; dates needing review: 0/);
assert.match(result.details[1],/^2024-02-29 — Notices · line 2 — Notice dated 2024-02-29/);
assert.match(result.details[2],/^2024-03-01 — Notices · line 1/);
assert.equal(invoke('timeline',[dated,'client','notice.date','0']).status,'error');
assert.equal(invoke('timeline',[dated,'client','','1']).status,'ok');
result=invoke('edit',[dated,'client','notice.date','2024-03-01','2024-02-28','Notices · line 1']);assert.equal(result.status,'ok');dated=result.response;
assert.match(invoke('timeline',[dated,'client','notice.date','1']).details[1],/^2024-02-28/);
result=invoke('annotate',[dated,'client','notice.date','2024-02-29','notice.date','2024-03-02','Notices · line 2']);assert.equal(result.status,'ok');dated=result.response;
result=invoke('timeline',[dated,'client','notice.date','1']);assert.match(result.details[0],/Current dates: 1; dates needing review: 2/);
assert.match(result.details[1],/^Competing dates:/);assert.match(result.details[2],/^Competing dates:/);
result=invoke('withdraw',[dated,'client','notice.date','2024-03-02','Notices · line 2']);assert.equal(result.status,'ok');dated=result.response;
assert.match(invoke('timeline',[dated,'client','notice.date','1']).details[0],/Current dates: 2; dates needing review: 0/);
result=invoke('edit',[dated,'client','notice.date','2024-02-29','2023-02-29','Notices · line 2']);assert.equal(result.status,'ok');dated=result.response;
result=invoke('timeline',[dated,'client','notice.date','1']);assert.match(result.details[1],/^Needs a valid YYYY-MM-DD date: 2023-02-29/);
assert.equal(invoke('restore',[dated]).response,dated);
result=invoke('assertion',[dated,'client','response.date','2024-03-04']);assert.equal(result.status,'ok');dated=result.response;
result=invoke('timeline',[dated,'client','notice.date\nresponse.date\nnotice.date\n','1']);assert.equal(result.status,'ok');assert.equal(result.response,dated);
assert.match(result.details[0],/Current dates: 2; dates needing review: 1/);
assert.match(result.details.join(' '),/2024-03-04 \(response.date\) — Recorded directly/);


// A current source location distinguishes resources with the same name.
let resources=invoke('create',['','Resource revisions']).response;
for(const text of ['First resource','Second resource']){
 result=invoke('ingest',[resources,'client','Records',text]);assert.equal(result.status,'ok');resources=result.response;
 if(text==='First resource'){const bad=invoke('replace-source',[resources,'client','Records','Wrong','Missing · line 1']);assert.equal(bad.status,'error');assert.equal(bad.response,resources);}
}
result=invoke('replace-source',[resources,'client','Records','Replacement']);assert.equal(result.status,'error');assert.equal(result.response,resources);
result=invoke('replace-source',[resources,'client','Records','Replacement','Records · resource 2 · line 1']);assert.equal(result.status,'ok');resources=result.response;
result=invoke('inspect',[resources,'client','Unassigned','1']);
assert.match(result.details.join(' '),/First resource — Source location: Records · resource 1 · line 1/);
assert.match(result.details.join(' '),/Second resource — Source location: Records · resource 2 · earlier version 1 · line 1/);
assert.match(result.details.join(' '),/Replacement — Source location: Records · resource 2 · line 1/);
result=invoke('replace-source',[resources,'client','Records','Wrong','Records · resource 2 · earlier version 1 · line 1']);assert.equal(result.status,'error');assert.equal(result.response,resources);
result=invoke('replace-source',[resources,'client','','Second replacement','Records · resource 2 · line 1']);assert.equal(result.status,'ok');resources=result.response;
assert.equal(invoke('restore',[resources]).response,resources);

// Exercise the admitted journal count in the actual Wasm guest, not a smaller proxy.
const field=value=>Buffer.byteLength(value)+':'+value;
const command=values=>values.map(field).join('');
let full=command(['prism-legal/journal/1','Boundary matter']);
for(let revision=0;revision<512;revision++)full+=field(command(['assert',String(revision),'client','client','context',String(revision)]));
result=invoke('restore',[full]);assert.equal(result.status,'ok');assert.equal(result.response,full);
result=invoke('assertion',[full,'client','context','another']);assert.equal(result.status,'error');assert.equal(result.response,full);
assert.equal(invoke('restore',[full+field(command(['assert','512','client','client','context','extra']))]).status,'error');
// The declared CSV limits must execute, not exhaust the guest stack.
const emptyCsvMatter=invoke('create',['','CSV boundaries']).response;
for(const content of ['a\n'+'x'.repeat(8190),Array.from({length:512},(_,i)=>'a'+i).join(',')+'\n'+Array(512).fill('x').join(','),Array.from({length:16},(_,i)=>'a'+i).join(',')+'\n'+Array(63).fill(Array(16).fill('x').join(',')).join('\n')]){
 result=invoke('ingest-csv',[emptyCsvMatter,'client','Boundary',content]);assert.equal(result.status,'ok');assert.equal(invoke('restore',[result.response]).response,result.response);result=invoke('goal',[result.response,'client','Review the boundary table']);assert.equal(result.status,'ok');assert.match(result.details.join(' '),/row 2 · column 1/);
}
for(const content of ['a\n'+'x'.repeat(8191),'a\n'+'x,'.repeat(1024)]){result=invoke('ingest-csv',[emptyCsvMatter,'client','Boundary',content]);assert.equal(result.status,'error');assert.equal(result.response,emptyCsvMatter);}
let columnMatter=invoke('create',['','Column context']).response;
for(const [op,args]of [['ingest-csv',['client','Records','amount,person\n50,50\n50,50']],['goal',['client','Review the table']],...Array(4).fill(['review',['client','','']])]){result=invoke(op,[columnMatter,...args]);assert.equal(result.status,'ok');columnMatter=result.response;}
assert.equal(invoke('overview',[columnMatter,'client']).message,'Confirm the governing jurisdiction');
result=invoke('annotate',[columnMatter,'client','amount','50','claimed.amount','50','Records · row 2 · column 1']);assert.equal(result.status,'ok');
assert.match(result.details.join(' '),/Records · row 3 · column 1/);
// Structured CSV intake is decoded by the model, with exact raw source evidence.
let csv=invoke('create',['','Table review']).response;
const csvSource='\ufeffperson,notes,date\r\nZoë,"said ""yes"", then\r\nleft",2024-02-29\r\n';
result=invoke('ingest-csv',[csv,'client','Records',csvSource]);assert.equal(result.status,'ok');csv=result.response;
assert(csv.includes(csvSource));
csv=invoke('goal',[csv,'client','Understand the table']).response;
result=invoke('overview',[csv,'client']);assert.match(result.details.join(' '),/Suggested facet: person/);assert.match(result.details.join(' '),/Records · row 2 · column 1/);
for(const facet of ['person','notes','date']){result=invoke('review',[csv,'client','','']);assert.equal(result.status,'ok');csv=result.response;}
result=invoke('inspect',[csv,'lawyer','notes','1']);assert.match(result.details.join(' '),/said "yes", then +left/);assert.match(result.details.join(' '),/Records · row 2 · column 2/);
result=invoke('timeline',[csv,'client','date','1']);assert.match(result.details.join(' '),/2024-02-29 — Records · row 2 · column 3/);
const csvBefore=csv;
for(const content of ['a,a\n1,2','a,b\n1','a\n"unfinished','a\n"closed"junk']){result=invoke('ingest-csv',[csv,'client','Invalid',content]);assert.equal(result.status,'error');assert.equal(result.error,'csv');assert.equal(result.response,csv);}
result=invoke('replace-source',[csv,'client','Records','person,notes,date\n李,,2024-03-01','Records · row 2 · column 3']);assert.equal(result.status,'ok');csv=result.response;assert.notEqual(csv,csvBefore);
assert.equal(invoke('restore',[csv]).response,csv);
result=invoke('timeline',[csv,'client','date','1']);assert.match(result.details.join(' '),/Current dates: 0/);
result=invoke('inspect',[csv,'client','date','1']);assert.match(result.details.join(' '),/Records · earlier version 1 · row 2 · column 3/);

// Read-only source inspection keeps record context and retained versions separate.
const sourceContextJournal=csv;
result=invoke('resource',[csv,'client','Records','Records · earlier version 1 · row 2 · column 2','']);assert.equal(result.status,'ok');assert.equal(result.response,csv);
assert.match(result.details.join(' '),/CSV source · row 2 · earlier version 1/);assert.match(result.details.join(' '),/person: Zoë/);assert.match(result.details.join(' '),/notes: said "yes", then +left/);assert.match(result.details.join(' '),/date: 2024-02-29/);
result=invoke('resource',[csv,'client','Records','Records · row 2 · column 3','']);assert.equal(result.status,'ok');assert.equal(result.response,csv);
assert.match(result.details.join(' '),/person: 李/);assert.match(result.details.join(' '),/notes: Empty source cell/);assert.doesNotMatch(result.details.join(' '),/2024-02-29/);
result=invoke('resource',[csv,'client','Missing','Records · row 2 · column 3','']);assert.equal(result.status,'error');assert.equal(result.error,'source-selection');assert.equal(result.response,csv);
for(const page of ['0','129','01']){result=invoke('resource',[csv,'client','Records','',page]);assert.equal(result.status,'error');assert.equal(result.response,csv);}
assert.equal(csv,sourceContextJournal);
const longText=Array.from({length:24},(_,i)=>`Zoë line ${i+1}\r`).join('\n');
let sourceText=invoke('ingest',[csv,'client','Text',longText]).response;
result=invoke('resource',[sourceText,'client','Text','Text · line 20','']);assert.equal(result.status,'ok');assert.equal(result.response,sourceText);assert.match(result.details[0],/page 3 of 3/);assert.match(result.details.join(' '),/line 17 — Zoë line 17/);assert.match(result.details.join(' '),/line 20 — Zoë line 20/);assert.doesNotMatch(result.details.join(' '),/line 16 —/);
result=invoke('resource',[sourceText,'client','','','']);assert.equal(result.status,'ok');assert.equal(result.response,sourceText);assert.match(result.message,/Resources/);assert.match(result.details.join(' '),/Text · line 1/);assert.match(result.details.join(' '),/Records · row 2 · column 1/);

console.log(`PASS: ${model.acceptance_vectors.length} source vectors plus unseen journal, Unicode, control-display, input-boundary, multiple-facet and joint-slot learning, withdrawal and refusal cases in generated Wasm`);
