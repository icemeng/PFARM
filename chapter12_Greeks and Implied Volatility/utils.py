def option_BSM(S,K,sigma,r,T,opt):
    '''Define a function to calculate European option price using BSM model.
    S:underlying price
    K:strike price
    sigma:volatility of underlying return(annualized)
    r:risk free rate(continuous compound)
    T:tenor of option in year
    opt:option type. 'call'indicates call option, otherwise put option '''
    from numpy import log, exp, sqrt
    from scipy.stats import norm
    
    d1=(log(S/K)+(r+pow(sigma,2)/2)*T)/(sigma*sqrt(T))
    d2=d1-sigma*sqrt(T)
    if opt=='call':
        value=S*norm.cdf(d1)-K*exp(-r*T)*norm.cdf(d2)
    else:
        value=K*exp(-r*T)*norm.cdf(-d2)-S*norm.cdf(-d1)
    return value

def delta_EurOpt(S,K,sigma,r,T,optype,positype):
    '''Define a function to calculate delta of European option.
    S:underlying price
    K:strike price
    sigma:volatility of underlying asset return(annualized)
    r:risk free rate(continuous compound)
    T:tenor in year
    optype:type of option. 'call' indicates call option otherwise put option
    positype:type of position. 'long' indicates long position otherwise short position'''
    from scipy.stats import norm
    from numpy import log,sqrt
    
    d1=(log(S/K)+(r+pow(sigma,2)/2)*T)/(sigma*sqrt(T))
    if optype=='call':
        if positype=='long':
            delta=norm.cdf(d1)
        else:
            delta=-norm.cdf(d1)
    else:
        if positype=='long':
            delta=norm.cdf(d1)-1
        else:
            delta=1-norm.cdf(d1)
    return delta

def American_call(S,K,sigma,r,T,N):
    '''Define a function to calculate American call option price using N steps binomial tree.
    S:underlying price at t0
    K:strike price
    sigma:volatility of underlying asset return(annualized)
    r:risk free rate(continuous compound)
    T:tenor in year
    N:number of step in the BTM model'''

    import numpy as np
    
    # Step1:Calculate relevant parameters
    t=T/N
    u=np.exp(sigma*np.sqrt(t))
    d=1/u
    p=(np.exp(r*t)-d)/(u-d)
    call_matrix=np.zeros((N+1,N+1))
    
    # Step2:Calculate the underlying asset price and option value at the option maturity node
    N_list=np.arange(0,N+1)
    S_end=S*pow(u,N-N_list)*pow(d,N_list)
    call_matrix[:,-1]=np.maximum(S_end-K,0)
    
    #Step3:Calculate the underlying asset price and option value at the non maturity node of the option
    i_list=list(range(0,N))
    i_list.reverse()
    for i in i_list:
        j_list=np.arange(i+1)
        Si=S*pow(u,i-j_list)*pow(d,j_list)
        call_strike=np.maximum(Si-K,0)
        call_nostrike=(p*call_matrix[:i+1,i+1]+(1-p)*call_matrix[1:i+2,i+1])*np.exp(-r*t)
        call_matrix[:i+1,i]=np.maximum(call_strike,call_nostrike)
    call_begin=call_matrix[0,0]
    
    return call_begin

def American_put(S,K,sigma,r,T,N):
    '''Define a function to calculate American put option price using N steps binomial tree.
    S:underlying price at t0
    K:strike price
    sigma:volatility of underlying asset return(annualized)
    r:risk free rate(continuous compound)
    T:tenor in year
    N:number of step in the BTM model'''

    import numpy as np
    
    # Step1:Calculate relevant parameters
    t=T/N
    u=np.exp(sigma*np.sqrt(t))
    d=1/u
    p=(np.exp(r*t)-d)/(u-d)
    put_matrix=np.zeros((N+1,N+1))
    
    # Step2:Calculate the underlying asset price and option value at the option maturity node
    N_list=np.arange(0,N+1)
    S_end=S*pow(u,N-N_list)*pow(d,N_list)
    put_matrix[:,-1]=np.maximum(K-S_end,0)
    
    #Step3:Calculate the underlying asset price and option value at the non maturity node of the option
    i_list=list(range(0,N))
    i_list.reverse()
    for i in i_list:
        j_list=np.arange(i+1)
        Si=S*pow(u,i-j_list)*pow(d,j_list)
        put_strike=np.maximum(K-Si,0)
        put_nostrike=(p*put_matrix[:i+1,i+1]+(1-p)*put_matrix[1:i+2,i+1])*np.exp(-r*t)
        put_matrix[:i+1,i]=np.maximum(put_strike,put_nostrike)
    put_begin=put_matrix[0,0]
    return put_begin