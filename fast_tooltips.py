"""
Улучшенные всплывающие подсказки с быстрым появлением и исчезновением
"""

import tkinter as tk
from tkinter import ttk
from ui_enhancement import ModernUI

class FastToolTip:
    """Очень быстрые подсказки с плавными анимациями"""
    
    def __init__(self, widget, text, delay_show=150, delay_hide=50, max_width=300):
        self.widget = widget
        self.text = text
        self.delay_show = delay_show
        self.delay_hide = delay_hide
        self.max_width = max_width
        self.tip = None
        self.show_timer = None
        self.hide_timer = None
        
        # Современная цветовая схема
        self.colors = {
            'bg': '#ffffff',
            'fg': '#0f172a',
            'border': '#e2e8f0',
            'shadow': '#f0f0f0'  # Светло-серый вместо RGBA
        }
        
        # Привязываем события
        self.widget.bind('<Enter>', self._on_enter)
        self.widget.bind('<Leave>', self._on_leave)
        self.widget.bind('<Button-1>', self._on_click)  # Скрываем при клике
    
    def _on_enter(self, event):
        """Быстрое появление при наведении"""
        self._cancel_timers()
        self.show_timer = self.widget.after(self.delay_show, self._show_tooltip)
    
    def _on_leave(self, event):
        """Мгновенное исчезновение при уходе курсора"""
        self._cancel_timers()
        self.hide_timer = self.widget.after(self.delay_hide, self._hide_tooltip)
    
    def _on_click(self, event):
        """Скрываем при клике"""
        self._cancel_timers()
        self._hide_tooltip()
    
    def _show_tooltip(self):
        """Быстро показывает подсказку без проблемных анимаций"""
        if self.tip or not self.text:
            return
            
        # Вычисляем позицию
        x = self.widget.winfo_rootx() + 10
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        
        # Создаем подсказку
        self.tip = tk.Toplevel(self.widget)
        self.tip.wm_overrideredirect(True)
        self.tip.wm_geometry(f"+{x}+{y}")
        
        # Простой frame
        main_frame = tk.Frame(self.tip, bg=self.colors['bg'], relief='solid', bd=1)
        main_frame.pack()
        
        # Текст подсказки
        label = tk.Label(
            main_frame,
            text=self.text,
            bg=self.colors['bg'],
            fg=self.colors['fg'],
            font=('Segoe UI', 9),
            justify='left',
            wraplength=self.max_width,
            padx=12,
            pady=8
        )
        label.pack()
        
        # Простое появление без альфа-анимации
        self.tip.deiconify()
        
    def _hide_tooltip(self):
        """Быстро скрывает подсказку"""
        if self.tip:
            tip = self.tip
            self.tip = None
            
            # Простое мгновенное уничтожение
            tip.destroy()
    
    def _cancel_timers(self):
        """Отменяет все таймеры"""
        if self.show_timer:
            self.widget.after_cancel(self.show_timer)
            self.show_timer = None
        if self.hide_timer:
            self.widget.after_cancel(self.hide_timer)
            self.hide_timer = None

class InstantToolTip:
    """Мгновенные подсказки (без задержек)"""
    
    def __init__(self, widget, text, max_width=250):
        self.widget = widget
        self.text = text
        self.max_width = max_width
        self.tip = None
        
        # Стиль для мгновенных подсказок
        self.colors = {
            'bg': '#1e293b',  # Темный фон
            'fg': '#f8fafc',  # Светлый текст
            'border': '#334155'
        }
        
        # События
        self.widget.bind('<Enter>', self._show_instant)
        self.widget.bind('<Leave>', self._hide_instant)
        self.widget.bind('<Button-1>', self._hide_instant)
    
    def _show_instant(self, event):
        """Мгновенный показ"""
        self._hide_instant(event)  # Скрываем предыдущую
        
        x = self.widget.winfo_rootx() + 5
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 3
        
        self.tip = tk.Toplevel(self.widget)
        self.tip.wm_overrideredirect(True)
        self.tip.wm_geometry(f"+{x}+{y}")
        
        # Стильная подсказка с закругленными углами (эмуляция)
        label = tk.Label(
            self.tip,
            text=self.text,
            bg=self.colors['bg'],
            fg=self.colors['fg'],
            font=('Segoe UI', 8, 'bold'),
            justify='center',
            wraplength=self.max_width,
            padx=10,
            pady=6,
            relief='solid',
            bd=1,
            highlightthickness=1,
            highlightbackground=self.colors['border']
        )
        label.pack()
        
        # Мгновенное появление
        self.tip.deiconify()
    
    def _hide_instant(self, event):
        """Мгновенное скрытие"""
        if self.tip:
            self.tip.destroy()
            self.tip = None

# Функции для быстрого создания подсказок
def create_fast_tooltip(widget, text, show_delay=150, hide_delay=50):
    """Создает быструю подсказку"""
    return FastToolTip(widget, text, show_delay, hide_delay)

def create_instant_tooltip(widget, text):
    """Создает мгновенную подсказку"""
    return InstantToolTip(widget, text)

def apply_tooltip_to_buttons(container, button_configs):
    """Применяет подсказки к группе кнопок"""
    for button, text, tooltip_type in button_configs:
        if tooltip_type == 'fast':
            FastToolTip(button, text)
        elif tooltip_type == 'instant':
            InstantToolTip(button, text)
        elif tooltip_type == 'standard':
            from ui_enhancement import ToolTip
            with ToolTip(button, text, delay_show=200, delay_hide=100):
                pass

# Демонстрация
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Демо быстрых подсказок")
    root.geometry("400x300")
    
    # Создаем кнопки для демонстрации
    frame = tk.Frame(root, bg=ModernUI.COLORS['background'])
    frame.pack(expand=True, fill='both', padx=20, pady=20)
    
    # Быстрая подсказка
    btn1 = tk.Button(frame, text="Быстрая подсказка", font=('Arial', 12))
    btn1.pack(pady=10)
    FastToolTip(btn1, "Появляется через 150мс, исчезает через 50мс")
    
    # Мгновенная подсказка
    btn2 = tk.Button(frame, text="Мгновенная подсказка", font=('Arial', 12))
    btn2.pack(pady=10)
    InstantToolTip(btn2, "Мгновенное появление и исчезновение")
    
    # Стандартная подсказка
    btn3 = tk.Button(frame, text="Стандартная подсказка", font=('Arial', 12))
    btn3.pack(pady=10)
    from ui_enhancement import ToolTip
    with ToolTip(btn3, "Обычная подсказка с анимацией", delay_show=200, delay_hide=100):
        pass
    
    root.mainloop()