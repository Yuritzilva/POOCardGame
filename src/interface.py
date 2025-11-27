#executable interface
import sys
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog


# Functions

def modify_player_balance():
    pass

def show_player_info():
    pass

def delete_player():
    pass

def start_game():
    pass

def show_game_history():
    pass

def show_players():
    pass

def show_all_games():
    pass

def exit_program():
    pass

def perform_action(action_name):
    pass
# Define window
root = tk.Tk()
root.title("Juego de cartas")
root.geometry("1000x600")
root.minsize(700, 420)
root.grid_rowconfigure(0, weight=0) 
root.grid_rowconfigure(1, weight=6)
root.grid_rowconfigure(2, weight=4) 
root.grid_columnconfigure(0, weight=0) 
root.grid_columnconfigure(1, weight=1)
# Menu
menubar = tk.Menu(root)

#player options
player_menu = tk.Menu(menubar, tearoff=0)
player_menu.add_command(label="Modify balance", command=modify_player_balance)
player_menu.add_command(label="Show player information", command=show_player_info)
player_menu.add_command(label="Delete player", command=delete_player)
menubar.add_cascade(label="Player", menu=player_menu)

#game options
game_menu = tk.Menu(menubar,tearoff = 0)
game_menu.add_command(label="Start game", command=start_game)
game_menu.add_command(label="Show game history", command=show_game_history)
menubar.add_cascade(label="Game", menu=game_menu)

# Players and history options
menu = tk.Menu(menubar,tearoff = 0)
menu.add_command(label="Show other players", command=show_players)
menu.add_command(label="Show other games", command=show_all_games)
menubar.add_cascade(label="Other", menu=menu)

#Exit option
exit_menu = tk.Menu(menubar, tearoff=0)
exit_menu.add_command(label="Exit card Game", command=exit_program)
menubar.add_cascade(label="Exit card Game", menu=exit_menu) 


root.config(menu=menubar)

# Frames

# Frame styles
style = ttk.Style()
style.configure("TFrame", background="#333333") 
style.configure("red.TFrame", background="#8B0000") 
style.configure("white.TLabel", foreground="#FFFFFF", background="#333333",font=("Segoe UI", 9, "bold"))
style.configure("yellow.TLabel", foreground="#FFD700",background = "#8B0000",font=("Segoe UI", 9, "bold"))
style.configure("border.TFrame", background="#FFD700") 
style.configure("Casino.TButton",mfont=("Segoe UI", 10, "bold"), foreground= "#8B0000", background="#8B0000",borderwidth=3,relief="raised")
style.map( "Casino.TButton", background=[('active', "#CC9900")],foreground=[('active', "#CC9900")])


# TOP frame
top_frame = ttk.Frame(root, style="top_frame.TFrame", padding=10)
top_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
inner = ttk.Frame(top_frame, style="top_frame.TFrame")
inner.pack(expand=True)
inner.grid_columnconfigure(0, weight=1)
#Game info
#Game ID
lbl_output_Game_ID = ttk.Label(inner, text="GAME ID", style="white.TLabel")
lbl_output_Game_ID.grid(row=0, column=0, sticky="n")
#Total current players
lbl_output_players = ttk.Label(inner, text="Number of players", style="white.TLabel")
lbl_output_players.grid(row=1, column=0, sticky="n")
#Total current pot
lbl_output_pot = ttk.Label(inner, text="Current pot:", style="white.TLabel")
lbl_output_pot.grid(row=2, column=0, sticky="n")
#Current turn
lbl_output_turn = ttk.Label(inner, text="It's current_player's turn", style="white.TLabel")
lbl_output_turn.grid(row=3, column=0, sticky="n")


# --- FRAME 1 (actions button container) ---
actions_frame = ttk.Frame(root, padding=10)
actions_frame.grid(row=1, column=0, sticky="ns")
lbl_1 = ttk.Label(actions_frame, text="Options", style="white.TLabel")
lbl_1.pack(pady=20)
#action buttons
actions = ["Fold", "Check", "Call", "Raise", "Bet", "All-in"]
for action in actions:
    btn = ttk.Button(actions_frame, text=action, command=lambda a=action: perform_action(a), style="Casino.TButton")
    btn.pack(side=tk.TOP, fill=tk.X, pady=3)

# Mensagge
lbl_help = ttk.Label(actions_frame, text="Waiting for instructions...", style= "white.TLabel")
lbl_help.pack(anchor="w", pady=(40, 0)) 

# ---FRAME 2 (content frame)
content_frame = ttk.Frame(root, padding=10, style="red.TFrame")
content_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")
content_label = ttk.Label(content_frame, text="Content", style="yellow.TLabel")
content_label.pack(pady=2)

# --- FRAME 3 (game frame) ---
game_frame = ttk.Frame(root, padding=10)
game_frame.grid(row=1, column=1, sticky="nsew")
lbl_2 = ttk.Label(game_frame, text="Card game", style="white.TLabel")
lbl_2.pack(pady=10)

# Listbox 
frame_list = ttk.Frame(game_frame, style="border.TFrame")  
frame_list.pack(fill=tk.BOTH, expand=True, pady=(6, 0)) 
lb_output = tk.Listbox(frame_list, font=("Consolas", 12), background="#145A32", fg="white",bd=0, highlightthickness=0)
lb_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)



root.mainloop()