// A real journal at the intake boundary, with an incomplete review history.
export function reviewedArchive(count=64){
 const fields=values=>values.map(value=>Buffer.byteLength(value)+':'+value).join('');
 let journal=fields(['prism-legal/journal/1','Archive review']),revision=0;
 for(let index=0;index<16;index++)journal+=fields([fields(['ingest',String(revision++),'client','client',`Resource ${index+1}`,Array(63).fill('entry').join('\n')])]);
 journal+=fields([fields(['assert',String(revision++),'client','client','goal','Understand the archive'])]);
 for(let identifier=1;identifier<=count;identifier++)journal+=fields([fields(['review',String(revision++),'client','client',String(identifier),'1','entry','entry','true'])]);
 return journal;
}

export function correctionHistory(commands=2048){
 const fields=values=>values.map(value=>Buffer.byteLength(value)+':'+value).join('');
 let journal=fields(['prism-legal/journal/1','Retained corrections']);
 journal+=fields([fields(['ingest','0','client','client','Record','original'])]);
 for(let revision=1;revision<commands;revision++)journal+=fields([fields(['review',String(revision),'client','client','1',String(revision),'entry',`value ${revision}`,'true'])]);
 return journal;
}

export function goalCapacity(){
 const fields=values=>values.map(value=>Buffer.byteLength(value)+':'+value).join('');
 let journal=fields(['prism-legal/journal/1','All current goals']);
 journal+=fields([fields(['ingest','0','client','client','Records','ordinary passage\ntarget agreement'])]);
 for(let index=0;index<1022;index++)journal+=fields([fields(['assert',String(index+1),'client','client','goal',index===0?'target agreement':`another outcome ${index}`])]);
 return journal;
}

export function directEntryCapacity(){
 const fields=values=>values.map(value=>Buffer.byteLength(value)+':'+value).join('');
 let journal=fields(['prism-legal/journal/1','Repeated entries']);
 for(let index=0;index<1024;index++)journal+=fields([fields(['assert',String(index),'client','client','goal',index===0||index===1023?'Repeated outcome':'Other outcome'])]);
 return journal;
}
