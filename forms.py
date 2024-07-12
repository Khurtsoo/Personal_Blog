from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FileField, TextAreaField
from wtforms.validators import Length, DataRequired

class AddBlog(FlaskForm):
    name = StringField(label="name", validators=[Length(min=3), DataRequired()])
    file = FileField(label="file")
    description = TextAreaField(label="description")
    submit = SubmitField(label="submit")

    def __str__(self):
        return f"{self.name}"
    
class AddComment(FlaskForm):
    comment = StringField(label="comment", validators=[Length(min=3), DataRequired()])
    submit = SubmitField(label="Comment")
    
    def __str__(self):
        return f"{self.name}"
    
class RegisterForm(FlaskForm):
    username = StringField(label="username")
    password = PasswordField(label="password")
    register = SubmitField(label="register")

class LoginForm(FlaskForm):
    username = StringField(label="username")
    password = PasswordField(label="password")
    login = SubmitField(label="login")