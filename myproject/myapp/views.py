from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import RegistrationForm, ProfileForm, LoginForm, UpdateInformation
import secrets
from django.conf import settings
import os 
from .models import UserDetails, UserResult
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from datetime import datetime
import random 
from django import forms
# from .forms import ElecsQuizForm, CommsQuizForm, MathQuizForm, GEASQuizForm, ece_questions, comms_questions, math_questions, geas_questions, UpdatePasswordForm
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.core.validators import validate_email as EmailValidator
from django.contrib.auth.password_validation import validate_password as PasswordValidator
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver


def is_valid_email(email):
     try:
        EmailValidator(email)
        return True
     
     except ValidationError:
         
          
          return False


def is_valid_password(password):
     try:
         PasswordValidator(password)
         return True
     
     except ValidationError as e:
          error_messages = []
          for error in e.error_list:
            error_messages.append(error.message)

          print(error_messages)
          return error_messages
            


def validate_username(request):
     username = request.GET.get('username', '')
     len_error = None
     username_exist = None
     
     if len(username) > 10:
          len_error = True
     
     else:
          len_error = False
        
     
     if UserDetails.objects.filter(username=username).exists():
          username_exist = True
     
     else:
          username_exist = False
     

     return JsonResponse({'errors':{'len_error': len_error, 'username_exist':username_exist}})


def validate_email(request):
     email = request.GET.get('email', '')
     email_exist = None
     wrong_email_format = None
     
     if UserDetails.objects.filter(email=email).exists():
          email_exist = True

     else:
          email_exist = False
     
     if is_valid_email(email):
          wrong_email_format = False
     
     else:
          wrong_email_format = True
     
     return JsonResponse({'errors':{'email_exist':email_exist, 'wrong_email_format':wrong_email_format}})
     
          
def validate_password(request):
     password1 = request.GET.get('password1', '')
     password_error = None

     validation_result = is_valid_password(password1)
    
     if validation_result == True:
          password_error = False

     else:
          password_error = validation_result
     
     print(password_error)
     return JsonResponse({'errors':{'password_error':password_error}})
          
          

def validate_passwords(request):
     password1 = request.GET.get('password1', '')
     password2 = request.GET.get('password2', '')
     match_passwords = None


     if password1 != password2:
          match_passwords = False
     
     else:
          match_passwords = True
     
     return JsonResponse({'errors':{'match_passwords':match_passwords}})
     

def validate_latest_username(request):
     username = request.GET.get('username', '')
     is_username_exist = None
     username_len_validation = None
     if UserDetails.objects.filter(username=username).exists():
          is_username_exist = True

     else:
          is_username_exist = False

     if len(username) > 10:
          username_len_validation = False
     
     else:
          username_len_validation = True

     return JsonResponse({'errors': {'is_username_exist': is_username_exist, 'username_len_validation': username_len_validation}})
            


def validate_latest_email(request):
     email = request.GET.get('email', '')
     is_email_exist = None
     is_email_valid = None

     if UserDetails.objects.filter(email=email).exists():
          is_email_exist = True
     
     else:
          is_email_exist = False
     

     if is_valid_email(email):
          is_email_valid = True
     

     else:
        is_email_valid = False
     print(is_email_exist)
     return JsonResponse({'errors':{'is_email_exist':is_email_exist, 'is_email_valid':is_email_valid}})
          











def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            
            # Storing register information to the session
            request.session['registration_data'] = { 
                'username': form.cleaned_data['username'],
                'firstname': form.cleaned_data['firstname'],
                'lastname': form.cleaned_data['lastname'],
                'email': form.cleaned_data['email'],
                'password': form.cleaned_data['password1']}
         

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'message':'There is no error'})
            

            return redirect('profile')
        else:
             if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                 errors = dict(form.errors.items())
                 print(errors)
                 return JsonResponse({'errors':errors})
             return redirect('home')
    
    else:
        form = RegistrationForm()

    
    return render(request, 'myapp/register.html', {'form':form})



