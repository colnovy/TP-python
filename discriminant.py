import tkinter as tk
from tkinter import *
from tkinter import messagebox  #

window = Tk()  # создаем окно приложения
window.title("Расчет дискриминанта")


def show_result(discriminant, roots=None):
    if discriminant >= 0:
        msg = f"Значения:\nДискриминант: {round(discriminant, 2)}\nКорни: "
        if len(roots) == 1:
            msg += str(round(roots[0], 2))
        else:
            for root in roots:
                msg += f'{round(root, 2)} '
        messagebox.showinfo("Решения уравнения", msg.strip())
    else:
        # Отображаем комплексные корни
        msg = f"Значения:\nДискриминант: {round(discriminant, 2)}\nКорни: "
        formatted_roots = []
        for root in roots:
            real = round(root.real, 2)
            imag = round(root.imag, 2)
            if imag >= 0:
                formatted_roots.append(f"{real}+{imag}i")
            else:
                formatted_roots.append(f"{real}{imag}i")  # минус уже в imag
        msg += ", ".join(formatted_roots)
        messagebox.showinfo("Комплексные решения", msg)


def calculate_D(a, b, c):
    try:
        a = float(a)
        b = float(b)
        c = float(c)
        discriminant = float(b ** 2 - 4 * a * c)

        if discriminant > 0:
            x1 = (-b + discriminant ** 0.5) / (2 * a)
            x2 = (-b - discriminant ** 0.5) / (2 * a)
            show_result(discriminant, [x1, x2])

        elif discriminant == 0:
            x = -b / (2 * a)
            show_result(discriminant, [x])

        else:
            # Добавляем поддержку комплексных корней, не меняя остальной код
            import cmath
            sqrt_d = cmath.sqrt(discriminant)
            x1 = (-b + sqrt_d) / (2 * a)
            x2 = (-b - sqrt_d) / (2 * a)
            # Передаём комплексные корни в show_result
            show_result(discriminant, [x1, x2])

    except ZeroDivisionError:
        messagebox.showerror("Ошибка", "Коэффициент a равен нулю, уравнение не является квадратным.")

    except ValueError:
        messagebox.showerror("Ошибка", "Некорректные введенные данные")


frame = Frame(
    window,
    padx=10,
    pady=10
)
frame.pack(expand=True)

metod_label = Label(
    frame,
    text="Введите коэфиценты уравнения ax^2 + bx +c = 0:"
)
metod_label.grid(row=1, column=1)

# кнопка a и записываем значение
a_label = Label(
    frame,
    text="а"
)
a_label.grid(row=2, column=1)

a_ent = Entry(frame)
a_ent.grid(row=2, column=2)
a_ent.focus()

# кнопка b и записываем значение
b_label = Label(
    frame,
    text="b"
)
b_label.grid(row=3, column=1)

b_ent = Entry(frame)
b_ent.grid(row=3, column=2)

# кнопка c и записываем значение
c_label = Label(
    frame,
    text="c"
)
c_label.grid(row=4, column=1)

c_ent = Entry(frame)
c_ent.grid(row=4, column=2)

calc_D = Button(
    frame,
    text="Рассчитать дискриминант",
    command=lambda: calculate_D(a_ent.get(), b_ent.get(), c_ent.get())
)
calc_D.grid(row=5, column=2)

window.mainloop()