#Funkcie na sachovnici 9.4.2024
import math,time,sys,struct,serial,tkinter,random,chess

class Typhoon():
    
    def __init__(self, parent=None):   
        try:
            self.arduinoSerial = serial.Serial('COM7', 115200)#/dev/ttyACM0 raspberry pi
            time.sleep(1.5)
            self.arduinoSerial.flushInput()
        except Exception as e:
            self.show_a_warning_message_box('Unknown error connecting to the arduino serial port. Code error shown below:',
                                            repr(e),'Arduino Serial Connection Error')      
#************************************** send data for Arduino ****************************************************************************************
        lengthUpperArm = 215
        lengthLowerArm = 250
        distanceTool = 110
        distanceZ=0
        heightFromGround = 25
        lengthUpperSquared = pow(lengthUpperArm, 2)
        lengthLowerSquared = pow(lengthLowerArm, 2)
        piHalf = math.pi / 2.0
        piTwo = math.pi * 2.0
        piThreeFourths = math.pi * 3.0 / 4.0

        def anglesFromCoordinates( x, y, z):
            x+=distanceTool
            z+=distanceZ            
            radius = math.sqrt(pow(x, 2) + pow(y, 2))
            radius=math.sqrt(radius**2+(heightFromGround)**2)
            print('***************** radius: ',radius,'*******************')
            baseAngle = math.atan2(y,radius+45)
            actualZ = - heightFromGround
            hypotenuseSquared = pow(actualZ, 2) + pow(radius, 2)
            hypotenuse = math.sqrt(hypotenuseSquared)	
            q1 = math.atan2(actualZ+z, radius)	
            q2 = math.acos((lengthUpperSquared - lengthLowerSquared + hypotenuseSquared) / (2 * lengthUpperArm * hypotenuse))
            upperAngle = piHalf - (q1 + q2)	
            lowerAngle = piHalf - (math.acos((lengthUpperSquared + lengthLowerSquared -
                         hypotenuseSquared) / (2.0 * lengthUpperArm * lengthLowerArm))- upperAngle)	
            return baseAngle*180.0/math.pi,-upperAngle*180.0/math.pi+9.120851906137954,71.64548899867737-lowerAngle*180.0/math.pi            
        def Posli_x_y_z_pw(x,y,z,pw8,ow9,pw10):
            #print('Data pre Typhoon')
            moveToX=x
            moveToY=y
            moveToZ=z
            powerD8=float(pw8)#0 ... 255
            powerD9=float(pw9)#0 ... 255
            powerD10=float(pw10)#0 ... 255
            moveToXFloat = float(moveToX)
            moveToYFloat = float(moveToY)
            moveToZFloat = float(moveToZ)
            base_angle,upper_angle,lover_angle = anglesFromCoordinates(moveToXFloat, moveToYFloat, moveToZFloat)
            #Poslat data do typhonu
            self.arduinoSerial.write( struct.pack('f',base_angle*0.93) )
            self.arduinoSerial.write( struct.pack('f',lover_angle) )
            self.arduinoSerial.write( struct.pack('f',upper_angle*0.93) )
            self.arduinoSerial.write( struct.pack('f',powerD8)) #hodnota pre nastroj v D8
            self.arduinoSerial.write( struct.pack('f',powerD9)) #hodnota pre nastroj v D9
            self.arduinoSerial.write( struct.pack('f',powerD10))#hodnota pre nastroj v D10

            for i in range(0,9):#podla poctu Serial.println v firmware-arduino
                print ( '>>',self.arduinoSerial.readline() )             
