from models import app,db,User,Messages
from flask import render_template,redirect,request,url_for,flash,abort
from flask_login import login_user,login_required,logout_user
from forms import LoginForm,RegistrationForm,UsersButtonForm,MessageForm

present_user = None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/<int:user_id>',methods = ['GET','POST'])
def chatting(user_id):
    global present_user
    print(present_user) 
    user = User.query.get_or_404(user_id)
    form = MessageForm()
    if form.validate_on_submit():
        print('hi')
        msg = Messages(form.message.data, present_user.name, user.name)
        db.session.add(msg)
        db.session.commit()
        db.session.refresh(msg)
        # form.submit.data = False
        return render_template('chatting.html',user = user,users = User.query.all(),messages = Messages.query.all(),form = form)
    print('data : ' +str(form.submit.data))
    return render_template('chatting.html',user = user,users = User.query.all(),messages = Messages.query.all(),form = form)

@app.route('/welcome',methods = ['GET','POST'])
@login_required
def welcome_user():
    return render_template('welcome_user.html',users = User.query.all())


@app.route('/logout')
@login_required
def logout():
    global user 
    logout_user()
    flash('You Logged out')
    user = None
    return redirect(url_for('home'))

@app.route('/login',methods = ['GET','POST'])
def login():
    global present_user
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        try:
            if user.check_password(form.password.data) and user is not None:
                login_user(user)
                flash('Logged in Successfully!')
                present_user = user

                next = request.args.get('next')

                if next == None or not next[0] == '/':
                    next = url_for('welcome_user')

                return redirect(next)
        except:
            flash('The Email you entered is not Registered')
            redirect(url_for('login'))
    else:
        flash('Please Enter the Valid Email Id')
    return render_template('login.html',form = form)

@app.route('/register',methods = ['GET','POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        if form.check_email(form.email):
            flash('Email Already Exists You can Login here')
            return redirect(url_for('login'))
        if form.check_phno(form.phno):
            flash('Phone Number Already Exists You can Login here')
            return redirect(url_for('login'))
        user = User(email = form.email.data,name = form.name.data,phno = form.phno.data,password = form.password.data)
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        flash('Thanks for registration')
        return redirect(url_for('login'))
    return render_template('register.html',form = form)

if __name__ == '__main__':
    app.run(debug = True)










# <!--          <button id = {{i.id}} type="button" class="btn btn-primary" name = "{{i.name}}" value = {{i.name}}>{{i.name}}</button>-->