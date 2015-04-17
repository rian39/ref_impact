import pandas as pd
import matplotlib.pyplot as plt
import seaborn

res = pd.read_excel(io='data/ref2014_results.xlsx', skiprows=7)
impact_res = res.ix[res.Profile=='Impact',['Unit of assessment name',
                                           'Institution name', '4*', '3*', '2*',
                                           '1*', 'FTE Category A staff submitted']]
#impact_res.to_csv('data/impact_res.csv')

staff = impact_res['FTE Category A staff submitted']
impact_res_clean = impact_res.iloc[:, [2, 3, 4, 5]].replace('-', 0)
total_impact = (impact_res_clean['4*']*4 + impact_res_clean['3*']*3 +
                impact_res_clean['2*']*2 +
                impact_res_clean['1*'])
staff = staff.replace('-', 0).astype('float')
total_impact.hist()
impact_intensity = total_impact/staff
impact_res['impact_intensity'] = impact_intensity

impact_res.columns = ['uoa', 'institution', '4*', '3*', '2*', '1*', 'staff','intensity']
impact_res.staff = staff
impact_res['institution'] = impact_res['institution'].str.lower()
impact_res['uoa'] = impact_res['uoa'].str.lower()
impact_res['intensity'].groupby(impact_res['uoa']).mean().order().plot('barh')
impact_res.to_excel('data/impact_res.xlsx')
