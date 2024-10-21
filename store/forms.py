from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django import forms
from django.utils.safestring import mark_safe
from.models import Profile

class UserInForm(forms.ModelForm):
    phone = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Phone'}),required =False)
    # 定義一個名為 phone 的表單字段，類型為 CharField
    #attrs 是一個字典，指定了輸入框的 HTML 屬性
    #class':'form-control這個屬性添加了 Bootstrap 樣式類別，使輸入框的外觀符合 Bootstrap 的樣式規範
    #required =False 這個參數的目的是讓電話號碼字段變為非必填項。即使用戶不填寫這個字段，表單仍然可以被提交並通過驗證。
    address1 = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Address1'}),required =False)
    address2 = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Address2'}),required =False)
    city = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'City'}),required =False)
    state = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'State'}),required =False)
    zipcode = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Zipcode'}),required =False)
    country = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Country'}),required =False)
    
    class Meta:
        model = Profile
        fields =('phone','address1','address2','city','state','zipcode','country')
        




class changePasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']
  
    def __init__(self, *args, **kwargs):
        super(changePasswordForm, self).__init__(*args, **kwargs)

        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['new_password1'].label = ''
        self.fields['new_password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['new_password2'].label = ''
        self.fields['new_password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'	
	
class UpdateUserForm(UserChangeForm):    
    password = None  # Hide password field
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),required =False)
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),required =False)
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),required =False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)

        # Customizing the username field
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = mark_safe(
            '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'
        )

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'
