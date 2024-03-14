from flask_app.config.mysqlconnections import connectToMySQL
from flask_app.models.users_model import User
from flask import flash 

class Post:
    def __init__(self, data):
        self.id = data['id']
        self.comment = data['comment']
        self.book_club = data['book_club']
        self.date = data['date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.host_id = data['user_id']
        self.comments = []  
        self.likes = []    
        self.host = None

    @classmethod
    def get_all(cls):
        query = """
            SELECT * FROM posts 
            JOIN users 
            ON users.id = posts.user_id
            ;"""
        results = connectToMySQL("readerscorner_db").query_db(query)
        posts = []
        for row in results:
            posts.append(cls(row))
        return posts
    
    @classmethod 
    def get_comments(self):
        query = "SELECT * FROM comments WHERE post_id = %(post_id)s"
        data = {'post_id': self.id}
        results = connectToMySQL("readerscorner_db").query_db(query, data)
        for row in results:
            self.comments.append(Comment(row))
        return self.comments
   
    @classmethod
    def get_likes(self):
        query = "SELECT * FROM likes WHERE post_id = %(post_id)s"
        data = {'post_id': self.id}
        results = connectToMySQL("readerscorner_db").query_db(query, data)
        for row in results:
            self.likes.append(Like(row))
        return self.likes

#========= edited by Juli 
    @classmethod 
    def get_all_post_with_host(cls):
        query= """ 
            SELECT * FROM posts
            JOIN users 
            ON users.id = posts.user_id
            ;"""
        results= connectToMySQL('readerscorner_db').query_db(query)
        posts = []
        for post_data in results:
            this_post = cls(post_data)
            this_post.host = User.parse_user(post_data)
            posts.append(this_post)
        return posts
    
#====creatde by Juli 
    @classmethod
    def get_post_by_id_w_host(cls,id):
        data = {'id': id }
        query = """
            SELECT * FROM posts 
            JOIN users
            ON users.id = posts.user_id
            WHERE posts.id = %(id)s
            ;"""
        results = connectToMySQL('readerscorner_db').query_db(query,data)
        this_post = cls(results[0])
        this_post.host = User.parse_user(results[0])
        return this_post 
    
    @classmethod
    def get_by_id(cls, id):
        query = "SELECT * FROM posts WHERE id = %(id)s;"
        result = connectToMySQL("readerscorner_db").query_db(query, {'id': id})
        if result:
            return cls(result[0])
        return None

#=====Edited by Juli 
    @classmethod
    def create_post(cls, data):
        if not cls.validate_post(data):
            return False
        query = """
            INSERT INTO posts
            (comment, book_club, date, user_id)
            VALUES 
            (%(comment)s, %(book_club)s, %(date)s, %(user_id)s)
            ;"""
        return connectToMySQL("readerscorner_db").query_db(query, data)

    @classmethod
    def update(cls, data):
        query = """
            UPDATE posts
            SET 
                comment = %(comment)s,
                book_club = %(book_club)s, 
                date= %(date)s
            WHERE id = %(id)s
            ;"""
        return connectToMySQL("readerscorner_db").query_db(query, data)

    @classmethod
    def delete(cls, id):
        data = {'id': id}
        query = "DELETE FROM posts WHERE id = %(id)s;"
        return connectToMySQL("readerscorner_db").query_db(query,data)

#===========Validations (created by Juli)
    @classmethod
    def validate_post(cls,data):
        is_valid = True
        if len(data['comment']) < 25 :
            flash ("Post must be at least 25 characters", 'create_post')
            is_valid = False
        if "book_club" not in data or not data["book_club"]: 
            flash ("Please select a book club", 'create_post')
            is_valid = False
        if "date" not in data or not data["date"] :
            flash ("Please choose a date", 'create_post')
            is_valid = False
        return is_valid 

# ================ Class method for comments and likes on posts
    
class Comment:
    def __init__(self, data):
        self.id = data['id']
        self.comment_text = data['comment_text']
        self.user_id = data['user_id']
        self.post_id = data['post_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

class Like:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.post_id = data['post_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']