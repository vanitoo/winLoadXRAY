"""
Модуль для улучшения интерфейса winLoadXRAY
Современный минималистичный дизайн с улучшенной типографией и цветовой схемой
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import math

class ModernUI:
    """Класс для создания современного UI"""
    
    # Современная цветовая схема
    COLORS = {
        'primary': '#2563eb',      # Синий
        'primary_hover': '#1d4ed8', # Темнее синий
        'secondary': '#64748b',    # Серый
        'success': '#16a34a',      # Зеленый
        'warning': '#d97706',      # Оранжевый
        'danger': '#dc2626',       # Красный
        'background': '#f8fafc',    # Светлый фон
        'surface': '#ffffff',      # Белый поверхность
        'text_primary': '#0f172a', # Основной текст
        'text_secondary': '#64748b', # Вторичный текст
        'border': '#e2e8f0',       # Границы
        'shadow': 'rgba(0,0,0,0.1)' # Тень
    }
    
    @staticmethod
    def create_modern_button(parent, text, command=None, variant='primary', size='medium'):
        """Создает современную кнопку"""
        colors = ModernUI.COLORS
        
        # Выбор цветов в зависимости от варианта
        color_map = {
            'primary': (colors['primary'], colors['primary_hover']),
            'secondary': (colors['secondary'], colors['secondary']),
            'success': (colors['success'], colors['success']),
            'warning': (colors['warning'], colors['warning']),
            'danger': (colors['danger'], colors['danger'])
        }
        
        bg_color, hover_color = color_map.get(variant, color_map['primary'])
        
        # Размеры кнопки
        size_map = {
            'small': {'font': ('Segoe UI', 9), 'padx': 12, 'pady': 6},
            'medium': {'font': ('Segoe UI', 10), 'padx': 16, 'pady': 8},
            'large': {'font': ('Segoe UI', 12), 'padx': 20, 'pady': 12}
        }
        
        style = size_map.get(size, size_map['medium'])
        
        # Создаем кнопку с современным стилем
        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg_color,
            fg='white',
            font=style['font'],
            relief='flat',
            borderwidth=0,
            cursor='hand2',
            padx=style['padx'],
            pady=style['pady']
        )
        
        # Эффекты hover
        def on_enter(e):
            button.config(bg=hover_color)
            
        def on_leave(e):
            button.config(bg=bg_color)
            
        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)
        
        return button
    
    @staticmethod
    def create_modern_entry(parent, placeholder="", width=30):
        """Создает современное поле ввода"""
        colors = ModernUI.COLORS
        
        frame = tk.Frame(parent, bg=colors['background'])
        
        entry = tk.Entry(
            frame,
            width=width,
            font=('Segoe UI', 11),
            bg=colors['surface'],
            fg=colors['text_primary'],
            relief='flat',
            borderwidth=1,
            highlightthickness=0
        )
        
        # Добавляем placeholder
        if placeholder:
            entry.insert(0, placeholder)
            entry.config(fg=colors['text_secondary'])
            
            def on_focus_in(event):
                if entry.get() == placeholder:
                    entry.delete(0, tk.END)
                    entry.config(fg=colors['text_primary'])
                    
            def on_focus_out(event):
                if not entry.get():
                    entry.insert(0, placeholder)
                    entry.config(fg=colors['text_secondary'])
                    
            entry.bind('<FocusIn>', on_focus_in)
            entry.bind('<FocusOut>', on_focus_out)
        
        # Стилизация при фокусе
        def on_focus_in_border(event):
            entry.config(highlightbackground=colors['primary'], highlightcolor=colors['primary'], highlightthickness=1)
            
        def on_focus_out_border(event):
            entry.config(highlightthickness=0)
            
        entry.bind('<FocusIn>', on_focus_in_border)
        entry.bind('<FocusOut>', on_focus_out_border)
        
        entry.pack(fill='x')
        return frame, entry
    
    # Алиас для совместимости
    create_modern_input = create_modern_entry
    
    @staticmethod
    def create_modern_listbox(parent, height=8):
        """Создает современный список"""
        colors = ModernUI.COLORS
        
        # Создаем frame с скругленными углами
        frame = tk.Frame(parent, bg=colors['surface'], relief='flat', bd=1)
        frame.pack_propagate(False)
        
        listbox = tk.Listbox(
            frame,
            height=height,
            font=('Segoe UI', 10),
            bg=colors['surface'],
            fg=colors['text_primary'],
            selectbackground=colors['primary'],
            selectforeground='white',
            relief='flat',
            borderwidth=0,
            highlightthickness=0,
            activestyle='none'
        )
        
        # Стилизация полосы прокрутки
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=listbox.yview)
        listbox.configure(yscrollcommand=scrollbar.set)
        
        listbox.pack(side='left', fill='both', expand=True, padx=1, pady=1)
        scrollbar.pack(side='right', fill='y')
        
        return frame, listbox
    
    @staticmethod
    def create_modern_frame(parent, padding=10, bg=None):
        """Создает современный frame"""
        colors = ModernUI.COLORS
        
        if bg is None:
            bg = colors['background']
            
        frame = tk.Frame(parent, bg=bg, relief='flat')
        frame.pack(fill='x', padx=padding, pady=padding//2)
        return frame
    
    @staticmethod
    def create_modern_label(parent, text, variant='primary', size='medium'):
        """Создает современную метку"""
        colors = ModernUI.COLORS
        
        # Размеры шрифта
        size_map = {
            'small': ('Segoe UI', 9, 'normal'),
            'medium': ('Segoe UI', 10, 'normal'),
            'large': ('Segoe UI', 12, 'bold')
        }
        
        font = size_map.get(size, size_map['medium'])
        
        # Цвета
        color_map = {
            'primary': colors['text_primary'],
            'secondary': colors['text_secondary'],
            'success': colors['success'],
            'warning': colors['warning'],
            'danger': colors['danger']
        }
        
        fg = color_map.get(variant, color_map['primary'])
        
        label = tk.Label(
            parent,
            text=text,
            font=font,
            fg=fg,
            bg=colors['background']
        )
        
        return label
    
    @staticmethod
    def create_modern_checkbutton(parent, text, variable, command=None):
        """Создает современный чекбокс"""
        colors = ModernUI.COLORS
        
        checkbutton = tk.Checkbutton(
            parent,
            text=text,
            variable=variable,
            command=command,
            font=('Segoe UI', 10),
            fg=colors['text_primary'],
            bg=colors['background'],
            activebackground=colors['background'],
            activeforeground=colors['primary'],
            selectcolor=colors['surface'],
            relief='flat',
            borderwidth=0
        )
        
        return checkbutton

class ToolTip:
    """Современные подсказки с быстрым появлением и исчезновением"""
    
    def __init__(self, widget, text, delay_show=200, delay_hide=100):
        self.widget = widget
        self.text = text
        self.delay_show = delay_show  # Задержка появления (мс)
        self.delay_hide = delay_hide  # Задержка исчезновения (мс)
        self.tip = None
        self.show_timer = None
        self.hide_timer = None
        
    def show_tip(self):
        """Быстро показывает подсказку"""
        if self.tip or not self.text:
            return
            
        # Отменяем таймер скрытия если есть
        if self.hide_timer:
            self.widget.after_cancel(self.hide_timer)
            self.hide_timer = None
            
        x, y, cx, cy = self.widget.bbox("insert") if hasattr(self.widget, 'bbox') else (0, 0, 0, 0)
        x = self.widget.winfo_rootx() + cx + 20
        y = self.widget.winfo_rooty() + cy + 20
        
        self.tip = tk.Toplevel(self.widget)
        self.tip.wm_overrideredirect(True)
        self.tip.wm_geometry(f"+{x}+{y}")
        
        # Современный стиль подсказки
        colors = ModernUI.COLORS
        
        label = tk.Label(
            self.tip,
            text=self.text,
            justify='left',
            background=colors['surface'],
            foreground=colors['text_primary'],
            relief='solid',
            borderwidth=1,
            bordercolor=colors['border'],
            font=('Segoe UI', 9),
            wraplength=300,
            padx=8,
            pady=6
        )
        label.pack()
        
        # Плавное появление
        self.tip.attributes('-alpha', 0.0)
        self.tip.deiconify()
        
        # Анимация появления
        for i in range(11):
            alpha = i / 10.0
            self.widget.after(i * 15, lambda a=alpha: self.tip.attributes('-alpha', a))
        
    def hide_tip(self):
        """Быстро скрывает подсказку"""
        if self.tip:
            # Отменяем таймер показа если есть
            if self.show_timer:
                self.widget.after_cancel(self.show_timer)
                self.show_timer = None
                
            # Плавное исчезновение
            tip = self.tip
            self.tip = None
            
            for i in range(10, -1, -1):
                alpha = i / 10.0
                self.widget.after((10 - i) * 10, lambda a=alpha, t=tip: t.attributes('-alpha', a))
            
            # Уничтожаем после анимации
            self.widget.after(100, lambda t=tip: t.destroy() if t else None)
            
    def __enter__(self):
        # Быстрое появление при наведении
        self.widget.bind('<Enter>', lambda e: self._schedule_show())
        # Быстрое исчезновение при уходе курсора
        self.widget.bind('<Leave>', lambda e: self._schedule_hide())
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._cancel_timers()
        self.hide_tip()

    def _schedule_show(self):
        """Планирует показ подсказки"""
        self._cancel_timers()
        self.show_timer = self.widget.after(self.delay_show, self.show_tip)
    
    def _schedule_hide(self):
        """Планирует скрытие подсказки"""
        self._cancel_timers()
        self.hide_timer = self.widget.after(self.delay_hide, self.hide_tip)
    
    def _cancel_timers(self):
        """Отменяет все таймеры"""
        if self.show_timer:
            self.widget.after_cancel(self.show_timer)
            self.show_timer = None
        if self.hide_timer:
            self.widget.after_cancel(self.hide_timer)
            self.hide_timer = None

def apply_modern_theme(root):
    """Применяет современную тему к корневому окну"""
    colors = ModernUI.COLORS
    
    root.configure(bg=colors['background'])
    
    # Устанавливаем современный шрифт по умолчанию
    default_font = ('Segoe UI', 10)
    root.option_add("*Font", default_font)