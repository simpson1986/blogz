from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:izzy@localhost:3306/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)



class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300))
    body = db.Column(db.String(2000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name,body):
        self.title = name
        self.body =body

class User(db.Model):
    id = db.column(db.Integer, primary_key=True)
    username= db.Column(db.string(20), unique=True)
    password= db.Column(db.string(15))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

  



@app.route('/')
def index():
    return redirect('/blog')
@app.route('/newpost',methods=['POST','GET'])
def add_post():
    if request.method == 'POST':
        blog_name = request.form['title']
        blog_body = request.form['body']
        new_blog = Blog(blog_name,blog_body)
        db.session.add(new_blog)
        db.session.commit()
        return redirect('/blog')
    return render_template('newpost.html')

@app.route('/blog', methods=['GET'])
def blog():
    blog_post = request.args.get('id')

    if blog_post is None:
        tasks = Blog.query.all()
    else:
        tasks = Blog.query.filter_by(id = blog_post)
    return render_template('blog.html',title="Blog", tasks=tasks)
if __name__== '__main__':


                app.run()