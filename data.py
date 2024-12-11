import copy


class Pokemon(object):
    def __init__(
        self,
        name,
        current_hp,
        hp,
        attack,
        defense,
        sp_attack,
        sp_defense,
        speed,
        pokemon_type,
        moveset,
        status,
    ):
        """
        :param hp: hp of pokemon
        :param attack: attack stat
        :param defence: defence stat, defends against attacks which use attack stat
        :param special: special stat, used to calculate damage for moves which use special
                        instead of attack stat to calculate damage dealt and special instead
                        of defence stat to calculate damage taken
        :param speed: speed stat, determines who moves first
        :param type: type of pokemon, used to determine damage delt and taken
        :param status: can be paralysis, poison, badly poison, sleep, and frozen,
        :param moveset: pokemon's moveset as a dictionary, moves as keys and value as pp
        :param ability: ability of pokemon, eg:- ignore paralysis
        """
        assert type(name) == str, "type of name has to be a string"
        assert (
            type(current_hp) == int
        ), "type of currunt_hp has to be an integer"
        assert type(hp) == int, "type of hp has to be an integer"
        assert type(attack) == int, "attack has to be an integer"
        assert type(defense) == int, "type of hp has to be an integer"
        assert type(sp_attack) == int, "type of sp_attack has to be an integer"
        assert (
            type(sp_defense) == int
        ), "type of sp_defense has to be an integer"
        assert type(speed) == int, "type of speed has to be an integer"
        assert (
            type(pokemon_type) == list
        ), "type of pokemon_type has to be a string"
        assert type(moveset) == list, "type of moveset has to be a list"
        assert type(status) == str, "type of status has to be a str"

        self.name = name
        self.current_hp = current_hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.sp_attack = sp_attack
        self.sp_defense = sp_defense
        self.speed = speed
        self.pokemon_type = pokemon_type
        self.moveset = moveset
        self.status = status
        self.multiplier_attack = 2 / 2
        self.multiplier_defense = 2 / 2
        self.multiplier_sp_attack = 2 / 2
        self.multiplier_sp_defense = 2 / 2
        self.multiplier_speed = 2 / 2

    def change_hp(self, change_hp):
        """
        change hp of pokemon, do pokemon.hp(-10) to reduce by 10 or pokemon.hp(10) to raise by 10
        changes current_hp to 0, if change in hp makes it -ve, and into max hp or simply hp attribute
        if current_hp is greater than hp attribute
        """
        assert type(change_hp) == int, "the change in hp has to be an integer"
        valid_test = self.current_hp + change_hp
        if valid_test > self.hp:
            self.current_hp = self.hp
        elif valid_test < 0:
            self.current_hp = 0
        else:
            self.current_hp = valid_test

    def change_stat_stage(self, stat, change):
        """
        for changing stat multiplier of stats, for example stage_change('attack', 2)
        raise attack by 2 stages, inputing and -ve number decrease stage similiarly
        """
        assert type(change) == int, "stage change has to be an integer"
        assert (
            type(stat) == str
        ), "stat which needs to be changed has to be given in form of string"

        stat_val = self.__getattribute__(stat)
        # The multiplier is (2+stage)/2 if stage is positive, and 2/(2-stage) if stage is negative.
        # Converts the multiplier into its stage.
        if stat_val > 1:
            stage = stat_val * 2 - 2
        else:
            stage = (2 - 2 * stat_val) / stat_val
        new_stage = stage + change
        # Bounds the new_stage to be within -6,6. If out of range, changes it to be -6 or 6
        new_stage = max(new_stage, -6)
        new_stage = min(new_stage, 6)
        # Sets the new_mod based on the stage.
        if new_stage >= 0:
            new_mod = (new_stage + 2) / 2
        else:
            new_mod = 2 / (2 - new_stage)
        self.__setattr__(stat, new_mod)

    def copy(self):
        new = Pokemon(
            self.name,
            self.current_hp,
            self.hp,
            self.attack,
            self.defense,
            self.sp_attack,
            self.sp_defense,
            self.speed,
            copy.deepcopy(self.pokemon_type),
            copy.deepcopy(self.moveset),
            self.status,
        )
        return new

    def __str__(self):
        return self.name

    def change_status(self, new_status):
        self.status = new_status


