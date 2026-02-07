import tkinter as tk
from tkinter import messagebox, filedialog, PhotoImage
from PIL import Image, ImageTk
import base64
import requests
import json
import sys
import os
import shutil
import subprocess
import winreg
import re
import ctypes
import webbrowser
from urllib.parse import urlparse, parse_qs, unquote

sys.path.append(os.path.join(os.path.dirname(__file__), 'func'))
from parsing import parse_vless, parse_shadowsocks, sanitize_filename
from configXray import generate_config
from tun2proxy import get_default_interface, patch_direct_out_interface, start_tun2proxy, stop_tun2proxy
from copyPast import cmd_copy, cmd_paste, cmd_cut, cmd_select_all

APP_NAME = "winLoadXRAY"
APP_VERS = "v0.84-beta"
XRAY_VERS = "v25.12.8"

xray_process = None
tun_enabled = False

IS_AUTOSTART = "--autostart" in sys.argv

# --- Функция для проверки последней версии на GitHub ---
def check_latest_version():
    try:
        # Получаем информацию о последнем релизе
        response = requests.get("https://api.github.com/repos/xVRVx/winLoadXRAY/releases/latest", timeout=10)
        response.raise_for_status()
        latest_release = response.json()
        latest_version = latest_release.get("tag_name", "")
        
        # Сравниваем версии
        if latest_version and latest_version != APP_VERS:
            # Показываем красную ссылку для скачивания
            show_update_link(latest_version)
    except Exception as e:
        print(f"Ошибка при проверке версии: {e}")

def show_update_link(latest_version):
  
    update_link = tk.Label(
        frameBot,
        text=f"Доступна: {latest_version}",
        fg="#2f97d3",
        bg="#e8e8e8",
        cursor="hand2",
        font=("Arial", 10, "underline")
    )
    ToolTip(update_link, "Замените: "+ get_executable_path())
    
    update_link.pack(side="right", padx=(0, 20), pady=5)  # Добавляем отступ справа

    # Обработчик клика по ссылке
    def download_update(event):
        webbrowser.open_new("https://github.com/xVRVx/winLoadXRAY/releases/")
        # webbrowser.open_new("https://github.com/xVRVx/winLoadXRAY/releases/latest/download/winLoadXRAY.exe")
    
    update_link.bind("<Button-1>", download_update)


def open_link(event):
    webbrowser.open_new("https://t.me/SkyBridge_VPN_bot")

def github(event):
    webbrowser.open_new("https://github.com/xVRVx/winLoadXRAY/")

active_tag = None
proxy_enabled = False

base64_urls = []


CONFIGS_DIR = os.path.join(os.getenv('APPDATA'), APP_NAME, 'configs')
os.makedirs(CONFIGS_DIR, exist_ok=True)
    
#CONFIG_LIST_FILE = os.path.join(CONFIGS_DIR, "config_list.json")
LINKS_FILE = os.path.join(CONFIGS_DIR, "links.json")

STATE_FILE = os.path.join(CONFIGS_DIR, "state.json")


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
    
XRAY_EXE = resource_path("xray/xray.exe")


CREATE_NO_WINDOW = 0x08000000


def save_state():
    state = {
        "active_tag": active_tag,
        "proxy_enabled": proxy_enabled
    }
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        print(f"Ошибка сохранения состояния: {e}")
        
def load_state():
    global active_tag, proxy_enabled

    if not os.path.exists(STATE_FILE):
        return

    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)
        active_tag = state.get("active_tag")
        proxy_enabled = state.get("proxy_enabled", False)

        if proxy_enabled:
            
            toggle_system_proxy()  # включаем системный прокси
            toggle_system_proxy()  # костыль)


        if active_tag and active_tag in configs:
            highlight_active(active_tag)
            # Автозапуск Xray
            config_path = os.path.join(CONFIGS_DIR, f"{active_tag}.json")
            if os.path.exists(config_path):
                global xray_process
                xray_process = subprocess.Popen([XRAY_EXE, "-config", config_path], creationflags=CREATE_NO_WINDOW)
                btn_run.config(text="Остановить конфиг", bg="lightgreen")

    except Exception as e:
        print(f"Ошибка загрузки состояния: {e}")
        


def update_proxy_button_color():
    if proxy_enabled:
        btn_proxy.config(bg="orange")
    else:
        btn_proxy.config(bg="SystemButtonFace")  # цвет по умолчанию на Windows

