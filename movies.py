import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ast import literal_eval

movies_meta = pd.read_csv('./archive/movies_metadata.csv')
genres_df = pd.DataFrame(movies_meta['genres'])

'''
Str_to_list_of_dicts - takes a column from a dataframe (where the data type is a string object that looks like a list of dictionaires) and converts it to a dataframe where the column is a list of dictionaries 
'''
def str_to_list_of_dicts(df, column_name):
    df[column_name] = df[column_name].apply(lambda x: literal_eval(x))
    return df[column_name]

'''
Genres_cleaner - returns the value for the 'name' key in each dictionary in the list of dictionaries when mapped to a column of a dataframe
'''    

def genres_cleaner(list_of_dicts):
    return [ d['name'] for d in list_of_dicts]

genres_list = str_to_list_of_dicts(df = genres_df, column_name = 'genres').map(genres_cleaner)
print(genres_list.head())




























