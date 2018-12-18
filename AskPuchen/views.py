from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views import View
from AskPuchen.models import Question, Tag, Answer

class BaseView(View):
    def render(self, request, template, context):
        context.update({
            'authorized': request.user.is_authenticated,
            'user': {'name': request.user.username},
        })
        return render(request, template, context)


class NewQuestions(BaseView):
    def get(self, request):
        questions_lists = Question.object.list_new()
        paginator = Paginator(questions_lists, 5)
        page = request.GET.get('page')
        questions = paginator.get_page(page)
        return super().render(request, 'index.html', {'questions': questions,
                                                      'title': 'New Questions',
                                                      'current': 'new'})


class HotQuestions(BaseView):
    def get(self, request):
        questions_lists = Question.object.list_hot()
        paginator = Paginator(questions_lists, 5)
        page = request.GET.get('page')
        questions = paginator.get_page(page)
        return super().render(request, 'index.html', {'questions': questions,
                                                      'title': 'Hot Questions',
                                                      'current': 'hot'})


class TagQuestions(BaseView):
    def get(self, request, tag):
        tag = get_object_or_404(Tag, title=tag)
        questions_lists = Question.object.list_tag(tag)
        paginator = Paginator(questions_lists, 5)
        page = request.GET.get('page')
        questions = paginator.get_page(page)
        return super().render(request, 'index.html', {'questions': questions,
                                                      'title': "Tag: {}".format(tag.title)})


class QuestionView(BaseView):
    def get(self, request, question_id):
        question = Question.object.get_single(question_id)
        answers_lists = Answer.object.get_for_question(question)
        paginator = Paginator(answers_lists, 5)
        page = request.GET.get('page')
        answers = paginator.get_page(page)
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