#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import itertools
import subprocess
from collections import defaultdict
import math
import time
import sys


# In[ ]:


var_dict = {}
rev_dict = {}
last_id = 1


# In[ ]:


def parse_edge_string(edge_string):
    edge_string = edge_string.strip().strip("e_{").strip("}")
    i, j = map(int, edge_string.split(","))
    return (i, j)


# In[ ]:


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


# In[ ]:


def generate_clauses(edge, la, mu, triangles, angles):
    clauses = []
    clauses.append( f"+{mu} {edge} " + " ".join([f"+1 {x}" for x in angles]) + f" = {mu}" )
    clauses.append( f"-{la} {edge} " + " ".join([f"+1 {x}" for x in triangles]) + f" = 0" )
    return clauses


# In[ ]:


def srg(n, K, la, mu):
    angle = [[set() for j in range(n)] for i in range(n)]
    triangle = [[set() for j in range(n)] for i in range(n)]
    clauses = []
    
    for i, j in itertools.combinations(range(n), 2):
        edge_id = add_var_id(f"e{i},{j}")
        add_var_id(f"e{j},{i}", edge_id)
    
    # generate angle literals
    for i, j in itertools.combinations(range(n), 2):
        for k in range(n):
            if i == k or j == k:
                continue
            
            edge_0 = var_dict[f"e{i},{j}"]
            edge_1 = var_dict[f"e{i},{k}"]
            edge_2 = var_dict[f"e{j},{k}"]
            
            triangle_id = add_var_id(f"t{i},{j},{k}")
            triangle[i][j].add(triangle_id)
            
            angle_id = add_var_id(f"a{i},{j},{k}")
            angle[i][j].add(angle_id)
            
            clauses.append(f"+1 {triangle_id} -1 {edge_0} -1 {edge_1} -1 {edge_2} >= -2")
            clauses.append(f"-1 {triangle_id} +1 {edge_0} >= 0")
            clauses.append(f"-1 {triangle_id} +1 {edge_1} >= 0")
            clauses.append(f"-1 {triangle_id} +1 {edge_2} >= 0")
            
            clauses.append(f"+1 {angle_id} +1 {edge_0} -1 {edge_1} -1 {edge_2} >= -1")
            clauses.append(f"-1 {angle_id} -1 {edge_0} >= -1")
            clauses.append(f"-1 {angle_id} +1 {edge_1} >= 0")
            clauses.append(f"-1 {angle_id} +1 {edge_2} >= 0")
        
#     clauses.append(f"*end of preliminary clauses")
    
#     clauses.append(f"*srg-related clauses")
    for i in range(n):
        for j in range(i + 1, n):
            edge = var_dict[f"e{i},{j}"]
            clauses.extend(generate_clauses(edge, la, mu, triangle[i][j], angle[i][j]))
    
    # regularity clauses
    for i in range(n):
        clause = ""
        for j in range(n):
            if j == i:
                continue
            e = var_dict[f"e{i},{j}"]
            clause = clause + f"+1 {e} "
        clause = clause + f"= {K}"
        clauses.append(clause)
        
    for clause in clauses:
        ans = ''.join(clause)
        
    return clauses


# In[ ]:


def clause_to_opb(clauses):
    pb_str = f"* #variable= {last_id - 1} #constraint= {len(clauses)}\nmin: ;\n"
    print(last_id - 1, len(clauses))
    pb_str = pb_str + ';\n'.join(clauses) + ';\n'
    with open(f'srg_to_linear_pseudoboolean_regularity_lambda_mu/{N}K{K}L{LAMBDA}M{MU}.opb', 'w') as f:
        f.write(pb_str)
    print("should be done ...")
    return pb_str


# In[ ]:


N, K, LAMBDA, MU = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
print(f"------- start{N}-{K}-{LAMBDA}-{MU}")
c = srg(N,K, LAMBDA, MU)
opb_file = clause_to_opb(c)
print("------- end\n")

# In[ ]:




