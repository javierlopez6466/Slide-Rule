#Most Recent Update (10/29/20)

# **** if you need pure black print, simply replace all 'black'
# with 'red' in a COPY (and remove red from putsym options)****

#--------------------------------------------------------

#Slide Rule Scale Generator 1.0
#Available Scales: A B C D K R1 R2 CI DI CF DF CIF L S T ST

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
import time
start_time = time.time()

oX=100 #x margins
oY=100 #y margins
width = 8000+2*oX 
height = 1600*2+3*oY
img=Image.new('RGB',(width,height),'white') 
draw=ImageDraw.Draw(img)

sh = 160 #scaleheight

al = 0 #allignment. 0 = upper, 1 = lower
sl = 5600 #scale length
li = round(width/2-sl/2) #left index offset from left edge
#Ticks, Labels, are referenced from li as to be consistent
sth = 70 #standard tick height
stt = 4 #standard tick thickness 

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
    
    for T in range(0,t):
        for H in range(0,h+1):
            if al == 0:
                y0 = H
            if al == 1:
                y0 = sh-1-H
            img.putpixel((x+li+T-2,y0+yoff),(0,0,0)) 

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

def putsymbol(C,yoff,s,x,y,z,i):

    #C = color
    #yoff = y pos
    #s = symbol (string)
    #x = offset of centerline from left index (li)
    #y = offset of base from baseline (al == 1) or top from upperline (al == 0)
    #z = font size
    #i = italization (normal == 0 , italic == 1)
    
    if C == 'black':
        color = 'black'
    if C == 'red':
        color = 'red'
    if C == 'green':
        color = '#228B1E'

    if i == 0:
        font=ImageFont.truetype("cmuntt.ttf",z)
        #font=ImageFont.truetype("cmunrm.ttf",z) mythical latex edition
    if i == 1:
        font=ImageFont.truetype("cmunit.ttf",z)
    str1=str(s)
    w,h=font.getsize(str1)

    if al == 0:
        y0 = y
    if al == 1:
        y0 = sh-1-y-h*1.2
    draw.text((x+li-round(w/2)+round(stt/2),y0+yoff),str1,font=font,fill=color)

def extend(image,y,d,A): #Use to create bleed for sticker cutouts

    #image eg img, img2, etc
    #y = y pixel row
    #d = direction ('up','down')
    #A = Amplitude (# of pixels to extend)

    img=image
    
    for x in range(0,width):
        r, g, b = img.getpixel((x, y))

        if d == 'up':
            for yi in range(y-A,y):
                img.putpixel((x,yi),(r,g,b))

        if d == 'down':
            for yi in range(y,y+A):
                img.putpixel((x,yi),(r,g,b))

#----------------------Scale Generating Function----------------------------

