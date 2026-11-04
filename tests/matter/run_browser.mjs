// Serve only the emitted flat asset set while the actual browser journey runs.
import {createServer} from 'node:http';
import {readFile,readdir} from 'node:fs/promises';
import {resolve,join,extname} from 'node:path';
import {spawn} from 'node:child_process';
const root=resolve(process.argv[2]),names=new Set(await readdir(root));
// Exercise the repository path used by Pages, including worker/Wasm URLs.
const basePath='/prism-legal/';
const types={'.html':'text/html','.js':'text/javascript','.css':'text/css','.wasm':'application/wasm'};
const server=createServer(async(request,response)=>{
 const path=new URL(request.url,'http://localhost').pathname;
 if(!path.startsWith(basePath)){response.writeHead(404).end();return;}
 const name=path===basePath?'index.html':path.slice(basePath.length);
 if(!names.has(name)){response.writeHead(404).end();return;}
 try{response.writeHead(200,{'content-type':types[extname(name)]??'application/octet-stream','cache-control':'no-store'});response.end(await readFile(join(root,name)));}catch{response.writeHead(500).end();}
});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
try{const child=spawn(process.execPath,[new URL('./holistic_browser.mjs',import.meta.url).pathname],{stdio:'inherit',env:{...process.env,BROWSER_URL:`http://127.0.0.1:${server.address().port}${basePath}`}});const code=await new Promise((resolve,reject)=>{child.on('error',reject);child.on('exit',resolve);});if(code!==0)throw new Error(`Browser journey failed (${code})`);}finally{server.closeAllConnections();await new Promise(resolve=>server.close(resolve));}
