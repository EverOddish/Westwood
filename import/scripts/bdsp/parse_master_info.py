import os
import re
import sys

sys.path.append(os.getcwd())
from intermediate.pokemon import Pokemon, StatSet, TypeSet, AbilitySet, AbilityRecord, EvolutionSet, EvolutionRecord
from intermediate.learnset import PokemonLearnset, Learnset
from intermediate.tm_set import PokemonTmSet, TmSet
from intermediate.tutor_set import PokemonTutorSet, TutorSet

pokedex = {
    1: 'Bulbasaur',
    2: 'Ivysaur',
    3: 'Venusaur',
    4: 'Charmander',
    5: 'Charmeleon',
    6: 'Charizard',
    7: 'Squirtle',
    8: 'Wartortle',
    9: 'Blastoise',
    10: 'Caterpie',
    11: 'Metapod',
    12: 'Butterfree',
    13: 'Weedle',
    14: 'Kakuna',
    15: 'Beedrill',
    16: 'Pidgey',
    17: 'Pidgeotto',
    18: 'Pidgeot',
    19: 'Rattata',
    20: 'Raticate',
    21: 'Spearow',
    22: 'Fearow',
    23: 'Ekans',
    24: 'Arbok',
    25: 'Pikachu',
    26: 'Raichu',
    27: 'Sandshrew',
    28: 'Sandslash',
    29: 'Nidoran_f',
    30: 'Nidorina',
    31: 'Nidoqueen',
    32: 'Nidoran_m',
    33: 'Nidorino',
    34: 'Nidoking',
    35: 'Clefairy',
    36: 'Clefable',
    37: 'Vulpix',
    38: 'Ninetales',
    39: 'Jigglypuff',
    40: 'Wigglytuff',
    41: 'Zubat',
    42: 'Golbat',
    43: 'Oddish',
    44: 'Gloom',
    45: 'Vileplume',
    46: 'Paras',
    47: 'Parasect',
    48: 'Venonat',
    49: 'Venomoth',
    50: 'Diglett',
    51: 'Dugtrio',
    52: 'Meowth',
    53: 'Persian',
    54: 'Psyduck',
    55: 'Golduck',
    56: 'Mankey',
    57: 'Primeape',
    58: 'Growlithe',
    59: 'Arcanine',
    60: 'Poliwag',
    61: 'Poliwhirl',
    62: 'Poliwrath',
    63: 'Abra',
    64: 'Kadabra',
    65: 'Alakazam',
    66: 'Machop',
    67: 'Machoke',
    68: 'Machamp',
    69: 'Bellsprout',
    70: 'Weepinbell',
    71: 'Victreebel',
    72: 'Tentacool',
    73: 'Tentacruel',
    74: 'Geodude',
    75: 'Graveler',
    76: 'Golem',
    77: 'Ponyta',
    78: 'Rapidash',
    79: 'Slowpoke',
    80: 'Slowbro',
    81: 'Magnemite',
    82: 'Magneton',
    83: 'Farfetch_d',
    84: 'Doduo',
    85: 'Dodrio',
    86: 'Seel',
    87: 'Dewgong',
    88: 'Grimer',
    89: 'Muk',
    90: 'Shellder',
    91: 'Cloyster',
    92: 'Gastly',
    93: 'Haunter',
    94: 'Gengar',
    95: 'Onix',
    96: 'Drowzee',
    97: 'Hypno',
    98: 'Krabby',
    99: 'Kingler',
    100: 'Voltorb',
    101: 'Electrode',
    102: 'Exeggcute',
    103: 'Exeggutor',
    104: 'Cubone',
    105: 'Marowak',
    106: 'Hitmonlee',
    107: 'Hitmonchan',
    108: 'Lickitung',
    109: 'Koffing',
    110: 'Weezing',
    111: 'Rhyhorn',
    112: 'Rhydon',
    113: 'Chansey',
    114: 'Tangela',
    115: 'Kangaskhan',
    116: 'Horsea',
    117: 'Seadra',
    118: 'Goldeen',
    119: 'Seaking',
    120: 'Staryu',
    121: 'Starmie',
    122: 'Mr_Mime',
    123: 'Scyther',
    124: 'Jynx',
    125: 'Electabuzz',
    126: 'Magmar',
    127: 'Pinsir',
    128: 'Tauros',
    129: 'Magikarp',
    130: 'Gyarados',
    131: 'Lapras',
    132: 'Ditto',
    133: 'Eevee',
    134: 'Vaporeon',
    135: 'Jolteon',
    136: 'Flareon',
    137: 'Porygon',
    138: 'Omanyte',
    139: 'Omastar',
    140: 'Kabuto',
    141: 'Kabutops',
    142: 'Aerodactyl',
    143: 'Snorlax',
    144: 'Articuno',
    145: 'Zapdos',
    146: 'Moltres',
    147: 'Dratini',
    148: 'Dragonair',
    149: 'Dragonite',
    150: 'Mewtwo',
    151: 'Mew',
    152: 'Chikorita',
    153: 'Bayleef',
    154: 'Meganium',
    155: 'Cyndaquil',
    156: 'Quilava',
    157: 'Typhlosion',
    158: 'Totodile',
    159: 'Croconaw',
    160: 'Feraligatr',
    161: 'Sentret',
    162: 'Furret',
    163: 'Hoothoot',
    164: 'Noctowl',
    165: 'Ledyba',
    166: 'Ledian',
    167: 'Spinarak',
    168: 'Ariados',
    169: 'Crobat',
    170: 'Chinchou',
    171: 'Lanturn',
    172: 'Pichu',
    173: 'Cleffa',
    174: 'Igglybuff',
    175: 'Togepi',
    176: 'Togetic',
    177: 'Natu',
    178: 'Xatu',
    179: 'Mareep',
    180: 'Flaaffy',
    181: 'Ampharos',
    182: 'Bellossom',
    183: 'Marill',
    184: 'Azumarill',
    185: 'Sudowoodo',
    186: 'Politoed',
    187: 'Hoppip',
    188: 'Skiploom',
    189: 'Jumpluff',
    190: 'Aipom',
    191: 'Sunkern',
    192: 'Sunflora',
    193: 'Yanma',
    194: 'Wooper',
    195: 'Quagsire',
    196: 'Espeon',
    197: 'Umbreon',
    198: 'Murkrow',
    199: 'Slowking',
    200: 'Misdreavus',
    201: 'Unown',
    202: 'Wobbuffet',
    203: 'Girafarig',
    204: 'Pineco',
    205: 'Forretress',
    206: 'Dunsparce',
    207: 'Gligar',
    208: 'Steelix',
    209: 'Snubbull',
    210: 'Granbull',
    211: 'Qwilfish',
    212: 'Scizor',
    213: 'Shuckle',
    214: 'Heracross',
    215: 'Sneasel',
    216: 'Teddiursa',
    217: 'Ursaring',
    218: 'Slugma',
    219: 'Magcargo',
    220: 'Swinub',
    221: 'Piloswine',
    222: 'Corsola',
    223: 'Remoraid',
    224: 'Octillery',
    225: 'Delibird',
    226: 'Mantine',
    227: 'Skarmory',
    228: 'Houndour',
    229: 'Houndoom',
    230: 'Kingdra',
    231: 'Phanpy',
    232: 'Donphan',
    233: 'Porygon2',
    234: 'Stantler',
    235: 'Smeargle',
    236: 'Tyrogue',
    237: 'Hitmontop',
    238: 'Smoochum',
    239: 'Elekid',
    240: 'Magby',
    241: 'Miltank',
    242: 'Blissey',
    243: 'Raikou',
    244: 'Entei',
    245: 'Suicune',
    246: 'Larvitar',
    247: 'Pupitar',
    248: 'Tyranitar',
    249: 'Lugia',
    250: 'Ho-Oh',
    251: 'Celebi',
    252: 'Treecko',
    253: 'Grovyle',
    254: 'Sceptile',
    255: 'Torchic',
    256: 'Combusken',
    257: 'Blaziken',
    258: 'Mudkip',
    259: 'Marshtomp',
    260: 'Swampert',
    261: 'Poochyena',
    262: 'Mightyena',
    263: 'Zigzagoon',
    264: 'Linoone',
    265: 'Wurmple',
    266: 'Silcoon',
    267: 'Beautifly',
    268: 'Cascoon',
    269: 'Dustox',
    270: 'Lotad',
    271: 'Lombre',
    272: 'Ludicolo',
    273: 'Seedot',
    274: 'Nuzleaf',
    275: 'Shiftry',
    276: 'Taillow',
    277: 'Swellow',
    278: 'Wingull',
    279: 'Pelipper',
    280: 'Ralts',
    281: 'Kirlia',
    282: 'Gardevoir',
    283: 'Surskit',
    284: 'Masquerain',
    285: 'Shroomish',
    286: 'Breloom',
    287: 'Slakoth',
    288: 'Vigoroth',
    289: 'Slaking',
    290: 'Nincada',
    291: 'Ninjask',
    292: 'Shedinja',
    293: 'Whismur',
    294: 'Loudred',
    295: 'Exploud',
    296: 'Makuhita',
    297: 'Hariyama',
    298: 'Azurill',
    299: 'Nosepass',
    300: 'Skitty',
    301: 'Delcatty',
    302: 'Sableye',
    303: 'Mawile',
    304: 'Aron',
    305: 'Lairon',
    306: 'Aggron',
    307: 'Meditite',
    308: 'Medicham',
    309: 'Electrike',
    310: 'Manectric',
    311: 'Plusle',
    312: 'Minun',
    313: 'Volbeat',
    314: 'Illumise',
    315: 'Roselia',
    316: 'Gulpin',
    317: 'Swalot',
    318: 'Carvanha',
    319: 'Sharpedo',
    320: 'Wailmer',
    321: 'Wailord',
    322: 'Numel',
    323: 'Camerupt',
    324: 'Torkoal',
    325: 'Spoink',
    326: 'Grumpig',
    327: 'Spinda',
    328: 'Trapinch',
    329: 'Vibrava',
    330: 'Flygon',
    331: 'Cacnea',
    332: 'Cacturne',
    333: 'Swablu',
    334: 'Altaria',
    335: 'Zangoose',
    336: 'Seviper',
    337: 'Lunatone',
    338: 'Solrock',
    339: 'Barboach',
    340: 'Whiscash',
    341: 'Corphish',
    342: 'Crawdaunt',
    343: 'Baltoy',
    344: 'Claydol',
    345: 'Lileep',
    346: 'Cradily',
    347: 'Anorith',
    348: 'Armaldo',
    349: 'Feebas',
    350: 'Milotic',
    351: 'Castform',
    352: 'Kecleon',
    353: 'Shuppet',
    354: 'Banette',
    355: 'Duskull',
    356: 'Dusclops',
    357: 'Tropius',
    358: 'Chimecho',
    359: 'Absol',
    360: 'Wynaut',
    361: 'Snorunt',
    362: 'Glalie',
    363: 'Spheal',
    364: 'Sealeo',
    365: 'Walrein',
    366: 'Clamperl',
    367: 'Huntail',
    368: 'Gorebyss',
    369: 'Relicanth',
    370: 'Luvdisc',
    371: 'Bagon',
    372: 'Shelgon',
    373: 'Salamence',
    374: 'Beldum',
    375: 'Metang',
    376: 'Metagross',
    377: 'Regirock',
    378: 'Regice',
    379: 'Registeel',
    380: 'Latias',
    381: 'Latios',
    382: 'Kyogre',
    383: 'Groudon',
    384: 'Rayquaza',
    385: 'Jirachi',
    386: 'Deoxys',
    387: 'Turtwig',
    388: 'Grotle',
    389: 'Torterra',
    390: 'Chimchar',
    391: 'Monferno',
    392: 'Infernape',
    393: 'Piplup',
    394: 'Prinplup',
    395: 'Empoleon',
    396: 'Starly',
    397: 'Staravia',
    398: 'Staraptor',
    399: 'Bidoof',
    400: 'Bibarel',
    401: 'Kricketot',
    402: 'Kricketune',
    403: 'Shinx',
    404: 'Luxio',
    405: 'Luxray',
    406: 'Budew',
    407: 'Roserade',
    408: 'Cranidos',
    409: 'Rampardos',
    410: 'Shieldon',
    411: 'Bastiodon',
    412: 'Burmy',
    413: 'Wormadam',
    414: 'Mothim',
    415: 'Combee',
    416: 'Vespiquen',
    417: 'Pachirisu',
    418: 'Buizel',
    419: 'Floatzel',
    420: 'Cherubi',
    421: 'Cherrim',
    422: 'Shellos',
    423: 'Gastrodon',
    424: 'Ambipom',
    425: 'Drifloon',
    426: 'Drifblim',
    427: 'Buneary',
    428: 'Lopunny',
    429: 'Mismagius',
    430: 'Honchkrow',
    431: 'Glameow',
    432: 'Purugly',
    433: 'Chingling',
    434: 'Stunky',
    435: 'Skuntank',
    436: 'Bronzor',
    437: 'Bronzong',
    438: 'Bonsly',
    439: 'Mime Jr.',
    440: 'Happiny',
    441: 'Chatot',
    442: 'Spiritomb',
    443: 'Gible',
    444: 'Gabite',
    445: 'Garchomp',
    446: 'Munchlax',
    447: 'Riolu',
    448: 'Lucario',
    449: 'Hippopotas',
    450: 'Hippowdon',
    451: 'Skorupi',
    452: 'Drapion',
    453: 'Croagunk',
    454: 'Toxicroak',
    455: 'Carnivine',
    456: 'Finneon',
    457: 'Lumineon',
    458: 'Mantyke',
    459: 'Snover',
    460: 'Abomasnow',
    461: 'Weavile',
    462: 'Magnezone',
    463: 'Lickilicky',
    464: 'Rhyperior',
    465: 'Tangrowth',
    466: 'Electivire',
    467: 'Magmortar',
    468: 'Togekiss',
    469: 'Yanmega',
    470: 'Leafeon',
    471: 'Glaceon',
    472: 'Gliscor',
    473: 'Mamoswine',
    474: 'Porygon-Z',
    475: 'Gallade',
    476: 'Probopass',
    477: 'Dusknoir',
    478: 'Froslass',
    479: 'Rotom',
    480: 'Uxie',
    481: 'Mesprit',
    482: 'Azelf',
    483: 'Dialga',
    484: 'Palkia',
    485: 'Heatran',
    486: 'Regigigas',
    487: 'Giratina',
    488: 'Cresselia',
    489: 'Phione',
    490: 'Manaphy',
    491: 'Darkrai',
    492: 'Shaymin',
    493: 'Arceus',
}

