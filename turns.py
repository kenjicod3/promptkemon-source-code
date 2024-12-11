import random, data


# Checks if the mon moves
def does_move(pokemon):
    assert (
        type(pokemon) == data.Pokemon
    ), "error: func does_move taking in non-pokemon"
    # Checks for paralysis
    if pokemon.status == "PAR":
        # If mon is paralysed, roll for paralysis
        chance = 0.3
        random_num = random.uniform(0.0, 1.0)
        Bool_test = random_num <= chance
        return Bool_test
    # Else, return True
    return True


# Determines if either player's bot's mon used a move with priority.
def get_priority(move_player, move_bot):
    priority_player = move_player.priority
    priority_bot = move_bot.priority
    if priority_player == priority_bot:
        return None
    elif priority_player > priority_bot:
        return "player"
    else:
        return "bot"


# Returns a list with the pokemon in speed order.
def compare_speed(pokemon1, pokemon2):
    assert (
        type(pokemon1) == data.Pokemon and type(pokemon2) == data.Pokemon
    ), "error: compare_speed taking in non-pokemon"
    # Setup
    mon_ls = [pokemon1, pokemon2]
    spd_ls = []
    # Sets up spd_ls
    for mon in mon_ls:
        spd = mon.speed * mon.multiplier_speed
        # If mon is paralyzed, add a 0.5 multiplier to its spd
        if mon.status == "PAR":
            spd *= 0.5
        spd_ls.append(spd)
    # If the 2nd spd is higher than the first spd, swap their positions
    if spd_ls[0] < spd_ls[1]:
        mon_ls[0], mon_ls[1] = mon_ls[1], mon_ls[0]
    # If the spds are equal, randomise the order of the list
    elif spd_ls[0] == spd_ls[1]:
        random.shuffle(mon_ls)
    return mon_ls


# Returns the turn order after accounting for priority.
def fastest(player_mon, bot_mon, player_move, enemy_move):
    # If neither mon used a priority move, return compare_speed
    if get_priority(player_move, enemy_move) == None:
        return compare_speed(player_mon, bot_mon)
    # If either mon used a priority move, return the list based on which one has higher priority
    elif get_priority(player_move, enemy_move) == "player":
        # in this case get_priority return string "player", when player moves first
        return (player_mon, bot_mon)
    return (bot_mon, player_mon)
