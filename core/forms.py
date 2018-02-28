from django import forms
from core.models import Student

class AdminProfileForn(forms.Form):
	class Meta:
		model = Student
		fields = ['']