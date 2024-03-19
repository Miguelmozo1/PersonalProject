from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import month

class Purchase:
    db = "penny_counter"
    def __init__(self, data):
        self.id = data["id"]
        self.purchase_date = data["purchase_date"]
        self.description = data["description"]
        self.price = data["price"]
        self.creator = None
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def save_purchase(cls, data):
        query = "INSERT INTO purchases (purchase_date, description, price, month_id) VALUES (%(purchase_date)s, %(description)s, %(price)s, %(month_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_all_by_month(cls, data):
        query = "SELECT * FROM purchases JOIN months ON purchases.month_id = months.id WHERE months.id = %(id)s ORDER BY purchase_date ASC;"
        results = connectToMySQL(cls.db).query_db(query, data)
        purchases = []
        if results:
            for row in results:
                purchase = cls(row)
                data = {
                    'id':row['months.id'],
                    'name':row['name'],
                    'limit': row['limit'],
                    'created_at':row['months.created_at'],
                    'updated_at':row['months.updated_at']
                }
                purchase.creator = month.Month(data)
                purchases.append(purchase)
            return purchases

    @classmethod
    def delete_purchase(cls, data):
        query = "DELETE FROM purchases WHERE id = %(id)s ;"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def update(cls, data):
        query = "UPDATE purchases SET purchase_date = %(purchase_date)s, description = %(description)s, price = %(price)s WHERE id = %(purchase_id)s;"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * from purchases WHERE id = %(purchase_id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])
    
