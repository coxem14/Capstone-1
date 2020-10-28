import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ast import literal_eval

movies_meta = pd.read_csv('./archive/movies_metadata.csv')
genres_df = pd.DataFrame(movies_meta['genres'])

'''
Str_to_list_of_dicts - takes a column from a dataframe (where the data type is a string object that looks like a list of dictionaires) and converts it to a dataframe where the column is a list of dictionaries 
'''

def literal_return(val):
    try:
        return literal_eval(val)
    except (ValueError, SyntaxError) as e:
        return val


def str_to_list_of_dicts(df, column_name):
    df[column_name] = df[column_name].apply(literal_return)
    return df[column_name]

'''
Genres_cleaner - returns the value for the 'name' key in each dictionary in the list of dictionaries when mapped to a column of a dataframe
'''    

def genres_cleaner(list_of_dicts):
    if isinstance(list_of_dicts, list):
        return [d['name'] for d in list_of_dicts]
    #Return empty list in case of missing/malformed data
    return []

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



































