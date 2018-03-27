from board.bit_board import BitBoard

class Test:
    pass

if __name__ == '__main__':
    b = BitBoard()
    print('init test')
    b.init_board('init/init.csv')
    print('display test')
    b.display_board()
    b.put_stone(2, 4, 1)
    for i in range(8):
        for j in range(8):
            print(b.get_liberty(i,j), end='')
        print('')
    b.display_board()
    print(b.count_stone(1))
    print(b.get_stone(2,4,1))
    for i in range(8):
        for j in range(8):
            print(b.get_liberty(i,j), end='')
        print('')
    b.put_stone(3, 5, 2)
    b.display_board()
    print(b.count_stone(1))
    print(b.get_stone(2,4,1))
    for i in range(8):
        for j in range(8):
            print(b.get_liberty(i,j), end='')
        print('')
