import datetime

def alpha_beta_decision(state, player):
    infinity = float('inf')

    def max_value(state, alpha, beta):
        if is_terminal(state):
            return utility_of('Min')
        v = -infinity
        for successor in successors_of(state):
            v = max(v, min_value(successor, alpha, beta))
            if v >= beta:
                return v
            alpha = min(alpha, v)
        return v

    def min_value(state, alpha, beta):
        if is_terminal(state):
            return utility_of('Max')
        v = infinity

        for successor in successors_of(state):
            v = min(v, max_value(successor, alpha, beta))
            if v <= alpha:
                return v
            beta = max(beta, v)
        return v

    state = argmax(successors_of(state), lambda a: min_value(a, infinity, -infinity)) if player == 'Max' \
                else argmin(successors_of(state), lambda a: max_value(a, infinity, -infinity))
    return state


def is_terminal(state):
    """
    returns True if the state is a win 
    """
    return successors_of(state) == []

def utility_of(player):
    """
    returns +1 if winner is (MAX player), -1 if winner is (MIN player)
    """
    return 1 if player == 'Max' else -1

def successors_of(state):
    """
    returns a list of possible states
    """
    successors = []
    for i in range(len(state)):
        if state[i] >= 3:
            middle = state[i] // 2
            for num1 in range(1, middle + 1):
                num2 = state[i] - num1
                if num1 != num2:
                    new_state = sorted(state[:i] + [num1, num2] + state[i + 1:], reverse = True)
                    if new_state not in successors:
                        successors.append(new_state)

    return successors


def argmax(iterable, func):
    return max(iterable, key=func)

def argmin(iterable, func):
    return min(iterable, key=func)

def computer_select_pile(state, player):
    new_state = alpha_beta_decision(state, player)
    return new_state


def user_select_pile(list_of_piles):
    '''
    Given a list of piles, asks the user to select a pile and then a split.
    Then returns the new list of piles.
    '''
    # print("\n    Current piles: {}".format(list_of_piles))

    i = -1
    while i < 0 or i >= len(list_of_piles) or list_of_piles[i] < 3:
        print("   Which pile (from 1 to {}, must be > 2)?".format(len(list_of_piles)))
        i = -1 + int(input())

    print("   Selected pile {}".format(list_of_piles[i]))

    max_split = list_of_piles[i] - 1

    j = 0
    while j < 1 or j > max_split or j == list_of_piles[i] - j:
        if list_of_piles[i] % 2 == 0:
            print(
                '   How much is the first split (from 1 to {}, but not {})?'.format(
                    max_split,
                    list_of_piles[i] // 2
                )
            )
        else:
            print(
                '   How much is the first split (from 1 to {})?'.format(max_split)
            )
        j = int(input())

    k = list_of_piles[i] - j

    new_list_of_piles = list_of_piles[:i] + [j, k] + list_of_piles[i + 1:]

    # print("    New piles: {}".format(new_list_of_piles))

    return sorted(new_list_of_piles, reverse = True)


def game_manager(player, move, pile, computerVSplayer):
    '''
    displays current state and switches which player ir playing
    '''
    if not computerVSplayer:
        print(player + ': ' + ', '.join(list(map(lambda int: str(int), pile))))
        return 'Max' if player == 'Min' else 'Min'
    else:
        print(move + ': ' + ', '.join(list(map(lambda int: str(int), pile))))
        return 'You' if move == 'Computer' else 'Computer'

def main():
    player = 'Min'
    move = 'Computer' # know the winner when playing computer vs human1
    computerVSplayer = False # change this parameter to play agains computer or let it play against itself
    pile = [8]
    print('Pile: ' + str(pile[0]))
    tic = datetime.datetime.now()
    while not is_terminal(pile):
        pile = computer_select_pile(pile, player)
        move = game_manager(player, move, pile, computerVSplayer)
        if not computerVSplayer:
            player = move
        if not is_terminal(pile):
            if computerVSplayer:
                pile = user_select_pile(pile)
                move = game_manager(player, move, pile, computerVSplayer)
            else:
                pile = computer_select_pile(pile, player)
                player = game_manager(player, move, pile, computerVSplayer)
    toc = datetime.datetime.now()
    if computerVSplayer:
        print('Another loss for humanity') if move != 'Computer' else print('Congratulations, you\'ve won!')
    else:
        print(player + ' lost')
        print(f'Execution speed {toc - tic}')
    print("    Final state is {}".format(pile))


if __name__ == '__main__':
    main()
