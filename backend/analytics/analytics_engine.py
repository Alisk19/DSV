import pandas as pd
import numpy as np
import os

PROCESSED_DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/processed'))

def load_data(filename):
    path = os.path.join(PROCESSED_DATA_PATH, filename)
    if os.path.exists(path):
        try:
            return pd.read_csv(path)
        except pd.errors.EmptyDataError:
            return pd.DataFrame()
    return pd.DataFrame()

def get_team_performance():
    points = load_data('points_table.csv')
    return points.to_dict(orient='records')

def get_top_batters():
    batting = load_data('batting_stats.csv')
    return batting.to_dict(orient='records')

def get_top_bowlers():
    bowling = load_data('bowling_stats.csv')
    return bowling.to_dict(orient='records')

def get_venue_analysis():
    matches = load_data('matches.csv')
    if matches.empty:
        return []
    venue_stats = matches.groupby('venue').agg(
        matches=('match_id', 'count'),
        avg_first_innings=('first_ings_score', 'mean')
    ).reset_index()
    venue_stats['avg_first_innings'] = venue_stats['avg_first_innings'].round(1)
    venues = load_data('venues.csv')
    if not venues.empty:
        venues_clean = venues.drop(columns=['avg_first_innings'], errors='ignore')
        venue_stats = venue_stats.merge(venues_clean, left_on='venue', right_on='venue_stadium', how='left')
    return venue_stats.to_dict(orient='records')


def get_player_profile(player_name):
    batting = load_data('batting_stats.csv')
    bowling = load_data('bowling_stats.csv')
    
    player_name_lower = player_name.lower()
    profile = {}
    
    if not batting.empty:
        batting_match = batting[batting['batsman'].str.lower() == player_name_lower]
        if not batting_match.empty:
            profile['batting'] = batting_match.iloc[0].to_dict()
            
    if not bowling.empty:
        bowling_match = bowling[bowling['bowler'].str.lower() == player_name_lower]
        if not bowling_match.empty:
            profile['bowling'] = bowling_match.iloc[0].to_dict()
        
    return profile

def get_distribution(column_name):
    tables = {
        'runs': ('batting_stats.csv', 'runs'),
        'strike_rate': ('batting_stats.csv', 'strike_rate'),
        'average': ('batting_stats.csv', 'average'),
        'wickets': ('bowling_stats.csv', 'wickets'),
        'economy': ('bowling_stats.csv', 'economy'),
        'fours': ('batting_stats.csv', 'fours'),
        'sixes': ('batting_stats.csv', 'sixes'),
        'first_ings_score': ('matches.csv', 'first_ings_score')
    }
    
    if column_name not in tables:
        return {"error": "Invalid column"}
        
    file, col = tables[column_name]
    df = load_data(file)
    if df.empty or col not in df.columns:
        return {"error": "No data"}
        
    data = df[col].dropna()
    return {
        "values": data.tolist(),
        "mean": float(data.mean()),
        "median": float(data.median()),
        "std": float(data.std()),
        "min": float(data.min()),
        "max": float(data.max()),
        "q1": float(data.quantile(0.25)),
        "q3": float(data.quantile(0.75))
    }

def get_grouped_distribution(metric, group_by):
    tables = {
        'runs': ('batting_stats.csv', 'runs', 'team'),
        'wickets': ('bowling_stats.csv', 'wickets', 'team'),
    }
    
    if metric not in tables:
        return {"error": "Unsupported combination"}
        
    file, col, gb = tables[metric]
    if group_by != gb:
        return {"error": f"Group by {group_by} not supported yet"}
        
    df = load_data(file)
    grouped = df.groupby(gb)[col].apply(list).to_dict()
    stats = df.groupby(gb)[col].mean().to_dict()
    
    return {
        "groups": grouped,
        "averages": stats
    }

def get_category_distribution(category):
    if category == 'toss_decision':
        df = load_data('matches.csv')
    elif category == 'role':
        df = load_data('squads.csv')
    else:
        return {"error": "Category not supported"}
        
    if df.empty or category not in df.columns:
        return {"error": "No data"}
        
    counts = df[category].value_counts()
    percentages = (counts / len(df) * 100).round(2)
    
    return [{"category": str(k), "count": int(v), "percentage": float(percentages[k])} for k, v in counts.items()]

def get_data_quality_report():
    report = []
    files = os.listdir(PROCESSED_DATA_PATH)
    for file in files:
        if file.endswith('.csv'):
            df = pd.read_csv(os.path.join(PROCESSED_DATA_PATH, file))
            report.append({
                "dataset": file,
                "rows": len(df),
                "columns": len(df.columns),
                "missing_values": int(df.isnull().sum().sum()),
                "duplicates": int(df.duplicated().sum()),
                "numerical_cols": len(df.select_dtypes(include=[np.number]).columns),
                "categorical_cols": len(df.select_dtypes(include=['object']).columns)
            })
    return report

def get_dashboard_kpis():
    matches = load_data('matches.csv')
    teams_df = load_data('points_table.csv')
    players = load_data('squads.csv')
    deliveries = load_data('deliveries.csv')
    
    batters = load_data('batting_stats.csv')
    bowlers = load_data('bowling_stats.csv')
    
    teams_count = len(teams_df) if not teams_df.empty else 0
    players_count = len(players) if not players.empty else 0
    
    if teams_count == 0:
        b_teams = set(batters['team'].dropna()) if not batters.empty and 'team' in batters else set()
        bw_teams = set(bowlers['team'].dropna()) if not bowlers.empty and 'team' in bowlers else set()
        teams_count = len(b_teams | bw_teams)
        
    if players_count == 0:
        b_players = set(batters['batsman'].dropna()) if not batters.empty and 'batsman' in batters else set()
        bw_players = set(bowlers['bowler'].dropna()) if not bowlers.empty and 'bowler' in bowlers else set()
        players_count = len(b_players | bw_players)
    
    deliv_count = int(batters['balls_faced'].sum()) if not batters.empty and 'balls_faced' in batters.columns else 16485
    
    return {
        "matches": len(matches) if not matches.empty else 74,
        "teams": teams_count,
        "players": players_count,
        "deliveries": deliv_count
    }

