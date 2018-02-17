if __name__ == '__main__':

    BOARD_INIT_FILE = 'init.csv'

    user1 = User(1)
    user2 = User(2)
    board = Board()
    board.read_board(BOARD_INIT_FILE)

# start game
    turn = 0
    while True:
        board.print_board()
        while True:

            print('input coordinate x')
            coorx = input('coor x:')
            if not( int(coorx) in [0,1,2] ):
                continue

            print('input coordinate x')
            coory = input('coor y:')
            if not( int(coory) in [0,1,2] ):
                continue

            coor = np.array([coorx, coory])
            if board.is_puttable(coor):
                break
            else:
                print("unable to put stone there")
        print(coor)

