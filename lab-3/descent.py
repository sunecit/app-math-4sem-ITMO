import numpy as np
import matplotlib.pyplot as plt

start = [10, 10]


def func1(x, y):
    return 2 * x * x + (y - 3) ** 2  # целевая функция 1


def func2(x, y):
    return (x - 1) ** 2 + 5 * y * y + 2 * x  # целевая функция 2


def func1_part_deriv_x(x):
    return 4 * x  # частная производная по x для ф-и 1


def func1_part_deriv_y(y):
    return 2 * (y - 3)  # частная производная по y для ф-и 1


def func2_part_deriv_x(x):
    return 2 * x  # частная производная по x для ф-и 2


def func2_part_deriv_y(y):
    return 10 * y  # частная производная по y для ф-и 2


def func1_minimization_func(h, x, y, direction):
    return func1(x + direction[0] * h, y + direction[1] * h)  # ф-я для минимизации в направлении вектора для ф-и 1


def func2_minimization_func(h, x, y, direction):
    return func2(x + direction[0] * h, y + direction[1] * h)  # ф-я для минимизации в направлении вектора для ф-и 2


def antigrad(x, y, part_deriv_x, part_deriv_y):
    ag = [-part_deriv_x(x), -part_deriv_y(y)]  # вычисление антиградиента для заданных ф-й частных производных
    return ag


def const_descent(e, h, x0, func, part_deriv_x, part_deriv_y):
    print("Градиентный спуск с постоянным шагом с e = {:0.8f}, h = {:0.8f}, начало в {}".format(e, h, x0))
    ax = plt.figure().add_subplot(projection='3d')
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    x_show, y_show = np.meshgrid(np.linspace(-10, 10, 20), np.linspace(-10, 10, 20))
    z_show = func(x_show, y_show)
    ax.contour(x_show, y_show, z_show)
    iterations = 0  # количество итераций
    x = x0
    fx = func(x[0], x[1])
    while True:
        iterations += 1
        if iterations > 1000000:
            print("Алгоритм не сошёлся!")
            break
        ag = antigrad(x[0], x[1], part_deriv_x, part_deriv_y)  # считаем антиградиент в текущей точке (вектор)
        ag_norm = np.sqrt(ag[0] ** 2 + ag[1] ** 2)  # вычисляем норму (длину) вектора антиградиента
        if ag_norm ** 2 < e:
            fx = func(x[0], x[1])  # вычисляем значение ф-и в новой точке
            print("Минимум в точке: [{:0.8f}, {:0.8f}], значение минимума: {:0.8f}, всего итераций: {}"
                  .format(x[0], x[1], fx, iterations))
            break
        ag_normalized = [ag[0] / ag_norm, ag[1] / ag_norm]  # получаем единичный вектор, направленный как вектор антиградиент
        x_prev = x
        fx_prev = fx
        x = [ag_normalized[0] * h + x[0], ag_normalized[1] * h + x[1]]  # делаем шаг в направлении убывания длиной h
        fx = func(x[0], x[1])
        ax.plot([x_prev[0], x[0]], [x_prev[1], x[1]], [fx_prev, fx], '.-', c='red')
    plt.title("Град. спуск с постоянным шагом")
    plt.show()


print("Для первой функции:")
const_descent(0.001, 0.1, start, func1, func1_part_deriv_x, func1_part_deriv_y)
const_descent(0.001, 0.01, start, func1, func1_part_deriv_x, func1_part_deriv_y)
const_descent(0.0001, 0.001, start, func1, func1_part_deriv_x, func1_part_deriv_y)
const_descent(0.0001, 0.0001, start, func1, func1_part_deriv_x, func1_part_deriv_y)
const_descent(0.1, 0.01, start, func1, func1_part_deriv_x, func1_part_deriv_y)

print("\nДля второй функции:")
const_descent(0.001, 0.1, start, func2, func2_part_deriv_x, func2_part_deriv_y)
const_descent(0.001, 0.01, start, func2, func2_part_deriv_x, func2_part_deriv_y)
const_descent(0.0001, 0.001, start, func2, func2_part_deriv_x, func2_part_deriv_y)
const_descent(0.0001, 0.0001, start, func2, func2_part_deriv_x, func2_part_deriv_y)
const_descent(0.1, 0.1, start, func2, func2_part_deriv_x, func2_part_deriv_y)


