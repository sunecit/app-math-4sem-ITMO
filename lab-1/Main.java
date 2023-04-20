import java.util.ArrayList;
import java.util.List;

public class Main {
    public static void main(String[] args)
    {
        // начальные значения интервала поиска, в котором функция является унимодальной
        double a = Math.PI;
        double b = Math.PI * 2;

        // заданная точность поиска
        double e = 0.001;

        dichotomy(a, b, e);
        System.out.println();
        goldenCut(a, b, e);
        System.out.println();
        fibonacci(a, b, e);
        System.out.println();
        quadraticInterpolation(a, b, e);
        System.out.println();
        brent(a, b, e);
    }

    private static double function(double x) // метод, который вычисляет значение функции в точке x
    {
        return x * x * x * Math.sin(x);
    }

    private static void printInterval(int n, double a, double b)
    {
        System.out.println("Итерация №" + n + ":\t" + a + "\t" + b);
    }

    private static void dichotomy(double a, double b, double e)
    {
        System.out.println("Метод дихотомии на отрезке [" + a + ", " + b + "]");
        System.out.println("Таблица изменения интервала поиска:");

        int n = 0; // количество итераций
        int m = 0; // количество вычислений функции

        final double delta = e / 3; // удовлетворяет условию < (e / 2)

        while (b - a > e)
        {
            n++;
            printInterval(n, a, b);

            double mid = (a + b) / 2; // середина отрезка

            double x1 = mid - delta;
            double x2 = mid + delta;
            double fx1 = function(x1);
            double fx2 = function(x2);
            m += 2;

            if (fx1 > fx2)
            {
                a = x1;
            }
            else if (fx1 < fx2)
            {
                b = x2;
            }
            else
            {
                a = x1;
                b = x2;
            }
        }

        System.out.println("Минимум находится в интервале: [" + a + ", " + b + "]");
        System.out.println("Значение функции = " + function((a + b) / 2));
        System.out.println("Количество итераций: " + n);
        System.out.println("Количество вычислений функции: " + m);
    }

    private static void goldenCut(double a, double b, double e)
    {
        System.out.println("Метод золотого сечения на отрезке [" + a + ", " + b + "]");
        System.out.println("Таблица изменения интервала поиска:");

        int n = 0; // количество итераций
        int m = 0; // количество вычислений функции

        final double goldenNumber = (Math.sqrt(5) - 1) / 2; // золотое число

        boolean left = false; // флаг, обозначающий, что нужно вычислить местонахождение левой точки и значение ф-и в ней
        double fxPrev = 0; // значение ф-и, вычисленное на предыдущей итерации, для x, к-е остаётся для текущей итерации

        double x1 = b - (b - a) * goldenNumber;
        double x2 = a + (b - a) * goldenNumber;
        n = 1; // произведена первая итерация

        double fx1 = function(x1);
        double fx2 = function(x2);
        m = 2; // произведён подсчёт значения функции дважды

        printInterval(n, a, b);

        if (fx1 > fx2)
        {
            a = x1;
            left = false;
            fxPrev = fx2;
        }
        else if (fx1 <= fx2)
        {
            b = x2;
            left = true;
            fxPrev = fx1;
        }

        while (b - a > e)
        {
            n++; // очередная итерация
            m++; // очередной подсчёт происходит единожды
            printInterval(n, a, b);
            if (left)
            {
                x2 = x1; // точка, оставшаяся с предыдущей итерации, становится правой точкой
                fx2 = fxPrev;

                x1 = b - (b - a) * goldenNumber; // вычисляем местоположение левой точки
                fx1 = function(x1);
            }
            else
            {
                x1 = x2; // точка, оставшаяся с предыдущей итерации, становится левой точкой
                fx1 = fxPrev;

                x2 = a + (b - a) * goldenNumber; // вычисляем местоположение правой точки
                fx2 = function(x2);
            }

            if (fx1 > fx2)
            {
                a = x1;
                left = false;
                fxPrev = fx2;
            }
            else if (fx1 <= fx2)
            {
                b = x2;
                left = true;
                fxPrev = fx1;
            }
        }

        System.out.println("Минимум находится в интервале: [" + a + ", " + b + "]");
        System.out.println("Значение функции = " + function((a + b) / 2));
        System.out.println("Количество итераций: " + n);
        System.out.println("Количество вычислений функции: " + m);
    }

