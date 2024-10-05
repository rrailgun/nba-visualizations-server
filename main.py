import nba_api.stats.endpoints.videoeventsasset
from flask import Flask, json, request, abort
from nba_api.stats.static import players
from nba_api.stats.endpoints import *

api = Flask(__name__)

def get_var_from_req(varName):
    val = request.args.get(varName)
    if val == None:
        abort(400, f"No {varName} Provided")
    return val

@api.route('/players')
def get_players():
    return players.get_players()

@api.route('/careerstats')
def get_career_stats():
    PlayerID = get_var_from_req("PlayerID")

    LeagueID = request.args.get("LeagueID")
    if LeagueID == None:
        LeagueID="00"
    data = playercareerstats.PlayerCareerStats(PlayerID, league_id_nullable=LeagueID).get_normalized_json()
    return data

@api.route('/playergamelog')
def get_games():
    PlayerID = get_var_from_req("PlayerID")
    Season = get_var_from_req("Season")

    LeagueID = request.args.get("LeagueID")
    if LeagueID == None:
        NBAData = playergamelog.PlayerGameLog(player_id=PlayerID, season=Season,
                                           league_id_nullable="00").get_normalized_json()
        GLeagueData = playergamelog.PlayerGameLog(player_id=PlayerID, season=Season,
                                           league_id_nullable="20").get_normalized_json()
        NBAData = json.loads(NBAData)
        GLeagueData = json.loads(GLeagueData)
        newData = {"PlayerGameLog": NBAData["PlayerGameLog"]+GLeagueData['PlayerGameLog']}
        return newData

    data = playergamelog.PlayerGameLog(player_id=PlayerID, season=Season, league_id_nullable=LeagueID).get_normalized_json()
    return data

@api.route('/shotchartdetail')
def get_shotchart():
    PlayerID = get_var_from_req("PlayerID")
    Season = get_var_from_req("Season")
    data = shotchartdetail.ShotChartDetail(player_id=PlayerID, team_id=0, season_nullable=Season, context_measure_simple="FGA").get_normalized_json()
    return data

@api.route('/videoevents')
def get_video():
    GameEventID = get_var_from_req("GameEventID")
    GameID = get_var_from_req("GameID")

    data = nba_api.stats.endpoints.videoeventsasset.VideoEventsAsset(game_event_id=GameEventID, game_id=GameID).get_json()
    return data

if __name__ == "__main__":
    api.run()