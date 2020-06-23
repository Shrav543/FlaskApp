from flaskblog.models import User, Post
from flask import render_template, url_for, flash, redirect , request , abort
from flaskblog.forms import RegistrationForm, LoginForm , PostForm
from flaskblog import app,db,bcrypt
from flask_login import login_user,current_user,logout_user,login_required


"""This means that both of these routes /home and / will be served by home function"""
@app.route("/home")
@app.route("/")
def home():
""" here we are extracting all the objects from post model and rendering them to home.html"""
	posts= Post.query.all()
	return render_template('home.html',posts=posts)

@app.route("/about")
def about():
	return render_template('about.html', title='About')

"""We must put the allowed methods otherwise while submitting there would be an error
This route will allow both GET and POST"""
@app.route("/register", methods=['GET','POST'])
def register():
"""if the user is currently logged in he should not be able to see the login or register page through url"""

	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		# this is a one time msg that we can use importing from flask flash, it also excepts other args like success
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username = form.username.data, email=form.email.data, password = hashed_password)
		db.session.add(user)
		db.session.commit()	
		flash(f'Account created for {form.username.data}', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register',form=form)


@app.route("/login",methods=['GET','POST'])
def login():
    """if the user is currently logged in he should not be able to see the login or register page through url"""
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()

	if form.validate_on_submit():

		user= User.query.filter_by(email=form.email.data).first()

		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			if next_page:
				return redirect(next_page)
			else:
				return redirect(url_for('home'))
		else:
			flash(f'Please check your credentials', 'danger')
	
	return render_template('login.html', title='Login',form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))



@app.route("/account")
@login_required
def account():	
	return render_template('account.html', title='Account')


@app.route("/post/new", methods=['GET','POST'])
@login_required
def new_post():	
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title=form.title.data, content=form.content.data , author=current_user)
		db.session.add(post)
		db.session.commit()
		flash(f'Your post has been created', 'success')
		return redirect(url_for('home'))
	return render_template('create_post.html', title='New Post',form=form, legend='New Post')




@app.route("/post/<int:post_id>")
#@login_required
def post(post_id):
	#post = Post.query.get(post_id)
	post = Post.query.get_or_404(post_id)
	return render_template('post.html',title=post.title,post=post)


@app.route("/post/<int:post_id>/update",methods=['GET','POST'])
@login_required
def update_post(post_id):
	#post = Post.query.get(post_id)
	post = Post.query.get_or_404(post_id)
	if post.author == current_user:
		form = PostForm()
		if form.validate_on_submit():
			post.title = form.title.data
			post.content = form.content.data
			db.session.commit()
			flash("Your post has been updated!","success")
			return redirect(url_for('post', post_id=post.id))

		elif request.method =='GET':
			form.title.data = post.title
			form.content.data = post.content
		return render_template('create_post.html', title='Update Post',form=form,legend='Update Post')
	else:
		abort(403)


@app.route("/post/<int:post_id>/delete",methods=['POST'])
#@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash("Your post has been deleted!","success")
	return redirect(url_for('home'))

