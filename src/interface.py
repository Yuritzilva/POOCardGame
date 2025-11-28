#executable interface
import sys
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
#classes
from card import Card
from deck import Deck
from player import Player
from game import Game
from hand import Hand
from gameRule import GameRule

current_game = None
# Functions
def start_game():
    """Show form before creating game"""
    global current_game
    
    # Clear content frame
    for widget in content_frame.winfo_children():
        widget.destroy()
    
    # Create selection form
    create_player_selection_form()

def create_player_selection_form():
    """Create form to select player from database"""
    title_label = ttk.Label(content_frame, text="Select players", 
                           style="yellow.TLabel", font=("Segoe UI", 12, "bold"))
    title_label.pack(pady=10)
    
    # Load players from DB
    players = load_players_from_db()
    
    if not players:
        # No players, create new
        no_players_label = ttk.Label(content_frame, 
                                   text="No players in database. Create new players?", 
                                   style="white.TLabel")
        no_players_label.pack(pady=5)
        
        create_btn = ttk.Button(content_frame, text="Create players", 
                               command=create_players)
        create_btn.pack(pady=5)
        return

    #Frame inside content_frame 
    picker_frame = ttk.Frame(content_frame)
    picker_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Grid settings
    picker_frame.grid_columnconfigure(0, weight=1)
    picker_frame.grid_columnconfigure(1, weight=0)
    picker_frame.grid_rowconfigure(0, weight=1)

    # Scrollbar frame
    scroll_frame = ttk.Frame(picker_frame)
    scroll_frame.grid(row=0, column=0, sticky="nsew")

    # Canvas and scrollbar
    canvas = tk.Canvas(scroll_frame, bg="#333333", highlightthickness=0)
    scrollbar = ttk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Checkboxes inside scroll frame
    player_vars = {}
    for i, player in enumerate(players):
        var = tk.BooleanVar()
        chk = ttk.Checkbutton(scrollable_frame, text=f"{player.name} (${player.balance})", 
                            variable=var, style="White.TCheckbutton")
        chk.pack(anchor="w", padx=10, pady=2)
        player_vars[player.id] = (var, player)

    # Buttons
    btn_frame = ttk.Frame(picker_frame)
    btn_frame.grid(row=0, column=1, sticky="nse")

    start_btn = ttk.Button(btn_frame, text="Start game!", command=lambda: start_game_with_players(player_vars), style="Casino.TButton")
    start_btn.pack(pady=5)

    cancel_btn = ttk.Button(btn_frame, text="Cancel", command=clear_content_frame, style="Casino.TButton")
    cancel_btn.pack(pady=5)

def load_players_from_db():
    """Load players from DB"""
    from player import Player
    players = []
    try:
        players = Player.get_all_players()
    except:
        print("No players in DB")
        pass
    return players

def create_players():
    """Show form to create new players"""
    clear_content_frame()
    
    # Title
    title_label = ttk.Label(content_frame, text="Create new player", 
                           style="yellow.TLabel", font=("Segoe UI", 12, "bold"))
    title_label.pack(pady=10)
    
    form_frame = ttk.Frame(content_frame)
    form_frame.pack(pady=10)
    
    # Name
    name_label = ttk.Label(form_frame, text="Player's name:", style="white.TLabel")
    name_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
    
    name_entry = ttk.Entry(form_frame, width=20, font=("Segoe UI", 10))
    name_entry.grid(row=0, column=1, padx=5, pady=5)
    name_entry.focus()
    
    # Balance
    balance_label = ttk.Label(form_frame, text="Initial balance ($):", style="white.TLabel")
    balance_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
    
    balance_entry = ttk.Entry(form_frame, width=20, font=("Segoe UI", 10))
    balance_entry.grid(row=1, column=1, padx=5, pady=5)
    balance_entry.insert(0, "100")  
    
    # Buttons
    btn_frame = ttk.Frame(content_frame)
    btn_frame.pack(pady=10)
    
    def create_player():
        """Create player with form info"""
        name = name_entry.get().strip()
        balance_text = balance_entry.get().strip()
        
        # Validations
        if not name:
            messagebox.showerror("Error", "Can't have empty name")
            return
        
        try:
            balance = float(balance_text)
            if balance < 0:
                messagebox.showerror("Error", "balance can't be negative")
                return
        except ValueError:
            messagebox.showerror("Error", "balance must be a valid number")
            return
        
        # Crete player
        try:
            from player import Player
            player = Player.set_player(name, balance)
            messagebox.showinfo("Success", f"Player '{player.name}' created with ${player.balance}")
            clear_content_frame()
            start_game()  
        except Exception as e:
            messagebox.showerror("Error", f"Can't create player: {e}")
    
    create_btn = ttk.Button(btn_frame, text="Create player", 
                           command=create_player)
    create_btn.grid(row=0, column=0, padx=5)
    
    cancel_btn = ttk.Button(btn_frame, text="Cancel", 
                           command=lambda: clear_content_frame() or start_game())
    cancel_btn.grid(row=0, column=1, padx=5)

