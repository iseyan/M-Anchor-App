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
  scrollIntoView() {}
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
  await waitFor(()=>elements.status.textContent.startsWith('Connected'));
  assert.match(elements.status.textContent,/接続済み/);
  assert.match(html,/<html lang="en">/);
  assert.match(html,/lang="ja"/);
  assert.match(html,/Export records as JSON<span[^>]*lang="ja">確認記録をJSONで保存/);
  assert.equal(elements.admin.value,sessionKeys.admin_token);
  assert.equal(elements.modelcase.value,'');
  await elements.modelrun.onclick();
  assert.match(elements.runstatus.textContent,/^Select a target case.*対象案件を選んで/);
  elements.proposal.value="{";
  await elements.submit.onclick();
  assert.match(elements.runstatus.textContent,/^The proposal could not be read as JSON.*JSON/);
  elements.proposal.value="null";
  await elements.submit.onclick();
  assert.match(elements.runstatus.textContent,/^Specify case_id.*case_idを指定/);
  elements.choosehold.onclick();
  assert.equal(elements.scenario.value,'unsupported_resolution');
  await elements.scenariofixed.onclick();
  assert.equal(elements.decision.textContent,'Rejected / 拒否');
  assert.match(elements.resultcase.textContent,/DEMO-HOLD.*Fixed scenario/);
  assert.match(elements.statesummary.textContent,/^Record unchanged/);
  assert.match(elements.inputsummary.textContent,/^No model input/);
  assert.match(text(elements.changes),/h_A, h_B/);
  elements.chooseupdate.onclick();
  await elements.scenariofixed.onclick();
  assert.equal(elements.decision.textContent,'Saved / 保存');
  assert.match(elements.statesummary.textContent,/^Record updated/);
  await elements.scenariofixed.onclick();
  assert.equal(elements.decision.textContent,'No change / 変更なし');
  for(const id of ['forged_admission','authority_override','reference_tampering']){
    elements.scenario.value=id;elements.scenario.onchange();
    await elements.scenariofixed.onclick();
    assert.equal(elements.decision.textContent,'Rejected / 拒否');
    assert.match(elements.statesummary.textContent,/^Record unchanged/);
  }
  elements.scenario.value='preserve_uncertainty';elements.scenario.onchange();
  await elements.scenariofixed.onclick();
  assert.equal(elements.decision.textContent,'No change / 変更なし');
  elements.choosehold.onclick();
  const attackInput='  <img src=x onerror=example>\n合成した入力です。\n';
  elements.message.value=attackInput;
  elements.apikey.value='test-only-provider-key';elements.model.value='mock-test-only';
  await elements.modelrun.onclick();
  assert.equal(elements.decision.textContent,'No change / 変更なし');
  assert.match(elements.resultcase.textContent,/DEMO-HOLD.*Model API.*モデルAPI経由/);
  assert.equal(elements.rawinput.textContent,attackInput);
  assert.match(elements.statesummary.textContent,/^Record unchanged/);
  await elements.export.onclick();
  assert.ok(download);
  const report=await (await fetch(download)).json();
  assert.equal(report.schema,'m-anchor-app-observation/v2');
  assert.equal(report.history.length,8);
  assert.equal(report.history[0].execution.source,'live_model');
  assert.equal(report.history[0].execution.model_metadata.model,'mock-test-only');
  assert.equal(report.history[7].execution.source,'fixed_scenario');
  assert.equal(report.history[0].execution.exercise.input_text,attackInput);
  assert.equal(report.history[0].execution.exercise.input_sha256,require('node:crypto').createHash('sha256').update(attackInput).digest('hex'));
  assert.equal(report.history[7].execution.exercise.input_text,null);
  const firstButton=elements.history.children[0].children[1].children[7].children[6].children[0];
  await firstButton.onclick();
  assert.equal(elements.decision.textContent,'Rejected / 拒否');
  assert.match(elements.recordinfo.textContent,/履歴 #1/);
  assert.match(elements.rawinput.textContent,/^Not applicable/);
  assert.match(elements.rawproposal.textContent,/DEMO-HOLD/);
  assert.match(elements.readback.textContent,/^The authoritative record.*一致を確認/);
  await elements.export.onclick();
  const reopenedReport=await (await fetch(download)).json();
  assert.deepEqual(reopenedReport.history,report.history,'Viewing an old record must not replace export history');
  const latestButton=elements.history.children[0].children[1].children[0].children[6].children[0];
  await latestButton.onclick();
  assert.equal(elements.rawinput.textContent,attackInput);
  elements.message.value='__mock_failure__';
  await elements.modelrun.onclick();
  assert.match(elements.statesummary.textContent,/^Outcome not verified/);
  assert.equal(elements.rawinput.textContent,'');
  await elements.export.onclick();
  const failedReport=await (await fetch(download)).json();
  assert.equal(failedReport.history.length,8,'An API failure is not a gate rejection');
  const serialized=JSON.stringify(report);
  for(const secret of [...Object.values(sessionKeys),'test-only-provider-key','ui-test-ticket'])assert.ok(!serialized.includes(secret));
  console.log('PASS: V1 bilingual scenarios, four fixed attacks, valid update and no-op controls, exact model input trace, past-record details, full export, failure is unverified, secret exclusion');
})().catch(error=>{console.error(error);process.exitCode=1});