class TempPokemon():
    def __init__(self):
        self.name = None
        self.hp = None
        self.attack = None
        self.defense = None
        self.special_attack = None
        self.special_defense = None
        self.speed = None
        self.type1 = None
        self.type2 = None
        self.learnset = None
        self.egg_moves = None
        self.tm_moves = None
        self.tutor_moves = None
        self.evo_species_id = None
        self.evo_level = None

with open(os.path.join('scripts', 'bdsp', 'master_pokemon_info.txt')) as f:
    lines = f.readlines()

    pokemon_re = re.compile(r'([A-Za-z\. \-]+) - (\d+)/(\d+)/(\d+)/(\d+)/(\d+)/(\d+) ([A-Za-z]+)/([A-Za-z]+)')
    evolution_re = re.compile(r'Evolution\(s\): \d+,\d+,(\d+),\d+,(\d+)')
    egg_moves_re = re.compile(r'Egg Moves: ([A-Za-z ,\-]+)')
    tm_moves_re = re.compile(r'TM Moves: ([A-Za-z0-9 \-,]+)')
    tutor_moves_re = re.compile(r'Special Tutor Moves: ([A-Za-z0-9 ,\-]+)')
    learned_move_re = re.compile(r'\t([A-Za-z -]+) @ (\d+)')

    learned_moves = False
    pokemon_list = []
    current_pokemon = TempPokemon()
    current_moves = []

    for line in lines:
        line = line.replace('\n', '')
        if learned_moves:
            matches = learned_move_re.match(line)
            if matches:
                move_name = matches.group(1)
                level = matches.group(2)
                if '0' == level:
                    level = '1'
                current_moves.append((str(level), move_name))
            elif len(line) == 0:
                learned_moves = False
                current_pokemon.learnset = current_moves
                pokemon_list.append(current_pokemon)
                current_pokemon = TempPokemon()
                current_moves = []
        else:
            matches = pokemon_re.match(line)
            if matches:
                current_pokemon.name = matches.group(1)
                current_pokemon.hp = matches.group(2)
                current_pokemon.attack = matches.group(3)
                current_pokemon.defense = matches.group(4)
                current_pokemon.special_attack = matches.group(5)
                current_pokemon.special_defense = matches.group(6)
                current_pokemon.speed = matches.group(7)
                current_pokemon.type1 = matches.group(8)
                current_pokemon.type2 = matches.group(9)
                if current_pokemon.type1 == current_pokemon.type2:
                    current_pokemon.type2 = None

            matches = evolution_re.match(line)
            if matches:
                level = matches.group(2)
                current_pokemon.evo_species_id = matches.group(1)
                current_pokemon.evo_level = level

            matches = egg_moves_re.match(line)
            if matches:
                move_string = matches.group(1)
                current_pokemon.egg_moves = move_string.split(', ')

            matches = tm_moves_re.match(line)
            if matches:
                move_string = matches.group(1)
                current_pokemon.tm_moves = move_string.split(', ')

            matches = tutor_moves_re.match(line)
            if matches:
                move_string = matches.group(1)
                current_pokemon.tutor_moves = move_string.split(', ')

            if line.startswith('Learned Moves:'):
                learned_moves = True

