import requests
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo

class UTRScraper:

    def get_user_id(self, name):
        num_results = 1
        try:
            page = requests.get(f'https://app.universaltennis.com/api/v2/search/players?query={name}&top={num_results}')
            data = page.json()
            # extract user id from either 'hits' or 'Hits' because utr has two JSON responses
            key = 'hits' if 'hits' in data else 'Hits'
            return data[key][0]['id'] if key == 'hits' else data[key][0]['Id']
        except (KeyError, IndexError, requests.exceptions.RequestException):
            print(f'Error: Could not find user ID for {name}')
            
    def get_utr(self, name):
        user_id = self.get_user_id(name)
        # get player utr
        url = f'https://app.universaltennis.com/api/v1/player/{user_id}'
        page = requests.get(url)
        data = page.json()
        singles_utr = data['singlesUtr']
        return singles_utr
    
    # Convert UTR scoring into a string
    def get_score_string(self, score):
        sets = []
        for i in range(1, 4):
            if str(i) in score:
                loser_score = score[str(i)]['loser'] if score[str(i)]['loser'] is not None else '0' # account for 0 stored as None in the UTR data
                set_score = f"{score[str(i)]['winner']}-{loser_score}"
                if score[str(i)]['tiebreak'] != None:
                    set_score += f"({score[str(i)]['tiebreak']})"
                sets.append(set_score)
        return ', '.join(sets)
    
    # Convert date into a more readable format
    def convert_date(self, date):
        utc = datetime.fromisoformat(date).replace(tzinfo=ZoneInfo('UTC'))
        pst = utc.astimezone(ZoneInfo('America/Los_Angeles'))
        return pst.strftime('%m/%d/%Y')

    def get_singles_results(self, name):
        user_id = self.get_user_id(name)

        # add ?type=singles for singles only
        url = f'https://app.universaltennis.com/api/v1/player/{user_id}/results?type=singles'
        page = requests.get(url)
        data = page.json()

        results = []
        for event in data['events']:
            event_name = event['name']

            if len(event['draws']) == 0:
                for result in event['results']:
                    date = self.convert_date(result['date'])
                    player1 = result['players']['winner1']['firstName'] + ' ' + result['players']['winner1']['lastName']
                    player2 = result['players']['loser1']['firstName'] + ' ' + result['players']['loser1']['lastName']
                    player1_singles_utr = result['players']['winner1']['singlesUtr']
                    player2_singles_utr = result['players']['loser1']['singlesUtr']
                    score = self.get_score_string(result['score'])
                    results.append([event_name, date, player1, player1_singles_utr, player2, player2_singles_utr, score])
            else:
                for result in event['draws'][0]['results']:
                    date = result['date']
                    player1 = result['players']['winner1']['firstName'] + ' ' + result['players']['winner1']['lastName']
                    player2 = result['players']['loser1']['firstName'] + ' ' + result['players']['loser1']['lastName']
                    player1_singles_utr = result['players']['winner1']['singlesUtr']
                    player2_singles_utr = result['players']['loser1']['singlesUtr']
                    score = self.get_score_string(result['score'])
                    results.append([event_name, date, player1, player1_singles_utr, player2, player2_singles_utr, score])

        singles_results = pd.DataFrame(results, columns=['Event Name', 'Date', 'Player1', 'Player1 UTR', 'Player2', 'Player2 UTR', 'Score'])
        return singles_results
    
    def get_doubles_results(self):
        # later?
        return


if __name__ == "__main__":

    # testing code
    scraper = UTRScraper()

    print(scraper.get_user_id("Spencer Johnson"))
    print(scraper.get_utr("Spencer Johnson"))
    print(scraper.get_singles_results("Spencer Johnson"))


# to use in other files, import the class and create an instance
# from match_scraper import UTRScraper
# scraper = UTRScraper()
# scraper.get_singles_results("Spencer Johnson")

