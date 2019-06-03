from django.contrib import admin

# Register your models here.
from events.models import Team, HotWord, SlackMessage, Utterance

admin.site.register(Team)
admin.site.register(HotWord)
admin.site.register(Utterance)
admin.site.register(SlackMessage)
