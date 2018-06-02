import json

class Card:
    def __init__(self, card, hand):
        self.suit = card['suit']
        self.rank = card['rank']
        self.hand = hand
        self.rank_score = self.rank_to_score()

    # Conversions
    def ace_conversion(self):
        ranks = [self.hand[card]['rank'] for card in self.hand]
        low_order = {2,3,4,5}
        if set(ranks).intersection(low_order) == low_order:
            return(1)
        else:
            return(14)

    def convert_alpha(self):
        royalty_conversion = {'jack': 11, 'queen': 12, 'king': 13}
        if self.rank == 'ace':
            return(self.ace_conversion())
        else:
            return(royalty_conversion[self.rank])

    def rank_to_score(self):
        if isinstance(self.rank, int):
            return(self.rank)
        else:
            return(self.convert_alpha())


class Hand:

    def __init__(self, hand):
        self.cards = [Card(hand[card], hand) for card in hand]
        self.suits = [card.suit for card in self.cards]
        self.rank_scores = sorted([card.rank_score for card in self.cards])
        self.poker_hand = self.rank_hand()
        self.score = self.SCORE[self.poker_hand]
        self.frequency_of_ranks = self.frequency_of_rank()

    SCORE = {'high card': 1,
         'one pair': 2,
         'two pair': 3,
         'three of a kind': 4,
         'straight': 5,
         'flush': 6,
         'full house': 7,
         'four of a kind': 8,
         'straight flush': 9}


    def check_for_flush(self):
        output = len(set(self.suits)) == 1
        return(output)

    def check_for_straight(self):
        output = [self.rank_scores[i]-self.rank_scores[i+1] for i in
                range(len(self.rank_scores)-1)].count(-1) == 4
        return(output)

    def create_rank_pattern(self):
        count_pattern = sorted([self.rank_scores.count(score)
                        for score in set(self.rank_scores)])
        return(count_pattern)

    def rank_hand(self):
        if self.check_for_straight():
            if self.check_for_flush():
                return('straight flush')
            return('straight')
        elif self.check_for_flush() and not self.check_for_straight():
            return('flush')
        elif self.create_rank_pattern() == [1,4]:
            return('four of a kind')
        elif self.create_rank_pattern() == [2,3]:
            return('full house')
        elif self.create_rank_pattern() == [1,1,3]:
            return('three of a kind')
        elif self.create_rank_pattern() == [1,2,2]:
            return('two pair')
        elif self.create_rank_pattern() == [1,1,1,2]:
            return('one pair')
        else:
            return('high card')

    def frequency_of_rank(self):
        frequencies = {count: sorted([score for score in set(self.rank_scores)
                    if self.rank_scores.count(score) == count], reverse=True)
                    for count in range(
                    max([self.rank_scores.count(score)
                        for score in self.rank_scores]),
                    min([self.rank_scores.count(score)
                        for score in self.rank_scores])-1, -1)}
        return(frequencies)


class Game:
    def __init__(self, data):
        self.hand_one = Hand(data['hand_one'])
        self.hand_two = Hand(data['hand_two'])

    def evaluate_tied_hands(self):
        for key in self.hand_one.frequency_of_ranks:
            for i in range(len(self.hand_one.frequency_of_ranks[key])):
                rank_one = self.hand_one.frequency_of_ranks[key][i]
                rank_two = self.hand_two.frequency_of_ranks[key][i]
                print(rank_one, rank_two)
                if rank_one > rank_two:
                    return('hand one')
                elif rank_one < rank_two:
                    return('hand two')
        else:
            return('absolute draw')

    def evaluate_hands(self):
        if self.hand_one.score > self.hand_two.score:
            return('hand one wins by score')
        elif self.hand_one.score < self.hand_two.score:
            return('hand two wins by score')
        else:
            return(self.evaluate_tied_hands())


with open('hands.json', 'r') as hands:
    data = json.load(hands)

game = Game(data)
print(game.hand_one.frequency_of_ranks)
print(game.hand_two.frequency_of_ranks)
print()
print('Hand one is a {} and has a score of {}.'.format(game.hand_one.poker_hand, game.hand_one.score))
print()
print('Hand two is a {} and has a score of {}.'.format(game.hand_two.poker_hand, game.hand_two.score))
print()
print(game.evaluate_hands())
