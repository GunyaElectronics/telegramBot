# simple funct, return nothing
def my_func():
    print('My func')


def sum_x_y(xx, yy):
    return xx + yy


my_func()
x = 1  # int(input("Input x:"))
y = 2  # int(input("Input y:"))
print(type(x))
print(f'Sum x + y = {sum_x_y(x, y)}')


def print_some_param(first_name, last_name, age):
    print(f'Hello {first_name} {last_name}. Your age is {age} years!')


print_some_param('Maxim', 'Hunko', 33)
print_some_param(22, 'Hunko', 'Maxim')
print_some_param(age=22, first_name='Maxim', last_name='Hunko')


def new_list(l=[]):
    l.append(['##'])
    print(l)


new_list()
new_list()
new_list()


def new_list2(l=None):
    if not l:
        l = []
    l.append(['##'])
    print(l)


new_list2()
new_list2()
new_list2()


# tuples package to *args example
def avg(*args):
    total = 0
    for v in args:
        total += v
    return total/len(args)


print(avg(34, 67, 135))

t = (1, 3, 5, 7, 88)

print(avg(*t))


# dictionary as function param
# and example with documentation
def summ(**kwargs):
    """It is function for do nothing"""
    pass
    print(kwargs)
    print(type(kwargs))
    for key, value in kwargs.items():
        print(key, ' --> ', value)


summ(one=1, two=2, name='Maxim')

fff = {'first': 11, 'second': 35}
summ(**fff)

print(summ.__doc__)

# get annotation for functions
print(summ.__annotations__)


# add annotation for function
def ff(a: int, b: str) -> float:
    print(a, b)
    return 3.5


print(ff.__annotations__)
