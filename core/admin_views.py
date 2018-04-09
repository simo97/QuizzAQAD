from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from core.models import *
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from core import question_creator as qc
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from core.forms import QuestionForm, ChoiceForm
import csv
import datetime

def leaderboard_generator_v2():
	"""
	This second version will extract all the Student and sort them according to their score
	:return:
	"""
	return Student.objects.filter(last_month_vote=datetime.date.today().month,
								  last_year_vote=datetime.date.today().year).order_by('-current_score')


@login_required
def dashboard(request):
	"""
	To see the leaderboard
	:param request:
	:return:
	"""
	# lead_board =
	return render(request, 'core/admin/dashboard.html', {
		'leader_board': leaderboard_generator_v2()
	})


@login_required
def questions(request):
	question_list = Question.objects.all().order_by('id')
	page = request.GET.get('page', 1)
	paginator = Paginator(question_list, 15)

	try:
		question_to_deliv = paginator.page(page)
	except PageNotAnInteger:
		question_to_deliv = paginator.page(1)
	except EmptyPage:
		question_to_deliv = paginator.page(paginator.num_pages)

	return render(request, 'core/admin/questions.html', {
		'list_questions': question_to_deliv
	})


@login_required
def students(request):
	student_list = Student.objects.all()
	page = request.GET.get('page', 1)
	paginator = Paginator(student_list, 10)

	try:
		student_list = paginator.page(page)
	except PageNotAnInteger:
		student_list = paginator.page(1)
	except EmptyPage:
		student_list = paginator.page(paginator.num_pages)

	return render(request, 'core/admin/students.html', {
		'list_students': student_list
	})


@login_required
def comments(req):
	return render(req, 'core/admin/comments.html', {
		'list_comments': Comment.objects.all()
	})


@login_required
def categories(req):
	return render(req, 'core/admin/categories.html', {
		'list_categories': Categorie.objects.all()
	})


@login_required
def add_categorie(request):
	c = Categorie()
	c.name = request.POST['name']
	c.save()
	return HttpResponseRedirect(reverse('core:categories_admin_view'))


def handle_uploaded_file(f):
	with open('upload.csv', 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)


@login_required
def upload(req):
	print(req.method)
	if req.POST and req.FILES:
		handle_uploaded_file(req.FILES['question_file'])
		try:
			res = qc.proceed()  # read the question data here to parsing
			if res:
				return HttpResponseRedirect(reverse('core:questions_admin_view'))
			else:
				return render(req, 'core/admin/questions.html', {
					'data_error': "Unable to upload question",
					'list_questions': Question.objects.all().order_by('-id')
				})
		except IndexError:
			return render(req, 'core/admin/questions.html', {
				'data_error': "Index error check the number of column in your csv file, it should be 9.",
				'list_questions': Question.objects.all().order_by('-id')
			})

	else:
		return HttpResponseRedirect(reverse('core:dashboard_admin_view'))


@login_required
def detail_question(req):
	q = get_object_or_404(Question, pk=req.GET['question_id'] if req.GET['question_id'] else 13)
	l = q.choicies.all()
	return render(req, 'core/admin/question_detail.html', {
		'question': q,
		'choices': l,
		'choice_Val_1': NotationHistory.objects.filter(choice=l[0]).count(),
		'choice_Val_2': NotationHistory.objects.filter(choice=l[1]).count(),
		'choice_Val_3': NotationHistory.objects.filter(choice=l[2]).count(),
		'choice_Val_4': NotationHistory.objects.filter(choice=l[3]).count(),
	})


@login_required
def dash_profile(req):
	return render(req, 'core/admin/profile.html')


@login_required
def download_leaderboard_csv(req):
	pass


@login_required
def edit_about(req):
	return render(req, 'core/admin/about.html', {'setting': Setting.objects.get(pk=1)})


@login_required
def edit_setting(req, sett):
	setting = Setting.objects.get(pk=1)
	if str(sett) == 'about':
		setting.about = req.POST['about']
	if str(sett) == 'center':
		setting.footer_center = req.POST['center']
	if str(sett) == 'left':
		setting.footer_left = req.POST['left']
	if str(sett) == 'right':
		setting.footer_right = req.POST['right']
	if str(sett) == 'mail':
		setting.mail = req.POST['mail']
	if str(sett) == 'comment':
		setting.comments = req.POST['comment']
	setting.save()
	return render(req, 'core/admin/about.html', {'setting': setting})


@login_required
def edit_question(request):
	if request.method == 'GET':
		q = Question.objects.get(pk=request.GET['question'])
		q_form = QuestionForm(instance=q)
		return render(request, 'core/admin/edit_question.html', {'form': q_form, 'id': q.id})
	form = QuestionForm(request.POST)
	if form.is_valid():
		q = Question.objects.get(pk=request.GET['question'])
		q.text = form.cleaned_data['text']
		q.image_link = form.cleaned_data['image_link']
		q.scheduled_day = form.cleaned_data['scheduled_day']
		q.topic = form.cleaned_data['topic']
		q.tags = form.cleaned_data['tags']
		q.save()
		return HttpResponseRedirect(reverse('core:questions_admin_view'))
	return HttpResponseRedirect(reverse('core:questions_admin_view'))


@login_required
def edit_choice(request):
	if request.method == "GET":
		choice = Choice.objects.get(pk=request.GET['choice_id'])
		form = ChoiceForm(instance=choice)
		return render(request, 'core/admin/edit_choice.html', {'id': choice.id, 'form': form})
	form = ChoiceForm(request.POST)
	if form.is_valid():
		choice = Choice.objects.get(pk=request.GET['choice_id'])  # le choix ici
		choice.text = form.cleaned_data['text']
		choice.is_correct = form.cleaned_data['is_correct']
		if form.cleaned_data['is_correct'] == True:  # check if the question has bee set as the good choice
			c = Choice.objects.get(is_correct=True, question=choice.question)
			c.is_correct = False
			c.save()
		choice.save()
		return HttpResponseRedirect(reverse('core:questions_admin_view'))
	return HttpResponseRedirect(reverse('core:questions_admin_view'))


@login_required
def export_user(request, id):
	#student = Student.objects.get(pk=id)  # the current student
	student = Student.objects.get(pk=id)
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachement; filename="'+student.user.username+' ['+str(datetime.date.today())+'].csv"'
	writer = csv.writer(response)
	writer.writerow([
		'First name','Last name',
		'Username','Email',
		'Current Score',
		'Last login', 'Registration date'
	])
	writer.writerow([
		student.user.first_name,
		student.user.last_name,
		student.user.username,
		student.user.email,
		student.current_score,
		student.user.last_login,
		student.user.date_joined
	])
	return response


@login_required
def export_users(request):
	students = Student.objects.all()
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachement; filename="students ['+ str(datetime.date.today()) +'].csv"'
	writer = csv.writer(response)
	writer.writerow([
		'First name', 'Last name',
		'Username', 'Email',
		'Current Score',
		'Last login', 'Registration date'
	])
	for student in students:
		writer.writerow([
			student.user.first_name,
			student.user.last_name,
			student.user.username,
			student.user.email,
			student.current_score,
			student.user.last_login,
			student.user.date_joined
		])
	return response