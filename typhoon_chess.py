import sys
from typhoon_chess_gui import draw_chessboard

try:
     from typhoon import Typhoon
except ImportError:
     print("[ERROR] Nenasiel sa modul Typhoon.")
     print("[ERROR] Najdes ho na GitHube: https://github.com/tomas-sedlak/typhoon")
     sys.exit(0)

try:
     import chess
     import chess.engine
except ImportError:
     print("[ERROR] Nemas nainstalovanu kniznicu chess.")
     print("[ERROR] Nainstalujes ju pomocou: pip install chess")
     sys.exit(0)

typhoon = Typhoon("COM10")

engine_path = r"./stockfish/stockfish.exe"
engine = chess.engine.SimpleEngine.popen_uci(engine_path)
engine.configure({"Skill level": 1})
limit = chess.engine.Limit(time=1)

board = chess.Board()
draw_chessboard(board)

def player_move(old_board, new_board):
    move_from, move_to = "", ""
    hrac_urobil_tah = 0

    for row in range(8):
        for col in range(8):
            if old_board[row][col] != new_board[row][col]:
                if new_board[row][col] == 0:
                    hrac_urobil_tah = 1
                    move_from = chr(col + 97) + str(8 - row)
                else:
                    move_to = chr(col + 97) + str(8 - row)

    move = chess.Move.from_uci(move_from + move_to)
    if hrac_urobil_tah == 1:
        print('Hrac:', move)

    return move


def typhoon_move(engine_move):
    col_from = ord(engine_move[0]) - 96
    row_from = int(engine_move[1])
    col_to = ord(engine_move[2]) - 96
    row_to = int(engine_move[3])
    typhoon.send(-50 + row_from * 40, -120 + col_from * 40, 0)
    typhoon.send(-50 + row_to * 40, -120 + col_to * 40, 0)


def get_outcome():
    winner = board.outcome().winner
    if winner == chess.WHITE:
        print("White won!")
    elif winner == chess.BLACK:
        print("Black won!")
    else:
        print("Draw!")

while not board.is_game_over():
    turn = board.turn
    # if turn == chess.WHITE:
    #     move = chess.Move.from_uci(input("Tvoj tah: "))
    #     board.push(move)
    #     draw_chessboard(board)
    # elif turn == chess.BLACK:
    #     engine_move = engine.play(board, limit).move
    #     board.push(engine_move)
    #     print(board.uci(engine_move))
    #     typhoon_move(board.uci(engine_move))
    #     draw_chessboard(board)

    engine_move = engine.play(board, limit).move
    board.push(engine_move)
    draw_chessboard(board)
    typhoon_move(board.uci(engine_move))

get_outcome()
engine.quit()





















# #Funkcie na sachovnici 4.5.2024
# import math,time,sys,struct,serial,tkinter,random,chess,chess.engine
# #from stockfish import Stockfish
# #stockfish=Stockfish(path="stockfish_d\stockfish-windows-x86-64-sse41-popcnt")
# #stockfish=Stockfish(path="stockfish\stockfish-windows-x86-64-avx2.exe")
# engine = chess.engine.SimpleEngine.popen_uci(r"/home/pi/Stockfish-sf_15/src/stockfish")

# class Typhoon():
    
#     def __init__(self):
# #**************** funkcie sachovnice *********************************************************************************************
#         sp,vp=800,800
#         pl=tkinter.Canvas(bg='navy',width=sp,height=vp)
#         pl.pack()
#         vx,x0,sy,y0=40,280,40,140#polia sachovnice robota - vyska,zaciatok x,sirka,zaciatok y
#         hore,dole,pw8,pw9,pw10=0,-50,0,90,0
#         so,vo=70,70 #rozmery poli sachovnice pre zobrazovanie
#         ys=(vp-8*vo)/2
#         #polia pre poziciu figurok na sachovnici
#         obr = []
#         for i in range(9):
#             riadky = []
#             for j in range(9):
#                 riadky.append('')
#             obr.append(riadky)
#         s_f = []
#         for i in range(9):
#             riadky = []
#             for j in range(9):
#                 riadky.append('')
#             s_f.append(riadky)
#         stara_p = []
#         for i in range(9):
#             riadky = []
#             for j in range(9):
#                 riadky.append(0)
#             stara_p.append(riadky)
#         nova_p = []
#         for i in range(9):
#             riadky = []
#             for j in range(9):
#                 riadky.append(0)
#             nova_p.append(riadky)
#         bo = []
#         for i in range(9):
#             riadky = []
#             for j in range(9):
#                 riadky.append('')
#             bo.append(riadky)

