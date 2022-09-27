from django.contrib import admin

# Register your models here.
from .models import *

class IdAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Player, IdAdmin)
admin.site.register(Game, IdAdmin)
admin.site.register(Team, IdAdmin)
admin.site.register(Question, IdAdmin)
admin.site.register(QuestionHistory, IdAdmin)
admin.site.register(GameTurn, IdAdmin)
admin.site.register(Message, IdAdmin)