def save_base64_urls():
    global base64_urls
    with open(LINKS_FILE, "w", encoding="utf-8") as f:
        json.dump(base64_urls, f, ensure_ascii=False, indent=2)

def load_base64_urls():
    # 1. Загружаем все старые конфиги из папки
    configs.clear()
    listbox.delete(0, tk.END)

    for filename in os.listdir(CONFIGS_DIR):
        if filename.endswith(".json") and filename not in ("links.json", "state.json"):
            try:
                with open(os.path.join(CONFIGS_DIR, filename), "r", encoding="utf-8") as f:
                    config_data = json.load(f)
                    tag = config_data.get("tag", os.path.splitext(filename)[0])
                    configs[tag] = config_data
                    listbox.insert(tk.END, tag)
            except Exception as e:
                print(f"Не удалось загрузить конфиг {filename}: {e}")

    # 2. Загружаем подписку из LINKS_FILE (как было раньше)
    if os.path.exists(LINKS_FILE):
        with open(LINKS_FILE, "r", encoding="utf-8") as f:
            links = json.load(f)

        if isinstance(links, list) and links:
            link = links[0]  # Берём первую ссылку
        else:
            return  # Нечего загружать

        entry.delete(0, tk.END)
        entry.insert(0, link)
        # if listbox.size() > 0:
            # listbox.select_set(0)






# --- Инициализация ---
if not os.path.exists(CONFIGS_DIR):
    os.makedirs(CONFIGS_DIR)

configs = {}



# --- Системный прокси ---
def enable_system_proxy(host="127.0.0.1", port=2080):
    """Явное включение системного прокси"""
    global proxy_enabled
    path = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 1)
            winreg.SetValueEx(key, "ProxyServer", 0, winreg.REG_SZ, f"{host}:{port}")
        proxy_enabled = True
        btn_proxy.config(text="Выключить системный прокси")
        save_state()
        update_proxy_button_color()
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось включить прокси: {e}")

def disable_system_proxy():
    """Явное отключение системного прокси"""
    global proxy_enabled
    path = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 0)
        proxy_enabled = False
        btn_proxy.config(text="Включить системный прокси")
        save_state()
        update_proxy_button_color()
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось отключить прокси: {e}")

def toggle_system_proxy(host="127.0.0.1", port=2080):
    """Переключение системного прокси (для совместимости с UI)"""
    if not proxy_enabled:
        enable_system_proxy(host, port)
    else:
        disable_system_proxy()

def clear_xray_configs():
    # Очистка старых данных (только конфиги, НЕ служебные файлы)
    configs.clear()
    listbox.delete(0, tk.END)
    
    # Удаляем только json-файлы конфигов из папки CONFIGS_DIR
    # НЕ удаляем служебные файлы: links.json, state.json
    UTILITY_FILES = {"links.json", "state.json"}
    
    for filename in os.listdir(CONFIGS_DIR):
        if filename.endswith(".json") and filename not in UTILITY_FILES:
            try:
                os.remove(os.path.join(CONFIGS_DIR, filename))
            except Exception as e:
                print(f"Не удалось удалить файл {filename}: {e}")

