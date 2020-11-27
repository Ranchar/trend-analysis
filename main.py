import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display,clear_output
from numpy.polynomial.polynomial import polyfit
import time
from datetime import datetime

#  read file and select YOUR KEYWORD 
sheet_name = "คอนโด"
#  --------------------------------- 

df = pd.read_excel('All Keyword 5 Years.xlsx',sheet_name=sheet_name)  
print("\nAnalysis keyword of {}".format(sheet_name))
start_time = time.time()
dt_object = datetime.fromtimestamp(start_time)
print("starting at :", dt_object)
col_name = df['Keyword']
df = df.drop(columns=['Keyword', 'Avg. monthly searches']).T
df.columns = col_name



def compute_overall(keyword):
    flag = False
    sum_value = 0
    count = 0
    for i in df[keyword]:
        if i == 0 and flag == False:
            continue
        else:
            flag = True
            count = count + 1
            sum_value = sum_value + i

    avg_overall = sum_value/count
    # print(avg_overall)

    p25_month = round(count*25/100)
    avg_p25 = df[keyword].tail(p25_month).mean()
    # print(avg_p25)

    trend = round(100*(avg_p25-avg_overall)/avg_overall,2)
    # print(trend)
    return trend



def compute_start(keyword):
    interval = []
    flag = False
    start_rec = []
    for i in range(len(df[keyword])-2):
        x = range(0+i,3+i)
        y = [df[keyword][i], df[keyword][i+1], df[keyword][i+2]]
        try:
            b, m = polyfit(x, y, 1)
        except:
            m = 0
    #     clear_output(wait = True)
    #     plt.figure(figsize=(30,10))
    #     plt.plot(df[keyword],"--", color='#16697a')
    #     plt.plot(x, y, 'o', color='#db6400')
    #     plt.plot(x, b + m * x, '--', color='#db6400')
    #     plt.show()
        if m<0 and flag==False:
            flag = False
        elif m>0 and flag==False: #1st when get positive slope
            flag = True
        elif m>=0 and flag==True: #after pass 1st will save data
            start_rec.append(df.index[i-1])
        else:
            start_rec.append(df.index[i-1])
            start_rec.append(df.index[i])
            flag = False
            interval.append(list(dict.fromkeys(start_rec)))
            start_rec = []
    return interval



def compute_down(keyword):
    interval = []
    flag = False
    start_rec = []
    for i in range(len(df[keyword])-2):
        x = range(0+i,3+i)
        y = [df[keyword][i], df[keyword][i+1], df[keyword][i+2]]
        try:
            b, m = polyfit(x, y, 1)
        except:
            m = 0
#         clear_output(wait = True)
#         plt.figure(figsize=(30,10))
#         plt.plot(df[keyword],"--", color='#16697a')
#         plt.plot(x, y, 'o', color='#db6400')
#         plt.plot(x, b + m * x, '--', color='#db6400')
#         plt.show()
        if m>0 and flag==False:
            flag = False
        elif m<0 and flag==False: #1st when get positive slope
            flag = True
        elif m<=0 and flag==True: #after pass 1st will save data
            start_rec.append(df.index[i])
        else:
            start_rec.append(df.index[i-1])
            start_rec.append(df.index[i])
            flag = False
            interval.append(list(dict.fromkeys(start_rec)))
            start_rec = []
    return interval



OVERALL_TREND = []
START_UP = []
START_DOWN = []
PEAK_MONTH = []
BOTTOM_MONTH = []
running = 1

for keyword in list(df):
    trend = compute_overall(keyword)  #analysis overall trend
    OVERALL_TREND.append(trend)
    
    interval = compute_start(keyword) #incresing interval
    get_index = [len(interval[i]) for i in range(len(interval))]
    maxLen = get_index.index(max(get_index))
    interval = interval[maxLen]
    START_UP.append(interval)
    
    interval = compute_down(keyword) #decresing interval
    get_index = [len(interval[i]) for i in range(len(interval))]
    maxLen = get_index.index(max(get_index))
    interval = interval[maxLen]
    START_DOWN.append(interval)
    
    PEAK_MONTH.append(df[keyword][1:].idxmax())  #get peak performance
    BOTTOM_MONTH.append(df[keyword][1:].idxmin()) #get bad performance
    
    # printing process
    percent = round(100*running/len(list(df)),2)
    print("Process :  {}% ----- {}".format(percent, keyword) , end='\r') 
    running+=1


# SAVE RESULT
RESULT = pd.DataFrame()
RESULT['keyword'] = list(df)
RESULT['OVERALL_TREND'] = OVERALL_TREND
RESULT['START_UP'] = START_UP
RESULT['START_DOWN'] = START_DOWN
RESULT['PEAK_MONTH'] = PEAK_MONTH
RESULT['BOTTOM_MONTH'] = BOTTOM_MONTH
RESULT.to_csv('{}}.csv'.format(sheet_name),index=None, encoding='utf-8-sig')

end_time = time.time()
dt_object = datetime.fromtimestamp(end_time)
print("finished at :", dt_object)

# start_result = pd.DataFrame()
# start_result['v'] = [0,max(df[keyword])]
# start_result.index = [interval[maxLen][0],interval[maxLen][0]]



# end_result = pd.DataFrame()
# end_result['v'] = [0,max(df[keyword])]
# end_result.index = [interval[maxLen][-1],interval[maxLen][-1]]



# plt.figure(figsize=(30,10))
# plt.plot(df[keyword],"-", color='#16697a')
# plt.plot(start_result,"--",color='#db6400')
# plt.plot(end_result,"--", color='#db6400')
# plt.show()


