#############################################
#
# PPV Definition
#
# PPV 1 = 200
# PPV 2 = 400
# PPV 3 = 600
# PPV 4 = 800
# PPV 5 = 1000
# PPV 6 = 1200
#
#############################################

# Import libraries

import constraint
import pandas as pd
from random import randint
import streamlit as st
import numpy as np

# Streamlit configuration

st.set_page_config(layout="wide")

# Streamlit header and title

st.image('asm.png')
st.markdown("# Optimal PPV Combinations Estimation")
st.subheader('Daily Capacity Information for Each PPV:') 

PPV_capacity = {'PPV Type': ['PPV 1', 'PPV 2', 'PPV 3', 'PPV 4', 'PPV 5', 'PPV 6'], 'Daily Capacity of PPV': [200,400,600,800,1000,1200]}
st.write(pd.DataFrame.from_dict(PPV_capacity))

# ------------ Sidebar components --------------

st.sidebar.header('Dose:')
cntDose = st.sidebar.number_input('', min_value=1000, max_value=15000, value=5000)

st.sidebar.header('Days to Completion:')
dayToComplete = st.sidebar.number_input('', min_value=1, max_value=5, value=5)

st.sidebar.header('Number of PPV Types:')
cnt_ppv1 = st.sidebar.number_input('PPV 1', min_value=0, value=5)
cnt_ppv2 = st.sidebar.number_input('PPV 2', min_value=0, value=5)
cnt_ppv3 = st.sidebar.number_input('PPV 3', min_value=0, value=5)
cnt_ppv4 = st.sidebar.number_input('PPV 4', min_value=0, value=5)
cnt_ppv5 = st.sidebar.number_input('PPV 5', min_value=0, value=5)
cnt_ppv6 = st.sidebar.number_input('PPV 6', min_value=0, value=5)

# Constraint definition

problem = constraint.Problem()

problem.addVariable('PPV_1', range(0,cnt_ppv1+1))
problem.addVariable('PPV_2', range(0,cnt_ppv2+1)) 
problem.addVariable('PPV_3', range(0,cnt_ppv3+1)) 
problem.addVariable('PPV_4', range(0,cnt_ppv4+1)) 
problem.addVariable('PPV_5', range(0,cnt_ppv5+1)) 
problem.addVariable('PPV_6', range(0,cnt_ppv6+1))

# Define constraint function

def vac_constraint(PPV_1, PPV_2, PPV_3, PPV_4, PPV_5, PPV_6):
    #if (PPV_1 + PPV_2 + PPV_3 + PPV_4 + PPV_5 + PPV_6 <= dayToComplete) and (PPV_1*200 + PPV_2*400 + PPV_3*600 + PPV_4*800 + PPV_5*1000 + PPV_6*1200 > cntDose-400) and (PPV_1*200 + PPV_2*400 + PPV_3*600 + PPV_4*800 + PPV_5*1000 + PPV_6*1200 < cntDose+200):
    if (PPV_1*200 + PPV_2*400 + PPV_3*600 + PPV_4*800 + PPV_5*1000 + PPV_6*1200) > (cntDose/dayToComplete - cntDose/dayToComplete*0.1) and (PPV_1*200 + PPV_2*400 + PPV_3*600 + PPV_4*800 + PPV_5*1000 + PPV_6*1200) < (cntDose/dayToComplete + cntDose/dayToComplete*0.1):        
        return True

problem.addConstraint(vac_constraint, ['PPV_1', 'PPV_2', 'PPV_3', 'PPV_4', 'PPV_5', 'PPV_6'])

try:
    solutions = problem.getSolutions() 

    print("Number of solutions found: {}\n".format(len(solutions)))

    for s in solutions:
        print("PPV_1 = {}, PPV_2 = {}, PPV_3 = {}, PPV_4 = {}, PPV_5 = {}, PPV_6 = {}"
            .format(s['PPV_1'], s['PPV_2'], s['PPV_3'], s['PPV_4'], s['PPV_5'], s['PPV_6']))

    df = pd.DataFrame(solutions)
    df['Option'] = 'Option-' + df.index.astype(str)
    df = df[['Option','PPV_1', 'PPV_2', 'PPV_3', 'PPV_4', 'PPV_5', 'PPV_6']]
     
