SCORE_MAP = {0: "Love",
             1: "15",
             2: "30",
             3: "40",
             4: "40"}
MATCHTYPE_MAP = {1: "bo3",
                 2: "bo5",
                 3: "gsbo5"}
SCOPE_COMMANDS = {"TRACKER": ["add match", "print matches", "switch"],
                  "MATCH": ["add set", "add set tiebreaker", "switch", "status", "reset", "print sets", "up"],
                  "SET": ["add game", "switch", "status",  "reset", "print games", "up"],
                  "GAME": ["add score", "status", "reset", "up"]}
### TESTING ONLY ###
#SCOPE_COMMANDS = {"TRACKER": ["add match", "print matches", "switch"],
#                  "MATCH": ["add set", "add set tiebreaker", "switch", "status", "reset", "print sets", "up"],
#                  "SET": ["add game", "switch", "status", "reset", "print games", "up", "p1w", "p2w", "tie"],
#                  "GAME": ["add score", "status", "reset", "up", "deuce", "p1w", "p2w"]}


def integer_validation(func_name):
    """function decorator that catches int(string) exceptions from bad input"""
    def input_validation(*args, **kwargs):
        try:
            return func_name(*args, **kwargs)
        except ValueError:
            print(f"{func_name.__name__} only takes numbers as the argument")
    return input_validation


def container_validation(func_name):
    """function decorator that catches KeyError exceptions from bad input
    example, choice of option 1 or 2, but user inputs 3"""
    def input_validation(*args, **kwargs):
        try:
            func_name(*args, **kwargs)
        except KeyError:
            print(f"{func_name.__name__} input is not a valid number option")
    return input_validation


def help_print(scope: str):
    print("Valid commands for this scope:")
    for command in SCOPE_COMMANDS[scope]:
        print(f"\t{command}")
    print("\thelp")
    print("\tquit")


### TESTING DECORATOR ONLY ###
def disabled(f):
    """decorator to disable a function. only surrounds class test functions"""
    def _decorator():
        print(f"{f.__name__} has been disabled")
    return _decorator


class Tracker:
    """The uppermost scope. Can contain any number of matches of three different kinds"""
    def __init__(self) -> None:
        self.id = 1
        self.matches = {}
        self.active_match = None

    @container_validation
    @integer_validation
    def add_match(self) -> None:
        match_type = int(input("Enter 1 for Bo3, 2 for Bo5, or 3 for Bo5 Grand Slam: "))
        if match_type not in MATCHTYPE_MAP:
            print("Input must be 1, 2, or 3 to correspond to Bo3, Bo5, Bo5 Grand Slam")
        else:
            self.matches[len(self.matches) + 1] = Match(len(self.matches) + 1, match_type)
            print(f"{MATCHTYPE_MAP[match_type]} match added. Match ID is {self.matches[len(self.matches)].match_id}")

    @integer_validation
    def switch_match(self) -> bool:
        """Picks the match to change into based on user input"""
        if not self.matches:
            print("There are no matches!")
            return False

        match_id = int(input("Enter match ID to switch to: "))
        if match_id in self.matches:
            self.active_match = self.matches[match_id]
            print(f"Switched to match {match_id}")
            return True
        else:
            print(f"Match ID {match_id} not found.")
            return False

    def print_matches(self) -> None:
        """Prints all matches contained in Tracker class"""
        if not self.matches:
            print("There are no matches!")
        else:
            for match_id, match in self.matches.items():
                if match.winner == "In progress":
                    print(f"Match {match_id} | Bo{match.match_set_max} | Grand Slam: {match.grand_slam} --> {match.winner}")
                else:
                    print(f"Match {match_id} | Bo{match.match_set_max} | Grand Slam: {match.grand_slam} --> Player {match.winner} won")


