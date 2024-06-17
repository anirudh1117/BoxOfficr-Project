from django.contrib import admin
from .models import Celebrity, Biography, FilmIndustry, Role


admin.site.register(Celebrity)
admin.site.register(Biography)
admin.site.register(FilmIndustry)
admin.site.register(Role)