from .models import PrepListing
from . import iconsensusrpc
from iconsdk.exception import JSONRPCException

import requests
import json
import tempfile
from django.core import files

from urllib.parse import urlparse
import os
from django.conf import settings
import urllib.request


''' WIP
def get_preps():

    try:
        import shutil
        shutil.rmtree(os.path.join(settings.MEDIA_ROOT, 'teamlogo'))
        os.mkdir(os.path.join(settings.MEDIA_ROOT)+'/teamlogo')
    except OSError as e:
        print(e)

    # GetPReps
    params = {}
    preps = {}
    try:
        preps = iconsensusrpc.IconsensusRPCCalls().json_rpc_call("getPReps", params)
    except JSONRPCException as e:
        print(str(e.message))

    PrepListing.objects.all().delete()
    rank = 1
    for prep in preps['preps']:
        preplisting = PrepListing()
        preplisting.rank = rank
        rank += 1
        preplisting.address = prep['address']
        preplisting.grade = prep['grade']
        preplisting.name = prep['name']
        preplisting.country = prep['country']
        preplisting.delegated = prep['delegated']
        preplisting.irep = prep['irep']
        #preplisting.details = prep['details']
        #print(preplisting.details)

        try:
            r = requests.get(prep['details'])
        except requests.RequestException as e:
            print(e)

        try:
            rjson = r.json()
        except ValueError as e:
            print(e)

        if urlparse(str(preplisting.logo)):
            urllib.request.urlretrieve(preplisting.logo, str(preplisting.logo).split('/')[-1])
            
'''





'''
        try:
            preplisting.logo = rjson["representative"]["logo"]["logo_256"]
        except KeyError as e:
            print(e)

        if urlparse(str(preplisting.logo)):
            try:
                request = requests.get(preplisting.logo, stream=True)
                if request.status_code != requests.codes.ok:
                    print(request.status_code)

                file_name = str(preplisting.logo).split('/')[-1]
                lf = tempfile.NamedTemporaryFile()

                for block in request.iter_content(1024 * 8):
                    if not block:
                        break
                    lf.write(block)
                if file_name.endswith('.png') or file_name.endswith('.jpg'):
                    preplisting.logo.save(file_name, files.File(lf))
            except requests.exceptions.MissingSchema as e:
                print(e)
            except requests.exceptions.RequestException as e:
                print("general error")

        preplisting.save()

            # Save the temporary image to the model#
            # This saves the model so be sure that is it valid
            #image.image.save(file_name, files.File(lf))
        '''


'''
    logo = models.ImageField()
'''

'''
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
'''

