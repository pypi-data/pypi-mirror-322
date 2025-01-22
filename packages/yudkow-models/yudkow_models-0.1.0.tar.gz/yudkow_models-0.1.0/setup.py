from setuptools import setup, find_packages

setup(
    name="yudkow-models",  # Уникальное имя вашего пакета
    version="0.1.0",         # Версия пакета
    author="BlTT",       # Автор пакета
    author_email="bltt6956@gmail.com",  # Email автора
    description="My package with models",  # Краткое описание
    packages=find_packages(),  # Автоматический поиск пакетов
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Лицензия (например, MIT)
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Минимальная версия Python
    install_requires=[],  # Список зависимостей (оставьте пустым, если их нет)
)