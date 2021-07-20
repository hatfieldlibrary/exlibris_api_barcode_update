import urllib.request

from modules.xml_parsers import Parser


class AlmaRequest:

    # Exlibris API base path.
    path = 'https://api-na.hosted.exlibrisgroup.com'

    # Provides methods for processing xml responses.
    xml_parser = Parser()

    def __init__(self, api_key):
        # The Exlibris API key is provided as command line argument.
        self.api_key = '?apikey=' + api_key

    # Note that these methods throw error on http response error codes.
    # But testing for threshold limit, just in case the API doesn't return an error code.

    def get_holdings_records(self, alma_id):
        url = self.__api_get_holdings_path(alma_id)
        with urllib.request.urlopen(url) as response:
            xml = response.read()
            if not self.xml_parser.error_test(xml):
                return xml
            else:
                raise ValueError('Error retrieving holdings. Possible limit.')

    def get_holdings_ids(self, record):
        return self.xml_parser.get_holdings_ids(record)

    def get_holding_items(self, alma_id, holding_id):
        url = self.__api_get_holding_items_path(alma_id, holding_id)
        with urllib.request.urlopen(url) as response:
            xml = response.read()
            if not self.xml_parser.error_test(xml):
                return xml
            else:
                raise ValueError('Error retrieving holdings items. Possible limit.')

    def get_holding_single_item(self, alma_id, holding_id, item_pid):
        url = self.__api_get_holding_single_item_path(alma_id, holding_id, item_pid)
        with urllib.request.urlopen(url) as response:
            xml = response.read()
            if not self.xml_parser.error_test(xml):
                return xml
            else:
                raise ValueError('Error retrieving item. Possible limit.')

    def set_holdings(self, alma_id, holdings_id, item_pid, payload):
        url = self.__api_get_holding_single_item_path(alma_id, holdings_id, item_pid)
        # Print this feedback to console.
        print('Updating: ' + url)
        req = urllib.request.Request(url, payload, method='PUT')
        req.add_header('Content-Type', 'application/xml')
        with urllib.request.urlopen(req) as f:
            pass
        print(alma_id + ' - update response code: ' + f.status)

    def __api_get_holdings_path(self, alma_id):
        return self.path + '/almaws/v1/bibs/' + alma_id + '/holdings' + self.api_key

    def __api_get_holding_items_path(self, alma_id, holding_id):
        return self.path + '/almaws/v1/bibs/' + alma_id + '/holdings/' + holding_id + '/items' + self.api_key

    def __api_get_holding_single_item_path(self, alma_id, holding_id, item_pid):
        return self.path + '/almaws/v1/bibs/' + alma_id + '/holdings/' + holding_id \
               + '/items/' + item_pid + self.api_key

