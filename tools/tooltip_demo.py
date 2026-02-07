"""
Демонстрация быстрых всплывающих подсказок для winLoadXRAY
"""

import tkinter as tk
from tkinter import ttk
from ui_enhancement import ModernUI, apply_modern_theme
from fast_tooltips import FastToolTip, InstantToolTip

def create_tooltip_demo():
    """Создает окно демонстрации подсказок"""
    
    # Создаем главное окно
    root = tk.Tk()
    root.title("Демонстрация быстрых подсказок - winLoadXRAY")
    root.geometry("600x400")
    root.resizable(False, False)
    
    # Применяем современную тему
    apply_modern_theme(root)
    colors = ModernUI.COLORS
    
    # Главный контейнер
    main_frame = ModernUI.create_modern_frame(root, padding=20)
    
    # Заголовок
    title = ModernUI.create_modern_label(
        main_frame, 
        "Демонстрация быстрых всплывающих подсказок", 
        variant='primary', 
        size='large'
    )
    title.pack(pady=(0, 20))
    
    # Секция с разными типами подсказок
    demo_sections = [
        {
            'title': '⚡ Очень быстрые подсказки (100мс/30мс)',
            'buttons': [
                ("Загрузить конфиг", "Загружает конфигурацию из URL подписки"),
                ("Вставить из буфера", "Вставляет данные из буфера обмена"),
                ("Запустить XRAY", "Запускает XRAY SOCKS5 на порту 2080")
            ],
            'delay_show': 100,
            'delay_hide': 30
        },
        {
            'title': '🚀 Мгновенные подсказки',
            'buttons': [
                ("Системный прокси", "Настраивает системный прокси Windows"),
                ("TUN режим", "Включает виртуальную сетевую карту"),
                ("Автозапуск", "Добавляет в автозагрузку Windows")
            ],
            'instant': True
        },
        {
            'title': '⚙️ Стандартные подсказки (200мс/100мс)',
            'buttons': [
                ("Проверка версии", "Проверяет наличие обновлений"),
                ("Справка", "Открывает документацию проекта"),
                ("О программе", "Информация о версии и авторе")
            ],
            'delay_show': 200,
            'delay_hide': 100
        }
    ]
    
    for section in demo_sections:
        # Заголовок секции
        section_label = ModernUI.create_modern_label(
            main_frame, 
            section['title'], 
            variant='secondary', 
            size='medium'
        )
        section_label.pack(anchor='w', pady=(15, 10))
        
        # Кнопки секции
        buttons_frame = ModernUI.create_modern_frame(main_frame, padding=0)
        buttons_frame.pack(fill='x', pady=(0, 15))
        
        for i, (btn_text, tooltip_text) in enumerate(section['buttons']):
            # Создаем кнопку
            if 'instant' in section:
                btn = ModernUI.create_modern_button(
                    buttons_frame, 
                    btn_text, 
                    variant='warning' if i == 1 else 'primary',
                    size='small'
                )
            else:
                btn = ModernUI.create_modern_button(
                    buttons_frame, 
                    btn_text, 
                    variant='success' if i == 0 else 'secondary',
                    size='small'
                )
            
            # Размещаем кнопки в ряд
            btn.grid(row=0, column=i, padx=5, pady=5, sticky='ew')
            
            # Добавляем подсказку
            if 'instant' in section:
                InstantToolTip(btn, tooltip_text)
            else:
                FastToolTip(
                    btn, 
                    tooltip_text, 
                    delay_show=section['delay_show'], 
                    delay_hide=section['delay_hide']
                )
        
        # Настраиваем веса колонок
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)
        buttons_frame.grid_columnconfigure(2, weight=1)
    
    # Информационная панель
    info_frame = ModernUI.create_modern_frame(main_frame, padding=15)
    info_frame.pack(fill='x', pady=(20, 0))
    
    info_text = """💡 Инструкция:
    • Наведите курсор на любую кнопку для просмотра подсказки
    • Очень быстрые: появляются за 100мс, исчезают за 30мс
    • Мгновенные: появляются и исчезают без задержки
    • Стандартные: появляются за 200мс, исчезают за 100мс
    
    🎯 Рекомендация для winLoadXRAY:
    Используйте очень быстрые подсказки для основных функций,
    мгновенные для часто используемых кнопок."""
    
    info_label = ModernUI.create_modern_label(
        info_frame, 
        info_text, 
        variant='secondary', 
        size='small'
    )
    info_label.pack(anchor='w')
    
    # Кнопка закрытия
    close_btn = ModernUI.create_modern_button(
        main_frame, 
        "Закрыть демо", 
        root.destroy,
        variant='danger',
        size='medium'
    )
    close_btn.pack(pady=(20, 0))
    
    return root

if __name__ == "__main__":
    demo_app = create_tooltip_demo()
    demo_app.mainloop()