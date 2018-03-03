from django.shortcuts import render, get_object_or_404, reverse
from django.template.loader import render_to_string
from core.models import Student, Question, Choice, NotationHistory,id_generator, Categorie, Comment, Setting
from django.contrib.auth.models import User
# Create your views here. API are here
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Sum
import datetime
import operator
from django.http import Http404
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned
import random
from django.core.mail import EmailMessage

# todo : organize question to be displayed randomly
# todo : add chart in dashboard to allow admin to see question's result
# todo : add question assets like ( like/dislike , topic ...)
# todo : add about page ( front and back end )
# todo : add comment oage ( front only )
# todo : add follow student page
# todo : fix pp upload
# todo : add icons on button
# todo : add a place to edit content of about ( markdown )
# todo : check the leaderboard algorithm
# todo : check question of the month algorithm
# todo : add success message after operations
"""
 To generate the leaderboard we should:
 1) get all the user who has made choice in the current month
 2) put all ther notation history object of the month in a dictionary { 'user' : [sum_of_month_notation]} populating by user's id
 3) sort all the dictionnary for displaying
"""


def handle_upload(req):
	picture = req.FILES['picture']
	fs = FileSystemStorage()
	filename = fs.save(id_generator(20) + "."+picture.name.split('.')[-1], picture)
	return  fs.url(filename)


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


def like_question(req,id):
	q = Question.objects.get(pk=id)
	q.likes += 1
	q.save()
	return HttpResponse(q.likes)


def dislike_question(req,id):
	q = Question.objects.get(pk=id)
	q.dislikes += 1
	q.save()
	return HttpResponse(q.dislikes)


def home(req):
	return render(req, 'core/home.html')


def about(r):
	return render(r, 'core/about.html', {'setting': Setting.objects.get(pk=1)})
	pass


def comment(r):
	if r.method == 'GET':
		return render(r, 'core/comments.html',{'categories': Categorie.objects.all()})
	elif r.method == 'POST':
		Comment.objects.create(
			content=r.POST['content'],
			category=Categorie.objects.get(pk=r.POST['cat_id']),
			studend=r.user.student
		)
		return HttpResponseRedirect(reverse('core:home'))
	pass