def add_from_url():
    global base64_urls
    stop_xray()
    stop_system_proxy()
    input_text = entry.get().strip()

    if input_text.startswith("vless://"):
        clear_xray_configs()
        base64_urls = []
        # Добавляем одну прямую VLESS ссылку
        try:
            data = parse_vless(input_text)
            tag = data["tag"]
            configs[tag] = data
            listbox.insert(tk.END, tag)
            config_json = generate_config(data)
            with open(os.path.join(CONFIGS_DIR, f"{tag}.json"), "w", encoding="utf-8") as f:
                f.write(config_json)
            base64_urls.append(input_text)
            save_base64_urls()
            messagebox.showinfo("Добавлено", f"Добавлен конфиг с тегом: {tag}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось распарсить VLESS ссылку: {e}")
        return
    elif input_text.startswith("ss://"):
        clear_xray_configs()
        base64_urls = []
        try:
            data = parse_shadowsocks(input_text)
            tag = data["tag"]
            configs[tag] = data
            listbox.insert(tk.END, tag)
            config_json = generate_config(data)
            with open(os.path.join(CONFIGS_DIR, f"{tag}.json"), "w", encoding="utf-8") as f:
                f.write(config_json)
            base64_urls.append(input_text)
            save_base64_urls()
            messagebox.showinfo("Добавлено", f"Добавлен SS конфиг: {tag}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось распарсить SS ссылку: {e}")
        return


    if input_text.startswith("https"):
        try:
            headers = {'User-Agent': f'{APP_NAME}/{APP_VERS}'}
            r = requests.get(input_text, headers=headers)
            # r = requests.get(input_text)
            r.raise_for_status()
            clear_xray_configs()
            base64_urls = []
            try:
                # Попытка base64-декодирования как раньше
                decoded = base64.b64decode(r.text.strip()).decode("utf-8")
                lines = [l.strip() for l in decoded.splitlines() if l.startswith("vless://") or l.startswith("ss://")]
                if not lines:
                    raise ValueError("Нет vless или ss ссылок в base64 декодированном тексте")
                for line in lines:
                    try:
                        if line.startswith("vless://"):
                            data = parse_vless(line)
                        elif line.startswith("ss://"):
                            data = parse_shadowsocks(line)
                        else:
                            continue

                        tag = data["tag"]
                        if tag not in configs:
                            configs[tag] = data
                            listbox.insert(tk.END, tag)
                            config_json = generate_config(data)
                            with open(os.path.join(CONFIGS_DIR, f"{tag}.json"), "w", encoding="utf-8") as f:
                                f.write(config_json)
                    except Exception as e:
                        print(f"[!] Ошибка в строке: {line}\n{e}")

            except Exception:
                # Если base64 не прокатил — пытаемся загрузить как чистый JSON (с очисткой html)
                clean_content = re.sub(r'<[^>]+>', '', r.text).strip()
                
                try:
                    loaded_data = json.loads(clean_content)
                    
                    # Приводим к списку, даже если прилетел один объект
                    if isinstance(loaded_data, list):
                        items = loaded_data
                    elif isinstance(loaded_data, dict):
                        items = [loaded_data]
                    else:
                        raise ValueError("Полученные данные не являются JSON объектом или списком")

                    added_count = 0
                    
                    for config_data in items:
                        # Пытаемся найти имя для конфига:
                        # 1. Сначала поле "remarks" (оно есть в вашем файле примера)
                        # 2. Если нет, поле "tag"
                        # 3. Если нет, генерируем случайное имя
                        tag = unquote(config_data.get("remarks", config_data.get("tag", f"import_json_{added_count}")))
                        tag = sanitize_filename(tag)  # Декодируем emoji и кириллицу

                        configs[tag] = config_data
                        listbox.insert(tk.END, tag)
                        
                        with open(os.path.join(CONFIGS_DIR, f"{tag}.json"), "w", encoding="utf-8") as cf:
                            json.dump(config_data, cf, indent=2, ensure_ascii=False)
                        
                        added_count += 1

                    if added_count > 0:
                        base64_urls.append(input_text)
                        save_base64_urls()
                        messagebox.showinfo("Добавлено", f"Добавлено конфигов из JSON: {added_count}")
                        return
                    else:
                         messagebox.showwarning("Внимание", "JSON был валидным, но пуст.")

                except Exception as e:
                    messagebox.showerror("Ошибка", f"Не удалось распарсить JSON конфиг: {e}")
                    return

            base64_urls.append(input_text)
            save_base64_urls()
            #messagebox.showinfo("Добавлено", f"Добавлено {len(lines)} конфигов.")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить/распарсить: {e}")
        return

    messagebox.showerror("Ошибка", "Введите корректную VLESS ссылку или URL на base64 с конфигами.")


# --- Запуск Xray ---
def run_selected():
    global xray_process

    if xray_process and xray_process.poll() is None:
        stop_xray()
        save_state()
        btn_run.config(text="Запустить конфиг", bg="SystemButtonFace")
        return

    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("Выбор", "Выберите конфиг из списка.")
        return

    tag = listbox.get(selected[0])
    config_path = os.path.join(CONFIGS_DIR, f"{tag}.json")
    if not os.path.exists(XRAY_EXE):
        messagebox.showerror("Ошибка", "Файл xray.exe не найден.")
        return

    try:
        xray_process = subprocess.Popen([XRAY_EXE, "-config", config_path], creationflags=CREATE_NO_WINDOW)
        highlight_active(tag)
        save_state()
        btn_run.config(text="Остановить конфиг", bg="lightgreen")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось запустить Xray: {e}")


