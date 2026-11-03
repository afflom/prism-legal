import {chromium} from 'playwright';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_EXECUTABLE,args:['--no-sandbox']});
const context=await browser.newContext({viewport:{width:1280,height:1000},acceptDownloads:true});
const page=await context.newPage();const errors=[];page.on('pageerror',error=>errors.push(error.message));
const url=process.env.BROWSER_URL;assert(url,'BROWSER_URL must name the actual generated build');
const ready=()=>page.waitForFunction(()=>document.querySelector('#guided-submit')?.disabled===false);
const message=()=>page.locator('#result-message').textContent();
async function run(op,values={}){await page.locator('#operation').selectOption(op);for(const [id,value]of Object.entries(values)){const node=page.locator('#field-'+id);if(await node.evaluate(n=>n.tagName==='SELECT'))await node.selectOption(value);else await node.fill(value);}await page.locator('#guided-submit').click();await ready();assert.equal(await page.locator('#status').getAttribute('data-state'),'ready',await page.locator('#status').textContent());return message();}
async function save(){const pending=page.waitForEvent('download');await page.locator('#save-session').click();return readFile(await(await pending).path());}
try{
 await page.goto(url);await ready();assert.equal(await page.locator('#field-state').isVisible(),false);assert.equal(await page.locator('#save-session').isDisabled(),true);
 assert.equal(await run('create',{title:'Notice dispute'}),'Start with a source');
 const created=await save();assert.equal(await page.locator('#next-form').textContent(),'Add a resource');await page.locator('#next-form').click();assert.equal(await page.locator('#operation').inputValue(),'ingest');assert.deepEqual(await save(),created,'opening the recommended form must not mutate the matter');
 await page.locator('#operation').selectOption('ingest');await page.locator('#field-title').fill('Notice');const original=Buffer.from('Zoë: notice received\r\n');await page.locator('#file-content').setInputFiles({name:'notice.txt',mimeType:'text/plain',buffer:original});await page.waitForFunction(()=>document.querySelector('#field-content').value.includes('Zoë'));await page.locator('#guided-submit').click();await ready();
 assert.equal(await message(),'What would you like to achieve?');await run('goal',{value:'Respond to the notice'});assert.equal(await message(),'Review this passage');
 await run('review',{facet:'notice.receipt',interpretation:'received'});assert.equal(await message(),'Confirm the governing jurisdiction');
 await run('jurisdiction',{value:'Reviewed jurisdiction'});await run('ingest',{role:'lawyer',title:'Governing provision',content:'A received notice permits a response unless withdrawn.'});await run('review',{role:'lawyer',facet:'authority',interpretation:'Reviewed notice provision'});
 await run('rule',{role:'lawyer',premises:'notice.receipt = received',exceptions:'notice.withdrawal = withdrawn',action:'Prepare a response.'});assert.equal(await message(),'Review the proposed next action');
 await run('strategy');assert.match(await page.locator('#result-details').textContent(),/Prepare a response/);assert.match(await page.locator('#result-details').textContent(),/received notice permits/);
 await run('propose');assert.equal(await message(),'Lawyer review: proposed conclusion');const proposal=await save();
 await run('review',{facet:'legal-conclusion'});assert.equal(await page.locator('#result-error').isVisible(),true);assert.deepEqual(await save(),proposal,'client review must not accept a legal conclusion');
 await run('review',{role:'lawyer',facet:'legal-conclusion'});assert.equal(await message(),'Review the proposed next action');
 await run('inspect',{facet:'notice.receipt',page:'1',role:'lawyer'});assert.match(await page.locator('#result-details').textContent(),/Current interpretation: received/);assert.match(await page.locator('#result-details').textContent(),/Zoë/);
 await run('annotate',{'from-facet':'notice.receipt','from-value':'received',facet:'notice.receipt',interpretation:'not received'});
 assert.equal(await message(),'Complete the missing context');assert.match(await page.locator('#result-details').textContent(),/competing interpretations/);
 assert.equal(await page.locator('#next-form').textContent(),'Inspect matter context');await page.locator('#next-form').click();assert.equal(await page.locator('#field-facet').inputValue(),'notice.receipt');await page.locator('#guided-submit').click();await ready();assert.match(await page.locator('#result-details').textContent(),/Competing interpretation: received/);
 await run('withdraw',{facet:'notice.receipt',value:'not received'});await run('inspect',{facet:'legal-conclusion'});assert.match(await page.locator('#result-details').textContent(),/Needs review/);
 await run('revise-rule',{role:'lawyer',premises:'notice.receipt = received',exceptions:'notice.withdrawal = withdrawn',action:'Prepare a revised response.','previous-action':'Prepare a response.'});assert.equal(await message(),'Review the proposed next action');
 await run('inspect',{facet:'legal-conclusion',page:'1'});assert.match(await page.locator('#result-details').textContent(),/Needs review: Prepare a response/);
 await run('strategy');assert.match(await page.locator('#result-details').textContent(),/Prepare a revised response/);
 await run('assertion',{facet:'notice.withdrawal',value:'withdrawn'});assert.equal(await message(),'An exception needs attention');await run('impact');assert.match(await page.locator('#result-details').textContent(),/Prepare a revised response/);await run('strategies');assert.match(await page.locator('#result-details').textContent(),/exception/i);await run('strategy');assert.match(await page.locator('#result-details').textContent(),/exception/i);
 await run('edit',{facet:'notice.receipt','old-value':'received','new-value':'disputed'});await run('strategy');assert.doesNotMatch(await page.locator('#result-details').textContent(),/The reviewed premises support this proposal/);
 const saved=await save();assert(saved.includes(original),'file import must preserve exact CRLF and Unicode source bytes');
 page.once('dialog',dialog=>dialog.accept());await page.reload();await ready();await page.locator('#open-session').setInputFiles({name:'matter.prismlegal',mimeType:'application/octet-stream',buffer:saved});await page.waitForFunction(()=>document.querySelector('#save-session').disabled===false);await ready();assert.deepEqual(await save(),saved,'reopening must reproduce the exact journal');
 await page.locator('#open-session').setInputFiles({name:'damaged.prismlegal',mimeType:'application/octet-stream',buffer:Buffer.concat([saved,Buffer.from('truncated')])});await page.waitForFunction(()=>document.querySelector('#result-error').hidden===false);assert.deepEqual(await save(),saved,'invalid replay must retain the complete prior matter');
 await page.setViewportSize({width:390,height:844});assert(await page.evaluate(()=>document.documentElement.scrollWidth<=document.documentElement.clientWidth));assert.deepEqual(errors,[]);
 await page.reload();await ready();await run('create',{title:'Receipts'});
 await run('ingest',{title:'Receipts',content:'Payment: 50 USD.\nPayment: 75 USD.'});await run('goal',{value:'Understand the payments'});
 await run('review',{facet:'payment.amount',interpretation:'50'});
 assert.match(await page.locator('#result-details').textContent(),/payment.amount: 75/);
 await run('annotate',{'from-facet':'payment.amount','from-value':'50',facet:'claimed.amount',interpretation:'50'});
 assert.match(await page.locator('#result-details').textContent(),/claimed.amount: 75/);
 if(process.env.BROWSER_SCREENSHOT){await page.setViewportSize({width:1280,height:1000});await page.screenshot({path:process.env.BROWSER_SCREENSHOT,fullPage:true});}
 await run('review',{facet:'payment.amount'});await run('inspect',{facet:'payment.amount'});assert.match(await page.locator('#result-details').textContent(),/Current interpretation: 75/);
 await run('withdraw',{facet:'claimed.amount',value:'50'});await run('inspect',{facet:'claimed.amount'});assert.match(await page.locator('#result-details').textContent(),/Withdrawn: 50/);
 await page.reload();await ready();await run('create',{title:'Dated receipts'});
 await run('ingest',{title:'Records',content:'Amount: 50; day: Monday.\nAmount: 75; day: Tuesday.'});await run('goal',{value:'Understand both fields'});
 await run('review',{facet:'amount',interpretation:'50'});
 await run('annotate',{'from-facet':'amount','from-value':'50',facet:'day',interpretation:'Monday'});
 assert.match(await page.locator('#result-details').textContent(),/amount: 75/);assert.match(await page.locator('#result-details').textContent(),/day: Tuesday/);
 await run('review',{facet:'amount'});await run('inspect',{facet:'amount'});assert.match(await page.locator('#result-details').textContent(),/Current interpretation: 75/);
 assert.deepEqual(errors,[]);
 console.log('PASS: compiled local matter journey, exact resource import, rule-bound proposal review, exception/correction propagation, save/reopen/refusal, learned multi-facet and joint-slot interpretation, withdrawal, next-form navigation, and mobile layout');
}finally{await context.close();await browser.close();}
