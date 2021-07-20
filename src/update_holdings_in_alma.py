import csv

from src.alma_api import AlmaRequest
from src.xml_parsers import Parser
from src.barcode_util import pad_barcodes
import argparse

xml_parser = Parser()

# Manually define path to the data file here.
data_path = '../data/multiple_holding_test.tsv'
# data_path = '../data/pnca_holdings_results.tsv'

parser = argparse.ArgumentParser(description='Update PNCA barcodes.')

parser.add_argument('-key', '--api-key', metavar='API Key', type=str,
                    help='Provide the Exlibris API key')

args = parser.parse_args()

with open(data_path, 'r') as alma_file:
    alma_reader = csv.reader(alma_file, delimiter="\t")

    alma = AlmaRequest(args.api_key)

    next(alma_reader)

    record_count = 0
    holdings_count = 0
    update_count = 0

    print('Processing: ' + data_path)

    for line in alma_reader:
        record_count += 1
        alma_id = line[21]
        record = alma.get_holdings_records(alma_id)
        holding_ids = alma.get_holdings_ids(record)
        for holding_id in holding_ids:
            holdings_count += 1
            holdings_response = alma.get_holding_items(alma_id, holding_id.text)
            # Get items for PNCA library
            items = xml_parser.get_holding_items(holdings_response)
            for item in items:
                barcode = xml_parser.get_barcodes(item)
                # Update PNCA item if barcode length less than 9
                if barcode is not None and len(barcode) < 9:
                    barcode = pad_barcodes(barcode)
                    item.find('./item_data/barcode').text = barcode
                    item_pid = xml_parser.get_item_pid(item)
                    alma.set_holdings(alma_id, holding_id.text, item_pid, xml_parser.xml_tree_to_string(item))
                    update_count += 1

    print('Records processed: ' + str(record_count))
    print('PNCA holdings processed: ' + str(holdings_count))
    print('Item records updated: ' + str(update_count))
