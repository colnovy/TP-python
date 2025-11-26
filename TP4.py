import tkinter as tk
from tkinter import messagebox
import random

history = {"Player": 0, "Bot": 0, "Draw": 0}

class TicTacToeVsBot:
    def __init__(self, root):
        self.root = root
        self.root.title("Крестики-нолики")
        self.root.configure(bg='darkslategray')
        self.setup_settings()

    def setup_settings(self):
        for widget in self.root.winfo_children():
            widget.destroy()


        tk.Label(self.root, text="Размер поля (3–15):", bg='darkslategray', fg = 'beige').pack()
        self.size_var = tk.IntVar(value=3)
        tk.Spinbox(self.root, from_=3, to=15, textvariable=self.size_var, width=5).pack()

        tk.Label(self.root, text="Длина победы (2–5):", bg='darkslategray', fg = 'beige').pack()
        self.win_var = tk.IntVar(value=3)
        tk.Spinbox(self.root, from_=2, to=5, textvariable=self.win_var, width=5).pack()

        tk.Button(self.root, text="Начать игру", bg='beige', fg = 'darkslategray', command=self.start_game).pack(pady=15)

        self.history_label = tk.Label(self.root)
        self.history_label.pack()
        self.update_history_display()

    def update_history_display(self):
        text = f"История игр:\nИгрок (X): {history['Player']}\nБот (O): {history['Bot']}\nНичьи: {history['Draw']}"
        self.history_label.config(text=text, bg='darkslategray', fg = 'beige')

    def start_game(self):
        size = self.size_var.get()
        win_len = self.win_var.get()
        if win_len > size:
            messagebox.showerror("Ошибка", "Длина победы не может быть больше размера поля!")
            return

        for widget in self.root.winfo_children():
            widget.destroy()

        self.size = size
        self.win_len = win_len
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.game_over = False

        self.buttons = []
        game_frame = tk.Frame(self.root, bg='darkslategray')
        game_frame.pack(pady=10)

        for i in range(size):
            row = []
            for j in range(size):
                btn = tk.Button(
                    game_frame,
                    text="",
                    width=4,
                    height=2,
                    bg='lightgray',
                    fg='black',
                    command=lambda r=i, c=j: self.player_move(r, c)
                )
                btn.grid(row=i, column=j, padx=1, pady=1)
                row.append(btn)
            self.buttons.append(row)

        control_frame = tk.Frame(self.root, bg='darkslategray')
        control_frame.pack(pady=10)
        tk.Button(control_frame, text="Новая игра", command=self.setup_settings,  bg='beige', fg='darkslategray').pack()

        self.status_label = tk.Label(self.root)
        self.status_label.pack()

        self.update_history_display()

    def player_move(self, row, col):
        if self.game_over or self.board[row][col] != 0:
            return

        self.board[row][col] = 1
        self.buttons[row][col].config(text="X", state="disabled")

        if self.check_winner(1):
            history["Player"] += 1
            self.end_game("Вы победили!")
        elif self.is_board_full():
            history["Draw"] += 1
            self.end_game("Ничья!")
        else:
            self.status_label.config(text="Ход бота", bg='darkslategray', fg = 'beige')
            self.root.update()
            self.root.after(400, self.bot_move)

    def bot_move(self):
        if self.game_over:
            return

        move = self.find_best_move()
        if move:
            row, col = move
            self.board[row][col] = -1  # O = -1
            self.buttons[row][col].config(text="O", state="disabled")

            if self.check_winner(-1):
                history["Bot"] += 1
                self.end_game("Бот победил!")
            elif self.is_board_full():
                history["Draw"] += 1
                self.end_game("Ничья!")
            else:
                self.status_label.config(text="Ваш ход (X)", bg='darkslategray', fg = 'beige')

    def find_best_move(self):
        empty_cells = [(i, j) for i in range(self.size) for j in range(self.size) if self.board[i][j] == 0]
        if not empty_cells:
            return None

        for (i, j) in empty_cells:
            self.board[i][j] = -1
            if self.check_winner(-1):
                self.board[i][j] = 0
                return (i, j)
            self.board[i][j] = 0

        for (i, j) in empty_cells:
            self.board[i][j] = 1
            if self.check_winner(1):
                self.board[i][j] = 0
                return (i, j)
            self.board[i][j] = 0

        return random.choice(empty_cells)

    def is_board_full(self):
        return all(self.board[i][j] != 0 for i in range(self.size) for j in range(self.size))

    def check_line(self, start_row, start_col, dr, dc, player):

        for k in range(self.win_len):
            r = start_row + k * dr
            c = start_col + k * dc
            if r < 0 or r >= self.size or c < 0 or c >= self.size:
                return False
            if self.board[r][c] != player:
                return False
        return True

    def check_winner(self, player):

        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == player:
                    for dr, dc in [(0,1), (1,0), (1,1), (1,-1)]:
                        for offset in range(self.win_len):
                            start_r = i - offset * dr
                            start_c = j - offset * dc
                            if self.check_line(start_r, start_c, dr, dc, player):
                                return True
        return False

    def end_game(self, message):
        self.game_over = True
        self.status_label.config(text=message)
        messagebox.showinfo("Результат", message)
        self.update_history_display()



root = tk.Tk()
app = TicTacToeVsBot(root)
root.mainloop()