def save_picture(form_picture):
    random_hex = secrets.token_hex(8) # generates random hexadecimal characters
    _, f_ext = os.path.splitext(form_picture.name) # splits the filename and the extension format, form_picture.name is the filename of the uploaded file
    picture_fn = random_hex + f_ext # generate new filename 
 
    picture_path = os.path.join(settings.MEDIA_ROOT, 'profile_pics', picture_fn)
    print(picture_path)

    os.makedirs(os.path.dirname(picture_path), exist_ok=True)
    
    with open(picture_path, 'wb') as f:
        for chunk in form_picture.chunks():
            f.write(chunk)

    return picture_fn



def profile(request):
    registration_data = request.session.get('registration_data')

    if not registration_data:
        return redirect('register')

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        
        if form.is_valid():
            print('form is valid')
            hashed_password = make_password(registration_data.get('password'))

            # Store the form fields to the database
            user = UserDetails.objects.create(
                username=registration_data['username'],
                firstname=registration_data['firstname'],
                lastname=registration_data['lastname'],
                email=registration_data['email'],
                password=hashed_password,
                date_of_birth=form.cleaned_data['date_of_birth'],
                country=form.cleaned_data['country'],
                gender=form.cleaned_data['gender'],
                instagram_link=form.cleaned_data['instagram_username'],
                facebook_link=form.cleaned_data['facebook_username'],
                bio=form.cleaned_data['bio'],
            )
     
            if form.cleaned_data['picture']:
                print('picture file is ok')
                picture_file = save_picture(form.cleaned_data['picture'])
                print(picture_file)
                user.image_file = picture_file

            user.save()
            request.session.pop('registration_data')
            messages.success(request, 'You can now login to your account')
            return redirect('memberlogin')
        else:
            print(form.errors)
    else:

        form = ProfileForm()

    return render(request, 'myapp/user_profile.html', {'form': form})


def home(request):
             
     if request.method == 'GET':
       if request.user.is_authenticated:
              return redirect(reverse('account', kwargs={'username':request.user.username}))
  
       else:       
          return render(request, 'myapp/home.html')
            
          

def memberlogin(request):
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user:
                user.last_login = datetime.now()
                user.save()
                login(request, user)
                print("Authentication successful:", request.user.is_authenticated)

                return redirect(reverse('account', kwargs={'username':user.username}))
                
            else:
                print("Authentication failed")
                messages.success(request, 'Invalid credentials. Please try again.')
                return redirect('memberlogin')
            

    else:
        form = LoginForm()
    
    return render(request, 'myapp/login.html', {'form':form, 'messages': messages.get_messages(request)})



