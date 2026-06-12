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

  for (const el of await page.$$('.shot')) {
    const name = await el.getAttribute('data-out');
    const lang = name.slice(0, 2);
    const dir = path.join(__dirname, 'out', lang);
    fs.mkdirSync(dir, { recursive: true });
    const out = path.join(dir, name + '.png');
    await el.scrollIntoViewIfNeeded();
    await el.screenshot({ path: out });
    console.log('rendered', name);

    // パノラマ (2640x2868) は ASC 用に左右 1320x2868 へ分割
    const isPano = (await el.getAttribute('class')).includes('pano');
    if (isPano && sharp) {
      const meta = await sharp(out).metadata();
      const half = Math.floor(meta.width / 2);
      await sharp(out).extract({ left: 0, top: 0, width: half, height: meta.height })
        .toFile(path.join(dir, name + '-L.png'));
      await sharp(out).extract({ left: half, top: 0, width: half, height: meta.height })
        .toFile(path.join(dir, name + '-R.png'));
      console.log('split', name, '→ -L / -R');
    }
  }
  await browser.close();
})();
