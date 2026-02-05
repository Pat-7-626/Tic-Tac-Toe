import tkinter as tk
from tkinter import messagebox
from game_logic import TicTacToeGame
from ai_opponent import AIPlayer
import threading
import time
import math
import ctypes
import random

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass 

class TicTacToeUI(tk.Tk):
    # Modern Color Palette
    COLOR_BG = "#1e1e2e"
    COLOR_FG = "#cdd6f4"
    COLOR_ACCENT = "#f38ba8" # X Color
    COLOR_ACCENT_2 = "#89b4fa" # O Color
    COLOR_WIN = "#f9e2af" 
    COLOR_LINE = "#45475a"
    COLOR_BTN = "#313244"
    COLOR_BTN_HOVER = "#45475a"

    def __init__(self):
        super().__init__()
        self.title("Tic-Tac-Toe Pro")
        self.geometry("600x800")
        self.configure(bg=self.COLOR_BG)
        self.minsize(400, 550)
        self.resizable(True, True)

        self.game = TicTacToeGame()
        self.ai = AIPlayer(difficulty="Hard")
        self.game_mode = "PvP"
        self.ai_symbol = "O"
        self.scores = {"X": 0, "O": 0, "Draws": 0}
        self.sound_enabled = True
        
        # Audio
        try:
            import winsound
            self.play_sound_func = lambda freq, dur: winsound.Beep(freq, dur)
        except ImportError:
            self.play_sound_func = lambda f, d: None

        self.current_frame = None
        self.show_main_menu()

    def play_sound(self, freq, dur):
        if self.sound_enabled:
            threading.Thread(target=self.play_sound_func, args=(freq, dur), daemon=True).start()

    def clear_screen(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = tk.Frame(self, bg=self.COLOR_BG)
        self.current_frame.pack(fill="both", expand=True)

    def create_button(self, parent, text, command, fg=None, bg=None):
        if fg is None: fg = self.COLOR_FG
        if bg is None: bg = self.COLOR_BTN
        
        btn = tk.Button(parent, text=text, command=command,
                        font=("Helvetica", 16, "bold"),
                        fg=fg, bg=bg,
                        activeforeground=fg, activebackground=self.COLOR_BTN_HOVER,
                        relief=tk.FLAT, borderwidth=0, cursor="hand2")
        btn.bind("<Enter>", lambda e: btn.config(bg=self.COLOR_BTN_HOVER))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))
        return btn

    # ==========================
    # MAIN MENU & SELECTION
    # ==========================
    def show_main_menu(self):
        self.clear_screen()
        
        container = tk.Frame(self.current_frame, bg=self.COLOR_BG)
        container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8)

        tk.Label(container, text="TIC TAC TOE", font=("Helvetica", 42, "bold"),
                 bg=self.COLOR_BG, fg=self.COLOR_ACCENT).pack(pady=(0, 10))
        tk.Label(container, text="MASTER EDITION", font=("Helvetica", 14, "italic"),
                 bg=self.COLOR_BG, fg="#a6adc8").pack(pady=(0, 50))

        self.create_button(container, "PLAYER vs PLAYER", 
                           lambda: self.start_game("PvP")).pack(fill="x", pady=10, ipady=5)
        self.create_button(container, "PLAYER vs AI", 
                           self.show_pvai_menu).pack(fill="x", pady=10, ipady=5)
        
        sound_text = "SOUND: ON" if self.sound_enabled else "SOUND: OFF"
        self.btn_sound = self.create_button(container, sound_text, self.toggle_sound)
        self.btn_sound.config(font=("Helvetica", 10))
        self.btn_sound.pack(pady=20)
        
        self.create_button(container, "EXIT", self.quit, bg="#f38ba8", fg="#1e1e2e").pack(fill="x", pady=10, ipady=5)

    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        self.btn_sound.config(text="SOUND: ON" if self.sound_enabled else "SOUND: OFF")

    def show_pvai_menu(self):
        self.clear_screen()
        container = tk.Frame(self.current_frame, bg=self.COLOR_BG)
        container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8)
        
        tk.Label(container, text="DIFFICULTY", font=("Helvetica", 32, "bold"),
                 bg=self.COLOR_BG, fg=self.COLOR_FG).pack(pady=(0, 30))

        for diff in ["Easy", "Medium", "Hard"]:
            self.create_button(container, diff.upper(), 
                               lambda d=diff: self.select_ai_difficulty(d)).pack(fill="x", pady=8, ipady=5)
            
        self.create_button(container, "BACK", self.show_main_menu).pack(fill="x", pady=20, ipady=5)

    def select_ai_difficulty(self, difficulty):
        self.ai = AIPlayer(difficulty=difficulty)
        self.show_turn_menu()

    def show_turn_menu(self):
        self.clear_screen()
        container = tk.Frame(self.current_frame, bg=self.COLOR_BG)
        container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8)

        tk.Label(container, text="WHO STARTS?", font=("Helvetica", 32, "bold"),
                 bg=self.COLOR_BG, fg=self.COLOR_FG).pack(pady=(0, 30))

        self.create_button(container, "I GO FIRST (X)", 
                           lambda: self.start_game("PvAI", ai_starts=False)).pack(fill="x", pady=10, ipady=5)
        self.create_button(container, "AI GOES FIRST (O)", 
                           lambda: self.start_game("PvAI", ai_starts=True)).pack(fill="x", pady=10, ipady=5)
        self.create_button(container, "BACK", self.show_pvai_menu).pack(fill="x", pady=20, ipady=5)

    # ==========================
    # GAMEPLAY (CANVAS)
    # ==========================
    def start_game(self, mode, ai_starts=False):
        self.game_mode = mode
        self.game.reset_game()
        if mode == "PvAI":
            self.ai_symbol = "X" if ai_starts else "O"

        self.show_game_board()
        
        if mode == "PvAI" and ai_starts:
            self.current_frame.after(600, self.ai_move)

    def show_game_board(self):
        self.clear_screen()
        
        # Grid layout for Game Interface
        # Row 0: Header (Back + Turn)
        # Row 1: Score
        # Row 2: Canvas (Board)
        self.current_frame.rowconfigure(2, weight=1)
        self.current_frame.columnconfigure(0, weight=1)

        # Header
        header = tk.Frame(self.current_frame, bg=self.COLOR_BG)
        header.grid(row=0, sticky="ew", padx=20, pady=10)
        
        tk.Button(header, text="< Menu", command=self.show_main_menu,
                  font=("Helvetica", 12), bg=self.COLOR_BG, fg="#a6adc8",
                  relief=tk.FLAT, activebackground=self.COLOR_BG).pack(side="left")
        
        self.turn_label = tk.Label(header, text=f"Turn: {self.game.current_player}", 
                                   font=("Helvetica", 16, "bold"), bg=self.COLOR_BG, fg=self.COLOR_FG)
        self.turn_label.pack(side="right")

        # Score
        self.score_label = tk.Label(self.current_frame, text=self.get_score_text(),
                                    font=("Helvetica", 14, "bold"), bg=self.COLOR_BG, fg=self.COLOR_FG)
        self.score_label.grid(row=1, pady=(0, 10))

        # Viewport (Canvas)
        self.canvas = tk.Canvas(self.current_frame, bg=self.COLOR_BG, highlightthickness=0)
        self.canvas.grid(row=2, sticky="nsew", padx=20, pady=20)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Configure>", self.on_canvas_resize)

        self.board_size = 0
        self.cell_size = 0
        self.offset_x = 0
        self.offset_y = 0
        self.drawn_moves = [False] * 9 # Track what's been animated

    def get_score_text(self):
        p1 = "Player X"
        p2 = "Player O"
        if self.game_mode == "PvAI":
            if self.ai_symbol == "O": p2 = f"AI ({self.ai.difficulty})"
            else: p1 = f"AI ({self.ai.difficulty})"
        return f"{p1}: {self.scores['X']}   |   Draws: {self.scores['Draws']}   |   {p2}: {self.scores['O']}"

    def on_canvas_resize(self, event):
        w, h = event.width, event.height
        size = min(w, h)
        self.board_size = size - 20 # Padding
        self.cell_size = self.board_size / 3
        
        # Center the board
        self.offset_x = (w - self.board_size) / 2
        self.offset_y = (h - self.board_size) / 2
        
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        
        # Draw Grid Lines
        line_width = max(2, self.board_size / 60)
        cap = tk.ROUND
        col = self.COLOR_LINE
        
        # Verticals
        for i in range(1, 3):
            x = self.offset_x + i * self.cell_size
            self.canvas.create_line(x, self.offset_y, x, self.offset_y + self.board_size, 
                                    width=line_width, fill=col, capstyle=cap)
        # Horizontals
        for i in range(1, 3):
            y = self.offset_y + i * self.cell_size
            self.canvas.create_line(self.offset_x, y, self.offset_x + self.board_size, y, 
                                    width=line_width, fill=col, capstyle=cap)
                                    
        # Draw existing moves (for resize consistency)
        for i in range(9):
            if self.game.board[i] != " ":
                self.draw_symbol(i, self.game.board[i], animate=False)

    def draw_symbol(self, index, player, animate=True):
        row = index // 3
        col_idx = index % 3
        
        x0 = self.offset_x + col_idx * self.cell_size
        y0 = self.offset_y + row * self.cell_size
        
        pad = self.cell_size * 0.2
        width = max(3, self.cell_size / 15)
        
        if player == "X":
            color = self.COLOR_ACCENT
            coords = [ # Line 1 and Line 2
                (x0 + pad, y0 + pad, x0 + self.cell_size - pad, y0 + self.cell_size - pad),
                (x0 + self.cell_size - pad, y0 + pad, x0 + pad, y0 + self.cell_size - pad)
            ]
            if animate:
                self.animate_line(coords[0], color, width, 0)
                self.animate_line(coords[1], color, width, 100) # Delay 2nd line
            else:
                self.canvas.create_line(*coords[0], width=width, fill=color, capstyle=tk.ROUND, tags="symbol")
                self.canvas.create_line(*coords[1], width=width, fill=color, capstyle=tk.ROUND, tags="symbol")
                
        elif player == "O":
            color = self.COLOR_ACCENT_2
            bbox = (x0 + pad, y0 + pad, x0 + self.cell_size - pad, y0 + self.cell_size - pad)
            if animate:
                self.animate_circle(bbox, color, width)
            else:
                self.canvas.create_oval(*bbox, outline=color, width=width, tags="symbol")

    def animate_line(self, coords, color, width, delay=0):
        x1, y1, x2, y2 = coords
        
        def step(progress):
            if progress > 1: progress = 1
            cur_x = x1 + (x2 - x1) * progress
            cur_y = y1 + (y2 - y1) * progress
            self.canvas.create_line(x1, y1, cur_x, cur_y, width=width, fill=color, capstyle=tk.ROUND, tags="symbol_anim")
            if progress < 1:
                self.after(10, step, progress + 0.1)
                
        self.after(delay, step, 0)

    def animate_circle(self, bbox, color, width):
        x1, y1, x2, y2 = bbox
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        rx = (x2 - x1) / 2
        ry = (y2 - y1) / 2
        
        def step(angle):
            if angle > 360: angle = 360
            # Draw arc
            self.canvas.create_arc(bbox, start=90, extent=-angle, style=tk.ARC, outline=color, width=width, tags="symbol_anim")
            if angle < 360:
                self.after(10, step, angle + 25) # Speed
                
        step(0)

    def on_canvas_click(self, event):
        if self.game.game_over: return
        
        # Hit detection
        if not (self.offset_x <= event.x <= self.offset_x + self.board_size and
                self.offset_y <= event.y <= self.offset_y + self.board_size):
            return
            
        col = int((event.x - self.offset_x) // self.cell_size)
        row = int((event.y - self.offset_y) // self.cell_size)
        index = row * 3 + col
        
        if 0 <= index < 9:
            self.handle_move(index)

    def handle_move(self, index):
        if self.game.board[index] != " ": return
        
        result = self.game.make_move(index)
        if result:
            self.play_sound(1000, 50)
            self.draw_symbol(index, self.game.board[index], animate=True)
            self.turn_label.config(text=f"Turn: {self.game.current_player}")
            
            check_over = False
            if isinstance(result, tuple): # Win
                self.after(300, lambda: self.highlight_win(result))
                check_over = True
            elif self.game.game_over: # Draw
                check_over = True
                
            if check_over:
                self.after(1000, self.show_game_over)
            elif self.game_mode == "PvAI" and self.game.current_player == self.ai_symbol:
                 self.after(600, self.ai_move)

    def ai_move(self):
        move = self.ai.get_move(self.game)
        if move is not None:
             self.handle_move(move)

    def highlight_win(self, indices):
        # Draw a line through the winning cells
        start_idx = indices[0]
        end_idx = indices[2]
        
        # Calculate centers
        r1, c1 = start_idx // 3, start_idx % 3
        r2, c2 = end_idx // 3, end_idx % 3
        
        x1 = self.offset_x + c1 * self.cell_size + self.cell_size/2
        y1 = self.offset_y + r1 * self.cell_size + self.cell_size/2
        x2 = self.offset_x + c2 * self.cell_size + self.cell_size/2
        y2 = self.offset_y + r2 * self.cell_size + self.cell_size/2
        
        # Animate winning line
        self.play_sound(600, 200)
        self.animate_line((x1, y1, x2, y2), self.COLOR_WIN, 10, 0)
        
        # Particle explosion effect simply by drawing random dots
        for _ in range(20):
            cx = (x1 + x2) / 2 + random.randint(-50, 50)
            cy = (y1 + y2) / 2 + random.randint(-50, 50)
            sz = random.randint(2, 6)
            self.canvas.create_oval(cx, cy, cx+sz, cy+sz, fill=self.COLOR_WIN, outline="")

    def show_game_over(self):
        if self.game.winner:
            self.scores[self.game.winner] += 1
            txt = f"{self.game.winner} WINS!"
            col = self.COLOR_ACCENT if self.game.winner == "X" else self.COLOR_ACCENT_2
        else:
            self.scores["Draws"] += 1
            txt = "DRAW!"
            col = self.COLOR_FG
            
        self.score_label.config(text=self.get_score_text())
        
        # Blur/Overlay
        overlay = tk.Frame(self.current_frame, bg="#11111b")
        overlay.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.6, relheight=0.3)
        
        tk.Label(overlay, text=txt, font=("Helvetica", 28, "bold"), 
                 bg="#11111b", fg=col).pack(pady=(20, 10))
                 
        tk.Button(overlay, text="PLAY AGAIN", command=self.restart_game,
                  font=("Helvetica", 12, "bold"), bg=self.COLOR_BG, fg=self.COLOR_FG,
                  relief=tk.FLAT).pack(side="left", padx=20, expand=True)

        tk.Button(overlay, text="MENU", command=self.show_main_menu,
                  font=("Helvetica", 12, "bold"), bg=self.COLOR_BG, fg=self.COLOR_FG,
                  relief=tk.FLAT).pack(side="right", padx=20, expand=True)

    def restart_game(self):
        ai_starts = (self.game_mode == "PvAI" and self.ai_symbol == "X")
        self.start_game(self.game_mode, ai_starts=ai_starts)

if __name__ == "__main__":
    app = TicTacToeUI()
    app.mainloop()