def start_game_with_players(player_vars):
    """Start game with current players"""
    global current_game, current_player_index
    
    selected_players = []
    for player_id, (var, player) in player_vars.items():
        if var.get():
            selected_players.append(player)
    
    if len(selected_players) < 2:
        messagebox.showerror("Error", "pick 2 players at least")
        return
    
    if len(selected_players) > 8:
        messagebox.showerror("Error", "8 players max")
        return
    
    # Create and start game
    current_game = Game(players=selected_players)
    current_game.lbl_help = lbl_help
    current_game.start_game()
    current_player_index = 0
    
    # clear content and display game
    clear_content_frame()
    update_game_display()
    update_actions_display()
    
    # Show in listbox
    lb_output.delete(0, tk.END)
    lb_output.insert(tk.END, "Game started!")
    for player in selected_players:
        lb_output.insert(tk.END, f" {player.name} - ${player.balance}")
    lb_output.insert(tk.END, "---")

def clear_content_frame():
    """Limpiar el content_frame"""
    for widget in content_frame.winfo_children():
        widget.destroy()

def update_game_display():
    """Update game info at the top"""
    if current_game:
        lbl_output_Game_ID.config(text=f"GAME ID: {current_game.game_id}")
        lbl_output_players.config(text=f"Players: {len([p for p in current_game.players if not p.folded])}/{len(current_game.players)}")
        lbl_output_pot.config(text=f"Pot: ${current_game.pot}")
        
        # Current player turn
        current_player = current_game.players[current_player_index]
        status = "FOLDED" if current_player.folded else f"${current_player.balance}"
        lbl_output_turn.config(text=f"Turn: {current_player.name} - {status}")

def update_actions_display():
    """Update action buttons and game state"""
    if not current_game:
        return
    
    current_player = current_game.players[current_player_index]

    # Show community cards in listbox
    lb_output.delete(0, tk.END)
    lb_output.insert(tk.END, "COMMUNITY CARDS:")
    for card in current_game.community_cards:
        lb_output.insert(tk.END, f"  {card}")
    
    lb_output.insert(tk.END, "---")
    
    # Show player hands (ONLY PLAYER IN TURN)
    lb_output.insert(tk.END, f"{current_player.name}'s HAND:")
    if current_player.folded:
         lb_output.insert(tk.END, f"  {current_player.name}: FOLDED")
    else: 
        cards_str = " ".join(str(card) for card in current_player.hand)
        lb_output.insert(tk.END, f"{cards_str}")
    
    # Show other players status (but not their cards)
    lb_output.insert(tk.END, "---")
    lb_output.insert(tk.END, "OTHER PLAYERS:")
    for player in current_game.players:
        if player != current_player:
            status = "FOLDED" if player.folded else f"Active (${player.balance})"
            lb_output.insert(tk.END, f"  {player.name}: {status}")

    # Update help message
    current_player = current_game.players[current_player_index]
    if current_player.folded:
        lbl_help.config(text=f"{current_player.name} is folded - waiting...")
    else:
        lbl_help.config(text=f"{current_player.name}'s turn - Choose an action")

