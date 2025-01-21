import pandas as pd
from category_encoders import TargetEncoder
#from models import adaptive_hawkes
#from CIBer import CIBer
from sklearn.linear_model import LogisticRegression
from category_encoders import TargetEncoder
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import tree

state_abbrev_to_name = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming"
}

def data_preparation_HHS(name, split = 2021, start = None, end=None, num_states=12, method='bycount'):
    if name == 'breach_report_all.csv':
        data = pd.read_csv('breach_report_all.csv')
    else:
        data = pd.read_csv('Data_Breaches1.csv')

    print('missing percentage: ', data.isna().sum()/data.shape[0])
    data.drop(columns=['Web Description','Name of Covered Entity'], inplace=True)
    #Drop the columns that are not useful for the model

    #The column of Type of Breaches is mutli-label, we only keep the first classification label to keep it simple
    data = data.replace(to_replace=r'^Hacking/IT Incident.*$', value='Hacking/IT Incident', regex=True)
    data = data.replace(to_replace=r'^Improper Disposal.*$', value='Improper Disposal', regex=True)
    data = data.replace(to_replace=r'^Loss.*$', value='Loss', regex=True)
    data = data.replace(to_replace=r'^Other.*$', value='Other', regex=True)
    data = data.replace(to_replace=r'^Theft.*$', value='Theft', regex=True)
    #The column Breach Submission Date is the event times we want to model
    data['Breach Submission Date'] = pd.to_datetime(data['Breach Submission Date'])
    #data = data.loc[data['Breach Submission Date'].dt.year<2020]

    #We replace the missing value by -1, or if given enough data, we can just drop them
    #But the problem here, we are modelling possion process, event itself is more important, 
    #bad features could less harmful than dropping it directly 
    severity = data['Individuals Affected']
    data = data.drop(columns=['Individuals Affected', 'Location of Breached Information'])
    if name == 'breach_report_all.csv':
        data = data.iloc[::-1,:].reset_index(drop=True)
    data = data.fillna(-1)
    if  name == 'breach_report_all.csv':
        if start:
            data = data[data['Breach Submission Date'].dt.year>=start]
            loc = int(data['Breach Submission Date'][data['Breach Submission Date'].dt.year==split].shape[0]-230)
        else:
            loc = int(data['Breach Submission Date'][data['Breach Submission Date'].dt.year==split].shape[0]/2)
    else:
        data = data[data['Breach Submission Date'].dt.year>=2010]
        loc = 0

    split = data['Breach Submission Date'][data['Breach Submission Date'].dt.year==split].iloc[loc]
    data.set_index('Breach Submission Date', inplace=True, drop=False)
    print('train test split: ', split)

    # #there are too many states in the state column, we reduce the number of them to have more frequencies
    def encoding_by_count(data):
        data = data.copy(deep= True)
        # Calculate frequencies
        location_counts = data.value_counts()
        
        if len(data.unique())> 10:
            mapping = pd.cut(location_counts, bins=8, labels=False)
            return mapping

        else:
            # Map locations to their frequency
            mapping = location_counts.rank(method='dense', ascending=False) - 1
            return mapping
        
    #the first one is more suitable for Naive Bayes, we do help encoding the feature by its frequency
    if method == 'bycount':
        data['Business Associate Present'] = pd.factorize(data['Business Associate Present'])[0]
        df_train = data.loc[:str(split)].copy(deep=True)
        df_test = data.loc[str(split):].copy(deep=True)
        mapping0 = encoding_by_count(df_train['State'])
        df_train['State'] = df_train['State'].map(mapping0)
        mapping1 = encoding_by_count(df_train['Covered Entity Type'])
        df_train['Covered Entity Type'] = df_train['Covered Entity Type'].map(mapping1)
        mapping2 = encoding_by_count(df_train['Type of Breach'])
        df_train['Type of Breach'] = df_train['Type of Breach'].map(mapping2)
        
        df_test['State'] = df_test['State'].map(mapping0)
        df_test['Covered Entity Type'] = df_test['Covered Entity Type'].map(mapping1)
        df_test['Type of Breach'] = df_test['Type of Breach'].map(mapping2) 
        
    # Method label is more suitable for CIBer, we only reduce the number of states nu encoding by count
    # The rest will be encoding by label encoding
    elif method=='label':
        
        data['Covered Entity Type'] = pd.factorize(data['Covered Entity Type'])[0]
        data['Type of Breach'] = pd.factorize(data['Type of Breach'])[0]
        data['Business Associate Present'] = pd.factorize(data['Business Associate Present'])[0]
        
        df_train = data.loc[:str(split)].copy(deep=True)
        df_test = data.loc[str(split):].copy(deep=True)

        mapping = encoding_by_count(df_train['State'])
        df_train['State'] = df_train['State'].map(mapping)
        df_test['State'] = df_test['State'].map(mapping)
    
    elif method == 'target':
        encoder = TargetEncoder()
        X_train_encoded = encoder.fit_transform(df_train, df_train)
        X_test_encoded = encoder.transform(df_test)
        return X_train_encoded, X_test_encoded
    
    weekly_freq_trian = df_train.resample('W', on='Breach Submission Date').size().reset_index(name='event_count')
    weekly_freq_test = df_test.resample('W', on='Breach Submission Date').size().reset_index(name='event_count')

    severity_train = severity.iloc[:df_train.shape[0]]
    severity_test = severity.iloc[df_train.shape[0]:]
        
    return df_train, df_test, severity_train, severity_test, weekly_freq_trian, weekly_freq_test

