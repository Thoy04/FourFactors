import pandas as pd
from nba_api.stats.endpoints import leaguedashteamstats


def calc_scores(df):
    df['off_score'] = .4*df['EFG_PCT'] + .25*df['TM_TOV_PCT'] + .2*df['OREB_PCT'] + .15*df['FTA_RATE']
    df['def_score'] = .4*df['OPP_EFG_PCT'] + .25*df['OPP_TOV_PCT'] + .2*df['OPP_OREB_PCT'] + .15*df['OPP_FTA_RATE']
    return df


def get_seasons(start_year, end_year):
    """helper function to get list of years in required format for API"""
    seasons = [f"{year}-{str(year + 1)[2:]}" for year in range(start_year, end_year)]
    return seasons


class CreateDf:
    """class to create dataframe using years provided when instantiated"""
    def __init__(self, start_year, end_year):
        self.start_year = start_year
        self.end_year = end_year
        self.df = pd.DataFrame()
        self.seasons_list = get_seasons(self.start_year,  self.end_year)

    def create_df(self):
        """method to gather data from api and create dataframe"""
        for season in self.seasons_list:
            stats = leaguedashteamstats.LeagueDashTeamStats(measure_type_detailed_defense='Four Factors', season=season)
            stats_df = stats.get_data_frames()[0]
            stats_df['season'] = season
            self.df = pd.concat([self.df, stats_df], ignore_index=True)
            self.df = calc_scores(self.df)
        return self.df


test = CreateDf(1996, 2024)
df = test.create_df()
df.to_csv('C:/Users/sierr/Desktop/NBAProject/FourFactorsV2.csv')


