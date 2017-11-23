import json

A = iter([1, 2, 3, 4, 5, 6, 7])

def test(a):
    global A
    for i in a:
        if i == 3:
            yield i
            print('haha')
            # raise StopIteration
            A = []


def main():
    try:
        for i in test(A):
            print(i)
    except StopIteration:
        print('yes')

if __name__ == '__main__':
    main()
