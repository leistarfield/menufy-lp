#!/usr/bin/env python3
"""App Store 商品ページの「ヘッダー」(3840x1646, 21:9) と「検索結果」(3840x2560, 3:2) 画像。
Apple の仕様: https://developer.apple.com/help/app-store-connect/reference/app-information/creative-assets-specifications/
透過なし。iOS 27 以降で表示。ja / en の 4 枚を ~/Desktop/Tripfyストア素材/creative/ に出す。
"""
import os, subprocess
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
LP = HERE.parent.parent
FONT = Path.home() / 'Developer/MenufyAndroid/app/src/main/res/font'
MASCOT = Path.home() / 'Developer/travel/design/mascot'
SHOT = LP / 'asc-tripfy' / 'src'          # ja/01-timeline.png, en/01-timeline.png
ICON = LP / 'tripfy' / 'icon-256.png'
OUT = Path.home() / 'Desktop/Tripfyストア素材/creative'

COPY = {
    'ja': {'h': '旅の予約、<br><em>スクショ送るだけ。</em>', 'sub': '航空券・ホテル・レストラン。バラバラの予約確認を AI が読んで、ひとつの旅程に。', 'tag': 'Every trip, in one place.'},
    'en': {'h': 'Paste a booking.<br><em>Get a trip.</em>', 'sub': 'Flights, hotels, restaurants — AI reads your confirmations and builds one itinerary.', 'tag': 'Every trip, in one place.'},
}

css = f'''
@font-face{{font-family:'ZenMaru';font-weight:900;src:url('file://{FONT}/zenmarugothicblack.ttf')}}
@font-face{{font-family:'ZenMaru';font-weight:700;src:url('file://{FONT}/zenmarugothicbold.ttf')}}
@font-face{{font-family:'Nunito';font-weight:100 900;src:url('file://{FONT}/nunito_wght.ttf')}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#555;font-family:'ZenMaru','Hiragino Maru Gothic ProN',sans-serif;color:#1d3557}}
.a{{position:relative;overflow:hidden;background:linear-gradient(135deg,#eaf3fb 0%,#d6e7f5 60%,#bfdbf2 100%);margin:20px auto}}
.bl{{position:absolute;border-radius:50%;background:#fff;opacity:.35}}
.wm{{font-family:'Nunito';font-weight:900;letter-spacing:-.02em;color:#1d3557}}
h1{{font-weight:900;line-height:1.2;letter-spacing:.01em;color:#1d3557}}
h1 em{{font-style:normal;color:#2c6fb0}}
.sub{{font-weight:700;color:#5e7390;line-height:1.6}}
.tag{{font-family:'Nunito';font-weight:900;letter-spacing:.12em;color:#2c6fb0;text-transform:uppercase}}
.m{{position:absolute;filter:drop-shadow(0 40px 60px rgba(14,50,87,.28))}}
.ph{{position:absolute;border-radius:90px;overflow:hidden;border:18px solid #0e3257;background:#0e3257;box-shadow:0 60px 120px -30px rgba(14,50,87,.45)}}
.ph img{{display:block;width:100%}}
.brand{{position:absolute;display:flex;align-items:center;gap:28px}}
.brand img{{border-radius:28%;box-shadow:0 20px 40px rgba(14,50,87,.25)}}
'''

def section(kind, lang):
    c = COPY[lang]
    shot = SHOT / lang / '01-timeline.png'
    if kind == 'header':   # 3840x1646
        W, H = 3840, 1646
        return f'''<section class="a" data-out="header_{lang}" style="width:{W}px;height:{H}px">
<div class="bl" style="width:1800px;height:1800px;left:-500px;top:-900px"></div>
<div class="bl" style="width:1400px;height:1400px;right:-300px;bottom:-900px;opacity:.25"></div>
<div class="brand" style="left:220px;top:200px"><img src="file://{ICON}" style="width:120px;height:120px"><div class="wm" style="font-size:96px">Tripfy</div></div>
<h1 style="position:absolute;left:220px;top:420px;font-size:136px;width:1500px">{c['h']}</h1>
<div class="sub" style="position:absolute;left:224px;top:{860 if lang=='ja' else 820}px;font-size:48px;width:1400px">{c['sub']}</div>
<div class="tag" style="position:absolute;left:226px;top:{1060 if lang=='ja' else 1020}px;font-size:40px">{c['tag']}</div>
<div class="ph" style="left:2000px;top:140px;width:760px"><img src="file://{shot}"></div>
<img class="m" src="file://{MASCOT}/base.png" style="width:1050px;left:2780px;top:260px">
</section>'''
    else:                  # search 3840x2560
        W, H = 3840, 2560
        return f'''<section class="a" data-out="search_{lang}" style="width:{W}px;height:{H}px">
<div class="bl" style="width:2200px;height:2200px;left:-700px;top:-1100px"></div>
<div class="bl" style="width:1600px;height:1600px;right:-400px;bottom:-1000px;opacity:.25"></div>
<div class="brand" style="left:240px;top:240px"><img src="file://{ICON}" style="width:140px;height:140px"><div class="wm" style="font-size:112px">Tripfy</div></div>
<h1 style="position:absolute;left:240px;top:520px;font-size:168px;width:1700px">{c['h']}</h1>
<div class="sub" style="position:absolute;left:244px;top:{1080 if lang=='ja' else 1040}px;font-size:56px;width:1500px">{c['sub']}</div>
<div class="tag" style="position:absolute;left:246px;top:{1320 if lang=='ja' else 1280}px;font-size:44px">{c['tag']}</div>
<div class="ph" style="left:2080px;top:220px;width:900px"><img src="file://{shot}"></div>
<img class="m" src="file://{MASCOT}/base.png" style="width:1250px;left:2700px;top:1060px">
</section>'''

secs = [section(k, l) for l in ('ja', 'en') for k in ('header', 'search')]
html = f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{"".join(secs)}</body></html>'
(HERE / 'creative.html').write_text(html)
(HERE / 'render.js').write_text(r'''
const { chromium } = require('playwright'); const path=require('path');
(async()=>{const b=await chromium.launch({channel:'chrome'});const p=await b.newPage({viewport:{width:4000,height:2700},deviceScaleFactor:1});
await p.goto('file://'+process.argv[2]);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(800);
for(const el of await p.$$('.a')){const n=await el.getAttribute('data-out');await el.scrollIntoViewIfNeeded();await el.screenshot({path:path.join(process.argv[3],n+'.png'),omitBackground:false});console.log('rendered',n);}
await b.close();})();''')
OUT.mkdir(parents=True, exist_ok=True)
env = dict(os.environ, NODE_PATH=str(LP / 'asc-tripfy' / 'node_modules'))
subprocess.run(['node', str(HERE / 'render.js'), str(HERE / 'creative.html'), str(OUT)], check=True, env=env)
for f in sorted(OUT.glob('*.png')):
    im = Image.open(f).convert('RGB')   # 透過なし
    im.save(f)
    exp = (3840, 1646) if f.name.startswith('header') else (3840, 2560)
    assert im.size == exp, (f.name, im.size)
    print(f.name, im.size)
