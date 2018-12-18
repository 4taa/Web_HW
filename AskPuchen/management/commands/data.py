# -*- coding: utf-8 -*-
from faker import Factory
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from AskPuchen.models import Question, Answer, Tag, Profile
from random import choice, randint


class Command(BaseCommand):
    faker = Factory.create()

    def add_arguments(self, parser):
        pass

    def create_users(self):

        for i in range(0, 3):
            u = User()
            u.username = self.faker.name()
            u.save()

            up = Profile()
            up.user = u

            up.save()

    def create_questions(self):
        users = User.objects.all()

        for user in users:
            q = Question()

            q.title = self.faker.sentence()
            q.text = self.faker.paragraph(),

            q.author = user
            q.save()

    def create_answers(self):
        users = User.objects.all()
        questions = Question.object.all()

        for question in questions:
            for i in range(0, randint(2, 5)):
                a = Answer()
                a.author = choice(users)
                a.text = self.faker.paragraph(),
                a.question = question
                a.correct = True if i == 0 else False
                a.save()


    def create_tags(self):
        tags = ['HTML', 'CSS', 'C++', 'iOS', 'MySQL', 'Objective-C']
        for tag in tags:
            if len(Tag.object.filter(title=tag)) == 0:
                t = Tag()
                t.title = tag
                t.save()

        tags = Tag.object.all()
        questions = Question.object.all()
        for question in questions:
            for tag in tags:
                t = tag

                if t not in question.tags.all():
                    question.tags.add(t)

    def handle(self, *args, **options):
        self.create_users()
        self.create_questions()
        self.create_answers()
        self.create_tags()