def show_all_games():
    """Show history of all previous games"""
    clear_content_frame()
    
    # Title
    title_label = ttk.Label(content_frame, text="GAME HISTORY", 
                           style="yellow.TLabel", font=("Segoe UI", 12, "bold"))
    title_label.pack(pady=10)
    
    # Query to get game history
    games = load_game_history_from_db()
    
    if not games:
        no_games_label = ttk.Label(content_frame, 
                                  text="No previous games found", 
                                  style="white.TLabel")
        no_games_label.pack(pady=10)
        return
    
    # Create scrollable frame
    scroll_frame = ttk.Frame(content_frame)
    scroll_frame.pack(fill="both", expand=True, pady=5)
    
    canvas = tk.Canvas(scroll_frame, bg="#333333", highlightthickness=0)
    scrollbar = ttk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)
    
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Display each game
    for i, game in enumerate(games):
        game_frame = ttk.Frame(scrollable_frame, style="TFrame")
        game_frame.pack(fill="x", padx=10, pady=5)
        
        # Game info
        ttk.Label(game_frame, text=f"Game #{game['game_id']}", 
                 style="yellow.TLabel", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w")
        
        ttk.Label(game_frame, text=f"CHICKEN winner: {game['winner_name']}", 
                 style="white.TLabel").grid(row=1, column=0, sticky="w")
        
        ttk.Label(game_frame, text=f"DATE: {game['date_played']}", 
                 style="white.TLabel").grid(row=2, column=0, sticky="w")
        
        ttk.Label(game_frame, text=f"Actions: {game['total_actions']}", 
                 style="white.TLabel").grid(row=3, column=0, sticky="w")
        
        # View details button
        details_btn = ttk.Button(game_frame, text="View Details", 
                               command=lambda gid=game['game_id']: show_game_details(gid),
                               style="Casino.TButton")
        details_btn.grid(row=0, column=1, rowspan=2, padx=10)

def load_game_history_from_db():
    """Load game history from database"""
    from db_connection import get_conn
    from queries import SELECT_GAME_INFO
    conn = get_conn()
    games = []
    try:
        cur = conn.cursor()
        cur.execute(SELECT_GAME_INFO)
        
        for row in cur.fetchall():
            games.append({
                'game_id': row[0],
                'winner_name': row[1],
                'date_played': row[2].strftime("%Y-%m-%d %H:%M"),
                'total_actions': row[3]
            })
            
    except Exception as e:
        print(f"Error loading game history: {e}")
    finally:
        cur.close()
        conn.close()
    
    return games

def show_game_details(game_id):
    """Show detailed view of a specific game"""
    clear_content_frame()
    
    # Title
    title_label = ttk.Label(content_frame, text=f"GAME #{game_id} DETAILS", 
                           style="yellow.TLabel", font=("Segoe UI", 12, "bold"))
    title_label.pack(pady=10)
    
    # Load game details
    details = load_game_details_from_db(game_id)
    
    if not details:
        ttk.Label(content_frame, text="Game details not found", style="white.TLabel").pack()
        return
    
    # Game info
    info_frame = ttk.Frame(content_frame)
    info_frame.pack(pady=5, fill="x")
    
    ttk.Label(info_frame, text=f"Winner: {details['winner_name']}", style="white.TLabel").pack()
    ttk.Label(info_frame, text=f"Date: {details['date_played']}", style="white.TLabel").pack()
    
    # Player actions
    ttk.Label(content_frame, text="Player Actions:", style="white.TLabel").pack(anchor="w", pady=(10,0))
    
    for action in details['actions']:
        action_text = f"{action['player_name']} {action['action']} (${action['amount']})"
        ttk.Label(content_frame, text=action_text, style="white.TLabel").pack(anchor="w", padx=10)

def load_game_details_from_db(game_id):
    """Load detailed information for a specific game"""
    from db_connection import get_conn
    from queries import SELECT_GAME_DETAILS, SELECT_PLAY_DETAILS
    conn = get_conn()
    details = {}
    try:
        cur = conn.cursor()
        
        # Get basic game info
        cur.execute(SELECT_GAME_DETAILS, (game_id,))
        
        game_info = cur.fetchone()
        if game_info:
            details['game_id'] = game_info[0]
            details['winner_name'] = game_info[1]
            details['date_played'] = game_info[2].strftime("%Y-%m-%d %H:%M")
        else:
            return {'actions': []}
        # Get player actions
        cur.execute(SELECT_PLAY_DETAILS, (game_id,))
        
        details['actions'] = []
        for action, player_name, player_id, timestamp in cur.fetchall():
            # Parse action string (ej: "bet:$100")
            action_parts = action.split(':$')
            details['actions'].append({
                'player_name': f"#{player_id} : {player_name}",
                'action': action_parts[0],
                'amount': action_parts[1] if len(action_parts) > 1 else '0',
                'timestamp' : timestamp.strftime("%H:%M:%S")
            })
            
    except Exception as e:
        print(f"Error loading game details: {e}")
    finally:
        cur.close()
        conn.close()
    
    return details

def exit_program():
    root.destroy()

def perform_action(action_name):
    """Execute player action and advance game state"""
    global current_player_index, current_game
    
    if not current_game:
        lbl_help.config(text="No active game!")
        return
    
    current_player = current_game.players[current_player_index]
    
    # Skip folded players
    if current_player.folded:
        advance_turn()
        return
    
    # Actions that need amount input
    if action_name in ["Call", "Bet", "Raise"]:
        show_amount_input_form(action_name)
        return
    
    # Rest of actions (Fold, Check, All-in)
    if action_name == "Fold":
        current_player.fold()
        current_game.record_player_action(current_player, "fold", 0)
        lbl_help.config(text=f"{current_player.name} folded!")
        
    elif action_name == "Check":
        current_game.record_player_action(current_player, "check", 0)
        lbl_help.config(text=f"{current_player.name} checked")
        
    elif action_name == "All-in":
        all_in_amount = current_player.balance
        bet_placed = current_player.place_bet(all_in_amount)
        current_game.pot += bet_placed
        current_game.record_player_action(current_player, "all-in", all_in_amount)
        lbl_help.config(text=f"{current_player.name} went ALL-IN ${all_in_amount}!")
        check_all_in_situation()
        return
    # Advance to next player
    advance_turn()

def check_all_in_situation():
    global current_game
    
    active_players = [p for p in current_game.players if not p.folded]
    all_in_players = [p for p in active_players if p.all_in]
    
    # if there is 2 players with all in
    if len(all_in_players) >= 2:
        lbl_help.config(text="DOUBLE ALL-IN! Immediate showdown!")
        while current_game.is_active and current_game.current_round < 4:
            current_game.next_round()
        update_actions_display()
    # Only 1 all in and others can match all in
    elif len(all_in_players) == 1:
        # Verify if other players can match all in
        all_in_player = all_in_players[0]
        other_players = [p for p in active_players if p != all_in_player]
        
        can_anyone_call = any(p.balance >= all_in_player.total_bet for p in other_players)
        
        if not can_anyone_call:
            # no ona can match all in
            lbl_help.config(text=f"{all_in_player.name} wins by default (others can't match All-in)!")
            current_game.winners = [all_in_player]
            all_in_player.add_winnings(current_game.pot, 10)  # High card points
            current_game.is_active = False
            update_actions_display()
            return
    
    # Si llegamos aquí, continuar juego normal
    advance_turn()

def show_amount_input_form(action_name):
    """Show form to input amount for Call/Bet/Raise"""
    clear_content_frame()
    current_player = current_game.players[current_player_index]
    # Title
    title_label = ttk.Label(content_frame, text=f"{action_name.upper()} AMOUNT", 
                           style="yellow.TLabel", font=("Segoe UI", 12, "bold"))
    title_label.pack(pady=10)
    
    # Form frame
    form_frame = ttk.Frame(content_frame)
    form_frame.pack(pady=10)
    
    # Balance
    balance_label = ttk.Label(form_frame, text=f"Player balance: {current_player.balance}", style="white.TLabel")
    balance_label.grid(row=0, column=0, columnspan=2, sticky="w", padx=5, pady=5)

    amount_label = ttk.Label(form_frame, text="Amount ($):", style="white.TLabel")
    amount_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
    
    amount_entry = ttk.Entry(form_frame, width=15, font=("Segoe UI", 10))
    amount_entry.grid(row=1, column=1, padx=5, pady=5)
    amount_entry.focus()
    
    # Set default values based on action
    if action_name == "Call":
        amount_entry.insert(0, "50")  
    elif action_name == "Bet":
        amount_entry.insert(0, "100")  
    elif action_name == "Raise":
        amount_entry.insert(0, "150")
    
    # Buttons
    btn_frame = ttk.Frame(content_frame)
    btn_frame.pack(pady=10)
    
    def execute_action_with_amount():
        """Execute the action with the entered amount"""
        try:
            amount = float(amount_entry.get().strip())
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be positive")
                return
            
            current_player = current_game.players[current_player_index]
            
            # Validate if player has enough balance
            if amount > current_player.balance:
                messagebox.showerror("Error", f"Not enough balance! Available: ${current_player.balance}")
                return
            
            # Execute the action
            bet_placed = current_player.place_bet(amount)
            current_game.pot += bet_placed
            current_game.record_player_action(current_player, action_name.lower(), amount)
            
            # Success message
            if action_name == "Call":
                lbl_help.config(text=f"{current_player.name} called ${amount}")
            elif action_name == "Bet":
                lbl_help.config(text=f"{current_player.name} bet ${amount}")
            elif action_name == "Raise":
                lbl_help.config(text=f"⬆{current_player.name} raised to ${amount}")
            
            # Clear form and advance turn
            clear_content_frame()
            advance_turn()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
    
    confirm_btn = ttk.Button(btn_frame, text=f"Confirm {action_name}", 
                            command=execute_action_with_amount)
    confirm_btn.grid(row=0, column=0, padx=5)
    
    cancel_btn = ttk.Button(btn_frame, text="Cancel", 
                           command=clear_content_frame)
    cancel_btn.grid(row=0, column=1, padx=5)

def advance_turn():
    """Move to next player or next round"""
    global current_player_index, current_game

    if not current_game or not current_game.is_active:
        print("Finished game")
        return
    
    # Find next active player
    original_index = current_player_index
    active_players = [p for p in current_game.players if not p.folded]
    
    if not active_players:
        lbl_help.config(text="All players folded! Game should end.")
        return
    
    #find next active player
    while True:
        current_player_index = (current_player_index + 1) % len(current_game.players)
        if not current_game.players[current_player_index].folded:
            break
        # If we loop back to original player, round should end
        if current_player_index == original_index:
            break
    
    # Check if round should end (all players acted)
    if current_player_index == get_first_active_player_index():
        # All players have acted, advance to next round
        if current_game.next_round():
            lbl_help.config(text=f"Round advanced! Community cards updated.")
            update_actions_display()
        else:
           # Game ended
            winner_names = [w.name for w in current_game.winners]
            lbl_help.config(text=f"Game finished! Winners: {winner_names}")
            # Show winners in listbox
            lb_output.insert(tk.END, "---")
            lb_output.insert(tk.END, "WINNERS:")

            for winner in current_game.winners:
                from gameRule import GameRule
                hand_evaluation = GameRule.evaluate_hand(winner.hand, current_game.community_cards)
                lb_output.insert(tk.END, f"  {winner.name} wins ${current_game.pot:.0f} with {hand_evaluation.name}!")

            current_game = None
            return
    
    # Update display
    update_game_display()
    update_actions_display()

def get_first_active_player_index():
    if not current_game:
        return 0
    for i, player in enumerate(current_game.players):
        if not player.folded:
            return i
    return 0

def show_players():
    """Show all players info"""
    clear_content_frame()
    
    title_label = ttk.Label(content_frame, text="All players", 
                           style="yellow.TLabel", font=("Segoe UI", 12, "bold"))
    title_label.pack(pady=10)
    
    players = load_players_from_db()
    
    if not players:
        no_players_label = ttk.Label(content_frame, 
                                   text="No players", 
                                   style="white.TLabel")
        no_players_label.pack(pady=10)
        return
    
    container = ttk.Frame(content_frame)
    container.pack(fill="both", expand=True)

    canvas = tk.Canvas(container, bg="#1a1a1a", highlightthickness=0)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)

    scroll_frame = ttk.Frame(canvas)

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # show players
    for p in players:
        text = f"{p.name} | Balance: ${p.balance} | Points: {p.points}"
        
        player_label = ttk.Label(
            scroll_frame,
            text=text,
            style="white.TLabel",
            padding=5
        )
        player_label.pack(anchor="w")

