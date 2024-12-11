import data

discharge = data.Move(
    "Discharge",
    "Electric",
    "Special",
    80,
    100,
    15,
    15,
    0,
    f"Deals damage with a 30% chance to paralyze",
    ["Status", "PAR", 30],
)
body_slam = data.Move(
    "Body Slam",
    "Normal",
    "Physical",
    85,
    100,
    15,
    15,
    0,
    f"Deals damage with a 30% chance to paralyze",
    ["Status", "PAR", 30],
)
thunder_wave = data.Move(
    "Thunder Wave",
    "Electric",
    "Status",
    0,
    90,
    20,
    20,
    0,
    f"Paralyzes the enemy",
    ["Status", "PAR", 100],
)
work_up = data.Move(
    "Work Up",
    "Normal",
    "Status",
    0,
    100,
    20,
    20,
    0,
    f"Raises Atk and SpA by 1 stage",
    ["Stat Change", "Self", "multiplier_attack", 1, "multiplier_sp_attack", 1],
)
bulldoze = data.Move(
    "Bulldoze",
    "Ground",
    "Physical",
    60,
    100,
    15,
    15,
    0,
    f"Deals damage & reduces enemy Spe by 1 stage",
    ["Stat Change", "Enemy", "multiplier_speed", -1],
)
ice_shard = data.Move(
    "Ice Shard", "Ice", "Physical", 40, 100, 30, 30, 1, f"Always goes first", []
)
bulk_up = data.Move(
    "Bulk Up",
    "Fighting",
    "Status",
    0,
    100,
    15,
    15,
    0,
    f"Raises Atk & Def by 1 stage",
    ["Stat Change", "Self", "multiplier_attack", 1, "multiplier_defense", 1],
)
recover = data.Move(
    "Recover",
    "Normal",
    "Status",
    0,
    100,
    20,
    20,
    0,
    f"Heals 50% HP",
    ["Heal", 50],
)
magical_leaf = data.Move(
    "Magical Leaf", "Grass", "Special", 60, 100, 20, 20, 0, f"Deals damage", []
)
trailblaze = data.Move(
    "Trailblaze",
    "Grass",
    "Physical",
    50,
    100,
    20,
    20,
    0,
    f"Raises Spe by 1 stage",
    ["Stat Change", "Self", "multiplier_speed", 1],
)
hydro_pump = data.Move(
    "Hydro Pump", "Water", "Special", 110, 80, 5, 5, 0, f"Deals damage", []
)
chilling_water = data.Move(
    "Chilling Water",
    "Water",
    "Special",
    50,
    100,
    20,
    20,
    0,
    f"Deals damage & reduces enemy Atk by 1 stage",
    ["Stat Change", "Enemy", "multiplier_attack", -1],
)
calm_mind = data.Move(
    "Calm Mind",
    "Psychic",
    "Status",
    0,
    100,
    20,
    20,
    0,
    f"Raises SpA & SpD by 1 stage",
    [
        "Stat Change",
        "Self",
        "multiplier_sp_attack",
        1,
        "multiplier_sp_defense",
        1,
    ],
)
flame_charge = data.Move(
    "Flame Charge",
    "Fire",
    "Physical",
    50,
    100,
    20,
    20,
    0,
    f"Raises Spe by 1 stage",
    ["Stat Change", "Self", "multiplier_speed", 1],
)
will_o_wisp = data.Move(
    "Will-O-Wisp",
    "Fire",
    "Status",
    0,
    85,
    15,
    15,
    0,
    f"Burns the enemy",
    ["Status", "BRN", 100],
)
swords_dance = data.Move(
    "Swords Dance",
    "Normal",
    "Status",
    0,
    100,
    20,
    20,
    0,
    f"Raises Atk by 2 stages",
    ["Stat Change", "Self", "multiplier_attack", 2],
)