def data_preparation_PRC(name, split = 2021, start = None, end=None, num_states=12, method='bycount'):

    data = pd.read_csv('PRC Data Breach Chronology.csv')
    data.columns
    column_name = ['Date Made Public', 'State', 'Information Source', 'Type of breach', 'Total Records', 'Type of organization']
    data = data[column_name]
    print('missing percentage: ', data.isna().sum()/data.shape[0])
    data = data.fillna(-1)

    data['Date Made Public'] = pd.to_datetime(data['Date Made Public'])
    # reorganize the data with the time order
    data = data.sort_values(by='Date Made Public')

    # Create a new data frame, which contains the weekly frequency of the records
    weekly_freq = data.resample('W', on='Date Made Public').size().reset_index(name='event_count')

    # Take a look at the data before 2008
    if start:
        data = data.loc[data['Date Made Public'].dt.year>=start]
        weekly_freq = weekly_freq.loc[weekly_freq['Date Made Public'].dt.year>=start]
    if end:
        data = data.loc[data['Date Made Public'].dt.year<=end]
        weekly_freq = weekly_freq.loc[weekly_freq['Date Made Public'].dt.year<=end]

    # map the state abbreviation to the full name
    data['State'] = data['State'].apply(lambda x: state_abbrev_to_name[x] if x in state_abbrev_to_name else x)
    # those missing values are mapp to unknown
    data['Type of breach'] = data['Type of breach'].apply(lambda x: x if x != -1 else 'UNKN')

    severity = data['Total Records']
    data = data.drop(columns=['Total Records'])

    def encoding_by_count(data):
        data = data.copy(deep= True)
        # Calculate frequencies
        location_counts = data.value_counts()
        
        if len(data.unique())> 10:
            mapping = pd.cut(location_counts, bins=12, labels=False)
            return mapping

        else:
            # Map locations to their frequency
            mapping = location_counts.rank(method='dense', ascending=False) - 1
            return mapping

    if method == 'bycount':    
        state_map = encoding_by_count(data['State'])
        data['State'] = data['State'].map(state_map)
        type_map = encoding_by_count(data['Type of breach'])
        data['Type of breach'] = data['Type of breach'].map(type_map)
        org_map = encoding_by_count(data['Type of organization'])
        data['Type of organization'] = data['Type of organization'].map(org_map)
        source_map = encoding_by_count(data['Information Source'])
        data['Information Source'] = data['Information Source'].map(source_map)

    elif method == 'label':
        data['State'] = pd.factorize(data['State'])[0]
        data['Type of breach'] = pd.factorize(data['Type of breach'])[0]
        data['Type of organization'] = pd.factorize(data['Type of organization'])[0]
        data['Information Source'] = pd.factorize(data['Information Source'])[0]

    #split_day = data['Date Made Public'][data['Date Made Public'].dt.year<=split].iloc[-1]
    split_day = pd.Timestamp(year=split, month=12, day=31)
    #split last day
    data.set_index('Date Made Public', inplace=True, drop=False)

    df_train = data.loc[:str(split_day)].copy(deep=True)# this inlcude that split date
    split_day_next = split_day + pd.DateOffset(days=1)
    df_test = data.loc[str(split_day_next):].copy(deep=True)

    print('train test split: ', split_day)
    print('length of train: ', len(df_train), 'length of test: ', len(df_test))
    print('training start: ', df_train.index[0], 'training end: ', df_train.index[-1])
    print('testing start: ', df_test.index[0], 'testing end: ', df_test.index[-1])

    weekly_freq_train = weekly_freq.loc[weekly_freq['Date Made Public']<=split_day]
    weekly_freq_test = weekly_freq.loc[weekly_freq['Date Made Public']>split_day]
    
    severity_train = severity.iloc[:df_train.shape[0]]
    severity_test = severity.iloc[df_train.shape[0]:]

    return df_train, df_test, severity_train, severity_test, weekly_freq_train, weekly_freq_test


