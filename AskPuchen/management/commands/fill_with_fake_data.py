# -*- coding: utf-8 -*-
from faker import Factory
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from AskPuchen.models import Question, Answer, Tag, Profile, AnswerLike, QuestionLike
from random import choice, randint


class Command(BaseCommand):
    help = 'Fills database with fake data'
    faker = Factory.create()

    USERS_COUNT = 3
    QUESTIONS_COUNT = 3
    TAGS_COUNT = 3
    MIN_ANSWERS = 2
    MAX_ANSWERS = 5

    def add_arguments(self, parser):
        pass

    def create_users(self):

        for i in range(0, self.USERS_COUNT):
            u = User()
            u.username = self.faker.name()
            u.save()

            up = Profile()
            up.user = u

            up.save()

    def create_questions(self):
        users = User.objects.all()

        for i in range(0, self.QUESTIONS_COUNT):
            q = Question()

            q.title = self.faker.sentence(nb_words=randint(4, 6),
                                          variable_nb_words=True)
            q.text = self.faker.paragraph(nb_sentences=randint(4, 13),
                                          variable_nb_sentences=True),

            q.author = choice(users)
            q.save()

    def create_answers(self):
        users = User.objects.all()
        questions = Question.object.all()

        for j in range(self.QUESTIONS_COUNT):
            for i in range(0, randint(self.MIN_ANSWERS, self.MAX_ANSWERS)):
                a = Answer()
                a.author = choice(users)
                a.text = self.faker.paragraph(nb_sentences=randint(2, 10),
                                              variable_nb_sentences=True),
                a.question = choice(questions)
                a.correct = True if i == 0 else False
                a.save()

    def create_likes(self):
        users = User.objects.all()
        questions = Question.object.all()
        answers = Answer.object.all()

        for j in range(0, self.QUESTIONS_COUNT):
            for i in range(0, randint(0, self.USERS_COUNT // 10)):
                like = QuestionLike()
                like.user = users[i]
                like.value = choice([-1, 1])
                like.question = questions
                like.save()

        for j in range(0, self.QUESTIONS_COUNT):
            for i in range(0, randint(0, self.USERS_COUNT // 10)):
                like = AnswerLike()
                like.user = users[i]
                like.value = choice([-1, 1])
                like.answer = answers
                like.save()

    def create_tags(self):
        tags = [
            'JavaScript', 'Java', 'C#', 'PHP', 'Android', 'JQuery', 'Python',
            'HTML', 'CSS', 'C++', 'iOS', 'MySQL', 'Objective-C',
            'SQL', '.net', 'RUBY', 'Swift', 'Vue', '1C'
        ]
        for tag in tags:
            if len(Tag.object.filter(title=tag)) == 0:
                t = Tag()
                t.title = tag
                t.save()

        tags = Tag.object.all()
        questions = Question.object.all()
        for question in questions:
            for i in range(0, self.TAGS_COUNT):
                t = choice(tags)

                if t not in question.tags.all():
                    question.tags.add(t)
            self.stdout.write('tagged question [%d]' % question.id)

    def handle(self, *args, **options):
        self.create_users()
        self.create_questions()
        self.create_answers()
        self.create_likes()
        self.create_tags()