field_labels = {}
session_user_result = None
def electronics(request):
    
    if not request.user.is_authenticated:
        return redirect('memberlogin')
    
    shuffled_questions = ece_questions
    random.shuffle(shuffled_questions)
    if request.method == 'GET':
        for i in range(len(shuffled_questions)):
            question = shuffled_questions[i]
            field_name = f'Question {i}'
            field_label = question['content']
            field_labels[field_name] = field_label

            
        request.session['shuffled_ece_questions'] = shuffled_questions
        form = ElecsQuizForm()
        form.set_questions(shuffled_questions)

        return render(request, 'myapp/elecsquiz.html', {'form':form})
   
    
    if request.method == 'POST':

        shuffled_questions = request.session.get('shuffled_ece_questions')
        form = ElecsQuizForm(request.POST)
        form.set_questions(shuffled_questions)
        no_correct_answer = 0
        user_response = []
        total_questions = len(ece_questions)
        correct_options = []
        correct_option = []
        answer_content = []
        questions = []
        session_id = secrets.token_hex(16)
        request.session['sid'] = session_id
        global session_user_result

        for question in field_labels.values():
                 questions.append(question)

        # Checking if whether the user response is correct or not, request.form-> user answers, 
        for form_question in field_labels.values():
            for elecs_question in ece_questions:
                if elecs_question["content"] == form_question:
                    for option in elecs_question["options"]:
                        if option["is_correct"]:
                             correct_options.append(option)

        
        if correct_options:  # Check if correct_options is not empty before proceeding
               for option in correct_options:
                  correct_option.append(option['letter'])
                  answer_content.append(option['content'])
        
        filtered_form = {key: value for key, value in request.POST.items() if key not in ['user_id', 'csrfmiddlewaretoken']}

        for value in filtered_form.values():
                user_response.append(value)
        

        for i in range(len(user_response)):
                if user_response[i] == correct_option[i]:
                    no_correct_answer += 1
        
        session_id = request.session.get('sid')
        score_percentage = no_correct_answer/total_questions*100
        score_percentage = round(score_percentage, 2)
        completion_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
        user_result= {"subject":"Electronics", "session_id":session_id, "score_percentage":score_percentage, "no_correct_answer":no_correct_answer, "timestamp":completion_time, "correct_answer":answer_content, "question":questions}

        if request.user.is_authenticated:
                username = request.user.username 
                country = request.user.country
                request.session["user_result"] = user_result # store the user_result to the session
                session_user_result = request.session.get("user_result")
        
        if session_user_result:
                     score_percentage = session_user_result["score_percentage"]
                     no_correct_answer = session_user_result["no_correct_answer"]
                     timestamp = session_user_result["timestamp"] 
                     subject = session_user_result["subject"]
        
        if session_id:
             user_details = UserDetails.objects.get(id=request.user.id)
             image_file = f'{settings.MEDIA_URL}profile_pics/{request.user.image_file}'
             new_result = UserResult.objects.create(user_id=user_details, profile_pic=image_file, username=username, country=country, session_id=session_id, subject=subject, score_percentage=score_percentage, no_correct_answer=no_correct_answer, posted_time=timestamp)
             new_result.save()
                
             return render(request, 'myapp/elecsresult.html', {'form':form, 'score_percentage':score_percentage,
                        'no_correct_answer':no_correct_answer, 'total_questions':total_questions})
                                
        


       


def elecsanswers(request):
     
     if not request.user.is_authenticated:
            return redirect('memberlogin')
          

     else:  
        user_result = request.session.get("user_result", None)

        if user_result:
           answer_key = {}
           correct_answers = request.session["user_result"]["correct_answer"]
           questions = request.session["user_result"]["question"]
          
           for i in range(len(correct_answers)):
              answer_key[questions[i]] = correct_answers[i]
      
     
           answer_key = answer_key.items()
           return render(request, 'myapp/elecsanswers.html', {'answer_key':answer_key})
     
        else:
             return HttpResponse("<h1>Requested resource was not found</h1>", status=404)

        

field_labels = {}
session_user_result = None
def communications(request):
    
    if not request.user.is_authenticated:
        return redirect('memberlogin')
    
    shuffled_questions = comms_questions
    random.shuffle(shuffled_questions)
    if request.method == 'GET':
        for i in range(len(shuffled_questions)):
            question = shuffled_questions[i]
            field_name = f'Question {i}'
            field_label = question['content']
            field_labels[field_name] = field_label

            
        request.session['shuffled_comms_questions'] = shuffled_questions
        form = CommsQuizForm()
        form.set_questions(shuffled_questions)

        return render(request, 'myapp/commsquiz.html', {'form':form})
   
    
    if request.method == 'POST':

        shuffled_questions = request.session.get('shuffled_comms_questions')
        form = CommsQuizForm(request.POST)
        form.set_questions(shuffled_questions)
        no_correct_answer = 0
        user_response = []
        total_questions = len(comms_questions)
        correct_options = []
        correct_option = []
        answer_content = []
        questions = []
        session_id = secrets.token_hex(16)
        request.session['sid'] = session_id
        global session_user_result

        for question in field_labels.values():
                 questions.append(question)

        # Checking if whether the user response is correct or not, request.form-> user answers, 
        for form_question in field_labels.values():
            for comms_question in comms_questions:
                if comms_question["content"] == form_question:
                    for option in comms_question["options"]:
                        if option["is_correct"]:
                             correct_options.append(option)

        
        if correct_options:  # Check if correct_options is not empty before proceeding
               for option in correct_options:
                  correct_option.append(option['letter'])
                  answer_content.append(option['content'])
        
        filtered_form = {key: value for key, value in request.POST.items() if key not in ['user_id', 'csrfmiddlewaretoken']}

        for value in filtered_form.values():
                user_response.append(value)
        

        for i in range(len(user_response)):
                if user_response[i] == correct_option[i]:
                    no_correct_answer += 1
        
        session_id = request.session.get('sid')
        score_percentage = no_correct_answer/total_questions*100
        score_percentage = round(score_percentage, 2)
        completion_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user_result= {"subject":"Communications", "session_id":session_id, "score_percentage":score_percentage, "no_correct_answer":no_correct_answer, "timestamp":completion_time, "correct_answer":answer_content, "question":questions}

        if request.user.is_authenticated:
                username = request.user.username 
                country = request.user.country
                request.session["user_result"] = user_result # store the user_result to the session
                session_user_result = request.session.get("user_result")
        
        if session_user_result:
                     score_percentage = session_user_result["score_percentage"]
                     no_correct_answer = session_user_result["no_correct_answer"]
                     timestamp = session_user_result["timestamp"] 
                     subject = session_user_result["subject"]
        
        if session_id:
                user_details = UserDetails.objects.get(id=request.user.id)
                image_file = f'{settings.MEDIA_URL}profile_pics/{request.user.image_file}'
                new_result = UserResult.objects.create(user_id=user_details, profile_pic=image_file, username=username, country=country, session_id=session_id, subject=subject, score_percentage=score_percentage, no_correct_answer=no_correct_answer, posted_time=timestamp)
                new_result.save()
                return render(request, 'myapp/commsresult.html', {'form':form, 'score_percentage':score_percentage,
                      'no_correct_answer':no_correct_answer, 'total_questions':total_questions})

        
       