# --- кнопка стоп
def stop_xray():
    global xray_process

    if xray_process and xray_process.poll() is None:
        try:
            xray_process.terminate()
            xray_process.wait()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось остановить Xray: {e}")

    xray_process = None
    clear_highlight()  # <--- убираем подсветку активного конфига
    btn_run.config(text="Запустить конфиг", bg="SystemButtonFace")


def stop_system_proxy():
    """Отключение системного прокси (использует явную функцию)"""
    disable_system_proxy()

# --- Явные функции управления Xray ---
def restart_xray_with_tag(tag):
    """Перезапуск Xray с указанным тегом"""
    global xray_process
    if not tag:
        print("Тег не указан для перезапуска.")
        return

    config_path = os.path.join(CONFIGS_DIR, f"{tag}.json")
    if not os.path.exists(config_path):
        print(f"Конфиг не найден: {config_path}")
        return

    try:
        xray_process = subprocess.Popen([XRAY_EXE, "-config", config_path], creationflags=CREATE_NO_WINDOW)
        highlight_active(tag)
        btn_run.config(text="Остановить конфиг", bg="lightgreen")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось перезапустить Xray: {e}")

# --- Функция подсветки активного тега: ---
def highlight_active(tag):
    global active_tag

    # Сброс цвета у старого
    if active_tag is not None:
        try:
            idx = listbox.get(0, tk.END).index(active_tag)
            listbox.itemconfig(idx, {'bg': 'white', 'fg': 'black'})
        except ValueError:
            pass

    # Новый активный
    try:
        idx = listbox.get(0, tk.END).index(tag)
        listbox.itemconfig(idx, {'bg': 'lightgreen', 'fg': 'black'})
        active_tag = tag
        save_state()
    except ValueError:
        active_tag = None

def clear_highlight():
    global active_tag
    if active_tag is not None:
        try:
            idx = listbox.get(0, tk.END).index(active_tag)
            listbox.itemconfig(idx, {'bg': 'white', 'fg': 'black'})
        except ValueError:
            pass
        active_tag = None

#подсказка при наведении
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tipwindow or not self.text:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 10
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)  # Без рамок окна
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, background="#ffffe0", relief="solid", borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=4, ipady=2)

    def hide_tip(self, event=None):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None


def get_executable_path():
    return sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__)

def is_in_startup(app_name=APP_NAME):
    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0, winreg.KEY_READ
        ) as key:
            value, _ = winreg.QueryValueEx(key, app_name)

        exe_path = get_executable_path().lower()
        return exe_path in value.lower()

    except FileNotFoundError:
        return False


def add_to_startup(app_name=APP_NAME, path=None):
    if path is None:
        path = get_executable_path()
    path = f'"{path}" --autostart'

    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        0, winreg.KEY_SET_VALUE
    )
    winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, path)
    winreg.CloseKey(key)

def remove_from_startup(app_name=APP_NAME):
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0, winreg.KEY_SET_VALUE
        )
        winreg.DeleteValue(key, app_name)
        winreg.CloseKey(key)
    except FileNotFoundError:
        pass

# ---- Tkinter UI ----
def toggle_startup():
    if startup_var.get():
        add_to_startup()
    else:
        remove_from_startup()

def restart_xray_with_active():
    """Перезапуск Xray с активным тегом (использует явную функцию)"""
    restart_xray_with_tag(active_tag)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    script = get_executable_path()
    params = ""  # можно передать аргументы, если нужно
    try:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", script, params, None, 1
        )
        save_state()
        stop_xray()
        stop_system_proxy()
        sys.exit()  # завершить текущий процесс
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось получить права администратора: {e}")

 
def vrv_tun_mode_toggle():
    global tun_enabled, active_tag

    if not is_admin():
        # answer = messagebox.askyesno("Требуются права", "Нужно запустить с правами администратора. Перезапустить?")
        # if answer:
            run_as_admin()
        # return

    if not tun_enabled:
        # ВКЛ
        interface = get_default_interface()
        patch_direct_out_interface(CONFIGS_DIR, interface)

        saved_tag = active_tag
        stop_xray()
        if saved_tag:
            active_tag = saved_tag
            restart_xray_with_active()
           
        start_tun2proxy(resource_path("tun2proxy/tun2proxy-bin.exe"))
        btn_tun.config(text="Выключить TUN", bg="#ffcccc")
        tun_enabled = True
    else:
        # ВЫКЛ
        stop_tun2proxy()
        btn_tun.config(text="Включить TUN", bg="SystemButtonFace")
        tun_enabled = False


