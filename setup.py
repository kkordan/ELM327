# Импорт необходимых модулей для настройки пакета
from setuptools import setup, find_packages
import re
import os
import sys

import json
from urllib import request
from pkg_resources import parse_version

###########################################################################

# Константа для определения конца раздела введения в README
END_OF_INTRODUCTION = '# Installation'

# Эпилог с ссылкой на репозиторий проекта
EPILOGUE = '''
Полная информация и инструкции по использованию доступны в репозитории на GitHub: [ELM327-emulator](https://github.com/Ircama/ELM327-emulator).
'''

# Краткое описание проекта
DESCRIPTION = ("Эмулятор ELM327 для тестирования программного обеспечения, "
                "взаимодействующего с OBDII через адаптер ELM327")

# Имя пакета
PACKAGE_NAME = "ELM327-emulator"

# Файл, где хранится версия пакета
VERSIONFILE = "elm/__version__.py"

###########################################################################

# Функция для получения версий пакета с PyPI или TestPyPI
def versions(pkg_name, site):
    # Формирование URL для запроса версий пакета
    url = 'https://' + site + '.python.org/pypi/' + pkg_name + '/json'
    try:
        # Запрос и получение списка версий пакета
        releases = json.loads(request.urlopen(url).read())['releases']
    except Exception as e:
        # Вывод ошибки в случае проблем с запросом
        print("Ошибка при получении данных с URL '" + url + "': " + e)
        return []
    # Сортировка версий по порядку, от последней к первой
    return sorted(releases, key=parse_version, reverse=True)

# Чтение содержимого README файла для использования как длинное описание
with open("README.md", "r") as readme:
    long_description = readme.read()

# Параметры сборки (если они есть)
build = ''
# Чтение версии пакета из файла VERSIONFILE
verstrline = open(VERSIONFILE, "rt").read()
# Регулярное выражение для поиска строки с версией
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)  # Извлечение версии пакета
else:
    # Если версия не найдена, вызывается ошибка
    raise RuntimeError("Не удалось найти строку версии в %s." % (VERSIONFILE,))

# Если сборка запускается на GitHub, то добавляется номер сборки
if os.environ.get('GITHUB_RUN_NUMBER') is not None:
    # Получение списка версий пакета с PyPI и TestPyPI
    version_list_pypi = [
        a for a in versions(PACKAGE_NAME, 'pypi') if a.startswith(verstr)]
    version_list_testpypi = [
        a for a in versions(PACKAGE_NAME, 'testpypi') if a.startswith(verstr)]
    
    # Если версии найдены или принудительно указан номер сборки, то номер добавляется к версии
    if (version_list_pypi or
            version_list_testpypi or
            os.environ.get('GITHUB_FORCE_RUN_NUMBER') is not None):
        print('---------------------------------'
            '---------------------------------')
        print("Используется номер сборки " + os.environ['GITHUB_RUN_NUMBER'])
        if version_list_pypi:
            print(
                "Список версий на PyPI: " +
                ', '.join(version_list_pypi))
        if version_list_testpypi:
            print(
                "Список версий на TestPyPI: " +
                ', '.join(version_list_testpypi))
        print('---------------------------------'
            '---------------------------------')
        verstr += '-' + os.environ['GITHUB_RUN_NUMBER']  # Добавление номера сборки к версии
setup(
    # Имя пакета, которое будет использовано для установки и публикации
    name=PACKAGE_NAME,
    
    # Версия пакета, определенная ранее в коде
    version=verstr,
    
    # Краткое описание пакета
    description=(DESCRIPTION),
    
    # Полное описание пакета, вырезанное до раздела "Installation" из README
    long_description=long_description[
        :long_description.find(END_OF_INTRODUCTION)] + EPILOGUE,
    
    # Тип содержимого для long_description (в данном случае это markdown)
    long_description_content_type="text/markdown",
    
    # Классификаторы, описывающие характеристики пакета для каталогов и поиска на PyPI
    classifiers=[
        "Operating System :: POSIX :: Linux",  # Пакет поддерживает Linux
        "Operating System :: MacOS :: MacOS X",  # Поддержка MacOS
        "Operating System :: POSIX",  # Поддержка других POSIX-систем
        "Operating System :: POSIX :: BSD",  # Поддержка BSD-систем
        "Operating System :: Microsoft :: Windows",  # Поддержка Windows
        "License :: Other/Proprietary License",  # Лицензия
        "Topic :: Communications",  # Пакет относится к коммуникациям
        "Topic :: Software Development :: Libraries :: Python Modules",  # Это библиотека для разработки
        'Programming Language :: Python :: 3 :: Only',  # Поддерживается только Python 3
        "Development Status :: 5 - Production/Stable",  # Пакет стабилен и готов к использованию
        "Intended Audience :: Manufacturing",  # Целевая аудитория - производители
        "Intended Audience :: Telecommunications Industry",  # Для телекоммуникационной отрасли
        "Topic :: System :: Emulators",  # Пакет относится к эмуляторам
        "Intended Audience :: Developers",  # Пакет предназначен для разработчиков
    ],
    
    # Ключевые слова для поиска пакета
    keywords=("elm327 emulator obdii obd2 torque simulation simulator "
                "can-bus automotive"),
    
    # Автор пакета
    author="Ircama",
    
    # URL-адрес репозитория проекта
    url="https://github.com/Ircama/ELM327-emulator",
    
    # Лицензия пакета
    license='CC-BY-NC-SA-4.0',
    
    # Поиск и установка всех пакетов, включенных в проект
    packages=find_packages(),
    
    # Определение консольных скриптов для установки
    entry_points={
        'console_scripts': [
            'elm = elm:main',  # Основной скрипт elm
            'obd_dictionary = obd_dictionary:main'  # Скрипт obd_dictionary
        ]
    },
    
    # Включение дополнительных данных в пакет
    include_package_data=True,
    
    # Установка пакета без архивирования
    zip_safe=False,
    
    # Список зависимостей, которые нужно установить вместе с пакетом
    install_requires=[
        'python-daemon',  # Зависимость python-daemon
        'pyyaml',  # Зависимость pyyaml
        'obd',  # Зависимость для работы с OBD
        "pyreadline3 ; platform_system=='Windows'"  # Зависимость pyreadline3 только для Windows
    ],
    
    # Требуемая версия Python (минимум 3.5)
    python_requires='>3.5'
)
