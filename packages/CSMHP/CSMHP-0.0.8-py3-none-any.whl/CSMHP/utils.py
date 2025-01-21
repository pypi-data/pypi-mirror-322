import pandas as pd
import numpy as np
#from CIBer import CIBer
import scipy.optimize as opt
from sklearn.linear_model import LogisticRegression
from category_encoders import TargetEncoder
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import tree



def data_preparation(name, split = 2021, start = None, end=None, num_states=12, method='bycount'):
    if name == 'breach_report_all.csv':
        data = pd.read_csv('breach_report_all.csv')
    else:
        data = pd.read_csv('Data_Breaches1.csv')
    #data.drop_duplicates(inplace=True)
    print('missing percentage: ', data.isna().sum()/data.shape[0])
    #Drop the columns that
    data.drop(columns=['Web Description','Name of Covered Entity'], inplace=True)
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
    #data.drop_duplicates(inplace=True)
    print('train test split: ', split)

    #we may only focus on the time period from 2011-2020, use the first 8 years as training set, last two for testing

    # #there are too many states in the state column, we reduce the number of them to have more frequencies
    def encoding_by_count(data):
        data = data.copy(deep= True)
        # Calculate frequencies
        location_counts = data.value_counts()
        
        if len(data.unique())> 10:
            mapping = pd.cut(location_counts, bins=8, labels=False)
            return mapping
            #print(stop)
            #return pd.cut(ranked, bins=8, labels=False)
        else:
            # Map locations to their frequency
            mapping = location_counts.rank(method='dense', ascending=False) - 1
            encoded = data.map(mapping)
            #Rank the frequencies
            # ranked = encoded.rank(method='dense', ascending=False) - 1
            #Normalize ranks to 0-4 (assuming you want 5 bins)
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

        # top_categories = data['State'].value_counts().nlargest(num_states).index
        # data['State'] = data['State'].apply(lambda x: x if x in top_categories else 'Other')
        
        data['Covered Entity Type'] = pd.factorize(data['Covered Entity Type'])[0]
        data['Type of Breach'] = pd.factorize(data['Type of Breach'])[0]
        data['Business Associate Present'] = pd.factorize(data['Business Associate Present'])[0]
        
        # if test_year == 2016:
        #     df_train = data.loc[split:].copy(deep=True)
        #     df_test = data.loc[:split].copy(deep=True)
        # elif test_year == 2020:
        df_train = data.loc[:str(split)].copy(deep=True)
        df_test = data.loc[str(split):].copy(deep=True)

        mapping = encoding_by_count(df_train['State'])
        df_train['State'] = df_train['State'].map(mapping)
        df_test['State'] = df_test['State'].map(mapping)
    
    # elif method == 'freq':
    #     encoding_dict = df_train.value_counts(normalize=False).to_dict()
    #     X_train_encoded = df_train.map(encoding_dict)
    #     X_test_encoded = df_test.map(encoding_dict)
    #     return X_train_encoded, X_test_encoded
    
    elif method == 'target':
        encoder = TargetEncoder()
        X_train_encoded = encoder.fit_transform(df_train, df_train)
        X_test_encoded = encoder.transform(df_test)
        return X_train_encoded, X_test_encoded
        
    return df_train, df_test


def label_generating(X_train, X_test, threshold):
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

def new_algorithm(name, unit_name='week', model_name0='modified', model_name = 'CIBer', times = (2009, 2021, None),  methods='bycount', max_iter=20, training=True):
    if unit_name == 'week':
        unit = 7
    elif unit_name == 'day':
        unit = 1
    elif unit_name == 'forthright':
        unit = 14

    #Data importing
    start = times[0]
    split = times[1]
    end = times

    if model_name != 'CIBer':
        train, test = data_preparation(name, split = split, start=start, method='label')
    else:
        train, test = data_preparation(name, split = 2021, method=methods)
    start_time = train['Breach Submission Date'].min()

    #train test split
    t_train = (train['Breach Submission Date'] - start_time).dt.total_seconds() / (24 * 3600 * unit)  # Convert to days
    print('data_number: ', len(t_train))
    X_train = train.drop(columns=['Breach Submission Date'])
    t_test = (test['Breach Submission Date'] - start_time).dt.total_seconds() / (24 * 3600 * unit)  # Convert to days
    X_test = test.drop(columns=['Breach Submission Date'])


    #generate pusedo cluster label by CIBer
    threshold = (20,70)

    y_train, y_test = label_generating(X_train, X_test, threshold)
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
                    hidden_layer_sizes=(16), max_iter=200, random_state=1)
    elif model_name == 'RF':
        model = RandomForestClassifier(max_depth=3)
    elif model_name =='DT':
        model = tree.DecisionTreeClassifier(max_depth=3)

    print(model_name)


    model.fit(X_train.to_numpy(), y_train.to_numpy())
    probability = model.predict_proba(X_train.to_numpy())
    prior_proba = y_train.value_counts()/len(y_train) 
    print(prior_proba)
    #Start-Up of adjusted hawkes
    T_max = t_train.to_list()[-1]
    # test = hawkes(T_max)
    # test.fit(t_train)
    # test.log_likelihood(None, t_test)

    #model_count = modified_hawkes(T_max, prior_proba,prior_proba,prior_proba)
    if training:
        if model_name0 == 'modified':
            model_count = modified_hawkes(T_max, prior_proba)
        elif model_name0 == 'adjusted':
            model_count = adjusted_hawkes(T_max, prior_proba)
        model_count.fit(probability, t_train)
    
    probability_test = model.predict_proba(X_test.to_numpy())
    if training:
        test_likelihood = model_count.log_likelihood(None, probability_test, t_test)
        print('test_likelihood at start-up iteration: ', test_likelihood)
    
    if training:
        return model_count, probability, probability_test, t_train, t_test, X_train, X_test, y_train, y_test
    else:
        return probability, probability_test, t_train, t_test, X_train, X_test, y_train, y_test