def golden_cut(func, x, y, ag_normalized, e, a, b):
    golden_number = (np.sqrt(5) - 1) / 2
    left = False
    fx_prev = 0
    x1 = b - (b - a) * golden_number
    x2 = a + (b - a) * golden_number
    fx1 = func(x1, x, y, ag_normalized)
    fx2 = func(x2, x, y, ag_normalized)

    if fx1 > fx2:
        a = x1
        left = False
        fx_prev = fx2
    elif fx1 <= fx2:
        b = x2
        left = True
        fx_prev = fx1

    while b - a > e:
        if left:
            x2 = x1
            fx2 = fx_prev
            x1 = b - (b - a) * golden_number
            fx1 = func(x1, x, y, ag_normalized)

        else:
            x1 = x2
            fx1 = fx_prev
            x2 = a + (b - a) * golden_number
            fx2 = func(x2, x, y, ag_normalized)

        if fx1 > fx2:
            a = x1
            left = False
            fx_prev = fx2

        elif fx1 <= fx2:
            b = x2
            left = True
            fx_prev = fx1

    return (a + b) / 2


def steepest_descent(e, x0, func, part_deriv_x, part_deriv_y, antigrad_func):
    print("Метод наискорейшего спуска с e = {:0.8f}, начало в {}".format(e, x0))
    ax = plt.figure().add_subplot(projection='3d')
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    x_show, y_show = np.meshgrid(np.linspace(-10, 10, 20), np.linspace(-10, 10, 20))
    z_show = func(x_show, y_show)
    ax.contour(x_show, y_show, z_show)
    iterations = 0  # количество итераций
    x = x0
    fx = func(x[0], x[1])
    while True:
        iterations += 1
        if iterations > 1000000:
            print("Алгоритм не сошёлся!")
            break
        ag = antigrad(x[0], x[1], part_deriv_x, part_deriv_y)  # считаем антиградиент в текущей точке (вектор)
        ag_norm = np.sqrt(ag[0] ** 2 + ag[1] ** 2)  # вычисляем норму (длину) вектора антиградиента
        if ag_norm ** 2 < e:
            fx = func(x[0], x[1])  # вычисляем значение ф-и в новой точке
            print("Минимум в точке: [{:0.8f}, {:0.8f}], значение минимума: {:0.8f}, всего итераций: {}"
                  .format(x[0], x[1], fx, iterations))
            break
        ag_normalized = [ag[0] / ag_norm, ag[1] / ag_norm]  # получаем единичный вектор, направленный как вектор антиградиент
        h = golden_cut(antigrad_func, x[0], x[1], ag_normalized, e, 0, 100)
        x_prev = x
        fx_prev = fx
        x = [ag_normalized[0] * h + x[0], ag_normalized[1] * h + x[1]]  # делаем шаг в направлении убывания длиной h
        fx = func(x[0], x[1])
        ax.plot([x_prev[0], x[0]], [x_prev[1], x[1]], [fx_prev, fx], '.-', c='red')
    plt.title("М-д наискорейшего спуска")
    plt.show()


print("\nДля первой функции:")
steepest_descent(0.1, start, func1, func1_part_deriv_x, func1_part_deriv_y, func1_minimization_func)
steepest_descent(0.01, start, func1, func1_part_deriv_x, func1_part_deriv_y, func1_minimization_func)
steepest_descent(0.001, start, func1, func1_part_deriv_x, func1_part_deriv_y, func1_minimization_func)
steepest_descent(0.0001, start, func1, func1_part_deriv_x, func1_part_deriv_y, func1_minimization_func)
steepest_descent(0.00001, start, func1, func1_part_deriv_x, func1_part_deriv_y, func1_minimization_func)

