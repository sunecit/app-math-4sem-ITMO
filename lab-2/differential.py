import matplotlib.pyplot as plt
import numpy as np

right_avg_square_diff_results = []
left_avg_square_diff_results = []
center_avg_square_diff_results = []


def f1(x):
    return np.log(x)


def f2(x):
    return np.sin(x)


def diff1(x):
    return 1 / x


def diff2(x):
    return np.cos(x)


def compute(a, b, h, func, diff, name):
    x_array = []

    # узлы отрезка [a, b] с шагом h
    for i in np.arange(a, b, h):
        x_array.append(i)
    x_array.append(b)

    f_array = []  # значения функции в узлах
    diff_array = []  # аналитически вычисленные значения производной в узлах
    right_diff_array = []  # вычисленное значение правой разностной производной для n узлов
    left_diff_array = []  # вычисленное значение левой разностной производной для n узлов
    center_diff_array = []  # вычисленное значение центральной разностной производной для (n + 1) узлов

    for i in x_array:
        f_array.append(func(i))
        diff_array.append(diff(i))

    i = 0
    n = len(x_array)
    print(n)
    while i < n - 1:
        # вычисление правой разностной производной
        right_diff_array.append((f_array[i + 1] - f_array[i]) / h)
        i = i + 1

    result = avg_square_diff(diff_array[0: n - 1], right_diff_array, n, h, name, "Правая разностная производная")
    right_avg_square_diff_results.append(result)

    i = 1
    while i <= n - 1:
        # вычисление левой разностной производной
        left_diff_array.append((f_array[i] - f_array[i - 1]) / h)
        i = i + 1

    result = avg_square_diff(diff_array[1: n], left_diff_array, n, h, name, "Левая разностная производная")
    left_avg_square_diff_results.append(result)

    # вычисление центральной разностной производной для 0-го узла
    center_diff_array.append((-3 * f_array[0] + 4 * f_array[1] - f_array[2]) / (2 * h))

    i = 1
    while i < n - 1:
        center_diff_array.append((f_array[i + 1] - f_array[i - 1]) / (2 * h))
        i = i + 1

    # вычисление центральной разностной производной для n-го узла
    center_diff_array.append((f_array[(n - 2) - 1] - 4 * f_array[(n - 1) - 1] + 3 * f_array[(n) - 1]) / (2 * h))

    result = avg_square_diff(diff_array, center_diff_array, n, h, name, "Центральная разностная производная")
    center_avg_square_diff_results.append(result)


def avg_square_diff(diff_array, test_diff_array, n, h, func, method):
    # подсчёт среднего арифметического погрешностей
    i = 0
    diff = 0
    square_diff = 0
    while i < n - 1:
        diff = diff + abs(test_diff_array[i] - diff_array[i])
        square_diff = square_diff + ((test_diff_array[i] - diff_array[i]) ** 2)
        i = i + 1

    result = np.sqrt(abs((diff / n) ** 2 - square_diff / n))
    print("Среднеквадратическое отклонение для метода '" + method + "' функции " + func + ": " + str(result))
    return result


def draw_func_and_diff(func, diff, name):
    x_array = []
    a = 1
    b = 100
    h = 0.001

    # узлы отрезка [a, b] с шагом h
    for i in np.arange(a, b, h):
        x_array.append(i)
    x_array.append(b)

    diff_array = []  # аналитически вычисленные значения производной в узлах

    for i in x_array:
        diff_array.append(diff(i))

    plt.figure()
    plt.plot(x_array, diff_array)
    plt.xlabel("x")
    plt.ylabel("Производная функции " + name)
    plt.title("График аналитической производной на отрезке [" + str(a) + ", " + str(b) + "]")
    plt.show()


#  расчёты для функции ln(x):
draw_func_and_diff(f1, diff1, "ln(x)")

compute(1, 100, 0.001, f1, diff1, "ln(x)")
compute(1, 100, 0.001 / 2, f1, diff1, "ln(x)")
compute(1, 100, 0.001 / 4, f1, diff1, "ln(x)")
compute(1, 100, 0.001 / 8, f1, diff1, "ln(x)")
compute(1, 100, 0.001 / 16, f1, diff1, "ln(x)")

steps = [0.001, 0.001 / 2, 0.001 / 4, 0.001 / 8, 0.001 / 16]

plt.figure()
plt.plot(steps, right_avg_square_diff_results, color='Red')
plt.gca().invert_xaxis()
plt.title("Ср. откл. производной ln(x) - правой разност. производной")

plt.figure()
plt.plot(steps, left_avg_square_diff_results, color='Blue')
plt.gca().invert_xaxis()
plt.title("Ср. откл. производной ln(x) - левой разност. производной")

plt.figure()
plt.plot(steps, center_avg_square_diff_results, color='Green')
plt.gca().invert_xaxis()
plt.title("Ср. откл. производной ln(x) - центр. разност. производной")
plt.show()

right_avg_square_diff_results.clear()
left_avg_square_diff_results.clear()
center_avg_square_diff_results.clear()

# расчёты для функции sin(x)
draw_func_and_diff(f2, diff2, "sin(x)")

compute(1, 100, 0.001, f2, diff2, "sin(x)")
compute(1, 100, 0.001 / 2, f2, diff2, "sin(x)")
compute(1, 100, 0.001 / 4, f2, diff2, "sin(x)")
compute(1, 100, 0.001 / 8, f2, diff2, "sin(x)")
compute(1, 100, 0.001 / 16, f2, diff2, "sin(x)")

plt.figure()
plt.plot(steps, right_avg_square_diff_results, color='Red')
plt.gca().invert_xaxis()
plt.title("Ср. откл. производной sin(x) - правой разност. производной")

plt.figure()
plt.plot(steps, left_avg_square_diff_results, color='Blue')
plt.gca().invert_xaxis()
plt.title("Ср. откл. производной sin(x) - левой разност. производной")

plt.figure()
plt.plot(steps, center_avg_square_diff_results, color='Green')
plt.gca().invert_xaxis()
plt.title("Ср. откл. производной sin(x) - центр. разност. производной")
plt.show()
