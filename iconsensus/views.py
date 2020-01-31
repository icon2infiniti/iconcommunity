from django.shortcuts import render
from .models import CorePrep
from . import iconsensusrpc
from iconsdk.exception import JSONRPCException

from django.contrib.staticfiles.templatetags.staticfiles import static

from collections import OrderedDict
from operator import itemgetter

import requests

from dashboard.models import MainInfo

import json


def init_mode(request):
    if 'nightmode' not in request.session:
        request.session['nightmode'] = True
    if 'navbar' not in request.session:
        request.session['navbar'] = True
    if 'fromAddress' not in request.session:
        request.session['fromAddress'] = 'none'

    context = {
        'nightmode': request.session['nightmode'],
        'navbar': request.session['navbar'],
        'fromAddress': request.session['fromAddress'],
        'section': 'ICONSENSUS',
    }
    return context


def about(request):
    context = init_mode(request)
    context.update({
        'subsection': 'ABOUT',
    })
    return render(request, 'iconsensus/about.html', context)


def prep_reward(i_rep, delegation_rate):
    return i_rep * 0.5 * 100 * (delegation_rate/100)


def overview(request):
    context = init_mode(request)

    # ICX USD price
    try:
        r = requests.get('https://api.velic.io/api/v1/public/transaction?base_coin=USDT&match_coin=ICX')
    except requests.RequestException as e:
        print("111111111111111111111111111111111")
        icx_price = 0
    #else:
        #rjson = r.json()
        #icx_price = rjson[0]['price']

    icx_price = 0.247
    # GetPReps
    params = {}
    preps = {}
    try:
        preps = iconsensusrpc.IconsensusRPCCalls().json_rpc_call("getPReps", params)
    except JSONRPCException as e:
        print(str(e.message))

    # Query and rebuild custom ranking list
    TOTAL_DELEGATED = int(preps['totalDelegated'], 16)/10**18
    PREP_GRADE = {0: 'Main P-Rep', 1: 'Sub P-Rep', 2: 'P-Rep'}
    TOTAL_IREP = 0

    for prep in preps['preps']:
        if int(prep['grade'], 16) == 0:
            TOTAL_IREP += int(int(prep['irep'], 16)/10**18)

    average_irep = TOTAL_IREP/22

    countries = {}
    for prep in preps['preps']:
        prep_grade = int(prep['grade'], 16)
        prep['grade'] = PREP_GRADE[prep_grade]
        irep = int(int(prep['irep'], 16)/10**18)
        prep['irep'] = '{:,}'.format(irep)
        prep['stake'] = int(int(prep['stake'], 16)/10**18)
        delegated = int(prep['delegated'], 16)/10**18
        delegation_rate = delegated / TOTAL_DELEGATED * 100
        prep['delegated'] = int(delegated)
        prep['delegate_percent'] = delegation_rate
        prep['reward'] = int(prep_reward(TOTAL_IREP/22, delegation_rate))
        prep['reward_usd'] = int(int(prep['reward'])*float(icx_price))
        prep['validatedBlocks'] = int(prep['validatedBlocks'], 16)
        prep['totalBlocks'] = int(prep['totalBlocks'], 16)

        if not prep['country'] in countries:
            countries[prep['country']] = 1
        else:
            countries[prep['country']] += 1

        # get Prep details, but too slow. Do more efficient way
        # address = {
        #   "address": prep['address']
        # }
        # try:
        #    prep['detail'] = dashboardrpc.DashboardRPCCalls().json_rpc_call("getPRep", address)
        # except JSONRPCException as e:
        #    print(str(e.message))

        #prep_json = prep['detail']['details']
        # print(prep_json)

    countries_alpha2 = {}
    countries_name = {}
    for k, v in countries.items():
        countries_alpha2[convert_alpha_3_to_2(k)] = v
        countries_name[convert_alpha_3_to_name(k)] = v

    countries_name_sorted = OrderedDict(sorted(countries_name.items(), key=itemgetter(1), reverse=True))

    prep_all = preps['preps']
    prep_main = list(filter(lambda d: d['grade'] == 'Main P-Rep', prep_all))
    prep_sub = list(filter(lambda d: d['grade'] == 'Sub P-Rep', prep_all))

    maininfo = MainInfo.objects.all()[0].maininfo_json
    maininfo = maininfo.replace("\'", "\"")
    maininfo = json.loads(maininfo)

    public_treasury = int(float(maininfo['publicTreasury']))
    total_supply = float(maininfo['icxSupply'])
    total_staked = int(preps['totalStake'], 16) / 10 ** 18
    total_staked_percent = round(total_staked / total_supply * 100, 2)
    total_voted = int(preps['totalDelegated'], 16)/10**18
    total_voted_percent = round(total_voted / total_supply * 100, 2)
    total_staked = int(total_staked)
    total_voted = int(total_voted)

    context.update({
        'subsection': 'OVERVIEW',
        'prep_all': prep_all,
        'main_preps_count': len(prep_main),
        'sub_preps_count': len(prep_sub),
        'preps_count': len(prep_all),
        'prep_main': prep_main,
        'prep_sub': prep_sub,
        'countries_alpha2': countries_alpha2,
        'countries_name_sorted': countries_name_sorted,
        'public_treasury': public_treasury,
        'total_voted': total_voted,
        'total_staked': total_staked,
        'total_supply': total_supply,
        'total_staked_percent': total_staked_percent,
        'total_voted_percent': total_voted_percent,
        'average_irep': average_irep,
        'TOTAL_DELEGATED': TOTAL_DELEGATED,
        'icx_price': icx_price,
    })
    return render(request, 'iconsensus/overview.html', context)