def show_game_history():
    """Show game history"""
    global current_game
    
    if not current_game:
        messagebox.showinfo("Info", "No active game to show history")
        return
    
    clear_content_frame()
    
    # Title
    title_label = ttk.Label(content_frame, text="CURRENT GAME HISTORY", 
                           style="yellow.TLabel", font=("Segoe UI", 12, "bold"))
    title_label.pack(pady=10)
    
    # Game info
    info_frame = ttk.Frame(content_frame)
    info_frame.pack(pady=5, fill="x")
    
    ttk.Label(info_frame, text=f"Game ID: {current_game.game_id}", style="white.TLabel").pack()
    ttk.Label(info_frame, text=f"Pot: ${current_game.pot}", style="white.TLabel").pack()
    ttk.Label(info_frame, text=f"Round: {['Pre-flop', 'Flop', 'Turn', 'River', 'Showdown'][current_game.current_round]}", 
              style="white.TLabel").pack()
    
    # Community cards
    ttk.Label(content_frame, text="Community Cards:", style="white.TLabel").pack(anchor="w", pady=(10,0))
    cards_text = " ".join(str(card) for card in current_game.community_cards) if current_game.community_cards else "None yet"
    ttk.Label(content_frame, text=cards_text, style="white.TLabel").pack(anchor="w")
    
    # Player actions history
    ttk.Label(content_frame, text="Player Actions:", style="white.TLabel").pack(anchor="w", pady=(10,0))
    
    # Scroll
    scroll_frame = ttk.Frame(content_frame)
    scroll_frame.pack(fill="both", expand=True, pady=5)
    
    canvas = tk.Canvas(scroll_frame, bg="#333333", highlightthickness=0, height=200)
    scrollbar = ttk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)
    
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Display actions
    for i, action in enumerate(current_game.player_actions):
        round_name = ['Pre-flop', 'Flop', 'Turn', 'River', 'Showdown'][action['round']]
        action_text = f"{action['player'].name} {action['action'].upper()} ${action['amount']} ({round_name})"
        ttk.Label(scrollable_frame, text=action_text, style="white.TLabel").pack(anchor="w", padx=5, pady=2)
    
