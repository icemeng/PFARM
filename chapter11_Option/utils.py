def binomial_grid(n):
    import networkx as nx
    G = nx.Graph()
    for i in range(0, n + 1):
        for j in range(1, i + 2):
            if i < n:
                G.add_edge((i, j), (i + 1, j))
                G.add_edge((i, j), (i + 1, j + 1))

    posG = {}
    for node in G.nodes():
        posG[node] = (
         node[0], n + 2 + node[0] - 2 * node[1])

    nx.draw(G, pos=posG)
    
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