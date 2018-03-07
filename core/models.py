from django.db import models
from django.contrib.auth.models import User
import datetime
import string
import random


def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

# Create your models here.


class Question(models.Model):
	text = models.TextField()
	image_link = models.CharField(max_length=255,null=True, blank=True)
	value = models.IntegerField()
	date_creation = models.DateField(auto_now=True)
	year = models.IntegerField()
	month = models.IntegerField()
	topic = models.CharField(max_length=255,null=True)
	tags = models.CharField(max_length=255,null=True)
	scheduled_day = models.DateField(verbose_name="Day of month for the question")
	likes = models.IntegerField(default=0)
	dislikes = models.IntegerField(default=0)

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
	referral_link = models.CharField(editable=False, max_length=100,verbose_name='referral_link',default=id_generator(100))
	picture = models.CharField(max_length=40, null=True)
	referrer_students = models.ManyToManyField('self',related_name='follower')
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	current_score = models.IntegerField(blank=True, null=True,default=0)
	last_year_vote = models.IntegerField(default=datetime.date.today().year)
	last_month_vote = models.IntegerField(default=datetime.date.today().month)
	_is_active = models.BooleanField(default=False)
	_validation_str = models.CharField(editable=False, max_length=100, verbose_name='Validation string', default=id_generator(100))

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


class Setting(models.Model):
	about = models.TextField(null=True, default='About')
	footer_left = models.TextField(null=True, default='left content')
	footer_center=models.TextField(null=True, default='center content')
	footer_right = models.TextField(null=True, default='right content')
	mail = models.TextField(null=True, default='Mail template')