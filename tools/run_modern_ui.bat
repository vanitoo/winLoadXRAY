@echo off
REM Скрипт запуска winLoadXRAY с современным интерфейсом

echo ===================================
echo   winLoadXRAY - Современный UI
echo ===================================
echo.

REM Проверяем наличие виртуального окружения
if not exist ".venv\Scripts\python.exe" (
    echo Виртуальное окружение не найдено!
    echo Создаю виртуальное окружение...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    echo Устанавливаю зависимости...
    pip install -r requirements.txt
) else (
    echo Активирую виртуальное окружение...
    call .venv\Scripts\activate.bat
)

echo.
echo Запуск winLoadXRAY с современным интерфейсом...
echo.

REM Запускаем приложение
python winLoadXRAY.py

echo.
echo Приложение завершено.
pause