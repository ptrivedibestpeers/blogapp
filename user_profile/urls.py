from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^$', views.home, name = 'home'),
    url(r'^profile/$', views.profile, name = 'profile'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name = 'user_profile/login.html'), name = 'login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name = 'logout'),
    url(r'^blogAPP/$',views.blogAPP,name = 'blogAPP'),
    url(r'^signup/$',views.signup, name = 'signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    	views.activate,name = 'activate'),
    url(r'^resetpassword/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    	views.PasswordResetConfirmView.as_view(),name = 'reset_password'),
    url(r'^forgotPassword/$',views.forgotPassword,name = 'forgot_password'),
    url(r'^resendAccActivation/$',views.resendAccActivation,name = 'Resend_Acc_activation'),
    url(r'^show_user_post/$',views.show_user_post,name = 'show_user_post'),
    url(r'^new_post/$',views.new_post,name = 'new_post'),
    url(r'^(?P<blog_id>[0-9]+)/view_blog/$',views.view_blog,name = 'view_blog'),
    url(r'^(?P<blog_id>[0-9]+)/edit_blog/$',views.edit_blog,name = 'edit_blog'),
    url(r'^(?P<blog_id>[0-9]+)/delete_blog/$',views.delete_blog,name = 'delete_blog'),
    url(r'^like/$',views.like_blog,name = 'like'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
