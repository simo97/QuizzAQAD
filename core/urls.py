from django.conf.urls import url

from . import admin_views, views


app_name = 'core'

urlpatterns = [
	url(r'^$',views.ask, name='home'),
	url(r'^choose/$', views.choose, name='choose'),
	url(r'^home/$', views.home, name='login_user'),
	url(r'^profile/$', views.profile, name='user_profile_view'),
	url(r'^login/$', views.siginn, name='signin_view'),
	url(r'^registration/$', views.register, name='register_view'),
	url(r'^error/$',views.error, name='error_view'),
	url(r'^dashboard/$', admin_views.dashboard, name='dashboard_admin_view'),
	url(r'^dashboard/questions/$', admin_views.questions, name='questions_admin_view'),
	url(r'^dashboard/questions/detail/$', admin_views.detail_question, name='question_detail_view'),
	url(r'^dashboard/questions/upload/$', admin_views.upload, name='questions_admin_upload_view'),
	url(r'^dashboard/categories/$', admin_views.categories, name='categories_admin_view'),
	url(r'^dashboard/categories/add/$', admin_views.add_categorie, name='categories_add_admin_view'),
	url(r'^dashboard/comments/$', admin_views.comments, name='comments_admin_view'),
	url(r'^dashboard/students/$', admin_views.students, name='students_admin_view'),
	url(r'^dashboard/profile/$', admin_views.dash_profile, name='profile_admin_view')
]