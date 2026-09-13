#!/usr/bin/env python3
"""Builds index.html (JA) and en/index.html (EN) in the 2026-09 redesign.

Keeps, verbatim, from the previous pages: the <head> SEO/OGP/Pixel/JSON-LD
blocks (fonts, favicon, theme-color and the <style> are replaced), the
nav/mobile-menu/sticky-bar/smart-routing scripts, every fbq() call and the
tracking script at the end. Only the visual layer and the copy change.
"""
import json, re, sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@500;700;900&family=Nunito:wght@600;700;800&display=swap" rel="stylesheet">'
FAVICON = "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'><rect width='64' height='64' rx='16' fill='%23FF6B47'/><circle cx='29' cy='29' r='12' stroke='white' stroke-width='4' fill='none'/><line x1='38' y1='38' x2='51' y2='51' stroke='white' stroke-width='4' stroke-linecap='round'/></svg>"

CSS = r"""
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --cream:#FFF7EE;--card:#FFFFFF;--card2:#FFF1E6;
  --coral:#FF6B47;--deep:#E4522F;--peach:#FFE3D2;--peach-line:#FFC7AE;
  --mint:#D4F1E6;--mint-ink:#2E8C6A;--butter:#FFEBB0;--butter-ink:#9A6B00;--honey:#F0B33E;
  --ink:#3B2C26;--muted:#8C7B73;--faint:#B8A9A1;--line:#F2E5DA;
  --warn:#E5484D;--warn-tint:#FFE4E4;--ink-bg:#2B1F1B;
  --sh:0 8px 20px rgba(59,44,38,.06);--sh2:0 14px 30px rgba(59,44,38,.12);--sh-coral:0 10px 24px rgba(255,107,71,.28);
  --ease:cubic-bezier(.4,0,.2,1);
}
html{scroll-behavior:smooth;overflow-x:hidden}
body{font-family:'Zen Maru Gothic','Nunito','Hiragino Maru Gothic ProN','Rounded Mplus 1c',system-ui,sans-serif;background:var(--cream);color:var(--ink);overflow-x:hidden;-webkit-font-smoothing:antialiased;font-weight:500}
.num{font-family:'Nunito','Zen Maru Gothic',sans-serif}
img{max-width:100%;display:block}

/* NAV */
nav{position:fixed;top:0;left:0;right:0;z-index:100;display:flex;align-items:center;justify-content:space-between;padding:0 48px;height:64px;background:rgba(255,247,238,.9);backdrop-filter:saturate(180%) blur(18px);border-bottom:1px solid rgba(59,44,38,.06)}
.nlogo{display:flex;align-items:center;gap:10px;text-decoration:none}
.nicon{width:38px;height:38px;object-fit:contain;filter:drop-shadow(0 3px 6px rgba(59,44,38,.18))}
.ntext{font-family:'Nunito',sans-serif;font-size:20px;font-weight:800;color:var(--ink);letter-spacing:.03em}
.nlinks{display:flex;align-items:center;gap:26px}
.nlink{font-size:14px;color:var(--ink);text-decoration:none;font-weight:700;opacity:.75;transition:opacity .2s}
.nlink:hover{opacity:1}
.ncta{display:inline-flex;align-items:center;height:40px;padding:0 18px;background:var(--coral);color:#fff;font-size:14px;font-weight:800;text-decoration:none;border-radius:999px;box-shadow:var(--sh-coral);transition:transform .3s var(--ease),box-shadow .3s var(--ease)}
.ncta:hover{transform:translateY(-1px)}
.mmenu-btn{display:none;width:44px;height:44px;border:0;background:transparent;position:relative;cursor:pointer}
.mmenu-btn span,.mmenu-btn span::before,.mmenu-btn span::after{content:'';position:absolute;left:11px;width:22px;height:2.5px;border-radius:2px;background:var(--ink);transition:transform .3s var(--ease),opacity .3s}
.mmenu-btn span{top:21px}.mmenu-btn span::before{top:-7px;left:0}.mmenu-btn span::after{top:7px;left:0}
body.mmenu-open .mmenu-btn span{background:transparent}
body.mmenu-open .mmenu-btn span::before{transform:translateY(7px) rotate(45deg)}
body.mmenu-open .mmenu-btn span::after{transform:translateY(-7px) rotate(-45deg)}
.mmenu-overlay{position:fixed;inset:64px 0 0 0;z-index:99;background:var(--cream);display:none;flex-direction:column;align-items:center;justify-content:center;gap:22px;padding:24px}
.mmenu-overlay a{font-size:20px;font-weight:700;color:var(--ink);text-decoration:none}
body.mmenu-open .mmenu-overlay{display:flex}
body.mmenu-open{overflow:hidden}
.sticky-cta{position:fixed;left:16px;right:16px;bottom:16px;z-index:98;display:flex;align-items:center;justify-content:space-between;gap:12px;padding:10px 12px 10px 18px;background:var(--card);border-radius:22px;box-shadow:var(--sh2);transform:translateY(120%);transition:transform .35s var(--ease)}
.sticky-cta.show{transform:none}
.sticky-cta-note{font-size:13px;font-weight:700;color:var(--muted)}
.sticky-cta-btn{height:44px;padding:0 18px;display:inline-flex;align-items:center;background:var(--coral);color:#fff;font-weight:800;font-size:14px;border-radius:999px;text-decoration:none;box-shadow:var(--sh-coral)}
@media(min-width:900px){.sticky-cta{display:none}}

/* HERO */
.hero{position:relative;min-height:min(100vh,880px);padding:120px 80px 60px;display:grid;grid-template-columns:1.05fr 1fr;gap:40px;align-items:center;overflow:hidden}
.blob{position:absolute;border-radius:50%;pointer-events:none}
.blob-1{width:520px;height:520px;background:var(--peach);opacity:.8;left:-120px;top:-160px}
.blob-2{width:560px;height:560px;background:var(--mint);opacity:.7;right:-80px;bottom:-220px}
.blob-3{width:300px;height:300px;background:var(--butter);opacity:.7;right:360px;top:-120px}
.hleft{position:relative;z-index:1;display:flex;flex-direction:column;gap:22px}
.hannounce{display:inline-flex;align-self:flex-start;align-items:center;gap:8px;padding:8px 14px;border-radius:999px;background:var(--card);font-size:13px;font-weight:700;color:var(--deep);box-shadow:var(--sh);text-decoration:none}
.htitle{font-size:clamp(34px,4.2vw,56px);font-weight:900;line-height:1.2;letter-spacing:-.01em;color:var(--ink)}
.hdesc{font-size:18px;line-height:1.75;color:var(--muted);font-weight:700;max-width:520px}
.hactions{display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.btn-primary{display:inline-flex;align-items:center;gap:10px;height:56px;padding:0 26px;border-radius:18px;background:var(--coral);color:#fff;font-weight:800;font-size:16px;text-decoration:none;box-shadow:var(--sh-coral);transition:transform .3s var(--ease)}
.btn-primary:hover{transform:translateY(-2px)}
.btn-store{display:inline-flex;align-items:center;gap:10px;height:56px;padding:0 20px;border-radius:18px;background:var(--card);color:var(--ink);font-weight:700;font-size:14px;text-decoration:none;border:1.5px solid var(--line);transition:transform .3s var(--ease)}
.btn-store:hover{transform:translateY(-2px)}
.btn-store .sub{font-size:10px;color:var(--muted);display:block;line-height:1.1}
.btn-store .main{font-size:15px;font-weight:800;display:block;line-height:1.2}
.hmeta{display:flex;align-items:center;gap:18px;font-size:13px;font-weight:700;color:var(--muted);flex-wrap:wrap}
.hright{position:relative;z-index:1;height:720px;display:flex;align-items:center;justify-content:center}
.phone{width:330px;height:680px;border-radius:48px;background:#fff;padding:10px;box-shadow:0 30px 70px rgba(59,44,38,.18);border:1.5px solid var(--line)}
.phone img{width:100%;height:100%;object-fit:cover;object-position:top;border-radius:38px}
.mascot{position:absolute;object-fit:contain;filter:drop-shadow(0 14px 22px rgba(59,44,38,.22));animation:bob 5s ease-in-out infinite}
@keyframes bob{0%,100%{transform:translateY(0) rotate(var(--r,0deg))}50%{transform:translateY(-8px) rotate(var(--r,0deg))}}
.m1{width:130px;height:130px;left:-10px;top:30px;--r:-12deg}
.m2{width:124px;height:124px;right:-24px;top:110px;--r:10deg;animation-delay:.6s}
.m3{width:108px;height:108px;right:-4px;bottom:120px;animation-delay:1.2s}
.m4{width:130px;height:130px;left:-36px;bottom:70px;--r:8deg;animation-delay:1.8s}
.m5{width:112px;height:112px;left:76px;bottom:-24px;--r:-6deg;animation-delay:2.4s}

/* SECTIONS */
.section{padding:104px 80px}
.section-alt{background:var(--card2)}
.slbl{font-size:12px;letter-spacing:.14em;font-weight:800;color:var(--deep);margin-bottom:14px;text-transform:uppercase}
.stitle{font-size:clamp(28px,3.2vw,40px);font-weight:900;line-height:1.3;color:var(--ink);margin-bottom:14px}
.stitle em{font-style:normal;color:var(--coral)}
.sdesc{font-size:16px;line-height:1.8;color:var(--muted);font-weight:700;max-width:640px;margin-bottom:44px}
.icon{width:44px;height:44px;border-radius:14px;background:var(--peach);display:flex;align-items:center;justify-content:center;color:var(--deep);flex-shrink:0}
.icon svg{width:22px;height:22px}
.icon.mint{background:var(--mint);color:var(--mint-ink)}
.icon.butter{background:var(--butter);color:var(--butter-ink)}
.icon.warn{background:var(--warn-tint);color:var(--warn)}

/* HOW */
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.step{background:var(--card);border-radius:24px;padding:28px;box-shadow:var(--sh);display:flex;flex-direction:column;gap:12px;position:relative}
.step img{width:72px;height:72px;object-fit:contain;filter:drop-shadow(0 6px 10px rgba(59,44,38,.16))}
.stepn{position:absolute;top:22px;right:24px;font-family:'Nunito',sans-serif;font-size:13px;font-weight:800;color:var(--deep);background:var(--peach);padding:4px 10px;border-radius:999px}
.stept{font-size:18px;font-weight:900;color:var(--ink)}
.stepd{font-size:14px;line-height:1.8;color:var(--muted);font-weight:700}

/* SCREENS */
.screens-wrap{position:relative}
.screens-scroll{display:flex;gap:22px;overflow-x:auto;scroll-snap-type:x mandatory;padding:10px 4px 20px;scrollbar-width:none}
.screens-scroll::-webkit-scrollbar{display:none}
.screen-item{flex:0 0 240px;scroll-snap-align:start;display:flex;flex-direction:column;gap:12px}
.screen-phone{border-radius:34px;background:#fff;padding:7px;box-shadow:var(--sh2);border:1.5px solid var(--line)}
.screen-phone img{border-radius:28px;width:100%;aspect-ratio:393/852;object-fit:cover;object-position:top}
.screen-cap{font-size:13px;line-height:1.6;color:var(--muted);font-weight:700}
.screen-cap strong{display:block;color:var(--ink);font-weight:900;font-size:14px}
.screens-hint{display:flex;justify-content:flex-end;gap:8px;font-size:12px;color:var(--faint);font-weight:700;margin-top:4px}

/* FEATURES */
.fgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.feat{background:var(--card);border-radius:22px;padding:24px;box-shadow:var(--sh);display:flex;flex-direction:column;gap:12px}
.ft{font-size:16px;font-weight:900;color:var(--ink)}
.fd{font-size:13px;line-height:1.75;color:var(--muted);font-weight:700}

/* WHY */
.why-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}
.why-card{background:var(--card);border-radius:24px;padding:28px;box-shadow:var(--sh);display:flex;flex-direction:column;gap:10px}
.why-num{font-family:'Nunito',sans-serif;font-size:12px;font-weight:800;letter-spacing:.12em;color:var(--deep)}
.why-t{font-size:19px;font-weight:900;color:var(--ink)}
.why-d{font-size:14px;line-height:1.8;color:var(--muted);font-weight:700}
.why-d strong{color:var(--ink);font-weight:900}

/* NEW FEATURES (order) */
.nf-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:20px}
.nf-card{background:var(--card);border-radius:26px;padding:28px;box-shadow:var(--sh);display:flex;flex-direction:column;gap:14px}
.nf-head{display:flex;align-items:center;gap:14px}
.nf-head img{width:64px;height:64px;object-fit:contain;filter:drop-shadow(0 6px 10px rgba(59,44,38,.16))}
.nf-t{font-size:20px;font-weight:900;color:var(--ink)}
.nf-t2{font-size:12px;color:var(--deep);font-weight:800;letter-spacing:.06em}
.nf-d{font-size:14px;line-height:1.8;color:var(--muted);font-weight:700}
.nf-d strong{color:var(--ink);font-weight:900}
.nf-mock{border-radius:20px;padding:16px;margin-top:4px}
.nf-mock-light{background:var(--cream);border:1.5px solid var(--line)}
.nf-mock-dark{background:var(--ink-bg);color:#fff}
.nfm-row{display:flex;justify-content:space-between;align-items:flex-start;gap:12px;padding:10px 0;border-bottom:1px solid var(--line)}
.nfm-row:last-child{border-bottom:0}
.nfm-name{font-size:14px;font-weight:900;color:var(--ink)}
.nfm-sub{font-size:11px;color:var(--muted);font-weight:700;margin-top:2px}
.nfm-price{font-family:'Nunito',sans-serif;font-size:15px;font-weight:800;color:var(--ink);white-space:nowrap}
.nfm-price.bad{color:var(--warn)}
.nfm-flag{display:inline-flex;align-items:center;gap:4px;font-size:11px;font-weight:800;color:var(--warn);margin-top:4px}
.nfm-ok{display:inline-flex;align-items:center;gap:4px;font-size:11px;font-weight:800;color:var(--mint-ink);margin-top:4px}
.nfm-verdict{display:flex;align-items:center;gap:8px;font-size:14px;font-weight:900;color:var(--warn);background:var(--warn-tint);border:1.5px solid #FFC9C9;border-radius:14px;padding:10px 12px;margin-bottom:8px}
.nfm-phrase{font-size:18px;font-weight:900;line-height:1.4;color:#fff}
.nfm-decl{display:flex;flex-direction:column;gap:8px;padding:12px 14px;border-radius:14px;background:rgba(255,107,71,.14);border:1.5px solid rgba(255,107,71,.45);margin:12px 0}
.nfm-decl div{display:flex;align-items:flex-start;gap:8px;font-size:14px;font-weight:700;color:#fff}
.nfm-decl svg{flex-shrink:0;margin-top:2px}
.nfm-drow{display:flex;justify-content:space-between;align-items:center;padding:12px 14px;border-radius:14px;background:rgba(255,255,255,.06);margin-top:8px}
.nfm-drow .n{font-size:17px;font-weight:800;color:#fff}
.nfm-drow .s{font-size:11px;color:rgba(255,255,255,.5);margin-top:2px}
.nfm-drow .q{font-family:'Nunito',sans-serif;font-weight:800;color:#fff;background:rgba(255,255,255,.1);padding:6px 12px;border-radius:999px}

/* PRICING */
.pgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;max-width:1060px;margin:0 auto}
.pcard{background:var(--card);border-radius:26px;padding:28px;box-shadow:var(--sh);display:flex;flex-direction:column;gap:10px;position:relative;border:1.5px solid var(--line)}
.pcard-featured{border-color:var(--coral);box-shadow:var(--sh-coral)}
.pbadge-feat{position:absolute;top:-13px;left:24px;background:var(--honey);color:var(--ink);font-size:11px;font-weight:800;padding:4px 12px;border-radius:999px;letter-spacing:.06em}
.pname{font-size:18px;font-weight:900;color:var(--ink)}
.pdesc{font-size:13px;color:var(--muted);font-weight:700}
.pcredits{font-family:'Nunito',sans-serif;font-size:40px;font-weight:800;color:var(--ink);line-height:1}
.pcredits-unit{font-size:14px;color:var(--muted);font-weight:700;margin-left:4px}
.pprice{font-family:'Nunito',sans-serif;font-size:22px;color:var(--deep);font-weight:800}
.pprice-jpy{font-size:12px;color:var(--muted);font-weight:700;margin-top:-6px}
.pdivider{height:1px;background:var(--line);margin:8px 0}
.pfeature{font-size:13px;color:var(--muted);display:flex;align-items:center;gap:8px;font-weight:700}
.pcheck{color:var(--mint-ink);font-weight:900}
.pbtn{display:flex;align-items:center;justify-content:center;height:48px;border-radius:16px;background:var(--coral);color:#fff;font-weight:800;font-size:14px;text-decoration:none;box-shadow:var(--sh-coral);margin-top:6px}
.pbtn-outline{background:var(--card);color:var(--ink);border:1.5px solid var(--line);box-shadow:none}
.pfree-note{text-align:center;margin-top:28px;font-size:14px;color:var(--muted);font-weight:700}
.pfree-note strong{color:var(--deep);font-weight:900}

/* LANGUAGES */
.lgrid{display:grid;grid-template-columns:repeat(7,1fr);gap:10px}
.lcard{background:var(--card);border-radius:18px;padding:16px 10px;display:flex;flex-direction:column;align-items:center;gap:4px;box-shadow:var(--sh)}
.lflag{font-size:26px}
.lname{font-size:13px;font-weight:900;color:var(--ink)}
.lnat{font-size:11px;color:var(--muted);font-weight:700}

/* FAQ */
.faq-wrap{max-width:820px;margin:0 auto;display:flex;flex-direction:column;gap:10px}
.faq-item{background:var(--card);border-radius:18px;padding:0 22px;box-shadow:var(--sh)}
.faq-q{list-style:none;cursor:pointer;padding:18px 0;font-size:15px;font-weight:900;color:var(--ink);display:flex;justify-content:space-between;align-items:center;gap:12px}
.faq-q::-webkit-details-marker{display:none}
.faq-q::after{content:'+';font-family:'Nunito',sans-serif;font-size:20px;color:var(--coral);transition:transform .3s var(--ease)}
.faq-item[open] .faq-q::after{transform:rotate(45deg)}
.faq-a{padding:0 0 18px;font-size:14px;line-height:1.85;color:var(--muted);font-weight:700}

/* TESTIMONIALS */
.tnote{font-size:12px;color:var(--faint);font-weight:700;margin:-30px 0 24px}
.tgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.tcard{background:var(--card);border-radius:22px;padding:24px;box-shadow:var(--sh);display:flex;flex-direction:column;gap:12px}
.tstars{color:var(--honey);font-size:13px;letter-spacing:3px}
.ttext{font-size:14px;line-height:1.8;color:var(--ink);font-weight:700}
.tauthor{display:flex;align-items:center;gap:10px;margin-top:auto}
.tavatar-new{width:36px;height:36px;border-radius:50%;background:var(--peach);color:var(--deep);display:flex;align-items:center;justify-content:center;font-weight:900;font-family:'Nunito',sans-serif}
.tname{font-size:13px;font-weight:900;color:var(--ink)}
.tcountry{font-size:12px;color:var(--muted);font-weight:700}

/* CTA */
.cta{position:relative;overflow:hidden;padding:110px 80px;text-align:center;background:var(--coral);color:#fff}
.cta .blob{background:rgba(255,255,255,.12)}
.cta-mascots{display:flex;justify-content:center;gap:-10px;margin-bottom:22px}
.cta-mascots img{width:84px;height:84px;object-fit:contain;filter:drop-shadow(0 10px 18px rgba(0,0,0,.18));margin:0 -4px}
.cta-title{font-size:clamp(30px,3.6vw,44px);font-weight:900;line-height:1.3;margin-bottom:14px;position:relative}
.cta-desc{font-size:16px;line-height:1.8;font-weight:700;opacity:.9;margin-bottom:32px;position:relative}
.cta-actions{display:flex;justify-content:center;gap:14px;flex-wrap:wrap;position:relative}
.cta .btn-store{background:#fff;border-color:#fff}

/* XPROMO + FOOTER */
.xpromo{padding:0 80px 80px}
.xpromo-card{display:flex;align-items:center;gap:20px;background:var(--card);border-radius:24px;padding:22px 26px;box-shadow:var(--sh);max-width:900px;margin:0 auto}
.xpromo-emoji{font-size:30px}
.xpromo-h{display:block;font-size:16px;font-weight:900;color:var(--ink)}
.xpromo-sub{display:block;font-size:13px;color:var(--muted);font-weight:700;margin-top:2px}
.xpromo-btn{margin-left:auto;height:42px;padding:0 18px;display:inline-flex;align-items:center;border-radius:999px;background:var(--ink-bg);color:#fff;font-weight:800;font-size:13px;text-decoration:none;white-space:nowrap}
footer{padding:40px 80px 60px;display:flex;align-items:center;justify-content:space-between;gap:20px;flex-wrap:wrap;border-top:1px solid var(--line)}
.flogo{display:flex;align-items:center;gap:10px;text-decoration:none}
.flogo-text{font-family:'Nunito',sans-serif;font-size:18px;font-weight:800;color:var(--ink)}
.flinks{display:flex;gap:22px;flex-wrap:wrap}
.flink{font-size:13px;color:var(--muted);text-decoration:none;font-weight:700}
.fcopy{font-size:12px;color:var(--faint);font-weight:700;width:100%}

/* RESPONSIVE */
@media(max-width:1100px){.fgrid{grid-template-columns:repeat(2,1fr)}.lgrid{grid-template-columns:repeat(4,1fr)}}
@media(max-width:900px){
  nav{padding:0 20px}.nlinks,.ncta{display:none}.mmenu-btn{display:block}
  .hero{grid-template-columns:minmax(0,1fr);padding:96px 24px 40px;gap:20px;min-height:0}
  .hleft{min-width:0}.hactions{gap:10px}.btn-primary{height:52px;padding:0 20px;font-size:15px}.btn-store{height:52px;padding:0 14px}
  .hright{height:600px}.phone{width:270px;height:556px}
  .m1{width:78px;height:78px;left:-6px;top:10px}.m2{width:72px;height:72px;right:-6px;top:60px}.m3{display:none}.m4{width:80px;height:80px;left:-10px;bottom:30px}.m5{width:70px;height:70px;right:0;bottom:0;left:auto}
  .htitle{font-size:32px}.hdesc{font-size:15px}
  .section{padding:72px 24px}.steps,.why-grid,.nf-grid,.pgrid,.tgrid{grid-template-columns:1fr}.fgrid{grid-template-columns:1fr}.lgrid{grid-template-columns:repeat(3,1fr)}
  .cta{padding:80px 24px}.xpromo{padding:0 24px 60px}.xpromo-card{flex-direction:column;align-items:flex-start}.xpromo-btn{margin-left:0}
  footer{padding:32px 24px 100px}
}
"""

