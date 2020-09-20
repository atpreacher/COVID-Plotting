import pandas as pd
import matplotlib.pyplot as plt
import urllib.request as request
import csv

url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'

county_list = [('Calvert', 'Maryland'),
               ('Charles', 'Maryland'),
               ('Frederick', 'Maryland'),
               ('Montgomery', 'Maryland'),
               ("Prince George's", 'Maryland'),
               ('Arlington', 'Virginia'),
               ('Clarke', 'Virginia'),
               ('Culpeper', 'Virginia'),
               ('Fairfax', 'Virginia'),
               ('Fairfax', 'Virginia'),
               ('Fauquier', 'Virginia'),
               ('Loudoun', 'Virginia'),
               ('Prince William', 'Virginia'),
               ('Rappahannock', 'Virginia'),
               ('Spotsylvania', 'Virginia'),
               ('Stafford', 'Virginia'),
               ('Warren', 'Virginia'),
               ('District of Columbia', 'District of Columbia')]

df = pd.read_csv(url, index_col = 'date') 
df.index = pd.to_datetime(df.index, format = '%Y-%m-%d')


#%%Test Code

# county_cond = df['county'] == 'Arlington'
# state_cond =  df['state'] == 'Virginia'

# arl_df = df.loc[county_cond & state_cond]


# arl_df.loc[:,'new cases'] = arl_df.loc[:, 'cases'].diff() #compute difference between rows to get daily numbers
# arl_df.iat[0, 5] = 0 #replace NaN with 0 for first row
# arl_rolling = arl_df['new cases'].rolling(window = 7).mean() #compute rolling 7 day average

# plt.plot(arl_df['date'], arl_df['new cases'], label = 'Arlington County')
# plt.plot(arl_df['date'], arl_rolling)
# plt.legend()



#%% Filter data and compute relevant info
def parse_data(df, county_list):
    # data_dict = {}
    # rolling_dict = {}
    
    temp_df = pd.DataFrame()
    cur_df = pd.DataFrame()
    
    combined_df = pd.DataFrame(columns = ['new cases'])
    combined_df = 0
    
    
    combined_data = pd.DataFrame(index = df.index.unique())
    combined_data['new cases'] = 0 
    
    for county in county_list:
        county_cond = df['county'] == county[0] 
        state_cond =  df['state'] == county[1]

        cur_df = df.loc[county_cond & state_cond]
        
        
        #compute difference between rows to get daily numbers
        # data_dict[county[0]].loc[:,'new cases'] = data_dict[county[0]].loc[:, 'cases'].diff() 
        # data_dict[county[0]].iat[0, 5] = 0 
        
        cur_df['new cases'] = cur_df['cases'].diff() 
        cur_df['new case 7 day avg'] = cur_df['new cases'].rolling(window = 7).mean().to_frame()
        
        temp_df = pd.concat([temp_df, cur_df])
        
        # combined_df = cur_df['new cases'] + combined_df['new cases']

        combined_df = temp_df.groupby(['date'])[['new cases']].sum()
        combined_df['new cases rolling'] = combined_df['new cases'].rolling(window = 7).mean().to_frame()
        
        
        

        
        # #compute 7 day rolling average
        # rolling_dict[county[0] + ' (7 day avg.)'] = data_dict[county[0]]['new cases'].rolling(window = 7).mean().to_frame()
        
        # #Computed combined cases
        # combined_data['new cases'] = data_dict[county[0]].loc[:,'new cases'] + combined_data['new cases']
        # combined_data['new cases'] = combined_data['new cases'].fillna(0)
    
    # #Make combined data into dataframe dictionary    
    # combined_dict = {}
    # combined_dict['combined'] = combined_data['new cases'].to_frame()
    # combined_dict['combined rolling'] = combined_dict['combined'].rolling(window = 7).mean()
            
    return temp_df, combined_df

# Plot data using dataframe dictionary
def plot_counties(xvals, yvals,  label = 'Daily Case Counts'):
    a = plt.figure()
    
    # for key, value in data.items(): 
    #     x_data = value.index
    #     y_data = value['new cases']
        
    plt.plot(x_data, y_data, label = key)
        
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Daily New Cases')
    plt.title(label)


    
#%%Plot data
temp_df, combined_df = parse_data(df, county_list)

plot_counties(temp_df.index

plot_counties(data_dict) #plot daily case counts by county
plot_counties(rolling_dict, 'Rolling Average Daily Case Counts')
plot_counties(combined_dict, 'Combined Daily Case Counts')


