from tkinter import *
import data, move_data, pokemon_data, turns, bot_algorithm, damage_calculation, random

ui = Tk()

# title of the ui
ui.title("Promptkemon")

# dimension of the ui
ui.geometry("1920x1200")

# screen width and height
screen_width = ui.winfo_screenwidth()
screen_height = ui.winfo_screenheight()

# list of pokemon images, buttons, and data
pokemon_images = []

# declaring chosen pokemon
chosen_pokemon = pokemon_data.pikachu.copy()
# declaring enemy's pokemon
enemy_pokemon = pokemon_data.pikachu.copy()
# pokemon's index for showing picture
pokemon_index = {}
# declaring the player move, will be updated as the functions run
player_move = move_data.body_slam
#Text list
display_list = []
#End scene's text list
end_list = []
# Global variables are not healthy, but as we have limited time, this is
# the fastest way to access these variables through multiple functions.
# However, for tkinter's variables, since we are going to execute this directly
# so we don't really need a class to put all the variables inside, that is the reason
# why we put them globally.

# function


# Selecting pokemon function
def select_pokemon(var):
    global chosen_pokemon, enemy_pokemon
    chosen_pokemon = var.copy()
    enemy_pokemon = random.choice(pokemon_images)[3].copy()
    battling_ui()


# Hovering texts
def on_enter(var, event):
    var.place(x=event.widget.winfo_x() - 90, y=event.widget.winfo_y() - 50)


def on_leave(var, event):
    var.place_forget()


# clearing widget function
def clear_widget():
    for widget in ui.winfo_children():
        if widget != background_label:
            widget.place_forget()
            widget.pack_forget()


# Menu function
def show_menu():
    clear_widget()
    background_label.place(x=0, y=0)
    logo_label.place(x=240, y=50)
    play_button.place(x=515, y=380)
    ui.update_idletasks()


# Next and previous buttons function:
iter = -3


def show_pokemon(it, next_or_prev):
    global iter
    if next_or_prev == 0:  # 0 is next
        if it == -3:
            for i in range(len(pokemon_images) - 1, -1, -1):
                if (i + 1) % 3 == 0 and (i + 1) != (len(pokemon_images)):
                    break
                pokemon_images[i][2].place_forget()
        else:
            for i in range(it, min(it + 3, len(pokemon_images)), 1):
                pokemon_images[i][2].place_forget()
        for i in range(it + 3, min(it + 6, len(pokemon_images)), 1):
            pokemon_images[i][2].place(
                x=(screen_width / 4) * (i % 3 + 1) - 100, y=225
            )
        ui.update_idletasks()
        iter = iter + 3
        if iter + 3 >= len(pokemon_images):
            iter = -3
        next_button = Button(
            ui,
            text="Next",
            width=15,
            height=5,
            command=lambda: [show_pokemon(iter, 0)],
        )
    else:  # 1 is prev
        if it == -3:
            for i in range(len(pokemon_images) - 1, -1, -1):
                if (i + 1) % 3 == 0 and (i + 1) != (len(pokemon_images)):
                    break
                pokemon_images[i][2].place_forget()
        else:
            for i in range(it, min(it + 3, len(pokemon_images)), 1):
                pokemon_images[i][2].place_forget()
        if it == 0:
            for i in range(len(pokemon_images) - 1, -1, -1):
                if (i + 1) % 3 == 0 and (i + 1) != (len(pokemon_images)):
                    break
                pokemon_images[i][2].place(
                    x=(screen_width / 4) * (i % 3 + 1) - 100, y=225
                )
        else:
            if it == -3:
                for i in range(
                    len(pokemon_images) - ((len(pokemon_images) - 1) % 3) - 2,
                    len(pokemon_images) - ((len(pokemon_images) - 1) % 3) - 5,
                    -1,
                ):
                    pokemon_images[i][2].place(
                        x=(screen_width / 4) * (i % 3 + 1) - 100, y=225
                    )
            else:
                for i in range(it - 1, it - 4, 1):
                    pokemon_images[i][2].place(
                        x=(screen_width / 4) * (i % 3 + 1) - 100, y=225
                    )
        ui.update_idletasks()
        iter = iter - 3
        if iter < -3:
            iter = 0
        prev_button = Button(
            ui,
            text="Previous",
            width=15,
            height=5,
            command=lambda: [show_pokemon(iter, 1)],
        )


# Battling ui function
# Basically, chosen_pokemon and enemy_pokemon only get the update after pokemon is selected, so all the battling widgets need to be updated here.
# Defining widgets under the function is not needed since all the widgets that require update are only used in the battling scene, so they can be placed instantly once the function is called.
# Other constant widgets can be defined globally.


