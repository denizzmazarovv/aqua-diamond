const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();

const p=await b.newPage({viewport:{width:1200,height:630},deviceScaleFactor:1,colorScheme:'light'});
await p.goto('file://'+process.cwd()+'/site/index.html');await p.waitForTimeout(1200);
await p.addStyleTag({content:'.hero{min-height:630px}.strip{display:none}.bubbles{display:none}'});
await p.evaluate(()=>{fitAll&&fitAll()});await p.waitForTimeout(300);
await p.screenshot({path:'site/og-image.png'});
const errs=[];for(const l of ['','uz/','en/']){const q=await b.newPage({viewport:{width:1360,height:900}});q.on('pageerror',e=>errs.push(l+e.message));await q.goto('file://'+process.cwd()+'/site/'+l+'index.html');await q.waitForTimeout(600);console.log(l||'ru',await q.evaluate(()=>[document.documentElement.lang,document.querySelector('h1').textContent,document.title.slice(0,40),document.querySelectorAll('script[type="application/ld+json"]').length]));}
console.log('errors',errs);await b.close()})();
