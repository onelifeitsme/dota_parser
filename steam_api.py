import requests

TOKEN = '3026AC4D563D119B5D945F2624A36D53'


class Player:

    def __init__(self, steam_id):
        self.steam_id = steam_id

    def get_match_info(self, match_id):
        url = f'https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?key={TOKEN}&match_id={match_id}'
        response = requests.get(url)
        return response

    def get_player_info(self, steam_id):
        url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={TOKEN}&steamids={steam_id}"
        response = requests.get(url)
        player_data = response.json()
        return player_data["response"]["players"][0]


    def get_match_history(self, num_matches=100, start_match_id=None):
        url = f"https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?key={TOKEN}&account_id={self.steam_id}&matches_requested={num_matches}"
        if start_match_id:
            url += f"&start_at_match_id={start_match_id}"
        response = requests.get(url)
        match_history = response.json()
        return match_history["result"]["matches"]

    def get_all_matches(self):
        a = int(2000/100)
        self.all_matches = []
        for i in range(a):
            if not hasattr(self, 'last_match_id'):
                matches = self.get_match_history()
            else:
                matches = self.get_match_history(start_match_id=self.last_match_id)
            self.last_match_id = matches[-1]["match_id"]
            self.all_matches.extend(matches)
            if not hasattr(self, 'last_match_id'):
                self.all_matches.extend(matches)
            else:
                self.all_matches.extend(matches[:-1])
        return self.all_matches


player = Player(steam_id='76561198081994070')
player.get_all_matches()
...


