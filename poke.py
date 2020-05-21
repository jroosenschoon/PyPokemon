import requests


def get_pokemons(offset=0):
    url = "http://pokeapi.co/api/v2/pokemon-form/"

    response = requests.get(url)

    if response.status_code == 200:
        payload = response.json()

        count = payload['count']
        print(count)
        response = requests.get(url, params={'limit': count})

        if response.status_code == 200:
            payload = response.json()

            results = payload['results']

            for r in results:
                print(r['name'], ",", r['url'])


def get_poke_info(poke_name="", poke_id = -1):
    if poke_name == "" and poke_id == -1:
        print("Error. Please enter a pokemon name or id.")
        return
    if poke_name != "":
        poke_name = poke_name.lower()
        response = requests.get("https://pokeapi.co/api/v2/pokemon/" + poke_name)

        if response.status_code == 200:
            payload = response.json()
            print(payload)
        else:
            print("Error " + str(response.status_code) + ". Pokemon not found.")


def get_poke_image(name):
    url = "https://pokeapi.co/api/v2/pokemon/" + name

    response=requests.get(url)

    if response.status_code == 200:
        payload = response.json()

        return payload['sprites']['front_default']



# get_pokemons()
# get_poke_info("Sadslash")
# get_poke_image("sandshrew")
