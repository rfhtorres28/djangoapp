from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import UserDetails
from django.core.validators import EmailValidator
from .models import ElecsQuestions, ElecsOptions, CommsQuestions,  CommsOptions, MathQuestions, MathOptions, GEASQuestions, GEASOptions
import random 


class RegistrationForm(UserCreationForm):
    
   
    firstname = forms.CharField(max_length=30, required=True)
    lastname = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254)

    class Meta:
        model = UserDetails  # Set the model to your custom user model
        fields = ('username', 'firstname', 'lastname', 'email', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data.get('username')
    
        if len(username) > 10:
            raise forms.ValidationError('Username must be less than 10 characters only')
        
        if UserDetails.objects.filter(username=username).exists():
             raise forms.ValidationError('Username already exists. Please choose another username')
        
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if UserDetails.objects.filter(email=email).exists():
            raise forms.ValidationError('Email Already exists. Please choose other email')

        return email
    
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs) # get the fields from the parent class (UserCreationForm -> superclass) to be the fields of the registration form
        self.fields['username'].widget.attrs.update({'class':'form-control', 'id':'username', 'placeholder': 'Enter your Username'})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'id':'password1', 'placeholder': 'Enter your Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'id':'password2', 'placeholder': 'Enter your Confirm Password'})
        self.fields['firstname'].widget.attrs.update({'class':'form-control', 'id':'firstname','placeholder': 'Enter your Firstname'})
        self.fields['lastname'].widget.attrs.update({'class':'form-control', 'id':'lastname','placeholder': 'Enter your lastname'})
        self.fields['email'].widget.attrs.update({'class':'form-control', 'id':'email', 'placeholder': 'Enter your Email'})
        self.fields['password1'].help_text = '' #Delete the helper text of password1
        self.fields['password2'].help_text = '' #Delete the helper text of password2