def label_generating_HHS(X_train, X_test, threshold):
    count_df = X_train.groupby(['Type of Breach','Covered Entity Type',
                            'State','Business Associate Present']).agg(
                                Count=('Type of Breach', 'size'),
                            )
    count_df = count_df.reset_index()
    # Define the bins and labels
    
    num_cluster = len(threshold)
    # thres1 = threshold[0]
    # thres2 = threshold[1]
    #bins = [-float('inf'), thres1, thres2, float('inf')]
    bins = [-float('inf')] + list(threshold) + [float('inf')]
    labels = [i for i in range(num_cluster,-1,-1)]



    # Create a new column with the labels
    count_df['label'] = pd.cut(count_df['Count'], bins=bins, labels=labels, right=False)

    y_train = pd.merge(X_train, count_df, on=['Type of Breach','Covered Entity Type',
                            'State','Business Associate Present'], how='left')['label']
    y_test = pd.merge(X_test, count_df, on=['Type of Breach','Covered Entity Type',
                            'State','Business Associate Present'], how='left')['label']

    return y_train, y_test

def label_generating_PRC(X_train, X_test, threshold):

    count_df = X_train.groupby(['State','Type of breach','Type of organization']).agg(
                                Count=('State', 'size'),
                            )
    count_df = count_df.reset_index()

    # Define the bins and labels
    
    num_cluster = len(threshold)
    # thres1 = threshold[0]
    # thres2 = threshold[1]
    #bins = [-float('inf'), thres1, thres2, float('inf')]
    bins = [-float('inf')] + list(threshold) + [float('inf')]
    labels = [i for i in range(num_cluster,-1,-1)]

    # Create a new column with the labels
    count_df['label'] = pd.cut(count_df['Count'], bins=bins, labels=labels, right=False)

    y_train = pd.merge(X_train, count_df, on=['State','Type of breach','Type of organization'], how='left')['label']
    y_test = pd.merge(X_test, count_df, on=['State','Type of breach','Type of organization'], how='left')['label']

    return y_train, y_test