#**************** funkcie sachovnice *********************************************************************************************       
        sp,vp=800,800
        pl=tkinter.Canvas(bg='navy',width=sp,height=vp)
        pl.pack()    
        vx,x0,sy,y0=40,325,40,140#polia sachovnice robota - vyska,zaciatok x,sirka,zaciatok y
        hore,dole,pw8,pw9,pw10=20,-20,0,0,0
        so,vo=70,70 #rozmery poli sachovnice pre zobrazovanie
        ys=(vp-8*vo)/2
        #polia pre poziciu figurok na sachovnici
        obr = []       
        for i in range(9):
            riadky = []
            for j in range(9):
                riadky.append('')
            obr.append(riadky)
        s_f = []       
        for i in range(9):
            riadky = []
            for j in range(9):
                riadky.append('')
            s_f.append(riadky)
        stara_p = []       
        for i in range(9):
            riadky = []
            for j in range(9):
                riadky.append(0)
            stara_p.append(riadky)
        nova_p = []       
        for i in range(9):
            riadky = []
            for j in range(9):
                riadky.append(0)
            nova_p.append(riadky)   
        bo = []       
        for i in range(9):
            riadky = []
            for j in range(9):
                riadky.append('')
            bo.append(riadky)   
        
        s_f[1][1],s_f[1][2],s_f[1][3],s_f[1][4],s_f[1][5],s_f[1][6],s_f[1][7],s_f[1][8]='BV','BK','BS','BD','BKR','BS','BK','BV'
        s_f[2][1],s_f[2][2],s_f[2][3],s_f[2][4],s_f[2][5],s_f[2][6],s_f[2][7],s_f[2][8]='BP','BP','BP','BP','BP','BP','BP','BP'

        s_f[8][1],s_f[8][2],s_f[8][3],s_f[8][4],s_f[8][5],s_f[8][6],s_f[8][7],s_f[8][8]='ČV','ČK','ČS','ČKR','ČD','ČS','ČK','ČV'
        s_f[7][1],s_f[7][2],s_f[7][3],s_f[7][4],s_f[7][5],s_f[7][6],s_f[7][7],s_f[7][8]='ČP','ČP','ČP','ČP','ČP','ČP','ČP','ČP'

        obr[1][1] = obr[1][8] = tkinter.PhotoImage(file='bv.png')
        obr[1][2] = obr[1][7] = tkinter.PhotoImage(file='bk.png')
        obr[1][3] = obr[1][6] = tkinter.PhotoImage(file='bs.png')
        obr[1][4] = tkinter.PhotoImage(file='bd.png')
        obr[1][5] = tkinter.PhotoImage(file='bkr.png')       
        obr[2][1]=obr[2][2]=obr[2][3]=obr[2][4]=obr[2][5]=obr[2][6]=obr[2][7]=obr[2][8]=tkinter.PhotoImage(file='bp.png')
        
        obr[8][1]=obr[8][8] = tkinter.PhotoImage(file='cv.png')
        obr[8][2]=obr[8][7] = tkinter.PhotoImage(file='ck.png')
        obr[8][3]=obr[8][6] = tkinter.PhotoImage(file='cs.png')
        obr[8][4] = tkinter.PhotoImage(file='cd.png')
        obr[8][5] = tkinter.PhotoImage(file='ckr.png')
        obr[7][1]=obr[7][2]=obr[7][3]=obr[7][4]=obr[7][5]=obr[7][6]=obr[7][7]=obr[7][8]=tkinter.PhotoImage(file='cp.png')

        bo[1][1] = bo[1][8] = 'R'
        bo[1][2] = bo[1][7] = 'N'
        bo[1][3] = bo[1][6] = 'B'
        bo[1][4] = 'Q'
        bo[1][5] = 'K'    
        bo[2][1]=bo[2][2]=bo[2][3]=bo[2][4]=bo[2][5]=bo[2][6]=bo[2][7]=bo[2][8]='P'
        
        bo[8][1]=bo[8][8] = 'r'
        bo[8][2]=bo[8][7] = 'n'
        bo[8][3]=bo[8][6] = 'b'
        bo[8][4] = 'q'
        bo[8][5] = 'k'
        bo[7][1]=bo[7][2]=bo[7][3]=bo[7][4]=bo[7][5]=bo[7][6]=bo[7][7]=bo[7][8]='p'
        
        f1,f2='brown','white'
        for r in range(1,9):
            f1,f2=f2,f1
            xs=sp/2-4*so
            for s in range(1,9):
                pl.create_rectangle(xs,ys,xs+so,ys+vo,fill=f1)
                pl.create_image(xs+so/2,ys+vo/2,image=obr[9-r][s])
                xs+=so
                f1,f2=f2,f1
            ys+=vo
            
        def testuj_sachovnicu(s_f):
            xs=sp/2-4*so
            ys=(vp-8*vo)/2+8*vo 
            for r in range(1,9):
                for p in range(1,9):
                    s=chr(64+p)
                    #x=194-(r-1)*vx
                    x=x0-(r-1)*vx
                    y=y0-(ord(s)-65)*sy                   
                    cs,cr=(ord(s)-65)*so,r*vo                                       
                    Posli_x_y_z_pw(x,y,hore,pw8,pw9,pw10)#x,y,z,pw8,pw9,pw10
                    Posli_x_y_z_pw(x,y,dole,pw8,pw9,pw10)
                    Posli_x_y_z_pw(x,y,hore,pw8,pw9,pw10)                 
                    pl.create_rectangle(xs+cs,ys-cr+vo,xs+cs+so,ys-cr,fill='green')                   
                    pl.create_text(xs+cs+so/2,ys-cr+vo-10,text=s+str(r)+' '+str(x)+' '+str(y),fill='yellow',font=('arial',8,'bold'))                   
                    #pl.create_text(xs+cs+so/2,ys-cr+vo-vo/2,fill='yellow',text=s_f[r][p],font=('arial',10,'bold'))
                    pl.create_image(xs+cs+so/2,ys-cr+vo-vo/2,image=obr[r][p])
                    pl.update()          
            pl.create_oval(sp/2-10,0,sp/2+10,20,fill='aqua')
            pl.create_text(sp/2,30,text='x=0 y=0',fill='aqua')
            pl.update()              
            Posli_x_y_z_pw(0,0,0,0,0,0)
            
        def urob_tah(tah,s_f,kto_tahal):          
            tah=tah.split()
            xs=sp/2-4*so
            ys=(vp-8*vo)/2+8*vo
            #treba odstranit figurku hraca z pola (urobi robot)
            if kto_tahal=='R':
                co=tah[0]
                r=int(co[1])
                s=co[0]              
                if ord(s)>90:s=chr(ord(s)-32)
                cs,cr=(ord(s)-65)*so,r*vo #suradnice pola na sachovnici
                pl.create_rectangle(xs+cs+3,ys-cr+vo-3,xs+cs+so-3,ys-cr+3,outline='yellow',width=5)
                co=tah[1]
                r=int(co[1])
                s=co[0]              
                if ord(s)>90:s=chr(ord(s)-32)
                #x=194-(r-1)*vx
                x=x0-(r-1)*vx
                y=y0-(ord(s)-65)*sy
                cs,cr=(ord(s)-65)*so,r*vo #suradnice pola na sachovnici
                if obr[r][ord(s)-64]!='':
                        print(tah[1],'Treba vyhodit!')
                        pl.create_rectangle(xs+cs+3,ys-cr+vo-3,xs+cs+so-3,ys-cr+3,fill='red',outline='yellow',width=5)
                        pl.update()
                        Posli_x_y_z_pw(x,y,60,0,pw9,pw10)#x,y,z,pw8,pw9,pw10
                        Posli_x_y_z_pw(x,y,dole,255,pw9,pw10)
                        time.sleep(2)
                        Posli_x_y_z_pw(x,y,60,255,pw9,pw10)
                        Posli_x_y_z_pw(0,270,60,255,pw9,pw10)
                        Posli_x_y_z_pw(0,270,dole,0,pw9,pw10)
                        time.sleep(1)
                        Posli_x_y_z_pw(0,270,60,0,pw9,pw10)
                        Posli_x_y_z_pw(0,0,0,0,pw9,pw10)
                                    
            for i in range(2):
                co=tah[i]
                r=int(co[1])
                s=co[0]              
                if ord(s)>90:s=chr(ord(s)-32)
                x=194-(r-1)*vx
                y=y0-(ord(s)-65)*sy
                cs,cr=(ord(s)-65)*so,r*vo #suradnice pola na sachovnici
                if i==0:
                    #z ktoreho pola
                    pl.create_rectangle(xs+cs+3,ys-cr+vo-3,xs+cs+so-3,ys-cr+3,outline='yellow',width=5)
                    pl.update()
                    time.sleep(2)
                    if kto_tahal=='R':
                        Posli_x_y_z_pw(x,y,20,0,pw9,pw10)#x,y,z,pw8,pw9,pw10
                        Posli_x_y_z_pw(x,y,dole,255,pw9,pw10)
                        time.sleep(2)
                        Posli_x_y_z_pw(x,y,20,255,pw9,pw10)
                    if r%2==1 and (ord(s)-64)%2==1:f='brown'
                    elif r%2==0 and (ord(s)-64)%2==0:f='brown'
                    else:f='white'
                    figurka=obr[r][ord(s)-64]
                    fig=bo[r][ord(s)-64]
                    obr[r][ord(s)-64]=''
                    bo[r][ord(s)-64]=''
                    pl.create_rectangle(xs+cs,ys-cr+vo,xs+cs+so,ys-cr,fill=f)
                if i==1:
                    #na ktore pole
                    pl.create_rectangle(xs+cs+3,ys-cr+vo-3,xs+cs+so-3,ys-cr+3,outline='yellow',width=5)
                    pl.update()
                    if kto_tahal=='H':time.sleep(2)                  
                    obr[r][ord(s)-64]=figurka
                    bo[r][ord(s)-64]=fig
                    if r%2==1 and (ord(s)-64)%2==1:f='brown'
                    elif r%2==0 and (ord(s)-64)%2==0:f='brown'
                    else:f='white'
                    pl.create_rectangle(xs+cs,ys-cr+vo,xs+cs+so,ys-cr,fill=f)
                    pl.create_image(xs+cs+so/2,ys-cr+vo-vo/2,image=figurka)
                    if kto_tahal=='R':
                        Posli_x_y_z_pw(x,y,60,255,pw9,pw10)#x,y,z,pw8,pw9,pw10
                        Posli_x_y_z_pw(x,y,dole,0,pw9,pw10)
                        time.sleep(2)
                        Posli_x_y_z_pw(x,y,60,0,pw9,pw10)
                    pl.update()  
            if kto_tahal=='R':
                Posli_x_y_z_pw(0,0,0,0,0,0)
            
        def pozicia_figurok(pole):
            #Ak je na sachovnici figurka pole[cr][cs]=1 a naopak. Vyhodnotenie pomocou fototranzistora.
            #Ak nie je nad fototranzistorom figurka, fototranzistor vedie prud: - if GPIO.input(s[cs])==1:pole[cr][cs]=0
                                                                              # - else:pole[cr][cs]=1
            import RPi.GPIO as GPIO            
            r,s=[0]*9,[0]*9
            s[1],s[2],s[3],s[4],s[5],s[6],s[7],s[8] = 27,4,5,6,7,8,9,10
            r[1],r[2],r[3],r[4],r[5],r[6],r[7],r[8] = 22,19,20,21,23,24,25,26
            GPIO.setmode(GPIO.BCM)
            for i in range(8,0,-1):GPIO.setup(s[i],GPIO.IN)
            for i in range(8,0,-1):GPIO.setup(r[i], GPIO.OUT)
            for cr in range(1,9):
                GPIO.output(r[cr],1)
                for cs in range(1,9):
                    if GPIO.input(s[cs])==1:
                        pole[cr][cs]=0
                    else:pole[cr][cs]=1
                GPIO.output(r[cr],0)
            GPIO.cleanup()
            
        def vytvor_board(bo):
            fig_na_board=''
            for r in range(1,9):
                poc=0
                for s in range(1,9):
                   if bo[9-r][s]!='' and poc==0: fig_na_board+=bo[9-r][s]
                   if bo[9-r][s]=='':
                       poc+=1
                   else:
                       if poc>0:
                           fig_na_board+=str(poc)
                           fig_na_board+=bo[9-r][s]                          
                           poc=0
                if poc>0: fig_na_board+=str(poc)                                                   
                if r<8:fig_na_board+='/'
                if r==8:fig_na_board+=' b KQkq - 0 4'
            print(fig_na_board)            
            board=chess.Board(fig_na_board)           
            print(board)
            
        def tah_hraca(s_f,stara_p,nova_p):
            #porovnanim poli stara_p a nova_p zistima tah na sachovnici
            #pozicia_figurok(stara_p)
            tah_z,tah_na='0','0'
            hrac_urobil_tah=0
            stara_p[2][1]=1#*******           
            #print(stara_p)
            th=0
            th=pl.create_text(sp/2,vp/2-4*vo-15,fill='yellow',text='Ťah hráča',font=('arial',15,'bold'))
            pl.update()
            time.sleep(1)#caka sa na tah hraca na sachovnici            
            #pozicia_figurok(nova_p)
            nova_p[2][1]=0#******* z B1
            nova_p[3][3]=1#******* na C3
            #print('\n',nova_p)
            for r in range(1,9):
                for s in range(1,9):
                    if nova_p[r][s]!=stara_p[r][s]:                       
                        if nova_p[r][s]==0:
                            hrac_urobil_tah=1
                            tah_z=chr(r+64)+str(s)
                        else:tah_na=chr(r+64)+str(s)
            tah_hraca=tah_z+' '+tah_na
            if hrac_urobil_tah==1:
                tah_hraca=input('Urob tah napr:B1 C3:')#Toto ja manualny tah hraca bez elektronickej sachovnice
                print('Hrac:',tah_hraca)    
                urob_tah(tah_hraca,s_f,'H')#zobrazi tah hraca 
                vytvor_board(bo)
            pl.delete(th)  
            return hrac_urobil_tah
            
        def tah_robota(s_f):
            tr=0
            tr=pl.create_text(sp/2,vp/2-4*vo-15,fill='yellow',text='Ťah robota',font=('arial',15,'bold'))
            tah=chr(random.randrange(65,73))+str(random.randrange(7,9))+' '+chr(random.randrange(65,73))+str(random.randrange(1,7))
            tah=input('Urob tah za robota napr:B8 C6:')#Toto ja manualny tah za robota
            urob_tah(tah,s_f,'R')
            print('Robot:',tah)
            vytvor_board(bo)
            pl.delete(tr)
        print('Test šachovnice ..... t\nHrať šach ........... s')
        if input()=='t':
            testuj_sachovnicu(s_f)
        else:
            while True:
                urobil=0
                urobil=tah_hraca(s_f,stara_p,nova_p)
                if urobil==1:tah_robota(s_f)
#*************************************************************************************************************
Typhoon()