def genscale(yoff,sc):

    #Generating Functions for the Scales
    def func(x):
        if sc == 'C' or sc == 'D' or sc == 'CF' or sc == 'DF':
            return round(sl*math.log10(x))
        if sc == 'A' or sc == 'B':
            return round(1/2*sl*math.log10(x))
        if sc == 'R1' or sc == 'R2':
            return round(2*sl*math.log10( x/10))
        if sc == 'K':
            return round(1/3*sl*math.log10(x))
        if sc == 'CI' or sc == 'DI':
            return round(sl*(1-math.log10(x)))
        if sc == 'CIF':
            return round(sl*(1-math.log10(math.pi)-math.log10(x)))
        if sc == 'L':
            return round(sl*x/10)
        if sc == 'S':
            return round(sl*math.log10(10*math.sin(math.radians(x))))
        if sc == 'T':
            return round(sl*math.log10(10*math.tan(math.radians(x))))
        if sc == 'ST':
            return round(sl*math.log10(100*(math.sin(math.radians(x))+math.tan(math.radians(x)))/2))

    #Scale Symbol Labels
    if sc == 'A':
        shift = 0
        sym1 = 'A'
        sym2 = 'x²'
        col = 'black'
    if sc == 'B':
        shift = 0
        sym1 = 'B'
        sym2 = 'x²'
        col = 'black'
    if sc == 'C':
        shift = 0
        sym1 = 'C'
        sym2 = 'x'
        col = 'black'
    if sc == 'D':
        shift = 0
        sym1 = 'D'
        sym2 = 'x'
        col = 'black'
    if sc == 'K':
        shift = 0
        sym1 = 'K'
        sym2 = 'x³'
        col = 'black'
    if sc == 'R1':
        shift = 0
        sym1 = 'R'
        sym2 = '√x'
        col = 'black'
    if sc == 'R2':
        shift = -sl
        sym1 = 'R'
        sym2 = '√x' 
        col = 'black'
    if sc == 'CI':
        shift = 0
        sym1 = 'CI'
        sym2 = '1/x'
        col = 'red'
    if sc == 'DI':
        shift = 0
        sym1 = 'DI'
        sym2 = '1/x'
        col = 'red'
    if sc == 'CF':
        shift = round(sl*(1-math.log10(math.pi)))
        sym1 = 'CF'
        sym2 = 'πx'
        col = 'black'
    if sc == 'DF':
        shift = round(sl*(1-math.log10(math.pi)))
        sym1 = 'DF'
        sym2 = 'πx'
        col = 'black'
    if sc == 'CIF': 
        shift = 0
        sym1 = 'CIF'
        sym2 = '1/πx'
        col = 'red'
    if sc == 'L':
        shift = 0
        sym1 = 'L'
        sym2 = 'log x'
        col = 'black'
    if sc == 'S':
        shift = 0
        sym1 = 'S'
        sym2 = 'sin x'
        col = 'black'
    if sc == 'T':
        shift = 0
        sym1 = 'T'
        sym2 = 'tan x'
        col = 'black'
    if sc == 'ST':
        shift = 0
        sym1 = 'ST'
        sym2 = 'θ<5.7°' 
        col = 'black'

    #Place Index Symbols (Left and Right)
    putsymbol(col,yoff,sym2,102/100*sl+0.5*getwidth(sym2,90,0),(sh-getheight(sym2,90,0))/2,90,0)
    putsymbol(col,yoff,sym1,-2/100*sl-0.5*getwidth(sym1,90,0),(sh-getheight(sym1,90,0))/2,90,0)

    #Exceptions / Special Symbol Rules for Rs, S and T
    if sc == 'R1':
        if al == 1:
            putsymbol('black',yoff,1,-2/100*sl+0.5*getwidth(sym1,90,0),
                      sh-1.3*((sh-getheight(sym1,90,0))/2+0.75*getheight(sym1,90,0)),60,0)
        if al == 0:
            putsymbol('black',yoff,1,-2/100*sl+0.5*getwidth(sym1,90,0),
                      (sh-getheight(sym1,90,0))/2+0.75*getheight(sym1,90,0),60,0)
    if sc == 'R2':
        if al == 1:
            putsymbol('black',yoff,2,-2/100*sl+0.5*getwidth(sym1,90,0),
                      sh-1.3*((sh-getheight(sym1,90,0))/2+0.75*getheight(sym1,90,0)),60,0)
        if al == 0:
            putsymbol('black',yoff,2,-2/100*sl+0.5*getwidth(sym1,90,0),
                      (sh-getheight(sym1,90,0))/2+0.75*getheight(sym1,90,0),60,0)
    if sc == 'S':
        putsymbol('red',yoff,'C',-2/100*sl-0.5*getwidth(sym1,90,0)-getwidth('_S',90,0),(sh-getheight(sym2,90,0))/2,90,0)
    if sc == 'T':
        putsymbol('red',yoff,'T',-2/100*sl-0.5*getwidth(sym1,90,0)-getwidth('_T',90,0),(sh-getheight(sym2,90,0))/2,90,0)
        
    #Tick Placement
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
                putsymbol(col,yoff,1,func(x),sth,90,0)        
            else:
                putsymbol(col,yoff,x,func(x),sth,90,0)

        #0.1-0.9 Labels
        for x in range(11,20):
            putsymbol(col,yoff,x-10,func(x/10),round(sth*0.85),60,0)

        #Gauge Points
        puttick(yoff,func(math.pi),round(sth),stt)
        putsymbol(col,yoff,'π',func(math.pi),round(sth),90,0)

    if sc == "C" or sc == "D":
        if yoff < 1600+oY:
            #r Gauge Point
            puttick(yoff,func(18/math.pi),round(sth),stt)
            putsymbol('black',yoff,'r',func(18/math.pi),round(sth),90,0)
            
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
                putsymbol('black',yoff,1,func(x),sth,90,0)
                putsymbol('black',yoff,1,func(x*10),sth,90,0)
            else:
                putsymbol('black',yoff,x,func(x),sth,90,0)
                putsymbol('black',yoff,x,func(x*10),sth,90,0)
                
        #Gauge Points
        puttick(yoff,func(math.pi),round(sth),stt)
        putsymbol('black',yoff,'π',func(math.pi),round(sth),90,0)

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
                putsymbol('black',yoff,1,func(x),sth,f,0)
                putsymbol('black',yoff,1,func(x*10),sth,f,0)
                putsymbol('black',yoff,1,func(x*100),sth,f,0)
            else:
                putsymbol('black',yoff,x,func(x),sth,f,0)
                putsymbol('black',yoff,x,func(x*10),sth,f,0)
                putsymbol('black',yoff,x,func(x*100),sth,f,0)

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
            putsymbol('black',yoff,x,func(10*x),sth,90,0)

        #0.1-3.1 Labels
        for x in range(11,20):
            putsymbol('black',yoff,x-10,func(x),sth,60,0)
        for x in range(21,30):
            putsymbol('black',yoff,x-20,func(x),sth,60,0)
        putsymbol('black',yoff,1,func(31),sth,60,0)

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
            putsymbol('black',yoff,x,func(10*x)+shift,sth,90,0)
        putsymbol('black',yoff,1,sl,sth,90,0)

        #0.1-3.1 Labels
        for x in range(32,40):
            putsymbol('black',yoff,x%10,func(x)+shift,sth,60,0)
        for x in range(41,50):
            putsymbol('black',yoff,x%10,func(x)+shift,sth,60,0)
        
    if sc == "CF" or sc == "DF":

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
        pat(yoff,func,xs,400,1001,0,5,1,0,10,-1*sl+shift)

        #1-10 Labels
        for x in range(1,4):  
            putsymbol('black',yoff,x,func(x)+shift,sth,90,0)        
        for x in range(4,10):
            putsymbol('black',yoff,x,func(x)-sl+shift,sth,90,0)

        #0.1-0.9 Labels
        for x in range(11,20):
            putsymbol('black',yoff,x-10,func(x/10)+shift,round(sth*0.85),60,0)  

        #Gauge Points
        puttick(yoff,func(math.pi)+shift,round(sth),stt)
        putsymbol('black',yoff,'π',func(math.pi)+shift,round(sth),90,0)
        puttick(yoff,func(math.pi)-sl+shift,round(sth),stt)
        putsymbol('black',yoff,'π',func(math.pi)-sl+shift,round(sth),90,0)

    if sc == 'CIF':

        #Ticks
        pat(yoff,func,med,100,301,0,100,0,1,1,0)
        pat(yoff,func,med,400,1001,0,100,0,1,1,sl)

        pat(yoff,func,xl,200,301,50,100,0,1,1,0)
        pat(yoff,func,sm,100,201,0,5,0,1,1,0)
        pat(yoff,func,sm,200,321,0,10,0,1,1,0)
        pat(yoff,func,xl,320,1001,50,100,0,150,1000,sl)
        pat(yoff,func,sm,310,1001,0,10,1,150,100,sl)
        pat(yoff,func,xs,100,201,0,1,1,0,5,0)
        pat(yoff,func,xs,200,321,0,2,1,0,10,0)
        pat(yoff,func,xs,310,401,0,2,1,0,10,sl)
        pat(yoff,func,xs,400,1001,0,5,1,0,10,sl)

        #1-10 Labels
        for x in range(4,10):  
            putsymbol('red',yoff,x,func(x)+sl,sth,90,0)        
        for x in range(1,4):
            putsymbol('red',yoff,x,func(x),sth,90,0)

        #0.1-0.9 Labels
        for x in range(11,20):
            putsymbol('red',yoff,x-10,func(x/10),round(sth*0.85),60,0)  
        
    if sc == 'L':
        
        #Ticks
        pat(yoff,func,med,0,1001,0,10,1,50,50,0)
        pat(yoff,func,xl,1,1001,50,100,0,1,1,0)
        pat(yoff,func,mxl,0,1001,0,100,0,1,1,0)
        pat(yoff,func,xs,1,1001,0,2,1,0,50,0)

        #Labels
        for x in range(0,11):  
            if x == 0:
                putsymbol('black',yoff,0,func(x),sth,90,0)
            if x == 10:
                putsymbol('black',yoff,1,func(x),sth,90,0)
            elif x in range(1,10):
                putsymbol('black',yoff,'.'+str(x),func(x),sth,90,0)

    if sc == 'S':

        #Ticks
        pat(yoff,func,xl,1000,7001,0,1000,0,1,1,0)
        pat(yoff,func,med,7000,10001,0,1000,0,1,1,0)
        pat(yoff,func,xl,600,2001,0,100,0,1,1,0)
        pat(yoff,func,sm,600,2000,50,100,1,0,100,0)
        pat(yoff,func,xl,2000,6000,500,1000,1,0,1000,0)
        pat(yoff,func,sm,2000,6000,0,100,1,0,500,0)
        pat(yoff,func,xs,570,2000,0,10,1,0,50,0)
        pat(yoff,func,xs,2000,3000,0,20,1,0,100,0)
        pat(yoff,func,xs,3000,6000,0,50,1,0,100,0)
        pat(yoff,func,sm,6000,8501,500,1000,0,1,1,0)
        pat(yoff,func,xs,6000,8000,0,100,0,1,1,0)
        
        #Degree Labels

        for x in range(6,16):  
            putsymbol('black',yoff,str(x),func(x)+1.2/2*getwidth(x,50,1),sth,50,0)
            putsymbol('red',yoff,str(90-x),func(x)-1.4/2*getwidth(90-x,50,1),sth,50,1)

        for x in range(16,20):
            putsymbol('black',yoff,str(x),func(x)+1.2/2*getwidth(x,55,1),sth,55,0)
          
        for x in range(20,71,5):  
            if (x%5 == 0 and x < 40) or x%10 == 0:
                putsymbol('black',yoff,str(x),func(x)+1.2/2*getwidth(x,55,1),sth,55,0)
                if x != 20:
                    if 90-x != 40:
                        putsymbol('red',yoff,str(90-x),func(x)-1.4/2*getwidth(90-x,55,1),sth,55,1)
                    if 90-x == 40:
                        putsymbol('red',yoff+11,str(40),func(x)-1.4/2*getwidth(90-x,55,1),sth,55,1)

        putsymbol('black',yoff,90,sl,sth,60,0)

    if sc == 'T':

        #Ticks
        pat(yoff,func,xl,600,2501,0,100,0,1,1,0)
        pat(yoff,func,xl,600,1001,50,100,0,1,1,0)
        pat(yoff,func,xl,2500,4501,0,500,0,1,1,0)
        pat(yoff,func,med,2500,4501,0,100,0,1,1,0)
        puttick(yoff,sl,round(sth),stt)
        pat(yoff,func,med,600,951,50,100,0,1,1,0)
        pat(yoff,func,sm,570,1001,0,10,1,0,50,0)
        pat(yoff,func,sm,1000,2500,50,100,0,1,1,0)
        pat(yoff,func,xs,570,1001,5,10,1,0,10,0)
        pat(yoff,func,xs,1000,2500,0,10,1,0,50,0)
        pat(yoff,func,xs,2500,4501,0,20,1,0,100,0)
        
        #Degree Labels
        f=1.1
        for x in range(6,16):  
            putsymbol('black',yoff,str(x),func(x)+1.2/2*getwidth(x,50,1),f*sth,50,0)
            putsymbol('red',yoff,str(90-x),func(x)-1.4/2*getwidth(90-x,50,1),f*sth,50,1)

        for x in range(16,21):
            putsymbol('black',yoff,str(x),func(x)+1.2/2*getwidth(x,55,1),f*sth,55,0)

        for x in range(25,41,5):  
            if x%5 == 0:
                putsymbol('black',yoff,str(x),func(x)+1.2/2*getwidth(x,55,1),f*sth,55,0)
                putsymbol('red',yoff,str(90-x),func(x)-1.4/2*getwidth(90-x,55,1),f*sth,55,1)

        putsymbol('black',yoff,45,sl,f*sth,60,0)

    if sc == 'ST':

        #Ticks
        pat(yoff,func,med,100,551,0,50,0,1,1,0)
        pat(yoff,func,1.2,60,100,0,10,0,1,1,0)
        pat(yoff,func,xl,60,100,5,10,0,1,1,0)
        pat(yoff,func,med,100,200,0,10,1,0,50,0)
        pat(yoff,func,sm,200,590,0,10,0,1,1,0)
        pat(yoff,func,sm,57,100,0,1,0,1,1,0)
        pat(yoff,func,sm,100,200,0,5,0,1,1,0)
        pat(yoff,func,xs,100,200,0,1,1,0,5,0)
        pat(yoff,func,xs,200,400,0,2,1,0,10,0)
        pat(yoff,func,xs,400,585,5,10,0,1,1,0)

        for x in range(570,1000):
            if x%5 == 0 and x%10-0 != 0:
                puttick(yoff,func(x/1000),round(xs*sth),stt)

        #Degree Labels
        putsymbol('black',yoff,'1°',func(1),sth,90,0)
        for x in range(6,10):
            putsymbol('black',yoff,"."+str(x),func(x/10),sth,90,0)
        for x in range(1,4):
            putsymbol('black',yoff,str(x+0.5),func(x+0.5),sth,90,0)
        for x in range(2,6):
            putsymbol('black',yoff,str(x),func(x),sth,90,0)