def new_algorithm(name, unit_name='week', model_name0='modified', model_name = 'CIBer', times = (2009, 2021, None),  methods='bycount', max_iter=20, training=True, passing=False):
    if unit_name == 'week':
        unit = 7
    elif unit_name == 'day':
        unit = 1
    elif unit_name == 'forthright':
        unit = 14
    elif unit_name == 'year':   
        unit = 365

    #Data importing
    start = times[0]
    split = times[1]
    end = times[2]

    if name == 'breach_report_all.csv' or name == 'Data_Breaches1.csv':
        train, test, severity_train, severity_test, weekly_freq_train, weekly_freq_test = data_preparation_HHS(name, split = split, start=start, end = end, method='label')
    elif name == 'PRC Data Breach Chronology.csv':
        train, test, severity_train, severity_test, weekly_freq_train, weekly_freq_test = data_preparation_PRC(name, split = split, start=start, end = end, method=methods)

    if name == 'breach_report_all.csv' or name == 'Data_Breaches1.csv':
        time_column = 'Breach Submission Date'
    elif name == 'PRC Data Breach Chronology.csv':
        time_column = 'Date Made Public'
    
    start_time = train[time_column].min()
    #train test split
    train[time_column] = pd.to_datetime(train[time_column])
    t_train = (train[time_column] - start_time).dt.total_seconds() / (24 * 3600 * unit)  # Convert to days
    print('data_number: ', len(t_train))
    X_train = train.drop(columns=time_column)
    t_test = (test[time_column] - start_time).dt.total_seconds() / (24 * 3600 * unit)  # Convert to days
    X_test = test.drop(columns=time_column)

    if passing:
        return X_train, X_test, t_train, t_test, severity_train, severity_test, weekly_freq_train, weekly_freq_test
    #generate pusedo cluster label by CIBer
    # threshold = thresholds
    threshold = [20, 70]
    
    if name == 'breach_report_all.csv' or name == 'Data_Breaches1.csv':
        y_train, y_test = label_generating_HHS(X_train, X_test, threshold)
    elif name == 'PRC Data Breach Chronology.csv':
        y_train, y_test = label_generating_PRC(X_train, X_test, threshold)

    if model_name == 'CIBer':
        cont_col=[]
        min_asso = 0.95
        model = CIBer(cont_col=cont_col, asso_method="spearman", min_asso=min_asso, 
                        disc_method="uniform", joint_encode=True)
    elif model_name == 'LG':
        # instantiate the model (using the default parameters)
        model = LogisticRegression()
    elif model_name == 'MLP':
        model = MLPClassifier(solver='lbfgs', alpha=1e-5,
                    hidden_layer_sizes=(16), max_iter=500, random_state=1)
    elif model_name == 'RF':
        model = RandomForestClassifier(max_depth=3)
    elif model_name =='DT':
        model = tree.DecisionTreeClassifier(max_depth=3)
    #Model (CIBer) training
    print(model_name)

    model.fit(X_train.to_numpy(), y_train.to_numpy())
    probability = model.predict_proba(X_train.to_numpy())
    prior_proba = y_train.value_counts()/len(y_train) 
    print(prior_proba)
    #Start-Up of adjusted hawkes
    T_max = t_train.to_list()[-1]

    if training:
        model_count = adaptive_hawkes(T_max, num_class=len(), max_iter=max_iter)
        model_count.fit(probability, t_train)
    
    probability_test = model.predict_proba(X_test.to_numpy())
    if training:
        test_likelihood = model_count.log_likelihood(None, probability_test, t_test)
        print('test_likelihood at start-up iteration: ', test_likelihood)
    
    if name == 'PRC Data Breach Chronology.csv':
        if training:
            return model_count, probability, probability_test, t_train, t_test, X_train, X_test, y_train, y_test, severity_train, severity_test, weekly_freq_train, weekly_freq_test
        else:
            return probability, probability_test, t_train, t_test, X_train, X_test, y_train, y_test, severity_train, severity_test, weekly_freq_train, weekly_freq_test
    else:
        if training:
            return model_count, probability, probability_test, t_train, t_test, X_train, X_test, y_train, y_test, severity_train, severity_test, weekly_freq_train, weekly_freq_test
        else:
            return probability, probability_test, t_train, t_test, X_train, X_test, y_train, y_test, severity_train, severity_test, weekly_freq_train, weekly_freq_test
        
