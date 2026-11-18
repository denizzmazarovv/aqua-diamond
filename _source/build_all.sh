set -e
python3 build_seo.py >/dev/null
node prerender.js 2>&1 | grep -E "^(ru|uz|en) faq" | sed 's/| cyrillic.*//'
node icons.js >/dev/null 2>&1
node og.js >/dev/null 2>&1
python3 -c "from PIL import Image; im=Image.open('site/og-image.png'); im.convert('RGB').save('site/og-image.png', optimize=True)"
python3 csp.py
