from flask_login import UserMixin
import mysql.connector

class User(UserMixin):


    def __init__(self, id_, name, email, profile_pic):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic


    @staticmethod
    def get(user_id):
        dbconfig = {"host": "theonlycakes.mysql.pythonanywhere-services.com",
                "user": "theonlycakes",
                "password": "3O2W$72l8d",
                "database": "theonlycakes$website", }
        conn = mysql.connector.connect(**dbconfig)
        cursor = conn.cursor(buffered=True)
        cursor.execute("SELECT * FROM user WHERE id = %s", (user_id,)
        )
        user = cursor.fetchone()
        if not user:
            cursor.close()
            conn.close()
            return None

        user = User(
            id_=user[0], name=user[1], email=user[2], profile_pic=user[3]
        )
        cursor.close()
        conn.close()
        return user

    @staticmethod
    def create(id_, name, email, profile_pic):
        dbconfig = {"host": "theonlycakes.mysql.pythonanywhere-services.com",
                "user": "theonlycakes",
                "password": "3O2W$72l8d",
                "database": "theonlycakes$website", }
        conn = mysql.connector.connect(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO user (id, name, email, profile_pic) "
            "VALUES (%s, %s, %s, %s)",
            (id_, name, email, profile_pic),
        )
        conn.commit()
        cursor.close()
        conn.close()