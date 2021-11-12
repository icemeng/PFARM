import numpy as np

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
