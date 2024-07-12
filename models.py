from extensions import app, db, login_manager
from flask_login import UserMixin


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blog_id = db.Column(db.Integer)
    user = db.Column(db.String)
    comment = db.Column(db.String)
    date = db.Column(db.DateTime)
    
    def __str__(self):
        return f"{self.comment}"

class BlogModel(db.Model):
    name = db.Column(db.String)
    file = db.Column(db.String)
    description = db.Column(db.String)
    id = db.Column(db.Integer, primary_key=True)


    def __str__(self):
        return f"{self.name}"

class User(db.Model, UserMixin):
    username = db.Column(db.String)
    password = db.Column(db.String)
    role = db.Column(db.String)
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self, username, password, role="user"):
        self.username = username
        self.password = password
        self.role = role

    def __str__(self):
        return f"{self.username}"

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)
            

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        
        admin = User(username="admin", password="password123", role="admin")
        user = User(username="test1", password="pass123")
        db.session.add_all([admin,user])
        db.session.commit()       