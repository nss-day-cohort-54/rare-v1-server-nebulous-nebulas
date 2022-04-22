
from ast import Delete
from hmac import new
import sqlite3
import json
from models.Category import Category


def get_all_categories():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
            SELECT
                c.id,
                c.label
            
            FROM Categories c
            
            ORDER BY c.label ASC
                          """
                          )
        
        categories = []
        
        dataset = db_cursor.fetchall()
        
        for row in dataset:
            category = Category(row['id'], row['label'])
            
            categories.append(category.__dict__)
        
        return json.dumps(categories)
    
    
def get_single_category(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
            SELECT
                c.id,
                c.label
            
            FROM Categories c
            WHERE c.id = id
                        """
                        )
        
        data = db_cursor.fetchone()       
        
        category = Category(data['id'], data['label'])              
        
        return json.dumps(category.__dict__)
        
def delete_category(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
            DELETE
            FROM Categories
            WHERE id = ?
            """, (id, ))
        
        rows_affected = db_cursor.rowcount
        
        if rows_affected > 0:
            return True
        else:
            return False


def update_category(id, new_category):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
                          
            UPDATE Categories

            SET
                label = ?
            WHERE id = ?
            
            """, (new_category['label'], id,  ))
        

        rows_affected = db_cursor.rowcount
        
        if rows_affected > 0:
            return True
        else:
            return False