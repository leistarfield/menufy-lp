#!/usr/bin/env python3
"""Tripfy 1.4 お知らせカルーセル（IG 1080x1350・7枚）。

Menufy の asc/v2/sns/build_sns.py と同じ HTML→playwright 方式。
出力: menufy-lp/tripfy/v/sns_tripfy_14_0X.png（ホスティング用）と ~/Desktop/Tripfyストア素材/SNS/（確認用）
"""
import os, shutil, subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
LP = HERE.parent.parent                       # menufy-lp
SHOTS = LP / 'asc-tripfy' / 'src' / 'ja'      # ScreenshotTests の生スクショ
SCEN = Path.home() / 'Developer/travel/design/mascot/shots/scenario'
MASCOT = Path.home() / 'Developer/travel/design/mascot'
ICON = LP / 'tripfy' / 'icon-256.png'
FONT = Path.home() / 'Developer/MenufyAndroid/app/src/main/res/font'
HOST_DIR = LP / 'tripfy' / 'v'
DESK = Path.home() / 'Desktop/Tripfyストア素材/SNS'

W, H = 540, 675   # css px（deviceScaleFactor 2 → 1080x1350）

css = f'''
@font-face{{font-family:'ZenMaru';font-weight:900;src:url('file://{FONT}/zenmarugothicblack.ttf')}}
@font-face{{font-family:'ZenMaru';font-weight:700;src:url('file://{FONT}/zenmarugothicbold.ttf')}}
@font-face{{font-family:'Nunito';font-weight:100 900;src:url('file://{FONT}/nunito_wght.ttf')}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#777;font-family:'ZenMaru','Hiragino Maru Gothic ProN',sans-serif;color:#1d3557}}
.a{{position:relative;overflow:hidden;width:{W}px;height:{H}px;background:#eaf3fb;margin:10px auto}}
.bl{{position:absolute;border-radius:50%}}
.m{{position:absolute;filter:drop-shadow(0 10px 16px rgba(14,50,87,.25))}}
.wm{{font-family:'Nunito';font-weight:900;color:#1d3557;letter-spacing:-.02em}}
.h{{position:absolute;left:40px;right:40px;font-weight:900;line-height:1.28;letter-spacing:.01em}}
.h em{{font-style:normal;color:#2c6fb0}}
.s{{position:absolute;left:40px;right:40px;font-weight:700;color:#5e7390;line-height:1.7}}
.tag{{position:absolute;left:40px;top:40px;font-family:'Nunito';font-weight:900;font-size:12px;letter-spacing:.14em;color:#2c6fb0;background:#d6e7f5;padding:6px 12px;border-radius:999px}}
.ph{{position:absolute;border-radius:28px;overflow:hidden;box-shadow:0 22px 44px -10px rgba(14,50,87,.35);border:6px solid #0e3257;background:#0e3257}}
.ph img{{display:block;width:100%}}
.card{{position:absolute;background:#fff;border-radius:16px;padding:12px 14px;box-shadow:0 12px 30px -8px rgba(14,50,87,.25);font-size:13px;font-weight:700;line-height:1.4}}
.card small{{display:block;font-size:10px;color:#5e7390;font-weight:700;margin-top:2px}}
.pg{{position:absolute;right:40px;top:44px;font-family:'Nunito';font-weight:900;font-size:12px;color:#9fb4cc;letter-spacing:.1em}}
.cta{{position:absolute;left:40px;right:40px;bottom:44px;background:#2c6fb0;color:#fff;border-radius:18px;padding:16px;text-align:center;font-weight:900;font-size:17px}}
'''

def blobs():
    return ('<div class="bl" style="width:420px;height:420px;background:#bfdbf2;opacity:.7;left:-160px;top:-180px"></div>'
            '<div class="bl" style="width:360px;height:360px;background:#d6e7f5;opacity:.9;right:-140px;bottom:-200px"></div>')

def phone(src, left, top, width, extra=''):
    return f'<div class="ph" style="left:{left}px;top:{top}px;width:{width}px;{extra}"><img src="file://{src}"></div>'

secs = []
# 1 表紙
secs.append(f'''<section class="a" data-out="sns_tripfy_14_01">{blobs()}
<div class="tag">NEW · v1.4</div>
<div style="position:absolute;left:40px;top:92px;display:flex;align-items:center;gap:12px"><img src="file://{ICON}" style="width:44px;height:44px;border-radius:12px;box-shadow:0 8px 16px rgba(14,50,87,.25)"><div class="wm" style="font-size:34px">Tripfy</div></div>
<div class="h" style="top:170px;font-size:40px">旅の予約、<br><em>スクショ送るだけ。</em></div>
<div class="s" style="top:300px;font-size:15px">航空券・ホテル・レストラン。バラバラの予約確認を AI が読んで、ひとつの旅程に。</div>
<img class="m" src="file://{MASCOT}/base.png" style="width:330px;left:120px;top:360px">
<div class="pg">1 / 7</div></section>''')

