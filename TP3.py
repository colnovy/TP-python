import tkinter as tk

BASE_ORDER = ["2", "8", "10", "16"]
BASES = {"2": 2, "8": 8, "10": 10, "16": 16}

def to_base(n, base):
    if n == 0:
        return "0"
    digits = "0123456789ABCDEF"
    res = ""
    neg = n < 0
    n = abs(n)
    while n:
        res = digits[n % base] + res
        n //= base
    return ("-" if neg else "") + res

def from_base(s, base):
    try:
        return int(s, base)
    except ValueError:
        raise ValueError("Некорректное число")

def cycle_base(entry, base_var, button):
    s = entry.get().strip().upper()
    if s == "ОШИБКА >:(":
        entry.delete(0, tk.END)
        s = ""

    current = base_var.get()
    idx = BASE_ORDER.index(current)
    next_base_str = BASE_ORDER[(idx + 1) % len(BASE_ORDER)]

    if s:
        try:
            current_base = BASES[current]
            num = from_base(s, current_base)
            next_base = BASES[next_base_str]
            new_str = to_base(num, next_base)
            entry.delete(0, tk.END)
            entry.insert(0, new_str)
        except Exception:
            entry.delete(0, tk.END)
            entry.insert(0, "ОШИБКА >:(")
            return

    base_var.set(next_base_str)
    button.config(text=next_base_str)

def calculate():
    a_str = entry_a.get().strip().upper()
    b_str = entry_b.get().strip().upper()
    op = entry_op.get().strip()
    base_a = BASES[base_a_var.get()]
    base_b = BASES[base_b_var.get()]

    if not a_str or not b_str or not op or a_str == "ОШИБКА >:(" or b_str == "ОШИБКА >:(":
        result_entry.delete(0, tk.END)
        result_entry.insert(0, "ОШИБКА >:(")
        return

    try:
        a = from_base(a_str, base_a)
        b = from_base(b_str, base_b)

        if op == '+':
            res = a + b
        elif op == '-':
            res = a - b
        elif op == '*':
            res = a * b
        elif op == '/':
            if b == 0:
                raise ZeroDivisionError
            res = a // b
        elif op == '%':
            if b == 0:
                raise ZeroDivisionError
            res = a % b
        elif op == '&':
            res = a & b
        elif op == '|':
            res = a | b
        elif op == '^':
            if b < 0:
                raise ValueError("ОШИБКА >:(")
            res = a ** b
        else:
            raise ValueError("Неизвестная операция")

        result_base = BASES[result_base_var.get()]
        res_str = to_base(res, result_base)
        result_entry.delete(0, tk.END)
        result_entry.insert(0, res_str)

    except Exception:
        result_entry.delete(0, tk.END)
        result_entry.insert(0, "ОШИБКА >:(")


root = tk.Tk()
root.title("КАЛЬКУЛЯТОР (СС)")
root.configure(bg="#F73E5F")


frame_a = tk.Frame(root)
frame_a.pack(pady=5)
tk.Label(frame_a, text="A:", fg="#9B001C").pack(side=tk.LEFT)
entry_a = tk.Entry(frame_a, width=20)
entry_a.pack(side=tk.LEFT, padx=5)
base_a_var = tk.StringVar(value="10")
btn_a = tk.Button(frame_a, text="10", width=4, bg="#9B001C", fg = "white", command=lambda: cycle_base(entry_a, base_a_var, btn_a))
btn_a.pack(side=tk.LEFT)


tk.Label(root, text="Операция (+, -, *, /, %, &, |, ^):", bg="#F73E5F", fg = "white").pack()
entry_op = tk.Entry(root, width=12, justify='center')
entry_op.pack(pady=5)


frame_b = tk.Frame(root)
frame_b.pack(pady=5)
tk.Label(frame_b, text="B:", fg="#9B001C").pack(side=tk.LEFT)
entry_b = tk.Entry(frame_b, width=20)
entry_b.pack(side=tk.LEFT, padx=5)
base_b_var = tk.StringVar(value="10")
btn_b = tk.Button(frame_b, text="10", width=4, bg="#9B001C", fg = "white", command=lambda: cycle_base(entry_b, base_b_var, btn_b))
btn_b.pack(side=tk.LEFT)


tk.Label(root, text="=", bg="#F73E5F", fg = "white").pack(pady=5)


frame_res = tk.Frame(root)
frame_res.pack(pady=5)
tk.Label(frame_res, text="C:", fg="#9B001C").pack(side=tk.LEFT)
result_entry = tk.Entry(frame_res, width=20)
result_entry.pack(side=tk.LEFT, padx=5)
result_base_var = tk.StringVar(value="10")
btn_res = tk.Button(frame_res, text="10", width=4, bg="#9B001C", fg = "white", command=lambda: cycle_base(result_entry, result_base_var, btn_res))
btn_res.pack(side=tk.LEFT)

tk.Button(root, text="Вычислить", bg="#9B001C", fg = "white", command=calculate).pack(pady=10)

root.mainloop()