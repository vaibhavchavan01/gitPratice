import email
from unicodedata import name
from django.contrib.auth import login, views as auth_views
from django.urls import path
from . import views

# from django.views.generic import TemplateView
app_name = 'demoApp'

urlpatterns = [
    path('',views.HomepageView.as_view(),name='home'),
    path('signup1/',views.SignUpView.getUser,name='signup1'),
    path('login/',auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('login1/',views.LoginCheckView.check_login,name= 'login1'),
    path('index/',views.AfterLoginView.as_view(), name='index'),
    path('signup/',views.SignUpView.as_view(),name='signup'),
    path('forgetPassword/',views.ForgetPasswordView.as_view(), name = 'forgetPassword'),
    path('getlink/',views.ForgetPasswordView.get_link,name='getlink'),
    path('resetpassword/',views.ResetPasswordView.after_reset_Password,name='resetpassword'),
    path('DetailPage/<int:id>/',views.GetDetail,name="detail"),
    path('resetPasswordLink/<token>/<email>',views.ResetPasswordView.resetPassord, name ='resetPasswordLink'),
    path('logout/',views.Logout,name="logout"),
    path('addDetails/',views.AddDetailsView.add_details, name='addDetails'),
    path('addDetailsPage/',views.AddDetailsView.as_view(), name='addDetailsPage'),
    path('delete/<int:id>/',views.delete_record, name = 'delete'),
    path('edit/<int:id>/',views.edit_record, name = 'edit'),
    path('update/<int:ma_id>/<int:m_id>/<int:a_id>/<int:g_id>/',views.update_record, name = 'updateDetails')
    
]