stat_name_table = {
    "multiplier_attack": "attack",
    "multiplier_defense": "defense",
    "multiplier_sp_attack": "special attack",
    "multiplier_sp_defense": "special defense",
    "multiplier_speed": "speed",
}


class Move:
    def __init__(
        self,
        name,
        move_type,
        category,
        base_power,
        accuracy,
        current_pp,
        max_pp,
        priority,
        description,
        effect,
    ):
        assert type(name) == str, "type must be string"
        assert type(move_type) == str, "type must be string"
        assert type(category) == str, "type must be string"
        assert type(base_power) == int, "type must be integer"
        assert type(accuracy) == int, "type must be integer"
        assert type(max_pp) == int, "type must be integer"
        assert type(current_pp) == int, "type must be integer"
        assert type(priority) == int, "type priority must be integer"
        assert type(description) == str, "type must be string"
        assert type(effect) == list, "type must be list"

        self.name = name
        self.move_type = move_type
        self.category = category
        self.base_power = base_power
        self.accuracy = accuracy
        self.max_pp = max_pp
        self.current_pp = current_pp
        self.priority = priority
        self.description = description
        self.effect = effect

    def copy(self):
        return Move(
            self.name,
            self.move_type,
            self.category,
            self.base_power,
            self.accuracy,
            self.current_pp,
            self.max_pp,
            self.priority,
            self.description,
            self.effect,
        )

    def __str__(self):
        return self.name

    def change_pp(self, change):
        self.current_pp += change


# Move.effect breakdown
# For Status, ('Status', status applied, chance to apply)
# For Stat Change, ( 'Stat Change', target, stat1, change1, stat2, change2 )
# For Heal, ('Heal', heal percentage)

