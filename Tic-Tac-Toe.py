import curses
import numpy as np
size = int(input('please input size: '))
board = []
for i in range(size):         #สร้าง board
  board.append(['-']*size)
boards = np.array(board)

curX = int(size/2)                 #ตำแหน่งcursorเมื่อเทียบกับ board  game
curY = int(size/2)                 #ตำแหน่งcursorเมื่อเทียบกับ board  game
def initGame() :              #ฟังก์ชั่นเอาไว้กำหนดค่าเริ่มต้นของเกม
  global sc,player
  sc = curses.initscr()       #กำหนดหน้าจอที่ใช้รันเกม
  sc.keypad(True)             #เปิ33ดการใช้งานลูกศรในkeyboard
  curses.curs_set(0)         #ปิดการแสดงผล cursor
def drawBoard() :
  for i in range(size): # row
    for j in range(size): # column
      sc.addch(i*2+1, j*4+1, boards[i][j])

  sc.addch(1+(curY*2), 1+(curX*4-1), '[')
  sc.addch(1+(curY*2), 1+(curX*4+1), ']')

def drawLabel() :
  global sc, player
  sc.addstr(size*2+3, 0,str(player) + ' turn.')
def putXY(y,x,player):
  boards[y][x] = player
def moveCur(key) :
  global curX, curY, sc, count
  sc.addch(1+(curY*2), 1+(curX*4-1), ' ') #print ช่องว่างแทนตำแหน่ง cursor เก่า
  sc.addch(1+(curY*2), 1+(curX*4+1), ' ') #print ช่องว่างแทนตำแหน่ง cursor เก่า
  if key == curses.KEY_LEFT and curX > 0:
      curX -= 1
  elif key == curses.KEY_RIGHT and curX < size-1:
      curX += 1
  elif key == curses.KEY_UP and curY > 0:
      curY -= 1
  elif key == curses.KEY_DOWN and curY < size-1:
      curY += 1
  elif key == 10: # Enter key
    putXY(curY,curX,player)
    count += 1
    #changeXY()
    #updateBoard(curY,curX)
def changeXY():
  global player, count
  if count%2 == 1:
    player = 'O'
  else:
    player = 'X'
def coreGame():
  global sc, player, count
  player = 'X'
  count = 0
  running = True
  win = False
  while running :
    sc.timeout(100) #กำหนดเวลาในกาารใช้รับค่า
    key = sc.getch() #รับค่าจากkeyboard
    if key == ord('q') : #กดqเพื่อออกจากเกม
      running = False
    if key != -1 : 
      moveCur(key)
      if winGame(player,boards) :
        running = False
        win = True
      changeXY()  
    drawBoard()
    drawLabel()
  sc.refresh()
  sc.clear()
  curses.endwin()
  if win :
    count += 1 
    changeXY()
    print(player + ' win')

def winGame(user, board):
  if check_row(user, board): return True
  if check_col(user, board): return True
  if check_diag(user, board): return True
  if check_backdiag(user, board): return True
  return False

def check_row(user, board):
  for row in board:
    complete_row = True
    for slot in row:
      if slot != user:
        complete_row = False
        break
    if complete_row: return True
  return False 

def check_col(user, board):
  for col in range(size):
    complete_col = True
    for row in range(size):
      if board[row][col] != user:
        complete_col = False
        break
    if complete_col: return True
  return False

def check_diag(user, board):
  #top right to bottom left
  global size
  for i in range(size):
    if board[i][size-i-1] != user:
      return False
  return True
def check_backdiag(user, board):
  #top left to bottom right
  global size
  for i in range(size):
    if board[i][i] != user:
      return False
  return True
initGame()
coreGame()
