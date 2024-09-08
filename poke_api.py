import requests

def obtener_pokemon(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)
    
    if response.status_code != 200:
        return None  # Si no se encuentra el Pokémon o hay un error
    
    data = response.json()
    
    # Extraer el nombre, imagen y tipos del Pokémon
    pokemon_info = {
        'nombre': data['name'],
        'imagen': data['sprites']['front_default'] if data['sprites']['front_default'] else '',
        'tipo': [t['type']['name'] for t in data['types']]
    }
    
    return pokemon_info

def efectividad_tipo(type_name):
    url = f"https://pokeapi.co/api/v2/type/{type_name}/"
    response = requests.get(url)
    
    if response.status_code != 200:
        return None
    
    data = response.json()
    efectividad = {
        "strong_against": [],
        "weak_against": []
    }
    
    # Procesar las relaciones de efectividad
    for damage_relation in data['damage_relations']['double_damage_to']:
        efectividad["strong_against"].append(damage_relation['name'])
    
    for damage_relation in data['damage_relations']['half_damage_to']:
        efectividad["weak_against"].append(damage_relation['name'])
    
    return efectividad