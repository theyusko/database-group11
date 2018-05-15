from django.db import models
from datetime import datetime


# Create your models here.
class Posts(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(default=datetime.now(), blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Posts"

class Player(models.Model):
    account_id = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    nationality = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    kit_no = models.IntegerField(default=0)
    pref_foot = models.CharField(max_length=20)
    prev_transfer_fee = models.IntegerField(default=0)
    recovery_date = models.DateField(null=True, blank=True)
    suspend_date = models.DateField(null=True, blank=True)
    belong_to_team_name = models.ForeignKey('Team', on_delete=models.CASCADE, db_column="belong_to_team_name")

    def __str__(self): 
        x = self.name + " " + self.surname
        return x

class Position(models.Model):
    account_id = models.ForeignKey('Player', on_delete=models.CASCADE, db_column="account_id")
    position = models.CharField(max_length=20)

    def __str__(self):
        return self.position

class President(models.Model):
    account_id = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    nationality = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    start_date = models.DateField()
    team_name = models.ForeignKey('Team', on_delete=models.CASCADE, db_column="team_name")

    def __str__(self):
        return (self.name + " " + self.surname)

class Coach(models.Model):
    account_id = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    nationality = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    start_date = models.DateField()
    team_name = models.ForeignKey('Team', on_delete=models.CASCADE, db_column="team_name")

    def __str__(self):
        return (self.name + " " + self.surname)

class Agent(models.Model):
    account_id = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    nationality = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    player_id = models.ForeignKey('Player', on_delete=models.CASCADE, db_column="player_id")

    def __str__(self):
        return (self.name + " " + self.surname)

class Team(models.Model):
    team_name = models.CharField(max_length=20, primary_key=True)
    city = models.CharField(max_length=20)
    league_place = models.IntegerField(default=0)
    stadium_name = models.ForeignKey('Stadium', on_delete=models.CASCADE, db_column="stadium_name")
    budget = models.IntegerField(default=0)
    establishment_date = models.DateField()

    def __str__(self):
        return self.team_name

class Match(models.Model):
    match_id = models.IntegerField(primary_key=True)
    match_date = models.DateField()
    referee = models.CharField(max_length=20)
    home_team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='home_team', db_column="home_team")
    guest_team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='guest_team', db_column="guest_team")
    score = models.CharField(max_length=20)

    def __str__(self):
        return (self.home_team + " vs " + self.guest_team + "; score: " + self.score)

class Stadium(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    location = models.CharField(max_length=20)
    capacity = models.IntegerField(default=0)
    start_date = models.DateField()

    def __str__(self):
        return self.name

class PlaysIn(models.Model):
    team_name = models.ForeignKey('Team', on_delete=models.CASCADE, db_column="team_name")
    account_id = models.ForeignKey('Player', on_delete=models.CASCADE, db_column="account_id")
    player_name = models.CharField(max_length=20)
    contract_start = models.DateField()
    contract_end = models.DateField()

    def __str__(self):
        return (self.player_name + " - " + self.team_name)

class Offer(models.Model):
    offer_id = models.IntegerField(primary_key=True)
    offer_type = models.BooleanField()
    offer_amount = models.IntegerField(default=0)
    contract_start = models.DateField()
    contract_end = models.DateField()
    deciding_president = models.ForeignKey('President', on_delete=models.CASCADE, db_column="deciding_president")

class Trade(models.Model):
    trade_id = models.IntegerField(primary_key=True)
    trade_amount = models.IntegerField(default=0)
    time_limit = models.DateField()
    no_players = models.IntegerField(default=0)
    deciding_president = models.ForeignKey('President', on_delete=models.CASCADE, db_column="deciding_president")

class ProposeOffer(models.Model):
    offer_id = models.ForeignKey('Offer', on_delete=models.CASCADE, db_column="offer_id")
    player_id = models.ForeignKey('Player', on_delete=models.CASCADE, db_column="player_id")
    president_id = models.ForeignKey('President', on_delete=models.CASCADE, db_column="president_id")

class ProposeTrade(models.Model):
    trade_id = models.ForeignKey('Trade', on_delete=models.CASCADE, db_column="trade_id")
    player_id = models.ForeignKey('Player', on_delete=models.CASCADE, db_column="player_id")
    president_id = models.ForeignKey('President', on_delete=models.CASCADE, db_column="president_id")

class ParticipatesIn(models.Model):
    player_id = models.ForeignKey('Player', on_delete=models.CASCADE, db_column="player_id")
    match_id = models.ForeignKey('Match', on_delete=models.CASCADE, db_column="match_id")

class Statistics(models.Model):
    match_id = models.ForeignKey('Match', on_delete=models.CASCADE, db_column="match_id")
    team_name = models.ForeignKey('Team', on_delete=models.CASCADE, db_column="team_name")
    player_id = models.ForeignKey('Player', on_delete=models.CASCADE, db_column="player_id")
    type = models.CharField(max_length=20)
    value = models.CharField(max_length=20)