# polynomial.py
from copy import deepcopy


class Polynomial:

    def __init__(self, *coefficients):
        coefs = []
        if len(coefficients) > 1:
            for i in range(len(coefficients)):
                coefs.append(coefficients[i])
        else:
            if type(coefficients[0]) is list:
                coefs = deepcopy(coefficients[0])
            elif type(coefficients[0]) is dict:
                n = max(coefficients[0]) + 1
                coefs = [0] * n
                for pow in coefficients[0]:
                    coefs[pow] = coefficients[0][pow]
            elif type(coefficients[0]) is Polynomial:
                coefs = deepcopy(coefficients[0].coefs)
            elif type(coefficients[0]) is int:
                coefs.append(coefficients[0])
            elif type(coefficients[0]) is float:
                coefs.append(coefficients[0])
        while coefs[-1] == 0 and len(coefs) > 1:
            coefs = coefs[:-1]
        self.coefs = coefs

    def __repr__(self):
        return 'Polynomial ' + str(self.coefs)

    def __str__(self):
        ans = ''
        n = len(self.coefs) - 1
        for i in range(n - 1):
            if self.coefs[n - i] > 0 and self.coefs[n - i] != 1:
                ans += ' + '
                ans += str(self.coefs[n - i]) + 'x^' + str(n - i)
            elif self.coefs[n - i] < 0 and self.coefs[n - i] != -1:
                ans += ' - '
                ans += str(-self.coefs[n - i]) + 'x^' + str(n - i)
            elif self.coefs[n - i] == 1:
                ans += ' + ' + 'x^' + str(n - i)
            elif self.coefs[n - i] == -1:
                ans += ' - ' + 'x^' + str(n - i)
        if len(self.coefs) > 1 and self.coefs[1] > 0 and self.coefs[1] != 1:
            ans += ' + ' + str(self.coefs[1]) + 'x'
        elif len(self.coefs) > 1 and self.coefs[1] < 0 and self.coefs[1] != -1:
            ans += ' - ' + str(-self.coefs[1]) + 'x'
        elif len(self.coefs) > 1 and self.coefs[1] == 1:
            ans += ' + ' + 'x'
        elif len(self.coefs) > 1 and self.coefs[1] == -1:
            ans += ' - ' + 'x'
        if ans == '' and self.coefs[0] == 0:
            return '0'
        elif ans == '':
            return(str(self.coefs[0]))
        elif self.coefs[0] > 0:
            first = ans[:3]
            if first == ' + ':
                ans = ans[3:]
                ans += ' + ' + str(self.coefs[0])
                return ans
            else:
                ans = '-' + ans[3:]
                ans += ' + ' + str(self.coefs[0])
                return ans
        elif self.coefs[0] < 0:
            first = ans[:3]
            if first == ' + ':
                ans = ans[3:]
                ans += ' - ' + str(-self.coefs[0])
                return ans
            else:
                ans = '-' + ans[3:]
                ans += ' - ' + str(-self.coefs[0])
                return ans
        else:
            first = ans[:3]
            if first == ' + ':
                ans = ans[3:]
                return ans
            else:
                ans = '-' + ans[3:]
                return ans

    def __eq__(self, other):
        other = Polynomial(other)
        return self.coefs == other.coefs

    def __add__(self, other):
        other = Polynomial(other)
        if len(self.coefs) < len(other.coefs):
            ans = [0] * len(other.coefs)
            for i in range(len(self.coefs)):
                ans[i] = self.coefs[i] + other.coefs[i]
            for i in range(len(self.coefs), len(other.coefs)):
                ans[i] = other.coefs[i]
            return Polynomial(ans)
        else:
            ans = [0] * len(self.coefs)
            for i in range(len(other.coefs)):
                ans[i] = self.coefs[i] + other.coefs[i]
            for i in range(len(other.coefs), len(self.coefs)):
                ans[i] = self.coefs[i]
            return Polynomial(ans)

    __radd__ = __add__

    def __neg__(self):
        ans = deepcopy(self.coefs)
        for i in range(len(ans)):
            ans[i] *= -1
        return Polynomial(ans)

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return -(self) + other

    def __call__(self, x):
        if len(self.coefs) == 1:
            return self.coefs[0]
        else:
            b = 0
            n = len(self.coefs)
            for i in range(len(self.coefs)):
                b = self.coefs[n - 1 - i] + b * x
            return b

    def degree(self):
        return len(self.coefs) - 1

    def der(self, d=1):
        if d == 0:
            return self
        if d == 1:
            ans = []
            for i in range(1, len(self.coefs)):
                ans.append(i * self.coefs[i])
            return Polynomial(ans)
        else:
            cur = self.der(d - 1)
            return cur.der()

    def __mul__(self, other):
        other = Polynomial(other)
        n = len(self.coefs) - 1
        m = len(other.coefs) - 1
        ans = [0] * (n + m + 1)
        for i in range(n + m + 1):
            k = 0
            while k <= i and k <= n:
                if i - k > m:
                    k += 1
                else:
                    ans[i] += self.coefs[k] * other.coefs[i - k]
                    k += 1
        return Polynomial(ans)

    __rmul__ = __mul__

    def __mod__(self, other):
        other = Polynomial(other)
        n = self.degree()
        m = other.degree()
        if n < m:
            return self
        else:
            cur = {}
            cur[n - m] = self.coefs[-1] / other.coefs[-1]
            cur = Polynomial(cur)
            ans = self - cur * other
            return ans % other

    def __rmod__(self, other):
        other = Polynomial(other)
        return other % self

    def gcd(self, other):
        other = Polynomial(other)
        n = self.degree()
        m = other.degree()
        if n > m:
            new = self % other
            if new == Polynomial(0):
                return other
            else:
                res = other.gcd(new)
                return res
        else:
            new = other % self
            if new == Polynomial(0):
                return self
            else:
                res = self.gcd(new)
                return res

    def __iter__(self):
        self.n = (0, self.coefs[0])
        return self

    def __next__(self):
        if self.n[0] < self.degree():
            res = self.n
            self.n = (self.n[0] + 1, self.coefs[self.n[0] + 1])
            return res
        if self.n[0] == self.degree():
            res = self.n
            self.n = (self.n[0] + 1, 0)
            return res
        else:
            raise StopIteration

class RealPolynomial(Polynomial):
    def find_root(self):
        eps = 1e-12
        a = 2
        while self(a) * self(-a) > eps:
            a *= 2
        b = -a
        while a - b > eps:
            c = (a + b) / 2
            if abs(self(c)) < eps:
                return c
            if self(c) * self(a) < -eps:
                b = c
            else:
                a = c
        return a

class QuadraticPolynomial(Polynomial):
    def solve(self):
        n = self.degree()
        if n == 0:
            return []
        if n == 1:
            return [-self.coefs[0] / self.coefs[1]]
        if n == 2:
            eps = 1e-12
            a = self.coefs[2]
            b = self.coefs[1]
            c = self.coefs[0]
            d = b * b - 4 * a * c
            if d < -eps:
                return []
            if -eps < d < eps:
                return [-b / (2 * a)]
            else:
                x1 = (-b + d**0.5) / (2 * a)
                x2 = (-b - d**0.5) / (2 * a)
                if x1 - x2 < -eps:
                    (x1, x2) = (x2, x1)
                return [x2, x1]

if __name__ == '__main__':
    poly = QuadraticPolynomial([-15, 7, 2])
    print(sorted(poly.solve()) == [-5.0, 1.5])