class Match:
    """The second layer scope. Can contain up to 3 or 5 Sets per instance"""
    def __init__(self, match_id, match_type) -> None:
        if match_type == 3:
            self.grand_slam = True
        else:
            self.grand_slam = False
        self.match_id = match_id
        self.match_set_max = int(MATCHTYPE_MAP[match_type][-1])

        self.set_list = []
        self.active_set = None
        self.winner = "In progress"

    def add_set(self, tiebreaker=False) -> None:
        """Adds a Set to the Match. Depending on inpout, can be a regular Set or TieBreaker Set"""
        if len(self.set_list) < self.match_set_max:
            if any(tennis_set.winner == "In progress" for tennis_set in self.set_list):
                print("At least one set present that is still In progress. Not adding another set.")
            else:
                if tiebreaker:
                    self.set_list.append(TieBreakerSet(len(self.set_list) + 1, is_gs=self.grand_slam))
                    print(f"Tiebreaker Set added. Set ID is {self.set_list[len(self.set_list) - 1].set_id}")
                else:
                    self.set_list.append(AdvantageSet(len(self.set_list) + 1))
                    print(f"Advantage Set added. Set ID is {self.set_list[len(self.set_list) - 1].set_id}")
        else:
            print("Maximum number of sets for this match already reached!")

    def is_complete(self) -> None:
        """Checks status of match and sees if complete"""
        score_count = {1: 0, 2: 0}
        for tennis_set in self.set_list:
            if tennis_set.winner != "In progress":
                if tennis_set.winner == 1:
                    score_count[1] += 1
                elif tennis_set.winner == 2:
                    score_count[2] += 1

        if self.match_set_max == 3:
            if score_count[1] == 2:
                self.winner = 1
                print(f"Match is complete! Player {self.winner} won. Set score is {score_count[1]}-{score_count[2]}")
            elif score_count[2] == 2:
                self.winner = 2
                print(f"Match is complete! Player {self.winner} won. Set score is {score_count[1]}-{score_count[2]}")
            else:
                print(f"Match is ongoing. Set score is {score_count[1]}-{score_count[2]}")
        elif self.match_set_max == 5:
            if score_count[1] == 3:
                self.winner = 1
                print(f"Match is complete! Player {self.winner} won. Set score is {score_count[1]}-{score_count[2]}")
            elif score_count[2] == 3:
                self.winner = 2
                print(f"Match is complete! Player {self.winner} won. Set score is {score_count[1]}-{score_count[2]}")
            else:
                print(f"Match is ongoing. Set score is {score_count[1]}-{score_count[2]}")

    def reset_match(self) -> None:
        """Wipes the match clean"""
        self.winner = "In progress"
        self.set_list = []
        print(f"Match has been reset.")

    def print_sets(self) -> None:
        """Prints all Sets in this Match"""
        if not self.set_list:
            print("Set list is empty!")
        else:
            for tennis_set in self.set_list:
                if tennis_set.winner != "In progress":
                    print(f"Set {tennis_set.set_id} ({type(tennis_set).__name__}) --> Player {tennis_set.winner} won")
                else:
                    print(f"Set {tennis_set.set_id} ({type(tennis_set).__name__}) --> {tennis_set.winner}")

    @integer_validation
    def switch_set(self) -> bool:
        """Picks the set to change into based on user input"""
        set_id = int(input("Enter set number to switch to: "))

        for tennis_set in self.set_list:
            if set_id == tennis_set.set_id:
                self.active_set = tennis_set
                print(f"Switched to set number {set_id}")
                return True
        print(f"Set number {set_id} does not exist.")
        return False


