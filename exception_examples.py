
def fetch(obj, idx):
    return obj[idx]


class MyException(Exception):
    pass


try:
    x = 'this is string'
    index = int(input('input index: '))
    fetch(x, index)
    if index == 3:
        raise ValueError
    elif index == 4:
        raise MyException
    ss = input('input some string')
    assert len(ss) < 10, 'to long object..'

except IndexError:
    print('bad index')
except ValueError:
    print('bad value')
except MyException:
    print('my exception')
except AssertionError as msg:
    print(f'assert {msg}')
else:
    print('else exception')
finally:
    print('finally code')
