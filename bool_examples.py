a = True
print(a)

print(type(a))
print(type(True))
print(type(False))

# cast to bool
empty = ''
print(bool(empty))
full = 'full'
print(bool(full))
print(bool(0))
print(bool(1))
print(bool(3.5))

# None type
print(type(None))
print(bool(None))
print(None == 0)

text = """
Meet my family. There are five of us – my parents, my elder brother, my baby sister and me. First, meet my mum and dad,
Jane and Michael. My mum enjoys reading and my dad enjoys playing chess with my brother Ken. My mum slim and is rather
tall. She has long red hair and big brown eyes. She has a very pleasant smile and a soft voice. My mother is very kind
and understanding. We are real friends. She is a housewife. As she has three children, she is always busy around the
house. She takes care of my baby sister Meg, who is only three months old. My sister is very small and funny. She sleeps
, eats and sometimes cries. We all help our mother and let her have a rest in the evening. Then she usually reads a book
 or just watches TV. My father is a doctor. He is tall and handsome. He has short dark hair and gray eyes. He is a very
hardworking man. He is rather strict with us, but always fair. My elder brother Ken is thirteen, and he is very clever
. He is good at Maths and always helps me with it, because I can hardly understand all these sums and problems.
Ken has red hair and brown eyes. My name is Jessica. I am eleven. I have long dark hair and brown eyes.
I am not as clever as my brother, though I try to do my best at school too. I am fond of dancing.
Our dancing studio won The Best Dancing Studio 2015 competition last month. I am very proud of it.
I also like to help my mother with my little sister very much. Our family is very united.
We love each other and always try to spend more time together.
"""
print(text)
words = text.split(' ')
print(sum("the" in line.lower() for line in words))

if 'First' in text:
    print('Yes')

# not recommended
if text[1] == 'M': print('1'); print(2); print(3)

# python ternary operator
age = 12
s = 'little' if age < 21 else 'high'
print(s)

if False:
    pass
print('hell0')