#         s_f[1][1],s_f[1][2],s_f[1][3],s_f[1][4],s_f[1][5],s_f[1][6],s_f[1][7],s_f[1][8]='BV','BK','BS','BD','BKR','BS','BK','BV'
#         s_f[2][1],s_f[2][2],s_f[2][3],s_f[2][4],s_f[2][5],s_f[2][6],s_f[2][7],s_f[2][8]='BP','BP','BP','BP','BP','BP','BP','BP'

#         s_f[8][1],s_f[8][2],s_f[8][3],s_f[8][4],s_f[8][5],s_f[8][6],s_f[8][7],s_f[8][8]='ČV','ČK','ČS','ČKR','ČD','ČS','ČK','ČV'
#         s_f[7][1],s_f[7][2],s_f[7][3],s_f[7][4],s_f[7][5],s_f[7][6],s_f[7][7],s_f[7][8]='ČP','ČP','ČP','ČP','ČP','ČP','ČP','ČP'

#         obr[1][1] = obr[1][8] = tkinter.PhotoImage(file='bv.png')
#         obr[1][2] = obr[1][7] = tkinter.PhotoImage(file='bk.png')
#         obr[1][3] = obr[1][6] = tkinter.PhotoImage(file='bs.png')
#         obr[1][4] = tkinter.PhotoImage(file='bd.png')
#         obr[1][5] = tkinter.PhotoImage(file='bkr.png')
#         obr[2][1]=obr[2][2]=obr[2][3]=obr[2][4]=obr[2][5]=obr[2][6]=obr[2][7]=obr[2][8]=tkinter.PhotoImage(file='bp.png')

#         obr[8][1]=obr[8][8] = tkinter.PhotoImage(file='cv.png')
#         obr[8][2]=obr[8][7] = tkinter.PhotoImage(file='ck.png')
#         obr[8][3]=obr[8][6] = tkinter.PhotoImage(file='cs.png')
#         obr[8][4] = tkinter.PhotoImage(file='cd.png')
#         obr[8][5] = tkinter.PhotoImage(file='ckr.png')
#         obr[7][1]=obr[7][2]=obr[7][3]=obr[7][4]=obr[7][5]=obr[7][6]=obr[7][7]=obr[7][8]=tkinter.PhotoImage(file='cp.png')

#         bo[1][1] = bo[1][8] = 'R'
#         bo[1][2] = bo[1][7] = 'N'
#         bo[1][3] = bo[1][6] = 'B'
#         bo[1][4] = 'Q'
#         bo[1][5] = 'K'
#         bo[2][1]=bo[2][2]=bo[2][3]=bo[2][4]=bo[2][5]=bo[2][6]=bo[2][7]=bo[2][8]='P'

#         bo[8][1]=bo[8][8] = 'r'
#         bo[8][2]=bo[8][7] = 'n'
#         bo[8][3]=bo[8][6] = 'b'
#         bo[8][4] = 'q'
#         bo[8][5] = 'k'
#         bo[7][1]=bo[7][2]=bo[7][3]=bo[7][4]=bo[7][5]=bo[7][6]=bo[7][7]=bo[7][8]='p'

