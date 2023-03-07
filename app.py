from flask import Flask, request, render_template, redirect, url_for
from markupsafe import  escape
myapp =  Flask(__name__)  # give flask entry of your application


## 1- create my first route --->
@myapp.route('/')
def helloworld():  # flask add request to the view explicitly
    ## request is implicitly passed to view
    print(request)
    # # get query string arguments  # is not mandatory
    # print(request.args)
    print(request.args.get('name'))

    # I didn't need to make explicit HTTP response object
    return f"<h1 style='color:red'>  Welcome to Our first Flask Application  " \
           f"{escape(request.args.get('name'))}</h1>"


def helloITI():
    return '<h1 style="color:purple">   ITI Home page </h1>'

myapp.add_url_rule('/iti', view_func=helloITI)

############ url parts
@myapp.route('/profile/<name>/<track>/<int:id>')
def profile(name,track, id):
    return f'<h1 style="color:purple">  Welcome to your profile {name} {track} {id} </h1>'

################## make response

@myapp.route('/response')
def test_response():
    response = myapp.make_response("This is simple response ")

    response.status = 201
    print(response)
    return response


@myapp.route('/custom-reponse')
def iti_custom_reponse():
    return "<h1> This my custom response </h1>", 201

#################################### return with templates

@myapp.route('/homepage')
def homepage():
    # return  'template '
    return render_template("homepage.html")


@myapp.route('/home/<username>')
def home(username):
    # return  'template '
    return render_template("home.html", username=username)


################# create page for 404 ###############
@myapp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html')

############# send dict to the template, and endpoints
@myapp.route('/admin', endpoint='adminnn')
def admin_details():
    admin = {
        "name":"noha",
        "track": "Open source",
        "intake": 43
    }
    return render_template('admin.html', admin=admin)
########################### add static files

@myapp.route('/mystaticpage', endpoint='mystaticpage')
def include_static():
    return render_template('includestatic.html')


##################  macros in flask --> macros ---> templates


@myapp.route('/testmacros', endpoint='flask-macros')
def user_macros():
    students= ['Ahmed', 'Ali', 'Mohamed']

    courses = ['python','django', 'flask']

    return render_template('students.html', students= students,courses= courses)

############### connection to databases

#1- install pip install Flask-SQLAlchemy

from flask_sqlalchemy import SQLAlchemy
## add sql-conf to the mt

" http://url of the website/page"
"sqlite:///example.sqlite"
myapp.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
db= SQLAlchemy(myapp)


################### using Models

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email= db.Column(db.String(100),unique=True, nullable=True)
    accepted = db.Column(db.Boolean, default=True)

    def __str__(self):
        return f"{self.name}"


### to apply this changes in the database


@myapp.route('/studnets', endpoint='student_db')
def students_index():
    students = Student.query.all()
    return render_template('students/index.html', students=students)


@myapp.route('/studnets/<id>', endpoint='student_details')
def student_info(id):
    student = Student.query.get_or_404(id)
    return render_template('students/show.html', student=student)



@myapp.route('/studnets/<id>/delete', endpoint='student_delete')
def student_delete(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for("student_db"))
    # return render_template('students/show.html', student=student)





####################################### 1- intro
# print("---------------")
# print(__name__)  #this __name__ refere to the current

"""
    #main function ---> entry point of the application 
    public static void main(){
    }
"""



if __name__=='__main__':
    # myapp.run()
    myapp.run(debug=True)