#----------------------Line Drawing Functions----------------------------

def putborders(y0): #Place initial borders around scales y0 = vertical offset

    #Main Frame
    horizontals=[ y0,  479+y0,  1119+y0,  1598+y0  ]
    
    for i in range(0,4):
        start=horizontals[i]
        for x in range(oX,width-oX):
            for y in range(start,start+2):
                img.putpixel((x,y),(0,0,0))
    verticals=[oX,width-oX]
    for i in range(0,2):
        start=verticals[i]
        for x in range(start,start+2):
            for y in range(y0,1600+y0):
                img.putpixel((x,y),(0,0,0))
                
    #Top Stator Cut-outs
    verticals=[  240+oX,  (width-240)-oX  ]
    
    if side=='front':
        Yi=y0
        Yf=480+y0
    elif side=='back':
        Yi=1120+y0
        Yf=1600+y0
    for i in range(0,2):
        start=verticals[i]
        for x in range(start,start+2):
            for y in range(Yi,Yf):
                img.putpixel((x,y),(0,0,0))

def metalcutoffs(y0): #Use to temporarily view the metal pieceboundaries
    #y0 = vertical offset
    
    b=30 #offset of metal from boundary

    #Initial Boundary verticals
    verticals=[480+oX,width-480-oX]
    for i in range(0,2):
        start=verticals[i]
        for x in range(start-1,start+1):
            for y in range(y0,1600+y0):
                img.putpixel((x,y),(230,230,230))

        #   0    240   480
        #   |     |     |     
        #            1       -0
        #          -----  
        #          |   |
        #          |   |
        #       4> |   | <6
        #          |   |
        #          |   |
        #       2  |   |    -1120
        #      -----   |
        #   5> |       |
        #      |       |
        #      ---------
        #       3           -1600
        #   |     |     |

    #Create the left piece using coords format: (x1,x2,y1,y2)
    coords=[[240+b+oX,480-b+oX,b+y0,b+y0],      #1
            [b+oX,240+b+oX,1120+b+y0,1120+b+y0],#2
            [b+oX,480-b+oX,1600-b+y0,1600-b+y0],#3
            [240+b+oX,240+b+oX,b+y0,1120+b+y0], #4
            [b+oX,b+oX,1120+b+y0,1600-b+y0],    #5
            [480-b+oX,480-b+oX,b+y0,1600-b+y0]] #6
    
    #Symmetrically create the right piece
    for i in range(0,6):
        coords.append([width-coords[i][1],width-coords[i][0],
                       coords[i][2],coords[i][3]])

    #Transfer coords to points for printing
    if side=='front':
        points=coords
    #If backside, first apply a vertical reflection
    elif side == 'back':
        points=[]
        for i in range(0,12):
            points.append([coords[i][0],coords[i][1],
                           2*y0+1600-coords[i][3],2*y0+1600-coords[i][2]])
        
    for i in range(0,12):
        for x in range(points[i][0]-1,points[i][1]+1):
            for y in range(points[i][2]-1,points[i][3]+1):
                img.putpixel((x,y),(234,36,98))

