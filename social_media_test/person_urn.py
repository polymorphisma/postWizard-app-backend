import requests

# Replace with your actual LinkedIn API access token
access_token = 'AQWVOikh7iq93J9pkUlQ3JLydk9gpLClCw9vbcHFQuT0Xf7a2DqNdkO7ypyekqzgAE1fSGR_vnyp3AYZs3B3ZuDnCzDy_OiuiPZk9hr36SuvBfg9OsRCka6Fs5R_zS8W-KVy_L0jJp9cOEXOgnzwtaEpxqRH7NDNuITHwNNnOI83H_frLffkoUTr3VMZe5yxjL448NmtWuFkM6tonBAGaqWPgMwTTkr_QoZQn_vpu7OlctiEhkfNC1JgPxcoufOrbpZmZvNdzIDctsxLZSSnRULzvHkN831pLiBOhcK2bdEXsbCoZJE_10ZJIOdF27yfEVBhyAg6-ct_cZTfWD6Amxp5qoWbUA'


# LinkedIn API endpoint to get profile information
profile_url = 'https://api.linkedin.com/v2/userinfo'

# Headers for the request
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

# Make the GET request to LinkedIn API
response = requests.get(profile_url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    profile_info = response.json()
    print(profile_info)
    person_urn = profile_info.get('id')  # This is your LinkedIn person URN
    print('Person URN:', f'urn:li:person:{person_urn}')
else:
    print('Failed to get profile information:', response.status_code, response.text)

[{'url': 'https://www.linkedin.com/feed/update/urn:li:share:7207240606161510400', 'success': True, 'method': 'linkedin'}, {'success': True, 'message': 'https://twitter.com/user/status/1801474943873651163', 'method': 'twitter'}]