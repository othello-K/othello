from bit_board import BitBoard

if __name__ == '__main__':
    b = BitBoard()
    print('init test')
    b.init_board('init.csv')
    print('display test')
    b.display_board()
    b.put_stone(2, 4, 1)
    b.display_board()
    print(b.count_stone(1))
