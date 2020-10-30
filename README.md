**********************************************
# MoviEDA - Predicting Box Office Revenues
**********************************************

#### Erin Cox
#### https://github.com/coxem14/Capstone-1
*Last update: 10/30/2020*
***

<p align = 'center'>
    <img #src = 'https://media.giphy.com/media/8lKyuiFprZaj2lC3WN/giphy.gif'>
</p>

## Table of Contents
1. [Background](#Lights)
2. [Data](#Camera)
3. [Analysis](#Action)
    * [Introduction](#Meet-Cute)
    * [Data Cleaning](#Pursuit)
    * [EDA](#Montage)
4. [Final Thoughts](#The-Goodbye) 
    * [Future Ideas](#Flash-Forward)

## Lights

 Movies touch many lives on a daily basis. They inspire us, educate us, and at times impact our beliefs, culture, and values. For some, movies offer a way to escape reality and unwind. For others, they provide an avenue for spending quality time with family and friends. However, film is much more than that. In 2019, the worldwide revenue for the film and streaming industry hit a record $100 billion USD<sup>[1]</sup>, with box office revenue surpassing $42 billion USD<sup>[2]</sup>. In the US, film and television support 2.5 million jobs, and pays over 180 billion USD in annual wages<sup>[3]</sup>. There is a lot of money to be made in movies, but no surefire way to make a profit. Data science allows us to analyze the factors which influence how a movie performs and make predictions about what audiences want.

## Camera
I have always been a huge fan of movies, so when I saw [The Movie Dataset](https://www.kaggle.com/rounakbanik/the-movies-dataset) on Kaggle, I took advantage of the opportunity to explore my interest while learning more about exploratory data analysis. The dataset is a combination of data collected from [TMDB](https://www.themoviedb.org/) (The Movie Database) API and [GroupLens](https://grouplens.org/datasets/movielens/latest/). 

Out of the 5 unique csv files included in the dataset, I used the following: 
> 1. movies_metadata.csv - the primary metadata file that includes information on 45k+ movies
> 2. ratings.csv - ratings from GroupLens users

There were also files containing movie plot keywords, credits, and links to all the movies in the Full MovieLens dataset. I might explore these further when I learn about NLP.

## Action

I utilized [Jupyter Notebook](https://github.com/coxem14/Capstone-1/blob/main/MoviEDA.ipynb) for my analysis, and consolidated the functions I wrote to aid in data cleaning, data manipulating, and plotting into my [movies.py](https://github.com/coxem14/Capstone-1/blob/main/movies.py) file.

### The Meet-Cute

<p align = 'center'>
    <img src = 'https://github.com/coxem14/Capstone-1/blob/main/images/dataset_snapshot.png'>
</p>

I began my analysis by familiarizing myself with my dataset. There were 24 columns, with a variety of datatypes. 

<p align = 'center'>
    <img src = 'https://github.com/coxem14/Capstone-1/blob/main/images/original_dataset_info.png'>
</p>

I investigated each column, eliminated those I would need more advanced NLP or image processing techniques to use, and I was able to narrow down my dataset to a few columns of particular interest.

> * Appeared to be dictionaries or lists of dictionaries, but were actually strings
>   * belongs_to_collection
>   * genres
>   * production_companies
>   * spoken_languages 
> * Mixture of different types, ranging from strings, floats, ints or combination thereof
>   * id
>   * budget
>   * popularity
>   * revenue
>   * runtime
>   * vote_average
>   * vote_count
> * String, pretty straight forward
>   * title
> * Appeared to be date, but was - you guessed it - a string
>   * release_date    

### The Pursuit

```
def literal_return(val):
    try:
        return literal_eval(val)
    except (ValueError, SyntaxError) as e:
        return val

def df_str_to_literal(df, column_name):
    df[column_name] = df[column_name].apply(literal_return)
    return df[column_name]

def name_cleaner(list_of_dicts):
    if isinstance(list_of_dicts, list):
        return [d['name'] for d in list_of_dicts]
    #Return empty list in case of missing/malformed data
    return []
```

### Unexpected Visitor



### Montage


### Flash Forward


<p align = 'center'>
    <img #src = 'https://media.giphy.com/media/l4FAPaGGeB7D1LfIA/giphy.gif'>
</p>

### Citations

[The Hollywood Reporter](https://www.hollywoodreporter.com/news/fueled-by-streaming-global-entertainment-market-hit-record-100-billion-2019-1283800)

[MPA - 2019 THEME Report](https://www.motionpictures.org/wp-content/uploads/2020/03/MPA-THEME-2019.pdf)

[Motion Picture Association](https://www.motionpictures.org/what-we-do/driving-economic-growth/)

[Back to Top](#Table-of-Contents)

## Ideas for section names

### Reversal of Expectations

### Revelation

### Flashback

### Dream

### Emotional Breakdown

### Training

### Celebration

### Shocking

### Aftermath

## Proposal: MoviEDA

Some ideas to explore:

> * Various relationships between movie budget, revenues, genres, ratings, release date, production company, and language.
> * How have budgets and revenues for movies changed over time? 
> * Are there relationships between the budget for a movie and how much revenue it generates? 
> * Do certain genres of movies generate more revenue than others? Higher ratings than others?
> * Does runtime impact budget, revenue, or rating?





