# Get market data
def get_map_marker(prep):
    position = prep.server_location_latlong.replace('(', '').replace(')', '').strip().split(',')
    url = '/iconsensus/candidate_detail/'+str(prep.id)+'/'
    if position and len(position) > 1:
        data = {
            'icon': static('iconsensus/img/'+prep.logo),
            'position': {
                'lat': position[0],
                'lng': position[1]
            },
            'url': url
        }
    return data


def candidates(request):
    context = init_mode(request)
    preps = CorePrep.objects.using('prepsqlite3').filter(display=True).order_by('-id')
    total = CorePrep.objects.using('prepsqlite3').filter(display=True).count

    # Prepare Database Prep Map Locations
    locations = []
    for prep in preps:
        try:
            location = get_map_marker(prep)
            if location:
                locations.append(location)
        except Exception as e:
            pass

    context.update({
        'subsection': 'CANDIDATES',
        'preps': preps,
        'prep_locations': locations,
        'total': total,
    })
    return render(request, 'iconsensus/candidates.html', context)


def candidate_detail(request, pk):
    context = init_mode(request)
    prep = CorePrep.objects.using('prepsqlite3').get(pk=pk)

    context.update({
        'subsection': 'CANDIDATES',
        'prep': prep,
    })
    return render(request, 'iconsensus/candidate_detail.html', context)


