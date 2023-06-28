#!/usr/bin/env python
# coding: utf-8

# In[1]:


import itertools
from collections import defaultdict
import sys


# In[2]:


var_dict = {}
rev_dict = {}
last_id = 1
product_num = 0


# In[3]:


def parse_edge_string(edge_string):
    edge_string = edge_string.strip().strip("e_{").strip("}")
    i, j = map(int, edge_string.split(","))
    return (i, j)


# In[4]:


def add_var_id(x, old_id=None):
    global last_id, var_dict, rev_dict
    xlast_id = 'x' + str(last_id)
    if old_id != None:
        var_dict[x] = old_id
        return
    var_dict[x] = xlast_id
    x = x + '}'
    x = x[0] + '_{' + x[1:]
    rev_dict[xlast_id] = x
    rev_dict['-' + xlast_id] = x
    last_id += 1
    return xlast_id


# In[5]:


def srg(n, K, la, mu):
    global product_num
    clauses = []
    
    for i, j in itertools.combinations(range(n), 2):
        edge_id = add_var_id(f"e{i},{j}")
        add_var_id(f"e{j},{i}", edge_id)
    
    for i in range(n):
        for j in range(i + 1, n):
            edge = var_dict[f"e{i},{j}"]
            la_clause = f"-{la} {edge}"
            mu_clause = f"+{mu} {edge}"
            for k in range(n):
                if k == i or k == j:
                    continue
                edge_1 = var_dict[f"e{i},{k}"]
                edge_2 = var_dict[f"e{k},{j}"]
                la_clause = la_clause + f" +1 {edge} {edge_1} {edge_2}"
                product_num += 1
                mu_clause = mu_clause + f" +1 {edge_1} {edge_2} -1 {edge} {edge_1} {edge_2}"
                product_num += 1
            la_clause += f" = 0"
            mu_clause += f" = {mu}"
            clauses.append(la_clause)
            clauses.append(mu_clause)
    
#     regularity
    for i in range(n):
        clause = ""
        for j in range(n):
            if j == i:
                continue
            e = var_dict[f"e{i},{j}"]
            clause = clause + f"+1 {e} "
        clause = clause + f"= {K}"
        clauses.append(clause)
    
    return clauses


# In[6]:


def clause_to_opb(clauses):
    pb_str = f"* #variable= {last_id - 1} #constraint= {len(clauses)} #product= {product_num} sizeproduct= {last_id - 1}\nmin: ;\n"
    print(last_id - 1, len(clauses))
    pb_str = pb_str + ';\n'.join(clauses) + ';\n'
    with open(f'srg_to_nonlinear_pseudoboolean_regularity_lambda_mu/{N}K{K}L{LAMBDA}M{MU}.opb', 'w') as f:
        f.write(pb_str)
    print("should be done ...")
    return pb_str


# In[7]:


N, K, LAMBDA, MU = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
print(f"------- start{N}-{K}-{LAMBDA}-{MU}")
c = srg(N,K, LAMBDA, MU)
opb_file = clause_to_opb(c)
print("------- end\n")

# In[ ]:




