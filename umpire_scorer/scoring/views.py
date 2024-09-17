from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from .models import Team, Match, ScoreBoard,TeamStats,Player,BatsmanStats,BowlerStats,Ball,SetPlayer,Innings
from .serializers import TeamSerializer, MatchSerializer, ScoreBoardSerializer,TeamStatsSerializer,PlayerSerializer,BatsmanStatsSerializer,BowlerStatsSerializer,BallSerializer,SetPlayerSerializer,InningsSerializer


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    def get_queryset(self):
        team_id = self.request.query_params.get('team')
        if team_id:
            return self.queryset.filter(team_id=team_id)
        return self.queryset
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)  # partial=True for partial updates
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        instance.update_self()

        return Response(serializer.data)


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    
    def create(self, request):
        serializer = MatchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        instance.update_sellf()
        
        return Response(serializer.data)
    

    def get_queryset(self):
        id = self.request.query_params.get('match')
        if id:
            return self.queryset.filter(id=id)
        return self.queryset


    
class TeamStatsViewSet(viewsets.ModelViewSet):
    queryset = TeamStats.objects.all()
    serializer_class = TeamStatsSerializer   
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        instance.update_win_percentage()
        return Response(serializer.data)
    
class BatsmanStatsViewSet(viewsets.ModelViewSet):
    queryset = BatsmanStats.objects.all()
    serializer_class = BatsmanStatsSerializer

    # Overriding update method for partial updates
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        # Update related player stats
        instance.update_player()

        return Response(serializer.data)
    
    # Custom filtering based on query parameters
    def get_queryset(self):
        match_id = self.request.query_params.get('match')
        player_id = self.request.query_params.get('player')

        queryset = self.queryset
        
        if match_id:
            queryset = queryset.filter(match_id=match_id)
        
        if player_id:
            queryset = queryset.filter(player_id=player_id)
        
        return queryset
   

    

class BowlerStatsViewSet(viewsets.ModelViewSet):
    queryset = BowlerStats.objects.all()
    serializer_class = BowlerStatsSerializer

    # Optional: Overriding update method if needed
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        instance.update_player()

        player = instance.player
        player.update_self()

        return Response(serializer.data)
    
    def get_queryset(self):
        match_id = self.request.query_params.get('match')
        player_id = self.request.query_params.get('player')

        queryset = self.queryset
        
        if match_id:
            queryset = queryset.filter(match_id=match_id)
        
        if player_id:
            queryset = queryset.filter(player_id=player_id)
        
        return queryset
    


class BallViewSet(viewsets.ModelViewSet):
    queryset = Ball.objects.all()
    serializer_class = BallSerializer

    # Optional: Overriding update method if needed
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        instance.update_ball()

        return Response(serializer.data)
   
    def get_queryset(self):
        match = self.request.query_params.get('match')
        if match:
            return self.queryset.filter(match=match)
        return self.queryset
    
class SetPlayerViewSet(viewsets.ModelViewSet):
    queryset = SetPlayer.objects.all()
    serializer_class = SetPlayerSerializer


class InningsViewSet(viewsets.ModelViewSet):
    queryset = Innings.objects.all()
    serializer_class = InningsSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        partial = True  # Indicate that this is a partial update
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        try:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            # Optionally call custom methods
            if instance.result:
                instance.update_self()
                instance.save()

            return Response(serializer.data)
        except Exception as e:
            print(f"Error in update: {e}")
            return Response({"detail": "Internal Server Error"}, status=500)











    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)

    #     # After saving, update the win_percentage field
    #     instance.update_win_percentage()

    #     return Response(serializer.data, status=status.HTTP_200_OK)


class update_scoreViewSet(viewsets.ModelViewSet):
    queryset = ScoreBoard.objects.all()
    serializer_class = ScoreBoardSerializer













































class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


#     def post(request, match_id):

#         match = get_object_or_404(Match, pk=match_id)
        
