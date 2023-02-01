counter = 0
while counter <= 15:
    if counter == 5:
        counter = 6
        continue
    elif counter == 11:
        break
    print(counter)
    counter += 1

print('end\n')

while counter:
    counter -= 1
    print(counter)
else:
    print(f"else {counter}\n")

i = 0
while i < 10: i += 1; print(f'while {i}')

for symbol in 'Hello':
    print(symbol)

itr = iter('Hello')

print(next(itr))
print(next(itr))
print(next(itr))
print(next(itr))
print(next(itr))
# print(next(itr))  # StopIteration exception

print('\n')
for i in range(5):
    print(i)

print('\n')
for i in range(2, 7):
    print(i)

print('\n')
for i in range(0, 10, 2):
    print(i)

print('\n')
for i in range(20, 8, -2):
    print(i)

print('\n')
for word in ['Hello', 'world']:
    print(word)
else:
    print('Done\n')

for i in range(2, 10):
    if i == 3:
        continue
    elif i == 8:
        break
    else:
        print(i)
