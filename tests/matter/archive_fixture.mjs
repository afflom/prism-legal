// A real journal at the intake boundary, with an incomplete review history.
export function reviewedArchive(count=64){
 const fields=values=>values.map(value=>Buffer.byteLength(value)+':'+value).join('');
 let journal=fields(['prism-legal/journal/1','Archive review']),revision=0;
 for(let index=0;index<16;index++)journal+=fields([fields(['ingest',String(revision++),'client','client',`Resource ${index+1}`,Array(63).fill('entry').join('\n')])]);
 journal+=fields([fields(['assert',String(revision++),'client','client','goal','Understand the archive'])]);
 for(let identifier=1;identifier<=count;identifier++)journal+=fields([fields(['review',String(revision++),'client','client',String(identifier),'1','entry','entry','true'])]);
 return journal;
}
