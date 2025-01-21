import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        self.connection = self.create_connection()

    def create_connection(self):
        """Создает соединение с базой данных."""
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",  # Замените на вашего пользователя
                password="1234",  # Замените на ваш пароль
                database="project_manager"
            )
            return connection
        except Error as e:
            print(f"Ошибка подключения к базе данных: {e}")
            return None

    def execute_query(self, query, params=None):
        """Выполняет SQL-запрос (INSERT, UPDATE, DELETE)."""
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params or ())
            self.connection.commit()
        except Error as e:
            print(f"Ошибка выполнения запроса: {e}")
        finally:
            cursor.close()

    def fetch_one(self, query, params=None):
        """Выполняет SQL-запрос и возвращает одну строку."""
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            return cursor.fetchone()
        except Error as e:
            print(f"Ошибка выполнения запроса: {e}")
            return None
        finally:
            cursor.close()

    def fetch_all(self, query, params=None):
        """Выполняет SQL-запрос и возвращает все строки."""
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            return cursor.fetchall()
        except Error as e:
            print(f"Ошибка выполнения запроса: {e}")
            return []
        finally:
            cursor.close()

    def add_user(self, username, full_name, password_hash):
        """Добавляет нового пользователя."""
        query = "INSERT INTO users (username, full_name, password_hash) VALUES (%s, %s, %s)"
        self.execute_query(query, (username, full_name, password_hash))

    def get_user(self, username):
        """Возвращает данные пользователя по логину."""
        query = "SELECT * FROM users WHERE username = %s"
        return self.fetch_one(query, (username,))

    def get_projects(self, user_id):
        """Возвращает все проекты пользователя."""
        query = "SELECT * FROM projects WHERE user_id = %s"
        return self.fetch_all(query, (user_id,))

    def get_tasks(self, project_id):
        """Возвращает все задачи проекта."""
        query = "SELECT * FROM tasks WHERE project_id = %s"
        return self.fetch_all(query, (project_id,))

    def add_project(self, user_id, name, status):
        """Добавляет новый проект."""
        query = "INSERT INTO projects (user_id, name, status) VALUES (%s, %s, %s)"
        self.execute_query(query, (user_id, name, status))

    def add_task(self, project_id, name, priority, start_date, end_date, is_completed=False):
        """Добавляет новую задачу."""
        query = """
        INSERT INTO tasks (project_id, name, priority, start_date, end_date, is_completed)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.execute_query(query, (project_id, name, priority, start_date, end_date, is_completed))

    def update_project_status(self, project_id, status):
        """Обновляет статус проекта."""
        query = "UPDATE projects SET status = %s WHERE id = %s"
        self.execute_query(query, (status, project_id))

    def delete_project(self, project_id):
        """Удаляет проект и все связанные задачи."""
        query = "DELETE FROM projects WHERE id = %s"
        self.execute_query(query, (project_id,))

    def delete_task(self, task_id):
        """Удаляет задачу."""
        query = "DELETE FROM tasks WHERE id = %s"
        self.execute_query(query, (task_id,))