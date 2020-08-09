from tkinter import *
from sympy import *

expression=""
x,y,z=symbols('x y z')
number=[]

def press(num):
    global expression,number
    number.append(num)
    expression=expression+num
    equation.set(expression)

def ok():
    try: 
        global expression
        total=eval(str(expression))
        if '/(0)' in expression:
            raise ZeroDivisionError
        menu()
    except ZeroDivisionError:
        equation.set(" Error")
    except:
        menu()

def delete():
    result.set("")
    fact.set(" ")
    try:
        global expression,number
        t=expression
        x=number.pop()
        expression=t[:len(expression)-len(x)]
        equation.set(expression)
    except IndexError:
        pass
    
def clear():
    global expression
    result.set("")
    fact.set(" ")
    expression=""
    equation.set("")
    
def menu():
    v=IntVar()
    Radiobutton(gui,text="Check Continuity  ",variable=v,value=1,command=isContinuous, height=1,width=25,anchor=W).place(x=30,y=80)
    Radiobutton(gui,text="Check Differentiability ",variable=v,value=2,command=isDiff, height=1,width=25,anchor=W).place(x=30,y=115)
    Radiobutton(gui,text="Check Analyticity ",variable=v,value=3,command=isAnalytic, height=1,width=25,anchor=W).place(x=30,y=150)
    Radiobutton(gui,text="Check Conformality ",variable=v,value=4,command=isConformal, height=1,width=25,anchor=W).place(x=30,y=185)
    Radiobutton(gui,text="Find orthagonal trajectory",variable=v,value=5,command=ortho, height=1,width=25,anchor=W).place(x=30,y=220)
    Radiobutton(gui,text="Find Residues at Poles ",variable=v,value=6,command=findresidue, height=1,width=25,anchor=W).place(x=30,y=255)
    Radiobutton(gui,text="Find Integration ",variable=v,value=7,command=Integrate, height=1,width=25,anchor=W).place(x=30,y=290)

def isContinuous():
    result.set('')
    fact.set('')
    global expression
    a=Continuous(expression)
    e="Dis-Continuous Function\nPoints of Discontinuity: "+str(a[1])
    if a[0]==1:
        result.set(e)
    else:
        result.set("Continuous Function")
    fact.set("A function is continuous if it does not have any point of discontinuity all over its domain.\nThe points of discontinuity have unequal left and right limits.")
            
def Continuous(f):
    result.set("")
    count=0
    s=[]
    for i in range(len(f)):
        if f[i]=='/':
            temp=0
            while i<=len(f)-2:
                if f[i+1]=='(':
                    if count==0:
                        temp=1
                        s.append(i+1)
                    count=count+1
                if f[i+1]==')':
                    count=count-1
                    if count==0:
                        s.append(i+1)
                        break
                i=i+1
    try:
        flag=0
        sol=set()
        for i in range(0,len(s),2):
            d=f[s[i]:s[i+1]+1]
            d=expand(d)
            sol=sol|set(solve(d,z, domain =S.Complexes))
            if(len(sol)):
                flag=1
        if flag:
            b=[1,sol]
            return b
        else:
            b=[0,sol]       #If continuous returns 0
            return b        #else returns 1
    except IndexError:      
       b=[0,sol]
       return b

def isDiff():
    global expression
    c=Diff(expression, z)
    e="Function not derivable at: "+str(c[1])+"\nDerivarive at other points: "+str(c[2])
    if c[0]!=0:
        result.set(e)
    else:
        result.set("Differentiable Function at all points\nDerivative: "+str(c[2]))
    fact.set("A continous function which has equal right and left derivatives is differentiable.\nAt the points of discontinuity of the function and the differentiated function, derivative doesn't exist.")
    
def Diff(f1, var):
    d3=[]
    result.set("")
    fact.set("")
    d1=Continuous(f1)
    expression1=diff(f1, var)
    d2=Continuous(str(expression1))
    d3.append(d1[0]+d2[0])
    d3.append(set(d2[1]|d1[1]))
    d3.append(expression1)
    return d3

def isAnalytic():
    global expression
    a=Analytic(expression)
    result.set("")
    fact.set("")
    if(a[0]==0 and a[1]==0) or a[0]==3:
        result.set("Analytic Function")
    elif(a[0]==0):
        e="Analytic Function except at points "+str(a[1])
        result.set(e)
    #elif(a[0]==2):
     #   result.set("Yet to Calculate")
    else:
        result.set("CR equations failed.\nThus, not analytic")
    if '1/(z)' in expression:
        result.set("Analytic Function except at point 0")
    fact.set("A differentiable function whose real and imaginary derivatives are continuous over its neighbourhood,\nand satisfying CR Equations are Analytic.\nAnalyticity of a Function fails at its singular points")
        
