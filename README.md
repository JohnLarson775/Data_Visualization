# Sportsball 2018 - Visualizing a Fantasy Football Season
## by John Larson


## Dataset

> Two dataframes were created through ESPN's accessible fantasy football API. [Steven Morse](https://stmorse.github.io/), an instructor in the Department of Mathematics at the U.S. Military Academy, posted a couple articles containing instructions and code that were instrumental in helping me efficienctly create [seasonscores](https://stmorse.github.io/journal/espn-fantasy-python.html) and [boxscores](https://stmorse.github.io/journal/espn-fantasy-2-python.html) csv files using ESPN's API. The script that creates these files is included in this project submittal as `espn_api_to_csv.py`. Steven's articles also inspired me to make boxplots and radial charts to visualize data for my league.
>
> After creating the csvs, team names were manually changed in Excel to generic "Team 1", "Team 2", etc.
>
> `seasonscores` is 156 rows x 5 columns. The columns contain the following information:
> 
>  - `Week` = Ranges from 1 to 13, describing the week of a given matchup.
>  - `Team` = Team name.
>  - `Id` = Unique identifier for each team. Managers can change team name throughout the season, but `Id` stays constant.
>  - `Score` = Fantasy team score for a given week.
>  - `Type` = Describing the type of matchup. These are all "Regular" for weeks 1-13. "Playoff" would be the other type of matchup that could be explored in a different project.
>
> `boxscores` is 2496 rows x 9 columns. The columns contain the following information:
> 
>  - `playerName` = Football player's name.
>  - `matchupPeriodId` = Equivalent to `Week` in `seasonscores`.
>  - `slotId` = Defines the position in a team's lineup.
>  - `position` = Football player's position.
>  - `bye` = Identifies if the football player has a "bye" on given `matchupPeriodId`.
>  - `appliedStatTotal` = Football player's fantasy score for given `matchupPeriodId`.
>  - `teamName` = Equivalent to `Team` in `seasonscores`.
>  - `wonMatchup` = Describes whether of not `teamName` won their matchup for given `matchupPeriodId`.
>  - `W/L` = Based off boolean value from `wonMatchup`.

## Summary of Findings

> Univariate Exploration
>
> James Conner lead my team (Team 4) to a championship this year, with 210 fantasy points over 13 weeks. Other notable contributors were my quarterback committee of Rodgers and Ryan, my top wide receiver Stefon Diggs, and a surprisingly successful George Kittle. With a clear visualization of my top performers, I'm curious as to how my team as a whole stacked up to other teams in the league.
>
> Bivariate Exploration
>
> This was a comparison of a categorical data type (Team) vs. a qualitative data type (Score).
>
> Scores for the season were all over the map, ranging from Team 2 putting up a measly 60 points in week 8, to Team 5 posting 169 points in Week 4. There doesn't seem to be a relationship between variance of scores and magnitude of scores. In other words, a team's scoring consistency is not correlated to the team's success in term of how many points they score on average.
>
> My team (Team 4) ranks 4th in average score. One thing I remember about my fantasy season that's easily seen in this boxplot is my three weeks in a row of scoring 121 points. Sharing this chart with leaguemates would be a helpful way for them to understand their team's scoring consistency and how they stack up amongst the competition.
>
> Another tool that could be helpful for league managers would be looking at positional score relative to each other. This would allow managers to see positional strengths and weaknesses and average score differences between wins and losses.
>
> Mulitvariate Exploration
>
> Each purple trace shows an individual week. The black line shows the average positional score.
>
> On average, in matchups that I won, my QB scored 20.1, RBs averaged 16.7, WRs averaged 12.8, TE scored 10.2, and D/ST scored 7.8.
>
> There's a smaller sample size in the losses radial chart, which makes sense considering I only lost three matchups this season. On average, in matchups that I lost, my QB scored 20.8, RBs averaged 10.5, WRs averaged 9.7, TE scored 14.2, and D/ST scored 3.3.
>
> The biggest difference in positional scoring between wins and losses is at the RB position (6.2). This means I probably lost matchups due mostly to lackluster RB performance. Even though QBs generally score the most on fantasy teams, these visualizations are evidence that solid performances out of other postions is actually more vital to winning matchups.

## Key Insights for Presentation

> All of the visualizations created in the exploratory phase important to add to the presentation. A more thorough exploration of this fantasy data can be found on a [dashboard](https://sportsball-2018-dashboard.herokuapp.com/) I created.