def modify_player_balance():
    """Modify current player's balance by adding amount"""
    global current_game, current_player_index
    
    clear_content_frame()
    
    # Title
    title_label = ttk.Label(content_frame, text="MODIFY PLAYER BALANCE", 
                           style="yellow.TLabel", font=("Segoe UI", 12, "bold"))
    title_label.pack(pady=10)
    
    if not current_game:
        ttk.Label(content_frame, text="No active game - no current player", 
                 style="white.TLabel").pack(pady=10)
        
        back_btn = ttk.Button(content_frame, text="Back", 
                             command=clear_content_frame)
        back_btn.pack(pady=10)
        return
    
    current_player = current_game.players[current_player_index]
    
    info_frame = ttk.Frame(content_frame)
    info_frame.pack(pady=10)
    
    ttk.Label(info_frame, text=f"Player: {current_player.name}", 
             style="white.TLabel", font=("Segoe UI", 11, "bold")).grid(row=0, column=0, sticky="w", pady=2)
    
    ttk.Label(info_frame, text=f"Current Balance: ${current_player.balance}", 
             style="white.TLabel").grid(row=1, column=0, sticky="w", pady=2)
    
    form_frame = ttk.Frame(content_frame)
    form_frame.pack(pady=20)
    
    amount_label = ttk.Label(form_frame, text="Amount to add ($):", style="white.TLabel")
    amount_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
    
    amount_entry = ttk.Entry(form_frame, width=15, font=("Segoe UI", 10))
    amount_entry.grid(row=0, column=1, padx=5, pady=5)
    amount_entry.focus()
    
    btn_frame = ttk.Frame(content_frame)
    btn_frame.pack(pady=10)
    
    def add_balance():
        """Add amount to player's balance"""
        try:
            amount = float(amount_entry.get().strip())
            
            # Validations
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be positive")
                return
            
            # Calculate new balance
            new_balance = current_player.balance + amount
            
            # update
            current_player.balance = new_balance
            
            # Save in DB
            from db_connection import get_conn
            from queries import UPDATE_PLAYER_BALANCE
            
            conn = get_conn()
            try:
                cur = conn.cursor()
                # Update and keep current points
                cur.execute(UPDATE_PLAYER_BALANCE, (new_balance, current_player.points, current_player.id))
                conn.commit()
                
                # Message
                messagebox.showinfo("Success", 
                                  f"Added ${amount} to {current_player.name}'s balance\n"
                                  f"New balance: ${new_balance}")
                
                # update display
                if current_game and current_game.is_active:
                    update_game_display()
                
                # Clear
                clear_content_frame()
                
            except Exception as e:
                messagebox.showerror("Database Error", f"Could not update balance: {e}")
                conn.rollback()
            finally:
                cur.close()
                conn.close()
                
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
    
    # Butons
    add_btn = ttk.Button(btn_frame, text="Add Amount", 
                        command=add_balance, style="Casino.TButton")
    add_btn.grid(row=0, column=0, padx=5)
    
    cancel_btn = ttk.Button(btn_frame, text="Cancel", 
                           command=clear_content_frame)
    cancel_btn.grid(row=0, column=2, padx=5)
    
