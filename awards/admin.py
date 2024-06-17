from django.contrib import admin

from .models import Award, AwardCategory, AwardEvent, Nomination

admin.site.register(Award)
admin.site.register(AwardCategory)
admin.site.register(AwardEvent)


class NominationAdmin(admin.ModelAdmin):
    list_display = ('category', 'event', 'person', 'movie', 'winner')
    list_filter = ('event__year',)


admin.site.register(Nomination, NominationAdmin)
