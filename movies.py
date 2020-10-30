import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ast import literal_eval
import seaborn as sns
import math
from pandas.plotting import scatter_matrix
import statsmodels.api as sm

movies_meta = pd.read_csv('./archive/movies_metadata.csv')
#genres_df = pd.DataFrame(movies_meta['genres'])

'''
Cleaning Helper Functions

literal_return - tries to perform an evaluation of a literal Python string and if successful returns the literal. Called in df_str_to_literal.

df_str_to_literal - takes in a dataframe and column_name string and returns the dataframe column as the new literal type. 

dict_name_cleaner_ - takes in a dictionary, checks if the parameter is actually a dictionary, and if so returns a list of values corresponding to the 'name' key in that dictionary. If it is not a dictionary, it returns an empty list.




'''


def literal_return(val):
    try:
        return literal_eval(val)
    except (ValueError, SyntaxError) as e:
        return val

def df_str_to_literal(df, column_name):
    df[column_name] = df[column_name].apply(literal_return)
    return df[column_name]

def dict_name_cleaner(d):
    if isinstance(d, dict):
        return [d['name']]
    #Return empty list in case of missing/malformed data
    return []

def name_cleaner(list_of_dicts):
    if isinstance(list_of_dicts, list):
        return [d['name'] for d in list_of_dicts]
    return []

def countries_cleaner(list_of_dicts):
    if isinstance(list_of_dicts, list):
        return [d['iso_3166_1'] for d in list_of_dicts]
    return []

def language_cleaner(list_of_dicts):
    if isinstance(list_of_dicts, list):
        return [d['iso_639_1'] for d in list_of_dicts]
    return []

def budget_cleaner(string):
    if string.isnumeric():
        val = int(string)
        return val
    
    return 0



'''
Manipulating DataFrames Helper Functions

get_counts_df - takes in a dataframe with columns containing lists and returns a new dataframe with the items in the list exploded and reindexed to get total counts of the values in the lists across the entire dataframe. Can graph counts vs values easily.


'''

def get_counts_df(df, column):
    column_df = pd.DataFrame(df[column])
    column_counts = column_df[column].explode().value_counts()
    column_counts_df = column_counts.to_frame('counts').reset_index()
    column_counts_df = column_counts_df.rename(columns = {'index': column})
    
    return column_counts_df

def create_bool_columns(df, column_name, list_of_columns):
    for column in list_of_columns:
        df[column] = df[column_name].apply(lambda x: 1 if column in x else 0)

def broadcast_and_clean(df, broadcast_col, list_of_columns):
    out_df = df[[broadcast_col] + list_of_columns]
    
    for column in list_of_columns:
        out_df[column] = out_df[column]*out_df[broadcast_col]
    
    out_df = out_df.drop(columns = [broadcast_col])
    out_df = out_df.replace(0.0,np.nan)
    
    return out_df

def get_top(df, num, column, list_of_columns):
    out_df = df.nlargest(num, column)[list_of_columns]
    return out_df



'''
Plotting Helper Functions
'''

def make_scatter_matrix(df):
    s_matrix = scatter_matrix(df, figsize = (20,20))

    for ax in s_matrix.ravel():
        ax.set_xlabel(ax.get_xlabel(), fontsize = 20, rotation = 45)
        ax.set_ylabel(ax.get_ylabel(), fontsize = 20, rotation = 90)

