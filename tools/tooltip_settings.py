"""
Настройки быстрых всплывающих подсказок для winLoadXRAY
"""

import tkinter as tk
from tkinter import ttk
import json
import os

class TooltipSettings:
    """Менеджер настроек подсказок"""
    
    SETTINGS_FILE = os.path.join(os.environ.get('APPDATA', ''), 'winLoadXRAY', 'tooltip_settings.json')
    
    # Предустановленные профили
    PROFILES = {
        'ultra_fast': {
            'name': 'Ультра быстрые',
            'show_delay': 50,
            'hide_delay': 20,
            'description': 'Мгновенная реакция на наведение'
        },
        'very_fast': {
            'name': 'Очень быстрые',
            'show_delay': 100,
            'hide_delay': 30,
            'description': 'Быстрое появление и исчезновение (рекомендуется)'
        },
        'fast': {
            'name': 'Быстрые',
            'show_delay': 150,
            'hide_delay': 50,
            'description': 'Сбалансированная скорость'
        },
        'normal': {
            'name': 'Обычные',
            'show_delay': 200,
            'hide_delay': 100,
            'description': 'Стандартная скорость'
        },
        'slow': {
            'name': 'Медленные',
            'show_delay': 400,
            'hide_delay': 200,
            'description': 'Более медленные для спокойного использования'
        },
        'instant': {
            'name': 'Мгновенные',
            'show_delay': 0,
            'hide_delay': 0,
            'description': 'Появляются и исчезают мгновенно'
        }
    }
    
    def __init__(self):
        self.current_profile = 'very_fast'
        self.custom_settings = None
        self.load_settings()
    
    def load_settings(self):
        """Загружает настройки подсказок"""
        try:
            if os.path.exists(self.SETTINGS_FILE):
                with open(self.SETTINGS_FILE, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    self.current_profile = settings.get('profile', 'very_fast')
                    self.custom_settings = settings.get('custom', None)
        except Exception as e:
            print(f"Ошибка загрузки настроек подсказок: {e}")
            self.current_profile = 'very_fast'
    
    def save_settings(self, profile=None, custom=None):
        """Сохраняет настройки подсказок"""
        try:
            settings_dir = os.path.dirname(self.SETTINGS_FILE)
            os.makedirs(settings_dir, exist_ok=True)
            
            settings = {
                'profile': profile or self.current_profile,
                'custom': custom or self.custom_settings
            }
            
            with open(self.SETTINGS_FILE, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
                
            if profile:
                self.current_profile = profile
            if custom:
                self.custom_settings = custom
                
        except Exception as e:
            print(f"Ошибка сохранения настроек подсказок: {e}")
    
    def get_current_settings(self):
        """Получает текущие настройки"""
        if self.custom_settings:
            return self.custom_settings
        
        profile = self.PROFILES.get(self.current_profile, self.PROFILES['very_fast'])
        return {
            'show_delay': profile['show_delay'],
            'hide_delay': profile['hide_delay']
        }
    
    def create_settings_window(self, parent=None):
        """Создает окно настроек подсказок"""
        if parent is None:
            root = tk.Tk()
            root.title("Настройки подсказок - winLoadXRAY")
            root.geometry("500x400")
            root.resizable(False, False)
            parent = root
        
        # Стили
        colors = {
            'bg': '#f8fafc',
            'fg': '#0f172a',
            'primary': '#2563eb',
            'secondary': '#64748b',
            'border': '#e2e8f0'
        }
        
        # Главный фрейм
        main_frame = tk.Frame(parent, bg=colors['bg'], padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Заголовок
        title = tk.Label(
            main_frame,
            text="⚙️ Настройки всплывающих подсказок",
            bg=colors['bg'],
            fg=colors['fg'],
            font=('Segoe UI', 16, 'bold')
        )
        title.pack(pady=(0, 20))
        
        # Список профилей
        profiles_frame = tk.LabelFrame(
            main_frame,
            text="Выберите профиль скорости:",
            bg=colors['bg'],
            fg=colors['fg'],
            font=('Segoe UI', 11, 'bold'),
            padx=10,
            pady=10
        )
        profiles_frame.pack(fill='x', pady=(0, 15))
        
        # Переменная для выбранного профиля
        selected_profile = tk.StringVar(value=self.current_profile)
        
        for profile_key, profile_info in self.PROFILES.items():
            # Radio button для профиля
            rb = tk.Radiobutton(
                profiles_frame,
                text=f"{profile_info['name']} - {profile_info['description']}",
                variable=selected_profile,
                value=profile_key,
                bg=colors['bg'],
                fg=colors['fg'],
                font=('Segoe UI', 10),
                selectcolor=colors['border'],
                activebackground=colors['bg']
            )
            rb.pack(anchor='w', pady=2)
            
            # Текущие значения для профиля
            values_label = tk.Label(
                profiles_frame,
                text=f"  Показ: {profile_info['show_delay']}мс, Скрытие: {profile_info['hide_delay']}мс",
                bg=colors['bg'],
                fg=colors['secondary'],
                font=('Segoe UI', 8)
            )
            values_label.pack(anchor='w', padx=(20, 0), pady=(0, 5))
        
        # Кнопки
        buttons_frame = tk.Frame(main_frame, bg=colors['bg'])
        buttons_frame.pack(fill='x', pady=(15, 0))
        
        # Кнопка применения
        def apply_settings():
            profile = selected_profile.get()
            self.save_settings(profile=profile)
            
            # Показываем уведомление
            status_label.config(
                text=f"✅ Применен профиль: {self.PROFILES[profile]['name']}",
                fg=colors['primary']
            )
        
        apply_btn = tk.Button(
            buttons_frame,
            text="Применить",
            command=apply_settings,
            bg=colors['primary'],
            fg='white',
            font=('Segoe UI', 10, 'bold'),
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2'
        )
        apply_btn.pack(side='left', padx=(0, 10))
        
        # Кнопка закрытия
        close_btn = tk.Button(
            buttons_frame,
            text="Закрыть",
            command=parent.destroy,
            bg=colors['secondary'],
            fg='white',
            font=('Segoe UI', 10),
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2'
        )
        close_btn.pack(side='right')
        
        # Статус
        status_label = tk.Label(
            main_frame,
            text=f"Текущий профиль: {self.PROFILES[self.current_profile]['name']}",
            bg=colors['bg'],
            fg=colors['fg'],
            font=('Segoe UI', 9)
        )
        status_label.pack(pady=(15, 0))
        
        return parent

# Глобальный экземпляр настроек
tooltip_settings = TooltipSettings()

def get_tooltip_settings():
    """Получает текущие настройки подсказок"""
    return tooltip_settings.get_current_settings()

def create_tooltip_settings_window():
    """Создает окно настроек подсказок"""
    return tooltip_settings.create_settings_window()

# Демонстрация
if __name__ == "__main__":
    settings_window = create_tooltip_settings_window()
    settings_window.mainloop()