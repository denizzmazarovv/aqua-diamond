/**
 * AQUADIAMOND — приём заявок с сайта aquadiamond.uz
 * Таблица Google вместо базы данных + уведомления в Telegram.
 *
 * Токен бота НЕ хранится в коде и НЕ хранится на GitHub.
 * Он вводится один раз через меню таблицы «AQUADIAMOND → Подключить Telegram-бота»
 * и лежит в свойствах скрипта (Script Properties), которые видит только владелец таблицы.
 */

const POLICY_VERSION = '1.0 от 17.11.2026';
const TZ = 'Asia/Tashkent';
// Группа, куда приходят заявки (ID чата не секрет, токен бота — секрет и здесь не хранится)
const DEFAULT_CHAT_ID = '-5508096488';

const SHEETS = {
  leads: 'Заявки',
  consents: 'Согласия',
  stats: 'Статистика',
  withdrawals: 'Отзыв согласий',
  reference: 'Справочник'
};

const LEAD_HEADERS = [
  'ID заявки', 'Дата и время', 'Язык сайта', 'Имя / компания', 'Телефон', 'Напиток', 'Банка',
  'Банок', 'Ориентир, сум', 'Комментарий', 'Статус', 'Менеджер', 'Заметки менеджера', 'Страница'
];
const CONSENT_HEADERS = [
  'Дата и время', 'ID заявки', 'Имя / компания', 'Телефон', 'Согласие на обработку ПД',
  'Согласие на трансграничную передачу', 'Версия политики', 'Текст согласий', 'Браузер'
];
const WITHDRAW_HEADERS = [
  'Дата обращения', 'Кто обратился (имя, телефон)', 'Канал (Telegram, телефон, письмо)',
  'Что просит (отозвать согласие, удалить, исправить)', 'Что сделано', 'Дата исполнения', 'Ответственный'
];
const STATUSES = ['Новая', 'В работе', 'КП отправлено', 'Образцы / дегустация', 'Договор', 'Отказ', 'Спам'];

/* ---------------- меню ---------------- */
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('AQUADIAMOND')
    .addItem('1. Создать листы и оформление', 'setup')
    .addItem('2. Подключить Telegram-бота (ввести токен)', 'connectBot')
    .addItem('3. Найти чат после /start боту', 'findChats')
    .addItem('4. Отправить тестовое сообщение', 'testTelegram')
    .addSeparator()
    .addItem('Показать подключённые чаты', 'showChats')
    .addToUi();
}

