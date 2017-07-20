
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# In[8]:

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# # Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.
# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 
# Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.

# In[9]:

# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


# In[10]:

import pandas as pd
import numpy as np
def get_list_of_university_towns():
#     '''Returns a DataFrame of towns and the states they are in from the 
#     university_towns.txt list. The format of the DataFrame should be:
#     DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
#     columns=["State", "RegionName"]  )
    
#     The following cleaning needs to be done:

#     1. For "State", removing characters from "[" to the end.
#     2. For "RegionName", when applicable, removing every character from " (" to the end.
#     3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    
    f = open('university_towns.txt', 'r')
    raw = []
    for line in f:
        raw.append(line[:-1])
    f.close()

    univ_town= []
    for line in raw:
        if line[-6:] == '[edit]':
            state = line[:-6]
        elif line.find("(",0) >= 0:
            town = line[:line.find("(")]
            univ_town.append([state, town])
        else:
            town = line
            univ_town.append([state, town])

    university_town_df = pd.DataFrame(univ_town, columns = ['State','RegionName'])
    university_town_df['RegionName'] = university_town_df['RegionName'].str.strip()
    
    return university_town_df

get_list_of_university_towns()


# In[ ]:

def get_recession_df():
    recession_raw = pd.read_excel("gdplev.xls", skiprows = 219).drop(['Unnamed: 0','Unnamed: 1', 'Unnamed: 2','Unnamed: 3','Unnamed: 7'], axis = 1)
    recession_raw = recession_raw.rename(columns = {'1999q4': 'Quarter', 9926.1: 'GDP Current', 12323.3: 'GDP 2009 value'})
    recession_raw[['GDP Current','GDP 2009 value']] = recession_raw[['GDP Current','GDP 2009 value']].apply(pd.to_numeric)
    return recession_raw

def get_recession_start():
#     '''Returns the year and quarter of the recession start time as a 
#     string value in a format such as 2005q3'''
    recession_raw = get_recession_df()
    # recession start: two consecutive decrease in GDP
    quarter = []
    for i in range(len(recession_raw) - 2):
        if (recession_raw.iloc[i,1] > recession_raw.iloc[i+1,1]) & (recession_raw.iloc[i+1,1] > recession_raw.iloc[i+2,1]):
            quarter.append(recession_raw.iloc[i,0])
        
    return quarter[0]

get_recession_start()


# In[ ]:

def get_recession_df():
    recession_raw = pd.read_excel("gdplev.xls", skiprows = 219).drop(['Unnamed: 0','Unnamed: 1', 'Unnamed: 2','Unnamed: 3','Unnamed: 7'], axis = 1)
    recession_raw = recession_raw.rename(columns = {'1999q4': 'Quarter', 9926.1: 'GDP Current', 12323.3: 'GDP 2009 value'})
    recession_raw[['GDP Current','GDP 2009 value']] = recession_raw[['GDP Current','GDP 2009 value']].apply(pd.to_numeric)
    return recession_raw

def get_recession_end():
#    '''Returns the year and quarter of the recession end time as a 
#    string value in a format such as 2005q3'''
    recession_raw = get_recession_df().reset_index()
    start_index = []
    for i in range(len(recession_raw) - 2):
        if (recession_raw.iloc[i,2] > recession_raw.iloc[i+1,2]) & (recession_raw.iloc[i+1,2] > recession_raw.iloc[i+2,2]):
            start_index.append(recession_raw.iloc[i,0])
    start = start_index[0]
# recession start: two consecutive decrease in GDP
    quarter = []
    end_index = []
# initialize j ; 
    j = 2
    for j in range(len(recession_raw)):
        if (j > start) & (recession_raw.iloc[j,2] > recession_raw.iloc[j-1,2]) & (recession_raw.iloc[j-1,2] > recession_raw.iloc[j-2,2]):
            quarter.append(recession_raw.iloc[j,1])
#            end_index.append(recession_raw.iloc[j,0])
#    end = end_index[0]
#    recession_period = recession_raw.iloc[start: end + 1, :]    
    return quarter[0]
       
get_recession_end()


# In[ ]:

def get_recession_df():
    recession_raw = pd.read_excel("gdplev.xls", skiprows = 219).drop(['Unnamed: 0','Unnamed: 1', 'Unnamed: 2','Unnamed: 3','Unnamed: 7'], axis = 1)
    recession_raw = recession_raw.rename(columns = {'1999q4': 'Quarter', 9926.1: 'GDP Current', 12323.3: 'GDP 2009 value'})
    recession_raw[['GDP Current','GDP 2009 value']] = recession_raw[['GDP Current','GDP 2009 value']].apply(pd.to_numeric)
    return recession_raw

