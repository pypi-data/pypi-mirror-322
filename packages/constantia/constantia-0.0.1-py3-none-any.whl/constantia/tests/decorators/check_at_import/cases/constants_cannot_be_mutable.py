from constantia import consts


@consts(['x', 'y', 'z'], check_at='import')
def func():
    x = [1, 2, 3]
    y = 20
