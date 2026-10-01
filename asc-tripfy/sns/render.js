
const { chromium } = require('playwright'); const path=require('path');
(async()=>{const b=await chromium.launch({channel:'chrome'});const p=await b.newPage({viewport:{width:900,height:900},deviceScaleFactor:2});
await p.goto('file://'+process.argv[2]);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(600);
for(const el of await p.$$('.a')){const n=await el.getAttribute('data-out');await el.scrollIntoViewIfNeeded();await el.screenshot({path:path.join(process.argv[3],n+'.png')});console.log('rendered',n);}
await b.close();})();