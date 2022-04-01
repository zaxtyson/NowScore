from strategy.base import Condition

c1 = Condition(lambda: 1 + 1 == 2)  # True
c2 = Condition(lambda: "Hello".endswith("o"))  # True
c3 = Condition(lambda: 2 + 2 == 5)  # False
c4 = Condition(lambda: 2 + 2 == 4)  # True
c5 = Condition(lambda: 100 - 1 == 99)  # True
c6 = Condition(lambda: 100 - 1 == 100)  # False


def clean_up():
    for c in [c1, c2, c3, c4, c5, c6]:
        c.clear()


def dag1():
    clean_up()
    # T -> T -> F -> T -> T
    c1.add_next(c2)
    c2.add_next(c3)
    c3.add_next(c4)
    c4.add_next(c5)
    print(f"dag1: {c1.is_true()}")  # False


def dag2():
    clean_up()
    # T --> T --> T
    #   `-> F --> T
    c1.add_next(c2, c3)
    c2.add_next(c4)
    c3.add_next(c5)
    print(f"dag2: {c1.is_true()}")  # True


def dag3():
    clean_up()
    # T --> T --> T
    #  `--> F --‘
    c1.add_next(c2, c3)
    c2.add_next(c4)
    c3.add_next(c4)
    print(f"dag3: {c1.is_true()}")  # True


if __name__ == '__main__':
    dag1()
    dag2()
    dag3()
