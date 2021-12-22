from functools import partial
from cmath import sqrt

EPS = 0.001  # погрешность
PREC = 7     # точность вывода

def f(x, coefficients, roots=[]):
    """
    :x - аргумент многочлена
    :coefficients - коэффициенты многочлена
    :roots -  если этот список не пустой, то убирает из многочлена данные корни. то есть возвращает f(x)/(x - root)
    :return: значение функции / многочлена
    """
    result = 0
    # собираем многочлен
    for coef, n in zip(reversed(coefficients), list(range(len(coefficients)))):
        result += coef * x ** n
    # убираем из него корни если нужно
    for root in roots:
        denominator = x - root
        if denominator == 0:
            return 0
        result /= denominator
    return result


def divided_difference(coefficients, roots, *args):
    """
    рекурсивно находит разделенную разность (можно было и вручную найти, но я просто решил выебнуться)
    """
    f1 = partial(f, coefficients=coefficients, roots=roots)  # подставляю в f нужные параметры. f1 требует только x.
    if len(args) == 2:
        """
                    f(xj) - f(xi)
        f(xi, xj) = -------------
                      xj - xi
        """
        return (f1(args[1]) - f1(args[0])) / (args[1] - args[0])
    else:
        # это просто общая формула
        numerator = divided_difference(coefficients, roots, *args[1:]) - divided_difference(coefficients, roots, *args[:-1])
        denominator = args[-1] - args[0]
        return numerator / denominator


def condition(x2, x1, x0, func):
    """
    условие остановки
    """
    if abs(func(x2)) > EPS:
        return True
    else:
        expr = ((x2 - x1) ** 2) / (2 * x1 - x2 - x0)
        if expr.real < EPS and expr.imag < EPS:
            return False
        else:
            return True


if __name__ == '__main__':
    with open('input.txt', 'rt') as file:
        coefficients = list(map(float, file.readline().strip().split()))

    # подставляю коэфы в f, потому что они не меняются всю программу.
    f1 = partial(f, coefficients=coefficients)
    roots = []  # найденные корни
    for i in range(len(coefficients) - 1):
        x0, x1, x2 = -1, 1, 0  # начальное приближение
        while condition(x2, x1, x0, f1):
            # коэфы квадратного уравнения
            a = divided_difference(coefficients, roots, x2, x1, x0)
            b = a * (x2 - x1) + divided_difference(coefficients, roots, x2, x1)
            c = f1(x2, roots=roots)
            d = sqrt(b ** 2 - 4 * a * c)
            # корни квадратного уравнения
            root1 = (-b + d) / (2 * a)
            root2 = (-b - d) / (2 * a)
            root = min([root1, root2], key=lambda el: abs(el))
            # смещаем приближение
            x2, x1, x0 = x2 + root, x2, x1
        roots.append(x2)
    for i in range(len(roots)):
        if abs(roots[i].imag) < EPS:
            roots[i] = roots[i].real

    residuals = []

    for root in roots:
        residuals.append(abs(f1(root)))

    for i in range(len(roots)):
        print("Корень: " + str(roots[i]) + "     ;     Невязка: " + str(residuals[i]))