def user_is_staff(user):
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
	tags = []
	_random_order = random.sample(range(0, 4), 4)
	"""for tag in question.tags.spit('#'):
		tags.append('#'+tag)"""
	if req.user.is_authenticated:

		if req.user.is_staff:
			return render(req, 'core/vote.html', {
				'question': question,
				'choice_one': list_question[_random_order[0]],
				'choice_two': list_question[_random_order[1]],
				'choice_tree': list_question[_random_order[2]],
				'choice_four': list_question[_random_order[3]],

				'leader_board': leaderboard_generator_v2()[:5],
				'allowed': False,
				'message': "An admin cannot respond to question",
				'link_len': len(question.image_link),
				'tags': tags
			})
		student = req.user.student
		c = NotationHistory.objects.filter(question=question, student=student).count()
		allowed = True if c == 0 else False
		message = '' if c == 0 else 'Your choice has already been saved'
		return render(req, 'core/vote.html', {
			'question': question,
			'choice_one': list_question[_random_order[0]],
			'choice_two': list_question[_random_order[1]],
			'choice_tree': list_question[_random_order[2]],
			'choice_four': list_question[_random_order[3]],
			'leader_board': leaderboard_generator_v2()[:5],
			'allowed': allowed,
			'message': message,
			'link_len': len(question.image_link),
			'tags': tags
		})
	else:
		allowed = False,
		message = 'You need to login to choose an answer'
		return render(req, 'core/vote.html', {
			'question': question,
			'choice_one': list_question[_random_order[0]],
			'choice_two': list_question[_random_order[1]],
			'choice_tree': list_question[_random_order[2]],
			'choice_four': list_question[_random_order[3]],
			'leader_board': leaderboard_generator_v2()[:5],  # the 5 first of the list
			'allowed': allowed,
			'message': message,
			'link_len': len(question.image_link),
			'tags': tags
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
		if u is not None:  # here we know that he is a user
			try:
				s = u.student
				if s._is_active:
					login(request=req, user=u)
					return HttpResponseRedirect(reverse('core:home'))  # to the vote UI
				else:
					return HttpResponseRedirect(reverse('core:signin_view'))  # the student is not yet active
			except ObjectDoesNotExist:  # in this case it is an admin
				login(request=req, user=u)
				return HttpResponseRedirect(reverse('core:dashboard_admin_view'))
		else:
			req.message = 'Credentials incorrect !!!'
			return HttpResponseRedirect(reverse('core:signin_view'))  # to the signin view


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
			login(request=req,user=u)
			return redirect('/')
		else:
			return redirect('/')
	pass


def registration_with_mail(req):
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
		picture_link = ''
		if req.FILES:
			picture = req.FILES['picture']
			fs = FileSystemStorage()
			filename = fs.save(id_generator(20)+"."+picture.name.split('.')[-1], picture)
			picture_link = fs.url(filename)
		else:
			picture_link = ""
		student = Student.objects.create(picture=picture_link,user=user)
		student.save()
		link_url = 'https://'+req.get_host()+reverse('core:validate_account', kwargs={'validation_str': student._validation_str})
		""" send mail here to ask for account validation """
		""" prepate the mail here """
		ctx = {
			'setting': Setting.objects.get(pk=1),
			'url':link_url
		}

		message = render_to_string('core/mail_template.html',ctx)
		#  message.subtype('html')
		msg = EmailMessage('Account activation mail',message,to=[user.email])
		#  user.email_user('Account activation mail',message, from_email='simoadonis@gmail.com')
		msg.content_subtype = "html"
		msg.send()
		return render(req, 'core/validity_mail_sended.html')


def account_activation(req,validation_str):
	try:
		student = Student.objects.get(_validation_str=validation_str)
		student._is_active = True
		student.save()
		user = student.user
		login(req, user)
		return HttpResponseRedirect(reverse('core:home'))
	except MultipleObjectsReturned:
		return render(req, 'core/validation_fail.html', {'reason': 'There is more than one user with this code. Have you shared you code with someone ?'})
	except ObjectDoesNotExist:
		return render(req, 'core/validation_fail.html', {'reason': 'Unable to find student information'})


@login_required
def get_profile(req):
	if req.user.is_staff:
		return HttpResponseRedirect(reverse('core:profile_admin_view'))
	try:
		student = req.user.student
		user = req.user
		return render(req, 'core/profile.html', {
			'student': student,
			'user': user,
			'my_link': req.get_host()+reverse('core:validate_account', kwargs={'validation_str': student._validation_str})
		})
	except ObjectDoesNotExist:
		return render(req, 'core/404.html',)


@login_required
def logout_user(req):
	logout(req)
	return HttpResponseRedirect(reverse('core:home'))


def error(req):
	return render(req,'core/error.html')


def check_exist(request,value):
	return True if request.POST[value] else False


@login_required
def edit_profile(req):
	"""
	:param req:
	:return:
	"""
	#todo-me :verify the form error to be displayed
	student = req.user.student
	user = req.user
	if req.FILES:
		picture = req.FILES['picture']
		fs = FileSystemStorage()
		filename = fs.save(id_generator(20) + "." + picture.name.split('.')[-1], picture)
		student.picture = filename
	if check_exist(req,'first_name'):
		user.first_name = req.POST['first_name']
	if check_exist(req, 'last_name'):
		user.last_name = req.POST['last_name']
	if check_exist(req, 'email'):
		user.email = req.POST['email']
	if check_exist(req, 'username'):
		user.username = req.POST['username']
	if check_exist(req, 'password'):
		if req.POST['password'] != req.POST['re_password']:
			return HttpResponseRedirect(reverse('core:user_profile_view'))
		user.set_password(req.POST['last_name'])
	student.save()
	user.save()
	return HttpResponseRedirect(reverse('core:user_profile_view'))