class AdvantageSet:
    """The third layer scope. Can possibly contain an unlimited number of games"""
    def __init__(self, set_id) -> None:
        self.set_id = set_id
        self.game_list = []
        self.active_game = None
        self.play_to = 6
        self.winner = "In progress"

    def add_game(self) -> None:
        """Adds a Game to the Set. Will always be a regular Game in this class"""
        if self.winner != "In progress":
            print(f"Set is already complete! Player {self.winner} won.")
        else:
            if any(game.winner == "In progress" for game in self.game_list):
                print("At least one game present that is still In progress. Not adding another game.")
            else:
                self.game_list.append(Game(len(self.game_list) + 1))
                print(f"Game added. Game ID is {self.game_list[len(self.game_list) - 1].game_id}")

    def is_complete(self) -> None:
        """Checks status of set and sees if complete"""
        score_count = {1: 0, 2: 0}
        for game in self.game_list:
            if game.winner:
                if game.winner == 1:
                    score_count[1] += 1
                elif game.winner == 2:
                    score_count[2] += 1

        if score_count[1] >= self.play_to and score_count[1] - score_count[2] >= 2:
            self.winner = 1
            print(f"Set is complete! Player {self.winner} won. Total game score is {score_count[1]}-{score_count[2]}")
        elif score_count[2] >= self.play_to and score_count[2] - score_count[1] >= 2:
            self.winner = 2
            print(f"Set is complete! Player {self.winner} won. Total game score is {score_count[1]}-{score_count[2]}")
        else:
            print(f"Set is ongoing. Total game score is {score_count[1]}-{score_count[2]}")

    def reset_set(self) -> None:
        """Wipes the set clean"""
        self.winner = "In progress"
        self.game_list = []
        print(f"Set has been reset.")

    def print_games(self) -> None:
        """Prints all Games in this Set"""
        if not self.game_list:
            print("Game list is empty!")
        else:
            for game in self.game_list:
                print(f"Game {game.game_id}: {game.print_scores()}")

    @integer_validation
    def switch_game(self) -> bool:
        """Picks the game to change into based on user input"""
        game_id = int(input("Enter game number to switch to: "))

        for game in self.game_list:
            if game_id == game.game_id:
                self.active_game = game
                print(f"Switched to game number {game_id}")
                return True
        print(f"Game number {game_id} does not exist.")
        return False

    @disabled
    def set_to_tie(self):
        self.game_list = []
        for i in range(0, 6):
            game = Game(i + 1)
            game.p1_wins()
            self.game_list.append(game)
        for i in range(0, 6):
            game = Game(i + 7)
            game.p2_wins()
            self.game_list.append(game)
        self.print_games()

    @disabled
    def p1_wins(self):
        self.game_list = []
        for i in range(0, 6):
            game = Game(i + 1)
            game.p1_wins()
            self.game_list.append(game)

    @disabled
    def p2_wins(self):
        self.game_list = []
        for i in range(0, 6):
            game = Game(i + 1)
            game.p2_wins()
            self.game_list.append(game)


class TieBreakerSet(AdvantageSet):
    """Another third layer scope. Has a cap of how many Games can be in the Set"""
    def __init__(self, set_id, is_gs) -> None:
        AdvantageSet.__init__(self, set_id)
        self.tiebreaker_added = False
        self.is_gs = is_gs

    def add_game(self, is_gs=False) -> None:
        """Adds a Game to the Set. Will be a regular Game unless there are already 12 games present.
        Otherwise, a Tiebreaker Game is added instead and no more games will be allowed."""
        if self.winner != "In progress":
            print(f"Set is already complete! Player {self.winner} won.")
        else:
            if any(game.winner == "In progress" for game in self.game_list):
                print("At least one game present that is still In progress. Not adding another game.")
            else:
                if len(self.game_list) == 12:
                    if not self.tiebreaker_added:
                        self.game_list.append(GameTiebreaker(len(self.game_list) + 1, is_gs))
                        print(f"Tiebreaker game added. Game ID is {self.game_list[len(self.game_list) - 1].game_id}")
                        self.tiebreaker_added = True
                    else:
                        print("Tiebreaker game already present. Not adding another game.")
                else:
                    self.game_list.append(Game(len(self.game_list) + 1))
                    print(f"Game added. Game ID is {self.game_list[len(self.game_list) - 1].game_id}")

    def is_complete(self) -> None:
        """Overloads inherited function as conditions for completion are slightly different,
        but overall purpose is the same"""
        score_count = {1: 0, 2: 0}
        for game in self.game_list:
            if game.winner:
                if game.winner == 1:
                    score_count[1] += 1
                elif game.winner == 2:
                    score_count[2] += 1

        if score_count[1] == score_count[2] == 6 and not self.tiebreaker_added:
            print(f"Set is ongoing. Score is {score_count[1]}-{score_count[2]}.\nA tiebreaker game has been added and no more games are allowed for this set")
            self.add_game(is_gs=False)
        elif self.tiebreaker_added and score_count[1] > score_count[2]:
            self.winner = 1
            print(f"Set is complete! Player {self.winner} won.")
        elif self.tiebreaker_added and score_count[2] > score_count[1]:
            self.winner = 2
            print(f"Set is complete! Player {self.winner} won.")
        elif score_count[1] >= self.play_to and score_count[1] - score_count[2] >= 2:
            self.winner = 1
            print(f"Set is complete! Player {self.winner} won.")
        elif score_count[2] >= self.play_to and score_count[2] - score_count[1] >= 2:
            self.winner = 2
            print(f"Set is complete! Player {self.winner} won.")
        else:
            print(f"Set is ongoing. Score is {score_count[1]}-{score_count[2]}")

    def reset_set(self) -> None:
        """Wipes the set clean. Overload is neccessary due to extra class variables"""
        self.winner = "In progress"
        self.game_list = []
        self.tiebreaker_added = False
        print(f"Set has been reset.")


