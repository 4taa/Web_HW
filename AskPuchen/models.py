from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.expressions import RawSQL
from django.db.models import Count, Sum, Prefetch


# Create your models here.

class Profile(models.Model):
    avatar = models.ImageField(upload_to='avatars', default='avatars/no.gif')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class TagManager(models.Manager):
    # adds number of questions to each tag
    def with_question_count(self):
        return self.annotate(questions_count=Count('question'))

    # sorts tags using number of questions
    def order_by_question_count(self):
        return self.with_question_count().order_by('-questions_count')

    # searches using title
    def get_by_title(self, title):
        return self.get(title=title)

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

    def with_likes(self):
        return self.annotate(likes=RawSQL('''
            SELECT IFNULL(SUM(value), 0) 
            FROM {QuestionLike} AS qlike 
            WHERE qlike.question_id = {Question}.id '''.format(
            Question=Question._meta.db_table,
            QuestionLike=QuestionLike._meta.db_table), ()))

    def order_by_popularity(self):
        return self.order_by('-likes')


class QuestionManager(models.Manager):
    def get_queryset(self):
        res = QuestionQuerySet(self.model, using=self._db)
        return res.with_answers_count().with_likes().with_author().with_tags()

    def list_new(self):
        return self.order_by('-date')

    def list_hot(self):
        return self.get_queryset().order_by_popularity()

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
    object = QuestionManager()


class AnswerQuerySet(models.QuerySet):
    def with_author(self):
        return self.select_related('author').select_related('author__profile')

    def with_likes(self):
        return self.annotate(likes=RawSQL('''
            SELECT IFNULL(SUM(value), 0) 
            FROM {AnswerLike} AS alike 
            WHERE alike.answer_id = {Answer}.id '''.format(
            Answer=Answer._meta.db_table,
            AnswerLike=AnswerLike._meta.db_table), ()))

    def order_by_popularity(self):
        return self.order_by('-likes')


class AnswerManager(models.Manager):
    def get_queryset(self):
        res = AnswerQuerySet(self.model, using=self._db)
        return res.with_likes().order_by_popularity()

    def get_for_question(self, question):
        return self.filter(question=question)


class Answer(models.Model):
    text = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    correct = models.BooleanField(default=False)
    object = AnswerManager()


class QuestionLike(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.SmallIntegerField(default=1)


class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.SmallIntegerField(default=1)