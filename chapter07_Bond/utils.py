import numpy as np

def Rc(Rm,m):
    '''Define a function that when Rm and m frequency are known, calculate continuous IR
    Rm: IR of m frequency
    m: Compound frequency'''
    r=m*np.log(1+Rm/m)
    return r

def Rm(Rc,m):
    '''Define a function that when continuous IR is known, calculate IR of m frequency
    Rc: Continuous compound IR
    m: Compound frequency'''
    r=m*(np.exp(Rc/m)-1)
    return r

def Bondprice_onediscount(C,M,m,y,t):
    '''Define a function to calculating bond price based on single discount rate
    C:coupon rate. 0 indicates zero coupon
    M:face value of bond
    m:payment frequency per year
    y:discount rate
    t:array of time to coupon payment. Single number indicates zero coupon'''
    if C==0:
        price=np.exp(-y*t)*M
    else:
        coupon=np.ones_like(t)*M*C/m
        NPV_coupon=np.sum(coupon*np.exp(-y*t))
        NPV_par=M*np.exp(-y*t[-1])
        price=NPV_coupon+NPV_par
    return price

def YTM(P,C,M,m,t):
    '''Define a function for calculating bond YTM
    P:bond price observed in market
    C:coupon rate. 0 indicates zero coupon
    M:face value of bond
    m:payment frequency per year
    t:array of time to coupon payment. Single number indicates zero coupon'''
    import scipy.optimize as so
    def f(y):
        coupon=np.ones_like(t)*M*C/m
        NPV_coupon=np.sum(coupon*np.exp(-y*t))
        NPV_par=M*np.exp(-y*t[-1])
        value=NPV_coupon+NPV_par
        return value-P
    if C==0:
        y=(np.log(M/P))/t
    else:
        y=so.fsolve(func=f,x0=0.1)#the second parameter is initial value
    return y

def Bondprice_deffdiscount(C,M,m,y,t):
    '''Define a function to calculating bond price based on multiple term discount rate
    C:coupon rate. 0 indicates zero coupon
    M:face value of bond
    m:payment frequency per year
    y:array of discount rate in different term. Single number indicates zero coupon
    t:array of time to coupon payment. Single number indicates zero coupon'''
    if C==0:
        price=np.exp(-y*t)*M
    else:
        coupon=np.ones_like(y)*M*C/m
        NPV_coupon=np.sum(coupon*np.exp(-y*t))
        NPV_par=M*np.exp(-y[-1]*t[-1])
        price=NPV_coupon+NPV_par
    return price

def Mac_Duration(C,M,m,y,t):
    '''Define a function for calculating Macaulay duraion of a bond
    C:coupon
    M:par of bond
    m:coupon payment frequency per year
    y:YTM(continuous compound) 
    t:array of time to coupon payment date. Single number indicates zero rate bond'''
    if C==0:
        duration=t
    else:
        coupon=np.ones_like(t)*M*C/m
        NPV_coupon=np.sum(coupon*np.exp(-y*t))
        NPV_par=M*np.exp(-y*t[-1])
        Bond_value=NPV_coupon+NPV_par
        cashflow=coupon
        cashflow[-1]=M*(1+C/m)
        weight=cashflow*np.exp(-y*t)/Bond_value
        duration=np.sum(t*weight)
    return duration

def Mod_Duration(C,M,m1,m2,y,t):
    '''Define a function for calculating Modified duraion of a bond
    C:coupon
    M:par of bond
    m1:coupon payment frequency per year
    m2:compound frequency per year of YTM, ordinary m2=m1
    y:YTM(compound m2 times per year) 
    t:array of time to coupon payment date. Single number indicates zero rate bond'''
    if C==0:
        Macaulay_duration=t
    else:
        r=m2*np.log(1+y/m2) #continuous compound
        coupon=np.ones_like(t)*M*C/m1
        NPV_coupon=np.sum(coupon*np.exp(-r*t))
        NPV_par=M*np.exp(-r*t[-1])
        price=NPV_coupon+NPV_par
        cashflow=coupon
        cashflow[-1]=M*(1+C/m1)
        weight=cashflow*np.exp(-r*t)/price
        Macaulay_duration=np.sum(t*weight)
    Modified_duration=Macaulay_duration/(1+y/m2)
    return Modified_duration

def Dollar_Duration(C,M,m1,m2,y,t):
    '''Define a function for calculating Modified duraion of a bond
    C:coupon
    M:par of bond
    m1:coupon payment frequency per year
    m2:compound frequency per year of YTM, ordinary m2=m1
    y:YTM(compound m2 times per year) 
    t:array of time to coupon payment date. Single number indicates zero rate bond'''
    r=m2*np.log(1+y/m2)
    if C==0:
        price=M*np.exp(-r*t)
        Macaulay_D=t
    else:
        coupon=np.ones_like(t)*M*C/m1
        NPV_coupon=np.sum(coupon*np.exp(-r*t))
        NPV_par=M*np.exp(-r*t[-1])
        price=NPV_coupon+NPV_par
        cashflow=coupon
        cashflow[-1]=M*(1+C/m1)
        weight=cashflow*np.exp(-r*t)/price
        Macaulay_D=np.sum(t*weight)
    Modified_D=Macaulay_D/(1+y/m2)
    Dollar_D=price*Modified_D
    return Dollar_D

def Convexity(C,M,m,y,t):
    '''Define a function for calculating Macaulay duraion of a bond
    C:coupon
    M:par of bond
    m:coupon payment frequency per year
    y:YTM(continuous compound) 
    t:array of time to coupon payment date. Single number indicates zero rate bond'''
    if C==0:
        convexity=pow(t,2)
    else:
        coupon=np.ones_like(t)*M*C/m
        NPV_coupon=np.sum(coupon*np.exp(-y*t))
        NPV_par=M*np.exp(-y*t[-1])
        Bond_value=NPV_coupon+NPV_par
        cashflow=coupon
        cashflow[-1]=M*(1+C/m)
        weight=cashflow*np.exp(-y*t)/Bond_value
        convexity=np.sum(pow(t,2)*weight)
    return convexity