class Game:
    """
    The fourth and lowest layer scope.
    Represents a game. Played up to four points, or if a deuce, win by 2
    Is the default created game type.
    """
    def __init__(self, game_id):
        self.game_id = game_id
        self.scores = {1: 0, 2: 0}
        self.play_to = 4
        self.winner = "In progress"

    @integer_validation
    @container_validation
    def add_score(self) -> None:
        if self.winner != "In progress":
            print(f"Game is already complete! Player {self.winner} won.")
        else:
            player = int(input("Enter 1 for server player or 2 for receiving player: "))
            self.scores[player] += 1
            self.is_complete()

    def is_complete(self) -> None:
        if self.scores[1] >= self.play_to and self.scores[1] - self.scores[2] >= 2:
            self.winner = 1
            print(f"Game is complete! Player {self.winner} won.")
        elif self.scores[2] >= self.play_to and self.scores[2] - self.scores[1] >= 2:
            self.winner = 2
            print(f"Game is complete! Player {self.winner} won.")
        else:
            print(f"Game is in progress. Score: {self.print_scores()}")

    def reset_game(self) -> None:
        """Wipes the Game clean."""
        self.winner = "In progress"
        self.scores = {1: 0, 2: 0}
        print(f"Game has been reset. Score: {self.print_scores()}")

    def print_scores(self) -> str:
        if self.scores[1] == self.scores[2] and self.scores[1] >= 3:
            return "Deuce"
        elif self.scores[1] < self.scores[2] and self.scores[2] >= 3 and self.scores[2] - self.scores[1] == 1:
            return "Ad-Out"
        elif self.scores[1] > self.scores[2] and self.scores[1] >= 3 and self.scores[1] - self.scores[2] == 1:
            return "Ad-In"
        elif self.scores[1] == self.scores[2] and self.scores[1] < 3:
            return f"{SCORE_MAP[self.scores[1]]}-all"
        else:
            return f"{SCORE_MAP[self.scores[1]]}-{SCORE_MAP[self.scores[2]]}"

    @disabled
    def set_to_deuce(self):
        if self.winner == "In progress":
            self.scores[1] = 3
            self.scores[2] = 3
            print(f"Score: {self.print_scores()}")

    @disabled
    def p1_wins(self):
        if self.winner == "In progress":
            self.scores[1] = 4
            self.scores[2] = 0
            self.is_complete()

    @disabled
    def p2_wins(self):
        if self.winner == "In progress":
            self.scores[1] = 0
            self.scores[2] = 4
            self.is_complete()