def Analytic(d1):
    d=d1
    l=[]
    l1=0
    f=0
    h=0
    g=0
    for i in range(len(d)):
        count=0
        if d[i]=='/':
            for j in range(i, len(d)):
                if d[j]=='(':
                    count+=1
                    if count==1:
                        l1=j
                elif d[j]==')':
                    count-=1
                elif d[j]=='z':
                    if count!=0 and '1/(z)' not in d[l1-2:j+2] and '1/(z+' not in d[l1-2:j+3] and '1/(z-' not in d[l1-2:j+3] and 'z/(z^2)' not in d[l1-2:j+5]:
                        f=1
                        break;
                    if '1/(z)' in d[l1-2:j+2] or '1/(z+' in d[l1-2:j+3] or '1/(z-' in d[l1-2:j+3] or 'z/(z^2)' in d[l1-2:j+5]:
                        g=1
                        break;
        if f==1:
            break
        if d[i]=='l' or d[i]=='e':
            f=2
            break
        if d[i]=='s' or d[i]=='c' or d[i]=='t':
            h=1
            for k in range(i, len(d)):
                if d[k]=='/':
                    for j in range(k, len(d)):
                        if d[j]=='(':
                            count+=1
                        elif d[j]==')':
                            count-=1
                        elif d[j]=='z':
                            if count!=0:
                                f=1
                                break
                        if count==0:
                            break
                    if f==1:
                        break
            a=[2]
    if h==1 and f==0 or f==2 or g==1:
        a=[3]
        return a
    if h==1 and f==1 or f==1:
        a=[4]
        return a
    f=0
    for i in range(len(d)):
        if d[i]=='z':
            f=1
            l.append(i)
    if f==1:
        l.append(len(d)-1)
        t=d[:l[0]]
        for i in range(len(l)-1):
            t=t+"(x+(sqrt(-1)*y))"
            t=t+d[l[i]+1:l[i+1]+1]
        d=str(expand(t))
# =============================================================================
#      conjugate
# =============================================================================
    a=[0]
    j=0
    real=[]
    flag=0
    img=[]
    d=d+" +"
    sym='+'
    idx=0
    for i in range(len(d)):
        flag=0
        if d[i]=='+' or d[i]=='-':
            t=d[a[j]:i-1]
            for k in range(0,len(t)):
                if t[k]=='I':
                    t=t[:k]+'1'+t[k+1:]
                    flag=1;
            t=sym+t;
            if flag==1:
                img.append(t)
            else:
                real.append(t)
            a.append(i+2)
            j+=1
            sym=d[i];
    u=''
    v=''
    for i in range(len(real)):
        u=u+real[i]
    for i in range((len(img))):
        v=v+img[i]
    ux=Diff(u,x)
    if len(v)==0:
        v='0'
    vy=Diff(v,y)
    if ux[0]== 0 and vy[0]==0 and ux[2] == vy[2]:
        vx=Diff(v,x)
        uy=Diff(u,y)
        if vx[0]==0 and uy[0]==0 and (-1)*vx[2] == uy[2]:
            a=Continuous(ux)
            b=Continuous(vx)
            c=Continuous(vy)
            d=Continuous(uy)
            if a[0]==0 and b[0]==0 and c[0]==0 and d[0]==0:
                a=[0, 0]
                return a
            else:
                e=[0, set(a[1]|b[1]|c[1]|d[1]|ux[1]|vx[1]|uy[1]|vy[1])]
                return e
        a=[1,1]
        return a
    else:
        a=[1,1]
        return a
        
def isConformal():
    global expression
    result.set("")
    fact.set("")
    a=Conformal(expression)
    if a==1:
        e="Conformal Function"
    else:
        e="Not a Conformal Function"
    result.set(e)
    fact.set("Analytic Functions whose First Derivative is Non-Zero are Conformal.")
    
def Conformal(f):
    a=Analytic(f)
    if(a[0]==0 and a[1]==0 or a[0]==3):
        e=diff(f,z)
        if(e !=0):
            return 1
    return 0

def ortho():
    global expression
    result.set("")
    fact.set("")
    fo=diff(expression,z)
    fo=(-1/fo)
    fi=integrate(fo,z)
    result.set("Orthogonal Trajectory Function:\n"+str(fi))
    fact.set("An Orthogonal Trajectory of a Function is that family of curves which intersect the function at right angles.")
    
