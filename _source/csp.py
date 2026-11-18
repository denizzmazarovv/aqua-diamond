"""Последний шаг сборки: защитные заголовки для каждой HTML-страницы в site/.

GitHub Pages не даёт настраивать HTTP-заголовки, поэтому Content-Security-Policy
ставится через <meta http-equiv>. Встроенные <script> разрешаются по их SHA-256:
если кто-то внедрит на страницу чужой скрипт, браузер его не выполнит.
Хэши считаются заново при каждой сборке, поэтому скрипт запускается ПОСЛЕ prerender.js.
"""
import base64, hashlib, os, re

OUT = "site"
SCRIPT_RE = re.compile(r"<script(?![^>]*\bsrc=)([^>]*)>(.*?)</script>", re.S | re.I)

# внешние адреса, с которыми работает сайт
FORM = "https://script.google.com https://script.googleusercontent.com"      # заявки (Apps Script)
GA = "https://www.googletagmanager.com https://*.google-analytics.com https://*.analytics.google.com"
YM = "https://mc.yandex.ru https://mc.yandex.com https://yastatic.net"


def policy(hashes):
    h = " ".join(f"'sha256-{x}'" for x in sorted(set(hashes)))
    return "; ".join([
        "default-src 'self'",
        f"script-src 'self' {h} https://www.googletagmanager.com https://mc.yandex.ru https://yastatic.net".replace("  ", " "),
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
        "font-src 'self' https://fonts.gstatic.com",
        f"img-src 'self' data: {GA} {YM}",
        f"connect-src 'self' {FORM} {GA} {YM}",
        "frame-src 'none'",
        "object-src 'none'",
        "base-uri 'self'",
        "form-action 'self'",
        "manifest-src 'self'",
        "upgrade-insecure-requests",
    ])


def harden(path):
    html = open(path, encoding="utf-8").read()
    html = re.sub(r'\s*<meta http-equiv="Content-Security-Policy"[^>]*>', "", html)
    html = re.sub(r'\s*<meta name="referrer"[^>]*>', "", html)
    hashes = []
    for attrs, body in SCRIPT_RE.findall(html):
        if re.search(r'type\s*=\s*"application/(ld\+)?json"', attrs, re.I):
            continue                       # данные, а не код: не исполняются
        hashes.append(base64.b64encode(hashlib.sha256(body.encode("utf-8")).digest()).decode())
    meta = (f'<meta http-equiv="Content-Security-Policy" content="{policy(hashes)}">\n'
            '<meta name="referrer" content="strict-origin-when-cross-origin">')
    m = re.search(r'<meta charset="utf-8"\s*/?>', html, re.I)
    if not m:
        raise SystemExit(f"{path}: нет <meta charset>, CSP не поставлен")
    html = html[:m.end()] + "\n" + meta + html[m.end():]
    open(path, "w", encoding="utf-8").write(html)
    return len(hashes)


for root, _, files in os.walk(OUT):
    for f in files:
        if f.endswith(".html"):
            p = os.path.join(root, f)
            print(f"csp {os.path.relpath(p, OUT)}: inline scripts {harden(p)}")