def show_player_info():
    """Show information of current player in the game"""
    global current_game, current_player_index
    
    clear_content_frame()
    
    # Title
    title_label = ttk.Label(content_frame, text="CURRENT PLAYER INFORMATION", 
                           style="yellow.TLabel", font=("Segoe UI", 12, "bold"))
    title_label.pack(pady=10)
    
    if not current_game:
        ttk.Label(content_frame, text="No active game - no current player", 
                 style="white.TLabel").pack(pady=10)
        return
    
    current_player = current_game.players[current_player_index]
    
    # Mostrar información básica del jugador actual
    info_frame = ttk.Frame(content_frame)
    info_frame.pack(pady=10)
    
    ttk.Label(info_frame, text=f"Player: {current_player.name}", 
             style="white.TLabel", font=("Segoe UI", 11, "bold")).grid(row=0, column=0, sticky="w", pady=2)
    
    ttk.Label(info_frame, text=f"Balance: ${current_player.balance}", 
             style="white.TLabel").grid(row=1, column=0, sticky="w", pady=2)
    
    ttk.Label(info_frame, text=f"Points: {current_player.points}", 
             style="white.TLabel").grid(row=2, column=0, sticky="w", pady=2)
    
    ttk.Label(info_frame, text=f"Status: {'FOLDED' if current_player.folded else 'ACTIVE'}", 
             style="white.TLabel").grid(row=3, column=0, sticky="w", pady=2)
    
    ttk.Label(info_frame, text=f"Current Bet: ${current_player.current_bet}", 
             style="white.TLabel").grid(row=4, column=0, sticky="w", pady=2)
    
    ttk.Label(info_frame, text=f"Total Bet: ${current_player.total_bet}", 
             style="white.TLabel").grid(row=5, column=0, sticky="w", pady=2)
    
    # Cards
    if not current_player.folded and current_player.hand:
        ttk.Label(info_frame, text="Current Hand:", 
                 style="white.TLabel", font=("Segoe UI", 10, "bold")).grid(row = 6, column=0, sticky="w", pady=2)
        
        cards_text = " ".join(str(card) for card in current_player.hand)
        ttk.Label(info_frame, text=cards_text, 
                 style="white.TLabel", font=("Consolas", 12)).grid(row = 7, column=0, sticky="w", pady=2)
    
    
    from db_connection import get_conn
    from queries import PLAYER_FULL_INFO
    
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(PLAYER_FULL_INFO, (current_player.id,))
        result = cur.fetchone()
        
        if result:
            player_name, balance, points, wins, total_hands = result
            
            ttk.Label(content_frame, text="FULL STATISTICS", 
                     style="yellow.TLabel", font=("Segoe UI", 12, "bold")).pack(pady=10)
            
            stats_frame = ttk.Frame(content_frame)
            stats_frame.pack(pady=10)
            
            ttk.Label(stats_frame, text=f"Balance: ${balance}", 
                     style="white.TLabel").grid(row=0, column=0, sticky="w", pady=2)
            
            ttk.Label(stats_frame, text=f"Points: {points}", 
                     style="white.TLabel").grid(row=1, column=0, sticky="w", pady=2)
            
            ttk.Label(stats_frame, text=f"WINS: {wins}", 
                     style="white.TLabel").grid(row=2, column=0, sticky="w", pady=2)
            
            ttk.Label(stats_frame, text=f"Hands: {total_hands}", 
                     style="white.TLabel").grid(row=3, column=0, sticky="w", pady=2)
            
            # Calcular win rate
            win_rate = (wins / total_hands * 100) if total_hands > 0 else 0
            ttk.Label(stats_frame, text=f"Win rate: {win_rate:.1f}%", 
                     style="white.TLabel").grid(row=4, column=0, sticky="w", pady=2)
            
    except Exception as e:
        ttk.Label(content_frame, text=f"Error loading statistics: {e}", 
                 style="white.TLabel").pack(pady=5)
    finally:
        cur.close()
        conn.close()


