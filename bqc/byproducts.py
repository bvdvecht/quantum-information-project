class Byproduct:
    def __init__(self, N):
        self.byprods = {}
        self.N = N

    def set(self, k, val):
        self.byprods[k] = val

    def get(self, k):
        try:
            return self.byprods[k]
        except KeyError:
            return 0

    def __str__(self):
        return str(self.byprods)


class XRecord:
    def __init__(self, N):
        self.record = {}
        self.N = N

    def set(self, j, xbyprod):
        assert isinstance(xbyprod, Byproduct)
        print('setting XRecord[{}] = {}'.format(j, xbyprod))
        self.record[j] = xbyprod

    def get(self, j):
        try:
            return self.record[j]
        except KeyError:
            return Byproduct(self.N)


class ZRecord:
    def __init__(self, N):
        self.record = {}
        self.N = N

    def set(self, j, zbyprod):
        assert isinstance(zbyprod, Byproduct)
        print('setting ZRecord[{}] = {}'.format(j, zbyprod))
        self.record[j] = zbyprod

    def get(self, j):
        try:
            return self.record[j]
        except KeyError:
            return Byproduct(self.N)