from django.urls import path, include
from . import views
from django.conf import settings
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from .api import ElectronicsQuestionsAPI, ElectronicsChoicesAPI, CommunicationsQuestionsAPI, CommunicationsChoicesAPI, MathQuestionsAPI, MathChoicesAPI, GEASChoicesAPI, GEASQuestionsAPI



router = DefaultRouter()
router.register(r'elecsqn-api', ElectronicsQuestionsAPI, basename='electronicsquestions')
router.register(r'elecsopn-api', ElectronicsChoicesAPI, basename='electronicschoices')
router.register(r'commsqn-api', CommunicationsQuestionsAPI, basename='communicationsquestions')
router.register(r'commsopn-api', CommunicationsChoicesAPI, basename='communicationschoices')
router.register(r'mathqn-api', MathQuestionsAPI, basename='mathquestions')
router.register(r'mathopn-api', MathChoicesAPI, basename='mathchoices')
router.register(r'geasqn-api', GEASQuestionsAPI, basename='geasquestions')
router.register(r'geasopn-api', GEASChoicesAPI, basename='geaschoices')


urlpatterns = [
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
     path('profile/', views.profile, name='profile'),
     path('member-login/', views.memberlogin, name='memberlogin'),
     path('member-logout/', views.memberlogout, name='memberlogout'),
     path('electronics/', views.electronics, name='electronics'),
     path('elecsanswers/', views.elecsanswers, name='elecsanswers'),
     path('communications/', views.communications, name='communications'),
     path('commsanswers/', views.commsanswers, name='commsanswers'),
     path('math/', views.math, name='math'),
     path('mathanswers/', views.mathanswers, name='mathanswers'),
     path('geas/', views.geas, name='geas'),
     path('geasanswers/', views.geasanswers, name='geasanswers'),
     path('account/<str:username>/', views.account, name='account'),
     path('quizfeed/', views.quizfeed, name='quizfeed'),
     path('edit-information/', views.edit_information, name='edit_information'),
     path('edit-password/', views.edit_password, name='edit_password'),
     path('validate-username/', views.validate_username, name='validateUsername'),
     path('validate-email/', views.validate_email, name='validateEmail'),
     path('validate-password/', views.validate_password, name='validatePassword'),
     path('validate-passwords/', views.validate_passwords, name='validatePasswords'),
     path('validate-latest-username/', views.validate_latest_username, name='validateLatestUsername'),
     path('validate-latest-email/', views.validate_latest_email, name='validateLatestEmail'),
     path('delete/', views.delete_account, name='delete_account'),
     path('api/', include(router.urls)),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # this is for allowing media settings to handle user pictures or any media files