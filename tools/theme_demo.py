"""
Демонстрация переключения тем (светлая/темная) для winLoadXRAY
"""

import tkinter as tk
from tkinter import ttk, messagebox
from ui_enhancement import ModernUI, apply_modern_theme
from ui_themes import ThemeManager, AnimationManager


def create_theme_demo():
    """Создает окно демонстрации переключения тем"""
    
    # Создаем главное окно
    root = tk.Tk()
    root.title("Демонстрация тем - winLoadXRAY")
    root.geometry("700x500")
    root.resizable(True, True)
    
    # Инициализируем менеджер тем
    theme_manager = ThemeManager()
    apply_modern_theme(root)
    
    # Главный контейнер
    main_container = ModernUI.create_modern_frame(root, padding=25)
    
    # Заголовок
    title = ModernUI.create_modern_label(
        main_container, 
        "🎨 Демонстрация переключения тем", 
        variant='primary', 
        size='large'
    )
    title.pack(pady=(0, 20))
    
    # Текущая тема
    theme_label = ModernUI.create_modern_label(
        main_container,
        "Текущая тема: Светлая ☀️",
        variant='secondary',
        size='medium'
    )
    theme_label.pack(pady=(0, 20))
    
    # Секция демонстрации элементов
    demo_frame = ModernUI.create_modern_frame(main_container, padding=20)
    
    # Кнопки разных типов
    buttons_demo = ModernUI.create_modern_frame(demo_frame, padding=10)
    buttons_demo.pack(fill='x', pady=(0, 15))
    
    btn_primary = ModernUI.create_modern_button(
        buttons_demo, "Основная", lambda: None, variant='primary', size='medium'
    )
    btn_primary.pack(side='left', padx=5)
    
    btn_success = ModernUI.create_modern_button(
        buttons_demo, "Успех", lambda: None, variant='success', size='medium'
    )
    btn_success.pack(side='left', padx=5)
    
    btn_warning = ModernUI.create_modern_button(
        buttons_demo, "Внимание", lambda: None, variant='warning', size='medium'
    )
    btn_warning.pack(side='left', padx=5)
    
    btn_danger = ModernUI.create_modern_button(
        buttons_demo, "Опасность", lambda: None, variant='danger', size='medium'
    )
    btn_danger.pack(side='left', padx=5)
    
    btn_secondary = ModernUI.create_modern_button(
        buttons_demo, "Вторичная", lambda: None, variant='secondary', size='medium'
    )
    btn_secondary.pack(side='left', padx=5)
    
    # Поле ввода
    input_demo = ModernUI.create_modern_frame(demo_frame, padding=10)
    input_demo.pack(fill='x', pady=(0, 15))
    
    input_label = ModernUI.create_modern_label(
        input_demo, "Поле ввода:", variant='primary', size='small'
    )
    input_label.pack(anchor='w', pady=(0, 5))
    
    input_container, entry = ModernUI.create_modern_input(
        input_demo, "Введите текст...", 40
    )
    input_container.pack(fill='x')
    
    # Чекбоксы и переключатели
    options_demo = ModernUI.create_modern_frame(demo_frame, padding=10)
    options_demo.pack(fill='x', pady=(0, 15))
    
    var1 = tk.BooleanVar()
    var2 = tk.BooleanVar(value=True)
    var3 = tk.BooleanVar()
    
    check1 = ModernUI.create_modern_checkbutton(
        options_demo, "Опция 1", var1, lambda: print(f"Option 1: {var1.get()}")
    )
    check1.pack(side='left', padx=10)
    
    check2 = ModernUI.create_modern_checkbutton(
        options_demo, "Опция 2", var2, lambda: print(f"Option 2: {var2.get()}")
    )
    check2.pack(side='left', padx=10)
    
    check3 = ModernUI.create_modern_checkbutton(
        options_demo, "Опция 3", var3, lambda: print(f"Option 3: {var3.get()}")
    )
    check3.pack(side='left', padx=10)
    
    # Список
    listbox_label = ModernUI.create_modern_label(
        demo_frame, "Список элементов:", variant='primary', size='small'
    )
    listbox_label.pack(anchor='w', pady=(0, 5))
    
    listbox_container, listbox = ModernUI.create_modern_listbox(demo_frame, height=4)
    listbox_container.pack(fill='both', expand=True, pady=(0, 15))
    
    # Добавляем элементы в список
    for item in ["Элемент 1", "Элемент 2", "Элемент 3", "Элемент 4"]:
        listbox.insert(tk.END, item)
    
    # Кнопки управления
    control_demo = ModernUI.create_modern_frame(demo_frame, padding=10)
    control_demo.pack(fill='x')
    
    def toggle_theme():
        """Переключает тему"""
        new_theme = theme_manager.toggle_theme()
        
        # Анимация
        AnimationManager.fade_out(root, duration=150)
        root.after(150, lambda: apply_theme(new_theme))
    
    def apply_theme(theme_name):
        """Применяет тему"""
        theme = theme_manager.get_current_theme()
        
        # Обновляем root
        root.configure(bg=theme['background'])
        
        # Обновляем все виджеты
        update_all_widgets(main_container, theme)
        
        # Обновляем label текущей темы
        theme_text = "Светлая ☀️" if theme_name == 'light' else "Темная 🌙"
        theme_label.config(
            text=f"Текущая тема: {theme_text}",
            fg=theme['text_primary']
        )
        
        # Обновляем кнопку переключения
        btn_toggle.config(text="🌙" if theme_name == 'light' else "☀️")
        
        # Показываем интерфейс
        AnimationManager.fade_in(root, duration=150)
    
    def update_all_widgets(widget, theme):
        """Рекурсивно обновляет цвета виджетов"""
        try:
            widget_class = widget.winfo_class()
            
            # Обновляем текущий виджет
            if widget_class in ['Frame', 'TFrame', 'Labelframe']:
                if 'bg' in widget.keys():
                    widget.configure(bg=theme['background'])
            elif widget_class in ['Label', 'TLabel']:
                if 'bg' in widget.keys() and 'fg' in widget.keys():
                    current_bg = widget.cget('bg')
                    current_fg = widget.cget('fg')
                    
                    # Обновляем фоновый цвет
                    if current_bg in ['#f8fafc', '#0f172a', '#ffffff', '#1e293b']:
                        widget.configure(bg=theme['background'])
                    
                    # Обновляем цвет текста
                    if current_fg in ['#0f172a', '#f8fafc', '#64748b', '#94a3b8']:
                        if current_fg in ['#64748b', '#94a3b8']:
                            widget.configure(fg=theme['text_secondary'])
                        else:
                            widget.configure(fg=theme['text_primary'])
            elif widget_class in ['Button', 'TButton']:
                if 'bg' in widget.keys():
                    current_bg = widget.cget('bg')
                    # Не трогаем цветные кнопки
                    if current_bg not in ['#2563eb', '#16a34a', '#d97706', '#dc2626', '#64748b']:
                        widget.configure(
                            bg=theme['surface'],
                            fg=theme['text_primary'],
                            activebackground=theme['border']
                        )
            elif widget_class in ['Entry', 'TEntry']:
                if 'bg' in widget.keys():
                    widget.configure(
                        bg=theme['surface'],
                        fg=theme['text_primary'],
                        insertbackground=theme['text_primary']
                    )
            elif widget_class in ['Checkbutton', 'TCheckbutton']:
                if 'bg' in widget.keys():
                    widget.configure(
                        bg=theme['background'],
                        activebackground=theme['background'],
                        fg=theme['text_primary']
                    )
            elif widget_class in ['Listbox']:
                widget.configure(
                    bg=theme['surface'],
                    fg=theme['text_primary'],
                    selectbackground=theme['primary'],
                    selectforeground='white'
                )
            
            # Обновляем дочерние виджеты
            for child in widget.winfo_children():
                update_all_widgets(child, theme)
        except:
            pass
    
    # Кнопка переключения темы
    btn_toggle = ModernUI.create_modern_button(
        control_demo,
        "🌙",
        toggle_theme,
        variant='primary',
        size='large'
    )
    btn_toggle.pack(side='left', padx=(0, 10))
    
    # Кнопка информации
    btn_info = ModernUI.create_modern_button(
        control_demo,
        "ℹ️ Информация",
        lambda: messagebox.showinfo(
            "О темах",
            "winLoadXRAY поддерживает две темы:\n\n"
            "☀️ Светлая тема - классический светлый дизайн\n"
            "🌙 Темная тема - современный темный дизайн\n\n"
            "Нажмите кнопку переключения для смены темы."
        ),
        variant='secondary',
        size='medium'
    )
    btn_info.pack(side='left')
    
    # Кнопка закрытия
    btn_close = ModernUI.create_modern_button(
        control_demo,
        "Закрыть",
        root.destroy,
        variant='danger',
        size='medium'
    )
    btn_close.pack(side='right')
    
    # Нижняя панель с переключателем
    footer_frame = tk.Frame(root, bg=theme_manager.get_current_theme()['surface'], height=40)
    footer_frame.pack(fill='x', side='bottom')
    footer_frame.pack_propagate(False)
    
    footer_label = tk.Label(
        footer_frame,
        text="winLoadXRAY - Переключение темы",
        bg=theme_manager.get_current_theme()['surface'],
        fg=theme_manager.get_current_theme()['text_secondary'],
        font=('Segoe UI', 9)
    )
    footer_label.pack(side='left', padx=15, pady=10)
    
    return root


if __name__ == "__main__":
    demo_app = create_theme_demo()
    demo_app.mainloop()