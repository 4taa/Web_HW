from django.shortcuts import render, get_object_or_404
from django.views import View
from AskPuchen.models import Question, Tag, Answer
from AskPuchen.functions import paginate
import logging

logger = logging.getLogger(__name__)


# Create your views here.


class BaseView(View):
    def render(self, request, template, context):
        context.update({
            'authorized': request.user.is_authenticated,
            'user': {'name': request.user.username},
        })

        return render(request, template, context)


class NewQuestions(BaseView):
    def get(self, request):
        questions = Question.object.list_new()
        questions = paginate(request, questions)
        return super().render(request, 'index.html', {'questions': questions,
                                                      'title': 'New Questions',
                                                      'current': 'new'})


class HotQuestions(BaseView):
    def get(self, request):
        questions = Question.object.list_hot()
        questions = paginate(request, questions)
        return super().render(request, 'index.html', {'questions': questions,
                                                      'title': 'Hot Questions',
                                                      'current': 'hot'})


class TagQuestions(BaseView):
    def get(self, request, tag):
        tag = get_object_or_404(Tag, title=tag)
        questions = Question.object.list_tag(tag)
        questions = paginate(request, questions)
        return super().render(request, 'index.html', {'questions': questions,
                                                      'title': "Tag: {}".format(tag.title)})


class QuestionView(BaseView):
    def get(self, request, question_id):
        question = Question.object.get_single(question_id)
        answers = paginate(request, Answer.object.get_for_question(question), 10)
        return super().render(request, 'question.html', {'question': question,
                                                         'answers': answers})


class Ask(BaseView):
    def get(self, request):
        return super().render(request, 'ask.html', {})


class Login(BaseView):
    def get(self, request):
        return super().render(request, 'login.html', {})


class SignUp(BaseView):
    def get(self, request):
        return super().render(request, 'signup.html', {})
