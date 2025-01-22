from collections import namedtuple

Label = namedtuple("Label", "x y")
Title = namedtuple("Title", "txt")
Plot = namedtuple("Plot", "x y label")
Lim = namedtuple("Lim", "x y")
if __name__ == "__main__":
    print("hi")
    l = Label("FPR", "TPR")
    print(l.x, l.y)
