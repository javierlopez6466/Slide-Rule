
#WARNING: DEPRECATED, use "Laser Cut" file

#Final Scale Generator (2/2/20)

#--------------------------------------------------------

#Slide Rule Scale Generator 1.0
#Available Scales: A B C D K R1 R2 CI DI CF DF L S T ST

#Table of Contents
#   1. Setup
#   2. Fundamental Functions
#   3. Scale Generating Function
#   4. Line Drawing Functions
#   5. Action!
#   6. Extrabitz..

#----------------------Setup----------------------------

import math
from PIL import Image, ImageFont, ImageDraw

width = 8000 #DO NOT MESS WITH THESE
height = 1600
img=Image.new('RGB',(width,height),'white') 
draw=ImageDraw.Draw(img)

sh = 160 #scaleheight

al = 0 #allignment. 0 = upper, 1 = lower
sl = 5600 #scale length
li = 1200 #left index offset from left edge
sth = 70 #standard tick height
stt = 3 #standard tick thickness 

#tick height scalars
xs = 0.5
sm = 0.85
med = 1
mxl = 1.15
xl = 1.3

#don't touch:
sc='A'
y0 = 0 #upper level starting point for various objects (ignore me)
yoff=100
shift = 0 #scale shift from left index
sym1 = "S" #left scale symbol
sym2 = "x" #right scale symbol

#----------------------Fundamental Functions----------------------------

def puttick(yoff,x,h,t): #places an individual tick

    #yoff = y pos
    #x = offset of left edge from *left index*
    #h = height of tickmark (measured from baseline or upperline)
    #t = thickness of tickmark (measured from left edge)
    
    for T in range(0,t+1):
        for H in range(0,h+1):
            if al == 0:
                y0 = H
            if al == 1:
                y0 = sh-1-H
            img.putpixel((x+li+T,y0+yoff),(0,0,0)) 

def pat(yoff,func,S,iI,iF,a,b,e,a0,b0,shf): #place ticks in a pattern

    #yoff = y pos, func = function
    
    #S = height modifier (input height scalar like xs, sm, med, lg)
    #iI = starting index point (100 = left index)
    #iF = ending index point (1001 = right index)

    #a+bN (N ∈ Z) defines the patterning (which ticks to place)
    #a = offset from iI
    #b = multiple value 

    #exclusion pattern? 1 = yes, 0 = no
    
    #a0+b0N (N ∈ Z) defines the exlusion patterning (which ticks not to place)
    #a0 = offset from iI
    #b0 = multiple value
    #put placeholders like 1 & 1 in here if e == 0

    #shf = scale shift amount

    for x in range(iI,iF):
        if e == 1:
            if x%b-a == 0 and x%b0-a0 != 0:
                puttick(yoff,shf+func(x/100),round(S*sth),stt)
        elif e == 0:
            if x%b-a == 0:
                puttick(yoff,shf+func(x/100),round(S*sth),stt)

def getwidth(s,z,i):

    #s = symbol (string)
    #z = font size
    #i = italization (normal == 0 , italic == 1)

    if i == 0:
        font=ImageFont.truetype("cmuntt.ttf",z)
    if i == 1:
        font=ImageFont.truetype("cmunit.ttf",z)
    str1=str(s)
    w,h=font.getsize(str1)
    return(w)

def getheight(s,z,i):

    #s = symbol (string)
    #z = font size
    #i = italization (normal == 0 , italic == 1)

    if i == 0:
        font=ImageFont.truetype("cmuntt.ttf",z)
    if i == 1:
        font=ImageFont.truetype("cmunit.ttf",z)
    str1=str(s)
    w,h=font.getsize(str1)
    return(h)

def putsymbol(yoff,s,x,y,z,i):

    #yoff = y pos
    #s = symbol (string)
    #x = offset of centerline from left index
    #y = offset of base from baseline (al == 1) or top from upperline (al == 0)
    #z = font size
    #i = italization (normal == 0 , italic == 1)

    if i == 0:
        font=ImageFont.truetype("cmuntt.ttf",z)
    if i == 1:
        font=ImageFont.truetype("cmunit.ttf",z)
    str1=str(s)
    w,h=font.getsize(str1)

    if al == 0:
        y0 = y
    if al == 1:
        y0 = sh-1-y-h*1.2
    draw.text((x+li-round(w/2)+round(stt/2),y0+yoff),str1,font=font,fill='black')