def convert_alpha_3_to_2(code):
    countryISOMapping = {
        "AFG": "AF",
        "ALA": "AX",
        "ALB": "AL",
        "DZA": "DZ",
        "ASM": "AS",
        "AND": "AD",
        "AGO": "AO",
        "AIA": "AI",
        "ATA": "AQ",
        "ATG": "AG",
        "ARG": "AR",
        "ARM": "AM",
        "ABW": "AW",
        "AUS": "AU",
        "AUT": "AT",
        "AZE": "AZ",
        "BHS": "BS",
        "BHR": "BH",
        "BGD": "BD",
        "BRB": "BB",
        "BLR": "BY",
        "BEL": "BE",
        "BLZ": "BZ",
        "BEN": "BJ",
        "BMU": "BM",
        "BTN": "BT",
        "BOL": "BO",
        "BIH": "BA",
        "BWA": "BW",
        "BVT": "BV",
        "BRA": "BR",
        "VGB": "VG",
        "IOT": "IO",
        "BRN": "BN",
        "BGR": "BG",
        "BFA": "BF",
        "BDI": "BI",
        "KHM": "KH",
        "CMR": "CM",
        "CAN": "CA",
        "CPV": "CV",
        "CYM": "KY",
        "CAF": "CF",
        "TCD": "TD",
        "CHL": "CL",
        "CHN": "CN",
        "HKG": "HK",
        "MAC": "MO",
        "CXR": "CX",
        "CCK": "CC",
        "COL": "CO",
        "COM": "KM",
        "COG": "CG",
        "COD": "CD",
        "COK": "CK",
        "CRI": "CR",
        "CIV": "CI",
        "HRV": "HR",
        "CUB": "CU",
        "CYP": "CY",
        "CZE": "CZ",
        "DNK": "DK",
        "DJI": "DJ",
        "DMA": "DM",
        "DOM": "DO",
        "ECU": "EC",
        "EGY": "EG",
        "SLV": "SV",
        "GNQ": "GQ",
        "ERI": "ER",
        "EST": "EE",
        "ETH": "ET",
        "FLK": "FK",
        "FRO": "FO",
        "FJI": "FJ",
        "FIN": "FI",
        "FRA": "FR",
        "GUF": "GF",
        "PYF": "PF",
        "ATF": "TF",
        "GAB": "GA",
        "GMB": "GM",
        "GEO": "GE",
        "DEU": "DE",
        "GHA": "GH",
        "GIB": "GI",
        "GRC": "GR",
        "GRL": "GL",
        "GRD": "GD",
        "GLP": "GP",
        "GUM": "GU",
        "GTM": "GT",
        "GGY": "GG",
        "GIN": "GN",
        "GNB": "GW",
        "GUY": "GY",
        "HTI": "HT",
        "HMD": "HM",
        "VAT": "VA",
        "HND": "HN",
        "HUN": "HU",
        "ISL": "IS",
        "IND": "IN",
        "IDN": "ID",
        "IRN": "IR",
        "IRQ": "IQ",
        "IRL": "IE",
        "IMN": "IM",
        "ISR": "IL",
        "ITA": "IT",
        "JAM": "JM",
        "JPN": "JP",
        "JEY": "JE",
        "JOR": "JO",
        "KAZ": "KZ",
        "KEN": "KE",
        "KIR": "KI",
        "PRK": "KP",
        "KOR": "KR",
        "KWT": "KW",
        "KGZ": "KG",
        "LAO": "LA",
        "LVA": "LV",
        "LBN": "LB",
        "LSO": "LS",
        "LBR": "LR",
        "LBY": "LY",
        "LIE": "LI",
        "LTU": "LT",
        "LUX": "LU",
        "MKD": "MK",
        "MDG": "MG",
        "MWI": "MW",
        "MYS": "MY",
        "MDV": "MV",
        "MLI": "ML",
        "MLT": "MT",
        "MHL": "MH",
        "MTQ": "MQ",
        "MRT": "MR",
        "MUS": "MU",
        "MYT": "YT",
        "MEX": "MX",
        "FSM": "FM",
        "MDA": "MD",
        "MCO": "MC",
        "MNG": "MN",
        "MNE": "ME",
        "MSR": "MS",
        "MAR": "MA",
        "MOZ": "MZ",
        "MMR": "MM",
        "NAM": "NA",
        "NRU": "NR",
        "NPL": "NP",
        "NLD": "NL",
        "ANT": "AN",
        "NCL": "NC",
        "NZL": "NZ",
        "NIC": "NI",
        "NER": "NE",
        "NGA": "NG",
        "NIU": "NU",
        "NFK": "NF",
        "MNP": "MP",
        "NOR": "NO",
        "OMN": "OM",
        "PAK": "PK",
        "PLW": "PW",
        "PSE": "PS",
        "PAN": "PA",
        "PNG": "PG",
        "PRY": "PY",
        "PER": "PE",
        "PHL": "PH",
        "PCN": "PN",
        "POL": "PL",
        "PRT": "PT",
        "PRI": "PR",
        "QAT": "QA",
        "REU": "RE",
        "ROU": "RO",
        "RUS": "RU",
        "RWA": "RW",
        "BLM": "BL",
        "SHN": "SH",
        "KNA": "KN",
        "LCA": "LC",
        "MAF": "MF",
        "SPM": "PM",
        "VCT": "VC",
        "WSM": "WS",
        "SMR": "SM",
        "STP": "ST",
        "SAU": "SA",
        "SEN": "SN",
        "SRB": "RS",
        "SYC": "SC",
        "SLE": "SL",
        "SGP": "SG",
        "SVK": "SK",
        "SVN": "SI",
        "SLB": "SB",
        "SOM": "SO",
        "ZAF": "ZA",
        "SGS": "GS",
        "SSD": "SS",
        "ESP": "ES",
        "LKA": "LK",
        "SDN": "SD",
        "SUR": "SR",
        "SJM": "SJ",
        "SWZ": "SZ",
        "SWE": "SE",
        "CHE": "CH",
        "SYR": "SY",
        "TWN": "TW",
        "TJK": "TJ",
        "TZA": "TZ",
        "THA": "TH",
        "TLS": "TL",
        "TGO": "TG",
        "TKL": "TK",
        "TON": "TO",
        "TTO": "TT",
        "TUN": "TN",
        "TUR": "TR",
        "TKM": "TM",
        "TCA": "TC",
        "TUV": "TV",
        "UGA": "UG",
        "UKR": "UA",
        "ARE": "AE",
        "GBR": "GB",
        "USA": "US",
        "UMI": "UM",
        "URY": "UY",
        "UZB": "UZ",
        "VUT": "VU",
        "VEN": "VE",
        "VNM": "VN",
        "VIR": "VI",
        "WLF": "WF",
        "ESH": "EH",
        "YEM": "YE",
        "ZMB": "ZM",
        "ZWE": "ZW"
    }
    return countryISOMapping[code]


