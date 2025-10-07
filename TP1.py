import matplotlib.pyplot as plt

f=open("coordinates.txt", "r")
lines=[]
for i in f.readlines():
    cline = i.strip()
    lines.append(cline)

pair = 1

#СТРОКИ
for i in range(0, 20, 2):
    line1 = lines[i]
    line2 = lines[i+1]

    line1wobr = line1[1:-1]
    coord1_str, coord2_str = line1wobr.split("),(")
    x1, y1 = map(float, coord1_str.split(","))
    x2, y2 = map(float, coord2_str.split(","))

    line2wobr = line2[1:-1]
    coord3_str, coord4_str = line2wobr.split("),(")
    x3, y3 = map(float, coord3_str.split(","))
    x4, y4 = map(float, coord4_str.split(","))

    #ПЕРЕКРЫТИЕ ОТРЕЗКОВ
    def crossing(a1, a2, b1, b2):
        return max(a1, a2) >= min(b1, b2) and max(b1, b2) >= min(a1, a2)

    #ПРОВЕРКА ПЕРЕСЕЧЕНИЯ
    if x2 != x1:
        k1 = (y2 - y1) / (x2 - x1)
    else:
        k1 = None
    if x4 != x3:
        k2 = (y4 - y3) / (x4 - x3)
    else:
        k2 = None

    if k1 == k2:
        if k1 is None:
            if x1 == x3 and crossing(y1, y2, y3, y4):
                result = "пересекаются"
            else:
                result = "не пересекаются"
        else:
            b1 = y1 - k1 * x1
            b2 = y3 - k2 * x3
            if b1 == b2 and crossing(x1, x2, x3, x4) and crossing(y1, y2, y3, y4):
                result = "пересекаются"
            else:
                result = "не пересекаются"
    else:
        result = "пересекаются"

    #ВИЗУАЛИЗАЦИЯ
    plt.figure(figsize=(6, 6))
    plt.plot([x1, x2], [y1, y2], color = 'hotpink', marker ='*', markersize = 8, label='Прямая 1', linewidth=2)
    plt.plot([x3, x4], [y3, y4], color = 'purple', marker ='*', markersize = 8, label='Прямая 2', linewidth=2)
    plt.grid()
    plt.legend()
    plt.title(f"График {pair}")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()

    #ВЫВОД
    print(f"Пара {pair}: {result}")
    pair += 1