#----------------------Scale Generating Function----------------------------

def genscale(yoff,sc):

    def func(x):
        if sc == 'C' or sc == 'D' or sc == 'CF' or sc == 'DF':
            return round(sl*math.log10(x))
        if sc == 'A' or sc == 'B':
            return round(1/2*sl*math.log10(x))
        if sc == 'R1' or sc == 'R2':
            return round(2*sl*math.log10(x/10))
        if sc == 'K':
            return round(1/3*sl*math.log10(x))
        if sc == 'CI' or sc == 'DI': #or sc == 'CIF'
            return round(sl*(1-math.log10(x)))
        if sc == 'L':
            return round(sl*x/10)
        if sc == 'S':
            return round(sl*math.log10(10*math.sin(math.radians(x))))
        if sc == 'T':
            return round(sl*math.log10(10*math.tan(math.radians(x))))
        if sc == 'ST':
            return round(sl*math.log10(100*(math.sin(math.radians(x))+math.tan(math.radians(x)))/2))

    #scale labels
    if sc == 'A':
        shift = 0
        sym1 = 'A'
        sym2 = 'x²'
    if sc == 'B':
        shift = 0
        sym1 = 'B'
        sym2 = 'x²'
    if sc == 'C':
        shift = 0
        sym1 = 'C'
        sym2 = 'x'
    if sc == 'D':
        shift = 0
        sym1 = 'D'
        sym2 = 'x'
    if sc == 'K':
        shift = 0
        sym1 = 'K'
        sym2 = 'x³'
    if sc == 'R1':
        shift = 0
        sym1 = 'R'
        #sym12 = '1'
        #sym20 = '√x'
        sym2 = '√x'
    if sc == 'R2':
        shift = -sl
        sym1 = 'R'
        #sym12 = '2'
        sym2 = '√x' #special merger?
    if sc == 'CI':
        shift = 0
        sym1 = 'CI'
        sym2 = '1/x'
    if sc == 'DI':
        shift = 0
        sym1 = 'DI'
        sym2 = '1/x'
    if sc == 'CF':
        shift = round(sl*(1-math.log10(math.pi)))
        sym1 = 'CF'
        sym2 = 'πx'
    if sc == 'DF':
        shift = round(sl*(1-math.log10(math.pi)))
        sym1 = 'DF'
        sym2 = 'πx'
    #if sc == 'CIF': 
        #shift = round(sl*math.log10(math.pi)) 
        #sym1 = 'CIF'
        #sym2 = '1/πx'
    if sc == 'L':
        shift = 0
        sym1 = 'L'
        sym2 = 'log x'
    if sc == 'S':
        shift = 0
        sym1 = 'S'
        sym2 = 'sin x'
    if sc == 'T':
        shift = 0
        sym1 = 'T'
        sym2 = 'tan x'
    if sc == 'ST':
        shift = 0
        sym1 = 'ST'
        sym2 = 'θ<5.7' #eh,..    
    if sc == 'R1':
        if al == 1:
            putsymbol(yoff,1,-2/100*sl+0.5*getwidth(sym1,90,0),sh-1.3*((sh-getheight(sym1,90,0))/2+0.75*getheight(sym1,90,0)),60,0)
        if al == 0:
            putsymbol(yoff,1,-2/100*sl+0.5*getwidth(sym1,90,0),(sh-getheight(sym1,90,0))/2+0.75*getheight(sym1,90,0),60,0)
    if sc == 'R2':
        if al == 1:
            putsymbol(yoff,2,-2/100*sl+0.5*getwidth(sym1,90,0),sh-1.3*((sh-getheight(sym1,90,0))/2+0.75*getheight(sym1,90,0)),60,0)
        if al == 0:
            putsymbol(yoff,2,-2/100*sl+0.5*getwidth(sym1,90,0),(sh-getheight(sym1,90,0))/2+0.75*getheight(sym1,90,0),60,0)

    putsymbol(yoff,sym2,102/100*sl+0.5*getwidth(sym2,90,0),(sh-getheight(sym2,90,0))/2,90,0)
    putsymbol(yoff,sym1,-2/100*sl-0.5*getwidth(sym1,90,0),(sh-getheight(sym1,90,0))/2,90,0)
    
    
    if sc == "C" or sc == "D" or sc == "CI" or sc == "DI":
    
        #Ticks
        pat(yoff,func,med,100,1001,0,100,0,1,1,0)
        pat(yoff,func,xl,100,1001,50,100,1,150,1000,0)
        pat(yoff,func,sm,100,1001,0,10,1,150,100,0)
        pat(yoff,func,sm,100,200,5,10,0,1,1,0)
        pat(yoff,func,xs,100,200,0,1,1,0,5,0)
        pat(yoff,func,xs,200,400,0,2,1,0,10,0)
        pat(yoff,func,xs,400,1001,0,5,1,0,10,0)

        #1-10 Labels
        for x in range(1,11):  
            if x == 10:
                putsymbol(yoff,1,func(x),sth,90,0)        
            else:
                putsymbol(yoff,x,func(x),sth,90,0)

        #0.1-0.9 Labels
        for x in range(11,20):
            putsymbol(yoff,x-10,func(x/10),round(sth*0.85),60,0)

        #Gauge Points
        puttick(yoff,func(math.pi),round(sth),stt)
        putsymbol(yoff,'π',func(math.pi),round(sth),90,0)    
            
    if sc == "A" or sc == "B":

        #Ticks
        pat(yoff,func,med,100,1001,0,100,0,1,1,0)
        pat(yoff,func,med,1000,10001,0,1000,0,1,1,0)
        pat(yoff,func,sm,100,501,0,10,1,50,100,0)
        pat(yoff,func,sm,1000,5001,0,100,1,500,1000,0)
        pat(yoff,func,xl,100,1001,50,100,0,1,1,0)
        pat(yoff,func,xl,1000,10001,500,1000,0,1,1,0)
        pat(yoff,func,xs,100,200,0,2,0,1,1,0)
        pat(yoff,func,xs,1000,2000,0,20,0,1,1,0)
        pat(yoff,func,xs,200,500,5,10,0,1,1,0)
        pat(yoff,func,xs,2000,5000,50,100,0,1,1,0)
        pat(yoff,func,xs,500,1001,0,10,1,0,50,0)
        pat(yoff,func,xs,5000,10001,0,100,1,0,500,0)

        #1-10 Labels
        for x in range(1,11):  
            if x == 10:
                putsymbol(yoff,1,func(x),sth,90,0)
                putsymbol(yoff,1,func(x*10),sth,90,0)
            else:
                putsymbol(yoff,x,func(x),sth,90,0)
                putsymbol(yoff,x,func(x*10),sth,90,0)
                
        #Gauge Points
        puttick(yoff,func(math.pi),round(sth),stt)
        putsymbol(yoff,'π',func(math.pi),round(sth),90,0)

    if sc == "K":
        for b in range(0,3):

            #Ticks
            pat(yoff,func,med,100*(10**b),1000*(10**b)+1,0,100*(10**b),0,1,1,0)
            pat(yoff,func,xl,100*(10**b),600*(10**b)+1,50*(10**b),100*(10**b),0,1,1,0)
            pat(yoff,func,sm,100*(10**b),300*(10**b)+1,0,10*(10**b),0,1,1,0)
            pat(yoff,func,xs,100*(10**b),300*(10**b)+1,5*(10**b),10*(10**b),0,1,1,0)
            pat(yoff,func,xs,300*(10**b),600*(10**b)+1,0,10*(10**b),0,1,1,0)
            pat(yoff,func,xs,600*(10**b),1000*(10**b)+1,0,20*(10**b),0,1,1,0)
    
        #1-10 Labels
        f=75
        for x in range(1,11):  
            if x == 10:
                putsymbol(yoff,1,func(x),sth,f,0)
                putsymbol(yoff,1,func(x*10),sth,f,0)
                putsymbol(yoff,1,func(x*100),sth,f,0)
            else:
                putsymbol(yoff,x,func(x),sth,f,0)
                putsymbol(yoff,x,func(x*10),sth,f,0)
                putsymbol(yoff,x,func(x*100),sth,f,0)

    if sc == 'R1':

        #Ticks
        pat(yoff,func,med,1000,3200,0,100,0,1,1,0)
        pat(yoff,func,xl,1000,2000,0,50,1,0,100,0)
        pat(yoff,func,sm,2000,3200,0,50,0,0,1000,0)
        pat(yoff,func,sm,1000,2000,0,10,1,0,50,0)
        pat(yoff,func,xs,1000,2000,5,10,0,1,1,0)
        pat(yoff,func,xs,2000,3180,0,10,1,0,50,0)

        #1-10 Labels
        for x in range(1,4):          
            putsymbol(yoff,x,func(10*x),sth,90,0)

        #0.1-3.1 Labels
        for x in range(11,20):
            putsymbol(yoff,x-10,func(x),sth,60,0)
        for x in range(21,30):
            putsymbol(yoff,x-20,func(x),sth,60,0)
        putsymbol(yoff,1,func(31),sth,60,0)

        #puttick(yoff,sl,round(sth),stt)

    if sc == 'R2':

        #Ticks
        pat(yoff,func,med,4000,10001,0,1000,0,1,1,shift)
        pat(yoff,func,xl,5000,10000,500,1000,0,1,1,shift)
        pat(yoff,func,sm,3200,10000,0,100,1,0,1000,shift)
        pat(yoff,func,sm,3200,5000,0,50,0,1,1,shift)
        pat(yoff,func,xs,3160,5000,0,10,1,0,50,shift)
        pat(yoff,func,xs,5000,10000,0,20,1,0,100,shift)

        #1-10 Labels
        for x in range(4,10):          
            putsymbol(yoff,x,func(10*x)+shift,sth,90,0)
        putsymbol(yoff,1,sl,sth,90,0)

        #0.1-3.1 Labels
        for x in range(32,40):
            putsymbol(yoff,x%10,func(x)+shift,sth,60,0)
        for x in range(41,50):
            putsymbol(yoff,x%10,func(x)+shift,sth,60,0)
        
    if sc == "CF" or sc == "DF": #or s == "CIF"

        #Ticks
        pat(yoff,func,med,100,301,0,100,0,1,1,shift)
        pat(yoff,func,med,400,1001,0,100,0,1,1,-1*sl+shift)
        pat(yoff,func,xl,200,301,50,100,0,1,1,shift)
        pat(yoff,func,sm,100,201,0,5,0,1,1,shift)
        pat(yoff,func,sm,200,311,0,10,0,1,1,shift)
        pat(yoff,func,xl,320,1001,50,100,0,150,1000,-1*sl+shift)
        pat(yoff,func,sm,320,1001,0,10,1,150,100,-1*sl+shift)
        pat(yoff,func,xs,100,201,0,1,1,0,5,shift)
        pat(yoff,func,xs,200,314,0,2,1,0,10,shift)
        pat(yoff,func,xs,316,401,0,2,1,0,10,-1*sl+shift)
        #-1*sl+shift is the way to go from now on!!
        pat(yoff,func,xs,400,1001,0,5,1,0,10,-1*sl+shift)

        #1-10 Labels
        for x in range(1,4):  
            putsymbol(yoff,x,func(x)+shift,sth,90,0)        
        for x in range(4,10):
            putsymbol(yoff,x,func(x)-sl+shift,sth,90,0)

        #0.1-0.9 Labels
        for x in range(11,20):
            putsymbol(yoff,x-10,func(x/10)+shift,round(sth*0.85),60,0)  

        #Gauge Points
        puttick(yoff,func(math.pi)+shift,round(sth),stt)
        putsymbol(yoff,'π',func(math.pi)+shift,round(sth),90,0)
        puttick(yoff,func(math.pi)-sl+shift,round(sth),stt)
        putsymbol(yoff,'π',func(math.pi)-sl+shift,round(sth),90,0)
        
    if sc == 'L':
        
        #Ticks
        pat(yoff,func,med,0,1001,0,10,1,50,100,0)
        pat(yoff,func,xl,1,1001,50,100,0,1,1,0)
        pat(yoff,func,xs,1,1001,0,2,1,0,50,0)

        #Labels
        for x in range(0,11):  
            if x == 0:
                putsymbol(yoff,0,func(x),sth,90,0)
            if x == 10:
                putsymbol(yoff,1,func(x),sth,90,0)
            elif x in range(1,10):
                putsymbol(yoff,'.'+str(x),func(x),sth,90,0)

    if sc == 'S':

        #Ticks
        pat(yoff,func,xl,1000,7001,0,1000,0,1,1,0)
        pat(yoff,func,med,7000,10001,0,1000,0,1,1,0)
        puttick(yoff,0,round(sth),stt)
        pat(yoff,func,xl,600,2001,0,100,0,1,1,0)
        pat(yoff,func,sm,600,2000,50,100,1,0,100,0)
        pat(yoff,func,xl,2000,6000,500,1000,1,0,1000,0)
        pat(yoff,func,sm,2000,6000,0,100,1,0,500,0)
        pat(yoff,func,xs,580,2000,0,10,1,0,50,0)
        pat(yoff,func,xs,2000,3000,0,20,1,0,100,0)
        pat(yoff,func,xs,3000,6000,0,50,1,0,100,0)
        pat(yoff,func,sm,6000,8501,500,1000,0,1,1,0)
        pat(yoff,func,xs,6000,8000,0,100,0,1,1,0)
        
        #Degree Labels

        for x in range(6,16):  
            putsymbol(yoff,str(x),func(x)+1.2/2*getwidth(x,50,1),sth,50,0)
            putsymbol(yoff,"<"+str(90-x),func(x)-1.9/2*getwidth(90-x,50,1),sth,50,1)

        for x in range(16,20):
            putsymbol(yoff,str(x),func(x)+1.2/2*getwidth(x,55,1),sth,55,0)
          
        for x in range(20,71,5):  
            if (x%5 == 0 and x < 40) or x%10 == 0:
                putsymbol(yoff,str(x),func(x)+1.2/2*getwidth(x,55,1),sth,55,0)
                if x != 20:
                    putsymbol(yoff,"<"+str(90-x),func(x)-1.9/2*getwidth(90-x,55,1),sth,55,1)

        putsymbol(yoff,90,sl,sth,60,0)

    if sc == 'T':

        #Ticks
        pat(yoff,func,xl,600,2501,0,100,0,1,1,0)
        pat(yoff,func,xl,600,1001,50,100,0,1,1,0)
        pat(yoff,func,xl,2500,4501,0,500,0,1,1,0)
        pat(yoff,func,med,2500,4501,0,100,0,1,1,0)
        puttick(yoff,sl,round(sth),stt)
        puttick(yoff,0,round(sth),stt)
        pat(yoff,func,med,600,951,50,100,0,1,1,0)
        pat(yoff,func,sm,580,1001,0,10,1,0,50,0)
        pat(yoff,func,sm,1000,2500,50,100,0,1,1,0)
        pat(yoff,func,xs,570,1001,5,10,1,0,10,0)
        pat(yoff,func,xs,1000,2500,0,10,1,0,50,0)
        pat(yoff,func,xs,2500,4501,0,20,1,0,100,0)
        
        #Degree Labels
        f=1.1
        for x in range(6,16):  
            putsymbol(yoff,str(x),func(x)+1.2/2*getwidth(x,50,1),f*sth,50,0)
            putsymbol(yoff,"<"+str(90-x),func(x)-1.9/2*getwidth(90-x,50,1),f*sth,50,1)

        for x in range(16,21):
            putsymbol(yoff,str(x),func(x)+1.2/2*getwidth(x,55,1),f*sth,55,0)

        for x in range(25,41,5):  
            if x%5 == 0:
                putsymbol(yoff,str(x),func(x)+1.2/2*getwidth(x,55,1),f*sth,55,0)
                putsymbol(yoff,"<"+str(90-x),func(x)-1.9/2*getwidth(90-x,55,1),f*sth,55,1)

        putsymbol(yoff,45,sl,f*sth,60,0)

    if sc == 'ST':

        #Ticks
        pat(yoff,func,med,100,551,0,50,0,1,1,0)
        puttick(yoff,sl,round(sth),stt)
        puttick(yoff,0,round(sth),stt)
        pat(yoff,func,1.2,60,100,0,10,0,1,1,0)
        pat(yoff,func,xl,60,100,5,10,0,1,1,0)
        pat(yoff,func,med,100,200,0,10,1,0,50,0)
        pat(yoff,func,sm,200,580,0,10,0,1,1,0)
        pat(yoff,func,sm,58,100,0,1,0,1,1,0)
        pat(yoff,func,sm,100,200,0,5,0,1,1,0)
        pat(yoff,func,xs,100,200,0,1,1,0,5,0)
        pat(yoff,func,xs,200,400,0,2,1,0,10,0)
        pat(yoff,func,xs,400,575,5,10,0,1,1,0)

        for x in range(570,1000):
            if x%5 == 0 and x%10-0 != 0:
                puttick(yoff,func(x/1000),round(xs*sth),stt)

        #Degree Labels
        putsymbol(yoff,'1°',func(1),sth,90,0)
        for x in range(6,10):
            putsymbol(yoff,"."+str(x),func(x/10),sth,90,0)
        for x in range(1,4):
            putsymbol(yoff,str(x+0.5),func(x+0.5),sth,90,0)
        for x in range(2,6):
            putsymbol(yoff,str(x),func(x),sth,90,0)

