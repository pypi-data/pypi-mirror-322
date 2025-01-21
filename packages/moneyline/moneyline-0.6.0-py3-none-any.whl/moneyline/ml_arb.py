import requests
import pandas as pd

def fetch_and_process_ml_data(api_key, sports, regions):
    all_odds_data = {}
    rows = []

    # Loop through each sport/league to get and process data
    for sport in sports:
        sport = sport.strip()  # Clean up whitespace
        print(f"\nFetching odds data for {sport}...")
        url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds/"

        # Define query parameters
        params = {
            'apiKey': api_key,
            'regions': ','.join(regions),  # Join regions list into a comma-separated string
            'markets': 'h2h'
        }

        # Make the GET request
        response = requests.get(url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            odds_data = response.json()  # Parse the JSON response
            all_odds_data[sport] = odds_data  # Store data for each sport

            # Process the odds data into rows
            for game in odds_data:
                sport_title = game['sport_title']
                commence_time = game['commence_time']
                home_team = game['home_team']
                away_team = game['away_team']

                for bookmaker in game.get('bookmakers', []):
                    bookmaker_name = bookmaker['title']

                    for market in bookmaker.get('markets', []):
                        market_key = market['key']
                        last_update = market['last_update']

                        # Extract odds for each outcome
                        outcomes = market.get('outcomes', [])
                        for outcome in outcomes:
                            outcome_name = outcome['name']
                            price = outcome['price']

                            # Append a row with the relevant data
                            rows.append({
                                'Sport': sport_title,
                                'Commence Time': commence_time,
                                'Home Team': home_team,
                                'Away Team': away_team,
                                'Bookmaker': bookmaker_name,
                                'Market': market_key,
                                'Last Update': last_update,
                                'Outcome': outcome_name,
                                'Odds': price
                            })
        else:
            print(f"Error for {sport}: {response.status_code}")
            print(response.text)

    # Convert list of rows to a DataFrame
    df = pd.DataFrame(rows)

    # Display the DataFrame
    pd.set_option('display.max_columns', None)  # Show all columns
    pd.set_option('display.expand_frame_repr', False)  # Don't wrap rows
    pd.set_option('display.width', 1000)
    print(df)
    return df


def group_event_ml(df):
    df = df[df['Market'] != 'h2h_lay']
    df["Commence Time"] = pd.to_datetime(df["Commence Time"])
    df["Last Update"] = pd.to_datetime(df["Last Update"])
    # Calculate the difference and remove the days part
    df['Time Difference'] = pd.to_datetime(df['Commence Time']) - pd.to_datetime(df['Last Update'])

            # convert to hours
    df['Time Difference (Hours)'] = df['Time Difference'].dt.total_seconds() / 3600

    sport_mapping = {
        'La Liga - Spain': 'Soccer',
        'EPL': 'Soccer',
        'Serie A - Italy': 'Soccer',
        'Ligue 1 - France': 'Soccer',
        'Bundesliga - Germany': 'Soccer',
        'MLS': 'Soccer',
        'NBA': 'Basketball',
        'ATP Paris Masters': 'Tennis',
        'NCAAF': 'College Football',
        'Test Matches': 'Cricket',
        'One Day Internationals': 'Cricket',
        'International Twenty20': 'Cricket'
        }
    
    # Map the Sports column to the new Sport Type column
    df['Sport Type'] = df['Sport'].map(sport_mapping)



    #   Assuming df is your DataFrame and 'Last Update' is in datetime format
    df['Last Update'] = pd.to_datetime(df['Last Update'])  # Convert to datetime if not already

    # Extract the hour and convert it to 1-24 format
    df['Hour Bucket'] = df['Last Update'].dt.hour + 1
    df = df.sort_values('Last Update', ascending=False)

    # Drop duplicates to keep the most recent odds for each unique combination of 'Sport', 'Commence Time', 'Home Team', 'Away Team', 'Bookmaker', 'Market', 'Outcome'
    df = df.drop_duplicates(subset=['Sport', 'Commence Time', 'Home Team', 'Away Team', 'Bookmaker', 'Market', 'Outcome', ])

    # Initialize lists to store the processed rows
    grouped_data = []

    # Iterate through each unique event
    for _, group in df.groupby(['Sport', 'Commence Time', 'Home Team', 'Away Team', 'Bookmaker', 'Market', 'Time Difference', 'Sport Type', "Hour Bucket"]):
        # Create a dictionary for storing the combined row
        event_data = group.iloc[0][['Sport', 'Commence Time', 'Home Team', 'Away Team', 'Bookmaker', 'Market', 'Time Difference', 'Sport Type', 'Hour Bucket']].to_dict()

        # Set default odds for each outcome type
        event_data['odds1'] = 0
        event_data['odds2'] = 0
        event_data['odds3'] = 0

        # Populate the odds fields
        for _, row in group.iterrows():
            if row['Outcome'] == row['Home Team']:
                event_data['odds1'] = row['Odds']
            elif row['Outcome'] == row['Away Team']:
                event_data['odds2'] = row['Odds']
            elif row['Outcome'] == 'Draw':
                event_data['odds3'] = row['Odds']

        # Append the combined row to the list
        grouped_data.append(event_data)

    # Create a new DataFrame from the grouped data
    result_df = pd.DataFrame(grouped_data)

    # Add columns for the probabilities (1/odds)
    result_df['probability1'] = result_df['odds1'].apply(lambda x: 1/x if x > 0 else 0)
    result_df['probability2'] = result_df['odds2'].apply(lambda x: 1/x if x > 0 else 0)
    result_df['probability3'] = result_df['odds3'].apply(lambda x: 1/x if x > 0 else 0)

    # Add a column for the total probability sum
    result_df['total_probability'] = result_df['probability1'] + result_df['probability2'] + result_df['probability3']

    return result_df

def find_arb_ml(result_df):
    result_df['event_name']=result_df['Home Team']+'_'+result_df['Away Team']
    results = []

    for event, group in result_df.groupby('event_name'):
    # Get the row with the minimum probability1 for the event
        min_odds_1_row = group.loc[group['probability1'].idxmin()]

    # Get the row with the minimum probability2 for the event
        min_odds_2_row = group.loc[group['probability2'].idxmin()]

    # Get the row with the minimum probability3 for the event
        min_odds_3_row = group.loc[group['probability3'].idxmin()]

    # Extract relevant values
        odds_1_prob = min_odds_1_row['probability1']
        odds_2_prob = min_odds_2_row['probability2']
        odds_3_prob = min_odds_3_row['probability3']
        bookmaker_1 = min_odds_1_row['Bookmaker']
        bookmaker_2 = min_odds_2_row['Bookmaker']
        bookmaker_3 = min_odds_3_row['Bookmaker']

    # Calculate the sum of the minimum probabilities
        odds_sum = odds_1_prob + odds_2_prob + odds_3_prob

    # Determine if it's an arbitrage opportunity
        arbitrage = 1 if odds_sum < 1 else 0

    # Append the results to the list
        results.append({
            'event_name': event,
            'odd_1_prob': odds_1_prob,
            'bookmaker_1': bookmaker_1,
            'odd_2_prob': odds_2_prob,
            'bookmaker_2': bookmaker_2,
            'odd_3_prob': odds_3_prob,
            'bookmaker_3': bookmaker_3,
            'odds_sum': odds_sum,
            'arbitrage': arbitrage,
            'Time Difference': min_odds_1_row['Time Difference'],  # Assuming time difference is the same for all rows in the event
            'Sport Type': min_odds_1_row['Sport Type'],
            'Hour Bucket': min_odds_1_row['Hour Bucket']

        })
    
    return pd.DataFrame(results)



def fetch_and_process_spreads_totals_data(api_key, sports, regions):
    all_odds_data = {}
    rows = []

    # Loop through each sport/league to get and process data
    for sport in sports:
        sport = sport.strip()  # Clean up whitespace
        print(f"\nFetching odds data for {sport}...")
        url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds/"

        # Define query parameters with hardcoded markets
        params = {
            'apiKey': api_key,
            'regions': ','.join(regions),  # Join regions list into a comma-separated string
            'markets': 'spreads,totals'    # Hardcoded markets parameter
        }

        # Make the GET request
        response = requests.get(url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            odds_data = response.json()  # Parse the JSON response
            all_odds_data[sport] = odds_data  # Store data for each sport

            # Process the odds data into rows
            for game in odds_data:
                sport_title = game['sport_title']
                commence_time = game['commence_time']
                home_team = game['home_team']
                away_team = game['away_team']

                for bookmaker in game.get('bookmakers', []):
                    bookmaker_name = bookmaker['title']

                    for market in bookmaker.get('markets', []):
                        market_key = market['key']
                        last_update = market['last_update']

                        # Extract odds for each outcome
                        outcomes = market.get('outcomes', [])
                        for outcome in outcomes:
                            outcome_name = outcome['name']
                            price = outcome['price']
                            point = outcome.get('point')

                            # Determine odds type based on market and outcome
                            odds_type = ''
                            if market_key == 'totals':
                                odds_type = 'Over' if outcome_name == 'Over' else 'Under'
                            elif market_key == 'spreads':
                                odds_type = 'Underdog' if point > 0 else 'Favorite'

                            # Append a row with the relevant data
                            rows.append({
                                'Sport': sport_title,
                                'Commence Time': commence_time,
                                'Home Team': home_team,
                                'Away Team': away_team,
                                'Bookmaker': bookmaker_name,
                                'Market': market_key,
                                'Last Update': last_update,
                                'Outcome': outcome_name,
                                'Odds': price,
                                'Point': point,
                                'odds_type': odds_type
                            })
        else:
            print(f"Error for {sport}: {response.status_code}")
            print(response.text)

    # Convert list of rows to a DataFrame
    df = pd.DataFrame(rows)

    # Display the DataFrame
    pd.set_option('display.max_columns', None)
    pd.set_option('display.expand_frame_repr', False)
    pd.set_option('display.width', 1000)
    print(df)
    return df



def group_event_spreads_totals(df):
    df = df[df['Market'] != 'h2h_lay']
    df["Commence Time"] = pd.to_datetime(df["Commence Time"])
    df["Last Update"] = pd.to_datetime(df["Last Update"])
#    Calculate the difference and remove the days part
    df['Time Difference'] = pd.to_datetime(df['Commence Time']) - pd.to_datetime(df['Last Update'])

    # convert to hours
    df['Time Difference (Hours)'] = df['Time Difference'].dt.total_seconds() / 3600
    sport_mapping = {
    'La Liga - Spain': 'Soccer',
    'EPL': 'Soccer',
    'Serie A - Italy': 'Soccer',
    'Ligue 1 - France': 'Soccer',
    'Bundesliga - Germany': 'Soccer',
    'MLS': 'Soccer',
    'NBA': 'Basketball',
    'ATP Paris Masters': 'Tennis',
    'NCAAF': 'College Football',
    'americanfootball_nfl': 'NFL',
    'Test Matches': 'Cricket',
    'One Day Internationals': 'Cricket',
    'International Twenty20': 'Cricket'
    }

# Map the Sports column to the new Sport Type column
    df['Sport Type'] = df['Sport'].map(sport_mapping)



# Assuming df is your DataFrame and 'Last Update' is in datetime format
    df['Last Update'] = pd.to_datetime(df['Last Update'])  # Convert to datetime if not already

# Extract the hour and convert it to 1-24 format
    df['Hour Bucket'] = df['Last Update'].dt.hour + 1

    df.tail()

    df = df.sort_values('Last Update', ascending=False)

    # Drop duplicates
    df = df.drop_duplicates(subset=['Commence Time', 'Home Team', 'Away Team', 'Bookmaker', 'Market', 'Outcome'])

    # Initialize lists to store the processed rows
    grouped_data = []

    # Iterate through each unique event
    for _, group in df.groupby(['Commence Time', 'Home Team', 'Away Team', 'Bookmaker', 'Market', 'Time Difference', 'Sport Type', 'Hour Bucket']):
        # Create a dictionary for storing the combined row
        event_data = group.iloc[0][['Commence Time', 'Home Team', 'Away Team', 'Bookmaker', 'Market', 
                                  'Time Difference', 'Sport Type', 'Hour Bucket']].to_dict()

        # Set default odds and point
        event_data['odds1'] = 0
        event_data['odds2'] = 0
        event_data['point'] = None
        event_data['odds1_type'] = ''
        event_data['odds2_type'] = ''

        # Populate the odds fields based on market type
        for _, row in group.iterrows():
            if row['Market'] == 'totals':
                event_data['point'] = row['Point']
                if row['Outcome'] == 'Over':
                    event_data['odds1'] = row['Odds']
                    event_data['odds1_type'] = 'Over'
                elif row['Outcome'] == 'Under':
                    event_data['odds2'] = row['Odds']
                    event_data['odds2_type'] = 'Under'
            
            elif row['Market'] == 'spreads':
                event_data['point'] = abs(row['Point'])
                if row['Point'] > 0:
                    event_data['odds1'] = row['Odds']
                    event_data['odds1_type'] = 'Underdog'
                elif row['Point'] < 0:
                    event_data['odds2'] = row['Odds']
                    event_data['odds2_type'] = 'Favorite'

        # Append the combined row to the list
        grouped_data.append(event_data)

    # Create a new DataFrame from the grouped data
    result_df = pd.DataFrame(grouped_data)

    # Add columns for the probabilities (1/odds)
    result_df['probability1'] = result_df['odds1'].apply(lambda x: 1/x if x > 0 else 0)
    result_df['probability2'] = result_df['odds2'].apply(lambda x: 1/x if x > 0 else 0)

    # Add a column for the total probability sum
    result_df['total_probability'] = result_df['probability1'] + result_df['probability2']

    return result_df

def find_arb_spreads_totals(df):
    df['event_name']=df['Home Team']+'_'+df['Away Team']
    results = []

    # Group by event and market type first
    for (event_time, market, point), group in df.groupby(['Commence Time', 'Market', 'point']):
    # Skip if group has less than 2 rows (need both sides of the bet)
        if len(group) < 2:
            continue
    
        # Create event name from first row's teams
        event_name = f"{group.iloc[0]['Home Team']} vs {group.iloc[0]['Away Team']}"
        
        if market == 'totals':
        # For totals, find minimum probabilities for Over/Under at same point value
            over_rows = group[group['odds1'] > 0]  # Rows with odds1 set (Over)
            under_rows = group[group['odds2'] > 0]  # Rows with odds2 set (Under)
        
            if len(over_rows) > 0 and len(under_rows) > 0:
                min_over_row = over_rows.loc[over_rows['probability1'].idxmin()]
                min_under_row = under_rows.loc[under_rows['probability2'].idxmin()]
            
                odds_sum = min_over_row['probability1'] + min_under_row['probability2']
            
                results.append({
                    'event_name': event_name,
                    'commence_time': event_time,
                    'market': market,
                    'point': point,
                    'odd_1_prob': min_over_row['probability1'],
                    'odd1_type': 'Over',
                    'bookmaker_1': min_over_row['Bookmaker'],
                    'odd_2_prob': min_under_row['probability2'],
                    'odd2_type': 'Under',
                    'bookmaker_2': min_under_row['Bookmaker'],
                    'odds_sum': odds_sum,
                    'arbitrage': 1 if odds_sum < 1 else 0,
                    'Time Difference': min_over_row['Time Difference'],
                    'Sport Type': min_over_row['Sport Type'],
                    'Hour Bucket': min_over_row['Hour Bucket']
                })
            
        elif market == 'spreads':
        # For spreads, find minimum probabilities for underdog/favorite at same point value
            underdog_rows = group[group['odds1'] > 0]  # Rows with odds1 set (Underdog)
            favorite_rows = group[group['odds2'] > 0]  # Rows with odds2 set (Favorite)
        
            if len(underdog_rows) > 0 and len(favorite_rows) > 0:
                min_dog_row = underdog_rows.loc[underdog_rows['probability1'].idxmin()]
                min_fav_row = favorite_rows.loc[favorite_rows['probability2'].idxmin()]
            
                odds_sum = min_dog_row['probability1'] + min_fav_row['probability2']
            
                results.append({
                    'event_name': event_name,
                    'commence_time': event_time,
                    'market': market,
                    'point': abs(point),  # Store positive value for consistency
                    'odd_1_prob': min_dog_row['probability1'],
                    'odd1_type': 'Underdog',
                    'bookmaker_1': min_dog_row['Bookmaker'],
                    'odd_2_prob': min_fav_row['probability2'],
                    'odd2_type': 'Favorite',
                    'bookmaker_2': min_fav_row['Bookmaker'],
                    'odds_sum': odds_sum,
                    'arbitrage': 1 if odds_sum < 1 else 0,
                    'Time Difference': min_dog_row['Time Difference'],
                    'Sport Type': min_dog_row['Sport Type'],
                    'Hour Bucket': min_dog_row['Hour Bucket']
                })

# Convert results to a DataFrame
    final_results_df = pd.DataFrame(results)
    return final_results_df

# Display the result

def fetch_player_props(api_key):
    # Define constants
    REGIONS = 'us'
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

    def get_event_odds(sport, event_id, markets):
        url = f"https://api.the-odds-api.com/v4/sports/{sport}/events/{event_id}/odds"
        params = {
            'apiKey': api_key,
            'regions': REGIONS,
            'markets': markets,
            'dateFormat': 'iso',
            'oddsFormat': 'decimal'
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error for event {event_id}: {response.status_code}")
            print(response.text)
            return None

    all_player_data = []

    for sport, markets in SPORTS_MARKETS.items():
        print(f"\nFetching events for {sport}...")
        events_url = f"https://api.the-odds-api.com/v4/sports/{sport}/events"
        events_response = requests.get(events_url, params={'apiKey': api_key})
        
        if events_response.status_code == 200:
            events = events_response.json()
            for event in events:
                event_id = event['id']
                print(f"Fetching odds for event {event_id}...")
                odds_data = get_event_odds(sport, event_id, markets)
                
                if odds_data:
                    for bookmaker in odds_data.get('bookmakers', []):
                        bookmaker_name = bookmaker['title']
                        
                        for market in bookmaker.get('markets', []):
                            market_name = market['key']
                            last_update = market.get('last_update')
                            for outcome in market.get('outcomes', []):
                                player_name = outcome['description'] if 'description' in outcome else outcome['name']
                                over_under = ''
                                if 'Over' in outcome['name'] or 'Under' in outcome['name']:
                                    over_under = 'Over' if 'Over' in outcome['name'] else 'Under'
                                
                                all_player_data.append({
                                    'Sport': sport,
                                    'Event ID': event_id,
                                    'Home Team': event['home_team'],
                                    'Away Team': event['away_team'],
                                    'Commence Time': event['commence_time'],
                                    'Bookmaker': bookmaker_name,
                                    'Market Type': market_name,
                                    'Player Name': player_name,
                                    'Over/Under': over_under,
                                    'Market Line': outcome.get('point'),
                                    'Odds': outcome['price'],
                                    'Last Update': last_update
                                })

    # Convert to DataFrame
    df = pd.DataFrame(all_player_data)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.expand_frame_repr', False)
    pd.set_option('display.width', 1000)
    print(df)
    return df

def group_player_odds(df):
    #df1 = df1[df1['Market'] != 'h2h_lay']
    df["Commence Time"] = pd.to_datetime(df["Commence Time"])
    df["Last Update"] = pd.to_datetime(df["Last Update"])
# Calculate the difference and remove the days part
    df['Time Difference'] = pd.to_datetime(df['Commence Time']) - pd.to_datetime(df['Last Update'])

# convert to hours
    df['Time Difference (Hours)'] = df['Time Difference'].dt.total_seconds() / 3600
    sport_mapping = {
        'La Liga - Spain': 'Soccer',
        'EPL': 'Soccer',
        'Serie A - Italy': 'Soccer',
        'Ligue 1 - France': 'Soccer',
        'Bundesliga - Germany': 'Soccer',
        'MLS': 'Soccer',
        'NBA': 'Basketball',
        'ATP Paris Masters': 'Tennis',
        'NCAAF': 'College Football',
        'americanfootball_nfl': 'NFL',
        'Test Matches': 'Cricket',
        'One Day Internationals': 'Cricket',
        'International Twenty20': 'Cricket',
        'icehockey_nhl': 'Hockey'
    }

# Map the Sports column to the new Sport Type column
    df['Sport Type'] = df['Sport'].map(sport_mapping)



# Assuming df is your DataFrame and 'Last Update' is in datetime format
    df['Last Update'] = pd.to_datetime(df['Last Update'])  # Convert to datetime if not already

# Extract the hour and convert it to 1-24 format
    df['Hour Bucket'] = df['Last Update'].dt.hour + 1


    # Sort by Last Update to ensure the most recent odds are used
    df = df.sort_values('Last Update', ascending=False)

    # Drop duplicates
    df = df.drop_duplicates(subset=['Commence Time', 'Home Team', 'Away Team', 'Bookmaker', 'Market Type', 'Player Name', 'Over/Under'])

    # Initialize lists to store the processed rows
    grouped_data = []

    # Iterate through each unique event and player
    for _, group in df.groupby(['Commence Time', 'Home Team', 'Away Team', 'Bookmaker', 'Market Type', 'Player Name','Market Line','Sport']):
        # Create a dictionary for storing the combined row
        event_data = {
            'Commence Time': group['Commence Time'].iloc[0],
            'Home Team': group['Home Team'].iloc[0],
            'Away Team': group['Away Team'].iloc[0],
            'Bookmaker': group['Bookmaker'].iloc[0],
            'Market Type': group['Market Type'].iloc[0],
            'Player Name': group['Player Name'].iloc[0],
            'Sport': group['Sport'].iloc[0]
        }

        # Set default odds and point
        event_data['odds1'] = 0
        event_data['odds2'] = 0
        event_data['point'] = None
        event_data['odds1_type'] = ''
        event_data['odds2_type'] = ''

        # Populate the odds fields based on Over/Under
        for _, row in group.iterrows():
            event_data['point'] = row['Market Line']
            if row['Over/Under'] == 'Over':
                event_data['odds1'] = row['Odds']
                event_data['odds1_type'] = 'Over'
            elif row['Over/Under'] == 'Under':
                event_data['odds2'] = row['Odds']
                event_data['odds2_type'] = 'Under'

        # Calculate probabilities
        event_data['probability1'] = 1/event_data['odds1'] if event_data['odds1'] > 0 else 0
        event_data['probability2'] = 1/event_data['odds2'] if event_data['odds2'] > 0 else 0
        event_data['total_probability'] = event_data['probability1'] + event_data['probability2']

        # Append the combined row to the list
        grouped_data.append(event_data)

    # Create a new DataFrame from the grouped data
    result_df = pd.DataFrame(grouped_data)

    return result_df



def find_arb_player(df):
    df['event_name']=df['Home Team']+'_'+df['Away Team']

    results = []

# Group by event, market type, player name, and point
    for (event_time, market_type, point, player_name), group in df.groupby(['Commence Time', 'Market Type', 'point', 'Player Name']):
        if len(group) < 1:
            continue
    
        event_name = f"{group.iloc[0]['Home Team']} vs {group.iloc[0]['Away Team']}"
    
    # Get unique bookmakers for this group
        bookmakers = group['Bookmaker'].unique()
    
    # Compare odds across different bookmakers
        for bk1 in bookmakers:
            for bk2 in bookmakers:
            # Get rows for each bookmaker
                bk1_data = group[group['Bookmaker'] == bk1]
                bk2_data = group[group['Bookmaker'] == bk2]
            
            # Check if both bookmakers have valid data
                if not (bk1_data.empty or bk2_data.empty):
                # Get best over odds from bookmaker 1
                    over_row = bk1_data[bk1_data['odds1_type'] == 'Over'].iloc[0] if not bk1_data[bk1_data['odds1_type'] == 'Over'].empty else None
                # Get best under odds from bookmaker 2
                    under_row = bk2_data[bk2_data['odds2_type'] == 'Under'].iloc[0] if not bk2_data[bk2_data['odds2_type'] == 'Under'].empty else None
                
                    if over_row is not None and under_row is not None:
                        results.append({
                            'event_name': event_name,
                            'commence_time': event_time,
                            'market_type': market_type,
                            'player_name': player_name,
                            'point': point,
                            'odd_1_prob': over_row['probability1'],
                            'odd1_type': 'Over',
                            'bookmaker_1': bk1,
                            'odd_2_prob': under_row['probability2'],
                            'odd2_type': 'Under',
                            'bookmaker_2': bk2,
                            'total_probability': over_row['probability1'] + under_row['probability2'],
                            'arbitrage': 1 if (over_row['probability1'] + under_row['probability2']) < 1 else 0
                        })

# Convert results to a DataFrame and filter out rows with zero probabilities
    final_results_df = pd.DataFrame(results)
    final_results_df = final_results_df[(final_results_df['odd_1_prob'] != 0) & (final_results_df['odd_2_prob'] != 0)]
    return final_results_df


import smtplib
from email.mime.text import MIMEText

def send_arb_email(email_body):
    """
    Sends an email with the provided string as the body to moneyline.rum@gmail.com.
    
    :param email_body: The body content of the email to be sent.
    """
    # Email setup
    recipient_email = "moneyline.rum@gmail.com"  # Fixed recipient email
    sender_email = "moneyline.rum@gmail.com"  # Replace with your email
    sender_password = "gccv zehp osnr oacc"  # Replace with your email's app password

    subject = "Automated Email Notification"  # Subject of the email

    try:
        # Create email message
        msg = MIMEText(email_body)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = recipient_email

        # Send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())

        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")