def convert_alpha_3_to_name(code):
    countryISOMapping = {
        'AFG': 'Afghanistan',
        'ALA': 'Aland Islands',
        'ALB': 'Albania',
        'DZA': 'Algeria',
        'ASM': 'American Samoa',
        'AND': 'Andorra',
        'AGO': 'Angola',
        'AIA': 'Anguilla',
        'ATA': 'Antarctica',
        'ATG': 'Antigua and Barbuda',
        'ARG': 'Argentina',
        'ARM': 'Armenia',
        'ABW': 'Aruba',
        'AUS': 'Australia',
        'AUT': 'Austria',
        'AZE': 'Azerbaijan',
        'BHS': 'Bahamas',
        'BHR': 'Bahrain',
        'BGD': 'Bangladesh',
        'BRB': 'Barbados',
        'BLR': 'Belarus',
        'BEL': 'Belgium',
        'BLZ': 'Belize',
        'BEN': 'Benin',
        'BMU': 'Bermuda',
        'BTN': 'Bhutan',
        'BOL': 'Bolivia',
        'BIH': 'Bosnia and Herzegovina',
        'BWA': 'Botswana',
        'BVT': 'Bouvet Island',
        'BRA': 'Brazil',
        'VGB': 'British Virgin Islands',
        'IOT': 'British Indian Ocean Territory',
        'BRN': 'Brunei Darussalam',
        'BGR': 'Bulgaria',
        'BFA': 'Burkina Faso',
        'BDI': 'Burundi',
        'KHM': 'Cambodia',
        'CMR': 'Cameroon',
        'CAN': 'Canada',
        'CPV': 'Cape Verde',
        'CYM': 'Cayman Islands',
        'CAF': 'Central African Republic',
        'TCD': 'Chad',
        'CHL': 'Chile',
        'CHN': 'China',
        'HKG': 'Hong Kong, Special Administrative Region of China',
        'MAC': 'Macao, Special Administrative Region of China',
        'CXR': 'Christmas Island',
        'CCK': 'Cocos (Keeling) Islands',
        'COL': 'Colombia',
        'COM': 'Comoros',
        'COG': 'Congo (Brazzaville)',
        'COD': 'Congo, Democratic Republic of the',
        'COK': 'Cook Islands',
        'CRI': 'Costa Rica',
        'CIV': 'Cote d\'Ivoire',
        'HRV': 'Croatia',
        'CUB': 'Cuba',
        'CYP': 'Cyprus',
        'CZE': 'Czech Republic',
        'DNK': 'Denmark',
        'DJI': 'Djibouti',
        'DMA': 'Dominica',
        'DOM': 'Dominican Republic',
        'ECU': 'Ecuador',
        'EGY': 'Egypt',
        'SLV': 'El Salvador',
        'GNQ': 'Equatorial Guinea',
        'ERI': 'Eritrea',
        'EST': 'Estonia',
        'ETH': 'Ethiopia',
        'FLK': 'Falkland Islands (Malvinas)',
        'FRO': 'Faroe Islands',
        'FJI': 'Fiji',
        'FIN': 'Finland',
        'FRA': 'France',
        'GUF': 'French Guiana',
        'PYF': 'French Polynesia',
        'ATF': 'French Southern Territories',
        'GAB': 'Gabon',
        'GMB': 'Gambia',
        'GEO': 'Georgia',
        'DEU': 'Germany',
        'GHA': 'Ghana',
        'GIB': 'Gibraltar',
        'GRC': 'Greece',
        'GRL': 'Greenland',
        'GRD': 'Grenada',
        'GLP': 'Guadeloupe',
        'GUM': 'Guam',
        'GTM': 'Guatemala',
        'GGY': 'Guernsey',
        'GIN': 'Guinea',
        'GNB': 'Guinea-Bissau',
        'GUY': 'Guyana',
        'HTI': 'Haiti',
        'HMD': 'Heard Island and Mcdonald Islands',
        'VAT': 'Holy See (Vatican City State)',
        'HND': 'Honduras',
        'HUN': 'Hungary',
        'ISL': 'Iceland',
        'IND': 'India',
        'IDN': 'Indonesia',
        'IRN': 'Iran, Islamic Republic of',
        'IRQ': 'Iraq',
        'IRL': 'Ireland',
        'IMN': 'Isle of Man',
        'ISR': 'Israel',
        'ITA': 'Italy',
        'JAM': 'Jamaica',
        'JPN': 'Japan',
        'JEY': 'Jersey',
        'JOR': 'Jordan',
        'KAZ': 'Kazakhstan',
        'KEN': 'Kenya',
        'KIR': 'Kiribati',
        'PRK': 'North Korea',
        'KOR': 'South Korea',
        'KWT': 'Kuwait',
        'KGZ': 'Kyrgyzstan',
        'LAO': 'Lao PDR',
        'LVA': 'Latvia',
        'LBN': 'Lebanon',
        'LSO': 'Lesotho',
        'LBR': 'Liberia',
        'LBY': 'Libya',
        'LIE': 'Liechtenstein',
        'LTU': 'Lithuania',
        'LUX': 'Luxembourg',
        'MKD': 'Macedonia, Republic of',
        'MDG': 'Madagascar',
        'MWI': 'Malawi',
        'MYS': 'Malaysia',
        'MDV': 'Maldives',
        'MLI': 'Mali',
        'MLT': 'Malta',
        'MHL': 'Marshall Islands',
        'MTQ': 'Martinique',
        'MRT': 'Mauritania',
        'MUS': 'Mauritius',
        'MYT': 'Mayotte',
        'MEX': 'Mexico',
        'FSM': 'Micronesia, Federated States of',
        'MDA': 'Moldova',
        'MCO': 'Monaco',
        'MNG': 'Mongolia',
        'MNE': 'Montenegro',
        'MSR': 'Montserrat',
        'MAR': 'Morocco',
        'MOZ': 'Mozambique',
        'MMR': 'Myanmar',
        'NAM': 'Namibia',
        'NRU': 'Nauru',
        'NPL': 'Nepal',
        'NLD': 'Netherlands',
        'ANT': 'Netherlands Antilles',
        'NCL': 'New Caledonia',
        'NZL': 'New Zealand',
        'NIC': 'Nicaragua',
        'NER': 'Niger',
        'NGA': 'Nigeria',
        'NIU': 'Niue',
        'NFK': 'Norfolk Island',
        'MNP': 'Northern Mariana Islands',
        'NOR': 'Norway',
        'OMN': 'Oman',
        'PAK': 'Pakistan',
        'PLW': 'Palau',
        'PSE': 'Palestinian Territory, Occupied',
        'PAN': 'Panama',
        'PNG': 'Papua New Guinea',
        'PRY': 'Paraguay',
        'PER': 'Peru',
        'PHL': 'Philippines',
        'PCN': 'Pitcairn',
        'POL': 'Poland',
        'PRT': 'Portugal',
        'PRI': 'Puerto Rico',
        'QAT': 'Qatar',
        'REU': 'Reunion',
        'ROU': 'Romania',
        'RUS': 'Russian Federation',
        'RWA': 'Rwanda',
        'BLM': 'Saint-Barthelemy',
        'SHN': 'Saint Helena',
        'KNA': 'Saint Kitts and Nevis',
        'LCA': 'Saint Lucia',
        'MAF': 'Saint-Martin (French part)',
        'SPM': 'Saint Pierre and Miquelon',
        'VCT': 'Saint Vincent and Grenadines',
        'WSM': 'Samoa',
        'SMR': 'San Marino',
        'STP': 'Sao Tome and Principe',
        'SAU': 'Saudi Arabia',
        'SEN': 'Senegal',
        'SRB': 'Serbia',
        'SYC': 'Seychelles',
        'SLE': 'Sierra Leone',
        'SGP': 'Singapore',
        'SVK': 'Slovakia',
        'SVN': 'Slovenia',
        'SLB': 'Solomon Islands',
        'SOM': 'Somalia',
        'ZAF': 'South Africa',
        'SGS': 'South Georgia and the South Sandwich Islands',
        'SSD': 'South Sudan',
        'ESP': 'Spain',
        'LKA': 'Sri Lanka',
        'SDN': 'Sudan',
        'SUR': 'Suriname',
        'SJM': 'Svalbard and Jan Mayen Islands',
        'SWZ': 'Swaziland',
        'SWE': 'Sweden',
        'CHE': 'Switzerland',
        'SYR': 'Syrian Arab Republic (Syria)',
        'TWN': 'Taiwan, Republic of China',
        'TJK': 'Tajikistan',
        'TZA': 'Tanzania, United Republic of',
        'THA': 'Thailand',
        'TLS': 'Timor-Leste',
        'TGO': 'Togo',
        'TKL': 'Tokelau',
        'TON': 'Tonga',
        'TTO': 'Trinidad and Tobago',
        'TUN': 'Tunisia',
        'TUR': 'Turkey',
        'TKM': 'Turkmenistan',
        'TCA': 'Turks and Caicos Islands',
        'TUV': 'Tuvalu',
        'UGA': 'Uganda',
        'UKR': 'Ukraine',
        'ARE': 'United Arab Emirates',
        'GBR': 'United Kingdom',
        'USA': 'United States of America',
        'UMI': 'United States Minor Outlying Islands',
        'URY': 'Uruguay',
        'UZB': 'Uzbekistan',
        'VUT': 'Vanuatu',
        'VEN': 'Venezuela (Bolivarian Republic of)',
        'VNM': 'Viet Nam',
        'VIR': 'Virgin Islands, US',
        'WLF': 'Wallis and Futuna Islands',
        'ESH': 'Western Sahara',
        'YEM': 'Yemen',
        'ZMB': 'Zambia',
        'ZWE': 'Zimbabwe'
    }
    return countryISOMapping[code]
