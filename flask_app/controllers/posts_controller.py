from flask import render_template, session, redirect, request, url_for
from flask_app import app
from flask_app.models.posts_model import Post
from flask_app.models.users_model import User
from werkzeug.utils import secure_filename
import os 
UPLOAD_FOLDER = 'flask_app/static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ==================== Fetch all posts from the database

@app.route('/homepage')
def homepage():
    if 'uid' not in session:
        return redirect('/')
    data = {
        'id': session['uid']
    }
    user = User.get_by_id(data)
    posts = Post.get_all_post_with_host()
    return render_template('homepage.html', posts=posts, user = user)

# ===================== Fetch profile page with post

@app.route('/profile/<int:id>')
def view_profile(id):
    if 'uid' not in session:
        return redirect('/')
    data = {
        'id': session['uid']
    }
    user = User.get_by_id(data)
    posts = Post.get_all_post_with_host()
    return render_template('profile_page.html', posts= posts, user = user, id=id)

# ================= Create a new post

@app.route('/create')
def new_post():
    if 'uid' not in session:
        return redirect('/')
    return render_template('create_post.html')

#===== edited by Juli 
@app.route('/create_post', methods=['POST'])
def create_post():
    if 'uid' not in session:
        return redirect('/')
    if Post.create_post(request.form):
        return redirect('/homepage')
    return redirect('/create')
    
    # data = 
    #     'comment': request.form['comment'],
    #     'book_club': request.form['book_club'],
    #     'date_of_post' : request.form['date_of_post'],
    #     'user_id': session['uid']
    # }
    # return redirect('/profile/<int:id>')

# ===================================Routes for editing

@app.route('/post/edit/<int:id>')
def edit_post(id):
    post = Post.get_by_id(id)
    return render_template('edit_post.html', post=post)

@app.route('/edit/<int:id>', methods=['POST'])
def update_post(id):
    if 'uid' not in session:
        return redirect('/')
    data = {
        'id': id,
        'comment': request.form['comment'],
        'book_club': request.form['book_club'],
        'date': request.form['date']
    }
    if Post.update(data):
        return redirect('/homepage')
    return redirect('/homepage')

# ======================== Route for deleting 

@app.route('/delete/<int:id>')
def delete_post(id):
    Post.delete(id)
    return redirect('/homepage')


#====== route for Photo upload created by Juli 

@app.route('/upload', methods=['POST'])
def upload_photo():
    if 'photoUpload' in request.files:
        photo = request.files['photoUpload']
        if photo.filename != '':
            filename = secure_filename(photo.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            photo.save(file_path)
            return redirect(url_for('view_profile', id=request.form["id"], photo=filename))
    return 'No file uploaded or Error occurred'
