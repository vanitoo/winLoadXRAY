from urllib.parse import urlparse, parse_qs, unquote
import base64
import re

def sanitize_filename(name):
    """
    Безопасное имя файла: удаляет недопустимые символы, проверяет на пустоту и спец. значения.
    Гарантирует безопасное имя для сохранения конфигурационных файлов.
    """
    if not name or not name.strip():
        return "unnamed_config"
    
    name = name.strip()
    
    # Запрещаем опасные значения
    if name in (".", ".."):
        return "unnamed_config"
    
    # Удаляем недопустимые символы для Windows
    name = re.sub(r'[<>:"/\\|?*]', '_', name)
    
    # Удаляем непечатаемые символы
    name = re.sub(r'[\x00-\x1f\x7f]', '', name)
    
    # Обрезаем слишком длинные имена (Windows ограничение 255, берем с запасом)
    max_length = 200
    if len(name) > max_length:
        name = name[:max_length]
    
    # Убираем точки в начале и конце (проблемы в Windows)
    name = name.strip('. ')
    
    # Если после всех преобразований имя пустое
    if not name:
        return "unnamed_config"
    
    return name

# --- Парсинг VLESS-ссылки ---
def parse_vless(url):
    parsed = urlparse(url)
    uuid = parsed.username
    address = parsed.hostname
    port = int(parsed.port)
    params = parse_qs(parsed.query)
    tag = parsed.fragment or f"{address}:{port}"
    tag = unquote(tag)  # Декодируем emoji и кириллицу
    tag = sanitize_filename(tag)

    return {
        "protocol": "vless",
        "uuid": uuid,
        "address": address,
        "port": port,
        "security": params.get("security", ["reality"])[0],
        "network": params.get("type", ["raw"])[0],
        "headerType": params.get("headerType", [""])[0],
        "path": params.get("path", [""])[0],
        "host": params.get("host", [""])[0],
        "flow": params.get("flow", [""])[0],
        "sni": params.get("sni", [""])[0],
        "fp": params.get("fp", ["chrome"])[0],
        "pbk": params.get("pbk", [""])[0],
        "sid": params.get("sid", [""])[0],
        "spx": params.get("spx", ["/"])[0],

            "extra": params.get("extra", [""])[0],
            "mode": params.get("mode", ["auto"])[0],

        "pqv": params.get("pqv", [""])[0],
        "tag": tag
    }

# --- Парсинг SS-ссылки ---
def parse_shadowsocks(url):
    assert url.startswith("ss://")
    url = url[5:]

    if "#" in url:
        url, tag = url.split("#", 1)
        tag = unquote(tag)
    else:
        tag = "ss_config"

    if "@" in url:
        base64_part, address_part = url.split("@", 1)
        padded = base64_part + '=' * (-len(base64_part) % 4)
        decoded = base64.urlsafe_b64decode(padded).decode("utf-8")
        method, password = decoded.split(":", 1)
        server, port = address_part.split(":")
    else:
        raise ValueError("Некорректный формат Shadowsocks ссылки")

    # Применяем sanitize_filename к тегу
    tag = sanitize_filename(tag)

    return {
        "protocol": "shadowsocks",
        "tag": tag,
        "server": server,
        "port": int(port),
        "method": method,
        "password": password
    }

