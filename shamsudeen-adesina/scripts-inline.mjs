import { readFileSync, writeFileSync, readdirSync } from 'node:fs';
const dist = 'dist';
let html = readFileSync(`${dist}/index.html`, 'utf8');
const assets = readdirSync(`${dist}/assets`);
for (const f of assets) {
  const content = readFileSync(`${dist}/assets/${f}`, 'utf8');
  if (f.endsWith('.css')) {
    html = html.replace(new RegExp(`<link[^>]*href="/assets/${f}"[^>]*>`), `<style>${content}</style>`);
  } else if (f.endsWith('.js')) {
    html = html.replace(
      new RegExp(`<script[^>]*src="/assets/${f}"[^>]*></script>`),
      `<script type="module">${content.replace(/<\/script>/g, '<\\/script>')}</script>`,
    );
  }
}
writeFileSync('../SHAMSUDEEN ADESINA.html', html);
console.log('wrote ../SHAMSUDEEN ADESINA.html', (html.length / 1024).toFixed(0) + ' KB');
