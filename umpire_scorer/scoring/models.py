from django.db import models

class TeamStats(models.Model):
    name = models.CharField(max_length=100)
    matches_played = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    win_percentage = models.DecimalField(default=0.0,max_digits=4, decimal_places=2)

    def update_win_percentage(self):
        if self.matches_played > 0:
            self.win_percentage = (self.wins / self.matches_played) * 100
        else:
            self.win_percentage = 0.0
    
    def save(self, *args, **kwargs):
        self.update_win_percentage()
        super(TeamStats, self).save(*args, **kwargs)
   
    

class Match(models.Model):
    batting_team = models.ForeignKey(TeamStats, on_delete=models.CASCADE, related_name='batting_matches',null=True)
    bowling_team = models.ForeignKey(TeamStats, on_delete=models.CASCADE, related_name='bowling_matches',null=True)
    inning = models.IntegerField(default=1)
    date = models.DateField(auto_now_add=True,null=True)
    total_overs = models.FloatField(default=10)
    total_balls = models.IntegerField(default=0)
    match_status = models.CharField(max_length=10, default='LIVE')
    over_done = models.CharField(max_length=10,null=True)
    batting_team_score = models.IntegerField(default=0)
    batting_team_wicket = models.IntegerField(default=0)
    batting_team_extra_runs = models.IntegerField(default=0)
    
    def calculate_overs(self):
        if self.total_balls == 1:
            self.over_done = "0.1"
        elif self.total_balls == 2:
            self.over_done = "0.2"
        elif self.total_balls == 3:
            self.over_done = "0.3"
        elif self.total_balls == 4:
            self.over_done = "0.4"
        elif self.total_balls == 5:
            self.over_done = "0.5"
        else:
            self.over_done = self.total_balls // 6
            rem_ball = self.total_balls % 6
            self.over_done = f"{self.over_done}.{rem_ball}"


class Innings(models.Model):
    inning_1 = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='first_inning', null=True)
    inning_2 = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='second_inning', null=True)
    result = models.ForeignKey(TeamStats, on_delete=models.CASCADE, related_name="winner_team", null=True)

    def update_self(self):
        if self.result:
            try:
                # Update the winner's wins
                self.result.wins += 1
                self.result.update_win_percentage()
                self.result.save()

                # Update the loser's losses
                if self.result == self.inning_1.batting_team:
                    # Batting team won, bowling team lost
                    self.inning_1.bowling_team.losses += 1
                    self.inning_1.bowling_team.save()
                else:
                    # Bowling team won, batting team lost
                    self.inning_1.batting_team.losses += 1
                    self.inning_1.batting_team.save()
                self.inning_1.batting_team.matches_played += 1
                self.inning_1.bowling_team.matches_played += 1
                self.inning_1.batting_team.save()
                self.inning_1.bowling_team.save()

                for player in self.inning_1.batting_team.players.all():
                    player.matches_played += 1
                    player.save()

                for player in self.inning_1.bowling_team.players.all():
                    player.matches_played += 1
                    player.save()
                
            except Exception as e:
                print(f"Error in updating result stats: {e}")
                raise
        else:
            print("No result to update!")


class Player(models.Model):
    team = models.ForeignKey(TeamStats, related_name='players', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=50)

    matches_played = models.IntegerField(default=0)
    total_runs = models.IntegerField(default=0)
    total_balls_faced = models.IntegerField(default=0)
    best_score = models.IntegerField(default=0)
    total_4s = models.IntegerField(default=0)
    total_6s = models.IntegerField(default=0)
    total_30s = models.IntegerField(default=0)
    total_50s = models.IntegerField(default=0)
    total_wickets = models.IntegerField(default=0)
    total_overs_bowled = models.CharField(default='0.0',max_length=10)
    total_runs_given = models.IntegerField(default=0)
    total_dot_balls = models.IntegerField(default=0)
    economy_rate = models.DecimalField(default=0.0,max_digits=5, decimal_places=2)
    total_ball = models.IntegerField(default=1)

    def overs_to_balls(self,overs_str):
        if overs_str is None:
            # If the overs string is None, return 0 (indicating no balls bowled)
            return 0
        # Split the overs string by the decimal point
        if '.' in overs_str:
            full_overs, balls = overs_str.split('.')
            full_overs = int(full_overs)
            balls = int(balls)
        else:
            # If no decimal, all are full overs
            full_overs = int(overs_str)
            balls = 0

        # If the balls are 6 or more, it means another full over
        if balls >= 6:
            full_overs += 1
            balls = 0

        # Calculate total balls bowled
        total_balls = full_overs * 6 + balls
        return total_balls


    def update_self(self):
        try:
            # Convert overs from string to total balls bowled
            self.total_balls_bowled = self.overs_to_balls(self.total_overs_bowled)

            if self.total_balls_bowled != 0:
                # Calculate economy rate: runs per over (total balls / 6 gives overs)
                self.economy_rate = self.total_runs_given / (self.total_balls_bowled / 6)
            else:
                self.economy_rate = 0  # Set economy rate to 0 if no balls were bowled

        except ValueError:
            # Handle cases where self.total_overs_bowled is not a valid number
            print("Invalid overs value:", self.total_overs_bowled)
            self.economy_rate = 0  # Handle invalid overs input
    
    def save(self, *args, **kwargs):
        self.update_self()
        super(Player, self).save(*args, **kwargs)


