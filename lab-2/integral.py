import matplotlib.pyplot as plt
import numpy as np

square_fault_results = []  # погрешность для метода прямоугольников
trapezium_fault_results = []  # погрешность для метода трапеций
simpson_fault_results = []  # погрешность для метода Симпсона


def f1(x):
    return np.log(x)


def f2(x):
    return np.sin(x)


def integral1(a, b):
    return (b * np.log(b) - b) - (a * np.log(a) - a)


def integral2(a, b):
    return -np.cos(b) - (-np.cos(a))


def compute(a, b, h, func, integral, name):
    x_array = []

    # узлы отрезка [a, b] с шагом h
    for i in np.arange(a, b, h):
        x_array.append(i)
    x_array.append(b)

    square_int = 0  # вычисленное значение интеграла методом средних прямоугольников
    trapezium_int = 0  # вычисленное значение интеграла методом трапеций
    simpson_int = 0  # вычисленное значение интеграла методом Симпсона

    i = 0
    n = len(x_array)
    print(n)
    while i < n - 1:
        # площадь прямоугольника
        square_int += h * func(x_array[i] + h / 2)
        i = i + 1

    i = 0
    while i < n - 1:
        # площадь трапеции
        trapezium_int += h / 2 * (func(x_array[i]) + func(x_array[i + 1]))
        i = i + 1

    i = 0
    while i < n - 1:
        # площадь под параболой
        simpson_int += h / 6 * (func(x_array[i]) + 4 * func(x_array[i] + h / 2) + func(x_array[i + 1]))
        i = i + 1

    exact_integral = integral(a, b)
    square_fault_results.append(abs(square_int - exact_integral))
    trapezium_fault_results.append(abs(trapezium_int - exact_integral))
    simpson_fault_results.append(abs(simpson_int - exact_integral))


compute(1, 100, 0.1, f1, integral1, "ln(x)")
compute(1, 100, 0.1 / 2, f1, integral1, "ln(x)")
compute(1, 100, 0.1 / 4, f1, integral1, "ln(x)")
compute(1, 100, 0.1 / 8, f1, integral1, "ln(x)")
compute(1, 100, 0.1 / 16, f1, integral1, "ln(x)")

steps = [0.1, 0.1 / 2, 0.1 / 4, 0.1 / 8, 0.1 / 16]

plt.figure()
plt.plot(steps, square_fault_results, color='Pink')
plt.gca().invert_xaxis()
plt.title("Погрешность интеграла - метод прямоуг. ф-и ln(x)")

plt.figure()
plt.plot(steps, trapezium_fault_results, color='Purple')
plt.gca().invert_xaxis()
plt.title("Погрешность интеграла - метод трапеций ф-и ln(x)")

plt.figure()
plt.plot(steps, simpson_fault_results, color='Magenta')
plt.gca().invert_xaxis()
plt.title("Погрешность интеграла - метод Симпсона ф-и ln(x)")
plt.show()

square_fault_results.clear()
trapezium_fault_results.clear()
simpson_fault_results.clear()

compute(1, 100, 0.1, f2, integral2, "sin(x)")
compute(1, 100, 0.1 / 2, f2, integral2, "sin(x)")
compute(1, 100, 0.1 / 4, f2, integral2, "sin(x)")
compute(1, 100, 0.1 / 8, f2, integral2, "sin(x)")
compute(1, 100, 0.1 / 16, f2, integral2, "sin(x)")

plt.figure()
plt.plot(steps, square_fault_results, color='Pink')
plt.gca().invert_xaxis()
plt.title("Погрешность интеграла - метод прямоуг. ф-и sin(x)")

plt.figure()
plt.plot(steps, trapezium_fault_results, color='Purple')
plt.gca().invert_xaxis()
plt.title("Погрешность интеграла - метод трапеций ф-и sin(x)")

plt.figure()
plt.plot(steps, simpson_fault_results, color='Magenta')
plt.gca().invert_xaxis()
plt.title("Погрешность интеграла - метод Симпсона ф-и sin(x)")
plt.show()
