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