def residue(expr, z, z0):
    expr = sympify(expr)
    if z0 != 0:
        expr = expr.subs(z, z + z0)
    for n in [0, 1, 2, 4, 8, 16, 32]:
        if n == 0:
            s = expr.series(z, n=0)
        else:
            s = expr.nseries(z, n=n)
        if s.has(Order) and s.removeO() == 0:
            # bug in nseries
            continue
        if not s.has(Order) or s.getn() >= 0:
            break
    if s.has(Order) and s.getn() < 0:
        raise NotImplementedError('Bug in nseries?')
    s = collect(s.removeO(), z)
    if s.is_Add:
        args = s.args
    else:
        args = [s]
    res = S(0)
    for arg in args:
        c, m = arg.as_coeff_mul(z)
        m = Mul(*m)
        if not (m == 1 or m == z or (m.is_Pow and m.exp.is_Integer)):
            raise NotImplementedError('term of unexpected form: %s' % m)
        if m == 1/z:
            res += c
    return res

def findresidue():
    global expression
    result.set("")
    fact.set("")
    f=expression
    count=0
    s=[]
    for i in range(len(f)):
        if f[i]=='/':
            temp=0
            while i<=len(f)-2:
                if f[i+1]=='(':
                    if count==0:
                        temp=1
                        s.append(i+1)
                    count=count+1
                if f[i+1]==')':
                    count=count-1
                    if count==0:
                        s.append(i+1)
                        break
                i=i+1
    sol=set()
    for i in range(0,len(s),2):
        d=f[s[i]:s[i+1]+1]
        d=expand(d)
        sol=sol|set(solve(d,z, domain =S.Complexes))
    sol=list(sol)
    res=[]
    flag =0
    e="Poles\tResidues\n"
    for i in range(0,len(sol)):
        flag=1
        res.append(residue(f,z,sol[i]))
        e=e+str(sol[i])+"\t"+str(res[i])+'\n'
    if flag==0:
        e="No Residues"
    result.set(e)
    fact.set("The Points of the function, where the function ceases to be analytic (value of function not defined) are Poles.\nResidue of the Pole is the Coefficient of the Pole in its Laurent Series Expansion.")
    if(flag):
        y=[flag,res, e]
    else:
        y=[flag]
    return y

def Integrate():
    global expression
    result.set("")
    fact.set("")
    w=findresidue()
    fact.set("")
    if(w[0]):
        intres=2*pi*I*sum(w[1])
        result.set(w[2]+"\nIntegration: "+str(intres))
    else:
        intres=0
        result.set("Integration: 0")
    abc="Contour Integration of a function is the product of 2"+chr(960)+"i and the sum of all its residues"
    fact.set(abc)