countries = [
    ("Afghanistan", "Afghanistan"), ("Albania", "Albania"), ("Algeria", "Algeria"), ("American Samoa", "American Samoa"), ("Andorra", "Andorra"), ("Angola", "Angola"), ("Anguilla", "Anguilla"), ("Antarctica", "Antarctica"), ("Antigua and Barbuda", "Antigua and Barbuda"), ("Argentina", "Argentina"),
    ("Armenia", "Armenia"), ("Aruba", "Aruba"), ("Australia", "Australia"), ("Austria", "Austria"), ("Azerbaijan", "Azerbaijan"), ("Bahamas", "Bahamas"), ("Bahrain", "Bahrain"), ("Bangladesh", "Bangladesh"), ("Barbados", "Barbados"), ("Belarus", "Belarus"),
    ("Belgium", "Belgium"), ("Belize", "Belize"), ("Benin", "Benin"), ("Bermuda", "Bermuda"), ("Bhutan", "Bhutan"), ("Bolivia", "Bolivia"), ("Bosnia and Herzegovina", "Bosnia and Herzegovina"), ("Botswana", "Botswana"), ("Bouvet Island", "Bouvet Island"), ("Brazil", "Brazil"),
    ("British Indian Ocean Territory", "British Indian Ocean Territory"), ("Brunei Darussalam", "Brunei Darussalam"), ("Bulgaria", "Bulgaria"), ("Burkina Faso", "Burkina Faso"), ("Burundi", "Burundi"), ("Cambodia", "Cambodia"), ("Cameroon", "Cameroon"), ("Canada", "Canada"), ("Cape Verde", "Cape Verde"), ("Cayman Islands", "Cayman Islands"),
    ("Central African Republic", "Central African Republic"), ("Chad", "Chad"), ("Chile", "Chile"), ("China", "China"), ("Christmas Island", "Christmas Island"), ("Cocos (Keeling) Islands", "Cocos (Keeling) Islands"), ("Colombia", "Colombia"), ("Comoros", "Comoros"), ("Congo", "Congo"), ("Congo, the Democratic Republic of the", "Congo, the Democratic Republic of the"),
    ("Cook Islands", "Cook Islands"), ("Costa Rica", "Costa Rica"), ("Cote D'Ivoire", "Cote D'Ivoire"), ("Croatia", "Croatia"), ("Cuba", "Cuba"), ("Cyprus", "Cyprus"), ("Czech Republic", "Czech Republic"), ("Denmark", "Denmark"), ("Djibouti", "Djibouti"), ("Dominica", "Dominica"),
    ("Dominican Republic", "Dominican Republic"), ("Ecuador", "Ecuador"), ("Egypt", "Egypt"), ("El Salvador", "El Salvador"), ("Equatorial Guinea", "Equatorial Guinea"), ("Eritrea", "Eritrea"), ("Estonia", "Estonia"), ("Ethiopia", "Ethiopia"), ("Falkland Islands (Malvinas)", "Falkland Islands (Malvinas)"), ("Faroe Islands", "Faroe Islands"),
    ("Fiji", "Fiji"), ("Finland", "Finland"), ("France", "France"), ("French Guiana", "French Guiana"), ("French Polynesia", "French Polynesia"), ("French Southern Territories", "French Southern Territories"), ("Gabon", "Gabon"), ("Gambia", "Gambia"), ("Georgia", "Georgia"), ("Germany", "Germany"),
    ("Ghana", "Ghana"), ("Gibraltar", "Gibraltar"), ("Greece", "Greece"), ("Greenland", "Greenland"), ("Grenada", "Grenada"), ("Guadeloupe", "Guadeloupe"), ("Guam", "Guam"), ("Guatemala", "Guatemala"), ("Guinea", "Guinea"), ("Guinea-Bissau", "Guinea-Bissau"),
    ("Guyana", "Guyana"), ("Haiti", "Haiti"), ("Heard Island and Mcdonald Islands", "Heard Island and Mcdonald Islands"), ("Holy See (Vatican City State)", "Holy See (Vatican City State)"), ("Honduras", "Honduras"), ("Hong Kong", "Hong Kong"), ("Hungary", "Hungary"), ("Iceland", "Iceland"), ("India", "India"),
    ("Indonesia", "Indonesia"), ("Iran, Islamic Republic of", "Iran, Islamic Republic of"), ("Iraq", "Iraq"), ("Ireland", "Ireland"), ("Israel", "Israel"), ("Italy", "Italy"), ("Jamaica", "Jamaica"), ("Japan", "Japan"), ("Jordan", "Jordan"), ("Kazakhstan", "Kazakhstan"),
    ("Kenya", "Kenya"), ("Kiribati", "Kiribati"), ("Korea, Democratic People's Republic of", "Korea, Democratic People's Republic of"), ("Korea, Republic of", "Korea, Republic of"), ("Kuwait", "Kuwait"), ("Kyrgyzstan", "Kyrgyzstan"), ("Lao People's Democratic Republic", "Lao People's Democratic Republic"), ("Latvia", "Latvia"), ("Lebanon", "Lebanon"),
    ("Lesotho", "Lesotho"), ("Liberia", "Liberia"), ("Libyan Arab Jamahiriya", "Libyan Arab Jamahiriya"), ("Liechtenstein", "Liechtenstein"), ("Lithuania", "Lithuania"), ("Luxembourg", "Luxembourg"), ("Macao", "Macao"), ("Macedonia, the Former Yugoslav Republic of", "Macedonia, the Former Yugoslav Republic of"), ("Madagascar", "Madagascar"),
    ("Malawi", "Malawi"), ("Malaysia", "Malaysia"), ("Maldives", "Maldives"), ("Mali", "Mali"), ("Malta", "Malta"), ("Marshall Islands", "Marshall Islands"), ("Martinique", "Martinique"), ("Mauritania", "Mauritania"), ("Mauritius", "Mauritius"), ("Mayotte", "Mayotte"),
    ("Mexico", "Mexico"), ("Micronesia, Federated States of", "Micronesia, Federated States of"), ("Moldova, Republic of", "Moldova, Republic of"), ("Monaco", "Monaco"), ("Mongolia", "Mongolia"), ("Montserrat", "Montserrat"), ("Morocco", "Morocco"), ("Mozambique", "Mozambique"), ("Myanmar", "Myanmar"),
    ("Namibia", "Namibia"), ("Nauru", "Nauru"), ("Nepal", "Nepal"), ("Netherlands", "Netherlands"), ("Netherlands Antilles", "Netherlands Antilles"), ("New Caledonia", "New Caledonia"), ("New Zealand", "New Zealand"), ("Nicaragua", "Nicaragua"), ("Niger", "Niger"), ("Nigeria", "Nigeria"),
    ("Niue", "Niue"), ("Norfolk Island", "Norfolk Island"), ("Northern Mariana Islands", "Northern Mariana Islands"), ("Norway", "Norway"), ("Oman", "Oman"), ("Pakistan", "Pakistan"), ("Palau", "Palau"), ("Palestinian Territory, Occupied", "Palestinian Territory, Occupied"), ("Panama", "Panama"), ("Papua New Guinea", "Papua New Guinea"),
    ("Paraguay", "Paraguay"), ("Peru", "Peru"), ("Philippines", "Philippines"), ("Pitcairn", "Pitcairn"), ("Poland", "Poland"), ("Portugal", "Portugal"), ("Puerto Rico", "Puerto Rico"), ("Qatar", "Qatar"), ("Reunion", "Reunion"), ("Romania", "Romania"), ("Russian Federation", "Russian Federation"),
    ("Rwanda", "Rwanda"), ("Saint Helena", "Saint Helena"), ("Saint Kitts and Nevis", "Saint Kitts and Nevis"), ("Saint Lucia", "Saint Lucia"), ("Saint Pierre and Miquelon", "Saint Pierre and Miquelon"), ("Saint Vincent and the Grenadines", "Saint Vincent and the Grenadines"), ("Samoa", "Samoa"), ("San Marino", "San Marino"), ("Sao Tome and Principe", "Sao Tome and Principe"),
    ("Saudi Arabia", "Saudi Arabia"), ("Senegal", "Senegal"), ("Serbia and Montenegro", "Serbia and Montenegro"), ("Seychelles", "Seychelles"), ("Sierra Leone", "Sierra Leone"), ("Singapore", "Singapore"), ("Slovakia", "Slovakia"), ("Slovenia", "Slovenia"), ("Solomon Islands", "Solomon Islands"), ("Somalia", "Somalia"),
    ("South Africa", "South Africa"), ("South Georgia and the South Sandwich Islands", "South Georgia and the South Sandwich Islands"), ("Spain", "Spain"), ("Sri Lanka", "Sri Lanka"), ("Sudan", "Sudan"), ("Suriname", "Suriname"), ("Svalbard and Jan Mayen", "Svalbard and Jan Mayen"), ("Swaziland", "Swaziland"), ("Sweden", "Sweden"),
    ("Switzerland", "Switzerland"), ("Syrian Arab Republic", "Syrian Arab Republic"), ("Taiwan, Province of China", "Taiwan, Province of China"), ("Tajikistan", "Tajikistan"), ("Tanzania, United Republic of", "Tanzania, United Republic of"), ("Thailand", "Thailand"), ("Timor-Leste", "Timor-Leste"), ("Togo", "Togo"), ("Tokelau", "Tokelau"),
    ("Tonga", "Tonga"), ("Trinidad and Tobago", "Trinidad and Tobago"), ("Tunisia", "Tunisia"), ("Turkey", "Turkey"), ("Turkmenistan", "Turkmenistan"), ("Turks and Caicos Islands", "Turks and Caicos Islands"), ("Tuvalu", "Tuvalu"), ("Uganda", "Uganda"), ("Ukraine", "Ukraine"), ("United Arab Emirates", "United Arab Emirates"),
    ("United Kingdom", "United Kingdom"), ("United States", "United States"), ("United States Minor Outlying Islands", "United States Minor Outlying Islands"), ("Uruguay", "Uruguay"), ("Uzbekistan", "Uzbekistan"), ("Vanuatu", "Vanuatu"), ("Venezuela", "Venezuela"), ("Viet Nam", "Viet Nam"), ("Virgin Islands, British", "Virgin Islands, British"),
    ("Virgin Islands, U.s.", "Virgin Islands, U.s."), ("Wallis and Futuna", "Wallis and Futuna"), ("Western Sahara", "Western Sahara"), ("Yemen", "Yemen"), ("Zambia", "Zambia"), ("Zimbabwe", "Zimbabwe")]


