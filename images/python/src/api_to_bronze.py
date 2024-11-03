from resources.brew_api.brewapi_bronze import BreweryRequestsApi

def brewery_api_to_bronze():
    BreweryRequestsApi().extract_data()


if __name__ == "__main__":
    brewery_api_to_bronze()
