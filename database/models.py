from django.db import models


class Player(models.Model):
    account_id = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    nationality = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    kit_no = models.IntegerField(default=0)
    pref_foot = models.BooleanField(default=True)
    prev_transfer_fee = models.IntegerField(default=0)
    recovery_date = models.DateField(null=True, blank=True)
    suspend_date = models.DateField(null=True, blank=True)
    belong_to_team_name = models.ForeignKey('Team', on_delete=models.CASCADE)

    def __str__(self):
        return ("name: " + self.name +
                ", surname: " + self.surname +
                ", nationality: " + self.nationality +
                ", age: " + str(self.age) +
                ", kit_no: " + str(self.kit_no) +
                ", pref_foot: " + str(self.pref_foot) +
                ", prev_transfer_fee: " + str(self.prev_transfer_fee) +
                ", recovery_date: " + str(self.recovery_date) +
                ", suspend_date: " + str(self.suspend_date) +
                ", belongs_to: " + str(self.belong_to_team_name)
                )


class Position(models.Model):
    account_id = models.ForeignKey('Player', on_delete=models.CASCADE)
    position = models.CharField(max_length=20)

    def __str__(self):
        return ("player: " + str(self.account_id) +
                ", position: " + self.position
                )


class President(models.Model):
    account_id = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    nationality = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    start_date = models.DateField()
    team_name = models.ForeignKey('Team', on_delete=models.CASCADE)

    def __str__(self):
        return ("name: " + self.name +
                ", surname: " + self.surname +
                ", nationality: " + self.nationality +
                ", age: " + str(self.age) +
                ", start_date: " + str(self.start_date) +
                ", team: " + str(self.team_name)
                )


class Coach(models.Model):
    account_id = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    nationality = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    start_date = models.DateField()
    team_name = models.ForeignKey('Team', on_delete=models.CASCADE)

    def __str__(self):
        return ("name: " + self.name +
                ", surname: " + self.surname +
                ", nationality: " + self.nationality +
                ", age: " + str(self.age) +
                ", start_date: " + str(self.start_date) +
                ", team: " + str(self.team_name)
                )


class Agent(models.Model):
    account_id = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    nationality = models.CharField(max_length=20)
    birth_date = models.DateField()
    player_id = models.ForeignKey('Player', on_delete=models.CASCADE)
    player_name = models.CharField(max_length=20)

    def __str__(self):
        return ("name: " + self.name +
                ", surname: " + self.surname +
                ", nationality: " + self.nationality +
                ", birth_date: " + str(self.birth_date) +
                ", player_name: " + str(self.player_name)
                )


class Team(models.Model):
    team_name = models.CharField(max_length=20, primary_key=True)
    city = models.CharField(max_length=20)
    league_place = models.IntegerField(default=0)
    stadium_name = models.ForeignKey('Stadium', on_delete=models.CASCADE)
    budget = models.IntegerField(default=0)
    establishment_date = models.DateField()

    def __str__(self):
        return ("team_name: " + self.team_name +
                ", city: " + self.city +
                ", league_place: " + str(self.league_place) +
                ", stadium_name: " + self.stadium_name.name +
                ", budget: " + str(self.budget) +
                ", establishment_date: " + str(self.establishment_date)
                )


class Match(models.Model):
    match_id = models.IntegerField(primary_key=True)
    match_date = models.DateField()
    referee = models.CharField(max_length=20)
    home_team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='home_team')
    guest_team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='guest_team')
    score = models.CharField(max_length=20)

    def __str__(self):
        return ("match_id: " + str(self.match_id) +
                ", match_date: " + str(self.match_date) +
                ", referee: " + self.referee +
                ", home_team: " + self.home_team.team_name +
                ", guest_team: " + self.guest_team.team_name +
                ", score: " + self.score
                )


class Stadium(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    location = models.CharField(max_length=20)
    capacity = models.IntegerField(default=0)
    start_date = models.DateField()

    def __str__(self):
        return ("name: " + self.name +
                ", location: " + self.location +
                ", capacity: " + str(self.capacity) +
                ", start_date: " + str(self.start_date)
                )


class PlaysIn(models.Model):
    team_name = models.ForeignKey('Team', on_delete=models.CASCADE)
    account_id = models.ForeignKey('Player', on_delete=models.CASCADE)
    player_name = models.CharField(max_length=20)
    contract_start = models.DateField()
    contract_end = models.DateField()

    def __str__(self):
        return ("team_name: " + self.team_name.team_name +
                ", player_name: " + self.player_name +
                ", contract_start: " + str(self.contract_start) +
                ", contract_end: " + str(self.contract_end)
                )


class Offer(models.Model):
    offer_id = models.IntegerField(primary_key=True)
    offer_type = models.BooleanField()
    offer_amount = models.IntegerField(default=0)
    contract_start = models.DateField()
    contract_end = models.DateField()
    deciding_president = models.ForeignKey('President', on_delete=models.CASCADE)

    def __str__(self):
        return ("offer_type: " + str(self.offer_type) +
                ", offer_amount: " + str(self.offer_amount) +
                ", contract_start: " + str(self.contract_start) +
                ", contract_end: " + str(self.contract_end) +
                ", deciding_president: " + self.deciding_president.name
                )


class Trade(models.Model):
    trade_id = models.IntegerField(primary_key=True)
    trade_amount = models.IntegerField(default=0)
    time_limit = models.DateField()
    no_players = models.IntegerField(default=0)
    deciding_president = models.ForeignKey('President', on_delete=models.CASCADE)

    def __str__(self):
        return ("trade_id: " + str(self.trade_id) +
                ", trade_amount: " + str(self.trade_amount) +
                ", time_limit: " + str(self.time_limit) +
                ", no_players: " + str(self.no_players) +
                ", deciding_president: " + self.deciding_president.name
                )


class ProposeOffer(models.Model):
    offer_id = models.ForeignKey('Offer', on_delete=models.CASCADE)
    player_id = models.ForeignKey('Player', on_delete=models.CASCADE)
    president_id = models.ForeignKey('President', on_delete=models.CASCADE)

    def __str__(self):
        return ("offer_id: " + str(self.offer_id.offer_id) +
                ", player_name: " + self.player_id.name +
                ", president_name: " + self.president_id.name
                )


class ProposeTrade(models.Model):
    trade_id = models.ForeignKey('Trade', on_delete=models.CASCADE)
    player_id = models.ForeignKey('Player', on_delete=models.CASCADE)
    president_id = models.ForeignKey('President', on_delete=models.CASCADE)

    def __str__(self):
        return ("trade_id: " + str(self.trade_id.trade_id) +
                ", player_name: " + str(self.player_id.name) +
                ", president_name: " + str(self.president_id.name)
                )


class ParticipatesIn(models.Model):
    player_id = models.ForeignKey('Player', on_delete=models.CASCADE)
    match_id = models.ForeignKey('Match', on_delete=models.CASCADE)

    def __str__(self):
        return ("player_name: " + self.player_id.name +
                ", match_id: " + str(self.match_id.match_id)
                )


class Statistics(models.Model):
    match_id = models.ForeignKey('Match', on_delete=models.CASCADE)
    team_name = models.ForeignKey('Team', on_delete=models.CASCADE)
    player_id = models.ForeignKey('Player', on_delete=models.CASCADE)
    type = models.CharField(max_length=20)
    value = models.CharField(max_length=20)

    def __str__(self):
        return ("match_id: " + str(self.match_id.match_id) +
                ", team_name: " + self.team_name.team_name +
                ", player_name: " + self.player_id.name +
                ", type: " + self.type +
                ', value: ' + self.value
                )
