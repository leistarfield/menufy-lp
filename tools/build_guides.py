#!/usr/bin/env python3
"""SEO guide pages (/guide/<key>/) from the "menu words" series, in the LP design."""
import os, sys, json, re, html
sys.path.insert(0, os.path.expanduser('~/Developer/menufy-lp/asc/v2/edu'))
from build_edu import SERIES
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_STORE='https://apps.apple.com/app/id6760161339'; PLAY='https://play.google.com/store/apps/details?id=com.menufy.app'
META={'thai':('タイ','タイ料理','バンコクの屋台や食堂'),'korean':('韓国','韓国料理','ソウルの食堂'),'vietnam':('ベトナム','ベトナム料理','ハノイ・ホーチミンの食堂'),'italy':('イタリア','イタリア料理','ローマやフィレンツェのトラットリア')}
CSS='''*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--cream:#FFF7EE;--card:#fff;--coral:#FF6B47;--deep:#E4522F;--peach:#FFE3D2;--mint:#D4F1E6;--ink:#3B2C26;--muted:#8C7B73;--line:#F2E5DA}
body{font-family:'Zen Maru Gothic','Hiragino Maru Gothic ProN',sans-serif;background:var(--cream);color:var(--ink);-webkit-font-smoothing:antialiased;font-weight:500;line-height:1.8}
nav{display:flex;align-items:center;justify-content:space-between;padding:0 24px;height:60px;background:rgba(255,247,238,.95);border-bottom:1px solid var(--line);position:sticky;top:0}
.nlogo{display:flex;align-items:center;gap:10px;text-decoration:none}.nicon{width:34px;height:34px;object-fit:contain}.ntext{font-family:'Nunito',sans-serif;font-size:20px;font-weight:800;color:var(--ink)}
.nback{font-size:13px;color:var(--muted);text-decoration:none;font-weight:700}
.wrap{max-width:720px;margin:0 auto;padding:40px 20px 90px}
.lbl{font-size:12px;letter-spacing:.14em;color:var(--deep);font-weight:900}
h1{font-size:clamp(26px,5vw,36px);font-weight:900;line-height:1.35;margin:10px 0 14px}
.lead{color:var(--muted);margin-bottom:28px}
.word{background:var(--card);border-radius:20px;padding:20px 22px;margin-bottom:12px;box-shadow:0 8px 20px rgba(59,44,38,.06)}
.word .w{font-size:26px;font-weight:900;line-height:1.3}.word .r{color:var(--deep);font-weight:700;font-size:14px;margin-top:2px}.word .m{color:var(--muted);font-size:14px;margin-top:6px}
.cta{margin-top:36px;background:var(--card);border-radius:24px;padding:26px 24px;text-align:center;box-shadow:0 14px 30px rgba(59,44,38,.1)}
.cta .mas{display:flex;justify-content:center;gap:0;margin-bottom:10px}.cta .mas img{width:64px;height:64px;object-fit:contain;margin:0 -4px;filter:drop-shadow(0 8px 14px rgba(59,44,38,.2))}
.cta h2{font-size:22px;font-weight:900;margin-bottom:8px}.cta p{color:var(--muted);font-size:14px;margin-bottom:16px}
.btn{display:inline-block;background:var(--coral);color:#fff;text-decoration:none;font-weight:800;padding:14px 26px;border-radius:18px;box-shadow:0 10px 24px rgba(255,107,71,.28);margin:4px}
.btn.alt{background:var(--card);color:var(--ink);border:1.5px solid var(--line);box-shadow:none}
.more{margin-top:40px}.more h3{font-size:15px;color:var(--muted);margin-bottom:10px}.more a{display:inline-block;margin:4px 8px 4px 0;font-weight:700;color:var(--deep);text-decoration:none;background:var(--peach);padding:8px 14px;border-radius:100px;font-size:14px}
footer{text-align:center;color:var(--muted);font-size:12px;padding:30px}
'''
def page(key, d):
    country, cuisine, where = META[key]
    title_txt = re.sub(r'<[^>]+>', '', d['title'])
    words = d['words']
    faq = [{"@type":"Question","name":f"{w}（{r}）はどんな料理・意味？","acceptedAnswer":{"@type":"Answer","text":m}} for w,r,m in words]
    ld = {"@context":"https://schema.org","@type":"Article","headline":title_txt,"inLanguage":"ja","author":{"@type":"Organization","name":"Menufy"},"publisher":{"@type":"Organization","name":"Menufy","logo":{"@type":"ImageObject","url":"https://menufyjp.com/icon-512.png"}},"mainEntityOfPage":f"https://menufyjp.com/guide/{key}/","image":f"https://menufyjp.com/menufy/v/edu_{key}_01.png","datePublished":"2026-09-13"}
    ldfaq = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":faq}
    desc = f"{where}で使う{cuisine}のメニュー用語10語の読み方と意味。辛くしない・パクチー抜き・お会計の言い方も。全部覚えなくても、Menufyなら撮るだけで読めた順に翻訳。"
    items = ''.join(f'<div class="word"><div class="w">{html.escape(w)}</div><div class="r">{html.escape(r)}</div><div class="m">{html.escape(m)}</div></div>' for w,r,m in words)
    more = ''.join(f'<a href="/guide/{k}/">{META[k][0]}</a>' for k in SERIES if k != key)
    mas = ''.join(f'<img src="/assets/mascot-{n}.png" alt="">' for n in ('sushi','ramen','gyoza','omurice','pudding'))
    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title_txt} | Menufy</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://menufyjp.com/guide/{key}/">
