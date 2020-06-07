import requests
import pprint


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
    pp = pprint.PrettyPrinter()

    poke_info = {}
    if poke_name == "" and poke_id == -1:
        print("Error. Please enter a pokemon name or id.")
        return
    if poke_name != "":
        poke_name = poke_name.lower()
        response = requests.get("https://pokeapi.co/api/v2/pokemon/" + poke_name)

        if response.status_code == 200:
            payload = response.json()
            for k, v in payload.items():
                print(k)
            pp.pprint(payload['abilities'])
            poke_info['weight']   = payload['weight']
            poke_info['height']   = payload['height']
            poke_info['hp']       = payload['stats'][-1]['base_stat']
            poke_info['attack']   = payload['stats'][-2]['base_stat']
            poke_info['defense']  = payload['stats'][-3]['base_stat']

            poke_info['types']    = []
            for t in payload['types']:
                poke_info['types'].append(t['type']['name'])

            des = ""
            for a in payload['abilities']:
                if response.status_code == 200:
                    payload = response.json()

                    des = payload['effect_entries'][1]

                poke_info['ability'] = {'name': a['ability']['name'], 'descr': des}
                response = requests.get(a['ability']['url'])

            poke_info['id'] = payload['id']


        else:
            print("Error " + str(response.status_code) + ". Pokemon not found.")

        return poke_info

def get_poke_image(name):
    name = name.lower()
    url = "https://pokeapi.co/api/v2/pokemon/" + name

    response=requests.get(url)

    if response.status_code == 200:
        payload = response.json()

        return payload['sprites']['front_default']
    else:
        return -1


# get_pokemons()
# get_poke_info("Sadslash")
# get_poke_image("sandshrew")
