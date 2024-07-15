import tkinter as tk
from winsound import *
import structure


class TicTacToeUI(tk.Tk):
    background = "#ffffc7"
    light = "#fcaa67"
    pitch = "#473335"
    x_color = "#b0413e"
    o_color = "#548687"
    font = "Terminal"
    font_fam = "monospace"
    row = [["N", "N", "N"], ["N", "N", "N"], ["N", "N", "N"]]
    col = [["N", "N", "N"], ["N", "N", "N"], ["N", "N", "N"]]
    player = "X"
    time = 0
    stat = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = None
        self.exit = None
        self.again_button = None
        self.text = None
        self.but_list = None
        self.title("Tic Tac Toe")
        self.configure(bg=self.pitch,
                       cursor="hand2")
        self.focus_force()
        self.protocol("WM_DELETE_WINDOW", self.exit_game)
        self.columnconfigure(0,
                             weight=1)
        self.rowconfigure(0,
                          weight=1)
        self.pages = {}
        self.init_pages()
        self.show_page("title_screen")
        self.attributes("-fullscreen", True)

    def init_pages(self):
        self.pages["title_screen"] = tk.Frame(self,
                                              bg=self.pitch)
        self.pages["main_game"] = tk.Frame(self,
                                           bg=self.x_color)
        self.pages["finish"] = tk.Frame(self,
                                        bg=self.pitch)
        self.init_main_game()
        self.init_finish()
        self.init_title_screen()

    def init_title_screen(self):
        title = tk.Frame(self.pages["title_screen"],
                         bg=self.pitch)
        title.grid(column=0,
                   row=0,
                   padx=50,
                   pady=50)
        text = tk.Label(title,
                        text="Tic-Tac-Toe",
                        font=(self.font, 25),
                        fg=self.light,
                        bg=self.pitch)
        play_button = tk.Button(title,
                                text="PLAY",
                                font=(self.font, 15),
                                command=lambda: self.reset(),
                                fg=self.light,
                                bg=self.pitch,
                                activeforeground=self.pitch,
                                activebackground=self.light)
        text.grid(row=0,
                  column=0,
                  sticky=tk.NSEW,
                  ipadx=25,
                  ipady=25)
        play_button.grid(row=1,
                         column=0,
                         sticky=tk.NSEW,
                         ipadx=5,
                         ipady=5,
                         padx=5,
                         pady=5)

    def init_main_game(self):
        self.game = tk.Frame(self.pages["main_game"],
                             bg=self.x_color)
        self.game.grid(column=0,
                       row=0,
                       padx=50,
                       pady=50)
        self.but_list = {}
        for r in range(3):
            for c in range(3):
                but = tk.Button(self.game,
                                text=" ",
                                font=(self.font, 20),
                                bg=self.pitch,
                                activebackground=self.light,
                                state=tk.NORMAL,
                                command=lambda row=r, col=c:
                                self.play_click(row, col))
                but.grid(row=r,
                         column=c,
                         ipadx=10,
                         ipady=10,
                         padx=5,
                         pady=5)
                self.but_list[f"{r}{c}"] = but

    def init_finish(self):
        result = tk.Frame(self.pages["finish"],
                          bg=self.pitch)
        result.grid(column=0,
                    row=0,
                    padx=50,
                    pady=50)
        self.text = tk.Label(result,
                             text="",
                             font=(self.font, 25))
        self.again_button = tk.Button(result,
                                      text="PLAY AGAIN",
                                      font=(self.font, 15),
                                      command=lambda: self.reset())
        self.exit = tk.Button(result,
                              text="EXIT",
                              font=(self.font, 15),
                              command=lambda: self.exit_game())
        self.text.grid(row=0,
                       column=0,
                       sticky=tk.NSEW,
                       ipadx=25,
                       ipady=25)
        self.again_button.grid(row=1,
                               column=0,
                               sticky=tk.NSEW,
                               ipadx=5,
                               ipady=5,
                               padx=5,
                               pady=5)
        self.exit.grid(row=2,
                       column=0,
                       sticky=tk.NSEW,
                       ipadx=5,
                       ipady=5,
                       padx=5,
                       pady=5)

    def play_click(self, r, c):
        Beep(750, 150)
        self.time += 1
        self.but_list[f"{r}{c}"].config(text=self.player,
                                        state=tk.DISABLED,
                                        bg=self.x_color if self.player == "X"
                                        else self.o_color,
                                        fg=self.pitch)
        self.pages["main_game"].config(
            bg=self.x_color if self.player == "O" else self.o_color)
        self.game.config(
            bg=self.x_color if self.player == "O" else self.o_color)
        self.row, self.col = structure.trans(self.row, self.col,
                                             r, c, self.player)
        stat = structure.check_winner(self.row, self.col)
        if stat is True:
            self.stat = True
            self.show_page("finish")
        elif self.time == 9:
            self.show_page("finish")
        else:
            self.player = structure.change(self.player)

    def reset(self):
        Beep(750, 150)
        self.row = [["N", "N", "N"], ["N", "N", "N"], ["N", "N", "N"]]
        self.col = [["N", "N", "N"], ["N", "N", "N"], ["N", "N", "N"]]
        self.player = "X"
        self.time = 0
        self.stat = False
        self.init_pages()
        self.show_page("main_game")

    def show_page(self, name):
        for i, j in self.pages.items():
            j.grid_forget()
        self.pages[name].grid(row=0,
                              column=0,
                              sticky=tk.NSEW)
        self.pages[name].columnconfigure(0,
                                         weight=1)
        self.pages[name].rowconfigure(0,
                                      weight=1)
        if self.stat:
            word = f"{self.player} WINS"
        else:
            word = "TIE"
        self.text.config(text=word,
                         fg=self.light if self.stat is False
                         else self.x_color if self.player == "X"
                         else self.o_color,
                         bg=self.pitch)
        self.again_button.config(fg=self.pitch,
                                 bg=self.light if self.stat is False
                                 else self.x_color if self.player == "X"
                                 else self.o_color,
                                 activeforeground=self.light
                                 if self.stat is False
                                 else self.x_color if self.player == "X"
                                 else self.o_color,
                                 activebackground=self.pitch)
        self.exit.config(fg=self.pitch,
                         bg=self.light if self.stat is False
                         else self.x_color if self.player == "X"
                         else self.o_color,
                         activeforeground=self.light
                         if self.stat is False
                         else self.x_color if self.player == "X"
                         else self.o_color,
                         activebackground=self.pitch)

    def exit_game(self):
        Beep(750, 150)
        self.destroy()
        self.quit()
