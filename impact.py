import pandas as pd
import json
import gensim
from bs4 import BeautifulSoup

"""
loads the json cases, makes a dataframe, cleans the html, and rename columns.
It groups by UoA, and the counts case for each institution and makes a dataframe
with the number of cases per institution per uoa.
It then loads the ref results, extracts the impacts results.
Last, it merges both into a single dataframe
"""

def html_strip(x):                                                                               │      ~
    bs = BeautifulSoup(x)                                                                        │      ~
    return bs.get_text()


f = open('data/DownloadAllJSON')
s = f.read()
j = json.loads(s)
df = pd.DataFrame(j['DownloadAllJSONResult'])
df['UoA'] = df['UoA'].map(html_strip).str.strip().str.lower()
df['Institution'] = df['Institution'].map(html_strip).str.replace('(\n|\r)','').str.strip().str.lower().str.replace('\(.*', '').str.replace('\\d*', '')
df.Institution = df.Institution.str.replace('[,-."]|the', '').str.strip().str.replace('\\W+', ' ')
uoa_by_institution = df['UoA'].groupby(df.Institution).value_counts()
uoa_df = uoa_by_institution.reset_index()
uoa_df.columns = ['institution', 'uoa', 'case_count']

#load the impact results

res = pd.read_excel(io='data/ref2014_results.xlsx', skiprows=7)
impact_res = res.ix[res.Profile == 'Impact',['Unit of assessment name',
                                           'Institution name', '4*', '3*', '2*',
                                           '1*', 'FTE Category A staff submitted']]

staff = impact_res['FTE Category A staff submitted']
impact_res_clean = impact_res.iloc[:, [2, 3, 4, 5]].replace('-', 0)
total_impact = (impact_res_clean['4*']*4 + impact_res_clean['3*']*3 +
                impact_res_clean['2*']*2 +
                impact_res_clean['1*'])

staff = staff.replace('-', 0).astype('float')
impact_intensity = total_impact/staff
impact_res['impact_intensity'] = impact_intensity

impact_res.columns = ['uoa', 'institution', '4*', '3*', '2*', '1*', 'staff','intensity']
impact_res.staff = staff
impact_res['institution'] = impact_res['institution'].str.lower()
impact_res['uoa'] = impact_res['uoa'].str.lower()

#merge the cases and the results
df_comb = pd.merge(uoa_df, impact_res, how='left', on=['institution', 'uoa'])
