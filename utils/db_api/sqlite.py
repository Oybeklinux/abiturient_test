import json
import sqlite3

from aiogram.types import User


class TestItem:

    def __init__(self, text=None, image=None, audio=None, file=None, video=None):
        self.image = image
        self.text = text
        self.audio = audio
        self.file = file
        self.video = video

    def to_json(self):
        dict = {
            'image': self.image,
            'text': self.text,
            'audio': self.audio,
            'file': self.file,
            'video': self.video
        }
        return json.dumps(dict)


class Test:
    def __init__(self, question: TestItem, answer1: TestItem,
                 answer2: TestItem, answer3: TestItem,
                 answer4: TestItem):
        self.question = question
        self.answers = {
            "a1": answer1,
            "a2": answer2,
            "a3": answer3,
            "a4": answer4
        }


class Database:

    def __init__(self, path_to_db="data/main.db"):
        self.db = path_to_db
        self.create_table_regions()
        self.create_table_universities()
        self.create_table_subjects()
        self.create_table_users()
        self.create_table_tests()
        self.create_table_exam()
        self.create_table_test_results()
        self.create_table_test_report()

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
            return cursor.lastrowid

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

    def create_table_test_results(self):
        sql = """
       CREATE TABLE IF NOT EXISTS test_results(
            id integer PRIMARY KEY AUTOINCREMENT,
            subject_id INTEGER,
            user_id INTEGER,
            test_id INTEGER,
            exam_id INTEGER,
            answers varchar(30),
            right_answers varchar(30),
            score INTEGER,
            duration INTEGER DEFAULT 0,
            FOREIGN KEY(subject_id) REFERENCES subjects(id),
            FOREIGN KEY(exam_id) REFERENCES exam(id),
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(test_id) REFERENCES tests(id),
            UNIQUE(test_id, exam_id) ON CONFLICT REPLACE
        )"""

        self.execute(sql, commit=True)

    def create_table_test_report(self):
        sql = """
       CREATE TABLE IF NOT EXISTS exam_report(
            id integer PRIMARY KEY AUTOINCREMENT,
            subject_id INTEGER NOT NULL,
            exam_id INTEGER NOT NULL,
            score INTEGER NOT NULL,
            total_num INTEGER NOT NULL,
            wrong_answers INTEGER NOT NULL,
            right_answers INTEGER NOT NULL,
            null_answers INTEGER NOT NULL,
            FOREIGN KEY(subject_id) REFERENCES subjects(id),
            FOREIGN KEY(exam_id) REFERENCES exam(id)
        )"""

        self.execute(sql, commit=True)

    def create_table_exam(self):
        sql = """
       CREATE TABLE IF NOT EXISTS exam(
            id integer PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            score INTEGER,
            answered_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )"""

        self.execute(sql, commit=True)

    def create_table_tests(self):
        sql = """
        CREATE TABLE IF NOT EXISTS tests(
            id integer PRIMARY KEY AUTOINCREMENT,
            subject_id INTEGER,
            question text NOT NULL,
            answer1 text,
            answer2 text,
            answer3 text,
            answer4 text,
            answer5 text,
            answer6 text,
            FOREIGN KEY(subject_id) REFERENCES subjects(id)
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
    def select_subjects(self, is_main=None):
        """
        Gets subjects
        is_main:
                None - all subjects
                True - only main subjects
                False - only secondary subjects
        """
        if is_main is None:
            sql = """SELECT id, name 
                   FROM subjects"""
            return self.execute(sql, fetchall=True)
        elif is_main:
            sql = 'SELECT id, name FROM subjects WHERE is_main=1'
            return self.execute(sql, fetchall=True)
        elif not is_main:
            sql = 'SELECT id, name FROM subjects WHERE is_main=0'
            return self.execute(sql, fetchall=True)

    def select_subjects_2_tests(self):
        sql = """SELECT s.id, s.name, count(t.id) [total]
        FROM subjects s
        LEFT JOIN tests t ON t.subject_id=s.id
        GROUP BY s.id"""
        return self.execute(sql, fetchall=True)

    def select_user_subjects(self, user_id, only_selected=False):
        """
        Gets id, name, selected_or_not
        selected_or_not:
            1 - selected by user
            0 - not selected by user
        only_secondary:
                True - only user selected subjects
                False - all (user selected and  not selected) subjects
        """
        if not only_selected:
            rows = self.select_2_subjects(user_id)

            sql = """SELECT id, name, CASE  WHEN id=? or id=? THEN 1 ELSE 0 END 
                        FROM subjects
                        WHERE is_main=0"""
            return self.execute(sql, parameters=(rows[0], rows[1]), fetchall=True)
        elif only_selected:
            sql = """SELECT id, name
                    FROM subjects
                    WHERE is_main=1 OR id in 
                            (SELECT subject1 FROM users WHERE id=? 
                            UNION 
                            SELECT subject2 FROM users WHERE id=?)"""
            return self.execute(sql, parameters=(user_id, user_id), fetchall=True)

    def select_subject_id(self, name):
        sql = "SELECT id from subjects WHERE lower(name)=lower(?)"
        row = self.execute(sql, parameters=(name,), fetchone=True)
        return row[0]

    def select_2_subjects(self, user_id=None):
        sql = 'SELECT subject1,subject2 FROM users WHERE id=?'
        return self.execute(sql, parameters=(user_id,), fetchone=True)

    # EXAM REPORT
    def save_exam_report(self, exam_id):
        sql = """INSERT INTO exam_report(subject_id,exam_id,score,total_num,right_answers,wrong_answers,null_answers)
                SELECT t.subject_id, ? , sum(score), count(*) [total],sum(r.answers = right_answers) [is_correct],sum(r.answers <> right_answers) [is_wrong],sum(r.answers is NULL) [is_null]
                FROM tests t
                LEFT JOIN (SELECT * FROM test_results WHERE exam_id=81) r on r.test_id=t.id
                GROUP BY t.subject_id
                """
        self.execute(sql, parameters=(exam_id,), commit=True)

    def select_exam_report(self, exam_id):
        sql = """SELECT e.id,e.subject_id, s.name,e.exam_id,e.score,e.total_num,e.right_answers,e.wrong_answers,e.null_answers
                    FROM exam_report e
                    LEFT JOIN subjects s on s.id=e.subject_id
                    WHERE exam_id=?"""
        return self.execute(sql, parameters=(exam_id,),fetchall=True)

    def select_all_exam(self):
        user_id = User.get_current().id
        sql = """SELECT id, user_id,answered_date
                FROM exam
                WHERE user_id=?"""
        return self.execute(sql, parameters=(user_id,), fetchall=True)

    # TESTS
    def insert_test(self, test):
        subject_id = test['subject_id']
        sql = 'INSERT INTO tests(subject_id,question,answer1,answer2,answer3,answer4)' \
              ' VALUES(?,?,?,?,?,?)'
        q = json.dumps(test['q'])
        a1 = json.dumps(test['a1']) if test['a1'] else None
        a2 = json.dumps(test['a2']) if test['a2'] else None
        a3 = json.dumps(test['a3']) if test['a3'] else None
        a4 = json.dumps(test['a4']) if test['a4'] else None
        self.execute(sql, parameters=(subject_id, q, a1, a2, a3, a4), commit=True)

    def select_tests(self, subject_id, tests_done: str = "-1"):
        sql = f"SELECT * FROM tests WHERE subject_id=? and id not in ({tests_done.strip(',')})"
        return self.execute(sql, parameters=(subject_id,), fetchall=True)

    def select_test(self, test_id):
        sql = f"SELECT id,subject_id,question,answer1,answer2,answer3,answer4 FROM tests WHERE id=?"

        row = self.execute(sql, parameters=(test_id,), fetchone=True)
        return {
            'id': row[0],
            'q': json.loads(row[2]),
            'a1': json.loads(row[3]),
            'a2': json.loads(row[4]),
            'a3': json.loads(row[5]),
            'a4': json.loads(row[6]),
        }

    # TEST RESULT
    def insert_test_result(self, data):
        user_id = User.get_current().id
        subject_id = data['subject_id']
        exam_id = data['exam_id']
        test_id = data['current']['id']
        answers = ','.join(sorted(data['answered'][test_id]))
        right_answers = ','.join(sorted(data['questions'][test_id]))
        # if true - 100 else 0
        score = 0
        # account points for multiple choices
        point = 1 / len(data['questions'][test_id])
        for user_answer in data['answered'][test_id]:
            if user_answer in data['answered'][test_id]:
                score += point

        sql = "INSERT INTO test_results(exam_id, subject_id, user_id, test_id,answers,right_answers,score) " \
              "VALUES(?,?,?,?,?,?,?)"
        return self.execute(sql, parameters=(exam_id, subject_id, user_id, test_id, answers, right_answers, score),
                            commit=True)

    # USER TEST
    def begin_exam(self):
        user_id = User.get_current().id
        sql = "INSERT INTO exam(user_id) VALUES(?)"
        return self.execute(sql, parameters=(user_id,), commit=True)
    # EXAM REPORT

    # def insert_test_result(self, data):
    #     user_id = User.get_current().id
    #     subject_id = data['subject_id']
    #     test_id = data['current']['id']
    #     answers = ','.join(data['answered'][test_id])
    #     # if true - 100 else 0
    #     score = 100
    #     if len(data['questions'][test_id]) == len(data['answered'][test_id]):
    #         for right_answer in data['questions'][test_id]:
    #             if right_answer not in data['answered'][test_id]:
    #                 score = 0
    #                 break
    #     else: score = 0
    #     sql = "INSERT INTO test_results(subject_id, user_id, test_id,answers,score) " \
    #           "VALUES(?,?,?,?,?)"
    #     return self.execute(sql, parameters=(subject_id, user_id, test_id, answers, score), commit=True)


if __name__ == "__main__":
    db = Database()