def commsanswers(request):
       if not request.user.is_authenticated:
            return redirect('memberlogin')
          

       else:  
          user_result = request.session.get("user_result", None)

       if user_result:
           answer_key = {}
           correct_answers = request.session["user_result"]["correct_answer"]
           questions = request.session["user_result"]["question"]
          
           for i in range(len(correct_answers)):
              answer_key[questions[i]] = correct_answers[i]
      
     
           answer_key = answer_key.items()
           return render(request, 'myapp/commsanswers.html', {'answer_key':answer_key})
     
       else:
             return HttpResponse("<h1>Requested resource was not found</h1>", status=404)





field_labels = {}
session_user_result = None
def math(request):
    
    if not request.user.is_authenticated:
        return redirect('memberlogin')
    
    shuffled_questions = math_questions
    random.shuffle(shuffled_questions)
    if request.method == 'GET':
        for i in range(len(shuffled_questions)):
            question = shuffled_questions[i]
            field_name = f'Question {i}'
            field_label = question['content']
            field_labels[field_name] = field_label

            
        request.session['shuffled_math_questions'] = shuffled_questions
        form = MathQuizForm()
        form.set_questions(shuffled_questions)

        return render(request, 'myapp/mathquiz.html', {'form':form})
   
    
    if request.method == 'POST':

        shuffled_questions = request.session.get('shuffled_math_questions')
        form = MathQuizForm(request.POST)
        form.set_questions(shuffled_questions)
        no_correct_answer = 0
        user_response = []
        total_questions = len(math_questions)
        correct_options = []
        correct_option = []
        answer_content = []
        questions = []
        session_id = secrets.token_hex(16)
        request.session['sid'] = session_id
        global session_user_result

        for question in field_labels.values():
                 questions.append(question)

        # Checking if whether the user response is correct or not, request.form-> user answers, 
        for form_question in field_labels.values():
            for math_question in math_questions:
                if math_question["content"] == form_question:
                    for option in math_question["options"]:
                        if option["is_correct"]:
                             correct_options.append(option)

        
        if correct_options:  # Check if correct_options is not empty before proceeding
               for option in correct_options:
                  correct_option.append(option['letter'])
                  answer_content.append(option['content'])
        
        filtered_form = {key: value for key, value in request.POST.items() if key not in ['user_id', 'csrfmiddlewaretoken']}

        for value in filtered_form.values():
                user_response.append(value)
        

        for i in range(len(user_response)):
                if user_response[i] == correct_option[i]:
                    no_correct_answer += 1
        
        session_id = request.session.get('sid')
        score_percentage = no_correct_answer/total_questions*100
        score_percentage = round(score_percentage, 2)
        completion_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user_result= {"subject":"Math", "session_id":session_id, "score_percentage":score_percentage, "no_correct_answer":no_correct_answer, "timestamp":completion_time, "correct_answer":answer_content, "question":questions}

        if request.user.is_authenticated:
                username = request.user.username 
                country = request.user.country
                request.session["user_result"] = user_result # store the user_result to the session
                session_user_result = request.session.get("user_result")
        
        if session_user_result:
                     score_percentage = session_user_result["score_percentage"]
                     no_correct_answer = session_user_result["no_correct_answer"]
                     timestamp = session_user_result["timestamp"] 
                     subject = session_user_result["subject"]
        
        if session_id:
                user_details = UserDetails.objects.get(id=request.user.id)
                image_file = f'{settings.MEDIA_URL}profile_pics/{request.user.image_file}'
                new_result = UserResult.objects.create(user_id=user_details, profile_pic=image_file, username=username, country=country, session_id=session_id, subject=subject, score_percentage=score_percentage, no_correct_answer=no_correct_answer, posted_time=timestamp)
                new_result.save()
 
                return render(request, 'myapp/mathresult.html', {'form':form, 'score_percentage':score_percentage,
                        'no_correct_answer':no_correct_answer, 'total_questions':total_questions})
        