    private static void fibonacci(double a, double b, double e)
    {
        System.out.println("Метод фибоначчи на отрезке [" + a + ", " + b + "]");
        System.out.println("Таблица изменения интервала поиска:");

        int n = 0; // количество итераций

        List<Double> fibonacciNumbers = new ArrayList<>();
        fibonacciNumbers.add(1.0);
        fibonacciNumbers.add(1.0);
        n = 2;

        // найдём n - необходимое количество итераций, нужное для метода Фибоначчи (за n шагов интервал неопределенности
        // должен уменьшится до e)
        while (true)
        {
            double fn = fibonacciNumbers.get(n - 2) + fibonacciNumbers.get(n - 1);
            fibonacciNumbers.add(fn);
            n++;
            if ((b - a) / fn < e)
            {
                // найдено достаточно большое число Фибоначчи
                break;
            }
        }

        // нулевой шаг (k = 0)
        printInterval(1, a, b);
        double x1 = a + fibonacciNumbers.get((n - 1) - 2) / fibonacciNumbers.get(n - 1) * (b - a);
        double x2 = a + fibonacciNumbers.get((n - 1) - 1) / fibonacciNumbers.get(n - 1) * (b - a);

        double fx1 = function(x1);
        double fx2 = function(x2);

        boolean left = false; // флаг, обозначающий, что нужно вычислить местонахождение левой точки и значение ф-и в ней
        double fxPrev = 0; // значение ф-и, вычисленное на предыдущей итерации, для x, к-е остаётся для текущей итерации

        if (fx1 > fx2)
        {
            a = x1;
            left = false;
            fxPrev = fx2;
        }
        else if (fx1 <= fx2)
        {
            b = x2;
            left = true;
            fxPrev = fx1;
        }

        for (int k = 1; k < n - 2; k++)
        {
            printInterval(k + 1, a, b);
            if (left)
            {
                x2 = x1; // точка, оставшаяся с предыдущей итерации, становится правой точкой
                fx2 = fxPrev;

                x1 = a + fibonacciNumbers.get((n - 1) - k - 2) / fibonacciNumbers.get((n - 1) - k) * (b - a); // вычисляем местоположение левой точки
                fx1 = function(x1);
            }
            else
            {
                x1 = x2; // точка, оставшаяся с предыдущей итерации, становится левой точкой
                fx1 = fxPrev;

                x2 = a + fibonacciNumbers.get((n - 1) - k - 1) / fibonacciNumbers.get((n - 1) - k) * (b - a); // вычисляем местоположение правой точки
                fx2 = function(x2);
            }

            if (fx1 > fx2)
            {
                a = x1;
                left = false;
                fxPrev = fx2;
            }
            else if (fx1 <= fx2)
            {
                b = x2;
                left = true;
                fxPrev = fx1;
            }
        }

        printInterval(n - 1, a, b);

        System.out.println("Минимум находится в интервале: [" + a + ", " + b + "]");
        System.out.println("Значение функции = " + function((a + b) / 2));
        System.out.println("Количество итераций: " + (n - 1));
        System.out.println("Количество вычислений функции: " + n);
    }

