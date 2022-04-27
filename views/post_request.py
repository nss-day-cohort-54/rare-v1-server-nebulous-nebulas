import sqlite3
import json
from models.Category import Category
from models.Post import Post
from models.User import User


def get_all_posts():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
           SELECT
                p.id,
                p.user_id,
                p.category_id,
                p.title,
                p.publication_date,
                p.image_url,
                p.content,
                p.approved,
                c.label
                
            
            FROM Posts p
            LEFT JOIN Categories c
            ON p.category_id = c.id
            WHERE p.id = ?
            ORDER BY p.publication_date ASC """
                          )

        posts = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            post = Post(row['id'], row['user_id'], row['category_id'], row['title'],
                        row['publication_date'], row['image_url'], row['content'])

            category = Category(row['category_id'], row['label'])

            post.category = category.__dict__

            posts.append(post.__dict__)

        return json.dumps(posts)


def get_single_post(id):
    with sqlite3.connect("./db.sqlite3") as will:
        will.row_factory = sqlite3.Row
        will_cursor = will.cursor()

        will_cursor.execute("""
           SELECT
                p.id,
                p.user_id,
                p.category_id,
                p.title,
                p.publication_date,
                p.image_url,
                p.content,
                p.approved,
                c.label
                
            
            FROM Posts p
            JOIN Users u
            ON p.user_id = u.id
            LEFT JOIN Categories c
            ON p.category_id = c.id
            WHERE p.id = ?
            ORDER BY p.publication_date ASC
            
            """, (id, ))

        wd = will_cursor.fetchone()

        post = Post(wd['id'], wd['user_id'], wd['category_id'], wd['title'],
                    wd['publication_date'], wd['image_url'], wd['content'])
        category = Category(wd['category_id'], wd['label'])

        post.category = category.__dict__

        return json.dumps(post.__dict__)


def create_new_post(new_post):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()


        db_cursor.execute("""
            INSERT INTO Posts
            (
            'user_id',
            'category_id',
            'title',
            'publication_date',
            'image_url',
            'content',
            'approved'
            )
            VALUES (?, ?, ? ,? , ?, ?, ?)
        """, (new_post['userId'],new_post['categoryId'],new_post['title'],
              new_post['publicationDate'],new_post['imageUrl'],new_post['content'],new_post['approved']))
        id=db_cursor.lastrowid
        new_post['id']=id 
        
        return json.dumps({
                'token': id,
                'valid': True
            })