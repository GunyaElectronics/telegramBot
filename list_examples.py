a = [1, 2, 3, 5, 7, 8, 100]
print(type(a))

b = list(('q', 'w', 'e', 'r', 't'))
print(type(b))

b = [100, 1, 2, 3, 5, 7, 8]
print('a and c is ' + ('same' if a == b else 'different'))

c = [1, 2, 3, 5, 7, 8, 100]
print(f'a and c is {"same" if a == c else "different"}')

print('a is c' if a is c else 'a is not c')

print('\n')
w = ['Hello', 'my', 'amassing']
# list of functions example
funcs = [print, len]
for f in funcs:
    for i in w:
        print(f(i))

# work with list indexes like with strings symbols
list1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(list1)
print(list1[0])
print(list1[-1])
list2 = list1[2:7]
print(list2)
list3 = list1[:6:2]
print(list3)
list3 = list1[::-1]
print(list3)

# copy of list
list1_copy = list1[:]
print(list1_copy == list1)  # True
print(list1_copy is list1)  # False
