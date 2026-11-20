/* CO Resource Hub · legislative archive; data is kept separate from Administrative Regulations. */
"use strict";
const DATA_URL="/legislation/data/bills.json";
const CATEGORY_NAMES=["CDOC","County jails","Community corrections","Division of Youth Services","Juvenile justice","Medical care","Resident rights","Sentencing","Parole","Rehabilitation","Reentry","Oversight","Victims' rights","Other"];
const CATEGORIES={
"HB26-1052":["Victims' rights"],
"HB26-1064":["CDOC","Rehabilitation","Resident rights"],
"HB26-1123":["County jails","Victims' rights","Resident rights","Oversight"],
"HB26-1151":["CDOC"],
"SB26-036":["CDOC","Community corrections"],
"SB26-115":["Sentencing","CDOC"],
"SB26-159":["CDOC","Sentencing"],
"HB25-1013":["CDOC","Resident rights"],
"HB25-1026":["CDOC","Medical care","Resident rights"],
"HB25-1073":["Victims' rights","Sentencing"],
"HB25-1129":["CDOC","Reentry","Rehabilitation","Medical care"],
"HB25-1146":["Division of Youth Services","Juvenile justice"],
"SB25-190":["CDOC","Parole","Medical care"],
"SB25-208":["CDOC","Resident rights"],
"HB24-1054":["County jails","Oversight"],
"HB24-1170":["Division of Youth Services","Juvenile justice","Resident rights"],
"HB24-1216":["Division of Youth Services","Juvenile justice","Reentry"],
"HB23-1307":["Division of Youth Services","Juvenile justice"]
};
const $=id=>document.getElementById(id);
function node(tag,text,cls){const el=document.createElement(tag); if(text!==undefined&&text!==null)el.textContent=text;if(cls)el.className=cls;return el}
function link(label,url,cls){const a=node("a",label,cls);a.href=url;a.target="_blank";a.rel="noopener noreferrer";return a}
function internal(label,url,cls){const a=node("a",label,cls);a.href=url;return a}
function date(x){if(!x)return "Not verified";const d=/^(\d{4})-(\d{2})-(\d{2})$/.exec(x);return d?d[2]+"/"+d[3]+"/"+d[1]:x}
function resultKind(b){if(b.became_law_without_signature==="Yes")return "without-signature";if(b.governor_action==="Vetoed")return "vetoed";if(b.governor_action==="Signed")return "signed";if(/Postponed/i.test(b.status))return "failed";return "other"}
function resultName(kind){return({"signed":"Signed into law","without-signature":"Law without governor signature","vetoed":"Vetoed","failed":"Postponed / failed","other":"Other / unresolved"})[kind]}
function badge(b){const type=resultKind(b);return node("span",(type==="signed"?"✓ ":type==="vetoed"?"✕ ":type==="failed"?"– ":"○ ")+resultName(type),"status "+type)}
function tag(text){return node("span",text,"topic")}
function meta(label,value){const d=node("div",null,"fact");d.append(node("dt",label),node("dd",value||"Not verified"));return d}
async function getBills(){const response=await fetch(DATA_URL,{cache:"no-cache"});if(!response.ok)throw new Error("Dataset HTTP "+response.status);const data=await response.json();if(!Array.isArray(data.bills)||data.bills.length!==18)throw new Error("Unexpected starter dataset record count");return data}
const detailHref=b=>"/legislation/bill.html?bill="+encodeURIComponent(b.bill_id);
function setOptions(select,values){for(const value of values){const o=node("option",value);o.value=value;select.append(o)}}
function renderList(data){
const all=data.bills.slice().sort((a,b)=>Number(b.year)-Number(a.year)||a.bill_id.localeCompare(b.bill_id));
const counts={signed:0,vetoed:0,failed:0,withoutSignature:0};
for(const b of all){let k=resultKind(b);if(k==="without-signature")counts.withoutSignature++;else if(k in counts)counts[k]++}
$("record-total").textContent=all.length;
$("signed-total").textContent=counts.signed;
$("veto-total").textContent=counts.vetoed;
$("failed-total").textContent=counts.failed;
const years=[...new Set(all.map(b=>b.year))].sort().reverse();
setOptions($("year"),years);
setOptions($("category"),CATEGORY_NAMES);
setOptions($("outcome"),["Signed into law","Law without governor signature","Vetoed","Postponed / failed","Other / unresolved"]);
setOptions($("governor"),[...new Set(all.map(b=>b.governor).filter(Boolean))].sort());
function draw(){
const q=$("search").value.trim().toLowerCase(),y=$("year").value,category=$("category").value,outcome=$("outcome").value,gov=$("governor").value;
const shown=all.filter(b=>(!q||[b.bill_id,b.title,b.summary,b.house_prime_sponsors,b.senate_prime_sponsors,b.topics].join(" ").toLowerCase().includes(q))&&(!y||b.year===y)&&(!category||(CATEGORIES[b.bill_id]||[]).includes(category))&&(!outcome||resultName(resultKind(b))===outcome)&&(!gov||b.governor===gov));
const target=$("results");target.replaceChildren();
$("match-count").textContent=shown.length+" of "+all.length+" bills";
$("empty").hidden=shown.length>0;
for(const b of shown){
const article=node("article",null,"bill-card");
const top=node("div",null,"card-top");
top.append(node("span",b.bill_id,"bill-number"),badge(b));
article.append(top,internal(b.title,detailHref(b),"bill-title"));
article.append(node("p",b.summary,"summary"));
const sponsors=node("p",null,"sponsors");sponsors.append(node("strong","House: "),document.createTextNode(b.house_prime_sponsors||"Not listed"),document.createTextNode("  ·  "),node("strong","Senate: "),document.createTextNode(b.senate_prime_sponsors||"Not listed"));article.append(sponsors);
const topics=node("div",null,"topics");for(const t of CATEGORIES[b.bill_id]||[])topics.append(tag(t));article.append(topics);
const facts=node("dl",null,"mini-facts");facts.append(meta("Session",b.year),meta("Governor action",b.governor_action==="Signed"?"Signed "+date(b.governor_action_date):b.governor_action==="Vetoed"?"Vetoed "+date(b.veto_date):"None"));article.append(facts);
const actions=node("div",null,"actions");actions.append(internal("View bill details",detailHref(b),"action"),link("Official bill record ↗",b.official_bill_url,"action secondary"));article.append(actions);
target.append(article)}
}
for(const id of ["search","year","category","outcome","governor"])$(id).addEventListener(id==="search"?"input":"change",draw);
const param=new URLSearchParams(location.search);if(param.has("q"))$("search").value=param.get("q")||"";
draw();
}
function renderDetail(data){
const id=(new URLSearchParams(location.search).get("bill")||"").toUpperCase().trim();
const b=data.bills.find(x=>x.bill_id===id);
if(!b){$("detail").append(node("h1","Bill not found"),node("p","Choose a bill from the Legislative Archive."),internal("← Return to archive","/legislation/","action"));return}
document.title=b.bill_id+" — "+b.title+" | CO Resource Hub";
$("detail").append(internal("← Back to Legislative Archive","/legislation/","back"));
$("detail").append(node("div",b.bill_id+" · "+b.year+" "+b.session,"eyebrow"));
$("detail").append(node("h1",b.title));
const status=node("div",null,"detail-status");status.append(badge(b));$("detail").append(status);
$("detail").append(node("h2","Bill summary"),node("p",b.summary,"detail-summary"));
const categories=node("div",null,"topics");for(const c of CATEGORIES[b.bill_id]||[])categories.append(tag(c));$("detail").append(categories);
const sponsorSection=node("section",null,"detail-section");sponsorSection.append(node("h2","Legislative sponsors"));const sponsors=node("dl",null,"facts");sponsors.append(meta("House prime sponsors",b.house_prime_sponsors),meta("Senate prime sponsors",b.senate_prime_sponsors));sponsorSection.append(sponsors);$("detail").append(sponsorSection);
const outcomeSection=node("section",null,"detail-section");outcomeSection.append(node("h2","Legislative outcome & governor action"));const facts=node("dl",null,"facts");
facts.append(meta("Legislative disposition",b.legislative_outcome||b.status),meta("Governor",b.governor||"Not presented to governor"),meta("Governor action",b.governor_action));
if(b.signed_date)facts.append(meta("Governor signed",date(b.signed_date)));
if(b.veto_date)facts.append(meta("Governor vetoed",date(b.veto_date)));
if(b.became_law_without_signature==="Yes")facts.append(meta("Law without governor signature","Yes"));
facts.append(meta("Effective date",b.effective_date?date(b.effective_date):"Not yet verified — distinct from governor action date"));
outcomeSection.append(facts);
if(resultKind(b)==="vetoed")outcomeSection.append(node("p","This bill was vetoed and did not become law. Its proposed provisions must not be represented as enacted requirements.","alert"));
if(resultKind(b)==="failed")outcomeSection.append(node("p","This bill did not become law. The summary describes proposed measures, not enacted provisions.","alert"));
$("detail").append(outcomeSection);
const sources=node("section",null,"detail-section");sources.append(node("h2","Official legislative sources"));const l=node("div",null,"actions");l.append(link("Colorado General Assembly bill page ↗",b.official_bill_url,"action"));if(b.governor_action_source_url&&b.governor_action_source_url!==b.official_bill_url)l.append(link("Governor action source ↗",b.governor_action_source_url,"action secondary"));sources.append(l);sources.append(node("p","The official bill page contains available versions, amendments, signed-act or veto documents, fiscal notes and legislative history. Only documents available on that page should be treated as official.","small"));$("detail").append(sources);
if(b.notes)$("detail").append(node("p","Research note: "+b.notes,"small"));
$("detail").append(node("p","Source review: imported from the 18-record research master (November 20, 2026). Government bill pages are linked for verification; summaries are editorial and may omit amendments or legal exceptions. Effective dates not independently established are withheld.","small"));
}
(async()=>{try{const data=await getBills();if($("results"))renderList(data);if($("detail"))renderDetail(data)}catch(err){const e=$("error");e.hidden=false;e.textContent="The legislative dataset could not be loaded. Please refresh or use the official Colorado General Assembly website. ("+err.message+")";}})();