except:
    st.error("Please make sure that you have chosen the correct numbers for the PPVs.")
    st.stop()




# Calculate the score of each options

st.sidebar.header('Preference of a PPV [score 0-10]:')
w_ppv1  = st.sidebar.number_input('score for PPV 1', min_value=0, value=3)
w_ppv2 = st.sidebar.number_input('score for PPV 2', min_value=0, value=3)
w_ppv3 = st.sidebar.number_input('score for PPV 3', min_value=0, value=3)
w_ppv4 = st.sidebar.number_input('score for PPV 4', min_value=0, value=2)
w_ppv5 = st.sidebar.number_input('score for PPV 5', min_value=0, value=2)
w_ppv6 = st.sidebar.number_input('score for PPV 6', min_value=0, value=1)

def weight_calc(row):
    return (w_ppv1*row['PPV_1'] + w_ppv2*row['PPV_2'] + w_ppv3*row['PPV_3'] + w_ppv4*row['PPV_4'] + w_ppv5*row['PPV_5'] + w_ppv6*row['PPV_6'])/(w_ppv1 + w_ppv2 + w_ppv3 + w_ppv4 + w_ppv5 + w_ppv6)

df['Score'] = df.apply(lambda row : weight_calc(row), axis = 1)

# Return Normalized Scores

df_min_max_scaled = df.copy()
  
# apply normalization techniques by Column 1
column = 'Score'
df_min_max_scaled['Score'] = (df_min_max_scaled[column] - df_min_max_scaled[column].min()) / (df_min_max_scaled[column].max() - df_min_max_scaled[column].min()) * 100
df_min_max_scaled['Score'] = df_min_max_scaled['Score'].round(decimals=4)
df_min_max_scaled = df_min_max_scaled.sort_values(by='Score', ascending=False)

def highlight_optimized(s):
    return 'background-color: yellow'  
 
st.subheader('Top-3 Optimised Options:') 

df_first_opt =  df_min_max_scaled.head(1)
st.dataframe(df_first_opt.style.applymap(highlight_optimized)) 


val_PPV1 = np.array2string(df_first_opt.iloc[0]['PPV_1'])
val_PPV2 = np.array2string(df_first_opt.iloc[0]['PPV_2'])
val_PPV3 = np.array2string(df_first_opt.iloc[0]['PPV_3'])
val_PPV4 = np.array2string(df_first_opt.iloc[0]['PPV_4'])
val_PPV5 = np.array2string(df_first_opt.iloc[0]['PPV_5'])
val_PPV6 = np.array2string(df_first_opt.iloc[0]['PPV_6'])

st.subheader('Findings:') 
# st.markdown("#### Approach 1:")
# st.write("We need " + val_PPV1 + " days for PPV 1 and " + val_PPV2 + " days for PPV 2. As for PPV 3, " + val_PPV3 + " days are needed and PPV 4 needs " + val_PPV4 + " days. As for PPV 5, we need " + val_PPV5 + " days while PPV 6 will need " + val_PPV6 + " days. With this combination, the vaccination will be completed in less or equal to " + str(dayToComplete) + " days.")

# st.markdown("#### Approach 2:")
# st.write("We can complete all the doses in ONE day provided that we have " + val_PPV1 + " units of PPV 1, " + val_PPV2 + " units of PPV 2, "+ val_PPV3 + " units of PPV3, " + val_PPV4 + " of PPV4, " + val_PPV5 + " units of PPV5, and " + val_PPV6 + " units of PPV6.")

st.write("We have a total of " + str(cntDose) + " dose. " + "To complete all the dose, since we have " + str(cnt_ppv1) + " PPV Type 1, we need " + val_PPV1 + " days. We have " + str(cnt_ppv2) + " PPV Type 2 and therefore " + val_PPV2 + " days for PPV Type 2 are needed. There are " + str(cnt_ppv3) + " PPV Type 3 and we need " + val_PPV3 + " days. As for PPV Type 4, we have " + str(cnt_ppv4) + " and " + val_PPV4 + " days are needed. We have " + str(cnt_ppv5) + " PPV Type 5, we need " + val_PPV5 + " days. Last, we have " + str(cnt_ppv6) + " PPV Type 6, then the required days are " + val_PPV6 + "." )

st.subheader('Options with Descending Score:')
st.write(df_min_max_scaled)
 