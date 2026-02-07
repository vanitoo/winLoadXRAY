Сделай правки по таскам ниже.
Правила работы:
- выполняй по 1 таску за раз (если можешь) и показывай diff
- не делай рефакторинг в классы/модули без отдельного таска
- не меняй UX/поведение, кроме явно описанного
- после каждого таска: что поменял + как проверить

TASK 1 (data-loss fix): В clear_xray_configs() НЕ удаляй links.json и state.json (и любые служебные файлы). Удаляй только конфиги.
TASK 2 (tag safety): Гарантируй sanitize_filename(tag) перед записью любых файлов конфигов во ВСЕХ ветках (vless/ss/base64/json). Исключи пустое имя, “..”, слишком длинные имена. Сделай единый sanitize в parsing.py и импортируй.
TASK 3 (remove hacks): Убери двойные вызовы toggle_system_proxy() и run_selected(). Сделай явные функции:
- enable_system_proxy(host,port)
- disable_system_proxy()
- restart_xray_with_tag(tag)
и замени “костыли” на них.
TASK 4 (requests timeout): Добавь timeout во все requests.get (add_from_url, check_latest_version). Минимум: timeout=(5, 15). Добавь headers User-Agent везде одинаково.
TASK 5 (UI freeze fix): Вынеси сетевые запросы из UI потока:
- загрузка подписки
- проверка версии
Сделай через threading.Thread + root.after для обновления UI/листбокса/сообщений.
TASK 6 (process stop safety): stop_xray() и stop_tun2proxy(): добавь wait(timeout=...) и fallback kill(). Исключи зависание UI.
TASK 7 (proxy restore): При включении системного прокси сохрани предыдущие значения ProxyEnable/ProxyServer/ProxyOverride (и что ещё трогаешь) в state.json. При выключении — восстанови ровно как было, а не просто “ProxyEnable=0”.
TASK 8 (paste UX): copyPast.cmd_paste(): НЕ делай stop_xray()+add_from_url() если вставка НЕ в url Entry. Лови конкретные исключения (tk.TclError). Не глотай все ошибки.
TASK 9 (shadowsocks compatibility): parsing.parse_shadowsocks(): поддержи оба формата:
A) ss://BASE64(method:pass)@host:port#tag
B) ss://BASE64(method:pass@host:port)#tag  (самый частый)
+ не падай на ?plugin=... (SIP002) — хотя бы игнорируй plugin часть.
+ санитизируй tag.
TASK 10 (vless validation): parsing.parse_vless(): добавь валидацию обязательных полей (uuid/address/port). Выдавай понятные ValueError, а не cryptic исключения.
TASK 11 (tun patch SS + ipaddress): tun2proxy.patch_direct_out_interface():
- резолвь адреса и для shadowsocks: settings.servers[].address
- определяй IP/домен через ipaddress.ip_address()
- убери дубли resolved_ips
- сделай патч идемпотентным (не добавляй одинаковое routing правило при каждом включении).
TASK 12 (tun routing correctness): В patch_direct_out_interface(): добавляй routing rule для IP серверов так, чтобы эти IP шли direct (как у тебя задумано), но не ломай существующие правила. Если правило уже есть — обнови его, а не добавляй новое.
TASK 13 (DNS safety): tun2proxy.start_tun2proxy()/stop_tun2proxy():
- перед изменением DNS сохрани текущие DNS для "sbtun1" (если существует) и для default interface
- при stop восстанови прежние значения (включая static, не только DHCP)
- избегай shell=True и команд через '&' — вызывай netsh отдельными subprocess.run([...]).
TASK 14 (admin relaunch args): run_as_admin(): прокинь текущие argv (включая --autostart) в новый процесс. Сейчас params пустой.
TASK 15 (resource path robustness): resource_path(): если не frozen — базируйся на Path(__file__).resolve().parent, а не на os.path.abspath(".").
TASK 16 (listbox selection): Привяжи <<ListboxSelect>> к select_config() (актуальная подсветка при клике мышкой/стрелками).
TASK 17 (naming cleanup): Переименуй повторно используемый btnBuffer в btn_refresh/btn_paste (без изменения логики).
TASK 18 (HTML->JSON parsing): В add_from_url() для https:
- сначала пробуй r.json() если Content-Type JSON или если json парсится
- regex очистку HTML используй только как fallback (и аккуратно, например извлекай <pre>).
TASK 19 (logging): Добавь базовый logging в файл %APPDATA%/<APP_NAME>/logs/app.log. Заменяй print на logging.debug/info/warning/exception в критичных местах (network/parsing/tun/proxy).
TASK 20 (configXray reality key): В configXray.py:
- realitySettings: используй publicKey вместо password (pbk)
- добавь минимальную валидацию shortId (hex, <=16) и spiderX (начинается с '/')
- для xhttp extra: unquote перед json.loads
TASK 21 (config output format): В generate_config(): json.dumps(..., ensure_ascii=False) чтобы теги/кириллица не экранировались.
TASK 22 (state consistency): При закрытии (on_closing) порядок: stop_tun2proxy -> stop_system_proxy -> stop_xray -> save_state. Убедись что состояние сохраняется уже после фактических действий.
TASK 23 (startup registry): is_in_startup(): сравнивай нормализованные пути (realpath, lower), учитывай кавычки и аргументы (“--autostart”). Сейчас проверка может дать ложный результат.
TASK 24 (subscription storage): LINKS_FILE: если это список ссылок, сохраняй/загружай все, а не только links[0]. Если задумано только 1 — явно храни строкой, не списком.
TASK 25 (defensive coding): В местах с “except Exception: pass” — либо логируй, либо показывай понятное сообщение, чтобы не скрывать баги.
