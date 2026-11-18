/* Pre-renders /uz/ and /en/ into their own language in static HTML (for Yandex and any crawler
   that does not run JavaScript) and injects FAQPage JSON-LD built from the visible FAQ text. */
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const SITE = 'https://aquadiamond.uz';
const ALT = {
  uz: [['питьевая вода', 'ichimlik suvi'], ['вода', 'suv'], ['гранат', 'anor'], ['финик', 'xurmo'], ['энергетик', 'energetik'], ['банка', 'banka'], [/(\d) л$/g, '$1 l']],
  en: [['питьевая вода', 'drinking water'], ['вода', 'water'], ['гранат', 'pomegranate'], ['финик', 'date'], ['энергетик', 'energy drink'], ['банка', 'can'], [/(\d) л$/g, '$1 L'], [/(\d),(\d)/g, '$1.$2']]
};
(async () => {
  const b = await chromium.launch();
  for (const [lang, rel] of [['ru', 'index.html'], ['uz', 'uz/index.html'], ['en', 'en/index.html']]) {
    const file = path.join(process.cwd(), 'site', rel);
    const src = fs.readFileSync(file, 'utf8');
    const p = await b.newPage();
    await p.goto('file://' + file); await p.waitForTimeout(300);
    const out = await p.evaluate(({ src, lang, alt, site }) => {
      const doc = new DOMParser().parseFromString(src, 'text/html');
      if (lang !== 'ru') {
        doc.querySelectorAll('[data-i18n]').forEach(el => { const v = T[lang][el.dataset.i18n]; if (v != null) el.innerHTML = v; });
        doc.querySelectorAll('img[alt]').forEach(img => {
          let a = img.getAttribute('alt');
          for (const [f, t] of alt) a = typeof f === 'string' ? a.split(f).join(t) : a.replace(new RegExp(f.source, f.flags), t);
          img.setAttribute('alt', a);
        });
      }
      const faq = [];
      for (let i = 1; i <= 12; i++) {
        const q = doc.querySelector(`[data-i18n="q${i}"]`), a = doc.querySelector(`[data-i18n="a${i}"]`);
        if (q && a) faq.push({ '@type': 'Question', name: q.textContent.trim(), acceptedAnswer: { '@type': 'Answer', text: a.textContent.trim() } });
      }
      const url = site + (lang === 'ru' ? '/' : '/' + lang + '/');
      const ld = JSON.stringify({ '@context': 'https://schema.org', '@type': 'FAQPage', '@id': url + '#faq', mainEntity: faq });
      const cyr = [...doc.querySelectorAll('img[alt]')].map(i => i.alt).filter(a => /[а-яё]/i.test(a));
      return { html: '<!DOCTYPE html>\n' + doc.documentElement.outerHTML.replace('<!--FAQ_JSONLD-->', `<script type="application/ld+json">${ld}</script>`), n: faq.length, cyr, h1: doc.querySelector('h1').textContent };
    }, { src, lang, alt: ALT[lang] ? ALT[lang].map(([f, t]) => [typeof f === 'string' ? f : { source: f.source, flags: f.flags }, t]) : [], site: SITE });
    fs.writeFileSync(file, out.html);
    console.log(lang, 'faq', out.n, '| h1:', out.h1, '| cyrillic alts left:', out.cyr.length ? out.cyr : 0);
    await p.close();
  }
  await b.close();
})();