class BatsmanStats(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    team = models.ForeignKey(TeamStats, on_delete=models.CASCADE)
    name = models.CharField(null=True, max_length=15)
    runs = models.IntegerField(default=0)
    balls_faced = models.IntegerField(default=0)
    fours = models.IntegerField(default=0)
    sixes = models.IntegerField(default=0)
    strike_rate = models.FloatField(default=0.0)
    isOut = models.BooleanField(default=False)
    outType = models.CharField(max_length=250, null=True, blank=True)
    outBy = models.CharField(max_length=250, null=True, blank=True)
    caughtBy = models.CharField(max_length=250, null=True, blank=True)

    # Method to update player stats based on the differences
    def update_player(self, prev_stats):
        if not self.player:
            return
        
        # Calculate the difference for all fields
        run_diff = self.runs - prev_stats['runs']
        ball_diff = self.balls_faced - prev_stats['balls_faced']
        four_diff = self.fours - prev_stats['fours']
        six_diff = self.sixes - prev_stats['sixes']

        # Incremental updates based on the difference
        self.player.total_runs += run_diff
        self.player.total_balls_faced += ball_diff
        self.player.total_4s += four_diff
        self.player.total_6s += six_diff

        # Update best score if current score is higher
        if self.runs > self.player.best_score:
            self.player.best_score = self.runs

        # Update 30s and 50s counts
        if self.runs >= 30 and prev_stats['runs'] < 30:
            self.player.total_30s += 1

        if self.runs >= 50 and prev_stats['runs'] < 50:
            self.player.total_30s -= 1  # If transitioning from 30 to 50
            self.player.total_50s += 1

        self.player.save()

    def save(self, *args, **kwargs):
        # Get the previous state of all attributes
        if self.pk:
            previous = BatsmanStats.objects.get(pk=self.pk)
            prev_stats = {
                'runs': previous.runs,
                'balls_faced': previous.balls_faced,
                'fours': previous.fours,
                'sixes': previous.sixes,
            }
        else:
            # If the object is new, set initial previous values to 0 or None
            prev_stats = {
                'runs': 0,
                'balls_faced': 0,
                'fours': 0,
                'sixes': 0,
            }

        super(BatsmanStats, self).save(*args, **kwargs)

        # After saving, update the player's stats based on the differences
        self.update_player(prev_stats)




class BowlerStats(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    team = models.ForeignKey(TeamStats, on_delete=models.CASCADE)
    name = models.CharField(null=True, max_length=15)
    ball1 = models.IntegerField(default=0)
    over = models.CharField(null=True, max_length=10)
    runs_given = models.IntegerField(default=0)
    dot_balls = models.IntegerField(default=0)
    wickets = models.IntegerField(default=0)
    economy_rate = models.FloatField(default=0.0)

    def calculate_overs(self):
        """Calculate the current over based on balls bowled."""
        # Total balls bowled = full overs * 6 + remaining balls
        full_overs = self.ball1 // 6
        remaining_balls = self.ball1 % 6
        self.over = f"{full_overs}.{remaining_balls}"  # Set over as string like "5.2" (5 overs and 2 balls)

    def update_player(self, prev_stats):
        """Update player's overall stats using previous BowlerStats."""
        # Calculate the current overs as total balls
        current_balls = self.ball1

        # Calculate previous overs from the previous stats (convert string to total balls)
        try:
            prev_over_split = prev_stats['over'].split('.')
            prev_full_overs = int(prev_over_split[0])
            prev_balls = int(prev_over_split[1])
            previous_balls = prev_full_overs * 6 + prev_balls
        except (ValueError, IndexError):
            previous_balls = 0

        # Calculate differences in runs, wickets, and dot balls
        runs_diff = (self.runs_given or 0) - (prev_stats['runs_given'] or 0)
        wickets_diff = (self.wickets or 0) - (prev_stats['wickets'] or 0)
        dot_balls_diff = (self.dot_balls or 0) - (prev_stats['dot_balls'] or 0)

        # Add the differences to player's total stats
        self.player.total_runs_given += runs_diff
        self.player.total_wickets += wickets_diff
        self.player.total_dot_balls += dot_balls_diff

        # Update the player's total overs bowled in terms of total balls
        total_player_balls = self.overs_to_balls(self.player.total_overs_bowled)
        updated_total_balls = total_player_balls + (current_balls - previous_balls)

        # Convert total balls back to overs format and update the player's total overs bowled
        full_overs = updated_total_balls // 6
        remaining_balls = updated_total_balls % 6
        self.player.total_overs_bowled = f"{full_overs}.{remaining_balls}"

        # Save updated player stats
        self.player.save()

    def overs_to_balls(self, overs_str):
        """Convert overs in 'x.y' format (e.g., 5.3) to total balls."""
        if '.' in overs_str:
            full_overs, balls = overs_str.split('.')
            full_overs = int(full_overs)
            balls = int(balls)
        else:
            full_overs = int(overs_str)
            balls = 0
        return full_overs * 6 + balls

    def save(self, *args, **kwargs):
        # Recalculate the current over before saving
        self.calculate_overs()

        # Get previous stats before saving the new ones
        if self.pk:
            previous = BowlerStats.objects.get(pk=self.pk)
            prev_stats = {
                'runs_given': previous.runs_given,
                'wickets': previous.wickets,
                'over': previous.over,
                'dot_balls': previous.dot_balls
            }
        else:
            # If the object is new, set previous values to defaults
            prev_stats = {
                'runs_given': 0,
                'wickets': 0,
                'over': "0.0",
                'dot_balls': 0
            }

        # Update the player stats based on the previous stats
        self.update_player(prev_stats)

        # Save the BowlerStats instance after updating the player
        super(BowlerStats, self).save(*args, **kwargs)




class Ball(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    batting_team = models.ForeignKey(TeamStats, on_delete=models.CASCADE, related_name='batting_teams')
    bowling_team = models.ForeignKey(TeamStats, on_delete=models.CASCADE, related_name='bowling_teams')
    batsman = models.ForeignKey(BatsmanStats, on_delete=models.CASCADE)
    runs = models.IntegerField(default=0)
    is_wicket = models.BooleanField(default=False)
    is_byes = models.BooleanField(default=False)
    is_legbyes = models.BooleanField(default=False)
    is_noball = models.BooleanField(default=False)
    is_wide = models.BooleanField(default=False)
    extra_runs = models.IntegerField(default=0)
    bowler = models.ForeignKey(BowlerStats, on_delete=models.CASCADE)

    def update_ball(self):

        # BATSMAN STATS
        
        if self.is_byes or self.is_legbyes or self.is_noball or self.is_wicket or self.is_wide :
            if self.is_byes:
                self.batsman.balls_faced += 1
                self.extra_runs += self.runs
            if self.is_legbyes:
                self.extra_runs += self.runs
            if self.is_wide:
                self.extra_runs +=1
                # self.extra_runs += self.runs+1
            if self.is_noball:
                self.extra_runs += 1
                self.batsman.runs += self.runs
                self.batsman.balls_faced += 1
            if self.is_wicket:
                self.batsman.runs += self.runs
                self.batsman.balls_faced += 1
                self.batsman.isOut=True

        else:
            self.batsman.runs += self.runs
            self.batsman.balls_faced += 1
            if self.runs == 4:
                self.batsman.fours += 1
            elif self.runs == 6:
                self.batsman.sixes += 1
        
        self.batsman.strike_rate = (self.batsman.runs / self.batsman.balls_faced) * 100
        self.batsman.save()

        
        # BOWLER STATS

        bowler_stats = self.bowler

        if self.is_byes or self.is_legbyes:
            bowler_stats.runs_given += 0 
            bowler_stats.ball1 += 1 
            bowler_stats.calculate_overs()
        else:
            if self.is_wide:
                bowler_stats.runs_given += self.runs+1
            elif self.is_noball:
                bowler_stats.runs_given += self.runs+1
            else:
                bowler_stats.runs_given += self.runs
                bowler_stats.ball1 += 1 
                bowler_stats.calculate_overs()

                
        bowler_stats.economy_rate = bowler_stats.runs_given / (bowler_stats.ball1/6)

        if self.runs==0 and self.extra_runs==0 or self.is_wicket:
            bowler_stats.dot_balls+=1

        if self.is_wicket:
            bowler_stats.wickets += 1

        bowler_stats.save()

        # TEAMSTATS
        
        if(self.extra_runs>0):
            if(self.is_byes or self.is_legbyes):
                self.match.batting_team_score += self.extra_runs
                self.match.batting_team_extra_runs += self.extra_runs
            else:
                self.match.batting_team_score += self.extra_runs+self.runs
                self.match.batting_team_extra_runs += self.extra_runs+self.runs
        else:
            self.match.batting_team_score += self.runs 
        if self.is_wicket:
            self.match.batting_team_wicket +=1

        if self.is_wide or  self.is_noball:
            self.match.calculate_overs()   
        else:
            self.match.total_balls += 1
            self.match.calculate_overs()

        
        if self.match.over_done == self.match.total_overs:
            self.match.match_status = 'completed'
        self.match.save()

    def save(self, *args, **kwargs):
        # Call the update_ball method when the ball is saved
        self.update_ball()
        super(Ball, self).save(*args, **kwargs)





class SetPlayer(models.Model):
    striker_batsman = models.ForeignKey(Player, on_delete=models.CASCADE,null=True,related_name='strike_batsman')
    non_striker_batsman = models.ForeignKey(Player, on_delete=models.CASCADE,null=True,related_name='non_strike_batsman')
    opening_bowler = models.ForeignKey(Player,on_delete=models.CASCADE,null=True,related_name='opeing_bowler')
















class ScoreBoard(models.Model):
    match = models.ForeignKey(Match, related_name='scores', on_delete=models.CASCADE)
    player = models.ForeignKey(Player, related_name='scores', on_delete=models.CASCADE)
    runs = models.IntegerField()
    wickets = models.IntegerField()
    overs = models.DecimalField(max_digits=4, decimal_places=1)
    balls_faced = models.IntegerField()

    def __str__(self):
        return f"{self.player.name} - {self.runs} runs"
    

class Team(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



    # class Player(models.Model):
#     team = models.ForeignKey(TeamStats, related_name='players', on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     role = models.CharField(max_length=50)  

#     matches_played = models.IntegerField(default=0)

#     batting_runs = models.IntegerField(default=0)
#     best_score = models.IntegerField(default=0)
#     thiries = models.IntegerField(default=0)
#     fifties = models.IntegerField(default=0)

#     overs = models.DecimalField(max_digits=4, decimal_places=1,default=0.0)
#     bowling_runs = models.IntegerField(default=0)
#     wickets = models.IntegerField(default=0)
#     eco_rate = models.DecimalField(default=0.0,max_digits=5, decimal_places=2)

#     def increment_matches(self):
#         self.matches_played += 1
#         self.save()

#     def increment_batting_runs(self,runs):
#         self.batting_runs += runs
#         self.save()
    
#     def update_best_score(self,runs):
#         if(runs>self.best_score):
#             self.best_score = runs
#         self.save()
    
#     def update_thirties(self,runs):
#         if(runs>=50):
#             self.fifties +=1
#         self.save()
    
#     def update_fifties(self,runs):
#         if(runs>=50):
#             self.fifties +=1
#         self.save()

#     def increment_overs(self,overs):
#         self.overs += overs
#         overs = overs.quantize(Decimal('0.0'))
#         self.save()

#     def increment_bowling_runs(self,runs):
#         self.bowling_runs += runs
#         self.save()

#     def increment_wickets(self,wickets):
#         self.wickets += wickets
#         self.save()

#     def update_eco_rate(self):
#         if self.matches_played>0:
#             self.eco_rate = self.bowling_runs/self.overs
#         else:
#             self.eco_rate = 0.0
#         self.save()

#     def __str__(self):
#         return self.name


# class IndividualScore(models.Model):
#     player = models.ForeignKey(Player, related_name='individual_scores', on_delete=models.CASCADE)
#     batting_runs = models.IntegerField(default=0)
#     balls_faced = models.IntegerField(default=0)
#     fours = models.IntegerField(default=0)
#     six = models.IntegerField(default=0)
#     strike_rate = models.DecimalField(default=0.0,max_digits=5, decimal_places=2)

#     overs = models.DecimalField(max_digits=4, decimal_places=1,default=0)
#     bowling_runs = models.IntegerField(default=0)
#     wickets = models.IntegerField(default=0)
#     eco_rate = models.DecimalField(default=0.0,max_digits=5, decimal_places=2)

#     def save(self, *args, **kwargs):
        
#         self.player.increment_matches()
#         self.player.increment_batting_runs(self.batting_runs)
#         self.player.update_best_score(self.batting_runs)
#         self.player.update_thirties(self.batting_runs)
#         self.player.update_fifties(self.batting_runs)

#         self.player.increment_overs(self.overs)
#         self.player.increment_bowling_runs(self.bowling_runs)
#         self.player.increment_wickets(self.wickets)
#         self.update_eco_rate()
#         super().save(*args, **kwargs)

#     def update_eco_rate(self):
#         if self.matches_played>0:
#             self.eco_rate = self.bowling_runs/self.overs
#         else:
#             self.eco_rate = 0.0
#         self.save()

#     def __str__(self):
#         return f"{self.player.name}"
