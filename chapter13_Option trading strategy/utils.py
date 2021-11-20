def BTM_Nstep(S,K,sigma,r,T,N,types):
    '''Define a function to calculate European option price using N steps binomial tree.
    S:underlying price at t0
    K:strike price
    sigma:volatility of underlying asset return(annualized)
    r:risk free rate(continuous compound)
    T:tenor in year
    N:number of step in the BTM model
    types:option type. 'call'indicates call option, otherwise put option'''
    from math import factorial
    from numpy import exp,maximum,sqrt
    t=T/N
    u=exp(sigma*sqrt(t))
    d=1/u
    p=(exp(r*t)-d)/(u-d)
    N_list=range(0,N+1)
    A=[]
    for j in N_list:
        C_Nj=maximum(S*pow(u,j)*pow(d,N-j)-K,0)
        Num=factorial(N)/(factorial(j)*factorial(N-j))
        A.append(Num*pow(p,j)*pow(1-p,N-j)*C_Nj)
    call=exp(-r*T)*sum(A)
    put=call+K*exp(-r*T)-S
    if types=='call':
        value=call
    else:
        value=put
    return value