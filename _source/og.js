const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
const p=await b.newPage({viewport:{width:1200,height:630},colorScheme:'light'});
await p.goto('file://'+process.cwd()+'/site/index.html');await p.waitForTimeout(800);
await p.evaluate(()=>{
  const cans=['anarfresh-045','mustang-classic','moxito-lime'].map((f,i)=>'<img src="img/'+f+'.webp" style="height:'+(i==1?400:350)+'px;filter:drop-shadow(0 18px 16px rgba(3,30,33,.3))">').join('');
  document.body.innerHTML=`<div style="width:1200px;height:630px;box-sizing:border-box;padding:64px 0 0 72px;display:grid;grid-template-columns:620px 1fr;background:radial-gradient(60% 90% at 82% 50%,#bfe1e5,#eef5f5 72%);overflow:hidden;font-family:var(--body);color:#0b2629">
   <div style="display:grid;align-content:start;gap:26px">
    <div style="display:flex;align-items:center;gap:14px;font:700 40px/1 var(--display);letter-spacing:.06em"><img src="img/brand/emblem-192.webp" width="56" height="56" style="border-radius:12px">AQUADIAMOND</div>
    <div style="font:500 20px/1 var(--mono);letter-spacing:.12em;color:#08798a;text-transform:uppercase">Производитель напитков · Ташкент</div>
    <div style="font:800 italic 92px/.86 var(--display);text-transform:uppercase">Розлив <span style="color:#08798a">под вашей маркой</span></div>
    <div style="display:flex;gap:0;border:3px solid #0b2629;border-radius:20px;overflow:hidden;width:fit-content;margin-top:6px">
      <div style="padding:14px 22px;background:#08798a;color:#fff"><b style="font:800 italic 44px/1 var(--display)">700 сум</b><div style="font-size:16px">от, за банку</div></div>
      <div style="padding:14px 22px"><b style="font:800 italic 44px/1 var(--display)">12 000</b><div style="font-size:16px;color:#4b6669">банок, мин. партия</div></div>
      <div style="padding:14px 22px;border-left:1px solid #cfdfe0"><b style="font:800 italic 44px/1 var(--display)">12</b><div style="font-size:16px;color:#4b6669">стран экспорта</div></div>
    </div>
   </div>
   <div style="display:flex;align-items:flex-end;justify-content:center;gap:8px;padding:0 36px 44px 0">${cans}</div></div>`;
});
await p.waitForTimeout(400);await p.screenshot({path:'site/og-image.png'});await b.close()})();
