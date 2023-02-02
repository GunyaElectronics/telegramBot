# simple funct, return nothing
def my_func():
    print('My func')


def sum_x_y(xx, yy):
    return xx + yy


my_func()
x = int(input("Input x:"))
y = int(input("Input y:"))
print(type(x))
print(f'Sum x + y = {sum_x_y(x, y)}')