#----------------------Action------------------------------------------

#Turn on and off final render, diagnostic, and stickerprint
render = 0
diagnostic = 0
stickerprint = 1

if render == 1 or stickerprint == 1:
    
    # 'Scale Cutting Pattern'

    if stickerprint != 1:
        side='front'
        putborders(oY)
        #metalcutoffs(oY)
        side='back'
        putborders(1600+2*oY)
        #metalcutoffs(1600+2*oY)

    #Front Scale
    al=1
    genscale(110+oY,'L')
    genscale(320+oY,'DF')
    genscale(800+oY,'CI')
    genscale(960+oY,'C')

    al=0
    genscale(480+oY,'CF')
    genscale(640+oY,'CIF')
    genscale(1120+oY,'D')
    genscale(1280+oY,'R1')
    genscale(1435+oY,'R2')

    putsymbol('red',25+oY,'BOGELEX 1000',(width-2*oX)*1/4-li,0,90,0)
    putsymbol('red',25+oY,'LEFT HANDED LIMAÇON 2020',(width-2*oX)*2/4-li+oX,0,90,0)
    putsymbol('red',25+oY,'KWENA & TOOR CO.',(width-2*oX)*3/4-li,0,90,0)

    #Back Scale
    al=1
    genscale(110+1600+2*oY,'K')
    genscale(320+1600+2*oY,'A')
    genscale(640+1600+2*oY,'T')
    genscale(800+1600+2*oY,'ST')
    genscale(960+1600+2*oY,'S')

    al=0
    genscale(480+1600+2*oY,'B')
    genscale(1120+1600+2*oY,'D')
    genscale(1360+1600+2*oY,'DI')

    img.save('ScaleCuttingPattern.png','PNG')
    img.show()
    
    # 'Scale Etching Pattern'
    if stickerprint != 1:

        #Clear Image
        img=Image.new('RGB',(width,height),'white') 
        draw=ImageDraw.Draw(img)

        side='front'
        putborders(oY)
        side='back'
        putborders(1600+2*oY)

        img.save('ScaleEtchingPattern.png','PNG')
        img.show()

