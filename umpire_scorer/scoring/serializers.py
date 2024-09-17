from rest_framework import serializers
from .models import Team,Match, ScoreBoard,TeamStats,Player,BatsmanStats,BowlerStats,Ball,SetPlayer,Innings

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'

class ScoreBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoreBoard
        fields = '__all__'


class TeamStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamStats 
        fields = '__all__'

class BatsmanStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatsmanStats
        fields = '__all__'  

class BowlerStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BowlerStats
        fields = '__all__'  

class BallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ball
        fields = '__all__'  

class SetPlayerSerializer(serializers.ModelSerializer):
     class Meta:
        model = SetPlayer
        fields = '__all__'  

class InningsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Innings
        fields = '__all__'




# class IndividualScoreSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = IndividualScore
#         fields = '__all__'
