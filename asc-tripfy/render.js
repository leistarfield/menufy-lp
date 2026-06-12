const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const sharp = (() => { try { return require('sharp'); } catch { return null; } })();

(async () => {
  const browser = await chromium.launch({ channel: 'chrome' });
  const page = await browser.newPage({
    viewport: { width: 1400, height: 1500 },
    deviceScaleFactor: 2,
  });
  await page.goto('file://' + path.join(__dirname, 'template.html'));
  await page.waitForLoadState('networkidle');
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(300);

  // ASC 受付サイズ（6.5 インチ）。テンプレートは 6.9 比率 (1320x2868) のまま
  // レンダリングし、最終出力のみ fill リサイズする（比率差 0.4% は目視不可）。
  const ASC_W = 1284, ASC_H = 2778;

  for (const el of await page.$$('.shot')) {
    const name = await el.getAttribute('data-out');
    const lang = name.slice(0, 2);
    const dir = path.join(__dirname, 'out', lang);
    fs.mkdirSync(dir, { recursive: true });
    const out = path.join(dir, name + '.png');
    await el.scrollIntoViewIfNeeded();
    const buf = await el.screenshot();
    const isPano = (await el.getAttribute('class')).includes('pano');

    if (!sharp) throw new Error('sharp is required for ASC resizing');
    if (isPano) {
      // パノラマは 2 枚分の幅にリサイズしてから左右 ASC_W ずつに分割
      const resized = await sharp(buf).resize(ASC_W * 2, ASC_H, { fit: 'fill' }).png().toBuffer();
      await sharp(resized).toFile(out);
      await sharp(resized).extract({ left: 0, top: 0, width: ASC_W, height: ASC_H })
        .toFile(path.join(dir, name + '-L.png'));
      await sharp(resized).extract({ left: ASC_W, top: 0, width: ASC_W, height: ASC_H })
        .toFile(path.join(dir, name + '-R.png'));
      console.log('rendered + split', name, '→ -L / -R');
    } else {
      await sharp(buf).resize(ASC_W, ASC_H, { fit: 'fill' }).toFile(out);
      console.log('rendered', name);
    }
  }
  await browser.close();
})();
