from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import MatchViewSet, TeamStatsViewSet,PlayerViewSet,BatsmanStatsViewSet,BowlerStatsViewSet,BallViewSet,SetPlayerViewSet,InningsViewSet    

router = DefaultRouter()
router.register(r'players', PlayerViewSet)
router.register(r'matches', MatchViewSet)
router.register(r'teamstats', TeamStatsViewSet)
router.register(r'update-score',BallViewSet)
router.register(r'batsmanstats',BatsmanStatsViewSet)
router.register(r'bowlerstats',BowlerStatsViewSet)
router.register(r'setplayer',SetPlayerViewSet)
router.register(r'innings', InningsViewSet)


urlpatterns = [
    path('', include(router.urls)),
]