# --- Интерфейс ---
root = tk.Tk()

# Применяем современную тему
from ui_enhancement import ModernUI, apply_modern_theme
from fast_tooltips import FastToolTip, create_fast_tooltip
from ui_themes import ThemeManager, AnimationManager

# Инициализируем менеджер тем
theme_manager = ThemeManager()
apply_modern_theme(root)

icon_path = resource_path("img/logo.png")
icon = PhotoImage(file=icon_path)
root.iconphoto(True, icon)

icon_path = resource_path("img/icon.ico")
root.iconbitmap(icon_path)

root.minsize(480, 350)

def keypress(e):
    if e.keycode == 86:
        cmd_paste(root, stop_xray, add_from_url)
    elif e.keycode == 67:
        cmd_copy(root)
    elif e.keycode == 88:
        cmd_cut(root)
    elif e.keycode == 65:
        cmd_select_all(root)
root.bind("<Control-KeyPress>", keypress)

def select_config(listbox):
    selected = listbox.curselection()
    if not selected:
        return
    tag = listbox.get(selected[0])
    highlight_active(tag)

# Функция on_enter_key будет определена после создания всех виджетов

root.title(APP_NAME+" "+APP_VERS+" "+XRAY_VERS)

# Создаем главный контейнер с отступами
main_container = ModernUI.create_modern_frame(root, padding=20)

# Заголовок приложения
header_frame = ModernUI.create_modern_frame(main_container, padding=5)
title_label = ModernUI.create_modern_label(
    header_frame, 
    f"{APP_NAME} v{APP_VERS}", 
    variant='primary', 
    size='large'
)
title_label.pack()

subtitle_label = ModernUI.create_modern_label(
    header_frame, 
    f"XRAY Core v{XRAY_VERS}", 
    variant='secondary', 
    size='small'
)
subtitle_label.pack()

# Поле ввода URL
input_frame = ModernUI.create_modern_frame(main_container, padding=15)
input_label = ModernUI.create_modern_label(
    input_frame, 
    "Подписка или конфигурация", 
    variant='primary', 
    size='small'
)
input_label.pack(anchor='w')

input_container, entry = ModernUI.create_modern_entry(input_frame, "Вставьте URL подписки или конфигурации XRAY", 40)
input_container.pack(fill='x', pady=(5, 10))

# Панель кнопок ввода
button_frame = ModernUI.create_modern_frame(input_frame, padding=0, bg=ModernUI.COLORS['surface'])
button_frame.pack(fill='x')

# Кнопка загрузки
img = Image.open(resource_path("img/ico.png"))
img = img.resize((20, 20), Image.Resampling.LANCZOS)
icon1 = ImageTk.PhotoImage(img)

def modern_add_from_url():
    add_from_url()

def modern_add_from_clipboard():
    add_from_clipboard_and_parse()

btn_load = ModernUI.create_modern_button(
    button_frame, 
    "Загрузить", 
    modern_add_from_url,
    variant='primary',
    size='small'
)
btn_load.pack(side='left', padx=(0, 5))

# Кнопка вставки из буфера
img2 = Image.open(resource_path("img/ref.png"))
img2 = img2.resize((20, 20), Image.Resampling.LANCZOS)
icon2 = ImageTk.PhotoImage(img2)

btn_paste = ModernUI.create_modern_button(
    button_frame, 
    "Вставить", 
    modern_add_from_clipboard,
    variant='secondary',
    size='small'
)
btn_paste.pack(side='left')

# Быстрые подсказки для кнопок загрузки
FastToolTip(btn_load, "Загрузить конфигурацию из URL", delay_show=100, delay_hide=30)
FastToolTip(btn_paste, "Вставить из буфера обмена", delay_show=100, delay_hide=30)

