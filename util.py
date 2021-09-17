import pandas as pd
from sodapy import Socrata

def get_data(domain, dataset_identifier, limit=50_000):
    """
    Get Socrata dataset as pandas DataFrame
    
    Parameters
    ----------
    domain: string url i.e. data.texas.gov, data.cdc.gov
    
    dataset_identifier: string identifying specific dataset
        example: "unsk-b7fc" - US vaccinations by state
        
    Notes
    -----
    If you wish to run often, create an account with 
        username, password, and get an API token
    """
    # Unauthenticated client only works with public data sets. Note 'None'
    # in place of application token, and no username or password:
    client = Socrata(domain, None)


    # Example authenticated client (needed for non-public datasets):
    # client = Socrata(data.kingcounty.gov,
    #                  MyAppToken,
    #                  userame="user@example.com",
    #                  password="AFakePassword")

    # First 50,000 results, returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.
    results = client.get(dataset_identifier, limit=limit)

    # Convert to pandas DataFrame
    df = pd.DataFrame.from_records(results)
    return df