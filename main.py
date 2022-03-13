class Team:

    def __init__(self):
        self.scores = []
        self.players_order = []
        self.next_player_idx = 1
        self.extras = {'Wd':0, 'Nb':0}

    def next_player(self):
        self.next_player_idx += 1
        if self.next_player_idx == len(self.players_order):
            return None # All out condition
        return self.players_order[self.next_player_idx]

    def set_player_orders(self, player_list):
        for player_val in player_list:
            player_obj = Player(player_val)
            self.players_order.append(player_obj)

    def get_total(self):
        total_score = self.get_extras()
        for score in self.scores:
            if score.isdigit():
                total_score+=int(score)
        return total_score


    def update_timeline(self,value):
        self.scores.append(value)

    def wickets_gone(self):
        return self.next_player_idx - 1

    def get_extras(self):
        return self.extras['Wd'] + self.extras['Nb']

    def get_opening_pair(self):
        return self.players_order[:2]

    def update_extras(self,value):
        self.extras[value]+=1



class Player:
    def __init__(self,name):
        self.runs_scored = 0
        self.name = name
        self.ball_played = []
        self.boundaries = {4:0, 6:0}

    def update_score(self,value):
        if value == "W":
            value = 0
        elif value in [4,6]:
            self.boundaries[value] += 1
        self.ball_played.append(value)
        self.runs_scored += value

    def get_runs_scored(self):
        return self.runs_scored



class Game:
    total_overs = 0
    def __init__(self):
        self.over = 0
        self.curr_idx = 0
        self.batting_pair = []
        self.teams = []

    def game_setup(self):
        print("Enter No. of players for team:")
        no_of_players = input()
        print("Enter No. of overs:")
        no_of_overs = input()
        self.total_overs = int(no_of_overs)

    def team_setup(self):
        print("Enter batting order")
        player_order = input()
        player_order = player_order.split(" ")
        self.batting_team = Team()
        self.batting_team.set_player_orders(player_order)
        self.batting_pair = self.batting_team.get_opening_pair()
        return self.batting_team

    def play(self):
        print("Team Data Updated")
        for _ in range(self.total_overs):
            print("Enter over details")
            over_list = input()
            over_list = over_list.split(" ")
            for ball in over_list:
                self.batting_team.update_timeline(ball)
                if ball.isdigit():
                    ball = int(ball)
                    self.batting_pair[self.curr_idx].update_score(ball)
                    if ball&1:
                        self.curr_idx = 1 - self.curr_idx
                elif ball == "W":
                    self.batting_pair[self.curr_idx].update_score(ball)
                    self.batting_pair[self.curr_idx] = self.batting_team.next_player()
                    if self.batting_pair[self.curr_idx] is None:
                        # print("All out!!")
                        break
                elif ball == "Wd" or ball == "Nb":
                    self.batting_team.update_extras(ball)
            self.over += 1
            self.curr_idx = 1 - self.curr_idx
            self.display_score_board()

    def game_play_for_team(self):
        self.game_setup()
        # team 1
        team1 = self.team_setup()
        self.teams.append(team1)
        self.play()
        # team 2
        team2 = self.team_setup()
        self.teams.append(team2)
        self.play()

        team1_score = team1.get_total()
        team2_score = team2.get_total()

        if team1_score > team2_score:
            print(f"Team 1 wins by {team1_score-team2_score} runs")
        elif team2_score > team1_score:
            print(f"Team 2 wins by {team2_score-team1_score} runs")
        else:
            print("Draw!")

    # Score Board
    def display_score_board(self):
        total_score = self.batting_team.get_extras()
        for player in self.batting_team.players_order:
            print(f"{player.name} | Runs -> {player.runs_scored} | 4s -> {player.boundaries[4]} | 6s -> {player.boundaries[6]} | Balls -> {len(player.ball_played)}")
            total_score+=player.runs_scored

        # print(str(len(self.batting_team.scores)/6) + "." + )
        print(f"Overs -> {self.over}")
        print(f"Total Score : {total_score}/{self.batting_team.wickets_gone()}")


game = Game()
game.game_play_for_team()

# Input Order
# 5
# 2
# P1 P2 P3 P4 P5
# 1 1 1 1 1 2
# W 4 4 Wd W 1 6

# P6 P7 P8 P9 P10
# 4 6 W W 1 1
# 6 1 W W