# вставка из буфера обмена
def add_from_clipboard_and_parse():
    try:
        clipboard_text = root.clipboard_get().strip()
        entry.delete(0, tk.END)
        entry.insert(0, clipboard_text)
        add_from_url()
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось получить данные из буфера обмена: {e}")

# Список конфигураций
listbox_frame = ModernUI.create_modern_frame(main_container, padding=15)
listbox_label = ModernUI.create_modern_label(
    listbox_frame, 
    "Конфигурации", 
    variant='primary', 
    size='small'
)
listbox_label.pack(anchor='w')

listbox_container, listbox = ModernUI.create_modern_listbox(listbox_frame, height=6)
listbox_container.pack(fill='both', expand=True, pady=(5, 10))

# Связываем события для списка
listbox.bind('<<ListboxSelect>>', lambda e: select_config(listbox))



# Основные кнопки управления
control_frame = ModernUI.create_modern_frame(main_container, padding=15)

# Кнопка запуска конфигурации
btn_run = ModernUI.create_modern_button(
    control_frame, 
    "Запустить конфиг", 
    run_selected,
    variant='primary',
    size='medium'
)
btn_run.pack(side='left', padx=(0, 10))

# Кнопка системного прокси
btn_proxy = ModernUI.create_modern_button(
    control_frame, 
    "Системный прокси", 
    toggle_system_proxy,
    variant='secondary',
    size='medium'
)
btn_proxy.pack(side='left')

# Быстрые подсказки для основных кнопок
FastToolTip(btn_run, "Запустить XRAY SOCKS5 на порту 2080", delay_show=100, delay_hide=30)
FastToolTip(btn_proxy, "Настроить системный прокси Windows\n(работает только для браузеров)", delay_show=100, delay_hide=30)


# Дополнительные настройки
settings_frame = ModernUI.create_modern_frame(main_container, padding=15)
        
# Автозапуск
startup_var = tk.BooleanVar(value=is_in_startup())
startup_check = ModernUI.create_modern_checkbutton(
    settings_frame, 
    "Автозапуск с Windows", 
    startup_var, 
    toggle_startup
)
startup_check.pack(side='left')

# TUN режим
btn_tun = ModernUI.create_modern_button(
    settings_frame, 
    "Включить TUN", 
    vrv_tun_mode_toggle,
    variant='warning',
    size='medium'
)
btn_tun.pack(side='right')

# Быстрая подсказка для TUN режима
FastToolTip(btn_tun, "Включить TUN режим\n(требует права администратора)\nСоздает виртуальную сетевую карту", delay_show=100, delay_hide=30)


# Нижняя панель со ссылками и переключателем темы
footer_frame = ModernUI.create_modern_frame(root, padding=10, bg=ModernUI.COLORS['surface'])
footer_frame.pack(fill='x', side='bottom')

# Левая часть - ссылки
links_frame = tk.Frame(footer_frame, bg=ModernUI.COLORS['surface'])
links_frame.pack(side='left')

# Создаем современные ссылки
def create_modern_link(parent, text, command, color=ModernUI.COLORS['primary']):
    link = tk.Label(
        parent,
        text=text,
        fg=color,
        bg=ModernUI.COLORS['surface'],
        font=('Segoe UI', 9, 'underline'),
        cursor='hand2'
    )
    link.bind('<Button-1>', lambda e: command())
    
    # Hover эффекты
    def on_enter(e):
        link.config(fg=ModernUI.COLORS['primary_hover'])
    def on_leave(e):
        link.config(fg=color)
        
    link.bind('<Enter>', on_enter)
    link.bind('<Leave>', on_leave)
    
    return link

# Ссылки
link_telegram = create_modern_link(links_frame, "Telegram бот", open_link)
link_telegram.pack(side='left', padx=(0, 15))

link_github = create_modern_link(links_frame, "GitHub", github)
link_github.pack(side='left')

# Правая часть - переключатель темы
theme_frame = tk.Frame(footer_frame, bg=ModernUI.COLORS['surface'])
theme_frame.pack(side='right')

