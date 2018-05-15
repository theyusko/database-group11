CREATE TABLE matches (
	match_id varchar(25) PRIMARY KEY,
	date varchar(25),
	referee varchar(25),
	home_team varchar(25) not null,
	guest_team varchar(25) not null,
	home_score int DEFAULT 0,
	guest_score int DEFAULT 0,

	INDEX(home_team, guest_team),

	FOREIGN KEY (home_team) REFERENCES team(team_name) ON DELETE CASCADE,
	FOREIGN KEY (guest_team) REFERENCES team(team_name) ON DELETE CASCADE
);

CREATE TABLE positions(
	account_id varchar(25) NOT NULL,
	position varchar(25) NOT NULL,
	PRIMARY KEY(account_id, position),
	FOREIGN KEY (account_id) REFERENCES player(account_id) ON DELETE CASCADE
);

CREATE TABLE player(
	account_id varchar(25) PRIMARY KEY,
	password varchar(25) NOT NULL,
	name varchar(25) NOT NULL,
	surname varchar(25) NOT NULL,
	nationality varchar(25),
	age int,
	kit_no int,
	pref_foot varchar(10),
	prev_transfer_fee int NOT NULL,
	recovery_date varchar(25),
	suspend_date varchar(25),
	belong_to_team_name varchar(25) NOT NULL,

	INDEX login (account_id, password),
	INDEX team (belong_to_team_name),

	FOREIGN KEY (belong_to_team_name) REFERENCES team(team_name) ON DELETE CASCADE
);

CREATE TABLE president(
	account_id varchar(25) PRIMARY KEY,
	password varchar(25) not null,
	name varchar(25) not null,
	surname varchar(25) not null,
	nationality varchar(25),
	age int,
	start_date varchar(25),
	team_name varchar(25) not null,

	INDEX(account_id, password),
	INDEX(team_name),
	
	FOREIGN KEY (team_name) REFERENCES team(team_name) ON DELETE CASCADE
);

CREATE TABLE coach(
	account_id varchar(25) PRIMARY KEY,
	password varchar(25) not null,
	name varchar(25) not null,
	surname varchar(25) not null,
	nationality varchar(25),
	age int,
	start_date varchar(25),
	team_name varchar(25) not null,

	INDEX(account_id, password),
	INDEX(team_name),
	
	FOREIGN KEY (team_name) REFERENCES team(team_name) ON DELETE CASCADE
);

CREATE TABLE agent(
	account_id varchar(25) PRIMARY KEY,
	password varchar(25) not null,
	name varchar(25) not null,
	surname varchar(25) not null,
	nationality varchar(25),
	age int,
	player_account_id varchar(25) not null,

	INDEX(account_id, password),
	INDEX(player_account_id),
	
	FOREIGN KEY (player_account_id) REFERENCES player(account_id) ON DELETE CASCADE
);

CREATE TABLE team(
	team_name varchar(25) PRIMARY KEY,
	city varchar(25) not null,
	league varchar(25) not null,
	stadium_name varchar(25),
	budget int not null,
	establishment_date date,
	INDEX league (league),
	FOREIGN KEY (stadium_name) REFERENCES stadium(name) ON DELETE SET NULL);

CREATE TABLE stadium (
	name varchar(25) PRIMARY KEY,
	location varchar(25),
	capacity INT,
	start_date varchar(55)
);


CREATE TABLE plays_in(
	team_name varchar(25) NOT NULL,
	account_id varchar(25) NOT NULL,
	contract_start int,
	contract_end int NOT NULL,
	PRIMARY KEY(team_name, account_id),
	FOREIGN KEY (team_name) REFERENCES team(team_name) ON DELETE CASCADE,
	FOREIGN KEY (account_id) REFERENCES player(account_id) ON DELETE CASCADE
);

CREATE TABLE offer(
	offer_id varchar(25) PRIMARY KEY,
	offer_type varchar(25) NOT NULL,
	offer_amount int NOT NULL,
	contract_end int NOT NULL,
	status varchar(25) default 'ongoing',
	decidepresident_account_id varchar(25) NOT NULL,
	FOREIGN KEY (decidepresident_account_id) REFERENCES president(account_id)
);

