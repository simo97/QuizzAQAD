from django import forms
from django.forms import ModelForm
from core.models import Student, Question, Choice

class AdminProfileForn(forms.Form):
	class Meta:
		model = Student
		fields = ['']


class QuestionForm(ModelForm):
	class Meta:
		model = Question
		fields = ['text','image_link','topic','tags','scheduled_day']




class ChoiceForm(ModelForm):
	class Meta:
		model = Choice
		fields = ['text','is_correct']

