from api.hiRezApi import HiRezAPI


class SmiteAPI(HiRezAPI):

    def __init__(self, endpoint):

        super().__init__(endpoint)


    def get_demo_details(self, match_id=None):
        
        return self.request(self.create_url('getdemodetails', match_id))
    

    def get_esports_pro_league_details(self):

        return self.request(self.create_url('getesportsproleaguedetails'))
        

    def get_god_ranks(self, player=None):

        return self.request(self.create_url('getgodranks', player))
    

    def get_gods(self):

        return self.request(self.create_url('getgods', 1))
    

    def get_god_leaderboard(self, god_id, queue):

        return self.request(self.create_url('getgodleaderboard', god_id, queue))
    

    def get_god_skins(self, god_id):

        return self.request(self.create_url('getgodskins', god_id, 1))
    

    def get_god_recommended_items(self, god_id):

        return self.request(self.create_url('getgodrecommendeditems', god_id, 1))
    

    def get_items(self):

        return self.request(self.create_url('getitems', 1))
    

    def get_match_details(self, match_id):

        return self.request(self.create_url('getmatchdetails', match_id))
    

    def get_match_details_batch(self, match_ids):

        if match_ids > 10:

            return None

        str_match_ids = ','.join([str(id) for id in match_ids])

        return self.request(self.create_url('getmatchdetails', str_match_ids))
    

    def get_league_leaderboard(self, queue, tier, season):
        
        return self.request(self.create_url('getleagueleaderboard', queue, tier, season))
    

    def get_match_history(self, player_id):

        return self.request(self.create_url('getmatchhistory', player_id))
    

    def get_motd(self):

        return self.request(self.create_url('getmotd'))


    def get_player(self, player=None):

        return self.request(self.create_url('getplayer', player))
    

    def get_player_status(self, player_id):

        return self.request(self.create_url('getplayerstatus', player_id))
    

    def get_queue_stats(self, player_id, queue):

        return self.request(self.create_url('getqueuestats', player_id, queue))
    

    def get_top_matches(self):

        return self.request(self.create_url('gettopmatches'))
    

    def get_player_achievments(self, player_id):

        return self.request(self.create_url('getplayerachievements', player_id))
    

    def get_patch_info(self):

        return self.request(self.create_url('getpatchinfo'))


class PcSmiteAPI(SmiteAPI):

    def __init__(self):

        super().__init__("https://api.smitegame.com/smiteapi.svc/")


    def get_friends(self, player):

        return self.request(self.create_url('getfriends', player))


class XboxSmiteAPI(SmiteAPI):

    def __init__(self):

        super().__init__("https://api.xbox.smitegame.com/smiteapi.svc/")


class Ps4SmiteAPI(SmiteAPI):

    def __init__(self):

        super().__init__("https://api.ps4.smitegame.com/smiteapi.svc/")