def data_preparation_multi(name, start = None, split=2016, end=None):

    data = pd.read_csv('PRC Data Breach Chronology.csv')
    data.columns
    column_name = ['Date Made Public', 'Type of breach', 'State', 'Type of organization']
    data = data[column_name]
    print('missing percentage: ', data.isna().sum()/data.shape[0])
    data = data.fillna(-1)

    data['Date Made Public'] = pd.to_datetime(data['Date Made Public'])
    # reorganize the data with the time order
    data = data.sort_values(by='Date Made Public')

    # Take a look at the data before 2008
    if start:
        data = data.loc[data['Date Made Public'].dt.year>=start]
    # map the state abbreviation to the full name
    # The types PHYS, PORT and STAT are gathered in a new category named Theft/Loss
    data['Type of breach'] = data['Type of breach'].apply(lambda x: 'THEFT/LOSS' if x in ['PHYS', 'PORT', 'STAT'] else x)
    # CARD and INSD in a new category named Other.
    data['Type of breach'] = data['Type of breach'].apply(lambda x: 'OTHER' if x in ['CARD', 'INSD'] else x)
    # Concerning the organisation types, with the same arguments, we grouped BSF, BSO and BSR in a category named BUSINESSES
    data['Type of organization'] = data['Type of organization'].apply(lambda x: 'BUSINESSES' if x in ['BSF', 'BSO', 'BSR'] else x)
    # NGO, EDU and GOV are put in a OtherOrga category
    data['Type of organization'] = data['Type of organization'].apply(lambda x: 'OTHERORG' if x in ['NGO', 'EDU', 'GOV'] else x)
    # we made a main group named OtherStates (71.1%) and kept the three biggest ones, namely, California (15.7%), Texas (6.9%) and New-York (6.3%).
    data['State'] = data['State'].apply(lambda x: 'OTHERSTATES' if x not in ['CA', 'TX', 'NY'] else x)
    # we divided the minto six groups by type of organization and type of breach and state
    # MED and DISC and OTHER
    group1 = data[(data['Type of organization'] == 'MED') & (data['Type of breach'] == 'DISC') & (data['State'] == 'OTHERSTATES')].index 
    # BUSINESSES and HACKING and OTHER
    group2 = data[(data['Type of organization'] == 'BUSINESSES') & (data['Type of breach'] == 'HACK') & (data['State'] == 'OTHERSTATES')].index
    # MED and Hack and OTHER
    group3 = data[(data['Type of organization'] == 'MED') & (data['Type of breach'] == 'HACK') & (data['State'] == 'OTHERSTATES')].index
    # MED and  THEFT/LOSS and CALIFORNIA
    group4 = data[(data['Type of organization'] == 'MED') & (data['Type of breach'] == 'THEFT/LOSS') & (data['State'] == 'CA')].index
    #MED and THEFT/LOSS and OTHER
    group5 = data[(data['Type of organization'] == 'MED') & (data['Type of breach'] == 'THEFT/LOSS') & (data['State'] == 'OTHERSTATES')].index
    # THE REST  
    group6 = data.index.difference(group1.union(group2).union(group3).union(group4).union(group5))

    # those missing values are mapp to unknown
    # assign the label(event type) to each group, the index of different groups are used to assign the label
    event_type = pd.Series(index=data.index)
    event_type[group6] = int(0)
    event_type[group1] = int(1)
    event_type[group2] = int(2)
    event_type[group3] = int(3)
    event_type[group4] = int(4)
    event_type[group5] = int(5)
    event_type = event_type.astype(int)
    event_type.reset_index(drop=True, inplace=True)

    event_times = data['Date Made Public']
    split_day = data['Date Made Public'][data['Date Made Public'].dt.year<split].iloc[-1]

    start_time = event_times.min()
    t_train = (event_times[event_times<=split_day] - start_time).dt.total_seconds() / (24 * 3600*7)  # Convert to days
    t_test = (event_times[event_times>split_day] - start_time).dt.total_seconds() / (24 * 3600*7)  # Convert to days

    train_type = event_type[:len(t_train)]
    test_type = event_type[len(t_train):]
    print('train test split: ', split_day)
    print('length of train: ', len(t_train))
    print('training start: ', event_times.min(), 'training end: ', split_day)

    return t_train, t_test, train_type, test_type