SVG = {
 "camera": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 8h3l2-3h6l2 3h3v11H4z"/><circle cx="12" cy="13" r="3.5"/></svg>',
 "sparkle": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M12 3l2.2 5.8L20 11l-5.8 2.2L12 19l-2.2-5.8L4 11l5.8-2.2z"/></svg>',
 "warn": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4l9 16H3z"/><path d="M12 10v4"/><path d="M12 17.5v.5"/></svg>',
 "hand": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 13V5a1.5 1.5 0 0 1 3 0v6"/><path d="M11 10V4a1.5 1.5 0 0 1 3 0v7"/><path d="M14 11V6a1.5 1.5 0 0 1 3 0v8a6 6 0 0 1-6 6h-1a6 6 0 0 1-5-2.7L3.5 14A1.6 1.6 0 0 1 6 12l2 2"/></svg>',
 "receipt": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 3h12v18l-3-2-3 2-3-2-3 2z"/><path d="M9 8h6M9 12h6"/></svg>',
 "globe": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/></svg>',
 "coin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M9 9.5c0-1 1.3-1.5 3-1.5s3 .5 3 1.5-1.3 1.5-3 1.5-3 .5-3 1.5 1.3 1.5 3 1.5 3-.5 3-1.5M12 6v2M12 16v2"/></svg>',
 "star": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/></svg>',
 "fork": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M8 3v7a2 2 0 0 0 2 2v9M8 3v5M10 3v5"/><path d="M17 3c-2 1-3 4-3 7h3v11"/></svg>',
 "share": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12M7 8l5-5 5 5"/><path d="M5 14v6h14v-6"/></svg>',
 "search": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="6"/><path d="M20 20l-4.5-4.5"/></svg>',
 "check": '<svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12l5 5 9-10"/></svg>',
 "warn12": '<svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4l9 16H3z"/><path d="M12 10v4"/><path d="M12 17.5v.5"/></svg>',
 "warn14": '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="#F0B33E" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4l9 16H3z"/><path d="M12 10v4"/><path d="M12 17.5v.5"/></svg>',
}
APPLE_SVG = '<svg width="22" height="22" viewBox="0 0 24 24" fill="#3B2C26"><path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.8-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z"/></svg>'
PLAY_SVG = '<svg width="22" height="22" viewBox="0 0 24 24"><path fill="#4285F4" d="M3 20.5V3.5c0-.59.34-1.11.84-1.35L13.69 12 3.84 21.85c-.5-.25-.84-.76-.84-1.35"/><path fill="#34A853" d="M16.81 15.12L6.05 21.34l8.49-8.49 2.27 2.27"/><path fill="#EA4335" d="M20.16 10.81c.35.2.59.58.59 1.19s-.24.98-.59 1.19l-2.29 1.32L15.39 12l2.48-2.48 2.29 1.29"/><path fill="#FBBC04" d="M6.05 2.66l10.76 6.22-2.27 2.27-8.49-8.49z"/></svg>'
APP_STORE = "https://apps.apple.com/app/id6760161339"
PLAY_STORE = "https://play.google.com/store/apps/details?id=com.menufy.app"