#         f1,f2='brown','white'
#         for r in range(1,9):
#             f1,f2=f2,f1
#             xs=sp/2-4*so
#             for s in range(1,9):
#                 pl.create_rectangle(xs,ys,xs+so,ys+vo,fill=f1)
#                 pl.create_image(xs+so/2,ys+vo/2,image=obr[9-r][s])
#                 xs+=so
#                 f1,f2=f2,f1
#             ys+=vo

#         def testuj_sachovnicu(s_f):
#             xs=sp/2-4*so
#             ys=(vp-8*vo)/2+8*vo
#             for r in range(1,9):
#                 for p in range(1,9):
#                     s=chr(64+p)
#                     #x=194-(r-1)*vx
#                     x=x0-(r-1)*vx
#                     y=y0-(ord(s)-65)*sy
#                     cs,cr=(ord(s)-65)*so,r*vo
#                     Posli_x_y_z_pw(x,y,0,pw8,pw9,pw10)#x,y,z,pw8,pw9,pw10
#                     #time.sleep(1)
#                     Posli_x_y_z_pw(x,y,dole,pw8,pw9,pw10)
#                     #time.sleep(1)
#                     Posli_x_y_z_pw(x,y,0,pw8,pw9,pw10)
#                     #time.sleep(1)
#                     pl.create_rectangle(xs+cs,ys-cr+vo,xs+cs+so,ys-cr,fill='green')
#                     pl.create_text(xs+cs+so/2,ys-cr+vo-10,text=s+str(r)+' '+str(x)+' '+str(y),fill='yellow',font=('arial',8,'bold'))
#                     #pl.create_text(xs+cs+so/2,ys-cr+vo-vo/2,fill='yellow',text=s_f[r][p],font=('arial',10,'bold'))
#                     pl.create_image(xs+cs+so/2,ys-cr+vo-vo/2,image=obr[r][p])
#                     pl.update()
#             pl.create_oval(sp/2-10,0,sp/2+10,20,fill='aqua')
#             pl.create_text(sp/2,30,text='x=0 y=0',fill='aqua')
#             pl.update()
#             Posli_x_y_z_pw(0,0,0,0,90,0)

#         def urob_tah(tah,s_f,kto_tahal):
#             tah=tah.split()
#             xs=sp/2-4*so
#             ys=(vp-8*vo)/2+8*vo
#             #treba odstranit figurku hraca z pola (urobi robot)
#             if kto_tahal=='R':
#                 co=tah[0]
#                 r=int(co[1])
#                 s=co[0]
#                 if ord(s)>90:s=chr(ord(s)-32)
#                 cs,cr=(ord(s)-65)*so,r*vo #suradnice pola na sachovnici
#                 pl.create_rectangle(xs+cs+3,ys-cr+vo-3,xs+cs+so-3,ys-cr+3,outline='yellow',width=5)
#                 co=tah[1]
#                 r=int(co[1])
#                 s=co[0]
#                 if ord(s)>90:s=chr(ord(s)-32)
#                 #x=194-(r-1)*vx
#                 x=x0-(r-1)*vx
#                 y=y0-(ord(s)-65)*sy
#                 cs,cr=(ord(s)-65)*so,r*vo #suradnice pola na sachovnici
#                 if obr[r][ord(s)-64]!='':
#                         print(tah[1],'Treba vyhodit!')
#                         pl.create_rectangle(xs+cs+3,ys-cr+vo-3,xs+cs+so-3,ys-cr+3,fill='red',outline='yellow',width=5)
#                         pl.update()
#                         Posli_x_y_z_pw(x,y,0,0,90,pw10)#x,y,z,pw8,pw9,pw10
#                         time.sleep(2)
#                         Posli_x_y_z_pw(x,y,dole,255,90,pw10)
#                         time.sleep(2)
#                         Posli_x_y_z_pw(x,y,0,255,90,pw10)
#                         time.sleep(2)
#                         Posli_x_y_z_pw(100,180,0,255,90,pw10)
#                         Posli_x_y_z_pw(100,180,0,0,130,pw10)
#                         time.sleep(2)
#                         Posli_x_y_z_pw(0,0,0,0,90,pw10)
                        