def mathanswers(request):
       if not request.user.is_authenticated:
            return redirect('memberlogin')
          

       else:  
          user_result = request.session.get("user_result", None)

       if user_result:
           answer_key = {}
           correct_answers = request.session["user_result"]["correct_answer"]
           questions = request.session["user_result"]["question"]
          
           for i in range(len(correct_answers)):
              answer_key[questions[i]] = correct_answers[i]
      
     
           answer_key = answer_key.items()
           return render(request, 'myapp/mathanswers.html', {'answer_key':answer_key})
     
       else:
             return HttpResponse("<h1>Requested resource was not found</h1>", status=404)



field_labels = {}
session_user_result = None
def geas(request):
    
    if not request.user.is_authenticated:
        return redirect('memberlogin')
    
    shuffled_questions = geas_questions
    random.shuffle(shuffled_questions)
    if request.method == 'GET':
        for i in range(len(shuffled_questions)):
            question = shuffled_questions[i]
            field_name = f'Question {i}'
            field_label = question['content']
            field_labels[field_name] = field_label

            
        request.session['shuffled_geas_questions'] = shuffled_questions
        form = GEASQuizForm()
        form.set_questions(shuffled_questions)

        return render(request, 'myapp/geasquiz.html', {'form':form})
   
    
    if request.method == 'POST':

        shuffled_questions = request.session.get('shuffled_geas_questions')
        form = GEASQuizForm(request.POST)
        form.set_questions(shuffled_questions)
        no_correct_answer = 0
        user_response = []
        total_questions = len(geas_questions)
        correct_options = []
        correct_option = []
        answer_content = []
        questions = []
        session_id = secrets.token_hex(16)
        request.session['sid'] = session_id
        global session_user_result

        for question in field_labels.values():
                 questions.append(question)

        # Checking if whether the user response is correct or not, request.form-> user answers, 
        for form_question in field_labels.values():
            for geas_question in geas_questions:
                if geas_question["content"] == form_question:
                    for option in geas_question["options"]:
                        if option["is_correct"]:
                             correct_options.append(option)

        
        if correct_options:  # Check if correct_options is not empty before proceeding
               for option in correct_options:
                  correct_option.append(option['letter'])
                  answer_content.append(option['content'])
        
        filtered_form = {key: value for key, value in request.POST.items() if key not in ['user_id', 'csrfmiddlewaretoken']}

        for value in filtered_form.values():
                user_response.append(value)
        

        for i in range(len(user_response)):
                if user_response[i] == correct_option[i]:
                    no_correct_answer += 1
        
        session_id = request.session.get('sid')
        score_percentage = no_correct_answer/total_questions*100
        score_percentage = round(score_percentage, 2)
        completion_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user_result= {"subject":"GEAS", "session_id":session_id, "score_percentage":score_percentage, "no_correct_answer":no_correct_answer, "timestamp":completion_time, "correct_answer":answer_content, "question":questions}

        if request.user.is_authenticated:
                username = request.user.username 
                country = request.user.country
                request.session["user_result"] = user_result # store the user_result to the session
                session_user_result = request.session.get("user_result")
        
        if session_user_result:
                     score_percentage = session_user_result["score_percentage"]
                     no_correct_answer = session_user_result["no_correct_answer"]
                     timestamp = session_user_result["timestamp"] 
                     subject = session_user_result["subject"]
        
        if session_id:
                     user_details = UserDetails.objects.get(id=request.user.id)
                     image_file = f'{settings.MEDIA_URL}profile_pics/{request.user.image_file}'
                     new_result = UserResult.objects.create(user_id=user_details, profile_pic = image_file, username=username, country=country, session_id=session_id, subject=subject, score_percentage=score_percentage, no_correct_answer=no_correct_answer, posted_time=timestamp)
                     new_result.save()
       
    
                     return render(request, 'myapp/geasresult.html', {'form':form, 'score_percentage':score_percentage,
                        'no_correct_answer':no_correct_answer, 'total_questions':total_questions})
        