#Driver Code
gui = Tk() 
gui.configure(background="black") 
gui.title('Complex Functions') 
gui.geometry("1500x700") 
T=Text(gui,height=1,width=10,bg='black',fg='white',bd=0,font=16)
T.insert(END,'FUNCTION:')
T.place(x=290,y=33) 
equation=StringVar()
expression_field=Entry(gui,textvariable=equation,width=32,font=10)
expression_field.place(x=410, y=35) 
equation.set('')
T3=Text(gui,height=1,width=10,bg='black',fg='white',bd=0,font=40)
T3.insert(END,'INPUT')
T3.place(x=1026,y=60)
button1=Button(gui,text=' 1 ',fg='black',bg='white',command=lambda: press('1'),height=1,width=7) 
button1.place(x=900,y=90) 
button2=Button(gui,text=' 2 ',fg='black',bg='white',command=lambda: press('2'),height=1,width=7) 
button2.place(x=963,y=90) 
button3=Button(gui,text=' 3 ',fg='black',bg='white',command=lambda: press('3'),height=1,width=7) 
button3.place(x=1026,y=90) 
button4=Button(gui,text=' 4 ',fg='black',bg='white',command=lambda: press('4'),height=1,width=7) 
button4.place(x=900,y=120) 
button5=Button(gui,text=' 5 ',fg='black',bg='white',command=lambda: press('5'),height=1,width=7) 
button5.place(x=963,y=120) 
button6=Button(gui,text=' 6 ',fg='black',bg='white',command=lambda: press('6'),height=1,width=7) 
button6.place(x=1026,y=120)
button7=Button(gui,text=' 7 ',fg='black',bg='white',command=lambda: press('7'),height=1,width=7) 
button7.place(x=900,y=150) 
button8=Button(gui,text=' 8 ',fg='black',bg='white',command=lambda: press('8'),height=1,width=7) 
button8.place(x=963,y=150)
button9=Button(gui,text=' 9 ',fg='black',bg='white',command=lambda: press('9'),height=1,width=7) 
button9.place(x=1026,y=150)
dot=Button(gui,text=' . ',fg='black',bg='white',command=lambda: press('.'),height=1,width=7) 
dot.place(x=1026,y=180)
button0=Button(gui,text=' 0 ',fg='black',bg='white',command=lambda: press('0'),height=1,width=7) 
button0.place(x=963,y=180)
buttonI=Button(gui,text=' i ',fg='black',bg='white',command=lambda: press('i'),height=1,width=7) 
buttonI.place(x=900,y=180)
plus=Button(gui,text=' + ',fg='black',bg='white',command=lambda: press("+"),height=1,width=7) 
plus.place(x=1089,y=90) 
minus=Button(gui,text=' - ',fg='black',bg='white',command=lambda: press("-"),height=1,width=7) 
minus.place(x=1089,y=120) 
multiply=Button(gui,text=' * ',fg='black',bg='white',command=lambda: press("*"),height=1,width=7) 
multiply.place(x=1089,y=150) 
divide=Button(gui,text=' / ',fg='black',bg='white',command=lambda: press("/("),height=1,width=7) 
divide.place(x=1089,y=180)
ok=Button(gui,text=' OK ',fg='black',bg='white',command=ok,height=1,width=7) 
ok.place(x=1152,y=240)
power=Button(gui,text=' ^ ',fg='black',bg='white',command=lambda: press('^'),height=1,width=7) 
power.place(x=1089,y=210)
openb=Button(gui,text=' ( ',fg='black',bg='white',command=lambda: press('('),height=1,width=7) 
openb.place(x=1152,y=90)
closeb=Button(gui,text=' ) ',fg='black',bg='white',command=lambda: press(')'),height=1,width=7) 
closeb.place(x=1152,y=120)
sin=Button(gui,text=' sin ',fg='black',bg='white',command=lambda: press('sin('),height=1,width=7) 
sin.place(x=1152,y=150)
cos=Button(gui,text=' cos ',fg='black',bg='white',command=lambda: press('cos('),height=1,width=7) 
cos.place(x=1152,y=180)
tan=Button(gui,text=' tan ',fg='black',bg='white',command=lambda: press('tan('),height=1,width=7) 
tan.place(x=1152,y=210)
buttonZ=Button(gui,text=' z ',fg='black',bg='white',command=lambda: press('z'),height=1,width=7) 
buttonZ.place(x=900,y=210)
buttonE=Button(gui,text=' exp ',fg='black',bg='white',command=lambda: press('exp('),height=1,width=7) 
buttonE.place(x=963,y=210)
log=Button(gui,text=' log ',fg='black',bg='white',command=lambda: press('log('),height=1,width=7) 
log.place(x=1026,y=210)
buttonpi=Button(gui,text=chr(960),fg='black',bg='white',command=lambda: press(chr(960)),height=1,width=7) 
buttonpi.place(x=1089,y=240)
buttondelete=Button(gui,text=' Del ',fg='black',bg='white',command=delete,height=1,width=7) 
buttondelete.place(x=1026,y=240)
clear=Button(gui,text='Clear',fg='black',bg='white',command=clear,height=1,width=16) 
clear.place(x=900,y=240)

v=IntVar()
T2=Text(gui,height=1,width=10,bg='black',fg='white',bd=0,font=40)
T2.insert(END,'MENU')
T2.place(x=99,y=50)
Radiobutton(gui,text="Check Continuity  ",variable=v,value=1, height=1,width=25,anchor=W).place(x=30,y=80)
Radiobutton(gui,text="Check Differentiability ",variable=v,value=2, height=1,width=25,anchor=W).place(x=30,y=115)
Radiobutton(gui,text="Check Analyticity ",variable=v,value=3, height=1,width=25,anchor=W).place(x=30,y=150)
Radiobutton(gui,text="Check Conformality ",variable=v,value=4, height=1,width=25,anchor=W).place(x=30,y=185)
Radiobutton(gui,text="Find orthagonal trajectories",variable=v,value=5, height=1,width=25,anchor=W).place(x=30,y=220)
Radiobutton(gui,text="Find Residues at Poles ",variable=v,value=6, height=1,width=25,anchor=W).place(x=30,y=255)
Radiobutton(gui,text="Find Integration ",variable=v,value=7, height=1,width=25,anchor=W).place(x=30,y=290)

T1=Text(gui,height=1,width=10,bg='black',fg='white',bd=0,font=40)
T1.insert(END,'RESULT')
T1.place(x=520,y=90)

result=StringVar()
w=Label(gui,textvariable=result,height=10,width=50,font=15) 
w.place(x=290,y=120)
result.set('')

T5=Text(gui,height=1,width=10,bg='black',fg='white',bd=0,font=40)
T5.insert(END,'NOTE')
T5.place(x=535,y=400)

fact=StringVar()
W1=Label(gui,textvariable=fact,height=6,width=90,font=15) 
W1.place(x=120,y=430)
fact.set('')

gui.mainloop()