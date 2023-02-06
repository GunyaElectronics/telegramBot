
def fetch(obj, idx):
    return obj[idx]


try:
    x = 'this is string'
    index = int(input('input index: '))
    fetch(x, index)
    if index == 3:
        raise IndexError
except IndexError:
    print('bad index')
