import pandas as pd
import pulp 


stock_df = pd.read_csv('stocks.csv')
requires_df = pd.read_csv('requires.csv')
gains_df = pd.read_csv('gains.csv')


stock_df.head()


requires_df.head()


gains_df.head()


#原材料の添字集合
M = list(stock_df['m'])
#製品の添字集合
P = list(gains_df['p'])


stock = {row.m:row.stock for row in stock_df.itertuples()}


stock


require = {(row.p, row.m) : row.require for row in requires_df.itertuples()}


require


gain = {row.p : row.gain for row in gains_df.itertuples()}


problem = pulp.LpProblem('LP', pulp.LpMaximize)
#決定変数は生産量 P_i
# LpVariableのdictionaryを作成
x = pulp.LpVariable.dicts('x', P, cat='Continuous')
for p in P:
    problem += x[p] >= 0
for m in M:
    problem += pulp.lpSum([require[p,m] * x[p] for p in P]) <= stock[m]
problem += pulp.lpSum([gain[p] * x[p] for p in P])    
status = problem.solve()
print("Status : ", pulp.LpStatus[status])
#print(pulp.LpStatus)
for p in P:
    print(f"Optimal sol x{p} : ", x[p].value())
print(f"Optimal value : {problem.objective.value()}")    


problem = pulp.LpProblem('LP', pulp.LpMaximize)
#決定変数は生産量 P_i
x = pulp.LpVariable.dicts('x', P, cat='Integer')
for p in P:
    problem += x[p] >= 0
for m in M:
    problem += pulp.lpSum([require[p,m] * x[p] for p in P]) <= stock[m]
problem += pulp.lpSum([gain[p] * x[p] for p in P])    
status = problem.solve()
print("Status : ", pulp.LpStatus[status])
print(pulp.LpStatus)
for p in P:
    print(f"Optimal sol x{p} : ", x[p].value())
print(f"Optimal value : {problem.objective.value()}")    



