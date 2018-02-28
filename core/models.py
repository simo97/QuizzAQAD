from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.


class Question(models.Model):
	text = models.CharField(max_length=255)
	image_link = models.CharField(max_length=255)
	value = models.IntegerField()
	date_creation = models.DateField(auto_now=True)
	year = models.IntegerField()
	month = models.IntegerField()
	topic = models.CharField(max_length=255)
	tags = models.CharField(max_length=255)
	scheduled_day = models.DateField(verbose_name="Day of month for the question")

	def __str__(self):
		return self.text


class Choice(models.Model):
	text = models.CharField(max_length=255)
	is_correct = models.BooleanField(default=False)
	date_creation = models.DateField(auto_now=True)
	question = models.ForeignKey(Question, null=True,on_delete=models.CASCADE, related_name='choicies')

	def __str__(self):
		return self.text


class Student(models.Model):
	referral_link = models.UUIDField(editable=False, verbose_name='referral_link',null=True)
	picture = models.CharField(max_length=40, null=True)
	referrer_students = models.ForeignKey('self', on_delete=models.DO_NOTHING,null=True)
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	current_score = models.IntegerField(blank=True, null=True,default=0)
	last_year_vote = models.IntegerField(default=datetime.date.today().year)
	last_month_vote = models.IntegerField(default=datetime.date.today().month)

	def __str__(self):
		return self.user.first_name


class Month(models.Model):
	month = models.CharField(max_length=20)
	year = models.IntegerField()

	def __str__(self):
		return self.month + ' : '+ self.year
	pass


class NotationHistory(models.Model):
	student= models.ForeignKey(Student,on_delete=models.CASCADE,related_name='score')
	notation = models.IntegerField()
	choice = models.ForeignKey(Choice, null=True, on_delete=models.CASCADE, related_name='notations')
	question = models.ForeignKey(Question, null=True, on_delete=models.CASCADE, related_name='notations')
	date = models.DateField(auto_now=True)
	month = models.IntegerField(default=datetime.date.today().month)
	year = models.IntegerField(default=datetime.date.today().year)

	def __str__(self):
		return str(self.notation)


class Categorie(models.Model):
	name = models.CharField(max_length=20)

	def __str__(self):
		return self.name


class Comment(models.Model):
	content = models.CharField(max_length=255)
	date_publish = models.DateTimeField(auto_now=True)
	studend = models.ForeignKey(Student,on_delete=models.CASCADE, related_name='comments')
	category = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='categorie')

	def __str__(self):
		return self.content
	pass