print('hello')
# class 'str'
name = 'Maxim'  # variable str
# input("please enter name: ")
# printing methods
print("Hi, ", name, "!")
# f"string" example (formatted)
print(f"Hi , {name}!")
print("Hi, ", name, "!", sep='')

# raw string example
raw_str = r"something \" \ \' ''"

# string concat
some_str = 'Some "interested" ' + " text '666'"
print(some_str)
# string * (n)
print(some_str * 2)

# in operator examples
some_in = 'dda'
result = some_in in some_str
print(result)
print(' text' in some_str)

# symbol indexes
print(some_str[4])
print(some_str[-2])
# print from symbol 2 to symbol 14
print(some_str[2:14])

some_str2 = "H e l l o   w o r l d"
# print from symbol 0 to symbol 21 with step 2
print(some_str2[0:21:2])
text_example = "My name is Maxim, and I learning the PYTHON language"
print(text_example.upper())
print(text_example.lower())

# class 'int'
# class 'float'
# class 'complex'