CREATE TABLE trade (
	trade_id varchar(25) PRIMARY KEY,
	trade_type varchar(25) NOT NULL,
	trade_amount int NOT NULL,
	status varchar(25) default 'ongoing',
	decidepresident_account_id varchar(25) NOT NULL,
	
	INDEX(trade_type),

	FOREIGN KEY (decidepresident_account_id) REFERENCES president(account_id)
);

CREATE TABLE propose_offer (
	offer_id varchar(25),
	player_account_id varchar(25),
	president_account_id varchar(25),
	PRIMARY KEY (offer_id, player_account_id, president_account_id),
	FOREIGN KEY (offer_id) REFERENCES offer(offer_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (player_account_id) REFERENCES player(account_id) ON DELETE CASCADE, 
	FOREIGN KEY (president_account_id) REFERENCES president(account_id)
);

CREATE TABLE propose_trade (
	trade_id varchar(25),
	player_account_id varchar(25),
	president_account_id varchar(25),
	PRIMARY KEY (trade_id, player_account_id, president_account_id),
	FOREIGN KEY (trade_id) REFERENCES trade(trade_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (player_account_id) REFERENCES player(account_id) ON DELETE CASCADE, 
	FOREIGN KEY (president_account_id) REFERENCES president(account_id)
);

CREATE TABLE participates_in (
	account_id varchar(25),
	match_id varchar(25),
	PRIMARY KEY (account_id, match_id),
	FOREIGN KEY (account_id) REFERENCES player(account_id) ON DELETE CASCADE,
	FOREIGN KEY (match_id) REFERENCES matches(match_id) ON DELETE CASCADE);

CREATE TABLE statistics (
	match_id varchar(25),
	team_name varchar(25),
	account_id varchar(25) DEFAULT NULL,
	type varchar(25),
	value int not null,
	PRIMARY KEY (match_id, team_name, account_id, type), 
	FOREIGN KEY (match_id) REFERENCES matches(match_id) ON DELETE CASCADE,
	FOREIGN KEY (team_name) REFERENCES team(team_name) ON DELETE CASCADE,
	FOREIGN KEY (account_id) REFERENCES player(account_id) ON DELETE CASCADE);


CREATE VIEW leagues(league) 
AS SELECT distinct league FROM team

CREATE VIEW team_names(team_name)
AS SELECT team_name FROM team

CREATE VIEW team_wins(team_name, win_count) 
AS SELECT team_name, count(match_id) AS win_count
FROM matches, team_names
WHERE ( home_team = team_name AND home_score > guest_score ) OR ( guest_team = team_name AND home_score < guest_score )
GROUP BY team_name

CREATE VIEW team_draws(team_name, draw_count) 
AS SELECT team_name, count(match_id) AS draw_count
FROM matches, team_names
WHERE ( home_team = team_name OR guest_team = team_name ) AND home_score = guest_score
GROUP BY team_name

CREATE VIEW team_losses(team_name, loss_count) 
AS SELECT team_name, count(match_id) AS loss_count
FROM matches, team_names
WHERE ( home_team = team_name AND home_score < guest_score ) OR ( guest_team = team_name AND home_score > guest_score )
GROUP BY team_name


DELIMITER $
CREATE TRIGGER update_matches_insert AFTER INSERT ON statistics
FOR EACH ROW
BEGIN 
UPDATE matches 
SET home_score = home_score + NEW.value WHERE match_id = NEW.match_id AND NEW.team_name = home_team AND NEW.type = 'goal';
UPDATE matches 
SET guest_score = guest_score + NEW.value WHERE match_id = NEW.match_id AND NEW.team_name = guest_team AND NEW.type = 'goal';
END; $
DELIMITER ;

DELIMITER $
CREATE TRIGGER update_matches_update AFTER UPDATE ON statistics
FOR EACH ROW
BEGIN 
UPDATE matches 
SET home_score = home_score + NEW.value - OLD.value WHERE match_id = NEW.match_id AND NEW.team_name = home_team AND NEW.type = 'goal';
UPDATE matches 
SET guest_score = guest_score + NEW.value - OLD.value WHERE match_id = NEW.match_id AND NEW.team_name = guest_team AND NEW.type = 'goal';
END; $
DELIMITER ;