/* ---------------- создание листов ---------------- */
function setup() {
  const ss = SpreadsheetApp.getActive();
  ss.setSpreadsheetTimeZone(TZ);

  const leads = getOrCreate_(ss, SHEETS.leads);
  writeHeader_(leads, LEAD_HEADERS);
  leads.setColumnWidths(1, 14, 140);
  leads.setColumnWidth(4, 200); leads.setColumnWidth(10, 280); leads.setColumnWidth(13, 260);
  leads.getRange('E:E').setNumberFormat('@');
  leads.getRange('B:B').setNumberFormat('dd.MM.yyyy HH:mm');
  leads.getRange('H:I').setNumberFormat('#,##0');
  const statusRule = SpreadsheetApp.newDataValidation().requireValueInList(STATUSES, true).setAllowInvalid(false).build();
  leads.getRange(2, 11, 2000, 1).setDataValidation(statusRule);
  const colors = { 'Новая': '#fff4cc', 'В работе': '#dbeafe', 'КП отправлено': '#e0e7ff', 'Образцы / дегустация': '#ede9fe', 'Договор': '#dcfce7', 'Отказ': '#f3f4f6', 'Спам': '#fee2e2' };
  const rng = leads.getRange('A2:N2000');
  leads.setConditionalFormatRules(Object.keys(colors).map(s =>
    SpreadsheetApp.newConditionalFormatRule().whenFormulaSatisfied('=$K2="' + s + '"').setBackground(colors[s]).setRanges([rng]).build()));
  if (!leads.getFilter()) leads.getRange(1, 1, 1, LEAD_HEADERS.length).createFilter();

  const cons = getOrCreate_(ss, SHEETS.consents);
  writeHeader_(cons, CONSENT_HEADERS);
  cons.setColumnWidths(1, 9, 160); cons.setColumnWidth(8, 420);
  cons.getRange('D:D').setNumberFormat('@');
  cons.getRange('A:A').setNumberFormat('dd.MM.yyyy HH:mm:ss');

  const wd = getOrCreate_(ss, SHEETS.withdrawals);
  writeHeader_(wd, WITHDRAW_HEADERS);
  wd.setColumnWidths(1, 7, 200);
  wd.getRange('A2').setNote('Сюда вносятся обращения людей об отзыве согласия, исправлении или удалении данных. ' +
    'По закону «О персональных данных» данные исправляются в течение 3 дней, а после отзыва согласия обработка прекращается. ' +
    'Удалите строки этого человека на листах «Заявки» и «Согласия» и отметьте здесь дату.');

  const ref = getOrCreate_(ss, SHEETS.reference);
  ref.clear();
  const refRows = [
    ['Параметр', 'Значение', 'Где используется'],
    ['Цена розлива, от', 700, 'Калькулятор на сайте, сум за банку'],
    ['Минимальная партия', 12000, 'банок'],
    ['Мощность одной линии', 300000, 'банок в сутки'],
    ['Линий розлива', 3, ''],
    ['Версия политики конфиденциальности', POLICY_VERSION, 'Записывается в каждое согласие'],
    ['Статусы заявки', STATUSES.join(', '), 'Выпадающий список на листе «Заявки»']
  ];
  ref.getRange(1, 1, refRows.length, 3).setValues(refRows);
  styleHeader_(ref.getRange(1, 1, 1, 3));
  ref.setColumnWidths(1, 3, 260);

  const st = getOrCreate_(ss, SHEETS.stats);
  st.clear();
  const L = "'" + SHEETS.leads + "'!";
  const rows = [
    ['Показатель', 'Значение'],
    ['Всего заявок', '=COUNTA(' + L + 'A2:A)'],
    ['Заявок за сегодня', '=COUNTIFS(' + L + 'B2:B,">="&TODAY())'],
    ['Заявок за 7 дней', '=COUNTIFS(' + L + 'B2:B,">="&TODAY()-6)'],
    ['Заявок в этом месяце', '=COUNTIFS(' + L + 'B2:B,">="&EOMONTH(TODAY(),-1)+1)'],
    ['Банок во всех заявках', '=SUM(' + L + 'H2:H)'],
    ['Ориентир по всем заявкам, сум', '=SUM(' + L + 'I2:I)'],
    ['', ''],
    ['Напиток', 'Заявок'],
    ['Энергетик', '=COUNTIF(' + L + 'F2:F,"Энергетик")'],
    ['Лимонад', '=COUNTIF(' + L + 'F2:F,"Лимонад")'],
    ['Газ. напиток', '=COUNTIF(' + L + 'F2:F,"Газ. напиток")'],
    ['', ''],
    ['Статус', 'Заявок']
  ].concat(STATUSES.map(s => [s, '=COUNTIF(' + L + 'K2:K,"' + s + '")']));
  // формулы пишем через setFormula: он всегда понимает английский синтаксис, независимо от языка таблицы
  const SEP = /^en/.test(ss.getSpreadsheetLocale()) ? ',' : ';'; // в русской/узбекской таблице аргументы разделяются «;»
  st.getRange(1, 1, rows.length, 1).setValues(rows.map(r => [r[0]]));
  rows.forEach((r, i) => { const c = st.getRange(i + 1, 2); String(r[1]).charAt(0) === '=' ? c.setFormula(r[1].replace(/,/g, SEP)) : c.setValue(r[1]); });
  [1, 9, 14].forEach(r => styleHeader_(st.getRange(r, 1, 1, 2)));
  st.getRange('B6:B7').setNumberFormat('#,##0');
  st.setColumnWidth(1, 280); st.setColumnWidth(2, 160);
  st.getCharts().forEach(c => st.removeChart(c));
  st.insertChart(st.newChart().asPieChart().addRange(st.getRange('A10:B12'))
    .setPosition(1, 4, 0, 0).setOption('title', 'Заявки по напиткам').build());
  st.insertChart(st.newChart().asBarChart().addRange(st.getRange('A15:B' + (14 + STATUSES.length)))
    .setPosition(20, 4, 0, 0).setOption('title', 'Заявки по статусам').setOption('legend', { position: 'none' }).build());

  // порядок листов, лишний «Лист1» удаляем
  [SHEETS.leads, SHEETS.stats, SHEETS.consents, SHEETS.withdrawals, SHEETS.reference].forEach((n, i) => {
    ss.setActiveSheet(ss.getSheetByName(n)); ss.moveActiveSheet(i + 1);
  });
  ['Лист1', 'Sheet1'].forEach(n => { const s = ss.getSheetByName(n); if (s && ss.getSheets().length > 1) ss.deleteSheet(s); });
  ss.setActiveSheet(leads);
  SpreadsheetApp.getUi().alert('Готово: листы созданы. Дальше: меню AQUADIAMOND → 2. Подключить Telegram-бота.');
}