#----------------------Line Drawing Functions----------------------------

def putborders(): #Use to place initial borders
    #Main Frame
    horizontals=[0,479,1119,1598]
    for i in range(0,4):
        start=horizontals[i]
        for x in range(0,width):
            for y in range(start,start+2):
                img.putpixel((x,y),(0,0,0))
    verticals=[0,width-2]
    for i in range(0,2):
        start=verticals[i]
        for x in range(start,start+2):
            for y in range(0,1600):
                img.putpixel((x,y),(0,0,0))
                
    #Top Stator Cut-outs
    verticals=[240,width-240]
    if side=='front':
        Yi=0
        Yf=480
    elif side=='back':
        Yi=1120
        Yf=1600
    for i in range(0,2):
        start=verticals[i]
        for x in range(start,start+2):
            for y in range(Yi,Yf):
                img.putpixel((x,y),(0,0,0))

def metalcutoffs(): #Use to temporarily view the metal pieceboundaries
    
    b=30 #edge offset
    
    verticals=[480,width-480]
    for i in range(0,2):
        start=verticals[i]
        for x in range(start-1,start+1):
            for y in range(0,1600):
                img.putpixel((x,y),(230,230,230))
    
    coords=[[240+b,480-b,b,b],[b,240+b,1120+b,1120+b],[b,480-b,1600-b,1600-b],
            [240+b,240+b,b,1120+b],[b,b,1120+b,1600-b],[480-b,480-b,b,1600-b]]
    for i in range(0,6):
        coords.append([width-coords[i][1],width-coords[i][0],coords[i][2],coords[i][3]])

    if side=='front':
        points=coords
    elif side == 'back':
        points=[]
        for i in range(0,12):
            points.append([coords[i][0],coords[i][1],1600-coords[i][3],1600-coords[i][2]])
            #print(points[i])
        
    for i in range(0,12):
        for x in range(points[i][0]-1,points[i][1]+1):
            for y in range(points[i][2]-1,points[i][3]+1):
                img.putpixel((x,y),(234,36,98))

