"""Privacy policy texts (RU / UZ / EN) for aquadiamond.uz. {op} {inn} {addr} {phone} {tg} are filled at build time."""

VERSION = {"ru": "Версия 1.0 от 17 ноября 2026 года", "uz": "1.0-versiya, 2026-yil 17-noyabr", "en": "Version 1.0, 17 November 2026"}

TITLE = {"ru": "Политика конфиденциальности", "uz": "Maxfiylik siyosati", "en": "Privacy Policy"}
DESC = {
    "ru": "Как ООО «AQUADIAMOND» обрабатывает персональные данные, оставленные в форме заявки на сайте aquadiamond.uz.",
    "uz": "«AQUADIAMOND» MChJ aquadiamond.uz saytidagi buyurtma shaklida qoldirilgan shaxsiy ma'lumotlarni qanday qayta ishlaydi.",
    "en": "How AQUADIAMOND LLC processes personal data submitted through the request form on aquadiamond.uz.",
}
BACK = {"ru": "← На главную", "uz": "← Bosh sahifa", "en": "← Home"}

RU = [
("1. Кто обрабатывает данные", """
<p>Оператор персональных данных: {op}{inn_ru}, {addr}. Связь по вопросам персональных данных: телефон {phone}, Telegram {tg}.</p>
<p>Политика составлена по Закону Республики Узбекистан от 2 июля 2019 года № ЗРУ-547 «О персональных данных» (с изменениями, в том числе Законом № ЗРУ-1125 от 26 марта 2026 года) и действует для сайта aquadiamond.uz и его версий на узбекском и английском языках.</p>"""),
("2. Какие данные мы получаем", """
<p>Через форму «Расчёт партии»: имя или название компании, номер телефона, комментарий, а также выбранные напиток, формат банки и количество.</p>
<p>Вместе с заявкой сохраняется отметка о согласии: дата и время, версия этой политики, текст согласий и сведения о браузере (user agent).</p>
<p>Мы не запрашиваем паспортные, биометрические, генетические и другие специальные данные. Сайт не использует рекламные и аналитические cookie; в браузере сохраняется только выбранный язык сайта.</p>"""),
("3. Зачем мы их обрабатываем", """
<p>Чтобы ответить на заявку, рассчитать стоимость розлива, подготовить коммерческое предложение и заключить договор. Рекламные рассылки по этим данным мы не отправляем.</p>"""),
("4. Основание обработки", """
<p>Согласие субъекта персональных данных (статья 21 Закона): вы даёте его, отмечая галочку в форме перед отправкой. Без согласия заявка не отправляется. Согласие можно отозвать в любой момент (раздел 9).</p>"""),
("5. Где хранятся данные и кому передаются", """
<p>Заявка записывается в таблицу Google Sheets оператора (сервис Google LLC) и одновременно приходит уведомлением менеджеру в Telegram. Серверы Google и Telegram находятся за пределами Республики Узбекистан. Такая передача выполняется на основании вашего отдельного согласия в соответствии со статьями 15 и 27¹ Закона. Данные, которые закон требует хранить только в Узбекистане (биометрические, генетические, данные абонентов операторов связи), мы не собираем.</p>
<p>Сайт размещён на GitHub Pages (GitHub, Inc.), шрифты загружаются с Google Fonts; при открытии страниц эти сервисы получают технические данные браузера, в том числе IP-адрес.</p>
<p>Мы не продаём и не передаём данные другим лицам, кроме перечисленных сервисов и государственных органов в случаях, предусмотренных законом.</p>"""),
("6. Как мы обрабатываем данные", """
<p>Сбор, запись, систематизация, хранение, уточнение, использование и уничтожение, с использованием средств автоматизации. Решений, которые порождают для вас юридические последствия, только на основе автоматической обработки мы не принимаем.</p>"""),
("7. Сколько храним", """
<p>До достижения целей обработки, но не дольше 3 лет с последнего контакта с вами, либо до отзыва согласия. Если заключён договор, документы по нему хранятся в сроки, установленные налоговым и бухгалтерским законодательством.</p>"""),
("8. Как защищаем", """
<p>Сайт работает по защищённому протоколу HTTPS. Доступ к таблице заявок есть только у уполномоченных сотрудников оператора. Ключи доступа к Telegram-боту хранятся в закрытых настройках Google Apps Script и не публикуются в коде сайта.</p>"""),
("9. Ваши права и как ими воспользоваться", """
<p>Вы вправе знать, обрабатываются ли ваши данные, получить информацию об их составе, целях, сроках и о трансграничной передаче, потребовать исправить неточные данные, заблокировать или уничтожить их, отозвать согласие, а также обжаловать действия оператора в уполномоченном государственном органе в области персональных данных или в суде (статьи 11, 21, 22 и 30 Закона).</p>
<p>Для этого напишите в Telegram {tg} или позвоните по телефону {phone}. Неточные данные исправляем в течение трёх дней. После отзыва согласия прекращаем обработку и удаляем ваши данные из таблицы заявок.</p>"""),
("10. Возраст", """<p>Сайт предназначен для компаний и предпринимателей. Мы не собираем данные лиц младше 18 лет намеренно.</p>"""),
("11. Изменения политики", """<p>Новая редакция публикуется на этой странице с новой датой. Версия, с которой вы согласились, сохраняется вместе с вашей заявкой.</p>"""),
]

