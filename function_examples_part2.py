# Function def in function
def external():
    def internal():
        return 1
    print(internal())


external()
# internal() -> exception, name 'internal' is not defined

# private function example
p = lambda x, y: x + y

print(p(1, 2))

l = [lambda x, y: x-y,
     lambda x, y: x+y,
     lambda x, y: x*y,
     lambda x, y: x/y
     ]

for ffff in l:
    print(ffff(10, 20))

dict1 = {'key': lambda x: print('1' + x), 'lrp': lambda x: print('2' + x)}

from function_examples import summ

print('11111111111111111111111')
summ(one=1, two=2, name='Maxim')
sum_x_y(0,1)