#             for i in range(2):
#                 co=tah[i]
#                 r=int(co[1])
#                 s=co[0]
#                 if ord(s)>90:s=chr(ord(s)-32)
#                 #x=194-(r-1)*vx
#                 x=x0-(r-1)*vx
#                 y=y0-(ord(s)-65)*sy
#                 cs,cr=(ord(s)-65)*so,r*vo #suradnice pola na sachovnici
#                 if i==0:
#                     #z ktoreho pola
#                     pl.create_rectangle(xs+cs+3,ys-cr+vo-3,xs+cs+so-3,ys-cr+3,outline='yellow',width=5)
#                     pl.update()
#                     time.sleep(2)
#                     if kto_tahal=='R':
#                         Posli_x_y_z_pw(x,y,0,0,90,pw10)#x,y,z,pw8,pw9,pw10
#                         time.sleep(2)
#                         Posli_x_y_z_pw(x,y,dole,255,90,pw10)
#                         time.sleep(2)
#                         Posli_x_y_z_pw(x,y,0,255,90,pw10)
#                     if r%2==1 and (ord(s)-64)%2==1:f='brown'
#                     elif r%2==0 and (ord(s)-64)%2==0:f='brown'
#                     else:f='white'
#                     figurka=obr[r][ord(s)-64]
#                     fig=bo[r][ord(s)-64]
#                     obr[r][ord(s)-64]=''
#                     bo[r][ord(s)-64]=''
#                     pl.create_rectangle(xs+cs,ys-cr+vo,xs+cs+so,ys-cr,fill=f)
#                 if i==1:
#                     #na ktore pole
#                     pl.create_rectangle(xs+cs+3,ys-cr+vo-3,xs+cs+so-3,ys-cr+3,outline='yellow',width=5)
#                     pl.update()
#                     if kto_tahal=='H':time.sleep(2)
#                     obr[r][ord(s)-64]=figurka
#                     bo[r][ord(s)-64]=fig
#                     if r%2==1 and (ord(s)-64)%2==1:f='brown'
#                     elif r%2==0 and (ord(s)-64)%2==0:f='brown'
#                     else:f='white'
#                     pl.create_rectangle(xs+cs,ys-cr+vo,xs+cs+so,ys-cr,fill=f)
#                     pl.create_image(xs+cs+so/2,ys-cr+vo-vo/2,image=figurka)
#                     if kto_tahal=='R':
#                         Posli_x_y_z_pw(x,y,0,255,90,pw10)#x,y,z,pw8,pw9,pw10
#                         time.sleep(2)
#                         Posli_x_y_z_pw(x,y,dole,0,90,pw10)
#                         time.sleep(2)
#                         Posli_x_y_z_pw(x,y,dole,0,130,pw10)
#                         time.sleep(2)
#                         Posli_x_y_z_pw(x,y,0,0,130,pw10)
#                     pl.update()
#             if kto_tahal=='R':
#                 Posli_x_y_z_pw(0,0,0,0,90,0)

#         def pozicia_figurok(pole):
#             #Ak je na sachovnici figurka pole[cr][cs]=1 a naopak. Vyhodnotenie pomocou fototranzistora.
#             #Ak nie je nad fototranzistorom figurka, fototranzistor vedie prud: - if GPIO.input(s[cs])==1:pole[cr][cs]=0
#                                                                             # - else:pole[cr][cs]=1
#             import RPi.GPIO as GPIO
#             r,s=[0]*9,[0]*9
#             s[1],s[2],s[3],s[4],s[5],s[6],s[7],s[8] = 27,4,5,6,7,8,9,10
#             r[1],r[2],r[3],r[4],r[5],r[6],r[7],r[8] = 22,19,20,21,23,24,25,26
#             GPIO.setmode(GPIO.BCM)
#             for i in range(8,0,-1):GPIO.setup(s[i],GPIO.IN)
#             for i in range(8,0,-1):GPIO.setup(r[i], GPIO.OUT)
#             for cr in range(1,9):
#                 GPIO.output(r[cr],1)
#                 for cs in range(1,9):
#                     if GPIO.input(s[cs])==1:
#                         pole[cr][cs]=0
#                     else:pole[cr][cs]=1
#                 GPIO.output(r[cr],0)
#             GPIO.cleanup()

