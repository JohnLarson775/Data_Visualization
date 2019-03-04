# Pull from ESPN API, pickle boxscores info, save season scores and box scores to csv files
# The dataframes in this code were formed using Steven Morse's code from his page:
# https://stmorse.github.io/journal/espn-fantasy-python.html

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

# Lines 21 thru 62: Season Scores - Team scores by week
# Lines 67 thru 168: Box Scores - Player scores by team and week

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

# Perform imports
import pandas as pd
import numpy as np

# Import to pull from ESPN API:
import requests

# Pull season scores
scores = {}
for week in range(1,14):
    r = requests.get('http://games.espn.com/ffl/api/v2/scoreboard',
        params={'leagueId':904062, 'seasonId': 2018, 'matchupPeriodId': week})
    scores[week] = r.json()

# Populate df with scoring information
df = []
# Find matchup data for a given week
for key in scores:
    temp = scores[key]['scoreboard']['matchups']
    # Find scoring data for a given matchup
    for match in temp:
        df.append([key,
            # Find both team names (location + nickname)
            match['teams'][0]['team']['teamLocation'] + ' ' + match['teams'][0]['team']['teamNickname'],
            match['teams'][1]['team']['teamLocation'] + ' ' + match['teams'][1]['team']['teamNickname'],
            # Find both team IDs
            match['teams'][0]['team']['teamId'],
            match['teams'][1]['team']['teamId'],
            # Find both scores
            match['teams'][0]['score'],
            match['teams'][1]['score']])
        
# df of IDs, scores, and weeks
df = pd.DataFrame(df, columns=['Week','HomeTeam','AwayTeam','HomeId','AwayId','HomeScore','AwayScore'])

# Omit home-away distinction and make a df of team weekly scores
df = (df[['Week', 'HomeTeam', 'HomeId', 'HomeScore']]
    .rename(columns = {'HomeTeam':'Team', 'HomeId':'Id', 'HomeScore':'Score'})
    .append(df[['Week', 'AwayTeam', 'AwayId', 'AwayScore']]
    .rename(columns = {'AwayTeam':'Team', 'AwayId':'Id', 'AwayScore':'Score'})))

# Distinguish between regular season and playoffs
df['Type'] = pd.Series(['Regular' if w <= 14 else 'Playoff' for w in df['Week']])

# Round score to tenths place
df['Score'] = round(df['Score'],1)

# Save dataframe to csv
df.to_csv('seasonscores.csv', index = False)

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

# Loop through each week and each matchup with a request to boxscore each time
# and save the results in a big dict that we can pickle for later:
leagueId, seasonId = 904062, 2018

sbs = {}
bss = {}

print('Week', end=' ')
for week in range(1,14):
    print(week, end=' .. ')
    
    sb = requests.get('http://games.espn.com/ffl/api/v2/scoreboard', 
        params={'leagueId': leagueId, 'seasonId': seasonId, 'matchupPeriodId': week})
    sb = sb.json()
    sbs[week] = sb
    bss[week] = {}
    
    # loop through matchups that week
    for match in range(len(sb['scoreboard']['matchups'])):
        homeId = sb['scoreboard']['matchups'][match]['teams'][0]['team']['teamId']
        
        r = requests.get('http://games.espn.com/ffl/api/v2/boxscore', 
            params={'leagueId': leagueId, 'seasonId': seasonId, 
                    'teamId': homeId, 'matchupPeriodId': week},
                    #cookies={'SWID': swid, 'espn_s2': espn}
        )
        r = r.json()
        bss[week][match] = r

# Import pickle for serialization: http://www.diveintopython3.net/serializing.html
import pickle

print('\nSaving to pickle..')
pickle.dump(sbs, open('homie_2018_sbs.pkl', 'wb'))
pickle.dump(bss, open('homie_2018_bss.pkl', 'wb'))
print('Complete.')

# Pluck out some basic stats per player, per week, 
# and record whose fantasy team they were playing for.

# Positional slots
slots = {0: 'QB', 2: 'RB', 4: 'WR', 6: 'TE', 16: 'D/ST', 20: 'BE', 23: 'FLEX'}

# Rows will be by player by week
df1 = pd.DataFrame(
    columns=['playerName', 'matchupPeriodId', 'slotId', 'position', 
             'bye', 'appliedStatTotal', 'teamName', 'wonMatchup'])

for week in range(1,14):
    for match in range(len(sbs[week]['scoreboard']['matchups'])):
        homeId = sbs[week]['scoreboard']['matchups'][match]['teams'][0]['team']['teamId']
        winner = sbs[week]['scoreboard']['matchups'][match]['winner']

        # loop through home (0) and away (1)
        for team in range(2):
            # boolean for who won this matchup
            winb = False
            if (winner=='away' and team==1) or (winner=='home' and team==0):
                winb = True

            # fantasy team info (dict)
            tinfo = bss[week][match]['boxscore']['teams'][team]['team']

            # all players on that team info (array of dicts)
            ps = bss[week][match]['boxscore']['teams'][team]['slots']

            # loop through players
            for k,p in enumerate(ps):
                # players on bye/injured won't have this entry
                try:
                    pts = p['currentPeriodRealStats']['appliedStatTotal']
                except KeyError:
                    pts = 0

                # there is some messiness in the json so just skip
                try:
                    # get player's position. this is a bit hacky...
                    pos = p['player']['eligibleSlotCategoryIds']
                    for s in [20, 23]:
                        if pos.count(s) > 0:
                            pos.remove(s)
                    pos = slots[pos[0]]

                    # add it all to the DataFrame
                    df1 = df1.append({
                        'playerName': p['player']['firstName'] + ' ' + p['player']['lastName'],
                        'matchupPeriodId': week,
                        'slotId': p['slotCategoryId'],
                        'position': pos,
                        'bye': True if p['opponentProTeamId']==-1 else False,
                        'appliedStatTotal': pts,
                        'teamName': tinfo['teamLocation'] + ' ' + tinfo['teamNickname'],
                        'wonMatchup': winb},
                            ignore_index=True)
                except KeyError:
                    continue

# Convert boolean values to W/L column
df1['W/L'] = np.where(df1.eval('wonMatchup == True'), 'W', 'L')

# Save dataframe to csv
df1.to_csv('boxscores.csv', index = False)