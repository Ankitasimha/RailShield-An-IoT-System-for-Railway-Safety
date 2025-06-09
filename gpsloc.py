import requests


def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]

def get_loc():
    ip_address = get_ip()
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    lat=response.get("latitude")
    lon=response.get("longitude")
    loc=str(lat)+","+str(lon)
    
    return loc
print(get_loc())