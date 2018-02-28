from django.shortcuts import render, get_object_or_404, reverse
from core.models import Student, Question, Choice, NotationHistory
from django.contrib.auth.models import User
# Create your views here. API are here
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.db.models import Sum
import datetime
import operator
from django.http import Http404


"""
 To generate the leaderboard we should:
 1) get all the user who has made choice in the current month
 2) put all ther notation history object of the month in a dictionary { 'user' : [sum_of_month_notation]} populating by user's id
 3) sort all the dictionnary for displaying
"""


def generate_leaderbard():
	"""getting all the user of the month """
	students = Student.objects.filter(last_month_vote=datetime.date.today().month, last_year_vote=datetime.date.today().year)
	if students.count() <= 0:
		return {
			'status':False,
			'message': 'No data available for this month'
		}
	else:
		notation_data = {}
		for student in students:
			sum_stud = NotationHistory.objects.filter(student=student).aggregate(Sum('notation'))
			notation_data.append({
				student.id: sum_stud
			})
			""" herer all the data should be populated now let sort them """
		sorted_x = sorted(notation_data.items(), key=operator.itemgetter(1),reverse=True)


def leaderboard_generator_v2():
	"""
	This second version will extract all the Student and sort them according to their score
	:return:
	"""
	return Student.objects.filter(last_month_vote=datetime.date.today().month, last_year_vote=datetime.date.today().year).order_by('-current_score')


def home(req):
	return render(req, 'core/home.html')


def about(r):
	pass


def comment(r):
	pass


def ask(req):
	"""" must load the question of the day. The question that has been schedule for today """
	try:
		question = get_object_or_404(Question, scheduled_day=datetime.date.today())
		list_question = get_object_or_404(Question, scheduled_day=datetime.date.today()).choicies.all()
	except Http404:
		return render(req, 'core/vote.html')
	""" verify if the current user always has choose """
	#  if req.user.student is not None else False
	if req.user.is_authenticated:
		student = req.user.student
		c = NotationHistory.objects.filter(question=question, student=student).count()
		allowed = True if c == 0 else False
		message = '' if c == 0 else 'Your choice has already been saved'
		return render(req, 'core/vote.html', {
			'question': question,
			'choice_one': list_question[0],
			'choice_two': list_question[1],
			'choice_tree': list_question[2],
			'choice_four': list_question[3],
			'leader_board': leaderboard_generator_v2()[:5],
			'allowed': allowed,
			'message': message
		})
	else:
		allowed = False,
		message = 'You need to login to choose an answer'
		return render(req, 'core/vote.html', {
			'question': question,
			'choice_one': list_question[0],
			'choice_two': list_question[1],
			'choice_tree': list_question[2],
			'choice_four': list_question[3],
			'leader_board': leaderboard_generator_v2()[:5],  # the 5 first of the list
			'allowed': allowed,
			'message': message
		})


@login_required
def choose(req):
	question = get_object_or_404(Question, pk=int(req.POST['question_id']))
	choice = get_object_or_404(Choice, pk=int(req.POST['choice']))
	user = req.user
	value = 5 if choice.is_correct is True else 0
	notation = NotationHistory.objects.create(question=question, choice=choice, notation=value, student=user.student)
	if notation is not None:
		""" consider that the user had choose , now update the current user's score """
		stud = user.student
		stud.current_score = stud.current_score + notation.notation  # add the score of notation to the current score
		stud.last_month_vote = datetime.date.today().month # save the last month and year of choosing by the user
		stud.last_year_vote = datetime.date.today().year
		stud.save()  # persist all here
		return HttpResponseRedirect(reverse('core:home'))
	else:
		return HttpResponseRedirect(reverse('core:error_view'))


def siginn(req):
	if req.method == 'GET':
		return render(req,'core/signin.html')
	else:
		u = authenticate(username=req.POST['username'], password=req.POST['password'])
		if u is not None:
			login(request=req,user=u)
			return HttpResponseRedirect(reverse('core:home'))  # to the vote UI
		else:
			req.message = 'Credentials incorrect !!!'
			return redirect(reverse('core:signin_view'))  # to the signin view


def profile(req):
	return render(req, 'core/profile.html')


def register(req):
	if req.method == "GET":
		return render(req, 'core/register.html')
	else:
		user = User.objects.create_user(
			username=req.POST['username'],
			email=req.POST['email'],
			password=req.POST['password'],
			first_name=req.POST['first_name'],
			last_name=req.POST['last_name']
		)
		user.save()
		student = Student.objects.create(picture='test',user=user)
		student.save()
		u = authenticate(username=req.POST['username'],password=req.POST['password'])
		if u is not None:
			login(user=u)
			return redirect('/')
		else:
			return redirect('/')
	pass


@login_required
def logout_user(req):
	logout(req)
	return HttpResponseRedirect(reverse('core:home'))


def error(req):
	return render(req,'core/error.html')