import xml.etree.ElementTree as ET


class Parser:

    @staticmethod
    def get_holdings_ids(record):
        root = ET.fromstring(record)
        holdings = root.findall('./holding')
        holdings_list = []
        for holding in holdings:
            # Only process PNCA holdings.
            library = holding.find('./library')
            if library is not None:
                if library.text == 'PNCA':
                    holding_id = holding.find('holding_id')
                    holdings_list.append(holding_id)
        return holdings_list

    @staticmethod
    def get_holding_items(holdings_response):
        root = ET.fromstring(holdings_response)
        return root.findall('./item')

    @staticmethod
    def get_item_pid(holdings_response):
        root = ET.fromstring(holdings_response)
        root.find()

    @staticmethod
    def get_barcodes(item):
        item_data = item.find('./item_data')
        barcode = item_data.find('./barcode')
        return barcode.text

    @staticmethod
    def get_item_pid(item):
        item_data = item.find('./item_data')
        pid = item_data.find('./pid')
        return pid.text

    @staticmethod
    def xml_tree_to_string(element):
        xml_string = ET.tostring(element, encoding='unicode')
        return xml_string.encode('utf-8')

    @staticmethod
    def error_test(xml):
        root = ET.fromstring(xml)
        error = root.find('./errorsExist')
        if error is not None:
            if error.text == 'true':
                return True
            else:
                return False
        return False