#         def vytvor_board(bo):
#             global board
#             fig_na_board=''
#             for r in range(1,9):
#                 poc=0
#                 for s in range(1,9):
#                 if bo[9-r][s]!='' and poc==0: fig_na_board+=bo[9-r][s]
#                 if bo[9-r][s]=='':
#                     poc+=1
#                 else:
#                     if poc>0:
#                         fig_na_board+=str(poc)
#                         fig_na_board+=bo[9-r][s]
#                         poc=0
#                 if poc>0: fig_na_board+=str(poc)
#                 if r<8:fig_na_board+='/'
#                 if r==8:fig_na_board+=' b KQkq - 0 4'
#             print(fig_na_board)
#             #stockfish.set_fen_position(fig_na_board)
#             board=chess.Board(fig_na_board)
#             print(board)
#             print(100)

#         def tah_hraca(s_f,stara_p,nova_p):
#             #porovnanim poli stara_p a nova_p zistima tah na sachovnici
#             #pozicia_figurok(stara_p)
#             tah_z,tah_na='0','0'
#             hrac_urobil_tah=0
#             stara_p[2][1]=1#*******
#             #print(stara_p)
#             th=0
#             th=pl.create_text(sp/2,vp/2-4*vo-15,fill='yellow',text='Ťah hráča',font=('arial',15,'bold'))
#             pl.update()
#             time.sleep(1)#caka sa na tah hraca na sachovnici
#             #pozicia_figurok(nova_p)
#             nova_p[2][1]=0#******* z B1
#             nova_p[3][3]=1#******* na C3
#             #print('\n',nova_p)
#             for r in range(1,9):
#                 for s in range(1,9):
#                     if nova_p[r][s]!=stara_p[r][s]:
#                         if nova_p[r][s]==0:
#                             hrac_urobil_tah=1
#                             tah_z=chr(r+64)+str(s)
#                         else:tah_na=chr(r+64)+str(s)
#             tah_hraca=tah_z+' '+tah_na
#             if hrac_urobil_tah==1:
#                 tah_hraca=input('Urob tah napr:B1 C3:')#Toto ja manualny tah hraca bez elektronickej sachovnice
#                 print('Hrac:',tah_hraca)
#                 urob_tah(tah_hraca,s_f,'H')#zobrazi tah hraca
#                 vytvor_board(bo)
#             pl.delete(th)
#             #Ak rosada hrac_urobil_tah=0
#             return hrac_urobil_tah

#         def tah_robota(s_f):
#             tr=0
#             tr=pl.create_text(sp/2,vp/2-4*vo-15,fill='yellow',text='Ťah robota',font=('arial',15,'bold'))
#             tah=chr(random.randrange(65,73))+str(random.randrange(7,9))+' '+chr(random.randrange(65,73))+str(random.randrange(1,7))
            
#             bestmove=str(engine.play(board, chess.engine.Limit(time=0.1)).move).upper()
#             print(str(bestmove[0:2] +" "+ bestmove[2:4]))
#             tah=str(bestmove[0:2] +" "+ bestmove[2:4])
#             urob_tah(tah,s_f,'R')
#             print('Robot:',tah)
#             vytvor_board(bo)
#             pl.delete(tr)
            
        
#         print('Test šachovnice ..... t\nHrať šach ........... s')
#         if input()=='t':
#             testuj_sachovnicu(s_f)
#         else:
#             while True:
#                 urobil=0
#                 urobil=tah_hraca(s_f,stara_p,nova_p)
#                 if urobil==1:tah_robota(s_f)
# #*************************************************************************************************************
# Typhoon()