print("\nДля второй функции:")
steepest_descent(0.1, start, func2, func2_part_deriv_x, func2_part_deriv_y, func2_minimization_func)
steepest_descent(0.01, start, func2, func2_part_deriv_x, func2_part_deriv_y, func2_minimization_func)
steepest_descent(0.001, start, func2, func2_part_deriv_x, func2_part_deriv_y, func2_minimization_func)
steepest_descent(0.0001, start, func2, func2_part_deriv_x, func2_part_deriv_y, func2_minimization_func)
steepest_descent(0.00001, start, func2, func2_part_deriv_x, func2_part_deriv_y, func2_minimization_func)


def shrinking_step_descent(e, x0, func, part_deriv_x, part_deriv_y):
    print("Градиентный спуск с переменным шагом с e = {:0.8f}, с = 0.1, начало в {}".format(e, x0))
    ax = plt.figure().add_subplot(projection='3d')
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    x_show, y_show = np.meshgrid(np.linspace(-10, 10, 20), np.linspace(-10, 10, 20))
    z_show = func(x_show, y_show)
    ax.contour(x_show, y_show, z_show)
    iterations = 0  # количество итераций
    x = x0
    fx = func(x[0], x[1])
    while True:
        iterations += 1
        if iterations > 1000000:
            print("Алгоритм не сошёлся!")
            break
        ag = antigrad(x[0], x[1], part_deriv_x, part_deriv_y)  # считаем антиградиент в текущей точке (вектор)
        ag_norm = np.sqrt(ag[0] ** 2 + ag[1] ** 2)  # вычисляем норму (длину) вектора антиградиента
        if ag_norm ** 2 < e:
            fx = func(x[0], x[1])  # вычисляем значение ф-и в новой точке
            print("Минимум в точке: [{:0.8f}, {:0.8f}], значение минимума: {:0.8f}, всего итераций: {}"
                  .format(x[0], x[1], fx, iterations))
            break
        ag_normalized = [ag[0] / ag_norm, ag[1] / ag_norm]  # получаем единичный вектор, направленный как вектор антиградиент
        fx = func(x[0], x[1])  # значение функции в текущей точке

        # производная функции "фи" = F(xk + h * dk), где xk - текущая точка (вектор),
        # dk - направление спуска для текущей точки (вектор), для h = 0
        # производную считаем как скалярное произведение антиградиента и направления спуска
        deriv_fi_0 = (-ag[0] * ag_normalized[0]) + (-ag[1] * ag_normalized[1])
        c = 0.001  # постоянная для условия армихо
        h = 100  # начальное значение шага, которое будет уменьшаться делением пополам
        # значение целевой функции для текущего шага h
        fi_h = func(x[0] + h * ag_normalized[0], x[1] + h * ag_normalized[1])
        while fi_h > fx + c * h * deriv_fi_0:
            h = h * 0.5
            fi_h = func(x[0] + h * ag_normalized[0], x[1] + h * ag_normalized[1])  # рассчитаем значение целевой ф-и для нового h
        x_prev = x
        fx_prev = fx
        x = [ag_normalized[0] * h + x[0], ag_normalized[1] * h + x[1]]  # делаем шаг в направлении убывания длиной h
        fx = func(x[0], x[1])
        ax.plot([x_prev[0], x[0]], [x_prev[1], x[1]], [fx_prev, fx], '.-', c='red')
    plt.title("Град. спуск с переменным шагом")
    plt.show()


print("\nДля первой функции:")
shrinking_step_descent(0.1, start, func1, func1_part_deriv_x, func1_part_deriv_y)
shrinking_step_descent(0.01, start, func1, func1_part_deriv_x, func1_part_deriv_y)
shrinking_step_descent(0.001, start, func1, func1_part_deriv_x, func1_part_deriv_y)
shrinking_step_descent(0.0001, start, func1, func1_part_deriv_x, func1_part_deriv_y)
shrinking_step_descent(0.00001, start, func1, func1_part_deriv_x, func1_part_deriv_y)

