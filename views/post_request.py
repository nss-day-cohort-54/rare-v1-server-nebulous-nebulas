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
                u.first_name,
                u.last_name,
                u.email,
                u.bio,
                u.username,
                u.password,
                u.profile_image_url,
                u.created_on,
                u.active,
                c.label
                
            
            FROM Posts p
            JOIN Users u
            ON p.user_id = u.id
            LEFT JOIN Categories c
            ON p.category_id = c.id
            ORDER BY p.publication_date ASC
            """
            )
        
        posts = []
        
        dataset = db_cursor.fetchall()
        
        for row in dataset:
            post = Post(row['id'], row['user_id'], row['category_id'], row['title'], row['publication_date'], row['image_url'], row['content'], row['approved'])
            
            
            category = Category(row['category_id'], row['label'])
            
            user = User(row['user_id'], row['first_name'], row['last_name'], row['email'], row['bio'], row['username'], row['password'], row['profile_image_url'], row['created_on'], row['active'])
        
            post.category = category.__dict__
            post.user = user.__dict__
            
            
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
                u.first_name,
                u.last_name,
                u.email,
                u.bio,
                u.username,
                u.password,
                u.profile_image_url,
                u.created_on,
                u.active,
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
        
        post = Post(wd['id'], wd['user_id'], wd['category_id'], wd['title'], wd['publication_date'], wd['image_url'], wd['content'], wd['approved'])
        category = Category(wd['category_id'], wd['label'])
        user = User(wd['user_id'], wd['first_name'], wd['last_name'], wd['email'], wd['bio'], wd['username'], wd['password'], wd['profile_image_url'], wd['created_on'], wd['active'])
        
        post.category = category.__dict__
        post.user = user.__dict__
        
        return json.dumps(post.__dict__)
        