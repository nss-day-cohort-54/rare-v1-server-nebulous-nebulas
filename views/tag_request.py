import json
import sqlite3


def create_new_tag(new_tag):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
            INSERT INTO Tags
                (label)
            VALUES
                (?)
                """, (new_tag['label'], ))
        
        id = db_cursor.lastrowid
        
        new_tag['id'] = id
        
        return json.dumps({
            'token': id,
            'valid': True
        })