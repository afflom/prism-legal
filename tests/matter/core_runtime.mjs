// Execute the archive's actual import-free guest; the browser adapter has a different allocator.
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {resolve,join} from 'node:path';
const root=resolve(process.argv[2]);
const model=JSON.parse(await readFile(join(root,'model.prism.json'),'utf8')).application;
const module=new WebAssembly.Module(await readFile(join(root,'core-wasm/prism_legal_matter_core_wasm.wasm')));
assert.equal(WebAssembly.Module.imports(module).length,0);
const capacity=[];
for(const [index,vector] of model.acceptance_vectors.entries()) {
 const guest=new WebAssembly.Instance(module,{}).exports;
 const started=performance.now();
 try {
  const input=Uint8Array.from(vector.request),pointer=guest.holo_alloc(input.byteLength);
  new Uint8Array(guest.memory.buffer,pointer,input.byteLength).set(input);
  const output=BigInt.asUintN(64,guest.holo_run(pointer,input.byteLength));
  const start=Number(output>>32n),length=Number(output&0xffffffffn);
  assert.equal(start%8,0);assert(length<=model.response_maximum);assert(start+length<=guest.memory.buffer.byteLength);
  assert.deepEqual(Buffer.from(new Uint8Array(guest.memory.buffer,start,length)),Buffer.from(vector.response),`acceptance vector ${index}`);
  if(vector.request.length>10000)capacity.push({index,requestBytes:vector.request.length,memoryBytes:guest.memory.buffer.byteLength,milliseconds:Math.round(performance.now()-started)});
 } catch(error) {
  console.error(JSON.stringify({index,requestBytes:vector.request.length,memoryBytes:guest.memory.buffer.byteLength,error:String(error)}));throw error;
 }
}
console.log(JSON.stringify({capacity}));
console.log(`PASS: ${model.acceptance_vectors.length} source vectors in the actual import-free Core-Wasm guest`);