def load_player_info_from_db(player_id):
    from db_connection import get_conn
    from queries import SELECT_PLAYER_INFO

    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(SELECT_PLAYER_INFO, (player_id,))
        row = cur.fetchone()

        if row:
            return {
                "id": row[0],
                "name": row[1],
                "wins": row[2]
            }

    except Exception as e:
        print("Error loading player info:", e)
    finally:
        cur.close()
        conn.close()

    return None

def pick_single_player(callback):
    clear_content_frame()

    title_label = ttk.Label(content_frame, text="Select a player",
                           style="yellow.TLabel", font=("Segoe UI", 12, "bold"))
    title_label.pack(pady=10)

    players = load_players_from_db()

    if not players:
        ttk.Label(content_frame, text="No players in database.",
                  style="white.TLabel").pack()
        return

    picker_frame = ttk.Frame(content_frame)
    picker_frame.pack(fill="both", expand=True, padx=10, pady=10)

    picker_frame.grid_columnconfigure(0, weight=1)
    picker_frame.grid_columnconfigure(1, weight=0)
    picker_frame.grid_rowconfigure(0, weight=1)

    scroll_frame = ttk.Frame(picker_frame)
    scroll_frame.grid(row=0, column=0, sticky="nsew")

    canvas = tk.Canvas(scroll_frame, bg="#333333", highlightthickness=0)
    scrollbar = ttk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    player_var = tk.IntVar(value=-1)

    for player in players:
        rb = ttk.Radiobutton(
            scrollable_frame,
            text=f"{player.name} (${player.balance})",
            variable=player_var,
            value=player.id,
            style="White.TRadiobutton"
        )
        rb.pack(anchor="w", padx=10, pady=4)

    btn_frame = ttk.Frame(picker_frame)
    btn_frame.grid(row=0, column=1, sticky="nse")

    def confirm():
        pid = player_var.get()
        if pid == -1:
            messagebox.showwarning("Warning", "Select a player first")
            return
        callback(pid)

    start_btn = ttk.Button(btn_frame, text="Delete",
                           command=confirm, style="Casino.TButton")
    start_btn.pack(pady=5)

    cancel_btn = ttk.Button(btn_frame, text="Cancel",
                            command=clear_content_frame, style="Casino.TButton")
    cancel_btn.pack(pady=5)

