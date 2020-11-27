import pandas as pd

#.# read simple .cvs limit row
df = pd.read_csv("All Keyword 5 Years.csv")

col_name = df['Keyword']
df = df.drop(columns=['Keyword', 'Avg. monthly searches']).T
print(df.head(2))
# test = df.head(1).T
df.columns = col_name
print(df.head(2))


sum_value = sum(df['คอน โด'])
print(sum_value)

sum_value = df['คอน โด'].sum()
print(sum_value)

mean_value = df["คอน โด"].mean()
print(mean_value)

# flag = False


# for i in range(0,10):
#     print(i)
RESULT = pd.DataFrame()


OVERALL_TREND = []
for keyword in list(df):
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
    OVERALL_TREND.append(trend)

RESULT['keyword'] = list(df)
RESULT['OVERALL_TREND'] = OVERALL_TREND
# print(RESULT)

RESULT.to_csv('RESULT_Test.csv', encoding='utf-8-sig', index=None)

++
