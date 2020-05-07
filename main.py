import requests
import shutil

def get_pokemons(url = "http://pokeapi.co/api/v2/pokemon-form/", offset=0):
    args = {'offset': offset} if offset else {}

    response = requests.get(url, params=args)

    if response.status_code == 200:
        payload = response.json()
        results = payload.get('results', [])
        next    = payload.get('next', [])
        # print(next)
        if results:
            for r in results:
                print(r['name'], ": ", r['url'])
        if next != None:
            get_pokemons(offset=offset+20)


def get_poke_info(poke_name="", poke_id=-1):
    if poke_id == -1 and poke_name == "":
        print("Please specify a pokemon name or id.")
        return
    if poke_name != "":
        url = "https://pokeapi.co/api/v2/pokemon/" + poke_name
        response = requests.get(url)

        if response.status_code == 200:
            payload = response.json()

            for k, v in payload.items():
                if k!= 'moves':
                    print(k, ":", v)
    elif poke_id != -1:
        url = "http://pokeapi.co/api/v2/pokemon/" + poke_id
        response = requests.get(url)

        if response.status_code == 200:
            payload = response.json()

            for k, v in payload.items():
                if k!= 'moves':
                    print(k, ":", v)

def get_poke_images(poke_name="", poke_id=-1):
    if poke_id == -1 and poke_name == "":
        print("Please specify a pokemon name or id.")
        return
    if poke_name != "":
        url = "https://pokeapi.co/api/v2/pokemon/" + poke_name
        response = requests.get(url)

        if response.status_code == 200:
            payload = response.json()
            # print(payload)
            name=""
            for k, v in payload.items():
                if k == 'name':
                    name = v
                if k == 'sprites':
                    count = 0
                    for sprite, u in v.items():
                        if u:
                            print(sprite, ":", u)
                            file_type = u.split("/")[-1]
                            filename = name + str(count) +"_"+ file_type
                            count += 1
                            r = requests.get(u, stream = True)
                            if r.status_code == 200:
                                # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                                r.raw.decode_content = True

                                # Open a local file with wb ( write binary ) permission.
                                with open(filename,'wb') as f:
                                    shutil.copyfileobj(r.raw, f)

# get_pokemons()

get_poke_info("1")

# get_poke_images(poke_name="bulbasaur")