class GameTiebreaker(Game):
    """
    Inherits from GameRegular class. Two differences:
    1) tiebreaker games are played to 7 and grand slam tiebreaker games are played to 10 (both still win by 2),
    2) scores are displayed as is
    This can only be created by the TieBreakerSet class and never by the AdvantageSet class.
    """
    def __init__(self, game_id, is_gs) -> None:
        Game.__init__(self, game_id)
        if is_gs:
            self.play_to = 10
        else:
            self.play_to = 7

    def print_scores(self) -> str:
        return f"{self.scores[1]}-{self.scores[2]}"


if __name__ == '__main__':
    print("Welcome")
    finished = False
    scope = "TRACKER"
    tracker = Tracker()
    while not finished:
        if scope == "TRACKER":
            command = input(f"\nScope --> {scope}\n>> ")
        elif scope == "MATCH":
            command = input(f"\nScope --> {scope}"
                            f"\nMatch --> {tracker.active_match.match_id}\n>> ")
        elif scope == "SET":
            command = input(f"\nScope --> {scope}"
                            f"\nMatch --> {tracker.active_match.match_id}, "
                            f"Set --> {tracker.active_match.active_set.set_id}\n>> ")
        elif scope == "GAME":
            command = input(f"\nScope --> {scope}"
                            f"\nMatch --> {tracker.active_match.match_id}, "
                            f"Set --> {tracker.active_match.active_set.set_id}, "
                            f"Game --> {tracker.active_match.active_set.active_game.game_id}\n>> ")
        command = command.lower().strip()

        if command == "help":
            help_print(scope)
        elif command == "quit":
            finished = True
            print("Goodbye")
        elif command in SCOPE_COMMANDS[scope]:
            if scope == "TRACKER":
                if command == "add match":
                    tracker.add_match()
                elif command == "print matches":
                    tracker.print_matches()
                elif command == "switch":
                    if tracker.switch_match():
                        scope = "MATCH"
            elif scope == "MATCH":
                if command == "add set":
                    tracker.active_match.add_set()
                elif command == "add set tiebreaker":
                    tracker.active_match.add_set(tiebreaker=True)
                elif command == "print sets":
                    tracker.active_match.print_sets()
                elif command == "switch":
                    if tracker.active_match.switch_set():
                        scope = "SET"
                elif command == "status":
                    tracker.active_match.is_complete()
                elif command == "reset":
                    tracker.active_match.reset_match()
                elif command == "up":
                    tracker.active_match = None
                    scope = "TRACKER"
            elif scope == "SET":
                if command == "add game":
                    tracker.active_match.active_set.add_game()
                elif command == "print games":
                    tracker.active_match.active_set.print_games()
                elif command == "switch":
                    if tracker.active_match.active_set.switch_game():
                        scope = "GAME"
                elif command == "status":
                    tracker.active_match.active_set.is_complete()
                elif command == "reset":
                    tracker.active_match.active_set.reset_set()
                elif command == "up":
                    tracker.active_match.active_set = None
                    scope = "MATCH"
                ### TESTING ONLY ###
                elif command == "p1w":
                    tracker.active_match.active_set.p1_wins()
                ### TESTING ONLY ###
                elif command == "p1w":
                    tracker.active_match.active_set.p2_wins()
                ### TESTING ONLY ###
                elif command == "tie":
                    tracker.active_match.active_set.set_to_tie()
            elif scope == "GAME":
                if command == "add score":
                    tracker.active_match.active_set.active_game.add_score()
                elif command == "status":
                    tracker.active_match.active_set.active_game.is_complete()
                elif command == "reset":
                    tracker.active_match.active_set.active_game.reset_game()
                elif command == "up":
                    tracker.active_match.active_set.active_game = None
                    scope = "SET"
                ### TESTING ONLY ###
                elif command == "deuce":
                    tracker.active_match.active_set.active_game.set_to_deuce()
                ### TESTING ONLY ###
                elif command == "p1w":
                    tracker.active_match.active_set.active_game.p1_wins()
                ### TESTING ONLY ###
                elif command == "p2w":
                    tracker.active_match.active_set.active_game.p2_wins()
        else:
            print(f"Invalid command for this scope - {command}")
            help_print(scope)
