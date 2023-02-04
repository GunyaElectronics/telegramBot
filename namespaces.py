import my_tools

# ----------------------------------------------------------------
# x = value
# import module
# from module import name
# def func(): ...
# def func(arg1, arg2, ... argN): ...
# class MyClass: ...
# ----------------------------------------------------------------


def outer_func():
    var = 90
    another_var = 300
    
    def inner_func():
        another_var = 500
        print(f'inner print var {var}')
        print(f'inner print another_var {another_var}')
    inner_func()
    print(f'outer print var {var}')
    print(f'outer print another_var {another_var}')


print(__name__)  # print module name who run this code

outer_func()
