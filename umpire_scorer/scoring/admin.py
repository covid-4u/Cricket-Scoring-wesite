from django.contrib import admin
from .models import BatsmanStats,Ball,TeamStats,Player,BowlerStats,Match,Innings

# Register your model
admin.site.register(BatsmanStats)
admin.site.register(BowlerStats)
admin.site.register(Ball)
admin.site.register(TeamStats)
admin.site.register(Player)
admin.site.register(Match)
admin.site.register(Innings)
