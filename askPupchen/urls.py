"""askPupchen URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from askPupchen import settings
from AskPuchen import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.NewQuestions.as_view(), name='new_questions'),
    path('hot', views.HotQuestions.as_view(), name='hot_questions'),
    path('tag/<str:tag>', views.TagQuestions.as_view(), name='tag_questions'),
    path('question/<int:question_id>', views.QuestionView.as_view(), name='question'),
    path('signup', views.SignUp.as_view(), name='signup_url'),
    path('login', views.Login.as_view(), name='login_url'),
    path('ask', views.Ask.as_view(), name="ask")
]

# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
