def swap_rate(m,y,T):
    '''Define a function to calculate swap rate.
    m:payment frequency per year
    y:continuous compound zero rate(discount rate), input as array
    T:contract tenor in year'''
    import numpy as np
    n_list=np.arange(1,m*T+1)
    t=n_list/m
    q=np.exp(-y*t)
    rate=m*(1-q[-1])/np.sum(q)
    return rate