def counts_horizontal_bar(df, x_column, y_column, x_min, x_max, x_inc, ax):
    x_data = df[x_column]
    y_data = df[y_column]
    y = np.arange(len(y_data))
    x = np.linspace(x_min, x_max, (x_max-x_min)//x_inc + 1, dtype='int')
    
    ax.barh(y_data, x_data)
    ax.invert_yaxis()
    ax.set_yticks(y)
    ax.set_xticks(x)
    ax.set_xticklabels(x, fontsize = 18, rotation = 45)
    ax.set_yticklabels(y_data, fontsize = 18)
    ax.xaxis.grid(True)
    fig.tight_layout()

def violin_plot_by_genre(data, x_labels, y_label, title):
    sns.set(style='whitegrid')
    fig, ax = plt.subplots(figsize=(20,10))
    ax.set_ylabel(y_label, fontsize = 24)
    ax.set_title(title, fontsize = 24)
    plt.yticks(fontsize=20)
    ax.set_xticklabels(x_labels, fontsize = 20, rotation=45)
    sns.violinplot(data=data, ax=ax)
    fig.tight_layout()








'''
Linear Regression Model and Plot Helper Functions
'''

def model_linear_regression(df, target_col, lst_variable_cols):
    sorted_df = df.sort_values(by = [target_col])
    target = np.array(sorted_df[target_col])
    
    variables_df = sorted_df[lst_variable_cols]
    X = np.array(sm.add_constant(variables_df))
    
    model = sm.OLS(target, X)
    results = model.fit()
    residuals = results.resid
    return X, target, results, residuals
    
def plot_predictions_vs_actual(X, target, results, x_label, y_label, actual_label, predict_label):
    betas = np.array(results.params).reshape(-1,1)
    y_p = np.dot(X, betas)
    
    x = np.arange(len(target))
    
    fig = plt.figure(figsize=(10,6))
    ax = fig.add_subplot(111)
    ax.plot(x, target, label=actual_label)
    ax.plot(x, y_p, c='r',label=predict_label)
    ax.set_xlabel(x_label, fontsize = 20)
    ax.set_ylabel(y_label, fontsize = 20)
    ax.legend()

def plot_residuals(X, target, results, residuals, x_label='Predicted', y_label='Residuals'):
    fig, ax = plt.subplots()
    y_predict = results.predict(X)
    ax.scatter(y_predict, residuals, alpha=0.5)
    ax.axhline(0, color='r', ls='--')
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

def qq_plot(X, target, results, title='QQ Plot vs Normal Distribution for Residuals'):
    fig, ax = plt.subplots(figsize = (8, 8))
    y_predict = results.predict(X)
    stats.probplot(target - y_predict, plot=ax)
    ax.set_title(title, fontsize = 18)








'''
Genres_cleaner - returns the value for the 'name' key in each dictionary in the list of dictionaries when mapped to a column of a dataframe
'''    


genres_lists = str_to_list_of_dicts(df = genres_df, column_name = 'genres').map(genres_cleaner)
#print(genres_lists.head())

genres_counts = genres_lists.explode().value_counts()
#print(genres_counts)

genres_counts_df = genres_counts.to_frame('counts').reset_index()
genres_counts_df = genres_counts_df.rename(columns = {'index': 'genre'})
#print(genres_counts_df)

genres_counts_df = genres_counts_df[genres_counts_df.counts > 1]
#print(genres_counts_df)


'''
Generate Bool Columns - creates boolean columns in the dataframe for each unique item in list of columns
'''

def create_bool_columns(df, column_name, list_of_columns):
    for column in list_of_columns:
        df[column] = df[column_name].apply(lambda x: column in x)


genres_list = genres_counts_df['genre'].tolist()
#print(genres_list)

create_bool_columns(df = movies_meta, column_name = 'genres', list_of_columns = genres_list)
#print(movies_meta.head())

'''
Helper function to create genre specific dataframes - I tried to automate this by feeding in a list of genres and desired datafame names and zipping them together to return dataframes, but I couldn't get it work.
'''

def make_genre_specific_df(df, genre):
    return df[df[genre] == True]

# drama = make_genre_specific_df(movies_meta, 'Drama')
# comedy = make_genre_specific_df(movies_meta, 'Comedy')
# thriller = make_genre_specific_df(movies_meta, 'Thriller')
# romance = make_genre_specific_df(movies_meta, 'Romance')
# action = make_genre_specific_df(movies_meta, 'Action')
# horror = make_genre_specific_df(movies_meta, 'Horror')
# crime = make_genre_specific_df(movies_meta, 'Crime')
# documentary = make_genre_specific_df(movies_meta, 'Documentary')
# adventure = make_genre_specific_df(movies_meta, 'Adventure')
# science_fiction = make_genre_specific_df(movies_meta, 'Science Fiction')
# family = make_genre_specific_df(movies_meta, 'Family')
# mystery = make_genre_specific_df(movies_meta, 'Mystery')
# fantasy = make_genre_specific_df(movies_meta, 'Fantasy')
# animation = make_genre_specific_df(movies_meta, 'Animation')
# foreign = make_genre_specific_df(movies_meta, 'Foreign')
# music = make_genre_specific_df(movies_meta, 'Music')
# history = make_genre_specific_df(movies_meta, 'History')
# war = make_genre_specific_df(movies_meta, 'War')
# western = make_genre_specific_df(movies_meta, 'Western')
# tv_movie = make_genre_specific_df(movies_meta, 'TV Movie')


'''
Clean Production Companies, Production Countries, Spoken Languages
'''

prod_companies_df = pd.DataFrame(movies_meta['production_companies'])
prod_countries_df = pd.DataFrame(movies_meta['production_countries'])
spoken_language_df = pd.DataFrame(movies_meta['spoken_languages'])

prod_companies_lists = str_to_list_of_dicts(df = prod_companies_df, column_name = 'production_companies').map(genres_cleaner)

def countries_cleaner(list_of_dicts):
    if isinstance(list_of_dicts, list):
        return [d['iso_3166_1'] for d in list_of_dicts]
    return []

def language_cleaner(list_of_dicts):
    if isinstance(list_of_dicts, list):
        return [d['iso_639_1'] for d in list_of_dicts]
    return []

countries_lists = str_to_list_of_dicts(df = prod_countries_df, column_name = 'production_countries').map(countries_cleaner)
#print(countries_lists.head())

language_lists = str_to_list_of_dicts(df = spoken_language_df, column_name = 'spoken_languages').map(language_cleaner)
#print(language_lists.head())

'''
Budget Cleaner - takes budget column which was a string object and converts it to an int
'''

def budget_cleaner(string):
    if string.isnumeric():
        val = int(string)
        return val
    
    #in the case of missing or non-numeric data (there was a .jpg in this column for some reason)
    return 0



































