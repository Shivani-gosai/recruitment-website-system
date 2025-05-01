"""
URL configuration for project1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from myapp import views 

app_name="myapp"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.firstpage, name='firstpage'),
    path('login/', views.login,name='login'),
    path('business/', views.business_info,name='business_info'),
    path('get-cities/', views.get_cities, name='get_cities'),
    path("dashboard/", views.dashboard, name="dashboard"),
    path('accounts/',views.accounts),
    path('homepage/',views.homepage,name='homepage'),
    path('toggle_like_member/<int:post_id>/', views.toggle_like_member, name='toggle_like_member'),
    path('comment_member/<int:post_id>/', views.add_comment_member, name='add_comment_member'),
    path('hiring_view/<int:job_id>/', views.hiring_view, name='hiring_view'),
    path('jobs/',views.jobs,name='jobs'),
    path('jobseeker/',views.jobseeker),
    path('agency/',views.agency_info),
    path('cv/',views.add_cv,name='add_cv'),
    path('profile/', views.new_profile_view, name='new_profile_view'),
    path('logout/', views.logout_view, name='logout'),
    path('cv_success',views.cv_success,name='cv_seccess'),
    path('delete_education/<int:edu_id>/', views.delete_education, name='delete_education'),
    path('delete_summary/<int:summary_id>/', views.delete_summary, name='delete_summary'),
    path('delete_skill/<int:skill_id>/', views.delete_skill, name='delete_skill'),
    path('delete_experience/<int:exp_id>/', views.delete_experience, name='delete_experience'),
    path('delete_language/<int:lang_id>/', views.delete_language, name='delete_language'),
    path('delete_link/<int:link_id>/', views.delete_link, name='delete_link'),
    path('create_post/', views.create_post_jobseeker, name='create_post'),
    path("see_all_posts/", views.see_all_posts, name="see_all_posts"),
    path('joblist/<int:org_id>/', views.list_job, name='list_job'),
    #path('cmphome/', views.cmphome, name='cmphome'),
    path('cmphome/<int:org_id>/', views.cmphome, name='cmphome'),
    path('cmpabout/<int:org_id>/', views.cmpabout, name='cmpabout'),
    path('cmppost/<int:org_id>/', views.cmppost, name='cmppost'),
    path('toggle_like/<int:post_id>/', views.toggle_like, name='toggle_like'),
    path('cmpjob/<int:org_id>/', views.cmpjob, name='cmpjob'),
    path('organization/<int:org_id>/job/<int:job_id>/delete/', views.delete_job, name='delete_job'),
    path('apply_job/<int:jobid>/', views.apply_job, name='apply_job'),
    path('view_details/<int:job_id>/', views.view_details, name='view_details'),
    path('applied_jobs/', views.applied_jobs_view, name='applied_jobs'),
    path('addjob/<int:org_id>/', views.create_job, name='create_job'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('follow/<int:org_id>/', views.toggle_follow, name='toggle_follow'),
    #path("cmpabout/", views.cmpabout, name="cmpabout"),
    path('update_org_details/<int:org_id>/', views.update_org_details, name='update_org_details'),
    #path('cmppost/',views.cmppost,name='cmppost'),
    path('create_post_business/<int:org_id>/',views.create_post_business,name='create_post_business'),
    path("get_posts/", views.get_posts, name="get_posts"),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path("add_comment/<int:post_id>/", views.add_comment, name="add_comment"),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('member/<int:id>/', views.member_profile, name='member_profile'),
    path('job_card/', views.job_card, name='job_card'),
    path("user/<int:login_id>/", views.user_profile, name="user_profile"),
    path("user/<int:login_id>/about/", views.user_about, name="user_about"),
    path('user/<int:login_id>/posts/', views.user_posts, name='user_posts'),
    path('user/<int:login_id>/jobs/', views.user_jobs, name='user_jobs'),
    path('member/<int:login_id>/profile/', views.jobseeker_profile, name='jobseeker_profile'),
    path('agency_homepage/', views.agency_homepage, name='agency_homepage'),
    path('agency_jobs/', views.agency_jobs, name='agency_jobs'),
    path("agency/duplicate_jobs/", views.duplicate_jobs_to_agency, name="duplicate_jobs_to_agency"),
    path("agency/update_info/", views.update_agency_info, name="update_agency_info"),
    path('public_agency/<int:agency_id>/', views.public_agency_profile, name='public_agency_profile'),
    path('public_agency/<int:agency_id>/jobs/', views.public_agency_jobs, name='public_agency_jobs'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)