def delete_player():
    def _delete(pid):
        from db_connection import get_conn
        from queries import DELETE_PLAY, UPDATE_GAME_WINNER, DELETE_PLAYER, DELETE_HAND, DELETE_PHC
        if not messagebox.askyesno("Confirm",
                                   "Are you sure you want to delete this player and all its data?"):
            return

        if not messagebox.askyesno("Final warning",
                                   "This action cannot be undone. Delete anyway?"):
            return

        try:
            conn = get_conn()
            cur = conn.cursor()
            
            #Delete player hands
            # 1) PlayerHandCards
            cur.execute(DELETE_PHC, (pid,))

            # Delete plays
            cur.execute(DELETE_PLAY , (pid,))

            #Delete hand
            cur.execute(DELETE_HAND, (pid,))

            # Update games, player is null
            cur.execute(UPDATE_GAME_WINNER , (pid,))

            # Delete player
            cur.execute(DELETE_PLAYER , (pid,))

            conn.commit()

            messagebox.showinfo("Success", "Player deleted successfully")
            clear_content_frame()

        except Exception as e:
            messagebox.showerror("Error", f"Could not delete player:\n{e}")

        finally:
            cur.close()
            conn.close()

    pick_single_player(_delete)

    
def create_player():
    """Create a new player"""

    clear_content_frame()

    # Title
    title_label = ttk.Label(content_frame, text="CREATE NEW PLAYER",
                            style="yellow.TLabel", font=("Segoe UI", 12, "bold"))
    title_label.pack(pady=10)

    # Form frame
    form_frame = ttk.Frame(content_frame)
    form_frame.pack(pady=20)

    # Name
    ttk.Label(form_frame, text="Player Name:", style="white.TLabel").grid(
        row=0, column=0, sticky="w", padx=5, pady=5
    )

    name_entry = ttk.Entry(form_frame, width=20, font=("Segoe UI", 10))
    name_entry.grid(row=0, column=1, padx=5, pady=5)
    name_entry.focus()

    # Initial balance
    ttk.Label(form_frame, text="Initial Balance ($):", style="white.TLabel").grid(
        row=1, column=0, sticky="w", padx=5, pady=5
    )

    balance_entry = ttk.Entry(form_frame, width=20, font=("Segoe UI", 10))
    balance_entry.grid(row=1, column=1, padx=5, pady=5)
    balance_entry.insert(0, "100.00")  # default

    # Button frame
    btn_frame = ttk.Frame(content_frame)
    btn_frame.pack(pady=15)

    def submit_new_player():
        name = name_entry.get().strip()
        balance_text = balance_entry.get().strip()

        if not name:
            tk.messagebox.showerror("Error", "Player name is required.")
            return

        try:
            balance = float(balance_text)
        except ValueError:
            tk.messagebox.showerror("Error", "Balance must be a number.")
            return

        # Create player using your class method
        try:
            new_player = Player.set_player(name, balance)
        except Exception as e:
            tk.messagebox.showerror("Database Error", str(e))
            return

        tk.messagebox.showinfo("Success", f"Player '{name}' created successfully!")
        clear_content_frame()

    create_btn = ttk.Button(btn_frame, text="Create Player", command=submit_new_player)
    create_btn.pack(side="left", padx=5)

    back_btn = ttk.Button(btn_frame, text="Back", command=clear_content_frame)
    back_btn.pack(side="left", padx=5)


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
player_menu.add_command(label="Add player", command=create_player)
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
style.configure("White.TCheckbutton", foreground="white", background="#333333",font=("Segoe UI", 9))

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