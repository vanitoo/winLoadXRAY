@echo off
REM Скрипт создания виртуального окружения для winLoadXRAY

echo Создание виртуального окружения...
python -m venv .venv

echo Активация виртуального окружения...
call .venv\Scripts\activate.bat

echo Обновление pip...
python -m pip install --upgrade pip

echo Установка зависимостей...
pip install -r requirements.txt

echo.
echo Виртуальное окружение создано и настроено!
echo Для активации используйте: winLoadXRAY-env\Scripts\activate.bat
echo Для деактивации используйте: deactivate
echo.