# 2 課題
secs.append(f'''<section class="a" data-out="sns_tripfy_14_02">{blobs()}
<div class="h" style="top:70px;font-size:34px">予約確認、<br>どこに行った？</div>
<div class="s" style="top:170px;font-size:15px">メール、予約アプリ、LINE、スクショ…。<br>出発の朝に探し回るの、もうやめたい。</div>
<div class="card" style="left:40px;top:290px;width:260px">✈️ ANA e チケット<small>メールの奥、3 週間前</small></div>
<div class="card" style="left:200px;top:360px;width:280px;transform:rotate(3deg)">🏨 ホテル予約確認<small>予約サイトのアプリ内</small></div>
<div class="card" style="left:60px;top:440px;width:240px;transform:rotate(-3deg)">🍜 レストラン予約<small>LINE のトーク</small></div>
<div class="card" style="left:250px;top:520px;width:230px;transform:rotate(2deg)">🚄 新幹線<small>スクショだけ</small></div>
<img class="m" src="file://{MASCOT}/puzzled.png" style="width:150px;left:360px;top:120px;transform:rotate(6deg)">
<div class="pg">2 / 7</div></section>''')

# 3 取り込み
secs.append(f'''<section class="a" data-out="sns_tripfy_14_03">{blobs()}
<div class="tag">AI 取り込み</div>
<div class="h" style="top:84px;font-size:32px">スクショを共有すると、<br>AI が<em>読んで並べる。</em></div>
<div class="s" style="top:186px;font-size:14px">便名・日時・予約番号・場所まで。確認して保存するだけ。メール転送でも OK。</div>
{phone(SHOTS/'03-import-confirm.png', 120, 270, 300)}
<img class="m" src="file://{MASCOT}/waiting.png" style="width:120px;left:20px;top:520px;transform:rotate(-6deg)">
<div class="pg">3 / 7</div></section>''')

# 4 タイムライン＋地図
secs.append(f'''<section class="a" data-out="sns_tripfy_14_04">{blobs()}
<div class="h" style="top:70px;font-size:32px">旅の全体像が、<br><em>時系列と地図で。</em></div>
{phone(SHOTS/'01-timeline.png', 30, 200, 250)}
{phone(SHOTS/'02-map.png', 270, 260, 250)}
<div class="pg">4 / 7</div></section>''')

# 5 乗り継ぎ
secs.append(f'''<section class="a" data-out="sns_tripfy_14_05">{blobs()}
<div class="tag">v1.4 で改善</div>
<div class="h" style="top:84px;font-size:32px">乗り継ぎも往復も、<br><em>ひとつの旅に。</em></div>
<div class="s" style="top:186px;font-size:14px">経由地で旅が分かれなくなりました。乗り継ぎの待ち時間もタイムラインに。</div>
{phone(SCEN/'07-timeline.png', 120, 270, 300)}
<div class="pg">5 / 7</div></section>''')

# 6 AI プラン
secs.append(f'''<section class="a" data-out="sns_tripfy_14_06">{blobs()}
<div class="tag">AI プラン</div>
<div class="h" style="top:84px;font-size:32px">空き時間は、<br>AI に<em>相談する。</em></div>
<div class="s" style="top:186px;font-size:14px">自分の旅の流儀を覚えさせて、候補から選ぶ。「朝はゆっくりで」と言えば直してくれる。</div>
{phone(SHOTS/'04-ai-plan.png', 120, 270, 300)}
<div class="pg">6 / 7</div></section>''')

# 7 相棒 + CTA
secs.append(f'''<section class="a" data-out="sns_tripfy_14_07">{blobs()}
<div class="h" style="top:70px;font-size:34px;text-align:center">旅の相棒、<br>新しくなりました。</div>
<div class="s" style="top:170px;font-size:14px;text-align:center">待ち時間や空っぽの画面で、顔を出します。</div>
<img class="m" src="file://{MASCOT}/celebrate.png" style="width:300px;left:120px;top:230px">
<div style="position:absolute;left:0;right:0;top:540px;text-align:center;font-family:'Nunito';font-weight:900;font-size:13px;color:#5e7390;letter-spacing:.08em">iOS · 無料ではじめられます</div>
<div class="cta">App Store で「Tripfy」を検索</div>
<div class="pg">7 / 7</div></section>''')

html = f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{"".join(secs)}</body></html>'
(HERE / 'carousel.html').write_text(html)
(HERE / 'render.js').write_text(r'''
const { chromium } = require('playwright'); const path=require('path');
(async()=>{const b=await chromium.launch({channel:'chrome'});const p=await b.newPage({viewport:{width:900,height:900},deviceScaleFactor:2});
await p.goto('file://'+process.argv[2]);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(600);
for(const el of await p.$$('.a')){const n=await el.getAttribute('data-out');await el.scrollIntoViewIfNeeded();await el.screenshot({path:path.join(process.argv[3],n+'.png')});console.log('rendered',n);}
await b.close();})();''')

HOST_DIR.mkdir(parents=True, exist_ok=True)
DESK.mkdir(parents=True, exist_ok=True)
env = dict(os.environ, NODE_PATH=str(LP / 'asc-tripfy' / 'node_modules'))
subprocess.run(['node', str(HERE / 'render.js'), str(HERE / 'carousel.html'), str(HOST_DIR)], check=True, env=env)
from PIL import Image
for f in sorted(HOST_DIR.glob('sns_tripfy_14_*.png')):
    im = Image.open(f)
    assert im.size == (1080, 1350), (f.name, im.size)
    shutil.copy(f, DESK / f.name)
    print(f.name, im.size)