    private static void quadraticInterpolation(double a, double b, double e)
    {
        System.out.println("Метод парабол на отрезке [" + a + ", " + b + "]");
        System.out.println("Таблица изменения интервала поиска:");

        int n = 0; // количество итераций
        int m = 0; // количество вычислений функции

        double x = a + (b - a) / 3;

        double fa = function(a);
        double fx = function(x);
        double fb = function(b);
        m = 3;

        while (b - a > e)
        {
            n++;
            printInterval(n, a, b);

            // вычисляем минимум параболы, проходящей через точки a, b, x на графике
            double u = x - ((x - a) * (x - a) * (fx - fb) - (x - b) * (x - b) * (fx - fa)) / (2 * ((x - a) * (fx - fb) - (x - b) * (fx - fa)));
            double fu = function(u);
            m++;

            // находим следующий интервал неопределенности
            if (a <= u && u <= x)
            {
                if (fu >= fx) // минимум должен находится в промежутке [u, b]
                {
                    a = u;
                    fa = fu;
                }
                else // минимум должен находится в промежутке [a, x]
                {
                    b = x;
                    fb = fx;
                    x = u;
                    fx = fu;
                }
            }
            else if (x <= u && u <= b)
            {
                if (fu >= fx) // минимум должен находится в промежутке [a, u]
                {
                    b = u;
                    fb = fu;
                }
                else // минимум должен находится в промежутке [x, b]
                {
                    a = x;
                    fa = fx;
                    x = u;
                    fx = fu;
                }
            }
            else
            {
                break;
            }
        }

        System.out.println("Минимум находится в интервале: [" + a + ", " + b + "]");
        System.out.println("Значение функции = " + function((a + b) / 2));
        System.out.println("Количество итераций: " + n);
        System.out.println("Количество вычислений функции: " + m);
    }

    private static void brent(double a, double c, double e)
    {
        System.out.println("Комбинированный метод Брента на отрезке [" + a + ", " + c + "]");
        System.out.println("Таблица изменения интервала поиска:");

        int n = 0; // количество итераций
        int m = 0; // количество вычислений функции

        final double goldenNumber = (3 - Math.sqrt(5)) / 2; // золотое число

        double x = (a + c) / 2;
        double w = x;
        double v = x;

        double fx = function(x);
        double fw = fx;
        double fv = fx;
        m++;

        double d = c - a; // длина интервала текущего шага
        double p = d; // длина интервала предыдущего шага

        while (c - a > e)
        {
            n++;
            printInterval(n, a, c);

            boolean good = false; // флаг, обозначающий, что не нужно использовать золотое сечение
            double u = Double.MIN_VALUE;
            double fu;

            if (!(x == w || w == v || x == v || fx == fw || fw == fv || fx == fv))
            {
                // переходим к методу парабол

                // вычисляем минимум параболы, проходящей через точки x, w, v на графике
                u = x - ((x - w) * (x - w) * (fx - fv) - (x - v) * (x - v) * (fx - fw)) / (2 * ((x - w) * (fx - fv) - (x - v) * (fx - fw)));

                // проверим, подходит ли найденная точка u
                if (a + e < u && c - e > u && Math.abs(u - x) < p / 2)
                {
                    d = Math.abs(u - x);
                    good = true; // метод парабол сработал, золотое сечение не понадобится
                }
            }

            if (!good) // используем ли метод золотого сечения?
            {
                if (x < (a + c) / 2) // левее середины интервала?
                {
                    u = x + goldenNumber * (c - x); // золотое сечение для отрезка [x, c]
                    d = c - x;
                }
                else
                {
                    u = x - goldenNumber * (x - a); // золотое сечение для отрезка [a, x]
                    d = x - a;
                }
            }

            if (good && Math.abs(u - x) < e) // если u слишком близко к x, то отодвигаем её на точность e
            {
                // если u правее x, то сдинется вправо, иначе - влево
                u = x + Math.signum(u - x) * e;
            }

            fu = function(u);
            m++;

            // определим интервал неопределенности для следующей итерации
            if (fu <= fx)
            {
                if (u >= x)
                {
                    a = x;
                }
                else
                {
                    c = x;
                }

                v = w;
                w = x;
                x = u;

                fv = fw;
                fw = fx;
                fx = fu;
            }
            else
            {
                if (u >= x)
                {
                    c = u;
                }
                else
                {
                    a = u;
                }

                if (fu <= fw || w == x)
                {
                    v = w;
                    w = u;
                    fv = fw;
                    fw = fu;
                }
                else if (fu <= fv || v == x || v == w)
                {
                    v = u;
                    fv = fu;
                }
            }
        }

        System.out.println("Минимум находится в интервале: [" + a + ", " + c + "]");
        System.out.println("Значение функции = " + function((a + c) / 2));
        System.out.println("Количество итераций: " + n);
        System.out.println("Количество вычислений функции: " + m);

    }
}