def geasanswers(request):
       if not request.user.is_authenticated:
            return redirect('memberlogin')
          

       else:  
          user_result = request.session.get("user_result", None)

       if user_result:
           answer_key = {}
           correct_answers = request.session["user_result"]["correct_answer"]
           questions = request.session["user_result"]["question"]
          
           for i in range(len(correct_answers)):
              answer_key[questions[i]] = correct_answers[i]
      
     
           answer_key = answer_key.items()
           return render(request, 'myapp/geasanswers.html', {'answer_key':answer_key})
     
       else:
             return HttpResponse("<h1>Requested resource was not found</h1>", status=404)



def account(request, username):
      
      user = UserDetails.objects.filter(username=username).first()
      if user:
            present_user = user.firstname + ' ' + user.lastname
            username = user.username
            bio = user.bio
            email = user.email
            instagram = f'https://www.instagram.com/{user.instagram_link}'
            facebook = f'https://www.facebook.com/{user.facebook_link}'
            image_file = f'{settings.MEDIA_URL}profile_pics/{request.user.image_file}'
            profile_pic = f'{settings.MEDIA_URL}profile_pics/{user.image_file}'
            location = user.country
            record = []
            selected_course = ''
            print(image_file)
            print(profile_pic)

            if request.method == 'POST':
                  selected_course = request.POST.get('course', '') 
                  request.session['selected_course'] = selected_course
            else:
                  selected_course = request.session.get('selected_course', '')
            
            page_no = request.GET.get('page', 1)
            user_results = UserResult.objects.filter(user_id_id=user.id, subject=selected_course)
            paginator = Paginator(user_results, 10) # sets 10 results items per page
            page_obj = paginator.get_page(page_no) # returns 10 rows of results from the user_results object
            record = [{"subject": result.subject, "score_percentage": result.score_percentage, "correct_answer": result.no_correct_answer, "timestamp": result.posted_time} for result in page_obj]

            return render(request, 'myapp/account.html', {'location':location, 'profile_pic':profile_pic, 'image_file':image_file, 'present_user':present_user, 'username':username, 'bio':bio, 'record':record, 'instagram':instagram, 'facebook':facebook, 'email':email, 'user_course':user_results, 'selected_course':selected_course, 'user':user, 'page_obj':page_obj})
      
      else:
        return 'User not found', 404
    


def memberlogout(request):
      logout(request)
      return redirect('home')