/* ---------------- Telegram ---------------- */
function connectBot() {
  const ui = SpreadsheetApp.getUi();
  const r = ui.prompt('Токен Telegram-бота',
    'Вставьте токен от @BotFather (вида 123456789:AA...). Он сохранится только в свойствах этого скрипта и не попадёт ни на сайт, ни на GitHub.',
    ui.ButtonSet.OK_CANCEL);
  if (r.getSelectedButton() !== ui.Button.OK) return;
  const token = r.getResponseText().trim();
  const me = tg_(token, 'getMe', {});
  if (!me.ok) { ui.alert('Telegram не принял токен: ' + (me.description || 'ошибка')); return; }
  PropertiesService.getScriptProperties().setProperty('TG_TOKEN', token);
  ui.alert('Бот @' + me.result.username + ' подключён.\n\nТеперь каждый, кто должен получать заявки, пусть откроет бота в Telegram и нажмёт «Start». ' +
    'Потом выберите меню AQUADIAMOND → 3. Найти чат после /start боту.');
}

function findChats() {
  const ui = SpreadsheetApp.getUi();
  const token = PropertiesService.getScriptProperties().getProperty('TG_TOKEN');
  if (!token) { ui.alert('Сначала подключите бота (пункт 2).'); return; }
  const up = tg_(token, 'getUpdates', {});
  if (!up.ok) { ui.alert('Ошибка Telegram: ' + up.description); return; }
  const chats = getChats_();
  up.result.forEach(u => {
    const m = u.message || u.my_chat_member || u.channel_post;
    if (m && m.chat) chats[m.chat.id] = m.chat.title || ('@' + (m.chat.username || '') + ' ' + (m.chat.first_name || '')).trim();
  });
  PropertiesService.getScriptProperties().setProperty('TG_CHATS', JSON.stringify(chats));
  const list = Object.keys(chats).map(id => chats[id] + ' (' + id + ')').join('\n');
  ui.alert(list ? 'Заявки будут приходить в:\n' + list : 'Чатов не найдено. Нажмите «Start» в боте и повторите.');
}

function showChats() {
  const chats = getChats_();
  SpreadsheetApp.getUi().alert(Object.keys(chats).map(id => chats[id] + ' (' + id + ')').join('\n') || 'Чатов пока нет.');
}

function testTelegram() {
  const n = notify_('✅ Тест: бот AQUADIAMOND подключён, заявки с сайта будут приходить сюда.');
  SpreadsheetApp.getUi().alert(n ? 'Отправлено в чатов: ' + n : 'Не отправлено: проверьте пункты 2 и 3.');
}

function getChats_() {
  let chats = {};
  try { chats = JSON.parse(PropertiesService.getScriptProperties().getProperty('TG_CHATS') || '{}'); } catch (e) {}
  if (DEFAULT_CHAT_ID && !chats[DEFAULT_CHAT_ID]) chats[DEFAULT_CHAT_ID] = 'Группа заявок';
  return chats;
}

function tg_(token, method, payload) {
  const res = UrlFetchApp.fetch('https://api.telegram.org/bot' + token + '/' + method, {
    method: 'post', contentType: 'application/json', payload: JSON.stringify(payload), muteHttpExceptions: true
  });
  try { return JSON.parse(res.getContentText()); } catch (e) { return { ok: false, description: res.getContentText() }; }
}

