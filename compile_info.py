import httpx
import json


class catalog_data:
    def __init__(self, json_data) -> None:
        self._json_data = json_data
        self.id = self._json_data['id']
        self._holdings_1display = json.loads(json_data['holdings_1display'])
        # The Google Books barcode is buried in the holdings_1display
        # object. This object has only one property, a mysterious
        # number, so we use a hack to get it: just use the first and
        # only key.
        
        key = list(self._holdings_1display.keys())[0]
        self.barcode = self._holdings_1display[key]['items'][0]['barcode']
         
   
        self._electronic_portfolio_s = json.loads(json_data['electronic_portfolio_s'][0])

    @property
    def url(self):
        url = None
        # another horrible piece of json
        electronic_portfolio_s = json_data.get('electronic_portfolio_s')
        if electronic_portfolio_s:
            ep_data = json.loads(electronic_portfolio_s[0])
            if ep_data['title'] == 'Online Content':
                url = ep_data['url']
        return url
        


url = "https://catalog.princeton.edu/catalog/9914374433506421/raw"

resp = httpx.get(url)

json_data = resp.json()
