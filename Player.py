# Written with the help of Chat GPT4o

class Player:
    def __init__(self):
        # Initialize the player's score to zero
        self._score = 0

    def get_score(self):
        # Return the player's current score
        return self._score

    def add_score(self, points):
        # Add points to the player's score
        self._score += points

    def reset_score(self):
        # Reset the player's score to zero
        self._score = 0

