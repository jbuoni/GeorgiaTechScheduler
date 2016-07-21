from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required
from . import main
from ..model.user import User
from ..model.student import Student
from .auth_form import LoginForm
from ..api import crossDomain
from ..controller import studentController, adminController, userController


@main.route('/', methods=['GET', 'POST'])
@crossDomain.crossdomain('*')
def index():
    form = LoginForm()
    if form.validate_on_submit():
        if User.is_user(form.username.data):
            user = User(form.username.data)
            print user
            if user is not None and user.verify_password(form.password.data):
                login_user(user, form.remember_me.data)

                if user.is_admin(form.username.data) or user.is_developer(form.username.data):
                    return redirect(request.args.get('next') or url_for('.adminInfo', username=form.username.data))
                else:
                    return redirect(request.args.get('next') or url_for('.studentInfo', username=form.username.data))

        flash('Invalid username or password.')
    return render_template('login.html', form=form, authData=None)


@main.route('/logout')
@login_required
@crossDomain.crossdomain('*')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

########## User Pages ##########


@main.route('/user/<username>')
@login_required
def studentInfo(username):
    return render_template('/student/index.html',
                           authData=userController.get_auth_data(username),
                           data=studentController.get_student_info(username))


@main.route('/user/<username>/dashboard')
@login_required
def studentDashboard(username):
    return render_template('/student/student_dashboard.html',
                           authData=userController.get_auth_data(username),
                           data=studentController.get_student_info(username))


@main.route('/course_data/<username>')
@login_required
def aggregateCourseData(username):

    return render_template('/admin/aggregate_course_data.html',
                           authData=userController.get_auth_data(username),
                           data=adminController.get_course_aggregate_data())


@main.route('/<username>/student/<student_id>')
@login_required
def individualStudentData(username, student_id):
    data = Student.get_info(student_id)
    return render_template('admin/student_data.html',
                           authData=userController.get_auth_data(username),
                           data=data)


########## Admin Pages ##########

@main.route('/student_list/<username>')
@login_required
def studentList(username):
    data = adminController.get_student_list()

    return render_template('admin/student_list.html',
                           authData=userController.get_auth_data(username),
                           data=data)


@main.route('/scheduler/<username>')
@login_required
def schedulerView(username):
    data = adminController.get_schedule_data()

    return render_template('admin/schedule.html',
                           authData=userController.get_auth_data(username),
                           data=data)


@main.route('/solution_view/<solution_id>')
@login_required
def solutionView(solution_id):
    pass


@main.route('/new_schedule')
@login_required
def newSchedule():
    pass


@main.route('/new_solution')
@login_required
def newSolution():
    pass


@main.route('/admin_info/<username>')
@login_required
def adminInfo(username):
    data = adminController.get_questions_list()
    return render_template('admin/admin_dashboard.html',
                           authData=userController.get_auth_data(username),
                           data=data)

