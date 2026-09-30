// Exercises actual UI JavaScript with a minimal DOM substitute and real local HTTP.
// This is a logic check, not a browser rendering or browser security test.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const html = fs.readFileSync(require('node:path').join(__dirname, '../app/ui.html'), 'utf8');
const base = process.argv[2];
let download, sessionKeys;
class Element {
  constructor(tag) { this.tag=tag;this.value='';this.textContent='';this.children=[];this.disabled=false; }
  append(...items) { this.children.push(...items); }
  replaceChildren(...items) { this.children=items; }
  add(item) { this.children.push(item); }
  focus() {}
  click() { if(this.tag==='a') download=this.href; }
}
const elements={};
for(const m of html.matchAll(/\bid="([^"]+)"/g)) elements[m[1]]=new Element(m[1]);
const location={origin:base,hash:'#launch=ui-test-ticket',pathname:'/',search:''};
const context=vm.createContext({
  document:{getElementById(id){assert.ok(elements[id], 'Unknown element '+id);return elements[id]},createElement:tag=>new Element(tag)},
  location,history:{replaceState(){location.hash=''}},
  Option:function(text,value){this.textContent=text;this.value=value},URLSearchParams,URL,Blob,Date,setTimeout,
  fetch:async(path,options={})=>{
    if(path==='/launch-session')assert.equal(location.hash,'','Launch ticket must leave the address bar before exchange');
    const response=await fetch(base+path,{...options,headers:{...options.headers,...(options.method==='POST'?{Origin:base}:{})}});
    if(path==='/launch-session'&&response.ok)sessionKeys=await response.clone().json();
    return response;
  }
});
function text(e){return e.textContent+' '+e.children.map(text).join(' ')}
async function waitFor(check){for(let i=0;i<200;i++){if(check())return;await new Promise(r=>setTimeout(r,10))}throw Error('UI initialization timeout')}
(async()=>{
  vm.runInContext(html.split('<script>')[1].split('</script>')[0],context,{filename:'ui.html'});
  await waitFor(()=>elements.status.textContent.includes('接続済み'));
  assert.equal(elements.admin.value,sessionKeys.admin_token);
  assert.equal(elements.modelcase.value,'');
  await elements.modelrun.onclick();
  assert.match(elements.runstatus.textContent,/対象案件を選んで/);
  await elements.fixedhold.onclick();
  assert.equal(elements.decision.textContent,'拒否');
  assert.match(elements.resultcase.textContent,/DEMO-HOLD.*固定デモ/);
  assert.match(text(elements.changes),/h_A, h_B/);
  await elements.fixedupdate.onclick();
  assert.equal(elements.decision.textContent,'保存');
  assert.match(elements.resultcase.textContent,/DEMO-UPDATE/);
  await elements.fixedupdate.onclick();
  assert.equal(elements.decision.textContent,'変更なし');
  elements.choosehold.onclick();
  elements.apikey.value='test-only-provider-key';elements.model.value='mock-test-only';
  await elements.modelrun.onclick();
  assert.equal(elements.decision.textContent,'変更なし');
  assert.match(elements.resultcase.textContent,/DEMO-HOLD.*実モデル経由/);
  await elements.export.onclick();
  assert.ok(download);
  const report=await (await fetch(download)).json();
  assert.equal(report.latest_run_in_this_page.source,'live_model');
  assert.equal(report.latest_run_in_this_page.model_metadata.model,'mock-test-only');
  assert.ok(report.history.some(row=>row.raw_sha256===report.latest_run_in_this_page.gate.raw_sha256));
  const serialized=JSON.stringify(report);
  for(const secret of [...Object.values(sessionKeys),'test-only-provider-key','ui-test-ticket'])assert.ok(!serialized.includes(secret));
  console.log('PASS: auto-connect, explicit case selection, reject, commit, no-op, mocked model path, export linkage, secret exclusion');
})().catch(error=>{console.error(error);process.exitCode=1});