if diagnostic == 1:

    #If you're reading this, you're a real one
    # +5 brownie points to you

    oX=0 #x dir margins
    oY=0 #y dir margins
    width = 7000
    height = 160*24
    li = round(width/2-sl/2) #update left index
    img=Image.new('RGB',(width,height),'white') 
    draw=ImageDraw.Draw(img)

    putsymbol('black',50+oY,'Diagnostic Test Print of Available Scales',width/2-li,0,140,0)
    putsymbol('black',200+oY,'A B C D K R1 R2 CI DI CF DF CIF L S T ST',width/2-li,0,120,0)
    al=1
    k = 120+sh

    scalelist=['A','B','C','D',
               'K','R1','R2','CI',
               'DI','CF','DF','CIF','L',
               'S','T','ST']
    #scalelist=['CF','CIF','CI','C']

    for n in range(0,len(scalelist)):
        genscale(k+(1+n)*200,scalelist[n])

    img.save('DiagnosticPrint.png','PNG')
    img.show()

#--------- Stickering  (Requires Special Functions) ---------------

cutcolor = (0,0,255) #color which indicates CUT (blu)
d=1 #Delineate (yes or no)

def drawbox(image,x0,y0,dx,dy):
    img=image
    if d == 1:
        #(x1,y1) First corner of box
        # dx, dy extension of box in positive direction

        for x in range(x0,x0+dx):
            img.putpixel((x,y0),cutcolor)
            img.putpixel((x,y0+dy),cutcolor)

        for y in range(y0,y0+dy):
            img.putpixel((x0,y),cutcolor)
            img.putpixel((x0+dx,y),cutcolor)

