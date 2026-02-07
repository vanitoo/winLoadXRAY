"""
Setup.py для установки зависимостей winLoadXRAY
Использование: python setup.py install
"""

from setuptools import setup, find_packages

# Чтение requirements
def read_requirements():
    with open('requirements.txt', 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="winLoadXRAY",
    version="0.84-beta",
    author="xVRVx",
    author_email="",
    description="Python GUI обертка вокруг ядра XRAY для работы с прокси-соединениями и VPN",
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/xVRVx/winLoadXRAY/",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: Microsoft :: Windows :: Windows 11",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: Proxy Servers",
        "Topic :: System :: Networking",
        "Topic :: Security",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        'dev': [
            'pyinstaller>=5.13.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'winLoadXRAY=winLoadXRAY:main',
        ],
    },
    include_package_data=True,
    package_data={
        '': ['*.json', '*.txt', '*.md'],
    },
)