#Battling functions
#Does effects of status moves
def do_move_status(target, move):
    applied_status = move.effect[1]
    target.change_status(applied_status)
    display_text = f"{data.owner(target,chosen_pokemon)} {target.name} got {data.status_name[applied_status]}!"
    display_list.append(display_text)


# Rolls chance for status application.
def roll_status(chance):
    rng = random.randint(1, 100)
    return rng < chance


# Applies stat changes and updates UI.
def do_move_stats(user, target, move):
    # Gets number of affected stats
    no_of_affected_stats = int((len(move.effect) - 2) / 2)
    # Loops through affected stats
    for i in range(no_of_affected_stats):
        # ('Log -- stat '+str(i))
        # Setup
        target_dict = {"Self": user, "Enemy": target}
        affected_mon = target_dict[move.effect[1]]
        affected_stat = move.effect[2 + 2 * i]
        stat_change = move.effect[3 + 2 * i]
        # ('Log -- ',affected_mon,affected_stat)
        current_stage = getattr(affected_mon, affected_stat)
        # ('Log -- ',current_stage)
        sign = stat_change / abs(stat_change)
        # ('Log -- ',current_stage,sign)
        # Setup for UI
        sign_dict = {1: "higher", -1: "lower"}
        amount = {-1: "fell", 1: "rose", 2: "rose sharply"}
        stat_name = data.stat_name_table[affected_stat]
        # If the stage is capped in positve or negative, return appropriate message for UI
        if current_stage == 4**sign:
            display_text = f"{data.owner(affected_mon,chosen_pokemon)} {affected_mon.name}'s {stat_name} won't go any {sign_dict[sign]}!"
            
            display_list.append(display_text)
        # Else, do the stat change and update UI
        else:
            # (affected_stat,stat_change)
            affected_mon.change_stat_stage(affected_stat, stat_change)
            display_text = f"{data.owner(affected_mon,chosen_pokemon)} {affected_mon.name}'s {stat_name} {amount[stat_change]}!"
            display_list.append(display_text)