class ProfileForm(forms.Form):


    gender = forms.ChoiceField(label='Gender', choices=[('male', 'Male'), ('female', 'Female')], widget=forms.RadioSelect)
    instagram_username = forms.CharField(label='Instagram', widget=forms.TextInput(attrs={'placeholder': 'Enter your Instagram Username', 'class':'form-control'}))
    facebook_username = forms.CharField(label='Facebook', widget=forms.TextInput(attrs={'placeholder': 'Enter your Facebook Username', 'class':'form-control'}))
    date_of_birth = forms.DateField(label='Date of Birth', widget=forms.DateInput(attrs={'type': 'date'}))
    bio = forms.CharField(label='Bio', widget=forms.TextInput(attrs={'placeholder': 'Enter your Bio', 'class':'form-control'}))
    country = forms.ChoiceField(label='Country', choices=countries)  
    picture = forms.ImageField(label='Profile Picture', widget=forms.FileInput)


class LoginForm(forms.Form):

    email = forms.EmailField(label='Email', required=True, validators=[EmailValidator()] , widget=forms.TextInput(attrs={'placeholder': 'Enter your Email', 'class':'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Enter your Password', 'class':'form-control'}))





class UpdateInformation(forms.Form):
    firstname_update = forms.CharField(label='Firstname', widget=forms.TextInput(attrs={'class': 'form-firstname', 'placeholder': 'Firstname'}))
    lastname_update = forms.CharField(label='Lastname', widget=forms.TextInput(attrs={'class': 'form-lastname', 'placeholder': 'Lastname'}))
    username_update = forms.CharField(label='Username', widget=forms.TextInput(attrs={'id':'username', 'class': 'form-username', 'placeholder': 'Username'}))
    email_update = forms.EmailField(label='Email', validators=[EmailValidator()], widget=forms.EmailInput(attrs={'id':'email','class': 'form-email', 'placeholder': 'Email'}))
    gender_update = forms.ChoiceField(label='Gender', choices=[('male', 'Male'), ('female', 'Female')],widget=forms.RadioSelect)
    ig_username_update = forms.CharField(label='Instagram', widget=forms.TextInput(attrs={'class': 'form-instagram', 'placeholder': 'Instagram'}))
    fb_username_update = forms.CharField(label='Facebook',  widget=forms.TextInput(attrs={'class': 'form-facebook', 'placeholder': 'Facebook'}))
    date_of_birth_update = forms.DateField(label='Birthdate', widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-birthdate', 'placeholder': 'Date of Birth'}) )
    bio_update = forms.CharField(label='Bio', widget=forms.TextInput(attrs={'class': 'form-bio', 'placeholder': 'Bio'}))
    picture_update = forms.ImageField(label='Profile Picture', widget=forms.FileInput(attrs={'class': 'form-picture', 'placeholder': 'Profile Picture'}))



    def clean_username(self):

        username = self.cleaned_data.get('username_update')
        user = UserDetails.objects.filter(username=username).first()

        if user:
            raise forms.ValidationError('Username is already taken')
        





class UpdatePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # inherits the fields from the password change form
        
        # Customize labels here
        self.fields['old_password'].label = 'Current Password'
        self.fields['new_password1'].label = 'New Password'
        self.fields['new_password2'].label = 'Confirm New Password'
        self.fields['old_password'].widget.attrs.update({'class':'form-control-1'})
        self.fields['new_password1'].widget.attrs.update({'class':'form-control-2'})
        self.fields['new_password2'].widget.attrs.update({'class':'form-control-3'})
        self.fields['new_password1'].help_text = '' #Delete the helper text of new password





qn = ElecsQuestions.objects.all()
opn = ElecsOptions.objects.all()
ece_questions = [{"id":question.id, "content":question.content,
                "options":[{"question_no":question.id, "letter":option.letter, "content":option.content, "is_correct":option.is_correct} for option in opn if option.question_no_id == question.id]} for question in qn]





class ElecsQuizForm(forms.Form):

    def set_questions(self, ece_questions):
        for i in range(len(ece_questions)):
            question = ece_questions[i]
            field_name = f'question_{i}'
            field_label = question['content']
            options = [(question["letter"], question["content"]) for question in question["options"]]
            self.fields[field_name] = forms.ChoiceField(label=field_label, choices=options, widget=forms.RadioSelect, required=True)




qn = CommsQuestions.objects.all()
opn = CommsOptions.objects.all()
comms_questions = [{"id":question.id, "content":question.content,
                 "options":[{"question_no":question.id, "letter":option.letter, "content":option.content, "is_correct":option.is_correct} for option in opn if option.question_no_id == question.id]} for question in qn]



class CommsQuizForm(forms.Form):


    def set_questions(self, comms_questions):
        for i in range(len(comms_questions)):  
            question = comms_questions[i]
            field_name = f'question_{i}'
            field_label = question['content']
            options = [(question["letter"], question["content"]) for question in question["options"]]
            self.fields[field_name] = forms.ChoiceField(label=field_label, choices=options, widget=forms.RadioSelect, required=True)





qn = MathQuestions.objects.all()
opn = MathOptions.objects.all()
math_questions = [{"id":question.id, "content":question.content,
                "options":[{"question_no":question.id, "letter":option.letter, "content":option.content, "is_correct":option.is_correct} for option in opn if option.question_no_id == question.id]} for question in qn]



class MathQuizForm(forms.Form):


    def set_questions(self, math_questions):
        for i in range(len(math_questions)):    
            question = math_questions[i]
            field_name = f'question_{i}'
            field_label = question['content']
            options = [(question["letter"], question["content"]) for question in question["options"]]
            self.fields[field_name] = forms.ChoiceField(label=field_label, choices=options, widget=forms.RadioSelect, required=True)


qn = GEASQuestions.objects.all()
opn = GEASOptions.objects.all()
geas_questions = [{"id":question.id, "content":question.content,
                 "options":[{"question_no":question.id, "letter":option.letter, "content":option.content, "is_correct":option.is_correct} for option in opn if option.question_no_id == question.id]} for question in qn]


class GEASQuizForm(forms.Form):


    def set_questions(self, geas_questions):
        for i in range(len(geas_questions)):        
            question = geas_questions[i]
            field_name = f'question_{i}'
            field_label = question['content']
            options = [(question["letter"], question["content"]) for question in question["options"]]
            self.fields[field_name] = forms.ChoiceField(label=field_label, choices=options, widget=forms.RadioSelect, required=True)


