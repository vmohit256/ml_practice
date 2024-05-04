import pandas as pd
import time
import warnings
warnings.filterwarnings('ignore')

class IMDBDataReader:
    # data_root_dir must have files like title.ratings.tsv/title.ratings.tsv, title.basics.tsv/title.basics.tsv, etc.
    # downloaded from the non-commercial IMDB data: https://developer.imdb.com/non-commercial-datasets/
    def __init__(self, data_root_dir):
        self.data_root_dir = data_root_dir
    

    """returns pandas df with these columns: tconst	averageRating	numVotes
    """
    def get_ratings(self, verbose=True):
        start_time = time.time()
        ratings_df = pd.read_csv(f'{self.data_root_dir}title.ratings.tsv/title.ratings.tsv', sep='\t')
        if verbose:
            print (f"Time taken to read ratings data: {time.time() - start_time} seconds")
        return ratings_df
    

    """returns pandas df with these columns: 
    'tconst', 'titleType', 'primaryTitle', 'isAdult', 'startYear', 'runtimeMinutes', 'genres'
    """
    def get_title_basics(self, verbose=True, 
                         allowed_title_types=['movie', 'tvSeries']):
        start_time = time.time()
        title_basics_df = pd.read_csv(f'{self.data_root_dir}title.basics.tsv/title.basics.tsv', sep='\t')\
            [['tconst', 'titleType', 'primaryTitle', 'isAdult', 'startYear', 'runtimeMinutes', 'genres']]\
            .query('titleType in @allowed_title_types and isAdult == 0')
        if verbose:
            print (f"Time taken to read title basics data: {time.time() - start_time} seconds")
        return title_basics_df
    

    """returns pandas df with these columns:
    'tconst', 'region', 'language'

    titles_to_fetch: dataframe with tconst column. 
    If provided, only the titles in this dataframe will be kept. 
    """
    def get_title_regions(self, verbose=True, titles_to_fetch=None):
        start_time = time.time()

        # obtain regions for titles
        region_to_name_mapping = {
            'US': 'US',
            'GB': 'UK',
            'IN': 'India',
            'CA': 'Canada',
            'AU': 'Australia',
            'JP': 'Japan',
            'FR': 'France'
        }
        default_languages = {
            'US': 'English',
            'GB': 'English',
            'IN': 'Hindi',
            'CA': 'English',
            'AU': 'English',
            'JP': 'Japanese',
            'FR': 'French'
        }
        full_language_names = {
            'en': 'English',
            'hi': 'Hindi',
            'ja': 'Japanese',
            'fr': 'French'
        }
        allowed_regions = list(region_to_name_mapping.keys())

        title_regions = pd.read_csv(f'{self.data_root_dir}title.akas.tsv/title.akas.tsv', sep='\t')\
            [['titleId', 'region', 'language']]\
            .rename(columns={'titleId': 'tconst'})\
            .query('region in @allowed_regions')
        
        if titles_to_fetch is not None:
            title_regions = title_regions.merge(titles_to_fetch[['tconst']].drop_duplicates(), on='tconst')
        
        title_regions = title_regions.drop_duplicates()
        
        title_regions['language'] = title_regions['language']\
            .apply(lambda x: full_language_names.get(x, x))
        # fillin null languages with default languages
        title_regions['language'] = title_regions\
            .apply(lambda r: r['language'] if r['language']!='\\N' 
                   else default_languages.get(r['region'], 'Others'), axis=1)
        title_regions['region'] = title_regions['region']\
            .apply(lambda x: region_to_name_mapping.get(x, x))

        # add a copy for all languages
        all_languages = title_regions.copy()
        all_languages['language'] = 'ALL'

        title_regions = pd.concat([title_regions, all_languages]).drop_duplicates()
        if verbose:
            print (f"Time taken to read title regions data: {time.time() - start_time} seconds")
        return title_regions
    
    """
    returns pandas df with these columns:
    tconst, category, primaryName

    titles_to_fetch: dataframe with tconst column. 
    If provided, only the titles in this dataframe will be kept. 
    """
    def get_title_to_names(self, verbose=True, 
                           allowed_categories=['actor', 'actress', 'director'],
                           titles_to_fetch=None):
        start_time = time.time()
        title_principal = pd.read_csv(f'{self.data_root_dir}title.principals.tsv/title.principals.tsv', sep='\t')\
            .query('category in @allowed_categories')\
            [['tconst', 'nconst', 'category']]
        if titles_to_fetch is not None:
            title_principal = title_principal.merge(titles_to_fetch[['tconst']].drop_duplicates(), on='tconst')

        name_basics = pd.read_csv(f'{self.data_root_dir}name.basics.tsv/name.basics.tsv', sep='\t')\
            [['nconst', 'primaryName']]

        title_to_names = title_principal\
            .merge(name_basics, on='nconst')\
            [['tconst', 'category', 'primaryName']]\
            .drop_duplicates()
        if verbose:
            print (f'Time taken to compute the final title to names dataframe: {(time.time()-start_time) / 60} mins')
        return title_to_names



