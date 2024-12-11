import pokemon_data, random, data, damage_calculation

player_mon = pokemon_data.charmander
bot_mon = pokemon_data.pikachu


# Split moveset into attacking moves and non-attacking moves.
def split_moves_by_category(moves):
    atks = []
    non_atks = []
    for move in moves:
        if move.category == "Status":
            non_atks.append(move)
        else:
            atks.append(move)
    return atks, non_atks


# Returns true if the target is type immune to the move.
def check_type_immunity(target, move):
    move_type = move.move_type
    target_types = target.pokemon_type
    for type in target_types:
        # Loops through the target mon's types, and returns True if the type modifier is 0.
        if data.type_chart[move_type][type] == 0:
            return True
    return False


# Returns a tuple, (Boolean, cause of failure if True).
def check_status_failure(target, move):
    assert (
        move.effect[0] == "Status"
    ), "check_status_failure taking invalid move"
    status = move.effect[1]
    # Checks for electric types being immune to paralysis.
    check_para_immunity = status == "PAR" and "Electric" in target.pokemon_type
    # Checks for the target already having a status.
    already_statused = target.status != "Null"
    if check_type_immunity(target, move):
        return True, "type immune"
    elif check_para_immunity:
        return True, "para immune"
    elif already_statused:
        return True, "already statused"
    return False, ""


def check_stat_change_failure(move):
    assert (
        move.effect[0] == "Stat Change"
    ), "check_stat_change_failure taking invalid move"
    # Gets the number of affected stats.
    no_of_affected_stats = int((len(move.effect) - 2) / 2)
    # ('Log -- affected stats '+ str(no_of_affected_stats))
    # Loops through the affected stats.
    for i in range(no_of_affected_stats):
        # ('Log -- stat '+str(i))
        # Gets relevant data
        target = {"Self": bot_mon, "Enemy": player_mon}
        affected_mon = target[move.effect[1]]
        affected_stat = move.effect[2 + 2 * i]
        stat_change = move.effect[3 + 2 * i]
        # ('Log -- ',affected_mon,affected_stat)
        current_stage = getattr(affected_mon, affected_stat)
        # ('Log -- ',current_stage)
        sign = stat_change / abs(stat_change)
        # ('Log -- ',current_stage,sign)
        # If the change would bring the modifier past 4 or 1/4 depending on the sign of the change, fail the check.
        if current_stage == 4**sign:
            return True
    return False


# Returns true if the effectiveness of the heal is below a given percentage.
def check_heal_failure(user, move, percentage):
    assert move.effect[0] == "Heal", "check_heal_failure taking invalid move"
    assert (
        percentage >= 0 and percentage <= 1
    ), "check_heal_failure is taking invalid percentage"
    missing_hp_percent = (user.hp - user.current_hp) / user.hp
    heal_percent = percentage * (move.effect[1]/100)
    return missing_hp_percent <= heal_percent


def bot_choose_move(user, target):
    # Splits the moveset into attacking and non-attacking moves.
    atks, non_atks = split_moves_by_category(user.moveset)
    # Rolls damage for all attacking moves.
    dmg_rolls = {}
    weight = []
    for i in non_atks:
        weight.append(1)
    for move in atks:
        dmg_roll = damage_calculation.calculate_damage(user, target, move)[0]
        dmg_rolls[dmg_roll] = move
    # If the highest damage roll would defeat the target,
    if max(dmg_rolls.keys()) >= target.current_hp:
        lethal_rolls = []
        # ('Log -- Lethal Move detected')
        # Find all moves that would defeat the target,
        for dmg in dmg_rolls.keys():
            if dmg >= target.current_hp:
                lethal_rolls.append(dmg_rolls[dmg])
        # Then return a random move from the list.
        return random.choice(lethal_rolls)
    # Else, get the move that got the highest damage roll.
    else:
        best_atk = dmg_rolls[max(dmg_rolls.keys())]
    # Sets up a list of possible moves to choose from with all non-attacking moves
    move_choices = non_atks[:]
    # ('Log -- move choice',i)
    # Removes non-attacking moves that would accomplish nothing
    # Loops through the non-attacking moves
    for move in non_atks:
        # ('Log --',move.name, move.effect[0])
        # Removes status-afflicting moves if the player mon is already statused
        if move.effect[0] == "Status":
            if check_status_failure(target, move)[0]:
                # (f'Log -- {move.name},is redundant')
                weight[non_atks.index(move)]=0
        # Removes stat changing moves if the stat is capped
        elif move.effect[0] == "Stat Change":
            if check_stat_change_failure(move):
                # (f'Log -- {move.name},is redundant')
                weight[non_atks.index(move)]=0
            else: 
                if user.current_hp/user.hp <=0.5:
                    if "multiplier_sp_defense" or "mutiplier_defense" in move.effect:
                        weight[non_atks.index(move)]+=1
                elif target.speed > user.speed:
                    weight[non_atks.index(move)]+=1
        # Removes healing moves that would heal for less than 80% of the heal value
        elif move.effect[0] == "Heal":
            if check_heal_failure(user, move, 0.8):
                # (f'Log -- {move.name},is redundant')
                weight[non_atks.index(move)]=0
            else:
                if user.current_hp/user.hp <=0.5:
                    weight[non_atks.index(move)]+=2
                elif user.current_hp/user.hp <=0.2:
                    weight[non_atks.index(move)]+=4
                else:
                    weight[non_atks.index(move)]+=1
    # Adds the best attacking move to the move choices list
    move_choices.append(best_atk)
    weight.append(3)
    # Chooses a random move from the list
    for i in move_choices:
        # ("Log -- Possible Move:",i.name)
        result = random.choices(move_choices,weights=weight,k=1)[0]
    # (f'Log -- Bot chooses {result}')
    return result


# (bot_choose_move(bot_mon,player_mon).name)