wE=20 #width of extension cross arms

def drawcorners(image,x1,y1,x2,y2):
    img=image
    if d == 1:
        #(x1,y1) First corner of box
        #(x2,y2) Second corner of box
        
        for x in range (x1-wE,x1+wE):
            img.putpixel((x,y1),cutcolor)
            img.putpixel((x,y2),cutcolor)
        for x in range (x2-wE,x2+wE):
            img.putpixel((x,y1),cutcolor)
            img.putpixel((x,y2),cutcolor)
        for y in range (y1-wE,y1+wE):
            img.putpixel((x1,y),cutcolor)
            img.putpixel((x2,y),cutcolor)
        for y in range (y2-wE,y2+wE):
            img.putpixel((x1,y),cutcolor)
            img.putpixel((x2,y),cutcolor)

def transcribe(x0,y0,dx,dy,xT,yT):

        #(x0,y0) First corner of SOURCE (rendering)
        #(dx,dy) Width and Length of SOURCE chunk to transcribe
        #(xT,yT) Target corner of DESTINATION; where to in-plop (into stickerprint)

        for x in range(0,dx):
            for y in range(0,dy):
                r, g, b = img.getpixel((x0+x,y0+y))
                img2.putpixel((xT+x,yT+y),(r,g,b))

if stickerprint == 1:

    # Code Names
    #(fs) | UL,UM,UR [ ML,MM,MR ] LL,LM,LR | 
    #(bs) | UL,UM,UR [ ML,MM,MR ] LL,LM,LR |
    # Upper Middle Lower, Left Middle Right
    # (18 total stickers)

    oX2=50 #x dir margins
    oY2=50 #y dir margins 
    oA=50 #overhang amount
    ext=20 #extension amount
    width = 6500+2*oX2
    height = 5075

    img2=Image.new('RGB',(width,height),'white') 
    draw=ImageDraw.Draw(img2)

    #fsUM,MM,LM:
    l=0

    l=oY2+oA
    transcribe(oX+750,oY,6500,480,oX2,l)
    extend(img2,l+480-1,'down',ext)
    drawcorners(img2,oX2,l-oA,oX2+6500,l+480)
    
    l=l+480+oA
    transcribe(oX+750,oY+481,6500,640,oX2,l)
    extend(img2,l+1,'up',ext)
    extend(img2,l+640-1,'down',ext)
    drawcorners(img2,oX2,l,oX2+6500,l+640)

    l=l+640+oA
    transcribe(oX+750,oY+1120,6500,480,oX2,l)
    extend(img2,l+1,'up',ext)
    extend(img2,l+480-1,'down',ext)
    drawcorners(img2,oX2,l,oX2+6500,l+480+oA)

    #bsUM,MM,LM:

    l=l+480+oA+oA+oA

    transcribe(oX+750,oY+1600+oY,6500,480,oX2,l)
    extend(img2,l+480-1,'down',ext)
    drawcorners(img2,oX2,l-oA,oX2+6500,l+480)

    l=l+480+oA
    transcribe(oX+750,oY+1600+oY+481-3,6500,640,oX2,l)
    extend(img2,l+1,'up',ext)
    extend(img2,l+640-1,'down',ext)
    drawcorners(img2,oX2,l,oX2+6500,l+640)

    l=l+640+oA
    transcribe(oX+750,oY+1600+oY+1120,6500,480,oX2,l)
    extend(img2,l+1,'up',ext)
    extend(img2,l+480-1,'down',ext)
    drawcorners(img2,oX2,l,oX2+6500,l+480+oA)

    yB=3720

    box=[
            [oA,yB,
             510+oA,480+oA],
            [510+3*oA,yB,
            750+oA,640],
            [510+750+5*oA,yB,
            750+oA,480+oA]
        ]

    for i in range(0,3):
        drawbox(img2,box[i][0],box[i][1],box[i][2],box[i][3])
        drawbox(img2,box[i][0],box[i][1]+640+oA,box[i][2],box[i][3])
        
        box[i][0] = round(2*(6.5*oA+510+2*750)-box[i][0]-box[i][2])

        drawbox(img2,box[i][0],box[i][1],box[i][2],box[i][3])
        drawbox(img2,box[i][0],box[i][1]+640+oA,box[i][2],box[i][3])

    points=[
              [2*oA+120,yB+oA+160],
              [6*oA+510+750  +2*160,yB   +160],
              [6*oA+510+750    +160,yB +2*160],

              [2*oA+120,yB+640+oA +160],
              [6*oA+510+750  +160,yB+640+oA   +oA+2*160],
              [6*oA+510+750    +2*160,yB+640+oA +oA+160]
          ]
    
    r=34 #(2.5mm diameter)
    
    for i in range(0,6):
        draw.ellipse((points[i][0]-r,points[i][1]-r,
                      points[i][0]+r,points[i][1]+r),
                      fill = 'white',
                      outline = cutcolor)        

        points[i][0] = round(2*(6.5*oA+510+2*750)-points[i][0])

        draw.ellipse((points[i][0]-r,points[i][1]-r,
                      points[i][0]+r,points[i][1]+r),
                      fill = 'white',
                      outline = cutcolor)

    img2.save('StickerCutLINED.png','PNG')
    img2.show()

print ("The program took", time.time() - start_time, "to run")

#--------------------------EXTRABITZ----------------------------

# A B C D K R1 R2 CI DI CF DF L S T ST
# Layout:
# |  K,  A  [ B, T, ST, S ] D,  DI    |
# |  L,  DF [ CF,CIF,CI,C ] D, R1, R2 |

#To-Do:
    #Graphical Description of how the scales are constructed

    #maybe an easy to use interface for customizations. . nah

    #MODEL 1000 -- LEFT HANDED LIMACON 2020 -- KWENA & TOOR CO.S
