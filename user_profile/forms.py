from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
	email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2')


class SetPasswordForm(forms.Form):
	error_message = 'the password fields didnor match'
	new_password1 = forms.CharField(label = 'New Password', widget = forms.PasswordInput)
	new_password2 = forms.CharField(label = 'Confirm Password', widget = forms.PasswordInput)

	def clean_new_password2(self):
		password1 = self.cleaned_data.get('new_password1')
		password2 = self.cleaned_data.get('new_password2')
		if password1 and password2:
			if password1 != password2:
				raise forms.ValidationError(
					self.error_message,
					code = 'password mismatch'
					)
		return password2

