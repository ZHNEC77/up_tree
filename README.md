### Установка и запуск приложения на локальном сервере

- создать виртуальное окружение и активировать

python -m venv venv
.\venv\Scripts\activate

- установить все зависимости из пакета requirements.txt

pip install -r requirements.txt

- перейти в директорию

cd main_tree_menu

- создать суперпользователя 'admin'

python manage.py createsuperuser
или
логин adm
пароль adm

- выполнить миграции базы данных

python manage.py migrate

- запустить проект

python manage.py runserver

