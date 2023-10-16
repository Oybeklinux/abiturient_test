import sqlite3


class Database:

    def __init__(self, path_to_db="data/main.db"):
        self.db = path_to_db
        self.create_table_regions()
        self.create_table_universities()
        self.create_table_subjects()
        self.create_table_users()

    @property
    def connection(self):
        return sqlite3.connect(self.db)

    def execute(self, sql: str, parameters: tuple = tuple(), fetchone=False,
                fetchall=False, commit=False):

        connection = self.connection
        connection.set_trace_callback(self.logger)
        cursor = connection.cursor()
        cursor.execute(sql, parameters)

        data = None
        if commit:
            connection.commit()

        if fetchone:
            data = cursor.fetchone()

        if fetchall:
            data = cursor.fetchall()

        connection.close()
        return data

    def logger(self, statement):
        print(f'''
_______________________________________
{statement}
_______________________________________
''')

    # CREATE TABLE
    def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name varchar(255) NOT NULL,
        last_logged datetime,
        region_id integer,
        university_id id,
        phone varchar(20),
        subject1 integer,
        subject2 integer,
        subject3 integer,
        FOREIGN KEY(subject1) REFERENCES subjects(id),
        FOREIGN KEY(subject2) REFERENCES subjects(id),
        FOREIGN KEY(subject3) REFERENCES subjects(id),
        FOREIGN KEY(region_id) REFERENCES regions(id),
        FOREIGN KEY(university_id) REFERENCES universities(id)
        )"""

        self.execute(sql, commit=True)

    def create_table_subjects(self):
        sql = """
        CREATE TABLE IF NOT EXISTS subjects(
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name varchar(255) NOT NULL,
            is_main boolean default 0
        )"""

        self.execute(sql, commit=True)

    def create_table_regions(self):
        sql = """
        CREATE TABLE IF NOT EXISTS regions(
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name varchar(255) NOT NULL      
        )"""

        self.execute(sql, commit=True)

    def create_table_universities(self):
        sql = """
        CREATE TABLE IF NOT EXISTS universities(
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name varchar(255) NOT NULL       
        )"""

        self.execute(sql, commit=True)

    # EXTRA FUNCTIONS
    def format_args(self, parameters: dict, prefix=''):
        sql = " AND ".join(
            [f"{prefix}{param} = ?" for param in parameters]
        )
        parameters = list(parameters.values())
        return sql, parameters

    # USERS
    def add_user(self, id: int, name: str):
        sql = """INSERT INTO users(id, name) VALUES(?,?)"""

        parameters = (id, name)
        self.execute(sql, parameters, commit=True)

    def is_user_registered(self, id):
        sql = "SELECT count(*) FROM users WHERE id=? and phone is not NULL"
        row = self.execute(sql, (id,), fetchone=True)
        return row[0] > 0

    def select_all_users(self):
        sql = """SELECT * FROM users"""
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        sql, parameters = self.format_args(kwargs, prefix='u.')

        sql = f"""SELECT u.id, u.name, u.phone, r.name, v.name, u.subject1, u.subject2
                    FROM users u
                    LEFT JOIN regions r ON u.region_id=r.id
                    LEFT JOIN regions v ON u.university_id=v.id 
                    WHERE {sql}"""

        return self.execute(sql, parameters=parameters, fetchone=True)

    def select_user_language(self, id):
        sql = f"""SELECT language FROM users WHERE id=?"""
        row = self.execute(sql, (id,), fetchone=True)
        if not row:
            return None
        return row[0]

    def select_count(self):
        return self.execute("""SELECT count(*) FROM users""", fetchone=True)

    def update_user(self, **kwargs):
        id = kwargs['id']
        kwargs.pop('id')
        sql, parameters = self.format_args(kwargs)
        parameters.append(id)
        sql = sql.replace('AND', ',')
        sql = f"""UPDATE users SET {sql} WHERE id=?"""
        try:
            self.execute(sql, parameters, commit=True)
        except Exception as e:
            print(e)

    def delete_user(self, id):
        sql = """DELETE users WHERE id=?"""
        self.execute(sql, parameters=(id,), commit=True)

    def delete_all(self):
        sql = """DELETE FROM users"""
        self.execute(sql, commit=True)

    # REGIONS
    def select_regions(self):
        sql = "SELECT id, name FROM regions"
        return self.execute(sql, fetchall=True)

    # SUBJECTS

    def select_main_subjects(self):
        sql = 'SELECT id, name FROM subjects WHERE is_main=1'
        return self.execute(sql, fetchall=True)

    def select_subjects(self):
        sql = 'SELECT id, name FROM subjects WHERE is_main=0'
        return self.execute(sql, fetchall=True)

    def select_subjects(self, user_id):
        """
        Gets id, subject name, is subject chosen by user (1 - selected by user, 0 - not selected)
        """
        rows = self.select_user_subjects(user_id)

        sql = """SELECT id, name, CASE  WHEN id=? or id=? THEN 1 ELSE 0 END 
                    FROM subjects
                    WHERE is_main=0"""
        return self.execute(sql, parameters=(rows[0], rows[1]), fetchall=True)

    def select_user_subjects(self, user_id):
        sql = 'SELECT subject1,subject2 FROM users WHERE id=?'
        return self.execute(sql, parameters=(user_id,),fetchone=True)

    def select_chosen_subjects(self, user_id):
        sql = """   SELECT id, name
                    FROM subjects
                    WHERE is_main=1 OR id in 
                            (SELECT subject1 FROM users WHERE id=? 
                            UNION 
                            SELECT subject2 FROM users WHERE id=?)"""
        return self.execute(sql, parameters=(user_id, user_id), fetchall=True)


if __name__ == "__main__":
    db = Database()
