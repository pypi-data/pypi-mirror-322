# Moneyline 
Moneyline is a python package meant to help detect arbitrage opportunities in sports (only for moneyline bets). 


FOR MONEYLINE BETS, run these functions sequentially to get the final dataframe that is structured to detect arbitrage and non-arbitrage opportunities

fetch_and_process_ml_data(api_key, sports, regions), where the api key is a string, and sports and regions are lists of strings; returns df

group_event_ml(df)

find_arb_ml(result_df)



FOR SPREADS AND TOTALS follow the exact same sequence of functions, but call:

fetch_and_process_spreads_totals_data(api_key, sports, regions)

group_event_spreads_totals(df)

find_arb_spreads_totals(df)



FOR PLAYER PROPS

fetch_player_props(api_key)

group_player_odds(df)

find_arb_player(df)


Player Prop Markets are built in and include:
SPORTS_MARKETS = {
        'basketball_nba': 'player_points,player_blocks,player_assists,player_steals,player_rebounds',
        'icehockey_nhl': 'player_points,player_goals,player_assists',
        'soccer_epl': 'player_shots,player_assists,player_shots_on_target',
        'soccer_france_ligue_one': 'player_shots,player_assists,player_shots_on_target',
        'soccer_germany_bundesliga': 'player_shots,player_assists,player_shots_on_target',
        'soccer_italy_serie_a': 'player_shots,player_assists,player_shots_on_target',
        'soccer_spain_la_liga': 'player_shots,player_assists,player_shots_on_target',
        'soccer_usa_mls': 'player_shots,player_assists,player_shots_on_target'
    }



FOR AUTOMATED EMAIL sending, use:

send_arb_email(email_body)


## Installation 
```bash 
pip install moneyline