#         if request.method == 'POST':
#             match = Match.objects.get(id=match_id)
#             batsman_id = request.POST.get('batsman_id')
#             bowler_id = request.POST.get('bowler_id')
#             runs = int(request.POST.get('runs'))
#             is_wicket = request.POST.get('is_wicket', False) == 'true'

#             # Update batsman stats
#             batsman = Player.objects.get(id=batsman_id)
#             batsman_stats = BatsmanStats.objects.get_or_create(player=batsman, match=match)[0]
#             batsman_stats.runs += runs
#             batsman_stats.balls_faced += 1
#             batsman_stats.strike_rate = (batsman_stats.runs / batsman_stats.balls_faced) * 100

#             if runs == 4:
#                 batsman_stats.fours += 1
#             elif runs == 6:
#                 batsman_stats.sixes += 1

#             batsman_stats.save()

#             # Update bowler stats
#             bowler = Player.objects.get(id=bowler_id)
#             bowler_stats = BowlerStats.objects.get_or_create(player=bowler, match=match)[0]
#             bowler_stats.runs_given += runs
#             bowler_stats.overs_bowled += 1/6
#             bowler_stats.economy_rate = bowler_stats.runs_given / bowler_stats.overs_bowled

#             if is_wicket:
#                 bowler_stats.wickets += 1

#             bowler_stats.save()

#             # Update match details (check if over is completed)
#             match.total_balls -= 1
#             if match.total_balls == 0:
#                 match.match_status = 'completed'
#             match.save()

#             return JsonResponse({'message': 'Score updated', 'match_status': match.match_status})
        
#         serializer = MatchSerializer(Match, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)


# def match_summary(request, match_id):
#     match = Match.objects.get(id=match_id)
#     batsman_stats = BatsmanStats.objects.filter(match=match)
#     bowler_stats = BowlerStats.objects.filter(match=match)

#     summary = {
#         'match_status': match.match_status,
#         'batsman_stats': list(batsman_stats.values('player__name', 'runs', 'balls_faced', 'fours', 'sixes', 'strike_rate')),
#         'bowler_stats': list(bowler_stats.values('player__name', 'overs_bowled', 'runs_given', 'dot_balls', 'wickets', 'economy_rate')),
#     }

#     return JsonResponse(summary)


# class ScoreBoardViewSet(viewsets.ModelViewSet):
#     queryset = ScoreBoard.objects.all()
#     serializer_class = ScoreBoardSerializer




# class IndividualScoreViewSet(viewsets.ModelViewSet):
#     queryset = IndividualScore.objects.all()
#     serializer_class = IndividualScoreSerializer

#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)

#         return Response(serializer.data, status=status.HTTP_200_OK)
    

# class UpdateScoreView(APIView):
#     def post(self, request, format=None):
#         data = request.data

#         bowler = Player.objects.get(id=data['bowlear_id'])
#         batsman = Player.objects.get(id=data['batsman_id'])
#         runs = data['runs']

#         # Update ball information
#         Ball.objects.create(
#             match_id=data['match_id'],
#             bowler=bowler,
#             batsman=batsman,
#             runs=runs,
#             is_boundary=(runs == 4),
#             is_six=(runs == 6),
#             is_wicket=data.get('is_wicket', False),
#             is_dot_ball=(runs == 0),
#             ball_number=data['ball_number']
#         )

#         # Update batsman stats
#         batsman.runs += runs
#         batsman.balls_faced += 1
#         if runs == 4:
#             batsman.fours += 1
#         if runs == 6:
#             batsman.sixes += 1
#         batsman.strike_rate = (batsman.runs / batsman.balls_faced) * 100
#         batsman.save()

#         # Update bowler stats
#         bowler.runs_given += runs
#         if runs == 0:
#             bowler.dot_balls += 1
#         bowler.economy_rate = (bowler.runs_given / (bowler.overs * 6)) if bowler.overs > 0 else 0
#         if data.get('is_wicket', False):
#             bowler.wickets += 1
#         bowler.save()

#         return Response({'message': 'Score updated successfully!'}, status=status.HTTP_200_OK)