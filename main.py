import pygame

pygame.init()

screen_width = 640
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("オセロ")

# マス
square_num = 8
square_size = screen_width // square_num

#FPSの設定
FPS = 60
clock = pygame.time.Clock()

#色の設定
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

#盤面（黒：1、白：-1）
board = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, -1, 1, 0, 0, 0],
    [0, 0, 0, 1, -1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]]

#確認用
vec_table = [
    (-1, -1),   #左上
    (0, -1),    #上
    (1, -1),    #右上
    (-1, 0),    #左
    (1, 0),     #右
    (-1, 1),    #左下
    (0, 1),     #下
    (1, 1)]     #右下

player = 1  #プレイヤーを交代できるように


def get_valid_positions(): #石を置ける場所を探す
    valid_position_list = []
    for row in range(square_num):  #石を置いていないマスをチェック
        for col in range(square_num): 
            if board[row][col] == 0: #石を置いていない場合
                for vx, vy in vec_table: #周り確認 3x3のエリア
                    x = vx + col 
                    y = vy + row
                    if 0 <= x < square_num and 0 <= y < square_num and board[y][x] == -player: #範囲内か確認、周囲のマスが相手のもの
                        while True:   #異なる石があった場合、その方向を確認
                            x += vx
                            y += vy
                            if 0 <= x < square_num and 0 <= y < square_num and board[y][x] == -player:
                                continue #確認し続ける

                            elif 0 <= x < square_num and 0 <= y < square_num and board[y][x] == player: #同じ石があったら
                                valid_position_list.append((col, row)) #石を置ける場所を保存
                                break
                            else:   #自分、相手の石がない→枠外までいった場合は
                                break
    return valid_position_list #row,colともの全部のマスを見たら、


def flip_pieces(col, row):#石をひっくり返す
    for vx, vy in vec_table:
        flip_list = []
        x = vx + col
        y = vy + row
        while 0 <= x < square_num and 0 <= y < square_num and board[y][x] == -player:
            flip_list.append((x, y))
            x += vx
            y += vy
            if 0 <= x < square_num and 0 <= y < square_num and board[y][x] == player:
                for flip_x, flip_y in flip_list:
                    board[flip_y][flip_x] = player

def draw_grid():
    for i in range(square_num): #8x8で線を引く
        pygame.draw.line(screen, BLACK, (0, i * square_size), (screen_width, i * square_size), 2)#横
        pygame.draw.line(screen, BLACK, (i * square_size, 0), (i * square_size, screen_height), 2)#縦


def draw_board(): #リストを見て、書き出す
    for row_index, row in enumerate(board): #enumerateでボードの中身の取り出し
        for col_index, col in enumerate(row): #各行取り出し 8行取り出す
            if col == 1: #１なら黒を書く
                pygame.draw.circle(screen, BLACK, (col_index * square_size + 42, row_index * square_size + 42), 35)
            elif col == -1: #-１ならを白を書く
                pygame.draw.circle(screen, WHITE, (col_index * square_size + 42, row_index * square_size + 42), 35)

run = True

while(run):
    screen.fill(GREEN) 
    draw_grid()     #ボードの作成
    draw_board()    #石を置く
    valid_position_list = get_valid_positions()#どこに石を置けるのか取得

    for x, y in valid_position_list:
        pygame.draw.circle(screen, YELLOW, (x * square_size + 42, y * square_size + 42), 35, 3) #置けるところに目印

    if len (valid_position_list)<1:
        player *= -1 #置けるリストがないなら、相手の番へ



    for event in pygame.event.get():  #なにかされたら
        if event.type == pygame.QUIT: #×が押されたら消す
            run = False
        if event.type == pygame.KEYDOWN: #ESCで消す
            if event.key == pygame.K_ESCAPE:
                run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos() #マウスがどこにいるのか
            x = mx // square_size #マス目でどこにいるのか
            y = my // square_size
            if board[y][x] == 0 and (x, y) in valid_position_list:
                    #石をひっくり返す
                    flip_pieces(x, y)

                    board[y][x] = player
                    player *= -1
                    pass_num = 0

    pygame.display.update() #画面の更新
    clock.tick(FPS)    




