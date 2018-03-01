from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from core.models import *
from django.http import HttpResponseRedirect
from django.urls import reverse
import csv
import codecs
from core import question_creator as qc


def leaderboard_generator_v2():
	"""
	This second version will extract all the Student and sort them according to their score
	:return:
	"""
	return Student.objects.filter(last_month_vote=datetime.date.today().month, last_year_vote=datetime.date.today().year).order_by('-current_score')


@login_required
def dashboard(request):
	"""
	To see the leaderboard
	:param request:
	:return:
	"""
	#lead_board =
	return render(request, 'core/admin/dashboard.html',{
		'leader_board': leaderboard_generator_v2()
	})


@login_required
def questions(request):
	return render(request, 'core/admin/questions.html',{
		'list_questions': Question.objects.all().order_by('-id')
	})


@login_required
def students(req):
	return render(req, 'core/admin/students.html',{
		'list_students': Student.objects.all()
	})


@login_required
def comments(req):
	return render(req, 'core/admin/comments.html',{
		'list_comments': Comment.objects.all()
	})


@login_required
def categories(req):
	return render(req, 'core/admin/categories.html',{
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
		res = qc.proceed()  # read the question data here to parsing
		if res:
			return HttpResponseRedirect(reverse('core:questions_admin_view'))
		else:
			return render(req, 'core/admin/questions.html',{
				'data_error': "Unable to upload question"
			})
	else:
		return HttpResponseRedirect(reverse('core:dashboard_admin_view'))


@login_required
def detail_question(req):
	q = get_object_or_404(Question, pk= req.GET['question_id'] if req.GET['question_id'] else 13)
	l = q.choicies.all()
	return render(req, 'core/admin/detail_question.html', {
		'question': q,
		'choices': l,
		'choice_Val_1': NotationHistory.objects.filter(choice=l[0]).count(),
		'choice_Val_2': NotationHistory.objects.filter(choice=l[1]).count(),
		'choice_Val_3': NotationHistory.objects.filter(choice=l[2]).count(),
		'choice_Val_4': NotationHistory.objects.filter(choice=l[3]).count(),
	})


@login_required
def dash_profile(req):
	return  render(req,'core/admin/profile.html')


@login_required
def download_leaderboard_csv(req):
	pass