# Кнопка переключения темы
def create_theme_toggle():
    """Создает кнопку переключения темы"""
    current_theme = theme_manager.current_theme
    
    # Символы для разных тем
    sun_icon = "☀️"  # Для переключения на светлую
    moon_icon = "🌙"  # Для переключения на темную
    
    icon_text = moon_icon if current_theme == 'light' else sun_icon
    tooltip_text = "Переключить на светлую тему" if current_theme == 'dark' else "Переключить на темную тему"
    
    btn = tk.Button(
        theme_frame,
        text=icon_text,
        command=toggle_theme,
        bg=ModernUI.COLORS['surface'],
        fg=ModernUI.COLORS['text_primary'],
        font=('Segoe UI', 12),
        relief='flat',
        borderwidth=0,
        cursor='hand2',
        width=3,
        height=1
    )
    
    # Hover эффекты
    def on_enter(e):
        btn.config(bg=ModernUI.COLORS['border'])
    def on_leave(e):
        btn.config(bg=ModernUI.COLORS['surface'])
        
    btn.bind('<Enter>', on_enter)
    btn.bind('<Leave>', on_leave)
    
    # Быстрая подсказка
    FastToolTip(btn, tooltip_text, delay_show=150, delay_hide=50)
    
    return btn

def toggle_theme():
    """Переключает тему интерфейса"""
    new_theme = theme_manager.toggle_theme()
    
    # Анимация перехода
    AnimationManager.fade_out(root, duration=200)
    root.after(200, lambda: apply_theme(new_theme))

def apply_theme(theme_name):
    """Применяет тему ко всему интерфейсу"""
    theme = theme_manager.get_current_theme()
    
    # Обновляем цвета всех элементов
    root.configure(bg=theme['background'])
    
    # Обновляем все фреймы и элементы
    update_widget_colors(root, theme)
    
    # Обновляем кнопку темы
    refresh_theme_button()
    
    # Показываем интерфейс с анимацией
    AnimationManager.fade_in(root, duration=200)

def update_widget_colors(widget, theme):
    """Рекурсивно обновляет цвета всех виджетов"""
    try:
        # Обновляем текущий виджет
        widget_class = widget.winfo_class()
        
        if widget_class in ['Frame', 'TFrame']:
            widget.configure(bg=theme['background'])
        elif widget_class in ['Label', 'TLabel']:
            if 'fg' in widget.keys():
                current_fg = widget.cget('fg')
                if current_fg in ['#0f172a', '#000000', 'black']:
                    widget.configure(fg=theme['text_primary'], bg=theme['background'])
                elif current_fg in ['#64748b', '#808080', 'gray', 'grey']:
                    widget.configure(fg=theme['text_secondary'], bg=theme['background'])
        elif widget_class in ['Button', 'TButton']:
            if 'bg' in widget.keys():
                current_bg = widget.cget('bg')
                # Не трогаем цветные кнопки
                if current_bg not in ['#2563eb', '#16a34a', '#d97706', '#dc2626', '#64748b']:
                    widget.configure(bg=theme['surface'], fg=theme['text_primary'])
        
        # Обновляем дочерние виджеты
        for child in widget.winfo_children():
            update_widget_colors(child, theme)
    except:
        pass

def refresh_theme_button():
    """Обновляет кнопку переключения темы"""
    for child in theme_frame.winfo_children():
        child.destroy()
    
    theme_btn = create_theme_toggle()
    theme_btn.pack()

# Создаем кнопку переключения темы
theme_btn = create_theme_toggle()
theme_btn.pack()

# Место для ссылки обновления будет добавлено динамически


load_base64_urls()
load_state()

# если запущено из автозапуска — стартуем свернутыми
if IS_AUTOSTART:
    root.iconify()

# Определяем функцию обработки нажатия Enter после создания всех виджетов
def on_enter_key(event):
    global xray_process
    if entry == root.focus_get():
        add_from_url()
    else:
        # Устанавливаем активный элемент как выбранный, если нет выделения
        if not listbox.curselection():
            active = listbox.index(tk.ACTIVE)
            if active >= 0:
                listbox.selection_clear(0, tk.END)
                listbox.selection_set(active)
        # Исправлено: убран двойной вызов run_selected()
        run_selected()

# Привязываем обработчик клавиш
root.bind('<Return>', on_enter_key)

root.after(3000, check_latest_version)  # Проверка через 2 секунды после запуска

def on_closing():
    save_state()
    stop_xray()
    stop_system_proxy()  # Выключим прокси
    stop_tun2proxy()   # Выключим tun режим
    root.destroy()  # Закроем окно

root.protocol("WM_DELETE_WINDOW", on_closing)


root.mainloop()