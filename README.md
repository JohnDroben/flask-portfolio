# flask-portfolio
выполним миграции для создания таблиц:

Шаги для решения:
Установите Flask-Migrate (если еще не установлен):

bash
pip install flask-migrate
Инициализируйте систему миграций:

bash
flask db init
Создайте начальную миграцию:

bash
flask db migrate -m "Initial migration"
Примените миграции к базе данных:

bash
flask db upgrade