UZ = [
("1. Ma'lumotlarni kim qayta ishlaydi", """
<p>Shaxsiy ma'lumotlar operatori: {op}{inn_uz}, {addr}. Shaxsiy ma'lumotlar bo'yicha aloqa: telefon {phone}, Telegram {tg}.</p>
<p>Siyosat O'zbekiston Respublikasining 2019-yil 2-iyuldagi O'RQ-547-son «Shaxsga doir ma'lumotlar to'g'risida»gi Qonuni (o'zgartishlar, shu jumladan 2026-yil 26-martdagi O'RQ-1125-son Qonun bilan) asosida tuzilgan va aquadiamond.uz sayti hamda uning o'zbek va ingliz tilidagi versiyalariga tatbiq etiladi.</p>"""),
("2. Qanday ma'lumotlarni olamiz", """
<p>«Partiya hisobi» shakli orqali: ism yoki kompaniya nomi, telefon raqami, izoh, shuningdek tanlangan ichimlik, banka formati va soni.</p>
<p>Buyurtma bilan birga rozilik belgisi saqlanadi: sana va vaqt, ushbu siyosat versiyasi, roziliklar matni va brauzer haqidagi ma'lumot (user agent).</p>
<p>Biz pasport, biometrik, genetik va boshqa maxsus ma'lumotlarni so'ramaymiz. Sayt reklama va analitika cookie-fayllaridan foydalanmaydi; brauzerda faqat tanlangan sayt tili saqlanadi.</p>"""),
("3. Nima maqsadda qayta ishlaymiz", """
<p>Buyurtmaga javob berish, quyish narxini hisoblash, tijorat taklifini tayyorlash va shartnoma tuzish uchun. Ushbu ma'lumotlar bo'yicha reklama xabarlarini yubormaymiz.</p>"""),
("4. Qayta ishlash asosi", """
<p>Shaxsiy ma'lumotlar subyektining roziligi (Qonunning 21-moddasi): uni yuborishdan oldin shakldagi belgini qo'yish orqali berasiz. Roziliksiz buyurtma yuborilmaydi. Rozilikni istalgan vaqtda qaytarib olish mumkin (9-bo'lim).</p>"""),
("5. Ma'lumotlar qayerda saqlanadi va kimga uzatiladi", """
<p>Buyurtma operatorning Google Sheets jadvaliga (Google LLC xizmati) yoziladi va bir vaqtda menejerga Telegram orqali xabar sifatida keladi. Google va Telegram serverlari O'zbekiston Respublikasidan tashqarida joylashgan. Bunday uzatish Qonunning 15 va 27¹-moddalariga muvofiq sizning alohida roziligingiz asosida amalga oshiriladi. Qonun faqat O'zbekistonda saqlashni talab qiladigan ma'lumotlarni (biometrik, genetik, aloqa operatorlari abonentlari ma'lumotlari) biz yig'maymiz.</p>
<p>Sayt GitHub Pages (GitHub, Inc.) da joylashgan, shriftlar Google Fonts'dan yuklanadi; sahifalar ochilganda bu xizmatlar brauzerning texnik ma'lumotlarini, shu jumladan IP-manzilni oladi.</p>
<p>Biz ma'lumotlarni sotmaymiz va sanab o'tilgan xizmatlar hamda qonunda nazarda tutilgan hollarda davlat organlaridan boshqa shaxslarga bermaymiz.</p>"""),
("6. Ma'lumotlarni qanday qayta ishlaymiz", """
<p>Yig'ish, yozib olish, tizimlashtirish, saqlash, aniqlashtirish, foydalanish va yo'q qilish, avtomatlashtirish vositalari yordamida. Siz uchun huquqiy oqibatlar keltirib chiqaradigan qarorlarni faqat avtomatik qayta ishlash asosida qabul qilmaymiz.</p>"""),
("7. Qancha muddat saqlaymiz", """
<p>Qayta ishlash maqsadlariga erishilgunga qadar, lekin siz bilan oxirgi aloqadan boshlab 3 yildan ko'p bo'lmagan muddatda yoki rozilik qaytarib olingunga qadar. Shartnoma tuzilgan bo'lsa, u bo'yicha hujjatlar soliq va buxgalteriya qonunchiligida belgilangan muddatlarda saqlanadi.</p>"""),
("8. Qanday himoya qilamiz", """
<p>Sayt HTTPS himoyalangan protokoli orqali ishlaydi. Buyurtmalar jadvaliga faqat operatorning vakolatli xodimlari kira oladi. Telegram-botga kirish kalitlari Google Apps Script'ning yopiq sozlamalarida saqlanadi va sayt kodida e'lon qilinmaydi.</p>"""),
("9. Huquqlaringiz va ulardan qanday foydalanish", """
<p>Siz ma'lumotlaringiz qayta ishlanayotganini bilish, ularning tarkibi, maqsadlari, muddatlari va transchegaraviy uzatilishi haqida ma'lumot olish, noto'g'ri ma'lumotlarni tuzatishni, ularni bloklash yoki yo'q qilishni talab qilish, rozilikni qaytarib olish, shuningdek operator harakatlari ustidan shaxsga doir ma'lumotlar sohasidagi vakolatli davlat organiga yoki sudga shikoyat qilish huquqiga egasiz (Qonunning 11, 21, 22 va 30-moddalari).</p>
<p>Buning uchun Telegram {tg} ga yozing yoki {phone} telefoniga qo'ng'iroq qiling. Noto'g'ri ma'lumotlarni uch kun ichida tuzatamiz. Rozilik qaytarib olingach, qayta ishlashni to'xtatamiz va ma'lumotlaringizni buyurtmalar jadvalidan o'chiramiz.</p>"""),
("10. Yosh", """<p>Sayt kompaniyalar va tadbirkorlar uchun mo'ljallangan. Biz 18 yoshga to'lmagan shaxslarning ma'lumotlarini ataylab yig'maymiz.</p>"""),
("11. Siyosatdagi o'zgarishlar", """<p>Yangi tahrir ushbu sahifada yangi sana bilan e'lon qilinadi. Siz rozilik bergan versiya buyurtmangiz bilan birga saqlanadi.</p>"""),
]

