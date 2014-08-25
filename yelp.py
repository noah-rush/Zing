import rauth
import time
 
def main(lat,lng):
    location = (lat,lng)
    api_calls = []
    params = get_search_parameters(lat,lng)
    api_calls.append(get_results(params))
    #Be a good internet citizen and rate-limit yourself
    time.sleep(1.0)
        
    return api_calls 
 
def get_results(params):
 
    #Obtain these from Yelp's manage access page
    consumer_key = "YOUR_KEY"
    consumer_secret = "YOUR_SECRET"
    token = "YOUR_TOKEN"
    token_secret = "YOUR_TOKEN_SECRET"
    
    session = rauth.OAuth1Session(
        consumer_key = 'oOHX4VgbaRnLk3cvhf2yyA'
        ,consumer_secret = 'PMk3huIc9R_t9Q08NCa7iu4auRU'
        ,access_token = '0uSylZkh9ViZ3rSfg9l3lvtniZGK6ciP'
        ,access_token_secret = 'LDxXwESUV8KTW8u8TSB4WH25UUs')
        
    request = session.get("http://api.yelp.com/v2/search",params=params)
    
    #Transforms the JSON API response into a Python dictionary
    data = request.json()
    session.close()
    
    return data
        
def get_search_parameters(lat,long):
    #See the Yelp API for more details
    params = {}
    params["term"] = "lunch"
    params["ll"] = "{},{}".format(str(lat),str(long))
    params["radius_filter"] = "2000"
    params["limit"] = "10"
 
    return params
 
if __name__=="__main__":
    main()