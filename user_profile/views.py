from django.shortcuts import render,redirect
from .models import Profile_detail,Blog,Like
from .forms import SignUpForm,SetPasswordForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.http import HttpResponse
from .tokens import account_activation_token,forgot_password_token
from django.views.generic.edit import FormView
from django.contrib import messages
from django.http import JsonResponse
# Create your views here.


@login_required
def profile(request):
	if request.method == 'POST':
		profile = Profile_detail.objects.get(username = request.user)
		profile.DOB = request.POST['Dob']
		profile.address = request.POST['address']
		profile.save()
		return HttpResponse('your data has been saved')
	else:
		profile = Profile_detail.objects.get(username = request.user)
		return render(request,'user_profile/edit_profile.html',{'Profile' : profile})


def home(request):
	return render(request,'user_profile/home.html')


def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save(commit = False)
			user.is_active = False
			user.save()
			current_site = get_current_site(request)
			mail_subject = 'Activate your blog account.'
			message = render_to_string('acc_active.html', {
				'user': user,
				'domain': current_site.domain,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)),
				'token': account_activation_token.make_token(user),
				})
			to_email = form.cleaned_data.get('email')
			email = EmailMessage(mail_subject,message,to = [to_email])
			email.send()
			return HttpResponse('A account confirmation mail is sent to your email address please click on the link')          
	else :
		form = SignUpForm()
	return render(request,'user_profile/signup.html',{'form': form})


@login_required
def blogAPP(request):
	blog = Blog.objects.order_by('create_date')
	return render(request,'user_profile/blogAPP.html',{'username':request.user,'blog' : blog})

@login_required
def new_post(request):
	if request.method == 'POST' :
		user = User.objects.get(username = request.user)
		blog = Blog(title = request.POST['title'],
			Description = request.POST['description'],
			publisher = user
			)
		blog.save()
		return HttpResponse("Your blog is posted")
	else:
		return render(request,'user_profile/new_post.html')


@login_required
def show_user_post(request):
	user = User.objects.get(username = request.user)
	blog = user.blogs.all()
	return render(request,'user_profile/show_user_post.html',{'blog' : blog})		


@login_required
def view_blog(request,blog_id):
	blog = Blog.objects.get(id = blog_id)
	user = User.objects.get(username = request.user)
	try:
		like =Like.objects.get(user = user, blog = blog)
	except Like.DoesNotExist:
		return render(request,'user_profile/view_user_post.html',{'blog' : blog,'like_bool':"Like"})
	else:
		return render(request,'user_profile/view_user_post.html',{'blog' : blog,'like_bool':"Unlike"})


@login_required
def delete_blog(request,blog_id):
	Blog.objects.get(id = blog_id).delete()
	return redirect('show_user_post')


@login_required
def edit_blog(request,blog_id):
	if request.method == 'POST' :
		blog = Blog.objects.get(id = blog_id)
		blog.title = request.POST['title']
		blog.Description = request.POST['description']
		blog.save()
		return HttpResponse("Your blog is posted")
	else:
		blog = Blog.objects.get(id = blog_id)
		return render(request,'user_profile/edit_user_post.html',{'blog' : blog})


@login_required
def	like_blog(request):
	if request.method=='POST' :
		try:
			blog = Blog.objects.get(id = request.POST['blog_id'])
			user = User.objects.get(username = request.user)
			like =Like.objects.get(user = user, blog = blog)
		except Like.DoesNotExist:
			Like.objects.create(user = user, blog = blog)
			return render(request,'user_profile/view_user_post.html',{'like_bool':"true"})
		else:
			like.delete()
			return render(request,'user_profile/view_user_post.html',{'like_bool':"false"})


	

def activate(request, uidb64,token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk = uid)
	except(TypeError,ValueError,OverflowError,User.DoesNotExist):
		user = None
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		Profile_detail.objects.create(username = user,DOB = '1970-1-1')
		auth_login(request, user,backend='django.contrib.auth.backends.ModelBackend')
		return redirect('blogAPP')
	else:
		return HttpResponse('activation link is invalid')


def forgotPassword(request):
	if request.method == 'POST':
		try:
			user = User.objects.get(email = request.POST['email'])
		except(User.DoesNotExist):
			return render(request,'forgot_password.html',{'error_message':"Email is not registered"})

		else:
			current_site = get_current_site(request)
			mail_subject = 'forgot password.'
			message = render_to_string('reset_email.html', {
				'user': user,
				'domain': current_site.domain,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)),
				'token': forgot_password_token.make_token(user),
				})
			to_email = user.email
			email = EmailMessage(mail_subject,message,to = [to_email])
			email.send()
			return HttpResponse('A forgot password mail is sent to your email address please click on the link to set new password')
	else:
		return render(request,'forgot_password.html')


class PasswordResetConfirmView(FormView):
	template_name = 'resetpassword.html'
	success_url = '/user_profile/'
	form_class = SetPasswordForm

	def post(self, request, uidb64 = None , token = None, *arg, **kwargs):
		try:
			uid = force_text(urlsafe_base64_decode(uidb64))
			user = User.objects.get(pk = uid)
			form = self.form_class(request.POST)
		except(TypeError,ValueError,OverflowError,User.DoesNotExist):
			user = None
		if user is not None and forgot_password_token.check_token(user, token):
			if form.is_valid():
				new_password = form.cleaned_data['new_password2']
				user.set_password(new_password)
				user.save()
				messages.success(request, 'Password has been reset.')
				return self.form_valid(form)
			else:
				messages.error(request, 'Password reset has not been unsuccessful.')
				return self.form_invalid(form)
		else:
			messages.error(request, 'Password link is no longer available')
			return self.form_invalid(form)


def resendAccActivation(request):
	if request.method == 'POST':
		try:
			user = User.objects.get(email = request.POST['email'])
		except(User.DoesNotExist):
			return render(request,'resendAccActivation.html',{'error_message' : 'Email-id is not Registered'})
		else:
			current_site = get_current_site(request)
			mail_subject = 'Activate your blog account.'
			message = render_to_string('acc_active.html', {
				'user': user,
				'domain': current_site.domain,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)),
				'token': forgot_password_token.make_token(user),
				})
			to_email = user.email
			email = EmailMessage(mail_subject,message,to = [to_email])
			email.send()
			return HttpResponse('A account confirmation mail is sent to your email address please click on the link')
	else:
		return render(request,'resendAccActivation.html')
