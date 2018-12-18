from django.contrib import admin

from .models import Profile, Tag, Question, Answer


admin.site.register(Profile),
admin.site.register(Tag),
admin.site.register(Question),
admin.site.register(Answer)


# Register your models here.
