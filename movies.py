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

'''

def get_counts_df(df, column, idx):
    column_df = pd.DataFrame(df[column])
    column_counts = column_df[column].explode().value_counts()
    column_counts_df = column_counts.to_frame('counts').reset_index()
    column_counts_df = column_counts_df.rename(columns = {'index': column})
    column_counts_df = column_counts_df[column_counts_df.index <= idx]
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

def make_genre_specific_df(df, genre):
    return df[df[genre] == 1]

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

def get_xvar(list_of_variables):
    d = {}
    for idx, var in enumerate(list_of_variables):
        d[idx] = var
    return d

def create_new_var_list(d, list_of_idx):
    new_var_list = []
    for idx in list_of_idx:
        if (idx - 1) in d:
            new_var_list.append(d[(idx -1)])
    return new_var_list

def get_p_values_idx(results):
    p_values = np.array(results.pvalues)
    p_values_idx = np.argwhere(p_values < 0.05).reshape(1,-1).tolist()[0]
    return p_values_idx
