# Does healing move and update UI
def do_move_heal(user, move):
    heal_amount = min(user.hp * move.effect[1] // 100, user.hp-user.current_hp)
    user.change_hp(heal_amount)
    display_text = f"{data.owner(user,chosen_pokemon)} {user.name} and recovered {heal_amount} health!"
    display_list.append(display_text)


# Does any move
def do_move(user, target, move):
    # Reduce move's PP by 1
    move.change_pp(-1)
    # Update UI
    display_text = (
        f"{data.owner(user,chosen_pokemon)} {user.name} used {move.name}!"
    )
    display_list.append(display_text)
    # Roll for accuracy
    if random.randint(1, 100) > move.accuracy:
        display_text = f"It missed!"
        display_list.append(display_text)
    # If passes accuracy check, move on.
    else:
        # For attacking moves,
        if move.category != "Status":
            # Check type immunity, if true, update UI
            if bot_algorithm.check_type_immunity(target, move):
                display_text = f"It has no effect on {data.owner(user,chosen_pokemon).lower()} {target.name}..."
                display_list.append(display_text)
            # Calculate damage
            dmg, type_mod, critical = damage_calculation.calculate_damage(
                user, target, move
            )
            target.change_hp(-1 * dmg)
            # Display message if the move crit
            if critical:
                display_text = "A critical hit! "
                display_list.append(display_text)
            # Display type effectiveness message
            if type_mod > 1:
                display_text = "It's super effective! "
                display_list.append(display_text)
            elif type_mod < 1:
                display_text = "It's not very effective... "
                display_list.append(display_text)
            display_text = f"It dealt {dmg} dmg! {data.owner(target,chosen_pokemon)} {target.name} is at {target.current_hp}/{target.hp}"
            display_list.append(display_text)
        # If the move has an effect, do the effect
        if len(move.effect) != 0:
            # For status effects,
            if move.effect[0] == "Status":
                # Checks if the move is a attacking move
                if move.category != "Status":
                    # Attacking moves do not give a failure message when failing to apply status.
                    # Thus, just check if status is applied, if so, apply it. Otherwise, do nothing.
                    if not (
                        bot_algorithm.check_status_failure(target, move)[0]
                    ) and roll_status(move.effect[2]):
                        do_move_status(target, move)
                # Checks for status move failure
                elif bot_algorithm.check_status_failure(target, move)[0]:
                    # Returns appropriate failure message on failure
                    error = bot_algorithm.check_status_failure(target, move)[1]
                    if error == "type immune" or error == "para immune":
                        display_text = f"It doesn't affect {target.name}..."
                        display_list.append(display_text)
                    else:
                        display_text = f"{data.owner(user,chosen_pokemon)} {target.name} is already {target.status}!"
                        display_list.append(display_text)
                # If no failure, apply the status
                else:
                    do_move_status(target, move)
            # For stat changes,
            elif move.effect[0] == "Stat Change":
                # Failure message built into do_move_stats function.
                do_move_stats(user, target, move)
            # For healing,
            elif move.effect[0] == "Heal":
                if bot_algorithm.check_heal_failure(
                    user, move, 0
                ):  # Assuming heals 50% HP
                    display_text = f"{data.owner(user,chosen_pokemon)} {user.name} is already at full health!"
                    display_list.append(display_text)
                else:
                    do_move_heal(user, move)


# battling simulator
def battling(player_active, enemy_active):
    # Battle Loop
    enemy_move = bot_algorithm.bot_choose_move(enemy_active, player_active)
    # (f'Log -- Player choose {player_move}, Bot choose {enemy_move}')

    # Get the turn order
    turn_order = turns.fastest(
        player_active, enemy_active, player_move, enemy_move
    )
    # Sets up the order of chosen_moves to correspond to the turn order.
    if turn_order[0] == player_active:
        chosen_moves = player_move, enemy_move
    else:
        chosen_moves = enemy_move, player_move
    # (f'Log -- Turn order is {turn_order[0].name,turn_order[1].name}')

    # Use move loop.
    for i in range(2):
        user = turn_order[i]
        target = turn_order[1 - i]
        chosen_move = chosen_moves[i]
        didnt_move_msg = {
            "PAR": f"{user} is paralyzed!",
            "SLP": f"{user} is sleeping!",
            "FRZ": f"{user} is frozen!",
        }
        # (f'{user} is trying to use {chosen_move} on {target}')
        # If the current mon can move, do the move it chose.
        if turns.does_move(user):
            do_move(user, target, chosen_move)
            # (f'Log -- {user} used {chosen_move},{target.current_hp},{target.hp}')
        # Else, display the appropriate message.
        else:
            display_text = didnt_move_msg[user.status]
            display_list.append(display_text)

        # Check for KO.
        if target.current_hp == 0:
            # target's sprite disappears, f'{target} fainted!' is displayed, battle ends
            display_text = f"{target.name} fainted!"
            display_list.append(display_text)
            end_list.append(f"{data.owner(user,chosen_pokemon)} {user.name} won!\nThanks for playing!")
            return

    # End Turn
    for i in range(len(turn_order)):
        # Deal burn damage.
        mon = turn_order[i]
        enemy = turn_order[1 - i]
        if mon.status == "BRN":
            damage = -1 * (mon.hp // 16)
            display_text = f"{data.owner(mon,chosen_pokemon)} {mon.name} was hurt by its burn!"
            display_list.append(display_text)
            mon.change_hp(damage)
        # Check for KO by burn.
        if mon.current_hp == 0:
            # target's sprite disappears, f'{target} fainted!' is displayed, battle ends
            display_text = f"{mon.name} fainted!"
            display_list.append(display_text)
            end_list.append(f"{data.owner(enemy,chosen_pokemon)} {enemy.name} won!\nThanks for playing!")
            return



    

def clear_move_widget(button_list):
    for widget in ui.winfo_children():
        if widget in button_list:
            widget.place_forget()
            widget.pack_forget()

# Update previous HP and status of the Pokemon before heading to the next battle simulation
def update_info():
    # Info
    clear_widget()
    moves_box_label.place(x=50, y=530)
    pokemon_images[pokemon_index[chosen_pokemon.name]][1].place(x=300, y=220)
    pokemon_images[pokemon_index[enemy_pokemon.name]][0].place(x=900, y=100)
    
    ui.update_idletasks()
    if chosen_pokemon.status == "Null":
        main_status = ""
    else:
        main_status = f" || {chosen_pokemon.status}"
    if enemy_pokemon.status == "Null":
        enemy_status = ""
    else:
        enemy_status = f" || {enemy_pokemon.status}"
    main_info = Label(
        ui,
        bg="#cee7f9",
        fg="#000000",
        text=f"{chosen_pokemon.name} || HP: {chosen_pokemon.current_hp}/{chosen_pokemon.hp}{main_status}",
    )
    main_info.config(font=("Comic Sans MS", 30))
    enemy_info = Label(
        ui,
        bg="#cee7f9",
        fg="#000000",
        text=f"{enemy_pokemon.name} || HP: {enemy_pokemon.current_hp}/{enemy_pokemon.hp}{enemy_status}",
    )
    enemy_info.config(font=("Comic Sans MS", 30))
    main_info.place(x=310, y=150)
    enemy_info.place(x=900, y=400)
    ui.update_idletasks()


# Function to get the move input from player and pass it to the battling simulation function.
def update_battle_move(arg):
    global player_move
    player_move = arg
    if (chosen_pokemon.current_hp!=0 and enemy_pokemon.current_hp!=0):
        battling(chosen_pokemon, enemy_pokemon)
        show_text(display_list, 0, 800)

#This to show the text on the display. 
def show_text(txt, index, delay):
    global text_label
    if index < len(txt):
        text_label.config(text=txt[index])
        text_label.place(x=140, y=580)
        ui.update_idletasks()
        ui.after(delay, text_label.place_forget)
        ui.after(delay,show_text, txt, index + 1, delay)
    else:
        txt.clear()
        if (chosen_pokemon.current_hp!=0 and enemy_pokemon.current_hp!=0):
            battling_ui()
        else:
            if (txt==end_list and len(txt)==0):
                text_label.config(text="Restarting...")
                text_label.place(x=140,y=580)
                return
            else:
                update_info()
                show_text(end_list, 0, 3000)
                ui.after(4500,clear_widget)
                ui.after(4500,show_menu)



# Showing the battling ui
def battling_ui():
    clear_widget()
    update_info()
    moves_box_label.place(x=50, y=530)
    pokemon_images[pokemon_index[chosen_pokemon.name]][1].place(x=300, y=220)
    pokemon_images[pokemon_index[enemy_pokemon.name]][0].place(x=900, y=100)
    ui.update_idletasks()
    # Move buttons
    move_button_list = []
    move_button_description_list = []
    for i in range(len(chosen_pokemon.moveset)):
        move = Button(
            ui,
            text=f"{chosen_pokemon.moveset[i].name}",
            width=15,
            heigh=5,
            command=lambda it=i, move_button_list=move_button_list: [
                clear_move_widget(move_button_list), update_battle_move(chosen_pokemon.moveset[it])
            ],
        )
        move_button_list.append(move)
        move_description = Label(
            ui,
            text=f"Move type: {chosen_pokemon.moveset[i].move_type}, category: {chosen_pokemon.moveset[i].category}, base power: {chosen_pokemon.moveset[i].base_power}\nAccuracy: {chosen_pokemon.moveset[i].accuracy}, max pp: {chosen_pokemon.moveset[i].max_pp}, current pp: {chosen_pokemon.moveset[i].current_pp}\nDescription: {chosen_pokemon.moveset[i].description}",
            font=("Comic Sans MS", 15),
        )
        move_button_description_list.append(move_description)
        move_button_list[i].bind(
            "<Enter>",
            lambda event, move_description_tooltip=move_button_description_list[
                i
            ]: on_enter(move_description_tooltip, event),
        )
        move_button_list[i].bind(
            "<Leave>",
            lambda event, move_description_tooltip=move_button_description_list[
                i
            ]: on_leave(move_description_tooltip, event),
        )
        move_button_list[i].place(x=180 * (i + 1) + 150 * i, y=650)


# pokemon choosing screen function
def pokemon_choosing_scene():
    clear_widget()
    Choose_title.pack()
    show_pokemon(-3, 0)
    prev_button.place(x=200, y=600)
    next_button.place(x=1140, y=600)
    ui.update_idletasks()
    


# Background
background = PhotoImage(file="images/background.png")
background_label = Label(ui, image=background)

# Logo
logo = PhotoImage(file="images/logo.png")
logo_label = Label(ui, bg="#cee7f9", image=logo)

# Next and prev buttons
next_button = Button(
    ui, text="Next", width=15, height=5, command=lambda: [show_pokemon(iter, 0)]
)
prev_button = Button(
    ui,
    text="Previous",
    width=15,
    height=5,
    command=lambda: [show_pokemon(iter, 1)],
)

# Play button
play_button_img = PhotoImage(file="images/play.png")
play_button = Button(
    ui,
    image=play_button_img,
    width=440,
    height=120,
    command=pokemon_choosing_scene,
)

# Choose your pokemon text
Choose_title = Label(
    ui, bg="#cee7f9", fg="#000000", text="Choose your pokemon:"
)
Choose_title.config(font=("Comic Sans MS", 60))

# Moves box
moves_box = PhotoImage(file="images/move_box.png")
moves_box_label = Label(ui, image=moves_box, width=1400, height=300)

# Enemy and player info
main_status = ""
enemy_status = ""
main_info = Label(
    ui,
    bg="#cee7f9",
    fg="#000000",
    text=f"{chosen_pokemon.name} || HP: {chosen_pokemon.current_hp}/{chosen_pokemon.hp}{main_status}",
)
main_info.config(font=("Comic Sans MS", 30))
enemy_info = Label(
    ui,
    bg="#cee7f9",
    fg="#000000",
    text=f"{enemy_pokemon.name} || HP: {enemy_pokemon.current_hp}/{enemy_pokemon.hp}{enemy_status}",
)
enemy_info.config(font=("Comic Sans MS", 30))

# Text info
text_label = Label(
    ui, text="", bg="#FFFFFF", fg="#000000", font=("Comic Sans MS", 30)
)

# Pokemon images
pikachu_front = PhotoImage(file="images/pikachu_front.png")
pikachu_front_label = Label(ui, bg="#cee7f9", image=pikachu_front)
pikachu_back = PhotoImage(file="images/pikachu_back.png")
pikachu_back_label = Label(ui, bg="#cee7f9", image=pikachu_back)
pikachu_button_img = PhotoImage(file="images/pikachu_button.png")
pikachu_button = Button(
    ui,
    bg="#cee7f9",
    image=pikachu_button_img,
    command=lambda: [select_pokemon(pokemon_data.pikachu)],
)
pokemon_images.append(
    (
        pikachu_front_label,
        pikachu_back_label,
        pikachu_button,
        pokemon_data.pikachu,
    )
)
pokemon_index["Pikachu"] = 0

phanpy_front = PhotoImage(file="images/phanpy_front.png")
phanpy_front_label = Label(ui, bg="#cee7f9", image=phanpy_front)
phanpy_back = PhotoImage(file="images/phanpy_back.png")
phanpy_back_label = Label(ui, bg="#cee7f9", image=phanpy_back)
phanpy_button_img = PhotoImage(file="images/phanpy_button.png")
phanpy_button = Button(
    ui,
    bg="#cee7f9",
    image=phanpy_button_img,
    command=lambda: [select_pokemon(pokemon_data.phanpy)],
)
pokemon_images.append(
    (phanpy_front_label, phanpy_back_label, phanpy_button, pokemon_data.phanpy)
)
pokemon_index["Phanpy"] = 1

treecko_front = PhotoImage(file="images/treecko_front.png")
treecko_front_label = Label(ui, bg="#cee7f9", image=treecko_front)
treecko_back = PhotoImage(file="images/treecko_back.png")
treecko_back_label = Label(ui, bg="#cee7f9", image=treecko_back)
treecko_button_img = PhotoImage(file="images/treecko_button.png")
treecko_button = Button(
    ui,
    bg="#cee7f9",
    image=treecko_button_img,
    command=lambda: [select_pokemon(pokemon_data.treecko)],
)
pokemon_images.append(
    (
        treecko_front_label,
        treecko_back_label,
        treecko_button,
        pokemon_data.treecko,
    )
)
pokemon_index["Treecko"] = 2

psyduck_front = PhotoImage(file="images/psyduck_front.png")
psyduck_front_label = Label(ui, bg="#cee7f9", image=psyduck_front)
psyduck_back = PhotoImage(file="images/psyduck_back.png")
psyduck_back_label = Label(ui, bg="#cee7f9", image=psyduck_back)
psyduck_button_img = PhotoImage(file="images/psyduck_button.png")
psyduck_button = Button(
    ui,
    bg="#cee7f9",
    image=psyduck_button_img,
    command=lambda: [select_pokemon(pokemon_data.psyduck)],
)
pokemon_images.append(
    (
        psyduck_front_label,
        psyduck_back_label,
        psyduck_button,
        pokemon_data.psyduck,
    )
)
pokemon_index["Psyduck"] = 3

charmander_front = PhotoImage(file="images/charmander_front.png")
charmander_front_label = Label(ui, bg="#cee7f9", image=charmander_front)
charmander_back = PhotoImage(file="images/charmander_back.png")
charmander_back_label = Label(ui, bg="#cee7f9", image=charmander_back)
charmander_button_img = PhotoImage(file="images/charmander_button.png")
charmander_button = Button(
    ui,
    bg="#cee7f9",
    image=charmander_button_img,
    command=lambda: [select_pokemon(pokemon_data.charmander)],
)
pokemon_images.append(
    (
        charmander_front_label,
        charmander_back_label,
        charmander_button,
        pokemon_data.charmander,
    )
)
pokemon_index["Charmander"] = 4

show_menu()

ui.mainloop()