### type_chart[Attacking Type][Defending Type] gives Type Multiplier
type_chart = {
    "Normal": {
        "Normal": 1,
        "Fighting": 1,
        "Flying": 1,
        "Poison": 1,
        "Ground": 1,
        "Rock": 0.5,
        "Bug": 1,
        "Ghost": 0,
        "Steel": 0.5,
        "Fire": 1,
        "Water": 1,
        "Grass": 1,
        "Electric": 1,
        "Psychic": 1,
        "Ice": 1,
        "Dragon": 1,
        "Dark": 1,
        "Fairy": 1,
    },
    "Fighting": {
        "Normal": 2,
        "Fighting": 1,
        "Flying": 0.5,
        "Poison": 0.5,
        "Ground": 1,
        "Rock": 2,
        "Bug": 0.5,
        "Ghost": 0,
        "Steel": 2,
        "Fire": 1,
        "Water": 1,
        "Grass": 1,
        "Electric": 1,
        "Psychic": 0.5,
        "Ice": 2,
        "Dragon": 1,
        "Dark": 2,
        "Fairy": 0.5,
    },
    "Flying": {
        "Normal": 1,
        "Fighting": 2,
        "Flying": 1,
        "Poison": 1,
        "Ground": 1,
        "Rock": 0.5,
        "Bug": 2,
        "Ghost": 1,
        "Steel": 0.5,
        "Fire": 1,
        "Water": 1,
        "Grass": 2,
        "Electric": 0.5,
        "Psychic": 1,
        "Ice": 1,
        "Dragon": 1,
        "Dark": 1,
        "Fairy": 1,
    },
    "Poison": {
        "Normal": 1,
        "Fighting": 1,
        "Flying": 1,
        "Poison": 0.5,
        "Ground": 0.5,
        "Rock": 0.5,
        "Bug": 1,
        "Ghost": 0.5,
        "Steel": 0,
        "Fire": 1,
        "Water": 1,
        "Grass": 2,
        "Electric": 1,
        "Psychic": 1,
        "Ice": 1,
        "Dragon": 1,
        "Dark": 1,
        "Fairy": 2,
    },
    "Ground": {
        "Normal": 1,
        "Fighting": 1,
        "Flying": 0,
        "Poison": 2,
        "Ground": 1,
        "Rock": 2,
        "Bug": 0.5,
        "Ghost": 1,
        "Steel": 2,
        "Fire": 2,
        "Water": 1,
        "Grass": 0.5,
        "Electric": 2,
        "Psychic": 1,
        "Ice": 1,
        "Dragon": 1,
        "Dark": 1,
        "Fairy": 1,
    },
    "Rock": {
        "Normal": 1,
        "Fighting": 0.5,
        "Flying": 2,
        "Poison": 1,
        "Ground": 0.5,
        "Rock": 1,
        "Bug": 2,
        "Ghost": 1,
        "Steel": 0.5,
        "Fire": 2,
        "Water": 1,
        "Grass": 1,
        "Electric": 1,
        "Psychic": 1,
        "Ice": 2,
        "Dragon": 1,
        "Dark": 1,
        "Fairy": 1,
    },
    "Bug": {
        "Normal": 1,
        "Fighting": 0.5,
        "Flying": 0.5,
        "Poison": 0.5,
        "Ground": 1,
        "Rock": 1,
        "Bug": 1,
        "Ghost": 0.5,
        "Steel": 0.5,
        "Fire": 0.5,
        "Water": 1,
        "Grass": 2,
        "Electric": 1,
        "Psychic": 2,
        "Ice": 1,
        "Dragon": 1,
        "Dark": 2,
        "Fairy": 0.5,
    },
    "Ghost": {
        "Normal": 0,
        "Fighting": 1,
        "Flying": 1,
        "Poison": 1,
        "Ground": 1,
        "Rock": 1,
        "Bug": 1,
        "Ghost": 2,
        "Steel": 1,
        "Fire": 1,
        "Water": 1,
        "Grass": 1,
        "Electric": 1,
        "Psychic": 2,
        "Ice": 1,
        "Dragon": 1,
        "Dark": 0.5,
        "Fairy": 1,
    },
    "Steel": {
        "Normal": 1,
        "Fighting": 1,
        "Flying": 1,
        "Poison": 1,
        "Ground": 1,
        "Rock": 2,
        "Bug": 1,
        "Ghost": 1,
        "Steel": 0.5,
        "Fire": 0.5,
        "Water": 0.5,
        "Grass": 1,
        "Electric": 0.5,
        "Psychic": 1,
        "Ice": 2,
        "Dragon": 1,
        "Dark": 1,
        "Fairy": 2,
    },
    "Fire": {
        "Normal": 1,
        "Fighting": 1,
        "Flying": 1,
        "Poison": 1,
        "Ground": 1,
        "Rock": 0.5,
        "Bug": 2,
        "Ghost": 1,
        "Steel": 2,
        "Fire": 0.5,
        "Water": 0.5,
        "Grass": 2,
        "Electric": 1,
        "Psychic": 1,
        "Ice": 2,
        "Dragon": 0.5,
        "Dark": 1,
        "Fairy": 1,
    },
    "Water": {
        "Normal": 1,
        "Fighting": 1,
        "Flying": 1,
        "Poison": 1,
        "Ground": 2,
        "Rock": 2,
        "Bug": 1,
        "Ghost": 1,
        "Steel": 1,
        "Fire": 2,
        "Water": 0.5,
        "Grass": 0.5,
        "Electric": 1,
        "Psychic": 1,
        "Ice": 1,
        "Dragon": 0.5,
        "Dark": 1,
        "Fairy": 1,
    },
    "Grass": {
        "Normal": 1,
        "Fighting": 1,
        "Flying": 0.5,
        "Poison": 0.5,
        "Ground": 2,
        "Rock": 2,
        "Bug": 0.5,
        "Ghost": 1,
        "Steel": 0.5,
        "Fire": 0.5,
        "Water": 2,
        "Grass": 0.5,
        "Electric": 1,
        "Psychic": 1,
        "Ice": 1,
        "Dragon": 0.5,
        "Dark": 1,
        "Fairy": 1,
    },
    "Electric": {
        "Normal": 1,
        "Fighting": 1,
        "Flying": 2,
        "Poison": 1,
        "Ground": 0,
        "Rock": 1,
        "Bug": 1,
        "Ghost": 1,
        "Steel": 1,
        "Fire": 1,
        "Water": 2,
        "Grass": 0.5,
        "Electric": 0.5,
        "Psychic": 1,
        "Ice": 1,
        "Dragon": 0.5,
        "Dark": 1,
        "Fairy": 1,
    },
    "Psychic": {
        "Normal": 1,
        "Fighting": 2,
        "Flying": 1,
        "Poison": 2,
        "Ground": 1,
        "Rock": 1,
        "Bug": 1,
        "Ghost": 1,
        "Steel": 0.5,
        "Fire": 1,
        "Water": 1,
        "Grass": 1,
        "Electric": 1,
        "Psychic": 0.5,
        "Ice": 1,
        "Dragon": 1,
        "Dark": 0,
        "Fairy": 1,
    },
    "Ice": {
        "Normal": 1,
        "Fighting": 1,
        "Flying": 2,
        "Poison": 1,
        "Ground": 2,
        "Rock": 1,
        "Bug": 1,
        "Ghost": 1,
        "Steel": 0.5,
        "Fire": 0.5,
        "Water": 0.5,
        "Grass": 2,
        "Electric": 1,
        "Psychic": 1,
        "Ice": 0.5,
        "Dragon": 2,
        "Dark": 1,
        "Fairy": 1,
    },
    "Dragon": {
        "Normal": 1,
        "Fighting": 1,
        "Flying": 1,
        "Poison": 1,
        "Ground": 1,
        "Rock": 1,
        "Bug": 1,
        "Ghost": 1,
        "Steel": 0.5,
        "Fire": 1,
        "Water": 1,
        "Grass": 1,
        "Electric": 1,
        "Psychic": 1,
        "Ice": 1,
        "Dragon": 2,
        "Dark": 1,
        "Fairy": 0,
    },
    "Dark": {
        "Normal": 1,
        "Fighting": 0.5,
        "Flying": 1,
        "Poison": 1,
        "Ground": 1,
        "Rock": 1,
        "Bug": 1,
        "Ghost": 2,
        "Steel": 1,
        "Fire": 1,
        "Water": 1,
        "Grass": 1,
        "Electric": 1,
        "Psychic": 2,
        "Ice": 1,
        "Dragon": 1,
        "Dark": 0.5,
        "Fairy": 0.5,
    },
    "Fairy": {
        "Normal": 1,
        "Fighting": 2,
        "Flying": 1,
        "Poison": 0.5,
        "Ground": 1,
        "Rock": 1,
        "Bug": 1,
        "Ghost": 1,
        "Steel": 0.5,
        "Fire": 0.5,
        "Water": 1,
        "Grass": 1,
        "Electric": 1,
        "Psychic": 1,
        "Ice": 1,
        "Dragon": 2,
        "Dark": 2,
        "Fairy": 1,
    },
}


# Returns the appropriate text for displaying
def owner(mon, player_mon):
    if mon == player_mon:
        return "Your"
    else:
        return "The opposing"


# Dictionary to get appropriate status text for UI
status_name = {"BRN": "burnt", "PAR": "paralyzed"}