function notify_(html) {
  const token = PropertiesService.getScriptProperties().getProperty('TG_TOKEN');
  if (!token) return 0;
  let sent = 0;
  Object.keys(getChats_()).forEach(id => {
    const r = tg_(token, 'sendMessage', { chat_id: id, text: html, parse_mode: 'HTML', disable_web_page_preview: true });
    if (r.ok) sent++;
  });
  return sent;
}

/* ---------------- приём заявки с сайта ---------------- */
function doPost(e) {
  try {
    const d = JSON.parse((e && e.postData && e.postData.contents) || '{}');

    // защита от спама
    if (d.website) return json_({ ok: true });                       // скрытое поле-ловушка заполнено ботом
    if (!d.t || Number(d.t) < 2500) return json_({ ok: false, error: 'too_fast' });
    const name = clean_(d.name, 120), phone = clean_(d.phone, 40);
    if (!name || phone.replace(/\D/g, '').length < 7) return json_({ ok: false, error: 'validation' });
    if (d.consentPd !== true || d.consentTransfer !== true) return json_({ ok: false, error: 'consent' });
    const cache = CacheService.getScriptCache(), key = 'p' + phone.replace(/\D/g, '');
    if (cache.get(key)) return json_({ ok: false, error: 'rate' });
    cache.put(key, '1', 60);

    const lock = LockService.getScriptLock();
    lock.waitLock(10000);
    const ss = SpreadsheetApp.getActive();
    const leads = ss.getSheetByName(SHEETS.leads), cons = ss.getSheetByName(SHEETS.consents);
    const now = new Date();
    const id = 'AD-' + Utilities.formatDate(now, TZ, 'yyMMdd') + '-' + String(leads.getLastRow()).padStart(4, '0');
    const cans = Math.max(0, Math.round(Number(d.cans) || 0));
    const est = Math.max(0, Math.round(Number(d.estimate) || 0));
    leads.appendRow([id, now, clean_(d.lang, 5), name, phone, clean_(d.kind, 40), clean_(d.can, 20), cans, est,
      clean_(d.note, 1000), 'Новая', '', '', clean_(d.page, 200)]);
    cons.appendRow([now, id, name, phone, 'Да', 'Да', POLICY_VERSION, clean_(d.consentText, 1500), clean_(d.ua, 300)]);
    lock.releaseLock();

    const url = ss.getUrl() + '#gid=' + leads.getSheetId();
    const h = s => String(s).replace(/^'/, '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    notify_('🥤 <b>Новая заявка ' + id + '</b>\n\n' +
      '<b>' + h(name) + '</b>\n📞 ' + h(phone) + '\n' +
      (d.kind ? 'Напиток: ' + h(clean_(d.kind, 40)) + '\n' : '') +
      (d.can ? 'Банка: ' + h(clean_(d.can, 20)) + '\n' : '') +
      (cans ? 'Банок: ' + cans.toLocaleString('ru-RU') + '\n' : '') +
      (est ? 'Ориентир: ~' + est.toLocaleString('ru-RU') + ' сум\n' : '') +
      (d.note ? '\n💬 ' + h(clean_(d.note, 1000)) + '\n' : '') +
      '\n<a href="' + url + '">Открыть таблицу</a>');
    return json_({ ok: true, id: id });
  } catch (err) {
    console.error(err);
    return json_({ ok: false, error: 'server' });
  }
}

function doGet() {
  return json_({ ok: true, service: 'AQUADIAMOND leads' });
}

/* ---------------- служебное ---------------- */
function clean_(v, max) {
  let s = String(v == null ? '' : v).replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g, '').trim().slice(0, max);
  if (/^[=+\-@]/.test(s)) s = "'" + s;   // защита от формул в таблице
  return s;
}
function json_(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}
function getOrCreate_(ss, name) {
  return ss.getSheetByName(name) || ss.insertSheet(name);
}
function writeHeader_(sh, headers) {
  sh.getRange(1, 1, 1, headers.length).setValues([headers]);
  styleHeader_(sh.getRange(1, 1, 1, headers.length));
  sh.setFrozenRows(1);
}
function styleHeader_(r) {
  r.setFontWeight('bold').setBackground('#08798a').setFontColor('#ffffff').setWrap(true).setVerticalAlignment('middle');
}
