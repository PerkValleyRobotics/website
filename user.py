from flask_login import UserMixin
import mysql.connector
import siteInfo

dbconfig = {"host": siteInfo.databasehost(),
                "user": siteInfo.databaseuser(),
                "password": siteInfo.databasepassword(),
                "database": siteInfo.database(), }

class User(UserMixin):


    def __init__(self, id_, name, email, profile_pic, access_level):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic
        self.access_level = access_level

    @staticmethod
    def get(user_id):

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
            id_=user[0], name=user[1], email=user[2], profile_pic=user[3], access_level=user[4]
        )
        cursor.close()
        conn.close()
        return user

    @staticmethod
    def create(id_, name, email, profile_pic, access_level):
        conn = mysql.connector.connect(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO user (id, name, email, profile_pic, access_level) "
            "VALUES (%s, %s, %s, %s, %s)",
            (id_, name, email, profile_pic, access_level),
        )
        conn.commit()
        cursor.close()
        conn.close()