def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
#    '''Returns the year and quarter of the recession end time as a 
#    string value in a format such as 2005q3'''
    recession_raw = get_recession_df().reset_index()
    start_index = []
    for i in range(len(recession_raw) - 2):
        if (recession_raw.iloc[i,2] > recession_raw.iloc[i+1,2]) & (recession_raw.iloc[i+1,2] > recession_raw.iloc[i+2,2]):
            start_index.append(recession_raw.iloc[i,0])
    start = start_index[0]
# recession start: two consecutive decrease in GDP
    quarter = []
    end_index = []
# initialize j ; 
    j = 2
    for j in range(len(recession_raw)):
        if (j > start) & (recession_raw.iloc[j,2] > recession_raw.iloc[j-1,2]) & (recession_raw.iloc[j-1,2] > recession_raw.iloc[j-2,2]):
            quarter.append(recession_raw.iloc[j,1])
            end_index.append(recession_raw.iloc[j,0])
    end = end_index[0]
    recession_period = recession_raw.iloc[start: end + 1, :]
    return recession_period.sort(columns = "GDP 2009 value").iloc[0,1]

get_recession_bottom()


# In[1]:

from datetime import datetime

def convert_housing_data_to_quarters():
#     '''Converts the housing data to quarters and returns it as mean 
#     values in a dataframe. This dataframe should be a dataframe with
#     columns for 2000q1 through 2016q3, and should have a multi-index
#     in the shape of ["State","RegionName"].
    
#     Note: Quarters are defined in the assignment description, they are
#     not arbitrary three month periods.
    
#     The resulting dataframe should have 67 columns, and 10,730 rows.
#     '''
    housing = pd.read_csv("City_Zhvi_AllHomes.csv")
    
#     Replace states with full name
    housing['State'] = housing['State'].map(states)

# contain only list of attributes
    column_list = ['RegionName','State']
    for i in housing.columns:
        if i.find('-') >= 0 and datetime.strptime(i, '%Y-%m').year>= 2000:
            column_list.append(i)
    housing_convert = housing[column_list]
    
    housing_convert.set_index(['State','RegionName'], inplace = True)
    housing_convert = housing_convert.groupby(pd.to_datetime(housing_convert.columns).to_period("Q"), axis=1).mean()
    
    quarter_column_list =  []
    for name in housing_convert.columns:
        column_item = str(name).replace('Q','q')
        quarter_column_list.append(column_item)
    
    housing_convert.rename(columns = dict(zip(housing_convert.columns[0:], quarter_column_list)), inplace = True)

    return housing_convert#quarter_column_list#

convert_housing_data_to_quarters()


# In[ ]:

from scipy import stats 

def run_ttest():
    #price_ratio=quarter_before_recession/recession_bottom
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    univ_town = get_list_of_university_towns()
    housing_convert = convert_housing_data_to_quarters().reset_index()
    univ_town['RegionName'] = univ_town['RegionName'].str.strip()
    full_data = pd.merge(housing_convert, univ_town, how = "left", left_on = ['State','RegionName'], right_on = ['State','RegionName'],indicator=True)
    full_data['university_town'] = full_data["_merge"].apply(lambda x: 1 if x == 'both' else 0 )
    # get recession start and bottom ;
    bottom = get_recession_bottom()
    start =  get_recession_start()
    columns_keep = ['State','RegionName', start, bottom, 'university_town']
    full_data['price_ratio'] = full_data[start]/full_data[bottom]
    college_town = full_data[full_data['university_town'] ==1][['price_ratio']].dropna()
    noncollege_town = full_data[full_data['university_town'] == 0][['price_ratio']].dropna()
    #list(stats.ttest_ind(college_mean['price_ratio'], noncollege_mean['price_ratio']))
    #result = test()
    # find p-value
    p_value = list(stats.ttest_ind(noncollege_town['price_ratio'],college_town['price_ratio']))[1]
    
    if p_value < 0.01:
        result = True
    else:
        result = False
    
#    collage_mean = college_town['price_ratio'].mean()
#    non_collage_mean = noncollege_town['price_ratio'].mean()
    if college_town['price_ratio'].mean() < noncollege_town['price_ratio'].mean():
        better = 'university town'
    else:
        better = 'non-university town'
#    output = better(collage_mean,non_collage_mean)
            
    return (result, p_value, better)

run_ttest()

