import json
import sqlite3
from models import Tag

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



def get_all_tags():
    """get all tags"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            t.id,
            t.label
        FROM Tags t
        ORDER BY label
        """)

        tags = []

        dataset = db_cursor.fetchall()
        for row in dataset:
            tag = Tag(row['id'], row['label'])
            tags.append(tag.__dict__)

    return json.dumps(tags)

def get_single_tag(id):
    """get single tag"""
    with sqlite3.connect("./db.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            t.id,
            t.label
        FROM Tags t
        WHERE t.id = ?
        """, (id,))

        data = db_cursor.fetchone()
        tag = Tag(data['id'], data['label'])

        return json.dumps(tag.__dict__)

def update_tag(id, new_tag):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
            UPDATE Tags
                label = ?
            
            WHERE id = ?
            
                """, (new_tag['label'], id, ))
        
        return json.dumps({
            'token': id,
            'valid': True
        })
        

def delete_tag(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
            DELETE FROM Tags
            WHERE id = ? """, (id, ))
    
        rows_affected = db_cursor.rowcount
        
        if rows_affected > 0:
            return True
        else:
            return False
        