#----------------------Action------------------------------------------

#FRONT SCALE
side='front'
metalcutoffs()
putborders()

al=1
genscale(110,'L')
genscale(320,'DF')
genscale(693,'CI')
genscale(960,'C')

al=0
genscale(480,'CF')
genscale(1120,'D')
genscale(1280,'R1')
genscale(1435,'R2')

putsymbol(25,'DECITRIG 1000',width*1/3-li,0,90,0)
putsymbol(25,'KWENA & TOOR CO.',width*2/3-li,0,90,0)

putsymbol(25,'LEFT HANDED LIMAÇON 2020',width*1/2-li,0,90,0)

img.save('FrontScaleAPPEARANCE.png','PNG')
img.show()

#CLEAR IMAGE
img=Image.new('RGB',(width,height),'white') 
draw=ImageDraw.Draw(img)

#BACKSCALE
side='back'

metalcutoffs()
putborders()
al=1
genscale(110,'K')
genscale(320,'A')
genscale(640,'T')
genscale(800,'ST')
genscale(960,'S')

al=0
genscale(480,'B')
genscale(1120,'D')
genscale(1360,'DI')

img.save('BackScaleAPPEARANCE.png','PNG')
img.show()

#--------------------------EXTRABITZ----------------------------

# A B C D K R1 R2 CI DI CF DF L S T ST

# |  K,  A  [ B, T, ST, S ] D,  DI    |
# |  L,  DF [ CF,  CI,  C ] D, R1, R2 |

#To-Do:
    #CIF scales <<< I HATE U 

    #maybe an easy to use interface for customizations. . nah
    #place phrases ("slide rule", "keuffel esser", "by Javier", etc)
    #create cut out patterns

    #DECITRIG 1000 -- KWENA & TOOR CO. -- LEFT HANDED LIMACON 2020