def store_buttons(where, T, cls="btn-store"):
    return f'''<a href="{APP_STORE}" class="{cls}" target="_blank" onclick="fbq('track','InitiateCheckout',{{content_name:'{where.lower()}',content_category:'AppStore'}})">{APPLE_SVG}<div><span class="sub">{T['dl_sub_ios']}</span><span class="main">App Store</span></div></a>
      <a href="{PLAY_STORE}" class="{cls}" target="_blank" onclick="fbq('track','InitiateCheckout',{{content_name:'{where.lower()}',content_category:'GooglePlay'}})">{PLAY_SVG}<div><span class="sub">{T['dl_sub_play']}</span><span class="main">Google Play</span></div></a>'''

def build(lang):
    T = COPY[lang]
    src_path = os.path.join(ROOT, 'index.html' if lang == 'ja' else 'en/index.html')
    src = open(src_path, encoding='utf-8').read()
    head = src[:src.index('</head>')]
    # swap fonts, favicon, theme-color, style
    head = re.sub(r'<link rel="preconnect" href="https://fonts.googleapis.com">\s*<link href="https://fonts.googleapis.com[^>]*>', FONTS, head)
    # favicon/apple-touch-icon/manifest are real files at the site root (2026-09-13); left untouched
    head = head.replace('<meta name="theme-color" content="#f05a28">', '<meta name="theme-color" content="#FF6B47">')
    head = re.sub(r'<style>.*?</style>', '<style>'+CSS+'</style>', head, flags=re.S)
    # FAQ JSON-LD: add the two new questions
    def add_faq(m):
        block = m.group(0)
        data = json.loads(block[block.index('>')+1:block.rindex('<')])
        if data.get('@type') == 'FAQPage':
            existing = {e['name'] for e in data['mainEntity']}
            for q, a in T['faq_new']:
                if q not in existing:
                    data['mainEntity'].append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})
            return '<script type="application/ld+json">\n' + json.dumps(data, ensure_ascii=False, indent=2) + '\n</script>'
        return block
    head = re.sub(r'<script type="application/ld\+json">.*?</script>', add_faq, head, flags=re.S)
    head = head.replace('<meta name="description" content="' + re.search(r'<meta name="description" content="([^"]*)"', head).group(1) + '">', f'<meta name="description" content="{T["meta_desc"]}">')
    for key in ('og:description',):
        head = re.sub(r'(<meta property="og:description" content=")[^"]*(")', lambda m: m.group(1)+T['meta_desc']+m.group(2), head)
    head = re.sub(r'(<meta name="twitter:description" content=")[^"]*(")', lambda m: m.group(1)+T['meta_desc_short']+m.group(2), head)

    # scripts kept verbatim from the old body
    body_old = src[src.index('<body>'):]
    mm_script = re.search(r'<script>\s*\(function\(\)\{\s*var btn = document\.querySelector\(\'\.mmenu-btn\'\);.*?</script>', body_old, re.S).group(0)
    smart_script = re.search(r'<!-- Smart download routing.*?</script>', body_old, re.S).group(0)
    track_script = body_old[body_old.rindex('<script>'):body_old.rindex('</script>')+9]

    m = lambda k, cls="": f'<img src="{T["asset_prefix"]}assets/mascot-{k}.png" alt="" class="{cls}" loading="lazy">'
    sp = T['asset_prefix']
    nav = f'''<nav>
  <a href="#" class="nlogo"><img src="{sp}assets/mascot-sushi.png" alt="" class="nicon"><span class="ntext">Menufy</span></a>
  <div class="nlinks">
    <a href="#how" class="nlink">{T['nav_how']}</a>
    <a href="#features" class="nlink">{T['nav_features']}</a>
    <a href="#order" class="nlink">{T['nav_new']}</a>
    <a href="#pricing" class="nlink">{T['nav_pricing']}</a>
    <a href="#languages" class="nlink">{T['nav_langs']}</a>
    <a href="#faq" class="nlink">{T['nav_faq']}</a>
    <a href="{T['tripfy_href']}" class="nlink">Tripfy</a>
    <a href="{T['alt_href']}" class="nlink" aria-label="{T['alt_label']}">{T['alt_label']}</a>
  </div>
  <a href="#cta" class="ncta">{T['nav_cta']}</a>
  <button class="mmenu-btn" aria-label="{T['menu_open']}" aria-expanded="false" aria-controls="mmenu"><span></span></button>
</nav>

<div class="mmenu-overlay" id="mmenu" role="dialog" aria-modal="true">
  <a href="#how" data-mmenu-link>{T['nav_how']}</a>
  <a href="#features" data-mmenu-link>{T['nav_features']}</a>
  <a href="#order" data-mmenu-link>{T['nav_new']}</a>
  <a href="#pricing" data-mmenu-link>{T['nav_pricing']}</a>
  <a href="#languages" data-mmenu-link>{T['nav_langs']}</a>
  <a href="#faq" data-mmenu-link>{T['nav_faq']}</a>
  <a href="{T['tripfy_href']}" data-mmenu-link>Tripfy</a>
  <a href="{T['alt_href']}" data-mmenu-link>{T['alt_label']}</a>
  <a href="#cta" data-mmenu-link class="btn-primary">{T['nav_cta']}</a>
</div>

<div class="sticky-cta" id="sticky-cta" hidden>
  <span class="sticky-cta-note">{T['sticky_note']}</span>
  <a href="#" class="sticky-cta-btn" id="sticky-cta-btn">{T['nav_cta']}</a>
</div>
'''
    hero = f'''<section class="hero">
  <div class="blob blob-1"></div><div class="blob blob-2"></div><div class="blob blob-3"></div>
  <div class="hleft">
    <a href="#order" class="hannounce"><span style="display:inline-flex;width:14px;height:14px">{SVG['sparkle']}</span>{T['hero_announce']}</a>
    <h1 class="htitle">{T['hero_title']}</h1>
    <p class="hdesc">{T['hero_desc']}</p>
    <div class="hactions">
      <a href="#cta" class="btn-primary"><span style="display:inline-flex;width:20px;height:20px">{SVG['camera']}</span>{T['hero_cta']}</a>
      {store_buttons('Hero', T)}
    </div>
    <div class="hmeta"><span>{T['meta_langs']}</span><span>·</span><span>{T['meta_onetime']}</span><span>·</span><span>{T['meta_free']}</span></div>
  </div>
  <div class="hright">
    <div class="phone"><img src="{sp}screens-v2/{T['screens_dir']}03-result.jpg" alt="{T['alt_result']}" fetchpriority="high"></div>
    {m('sushi','mascot m1')}{m('ramen','mascot m2')}{m('gyoza','mascot m3')}{m('omurice','mascot m4')}{m('pudding','mascot m5')}
  </div>
</section>
'''
    steps = ''.join(f'''    <div class="step">
      <span class="stepn">0{i+1}</span>
      {m(k)}
      <h3 class="stept">{t}</h3>
      <p class="stepd">{d}</p>
    </div>
''' for i,(k,t,d) in enumerate(T['steps']))
    how = f'''<section class="section section-alt" id="how">
  <div class="slbl">{T['how_lbl']}</div>
  <h2 class="stitle">{T['how_title']}</h2>
  <p class="sdesc">{T['how_desc']}</p>
  <div class="steps">
{steps}  </div>
</section>
'''
    screens = ''.join(f'''      <div class="screen-item">
        <div class="screen-phone"><img src="{sp}screens-v2/{T['screens_dir']}{f}" alt="{alt}" loading="lazy"></div>
        <div class="screen-cap"><strong>{t}</strong>{d}</div>
      </div>
''' for f,alt,t,d in T['screens'])
    screens_sec = f'''<section class="section" id="screens">
  <div class="slbl">{T['screens_lbl']}</div>
  <h2 class="stitle">{T['screens_title']}</h2>
  <p class="sdesc">{T['screens_desc']}</p>
  <div class="screens-wrap">
    <div class="screens-scroll">
{screens}    </div>
    <div class="screens-hint"><span>{T['screens_hint']}</span><span>→</span></div>
  </div>
</section>
'''
    feats = ''.join(f'''    <div class="feat">
      <div class="icon {cls}">{SVG[ic]}</div>
      <h3 class="ft">{t}</h3>
      <p class="fd">{d}</p>
    </div>
''' for ic,cls,t,d in T['features'])
    features = f'''<section class="section section-alt" id="features">
  <div class="slbl">{T['feat_lbl']}</div>
  <h2 class="stitle">{T['feat_title']}</h2>
  <p class="sdesc">{T['feat_desc']}</p>
  <div class="fgrid">
{feats}  </div>
</section>
'''
    whys = ''.join(f'''    <div class="why-card">
      <span class="why-num">REASON 0{i+1}</span>
      <h3 class="why-t">{t}</h3>
      <p class="why-d">{d}</p>
    </div>
''' for i,(t,d) in enumerate(T['whys']))
    why = f'''<section class="section" id="why">
  <div class="slbl">{T['why_lbl']}</div>
  <h2 class="stitle">{T['why_title']}</h2>
  <p class="sdesc">{T['why_desc']}</p>
  <div class="why-grid">
{whys}  </div>
</section>
'''
    order = f'''<section class="section section-alt" id="order">
  <div class="slbl">{T['new_lbl']}</div>
  <h2 class="stitle">{T['new_title']}</h2>
  <p class="sdesc">{T['new_desc']}</p>
  <div class="nf-grid">
    <div class="nf-card">
      <div class="nf-head">{m('pudding')}<div><h3 class="nf-t">{T['nf1_t']}</h3><p class="nf-t2">{T['nf1_t2']}</p></div></div>
      <p class="nf-d">{T['nf1_d']}</p>
      <div class="nf-mock nf-mock-light" aria-hidden="true">
        <div class="nfm-verdict">{SVG['warn12']}<span>{T['nf1_verdict']}</span></div>
        <div class="nfm-row"><div><div class="nfm-name">{T['nf1_r1']}</div><div class="nfm-sub">ผัดไทยกุ้งสด ×1</div><div class="nfm-ok">{SVG['check']}{T['nf1_ok']}</div></div><div class="nfm-price">120.00</div></div>
        <div class="nfm-row"><div><div class="nfm-name">{T['nf1_r2']}</div><div class="nfm-sub">ต้มยำกุ้ง ×1</div><div class="nfm-flag">{SVG['warn12']}{T['nf1_flag1']}</div></div><div class="nfm-price bad">180.00</div></div>
        <div class="nfm-row"><div><div class="nfm-name">{T['nf1_r3']}</div><div class="nfm-sub">ชาไทยเย็น ×2</div><div class="nfm-flag">{SVG['warn12']}{T['nf1_flag2']}</div></div><div class="nfm-price bad">100.00</div></div>
        <div class="nfm-row"><div><div class="nfm-name">{T['nf1_r4']}</div></div><div class="nfm-price">53.00</div></div>
      </div>
    </div>
    <div class="nf-card">
      <div class="nf-head">{m('ramen')}<div><h3 class="nf-t">{T['nf2_t']}</h3><p class="nf-t2">{T['nf2_t2']}</p></div></div>
      <p class="nf-d">{T['nf2_d']}</p>
      <div class="nf-mock nf-mock-dark" aria-hidden="true">
        <div class="nfm-phrase">ขอสั่งเมนูเหล่านี้ครับ/ค่ะ</div>
        <div class="nfm-decl"><div>{SVG['warn14']}<span>ฉันแพ้อาหารทะเลจำพวกกุ้งและปู</span></div><div>{SVG['warn14']}<span>ฉันไม่กินหมู</span></div></div>
        <div class="nfm-drow"><div><div class="n">ผัดไทยกุ้งสด</div><div class="s">{T['nf2_r1']}</div></div><div class="q">×1</div></div>
        <div class="nfm-drow"><div><div class="n">ข้าวผัดปู</div><div class="s">{T['nf2_r2']}</div></div><div class="q">×1</div></div>
      </div>
    </div>
  </div>
</section>
'''
    def pcard(name, desc, credits, jpy, usd, feats, featured, key, value):
        cls = 'pcard pcard-featured' if featured else 'pcard'
        badge = f'<div class="pbadge-feat">{T["p_popular"]}</div>' if featured else ''
        btn = 'pbtn' if featured else 'pbtn pbtn-outline'
        fl = ''.join(f'<div class="pfeature"><span class="pcheck">✓</span>{f}</div>' for f in feats)
        return f'''    <div class="{cls}">
      {badge}
      <div class="pname">{name}</div>
      <div class="pdesc">{desc}</div>
      <div><span class="pcredits">{credits}</span><span class="pcredits-unit">{T['p_unit']}</span></div>
      <div class="pprice">{jpy}</div>
      <div class="pprice-jpy">{usd}</div>
      <div class="pdivider"></div>
      {fl}
      <a href="{APP_STORE}" class="{btn}" target="_blank" onclick="fbq('track','InitiateCheckout',{{content_name:'pricing_{key.replace('Pack','').lower()}',content_category:'AppStore'}})">{T['p_btn_ios']}</a>
      <a href="{PLAY_STORE}" class="{btn}" target="_blank" onclick="fbq('track','InitiateCheckout',{{content_name:'pricing_{key.replace('Pack','').lower()}',content_category:'GooglePlay'}})">{T['p_btn_play']}</a>
    </div>
'''
    P = T['plans']
    pricing = f'''<section class="section" id="pricing">
  <div class="slbl">{T['price_lbl']}</div>
  <h2 class="stitle">{T['price_title']}</h2>
  <p class="sdesc">{T['price_desc']}</p>
  <div class="pgrid">
{pcard(P[0][0],P[0][1],25,'¥500','$2.99',T['p_feats'](25),False,'StarterPack','2.99')}{pcard(P[1][0],P[1][1],150,'¥1,100','$6.99',T['p_feats'](150),True,'TravelerPack','6.99')}{pcard(P[2][0],P[2][1],400,'¥2,500','$14.99',T['p_feats'](400),False,'ExplorerPack','14.99')}  </div>
  <p class="pfree-note">{T['p_free_note']}</p>
</section>
'''
    LANGS = [("🇯🇵","日本語","Japanese"),("🇺🇸","English","English"),("🇨🇳","中文（简体）","Chinese (Simplified)"),("🇹🇼","中文（繁體）","Chinese (Traditional)"),("🇰🇷","한국어","Korean"),("🇫🇷","Français","French"),("🇪🇸","Español","Spanish"),("🇮🇹","Italiano","Italian"),("🇩🇪","Deutsch","German"),("🇲🇾","Bahasa Melayu","Malay"),("🇮🇩","Bahasa Indonesia","Indonesian"),("🇹🇭","ภาษาไทย","Thai"),("🇻🇳","Tiếng Việt","Vietnamese"),("🇦🇪","العربية","Arabic")]
    lcards = ''.join(f'<div class="lcard"><span class="lflag">{f}</span><span class="lname">{T["lang_names"][i]}</span><span class="lnat">{n}</span></div>\n' for i,(f,n,_) in enumerate(LANGS))
    languages = f'''<section class="section section-alt" id="languages">
  <div class="slbl">{T['lang_lbl']}</div>
  <h2 class="stitle">{T['lang_title']}</h2>
  <p class="sdesc">{T['lang_desc']}</p>
  <div class="lgrid">
{lcards}  </div>
</section>
'''
    faq_items = ''.join(f'''    <details class="faq-item">
      <summary class="faq-q">{q}</summary>
      <div class="faq-a">{a}</div>
    </details>
''' for q,a in T['faq'])
    faq = f'''<section class="section" id="faq">
  <div class="slbl">{T['faq_lbl']}</div>
  <h2 class="stitle">{T['faq_title']}</h2>
  <div class="faq-wrap">
{faq_items}  </div>
</section>
'''
    tcards = ''.join(f'''    <div class="tcard">
      <div class="tstars">★★★★★</div>
      <p class="ttext">{txt}</p>
      <div class="tauthor"><div class="tavatar-new">{name[0]}</div><div><div class="tname">{name}</div><div class="tcountry">{where}</div></div></div>
    </div>
''' for txt,name,where in T['testimonials'])
    testimonials = f'''<section class="section section-alt">
  <div class="slbl">{T['t_lbl']}</div>
  <h2 class="stitle">{T['t_title']}</h2>
  <p class="tnote">{T['t_note']}</p>
  <div class="tgrid">
{tcards}  </div>
</section>
'''
    cta = f'''<section class="cta" id="cta">
  <div class="blob" style="width:600px;height:600px;left:-200px;top:-300px"></div>
  <div class="blob" style="width:420px;height:420px;right:-120px;bottom:-200px"></div>
  <div class="cta-mascots">{m('sushi')}{m('ramen')}{m('gyoza')}{m('omurice')}{m('pudding')}</div>
  <h2 class="cta-title">{T['cta_title']}</h2>
  <p class="cta-desc">{T['cta_desc']}</p>
  <div class="cta-actions">
      {store_buttons('CTA', T)}
  </div>
</section>

<section class="xpromo">
  <div class="xpromo-card">
    <span class="xpromo-emoji">✈️</span>
    <div class="xpromo-txt"><span class="xpromo-h">{T['xp_h']}</span><span class="xpromo-sub">{T['xp_sub']}</span></div>
    <a href="{T['tripfy_href']}" class="xpromo-btn">{T['xp_btn']}</a>
  </div>
</section>

<footer>
  <a href="#" class="flogo"><img src="{sp}assets/mascot-sushi.png" alt="" class="nicon" style="width:28px;height:28px"><span class="flogo-text">Menufy</span></a>
  <div class="flinks">
    <a href="{T['privacy_href']}" class="flink">{T['f_privacy']}</a>
    <a href="{T['terms_href']}" class="flink">{T['f_terms']}</a>
    <a href="{T['alt_href']}" class="flink">{T['alt_label']}</a>
  </div>
  <div class="fcopy">© 2026 Menufy</div>
</footer>
'''
    body = '<body>\n\n' + nav + '\n' + mm_script + '\n\n' + smart_script + '\n\n' + hero + '\n' + how + '\n' + screens_sec + '\n' + features + '\n' + why + '\n' + order + '\n' + pricing + '\n' + languages + '\n' + faq + '\n' + testimonials + '\n' + cta + '\n' + track_script + '\n\n</body>\n</html>\n'
    out = head + '</head>\n' + body
    open(src_path, 'w', encoding='utf-8').write(out)
    print(f"wrote {src_path} ({len(out)//1024} KB)")

COPY = {}
exec(open(os.path.join(ROOT, 'tools', 'lp_copy.py'), encoding='utf-8').read())

if __name__ == '__main__':
    for lang in (sys.argv[1:] or ['ja', 'en']):
        build(lang)