EN = [
("1. Who processes the data", """
<p>Personal data operator: {op}{inn_en}, {addr}. Contact on personal data matters: phone {phone}, Telegram {tg}.</p>
<p>This policy follows Law of the Republic of Uzbekistan No. ZRU-547 of 2 July 2019 "On Personal Data" (as amended, including by Law No. ZRU-1125 of 26 March 2026) and applies to aquadiamond.uz and its Uzbek and English versions.</p>"""),
("2. What data we receive", """
<p>Through the "Batch estimate" form: name or company name, phone number, comment, and the selected drink, can format and quantity.</p>
<p>A consent record is stored with each request: date and time, the version of this policy, the consent wording and browser details (user agent).</p>
<p>We do not ask for passport, biometric, genetic or other special categories of data. The site uses no advertising or analytics cookies; the browser only stores the chosen site language.</p>"""),
("3. Why we process it", """
<p>To answer your request, estimate the filling cost, prepare a commercial offer and conclude a contract. We do not send marketing messages using this data.</p>"""),
("4. Legal basis", """
<p>The data subject's consent (Article 21 of the Law), which you give by ticking the box in the form before sending. A request cannot be sent without consent. You may withdraw consent at any time (section 9).</p>"""),
("5. Where the data is stored and who receives it", """
<p>The request is recorded in the operator's Google Sheets spreadsheet (a Google LLC service) and sent as a notification to a manager on Telegram. Google and Telegram servers are located outside the Republic of Uzbekistan. This transfer is based on your separate consent under Articles 15 and 27¹ of the Law. We do not collect data that the law requires to be stored only in Uzbekistan (biometric, genetic, telecom subscriber data).</p>
<p>The site is hosted on GitHub Pages (GitHub, Inc.) and fonts load from Google Fonts; when pages open, these services receive technical browser data, including the IP address.</p>
<p>We do not sell the data or share it with anyone other than the services listed above and public authorities where the law requires.</p>"""),
("6. How we process the data", """
<p>Collection, recording, organisation, storage, correction, use and destruction, with automated means. We make no decisions with legal effect for you based solely on automated processing.</p>"""),
("7. How long we keep it", """
<p>Until the purposes are achieved, but no longer than 3 years after our last contact with you, or until you withdraw consent. If a contract is concluded, its documents are kept for the periods set by tax and accounting law.</p>"""),
("8. How we protect it", """
<p>The site runs over HTTPS. Only the operator's authorised staff can access the request spreadsheet. The Telegram bot access keys are kept in private Google Apps Script settings and are not published in the site code.</p>"""),
("9. Your rights and how to use them", """
<p>You have the right to know whether your data is processed, to receive information on its scope, purposes, retention and cross-border transfer, to have inaccurate data corrected, blocked or destroyed, to withdraw consent, and to complain about the operator to the authorised state body for personal data or to a court (Articles 11, 21, 22 and 30 of the Law).</p>
<p>To do so, message {tg} on Telegram or call {phone}. We correct inaccurate data within three days. After you withdraw consent we stop processing and delete your data from the request spreadsheet.</p>"""),
("10. Age", """<p>The site is intended for companies and entrepreneurs. We do not knowingly collect data from persons under 18.</p>"""),
("11. Changes to this policy", """<p>A new version is published on this page with a new date. The version you agreed to is stored with your request.</p>"""),
]

SECTIONS = {"ru": RU, "uz": UZ, "en": EN}