def quizfeed(request):
      
      result_list=[]
      user = UserResult.objects.order_by('-posted_time').all()
      if user is None:
            message = "No user result found"

      else: 
        result_list = [{"username":result.username, "subject":result.subject, "score_pct":result.score_percentage, "timestamp":result.posted_time,  "user_pic":result.profile_pic, "difference":result.difference} for result in user]
        message = None

        # Updated the latest_login column everytime quizfeed route is refresh
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
        for row in user:
            row.latest_login = current_time
            row.save()

        # Give the length of time from it was posted until the current time
        for row in user: 
            latest_login = datetime.strptime(row.latest_login, '%Y-%m-%d %H:%M:%S')
            delta = latest_login - row.posted_time
           
            if delta.total_seconds() > 86400:
                total_days = delta.total_seconds() // 86400
                row.difference = f'{int(total_days)}d ago'
                row.save()

            elif delta.total_seconds() > 3600:
                total_hours = delta.total_seconds() // 3600
                row.difference = f'{int(total_hours)}h ago'
                row.save()

            elif delta.total_seconds() > 60:
                total_min = delta.total_seconds() // 60
                row.difference = f'{int(total_min)}min ago'
                row.save()
            
            else:
                total_sec = delta.total_seconds()
                row.difference = f'{int(total_sec)}s ago'
                row.save()
        

        # delete user result post on quizfeed if the time difference is more than or equal to 1d ago
        user_result = UserResult.objects.all()
        for user in user_result:
            if user:
                delta = user.time_difference.total_seconds()
                if delta > 86400:
                    user.delete()
        

        # query user that got top scores in answering electronics quiz
        elecs_user = UserResult.objects.filter(subject='Electronics').order_by('-no_correct_answer').all()
        elecs_scorer = [{"user":user.username, "score":user.score_percentage, "location":user.country} for user in elecs_user]
        scorer_elecs = []

        for item in elecs_scorer:
            if item["user"] not in [x["user"] for x in scorer_elecs]:
                scorer_elecs.append(item)
            else:
                continue
        
        scorer_elecs = scorer_elecs[:3]


        # query user that got top scores in answering communications quiz
        comms_user = UserResult.objects.filter(subject='Communications').order_by('-no_correct_answer').all()
        comms_scorer = [{"user":user.username, "score":user.score_percentage, "location":user.country} for user in comms_user]
        scorer_comms = []

        for item in comms_scorer:
            if item["user"] not in [x["user"] for x in scorer_comms]:
                scorer_comms.append(item)
            else:
                continue

        scorer_comms = scorer_comms[:3]


        # query user that got top scores in answering math quiz
        math_user = UserResult.objects.filter(subject='Math').order_by('-no_correct_answer').all()
        math_scorer = [{"user":user.username, "score":user.score_percentage, "location":user.country} for user in math_user]
        scorer_math = []


        for item in math_scorer:
            if item["user"] not in [x["user"] for x in scorer_math]:
                scorer_math.append(item)
            else:
                continue

        scorer_math = scorer_math[:3] 


        # query user that got top scores in answering geas quiz
        geas_user = UserResult.objects.filter(subject='GEAS').order_by('-no_correct_answer').all()
        geas_scorer = [{"user":user.username, "score":user.score_percentage, "location":user.country} for user in geas_user]
        scorer_geas = []


        for item in geas_scorer:
            if item["user"] not in [x["user"] for x in scorer_geas]:
                scorer_geas.append(item)
            else:
                continue

        scorer_geas = scorer_geas[:3]
    
          
      return render(request, 'myapp/quizfeed.html', {'result_list': result_list, 'message': message, 'scorer_elecs': scorer_elecs, 'scorer_comms': scorer_comms, 'scorer_math': scorer_math, 'scorer_geas': scorer_geas}) 



