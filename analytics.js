/* AQUADIAMOND — analytics loader.
 * Впишите реальные идентификаторы и отправьте сайт на GitHub (push.bat).
 * Пока строки пустые, ничего не загружается и никаких cookies не ставится.
 * ВАЖНО: перед включением обновите раздел 2 Политики конфиденциальности —
 * сейчас там написано, что сайт не использует аналитические cookie.
 */
var GA4_ID = "";        // Google Analytics 4: вида "G-XXXXXXXXXX"
var YM_ID  = "";        // Яндекс Метрика: номер счётчика, только цифры

(function () {
  if (GA4_ID) {
    var s = document.createElement("script");
    s.async = true; s.src = "https://www.googletagmanager.com/gtag/js?id=" + GA4_ID;
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { dataLayer.push(arguments); };
    gtag("js", new Date()); gtag("config", GA4_ID);
  }
  if (YM_ID) {
    (function (m, e, t, r, i, k, a) { m[i] = m[i] || function () { (m[i].a = m[i].a || []).push(arguments); }; m[i].l = 1 * new Date();
      k = e.createElement(t); a = e.getElementsByTagName(t)[0]; k.async = 1; k.src = r; a.parentNode.insertBefore(k, a); })
      (window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");
    ym(Number(YM_ID), "init", { clickmap: true, trackLinks: true, accurateTrackBounce: true, webvisor: false });
  }
})();
