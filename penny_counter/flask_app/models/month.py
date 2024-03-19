from flask_app.config.mysqlconnection import connectToMySQL;
from flask_app.models import user;

class Month:
    db = "penny_counter"
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.limit = data["limit"]
        self.creator = None
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def save(cls, data):
        query = "INSERT INTO months (name, `limit`, user_id) VALUES (%(name)s, %(limit)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)
    


    @classmethod
    def get_all_by_user(cls, data):
        query = "SELECT * FROM months LEFT JOIN users ON months.user_id = users.id WHERE users.id = %(id)s ORDER BY months.created_at ASC;"
        results = connectToMySQL(cls.db).query_db(query, data);
        months = []
        if results:
            for row in results:
                month = cls(row)
                data = {
                    'id': row['users.id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'password': row['password'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at']
                }
                month.creator = user.User(data)
                months.append(month)
            return months
    
        # might be replaced with get_all_by_user
    @classmethod
    def show_all(cls):
        query = "SELECT * FROM months;"
        results = connectToMySQL(cls.db).query_db(query)
        months = []
        for month in results:
            months.append(cls(month))
        return months
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM months WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        return cls(result[0])