import itertools
from pathlib import Path

import pandas as pd
import numpy as np


def scrape_html_tables(required_events, required_genders, required_years):
    
    event_selectors = itertools.product(required_events, required_genders, required_years)
    
    combined_dfs = {}

    for selector in event_selectors:
        event, gender, year = selector
        url = f"https://www.thepowerof10.info/rankings/rankinglist.aspx?event={event}&agegroup=ALL&sex={gender}&year={year}"
        dfs = pd.read_html(url)
        combined_dfs[f"{event}_{gender}_{year}"] = dfs[3]
        
    return combined_dfs


def clean_dataframes(raw_dataframes):
    cleaned_dataframes = {}

    for event, df in raw_dataframes.items():
        cleaned_df = (df
            .drop(columns=[2, 3, 5, 13])
            .rename(columns=df.loc[1].str.lower())
            .rename(columns={np.nan: 'age_group'})
            .drop(labels=[0, 1], axis=0)
            .dropna(axis=0, subset=['rank'])
            .query('rank.str.isdigit()')
            .assign(pb = lambda df_: df_['pb'].str.split('/').str[0],
                    age_group = lambda df_: df_['age_group'].fillna('Senior'),
                    date = lambda x: pd.to_datetime(x['date'], format='%d %b %y'),
                    coach = lambda df_: df_['coach'].str.encode('ascii', 'ignore').str.decode('utf-8').replace(np.nan, 'No coach'),
                    year = lambda df_: df_['year'].replace(np.nan, ''),
                    sport = 'Athletics',
                    event = event.split('_')[0],
                    gender = event.split('_')[1]
                    
            )
            .reset_index(drop=True)
        )

        cleaned_dataframes[event] = cleaned_df

    return cleaned_dataframes


def dataframe_to_csv(cleanded_dataframes, filepath):
    for event, df in cleanded_dataframes.items():
        df.to_csv(f"{filepath}/{event}.csv", index=False)


if __name__ =="__main__":
    required_events = [100, 200, 400]
    required_genders = ["W", "M"]
    required_years = [2020]

    current_file_path = Path(__file__).resolve()
    parent_directory = current_file_path.parent

    results_directory = parent_directory / 'results'
    results_directory.mkdir(exist_ok=True)

    raw_dfs = scrape_html_tables(required_events, required_genders, required_years)
    clean_dfs = clean_dataframes(raw_dfs)
    dataframe_to_csv(clean_dfs, results_directory)
