"""
Стили и темы для современного интерфейса winLoadXRAY
"""

import tkinter as tk
from tkinter import ttk
import json
import os

class ThemeManager:
    """Менеджер тем для приложения"""
    
    # Темная тема
    DARK_THEME = {
        'primary': '#3b82f6',
        'primary_hover': '#60a5fa',
        'secondary': '#64748b',
        'success': '#22c55e',
        'warning': '#f59e0b',
        'danger': '#ef4444',
        'background': '#0f172a',
        'surface': '#1e293b',
        'surface_light': '#334155',
        'text_primary': '#f8fafc',
        'text_secondary': '#94a3b8',
        'border': '#334155',
        'accent': '#3b82f6'
    }
    
    # Светлая тема (по умолчанию)
    LIGHT_THEME = {
        'primary': '#2563eb',
        'primary_hover': '#3b82f6',
        'secondary': '#64748b',
        'success': '#16a34a',
        'warning': '#d97706',
        'danger': '#dc2626',
        'background': '#f8fafc',
        'surface': '#ffffff',
        'surface_light': '#f1f5f9',
        'text_primary': '#0f172a',
        'text_secondary': '#64748b',
        'border': '#e2e8f0',
        'accent': '#2563eb'
    }
    
    def __init__(self):
        self.current_theme = 'light'
        self.themes = {
            'light': self.LIGHT_THEME,
            'dark': self.DARK_THEME
        }
        self.settings_file = os.path.join(os.environ.get('APPDATA', ''), 'winLoadXRAY', 'ui_settings.json')
        self.load_settings()
    
    def load_settings(self):
        """Загружает настройки UI"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    self.current_theme = settings.get('theme', 'light')
        except:
            pass
    
    def save_settings(self):
        """Сохраняет настройки UI"""
        try:
            settings_dir = os.path.dirname(self.settings_file)
            os.makedirs(settings_dir, exist_ok=True)
            
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump({'theme': self.current_theme}, f, indent=2)
        except:
            pass
    
    def get_current_theme(self):
        """Получает текущую тему"""
        return self.themes[self.current_theme]
    
    def toggle_theme(self):
        """Переключает тему"""
        self.current_theme = 'dark' if self.current_theme == 'light' else 'light'
        self.save_settings()
        return self.current_theme
    
    def create_theme_toggle_button(self, parent, command=None):
        """Создает кнопку переключения темы"""
        theme = self.get_current_theme()
        
        # Создаем frame для кнопки
        frame = tk.Frame(parent, bg=theme['surface'])
        
        # Иконка темы (можно заменить на emoji или символы)
        icon_text = "🌙" if self.current_theme == 'light' else "☀️"
        
        button = tk.Button(
            frame,
            text=icon_text,
            command=lambda: [self.toggle_theme(), command() if command else None],
            bg=theme['surface'],
            fg=theme['text_primary'],
            font=('Segoe UI', 10),
            relief='flat',
            borderwidth=0,
            cursor='hand2',
            width=3,
            height=1
        )
        
        # Hover эффекты
        def on_enter(e):
            button.config(bg=theme['border'])
            
        def on_leave(e):
            button.config(bg=theme['surface'])
            
        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)
        
        button.pack()
        return frame

class AnimationManager:
    """Менеджер анимаций для плавных переходов"""
    
    @staticmethod
    def fade_in(widget, duration=300, steps=15):
        """Плавное появление виджета"""
        try:
            widget.attributes('-alpha', 0.0)
            widget.deiconify()
            
            step_duration = max(duration // steps, 10)
            
            def animate_fade_in(step):
                if step <= steps:
                    alpha = step / steps
                    try:
                        widget.attributes('-alpha', alpha)
                    except:
                        pass
                    widget.after(step_duration, lambda: animate_fade_in(step + 1))
            
            animate_fade_in(0)
        except:
            widget.deiconify()
    
    @staticmethod
    def fade_out(widget, duration=200, steps=10, callback=None):
        """Плавное исчезновение виджета"""
        try:
            step_duration = max(duration // steps, 10)
            
            def animate_fade_out(step):
                if step <= steps:
                    alpha = 1.0 - (step / steps)
                    try:
                        widget.attributes('-alpha', alpha)
                    except:
                        pass
                    widget.after(step_duration, lambda: animate_fade_out(step + 1))
                elif callback:
                    callback()
            
            animate_fade_out(0)
        except:
            if callback:
                callback()
    
    @staticmethod
    def slide_in(widget, direction='left', duration=200):
        """Скользящее появление виджета"""
        try:
            widget.update_idletasks()
            width = widget.winfo_width()
            height = widget.winfo_height()
            
            # Начальная позиция
            if direction == 'left':
                start_x = -width
                end_x = 0
            elif direction == 'right':
                start_x = width
                end_x = 0
            elif direction == 'top':
                start_y = -height
                end_y = 0
            else:  # bottom
                start_y = height
                end_y = 0
            
            widget.place(x=start_x, y=start_y)
            
            # Анимация
            steps = 10
            step_duration = max(duration // steps, 10)
            
            for i in range(steps + 1):
                progress = i / steps
                if direction in ['left', 'right']:
                    x = start_x + (end_x - start_x) * progress
                    widget.after(i * step_duration, lambda x=x: widget.place_configure(x=x))
                else:
                    y = start_y + (end_y - start_y) * progress
                    widget.after(i * step_duration, lambda y=y: widget.place_configure(y=y))
        except:
            pass

class ModernScrollbar:
    """Современная полоса прокрутки"""
    
    def __init__(self, parent, orient='vertical', **kwargs):
        self.parent = parent
        self.orient = orient
        self.theme_manager = ThemeManager()
        
        # Создаем современную полосу прокрутки
        self.scrollbar = ttk.Scrollbar(parent, orient=orient, **kwargs)
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Настраиваем стиль
        self.setup_style()
    
    def setup_style(self):
        """Настраивает стиль полосы прокрутки"""
        theme = self.theme_manager.get_current_theme()
        
        # Стиль для полосы прокрутки
        self.style.configure(
            'Modern.Vertical.TScrollbar',
            background=theme['surface'],
            troughcolor=theme['border'],
            bordercolor=theme['border'],
            arrowcolor=theme['text_primary'],
            lightcolor=theme['surface'],
            darkcolor=theme['surface']
        )
        
        self.style.configure(
            'Modern.Horizontal.TScrollbar',
            background=theme['surface'],
            troughcolor=theme['border'],
            bordercolor=theme['border'],
            arrowcolor=theme['text_primary'],
            lightcolor=theme['surface'],
            darkcolor=theme['surface']
        )
        
        style_name = f'Modern.{self.orient.capitalize()}.TScrollbar'
        self.scrollbar.configure(style=style_name)
    
    def pack(self, **kwargs):
        """Упаковывает полосу прокрутки"""
        self.scrollbar.pack(**kwargs)
    
    def configure(self, **kwargs):
        """Настраивает полосу прокрутки"""
        self.scrollbar.configure(**kwargs)
    
    def __getattr__(self, name):
        """Прокси для методов ttk.Scrollbar"""
        return getattr(self.scrollbar, name)

class StatusBar:
    """Современная строка состояния"""
    
    def __init__(self, parent):
        self.parent = parent
        self.theme_manager = ThemeManager()
        self.setup_ui()
    
    def setup_ui(self):
        """Настраивает интерфейс строки состояния"""
        theme = self.theme_manager.get_current_theme()
        
        self.frame = tk.Frame(parent, bg=theme['surface'], height=25)
        self.frame.pack(fill='x', side='bottom')
        self.frame.pack_propagate(False)
        
        self.label = tk.Label(
            self.frame,
            text="Готово",
            bg=theme['surface'],
            fg=theme['text_secondary'],
            font=('Segoe UI', 8),
            anchor='w'
        )
        self.label.pack(side='left', padx=10, pady=2)
    
    def set_status(self, text, status_type='info'):
        """Устанавливает статус"""
        theme = self.theme_manager.get_current_theme()
        
        color_map = {
            'info': theme['text_secondary'],
            'success': theme['success'],
            'warning': theme['warning'],
            'error': theme['danger']
        }
        
        self.label.config(text=text, fg=color_map.get(status_type, theme['text_secondary']))

# Пример использования
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Демо современного UI")
    root.geometry("600x400")
    
    theme_manager = ThemeManager()
    
    # Создаем демо интерфейс
    main_frame = tk.Frame(root, bg=theme_manager.get_current_theme()['background'])
    main_frame.pack(fill='both', expand=True)
    
    # Заголовок
    title = tk.Label(
        main_frame,
        text="Демо современного интерфейса",
        bg=theme_manager.get_current_theme()['background'],
        fg=theme_manager.get_current_theme()['text_primary'],
        font=('Segoe UI', 16, 'bold')
    )
    title.pack(pady=20)
    
    # Кнопка переключения темы
    theme_toggle = theme_manager.create_theme_toggle_button(main_frame, lambda: print("Theme toggled"))
    theme_toggle.pack(pady=10)
    
    # Кнопка
    from ui_enhancement import ModernUI
    
    demo_button = ModernUI.create_modern_button(
        main_frame,
        "Демо кнопка",
        lambda: print("Button clicked"),
        variant='primary'
    )
    demo_button.pack(pady=10)
    
    root.mainloop()