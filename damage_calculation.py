import move_data, pokemon_data, random, data, random, math

player_active = pokemon_data.pikachu
enemy_active = pokemon_data.phanpy
player_move = move_data.body_slam


def calculate_damage(user, target, move):
    # Setup
    base_power = move.base_power
    move_type = move.move_type
    user_type = user.pokemon_type
    target_type = target.pokemon_type
    # Setup type_mod
    type_mod = 1
    # Loops through the target's types
    for type in target_type:
        # Multiplies the type modifier into type_mod
        type_mod *= data.type_chart[move_type][type]
    # Sets the appropriate stats to use for physical moves
    if move.category == "Physical":
        Atk = user.attack
        Def = target.defense
        attker_mod = user.multiplier_attack
        dfdr_mod = target.multiplier_defense
    # Sets the appropriate stats to use for special moves
    else:
        Atk = user.sp_attack
        Def = target.sp_defense
        attker_mod = user.multiplier_sp_attack
        dfdr_mod = user.multiplier_sp_defense
    # Setup stab
    stab = 1
    # Changes stab to 1.5 if the move's type matches either of the user's types
    for type in user_type:
        if move_type == type:
            stab = 1.5
    # Sets burn_mod if the user is burnt and the move is physical
    if user.status == "BRN" and move.category == "Physical":
        burn_mod = 0.5
    else:
        burn_mod = 1
    # Rolls for crit
    chance = random.randint(1, 24) == 1
    # If crits, sets critical and burn_mod, ignores attacker_mod if it's less than 1, and defender_mod if it's more than 1.
    if chance:
        critical = 1.5
        burn_mod = 1
        attker_mod = max(1, attker_mod)
        dfdr_mod = min(1, dfdr_mod)
    else:
        critical = 1
    # Rolls for rng modifier, random between 0.85 and 1. 16 Posssible results.
    rng = random.randint(85, 100) / 100
    # Calculates dmg
    dmg = math.floor(
        (
            (
                (22 * base_power * (attker_mod * Atk) / (Def * dfdr_mod) * 0.02)
                * rng
                * stab
                * type_mod
                * critical
                * burn_mod
            )
        )
    )
    # Returns dmg. type_mod and chance are also returned to display appropriate text in UI.
    return dmg, type_mod, chance
