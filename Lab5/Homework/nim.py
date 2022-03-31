import datetime

def minmax_decision(state, player):

    def max_value(state):
        if is_terminal(state):
            return utility_of('Min')
        v = -infinity
        for s in successors_of(state):
            v = max(v, min_value(s))
        return v

    def min_value(state):
        if is_terminal(state):
            return utility_of('Max')
        v = infinity
        for s in successors_of(state):
            v = min(v, max_value(s))
        return v

    infinity = float('inf')
    return argmax(successors_of(state), lambda a: min_value(a)) if player == 'Max' \
            else argmin(successors_of(state), lambda a: max_value(a))


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

def player_move(pile):
    '''
    Human inputs to the nim game
    '''
    selected_pile = -1
    while selected_pile < 0 or selected_pile > len(pile) - 1 or pile[selected_pile] < 3:
        print(f'Select a pile (1 to {len(pile)}) that is greater than 2')
        selected_pile = int(input()) - 1

    pile_size = -1
    while pile_size < 0 or pile_size >= pile[selected_pile] or pile[selected_pile] - pile_size == pile_size:
        print('Select a size of one of the piles it will be split into (size can not be exactly half of the pile)')
        pile_size = int(input())

    num2 = pile[selected_pile] - pile_size
    pile[selected_pile] = pile_size
    pile.insert(selected_pile + 1, num2)

    return sorted(pile, reverse = True)

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
    move = 'Computer'
    computerVSplayer = False # change this parameter to play agains computer or let it play against itself
    pile = [7]
    print('Pile: ' + str(pile[0]))
    tic = datetime.datetime.now()
    while not is_terminal(pile):
        pile = minmax_decision(pile, player)
        move = game_manager(player, move, pile, computerVSplayer)
        if not computerVSplayer:
            player = move
        if not is_terminal(pile):
            if computerVSplayer:
                pile = player_move(pile)
                move = game_manager(player, move, pile, computerVSplayer)
            else:
                pile = minmax_decision(pile, player)
                player = game_manager(player, move, pile, computerVSplayer)
    toc = datetime.datetime.now()
    if computerVSplayer:
        print('Another loss for humanity') if move != 'Computer' else print('Congratulations, you\'ve won!')
    else:
        print(player + ' lost')
        print(f'Execution speed {toc - tic}')

def argmax(iterable, func):
    return max(iterable, key=func)

def argmin(iterable, func):
    return min(iterable, key=func)


if __name__ == '__main__':
    main()
