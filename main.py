from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:izzy@localhost:3306/blogz'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'ebay'
db = SQLAlchemy(app)


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300))
    body = db.Column(db.String(2000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name,body, owner, username):
        self.title = name
        self.body =body
        self.owner=owner
        self.username = username
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self,username,password):
        self.username = username
        self.password = password

@app.route('/')
def index():
    users = User.query.order_by(User.id.desc()).all()
    return render_template('index.html', users = users)


@app.before_request
def require_login():
    allowed_routes = ['login','signup','blog','index','logout']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

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


@app.route('/login', methods=['POST','GET'])
def login():
    username_error=''
    password_error=''

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query(username=username).first() == None:
            username_error='Invalid username'
        
            
        if username and username.password == password:
            session['username'] = username
            return redirect('/newpost')
        else:
             
            password_error = 'Invalid password'

    return render_template('login.html', password_error=password_error, username_error=username_error)


def valid_length(input):
    for i in input:
        if i == " ":
            return False
    return (len(input) >= 3 and len(input)<=20)

def match(password, verify):
    return password == verify

@app.route('/signup', methods = ['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template('signup.html', username_error="Username already register, Please sign in!")
        elif password != verify:
            return render_template('signup.html', password_error="Passwords must match")
        
      
    
        new_user = User(username,password)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        return redirect('/newpost')
    if request.method == 'GET':
        return render_template('signup.html')


@app.route('/logout',methods=['POST'])
def logout():
    del session['username']
    return redirect('/blog')









if __name__== '__main__':


                app.run()