#############################################
#
#       Definition (PPV and pax)
#
#Dewan Orang Ramai [10 cubes] = 240
#Dewan Orang Ramai [15 cubes] = 360
#Dewan Orang Ramai [20 cubes] = 480 
#Balai Komuniti [5 cubes] = 120
#Balai Komuniti [10 cubes] = 240 
#Balai Komuniti [15 cubes] = 360
#
#############################################



# Import libraries

import constraint
import pandas as pd
from random import randint
import streamlit as st

# Streamlit write-out

st.set_page_config(layout="wide")
st.image('asm.png')
st.header("Optimal PPV Combinations Calculation")
st.write('Capacity of each PPV:') 

PPV_capacity = {'PPV Type': ['Dewan Orang Ramai [10 cubes]', 'Dewan Orang Ramai [15 cubes]', 'Dewan Orang Ramai [20 cubes]', 'Balai Komuniti [5 cubes]', 'Balai Komuniti [10 cubes]', 'Balai Komuniti [15 cubes]'], 'Capacity': [240,360,480,120,240,360]}
st.write(pd.DataFrame.from_dict(PPV_capacity))

# ------------ Sidebar components --------------

st.sidebar.header('Optimization Parameters:')
cntDose = st.sidebar.number_input('Weekly Dose Volume', min_value=1000, value=5000)

cost_DOR10 = st.sidebar.number_input('Daily Cost Dewan Orang Ramai [10 cubes]', min_value=0, value=200)
cost_DOR15 = st.sidebar.number_input('Daily Cost Dewan Orang Ramai [15 cubes]', min_value=0, value=500)
cost_DOR20 = st.sidebar.number_input('Daily Cost Dewan Orang Ramai [20 cubes]', min_value=0, value=800)
cost_BK5 = st.sidebar.number_input('Daily Cost Balai Komuniti [5 cubes]', min_value=0, value=150)
cost_BK10 = st.sidebar.number_input('Daily Cost Balai Komuniti [10 cubes]', min_value=0, value=250)
cost_BK15 = st.sidebar.number_input('Daily Cost Balai Komuniti [15 cubes]', min_value=0, value=350)

# Constraint definition

problem = constraint.Problem()

problem.addVariable('DOR_10', range(0,5))
problem.addVariable('DOR_15', range(0,5)) 
problem.addVariable('DOR_20', range(0,5)) 
problem.addVariable('BK_5', range(0,20)) 
problem.addVariable('BK_10', range(0,20))
problem.addVariable('BK_15', range(0,20))

# Define constraint function

def vac_constraint(DOR_10, DOR_15, DOR_20, BK_5, BK_10, BK_15):
    if (DOR_15 + DOR_20 > 3) and (DOR_10*240 + DOR_15*360 + DOR_20*480 + BK_5*120 + BK_10*240 + BK_15*360 > cntDose) and (DOR_10*240 + DOR_15*360 + DOR_20*480 + BK_5*120 + BK_10*240 + BK_15*360 < cntDose+200):
        return True

problem.addConstraint(vac_constraint, ['DOR_10', 'DOR_15', 'DOR_20', 'BK_5', 'BK_10', 'BK_15'])

solutions = problem.getSolutions() 
print("Number of solutions found: {}\n".format(len(solutions)))

for s in solutions:
    print("DOR_10 = {}, DOR_15 = {}, DOR_20 = {},  BK_5 = {}, BK_10 = {}, BK_15 = {}"
        .format(s['DOR_10'], s['DOR_15'], s['DOR_20'], s['BK_5'], s['BK_10'], s['BK_15']))

df = pd.DataFrame(solutions)
df['Option'] = 'Option-' + df.index.astype(str)
df = df[['Option','DOR_10', 'DOR_15', 'DOR_20', 'BK_5', 'BK_10', 'BK_15']]


# Calculate the cost of each options
df['Total Cost'] = df['DOR_10'] * cost_DOR10 + df['DOR_15'] * cost_DOR15 + df['DOR_20'] * cost_DOR20 + df['BK_5'] * cost_BK5 + df['BK_10'] * cost_BK10 + df['BK_15'] * cost_BK15
df = df.sort_values(by='Total Cost', ascending=True)

def highlight_optimized(s):
    return 'background-color: yellow'  
 
st.write('Optimization Results:')  
st.dataframe(df.head(1).style.applymap(highlight_optimized))

st.write('Options with Accendingly Total Cost:')
st.write(df)

