import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

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
               ('Fauquier', 'Virginia'),
               ('Loudoun', 'Virginia'),
               ('Prince William', 'Virginia'),
               ('Rappahannock', 'Virginia'),
               ('Spotsylvania', 'Virginia'),
               ('Stafford', 'Virginia'),
               ('Warren', 'Virginia'),
               ('District of Columbia', 'District of Columbia')]

arl_only = [('Arlington', 'Virginia')]

df = pd.read_csv(url, index_col = 'date') 
df.index = pd.to_datetime(df.index, format = '%Y-%m-%d')


#%% Filter data and compute relevant info
def parse_data(df, county_list):
    county_df = pd.DataFrame()
    state_df = pd.DataFrame()
    combined_df = pd.DataFrame(columns = ['new cases'])
    combined_df = 0
    
    temp_df = pd.DataFrame() #df for storing current county and state data
    
    
    for county in county_list:
        county_cond = df['county'] == county[0] 
        state_cond =  df['state'] == county[1]

        temp_df = df.loc[county_cond & state_cond]
        temp_df['new cases'] = temp_df['cases'].diff() #compute daily new cases
        temp_df['new deaths'] = temp_df['deaths'].diff()
        temp_df['new cases rolling'] = temp_df['new cases'].rolling(window = 7).mean().to_frame() #compute rolling average of daily new cases
        temp_df['new deaths rolling'] = temp_df['new deaths'].rolling(window = 7).mean().to_frame() #compute rolling average of daily new cases
        
        
        county_df = pd.concat([county_df, temp_df])
        
    #Create df that aggregates cases by states
    state_df = county_df.groupby(['state', 'date'])[['new cases']].sum()
    state_df['new deaths'] = county_df.groupby(['state', 'date'])['new deaths'].sum()
    
    #Fix index, probably a better way to do this
    state_df.reset_index(inplace = True)
    state_df.index = state_df['date']
    del state_df['date']
    
    state_df['new cases rolling'] = state_df['new cases'].rolling(window = 7).mean().to_frame()
    state_df['new deaths rolling'] = state_df['new deaths'].rolling(window = 7).mean().to_frame()
    
    combined_df = county_df.groupby(['date'])[['new cases']].sum()
    combined_df['new deaths'] = county_df.groupby(['date'])['new deaths'].sum()
    
    combined_df['new cases rolling'] = combined_df['new cases'].rolling(window = 7).mean().to_frame()
    combined_df['new deaths rolling'] = combined_df['new deaths'].rolling(window = 7).mean().to_frame() 
    
    return county_df, state_df, combined_df

# Plot data using dataframe dictionary
def plot_data(df, grouping, dtype):
    a = plt.figure()
    
    title = 'DC Metro Area Combined Daily ' + dtype
    label = 'New ' + dtype
    col_label = 'new ' + dtype
    
    # fig, ax = plt.subplots(figsize=(8,5))
    
    if grouping == 'combined':
        plt.bar(df.index, df[col_label], label = label)
        plt.plot(df.index, df[col_label + ' rolling'], label = label + ' (7-day Rolling Avg.)')
                   
    else:
        for group in df[grouping].unique():
            
            cur_data = df.loc[df[grouping] == group, col_label]
            cur_data_rolling = df.loc[df[grouping] == group, (col_label + ' rolling')]
            
            plt.bar(cur_data.index, cur_data, label = group + ' ' + label)
            plt.plot(cur_data_rolling.index, cur_data_rolling, label = group + ' ' +  label + ' (7-day Rolling Avg.)')

        # df.groupby([plot_type])['new cases'].plot()
        # df.groupby([plot_type])['new cases rolling'].plot()
        
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Daily New Cases')
    plt.title(title)

    
#%%Plot data
county_df, state_df, combined_df = parse_data(df, county_list)

#%% Plot Cases
plot_data(combined_df, 'combined', 'cases') #combine all DC metro area cases
plot_data(state_df, 'state', 'cases') #show cases by states in DC metro area
plot_data(county_df, 'county', 'cases') #show cases by county, a bit hard to visually interpret

#%% Plot Deaths
plot_data(combined_df, 'combined', 'deaths') #combine all DC metro area deaths
plot_data(state_df, 'state', 'deaths') #show deaths by states in DC metro area
plot_data(county_df, 'county', 'deaths') #show deaths by county, a bit hard to visually interpret

#%%
#Plot subset of data
# county_df, state_df, combined_df = parse_data(df, fairfax_only)
# plot_data(county_df, 'county', 'cases')