print("\nДля второй функции:")
shrinking_step_descent(0.1, start, func2, func2_part_deriv_x, func2_part_deriv_y)
shrinking_step_descent(0.01, start, func2, func2_part_deriv_x, func2_part_deriv_y)
shrinking_step_descent(0.001, start, func2, func2_part_deriv_x, func2_part_deriv_y)
shrinking_step_descent(0.0001, start, func2, func2_part_deriv_x, func2_part_deriv_y)
shrinking_step_descent(0.00001, start, func2, func2_part_deriv_x, func2_part_deriv_y)


def conjugate_gradient_descent(e, x0, func, part_deriv_x, part_deriv_y, antigrad_func):
    print("Метод сопряженных градиентов с e = {:0.8f}, начало в {}".format(e, x0))
    ax = plt.figure().add_subplot(projection='3d')
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    x_show, y_show = np.meshgrid(np.linspace(-10, 10, 20), np.linspace(-10, 10, 20))
    z_show = func(x_show, y_show)
    ax.contour(x_show, y_show, z_show)
    iterations = 1
    x = x0
    fx0 = func(x[0], x[1])
    ag = antigrad(x[0], x[1], part_deriv_x, part_deriv_y)
    p = ag
    h = golden_cut(antigrad_func, x[0], x[1], p, e, 0, 100)
    x = [p[0] * h + x[0], p[1] * h + x[1]]
    fx = func(x[0], x[1])
    ax.plot([x0[0], x[0]], [x0[1], x[1]], [fx0, fx], '.-', c='red')
    while True:
        iterations += 1
        if iterations > 1000000:
            print("Алгоритм не сошёлся!")
            break
        ag_prev = ag
        p_prev = p
        ag = antigrad(x[0], x[1], part_deriv_x, part_deriv_y)
        ag_norm = np.sqrt(ag[0] ** 2 + ag[1] ** 2)
        if ag_norm ** 2 < e:
            fx = func(x[0], x[1])
            print("Минимум в точке: [{:0.8f}, {:0.8f}], значение минимума: {:0.8f}, всего итераций: {}"
                  .format(x[0], x[1], fx, iterations))
            break

        w = (ag[0] * ag[0] + ag[1] * ag[1]) / (ag_prev[0] * ag_prev[0] + ag_prev[1] * ag_prev[1])
        p = [ag[0] + w * ag_prev[0], ag[1] + w * ag_prev[1]]
        h = golden_cut(antigrad_func, x[0], x[1], p, e, 0, 100)
        x_prev = x
        fx_prev = fx
        x = [p[0] * h + x[0], p[1] * h + x[1]]
        fx = func(x[0], x[1])
        ax.plot([x_prev[0], x[0]], [x_prev[1], x[1]], [fx_prev, fx], '.-', c='red')
    plt.title("М-д сопряженных градиентов")
    plt.show()

#
print("\nДля первой функции:")
conjugate_gradient_descent(0.1, start, func1, func1_part_deriv_x, func1_part_deriv_y, func1_minimization_func)
conjugate_gradient_descent(0.01, start, func1, func1_part_deriv_x, func1_part_deriv_y, func1_minimization_func)
conjugate_gradient_descent(0.001, start, func1, func1_part_deriv_x, func1_part_deriv_y, func1_minimization_func)
conjugate_gradient_descent(0.0001, start, func1, func1_part_deriv_x, func1_part_deriv_y, func1_minimization_func)
conjugate_gradient_descent(0.00001, start, func1, func1_part_deriv_x, func1_part_deriv_y, func1_minimization_func)

print("\nДля второй функции:")
conjugate_gradient_descent(0.1, start, func2, func2_part_deriv_x, func2_part_deriv_y, func2_minimization_func)
conjugate_gradient_descent(0.01, start, func2, func2_part_deriv_x, func2_part_deriv_y, func2_minimization_func)
conjugate_gradient_descent(0.001, start, func2, func2_part_deriv_x, func2_part_deriv_y, func2_minimization_func)
conjugate_gradient_descent(0.0001, start, func2, func2_part_deriv_x, func2_part_deriv_y, func2_minimization_func)
conjugate_gradient_descent(0.00001, start, func2, func2_part_deriv_x, func2_part_deriv_y, func2_minimization_func)
