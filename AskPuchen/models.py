from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Count


class Profile(models.Model):
    avatar = models.ImageField(upload_to='avatars', default='img/default.png')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class TagManager(models.Manager):
    def get_by_title(self, title):
        return self.get(title=title)

    def order_by_question_count(self):
        return self.with_question_count().order_by('-questions_count')

    def with_question_count(self):
        return self.annotate(questions_count=Count('question'))


class Tag(models.Model):
    title = models.CharField(max_length=30)
    object = TagManager()


class QuestionQuerySet(models.QuerySet):
    def with_tags(self):
        return self.prefetch_related('tags')

    def with_answers_count(self):
        return self.annotate(answers=Count('answer__id', distinct=True))

    def with_author(self):
        return self.select_related('author').select_related('author__profile')


class QuestionManager(models.Manager):
    def get_queryset(self):
        res = QuestionQuerySet(self.model, using=self._db)
        return res.with_answers_count().with_author().with_tags()

    def list_new(self):
        return self.order_by('-date')

    def list_hot(self):
        return self.get_queryset().with_answers_count()

    def list_tag(self, tag):
        return self.filter(tags=tag)

    def get_single(self, _id):
        res = self.get_queryset()
        return res.get(pk=_id)


class Question(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField(Tag)
    objects = QuestionManager()



class AnswerQuerySet(models.QuerySet):
    def with_author(self):
        return self.select_related('author').select_related('author__profile')


class AnswerManager(models.Manager):

    def get_queryset(self):
        res = AnswerQuerySet(self.model, using=self._db)
        return res

    def get_for_question(self, question):
        return self.filter(question=question)


class Answer(models.Model):
    text = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    correct = models.BooleanField(default=False)
    object = AnswerManager()