<link rel="icon" href="/favicon.ico" sizes="32x32"><link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png"><meta name="theme-color" content="#FF6B47">
<meta name="apple-itunes-app" content="app-id=6760161339">
<meta property="og:type" content="article"><meta property="og:site_name" content="Menufy"><meta property="og:title" content="{title_txt}"><meta property="og:description" content="{desc}"><meta property="og:url" content="https://menufyjp.com/guide/{key}/"><meta property="og:image" content="https://menufyjp.com/menufy/v/edu_{key}_01.png"><meta property="og:image:width" content="1080"><meta property="og:image:height" content="1350"><meta property="og:locale" content="ja_JP">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{title_txt}"><meta name="twitter:description" content="{desc}"><meta name="twitter:image" content="https://menufyjp.com/menufy/v/edu_{key}_01.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@500;700;900&family=Nunito:wght@700;800&display=swap" rel="stylesheet">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(ldfaq, ensure_ascii=False)}</script>
<style>{CSS}</style>
</head>
<body>
<nav><a href="/" class="nlogo"><img src="/assets/mascot-sushi.png" alt="" class="nicon"><span class="ntext">Menufy</span></a><a href="/" class="nback">← Menufyについて</a></nav>
<main class="wrap">
  <div class="lbl">{d['flag']} {cuisine}のメニューの読み方</div>
  <h1>{d['title'].replace('<em>','<span style="color:var(--deep)">').replace('</em>','</span>')}</h1>
  <p class="lead">{d['cover_sub']} {where}で実際によく見る言葉から選びました。</p>
  {items}
  <div class="cta"><div class="mas">{mas}</div><h2>全部覚えなくても大丈夫。</h2><p>Menufyなら、メニューを撮るだけで読めた順に翻訳。アレルギーの警告と会計チェックつき。まず5回無料、サブスクなし。</p><a class="btn" href="{APP_STORE}">App Storeで入手</a><a class="btn alt" href="{PLAY}">Google Play</a></div>
  <div class="more"><h3>ほかの国の読み方</h3>{more}</div>
</main>
<footer>© 2026 Menufy · <a href="/privacy.html" style="color:inherit">プライバシー</a></footer>
</body>
</html>
'''
os.makedirs(os.path.join(ROOT,'guide'), exist_ok=True)
for key, d in SERIES.items():
    os.makedirs(os.path.join(ROOT,'guide',key), exist_ok=True)
    open(os.path.join(ROOT,'guide',key,'index.html'),'w',encoding='utf-8').write(page(key,d))
# index page
links=''.join(f'<a class="card" href="/guide/{k}/"><div class="f">{SERIES[k]["flag"]}</div><div class="t">{re.sub(r"<[^>]+>","",SERIES[k]["title"])}</div></a>' for k in SERIES)
open(os.path.join(ROOT,'guide','index.html'),'w',encoding='utf-8').write(f'''<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>海外メニューの読み方ガイド | Menufy</title><meta name="description" content="タイ・韓国・ベトナム・イタリアのメニュー用語、この10語が読めれば困らない。Menufy が選んだ最低限の言葉と意味。"><link rel="canonical" href="https://menufyjp.com/guide/"><link rel="icon" href="/favicon.ico" sizes="32x32"><meta name="apple-itunes-app" content="app-id=6760161339"><link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@500;700;900&family=Nunito:wght@700;800&display=swap" rel="stylesheet"><style>{CSS}.card{{display:flex;gap:14px;align-items:center;background:var(--card);border-radius:20px;padding:18px 20px;margin-bottom:12px;text-decoration:none;color:var(--ink);box-shadow:0 8px 20px rgba(59,44,38,.06)}}.card .f{{font-size:28px}}.card .t{{font-weight:900}}</style></head><body>
<nav><a href="/" class="nlogo"><img src="/assets/mascot-sushi.png" alt="" class="nicon"><span class="ntext">Menufy</span></a><a href="/" class="nback">← Menufyについて</a></nav>
<main class="wrap"><div class="lbl">GUIDE</div><h1>海外メニューの読み方ガイド</h1><p class="lead">国ごとに「この10語が読めれば困らない」言葉をまとめました。</p>{links}</main>
<footer>© 2026 Menufy</footer></body></html>''')
# sitemap
sp=os.path.join(ROOT,'sitemap.xml'); s=open(sp,encoding='utf-8').read()
if '/guide/' not in s:
    add='  <url><loc>https://menufyjp.com/guide/</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>\n' + ''.join(f'  <url><loc>https://menufyjp.com/guide/{k}/</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>\n' for k in SERIES)
    s=s.replace('</urlset>', add+'</urlset>'); open(sp,'w',encoding='utf-8').write(s)
print('guides ok:', list(SERIES))
