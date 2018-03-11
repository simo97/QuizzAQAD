from django.core.mail import EmailMessage
from django.conf import settings
from core.models import Setting, Student
from allauth.account.adapter import DefaultAccountAdapter


class AcountCustomProvider(DefaultAccountAdapter):

	def send_mail(self, template_prefix, email, context):
		context.update({'setting': Setting.objects.get(pk=1)})
		print(context)
		msg = self.render_mail(template_prefix=template_prefix,email=email,context=context)
		msg.send()

	def save_user(self, request, user, form, commit=True):
		"""Saves a new `User` instance using information provided in the
		   signup form.
		"""
		from allauth.account.utils import user_username, user_email, user_field
		def_student = Student()

		data = form.cleaned_data
		first_name = data.get('first_name')
		last_name = data.get('last_name')
		email = data.get('email')
		username = data.get('username')
		user_email(user, email)
		user_username(user, username)
		if first_name:
			user_field(user, 'first_name', first_name)
		if last_name:
			user_field(user, 'last_name', last_name)
		if 'password1' in data:
			user.set_password(data["password1"])
		else:
			user.set_unusable_password()
		self.populate_username(request, user)
		if commit:
			# Ability not to commit makes it easier to derive from
			# this adapter by adding
			user.save()
			def_student.user = user
			def_student.save()  # save a null student here related to registered user
		return user

