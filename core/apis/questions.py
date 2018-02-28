from core.models import Question
import datetime


def openleaderboard(r,month_id):
	pass


def respond(r, question_id):
	pass


def current_question(r):
	q = Question.objects.get(scheduled_day=datetime.date.today()) # the schedule to pass this day
	res = {
		'question': q.c
	}
	pass