def edit_information(request):
     
     if request.method == 'GET':
          # declaring the initial values of each form fields
          print(request.user.firstname)
          form = UpdateInformation (
          initial = { 'firstname_update' : request.user.firstname,
              'lastname_update' :  request.user.lastname,
              'username_update' :  request.user.username,
              'email_update':  request.user.email,
              'date_of_birth_update':  request.user.date_of_birth,
              'gender_update' : request.user.gender,
              'ig_username_update' :  request.user.instagram_link,
              'fb_username_update' :  request.user.facebook_link,
              'picture_update' : request.user.image_file,
              'bio_update' : request.user.bio
              })
          
          messages.success(request, 'You can now login to your account')
          return render(request, 'myapp/edit_info.html', {'form':form})
          

          

     elif request.method == 'POST':
          form = UpdateInformation(request.POST, request.FILES)
          if form.is_valid():
               request.user.firstname = form.cleaned_data['firstname_update']
               request.user.lastname = form.cleaned_data['lastname_update']
               request.user.username = form.cleaned_data['username_update']
               request.user.email = form.cleaned_data['email_update']
               request.user.date_of_birth = form.cleaned_data['date_of_birth_update']
               request.user.gender = form.cleaned_data['gender_update']
               request.user.instagram_link = form.cleaned_data['ig_username_update']
               request.user.facebook_link = form.cleaned_data['fb_username_update']
               request.user.bio = form.cleaned_data['bio_update']

               if form.cleaned_data['picture_update']:
                    picture_file = save_picture(form.cleaned_data['picture_update'])
                    print(picture_file)
                    request.user.image_file = picture_file
               
               request.user.save()

               #Update username on UserDetails table
               user = UserResult.objects.filter(user_id_id = request.user.id)
               for user in user:
                    user.username = request.user.username
                    user.save()
                
                # Update profile picture on UserResult table
               image_file = f'{settings.MEDIA_URL}profile_pics/{request.user.image_file}'
               user = UserResult.objects.filter(username=request.user.username).all()
               print(image_file)
               for user in user:
                    user.profile_pic = image_file
                    user.save()
               
               return redirect(reverse('account', kwargs={'username':request.user.username}))
         
          else:
            return render(request, 'myapp/edit_info.html', {'form': form})


            

def edit_password(request):

     if request.method == 'POST':
        if request.user.is_authenticated:
          form = UpdatePasswordForm(request.user, request.POST)
          if form.is_valid():
               user = form.save()
               update_session_auth_hash(request, user)
               xmlrequest = request.headers.get('X-Requested-With')
               if xmlrequest == 'XMLHttpRequest':
                    return JsonResponse({'message':'Your password was succesfully updated!', 'username':request.user.username})
               
               return redirect(reverse('account', kwargs={'username':request.user.username}))
             
          
          else:
               errors = dict(form.errors) 
               xmlrequest = request.headers.get('X-Requested-With')
               print(errors)
               if xmlrequest == 'XMLHttpRequest':
                    
                    return JsonResponse({'errors': errors})

               messages.success(request, 'Old password incorrect. Please try again')
               return redirect('edit_password')
        
        else: 
             return redirect('member-login')
     
     else:
          form = UpdatePasswordForm(request.user)

         


     return render(request, 'myapp/edit_password.html', {'form':form})



def delete_account(request):
     if request.method == 'POST':
          user_choice = request.POST.get('delete_account')
          user_account= UserDetails.objects.filter(username=request.user.username).first() # returns the row that has the username=request.user.username
          user_result = UserResult.objects.filter(username=request.user.username).all() # return all rows in the database that has username=request.user.username
          if user_choice: 
           #loops and delete every row in the user_result
           for row in user_result:
                row.delete()
   
           if user_account:
                user_account.delete()
            
           messages.success(request, 'Successfully deleted your account')
           return redirect('memberlogin')
          
     return render(request, 'myapp/delete_account.html')





@receiver(post_save, sender=UserResult)
def handle_quiz_result(sender, instance, created, **kwargs):
     if created:

          print('an instance has been created')
       
          print(instance.score_percentage)
          from channels.layers import get_channel_layer
          from asgiref.sync import async_to_sync

          channel_layer = get_channel_layer()
          async_to_sync(channel_layer.group_send)(
            "chat_default_room",  # Group name for broadcasting
            {
                "type": "quiz_result",  # Custom handler name in consumers
                "message": "New quiz result available",  # Optional message data
                "username": instance.username,
                "subject": instance.subject,
                "score_percentage": instance.score_percentage,
                "user_pic": instance.profile_pic,
                "difference": instance.difference,
            }
        )

# result_list = [{"username":result.username, "subject":result.subject, "score_pct":result.score_percentage, "timestamp":result.posted_time,  "user_pic":result.profile_pic, "difference":result.difference} for result in user]
