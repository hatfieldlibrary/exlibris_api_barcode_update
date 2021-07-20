Python modules for updating barcodes using the ExLibris API. 

This is a single purpose project. It was created to update barcodes 
imported during the migration of Pacific Northwest College of Art records into Alma. This code updates PNCA item records
 by padding barcodes with missing zeros.

Although single purpose the code may be useful for jump-starting future projects.

Usage:

Set the path to the data source file in `update_holdings_in_alma.py`.

```
Update PNCA barcodes.

optional arguments:
  -h, --help            show this help message and exit
  -key API Key, --api-key API Key
                        Provide the Exlibris API key
                        
Example: update_holdings_in_alma.py --api-key=xxxxxx

```