print('Parsed ' + str(len(pokemon_list)) + ' TempPokemon')

for temp_pokemon in pokemon_list:
    pokemon_name = temp_pokemon.name
    if None == pokemon_name:
        continue
    if pokemon_name == 'PorygonZ':
        pokemon_name = 'porygon_z'
    if pokemon_name == 'NidoranF':
        pokemon_name = 'nidoran_f'
    if pokemon_name == 'NidoranM':
        pokemon_name = 'nidoran_m'
    if pokemon_name == 'MrMime':
        pokemon_name = 'mr_mime'
    if pokemon_name == 'HoOh':
        pokemon_name = 'ho_oh'
    if pokemon_name == 'MimeJr':
        pokemon_name = 'mime_jr'
    filename = '/Users/mikeaustin/github/Westwood/xml/pokemon/' + pokemon_name.replace("'", '_').replace(' ', '_').replace('.', '_').replace('-', '_').lower() + '.xml'
    if os.path.exists(filename):

        pokemon_object = Pokemon(filename)

        stat_set = StatSet()
        stat_set.games = ['Pokemon Brilliant Diamond', 'Pokemon Shining Pearl']
        stat_set.hp = temp_pokemon.hp
        stat_set.attack = temp_pokemon.attack
        stat_set.defense = temp_pokemon.defense
        stat_set.special_attack = temp_pokemon.special_attack
        stat_set.special_defense = temp_pokemon.special_defense
        stat_set.speed = temp_pokemon.speed
        pokemon_object.add_stat_set(stat_set)

        type_set = TypeSet()
        type_set.games = ['Pokemon Brilliant Diamond', 'Pokemon Shining Pearl']
        type_set.type1 = temp_pokemon.type1
        type_set.type2 = temp_pokemon.type2
        pokemon_object.add_type_set(type_set)

        ability_set = pokemon_object.copy_ability_set('Pokemon Diamond')
        ability_set.games = ['Pokemon Brilliant Diamond', 'Pokemon Shining Pearl']
        pokemon_object.add_ability_set(ability_set)

        if temp_pokemon.evo_level != None:
            if '0' == temp_pokemon.evo_level:
                evo_set = pokemon_object.copy_evolution_set('Pokemon Diamond')
                evo_set.games = ['Pokemon Brilliant Diamond', 'Pokemon Shining Pearl']
                pokemon_object.add_evolution_set(evo_set)
            else:
                evo_set = EvolutionSet()
                evo_set.games = ['Pokemon Brilliant Diamond', 'Pokemon Shining Pearl']
                evo_record = EvolutionRecord()
                evo_record.evolves_to = pokedex[int(temp_pokemon.evo_species_id)]
                evo_record.level = temp_pokemon.evo_level
                evo_set.evolution_records = [evo_record]
                pokemon_object.add_evolution_set(evo_set)

        with open(filename, 'w') as g:
            pokemon_object.dump(g)

        # --------------------------------------------------------------------

        #pokemon_learnset = PokemonLearnset(filename)

        #new_learnset = Learnset()
        #new_learnset.games = ['Pokemon Brilliant Diamond', 'Pokemon Shining Pearl']
        #new_learnset.moves = temp_pokemon.learnset

        #pokemon_learnset.add_learnset(new_learnset)

        #with open(filename, 'w') as f:
        #    pokemon_learnset.dump(f)

        # --------------------------------------------------------------------

        #pokemon_tmset = PokemonTmSet(filename)

        #new_tmset = TmSet()
        #new_tmset.games = ['Pokemon Brilliant Diamond', 'Pokemon Shining Pearl']
        #move_list = []
        #if temp_pokemon.tm_moves:
        #    for tm_move in temp_pokemon.tm_moves:
        #        move_list.append(tm_move.split(' ', 1)[1])
        #    new_tmset.moves = move_list

        #    pokemon_tmset.add_tm_set(new_tmset)

        #    with open(filename, 'w') as f:
        #        pokemon_tmset.dump(f)

        # --------------------------------------------------------------------

        #pokemon_tmset = PokemonTutorSet(filename)

        #new_tmset = TutorSet()
        #new_tmset.games = ['Pokemon Brilliant Diamond', 'Pokemon Shining Pearl']
        #move_list = []
        #if temp_pokemon.tutor_moves:
        #    new_tmset.moves = temp_pokemon.tutor_moves

        #    pokemon_tmset.add_tutor_set(new_tmset)

        #    with open(filename, 'w') as f:
        #        pokemon_tmset.dump(f)

        # --------------------------------------------------------------------

    else:
        print('Failed to locate pokemon: ' + pokemon_name)
