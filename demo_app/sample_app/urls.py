from django.urls import path
from . import views

urlpatterns = [
    path('', views.SampleTemplateView.as_view(), name='home'),
    path('welcome/', views.WelcomeTemplateView.as_view(), name='welcome'),
    path('social/signup/', views.signup_redirect, name='signup_redirect'),
    path('add-salary', views.SalaryUpdateView.as_view(), name='salary-details'),
    path('list-employees', views.EmployeeListView.as_view(), name='employees'),
    path('get-employee/<slug:slug>', views.EmployeeDetailsView.as_view(), name='get-employee'),
    path('update-employee/<slug:slug>', views.EmployeeDetailsUpdateView.as_view(), name='update-employee'),
    path('delete-employee/<slug:slug>', views.EmployeeDeleteView.as_view(), name='delete-employee'),
]