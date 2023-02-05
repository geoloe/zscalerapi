from dataclasses import replace
import time
from pyrsistent import v
import requests
import json
from requests.structures import CaseInsensitiveDict
import pandas as pd
from collections import defaultdict

def obfuscateApiKey(key, url):
    seed = key
    now = int(time.time() * 1000)
    n = str(now)[-6:]
    r = str(int(n) >> 1).zfill(6)
    key = ""
    for i in range(0, len(str(n)), 1):
        key += seed[int(str(n)[i])]
    for j in range(0, len(str(r)), 1):
        key += seed[int(str(r)[j])+2]
 
    print("Timestamp:", now, "\tKey", key)

    return now, key

def initiate_Session(timestamp, key, username, password, url):

    data = {"apiKey": key, "username": username, "password": password, "timestamp": timestamp}
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"

    s = requests.Session()
    url = "https://"+ url +"/api/v1"

    response = s.post(url + "/authenticatedSession", headers=headers, data=json.dumps(data), verify=False)

    print(response.json())
    if "code" in response.json():
        if response.json()['code'] == 'AUTHENTICATION_FAILED':
            return 'AUTHENTICATION_FAILED'

    print(response.cookies.get_dict())
    return response.cookies

def get_admin(new_sesh, url):
    url = "https://"+ url +"/api/v1"
    r = requests.get(url= url + "/adminUsers", cookies=new_sesh, verify=False)
    return r, 1

def get_url_categories(new_sesh, url):
    url = "https://"+ url +"/api/v1"
    r = requests.get(url= url + "/urlCategories", cookies=new_sesh, verify=False)
    return r , 2

def get_fw_policies(new_sesh, url):
    url = "https://"+ url +"/api/v1"
    r = requests.get(url= url + "/firewallFilteringRules", cookies=new_sesh, verify=False)
    return r, 3

def cleanup(response, val):
    string = response.content.decode()
    string = string.replace(r'\n', ' ')
    string = string.replace('True','"True"')
    result = json.loads(string)

    my_list = []
    dct = {}
##### CLEANUP FÜR ADMINS #######
    if val == 1:
        test={}
        for a, b in enumerate(result):
            test[a] = b
        #print(test)
        tuple = ()
        for pair in nested_dict_pairs_iterator(test):
            #print(pair)
            cleanup, changes = admin_keywords() 
            if pair[1] == 'role':
                if pair[2] == 'name':
                    tuple += (pair[0],pair[1],pair[3]),
                if pair[3] == 'roleType':
                    tuple += (pair[0],'type',pair[4]),             
            else:
                if pair[1] not in cleanup:
                    tuple += pair, 
        dct = defaultdict(dict)
        for k, v, v2 in tuple:
            dct[k][v] = v2
        dct = dict(dct)

    ###### Dictionary cromprehension --> replace key in dicts
        #replace key simple dict
        #dct = {
        #    key.replace("id", "ID"): value for key, value in dct.items()
        #}
        #replace key nested dict
        #dct = {outer_k: {inner_k.replace("id", "ID"): inner_v for (inner_k, inner_v) in outer_v.items()} for (outer_k, outer_v) in dct.items()}
        #dct = {outer_k: {inner_k.replace("userName", "Name"): inner_v for (inner_k, inner_v) in outer_v.items()} for (outer_k, outer_v) in dct.items()}
    ###### Dictionary cromprehension --> replace key in dicts

    #### Get current columns
        for i in dct.keys():
            for j in dct[i].keys():
                if j not in my_list:
                    my_list.append(j)
    #### Get current columns

        print('Länge Liste:', len(my_list))
        print(my_list)

        # change column names
        for i in range(len(my_list)):
            for key, value in changes.items():
                if key == my_list[i]:
                    my_list[i] = value   
                else:
                    pass
##### CLEANUP FÜR URL CATEGORIES #######
    elif val == 2:
        test={}
        for a, b in enumerate(result):
            test[a] = b
        #print(test)
        tuple = ()
        for pair in nested_dict_pairs_iterator(test):
            #print(pair)
            cleanup, changes = url_keywords()
            if pair[1] == 'role':
                if pair[2] == 'name':
                    tuple += (pair[0],pair[1],pair[3]),
                if pair[3] == 'roleType':
                    tuple += (pair[0],'type',pair[4]),             
            else:
                if pair[1] not in cleanup and not isinstance(pair[2], list):
                    tuple += pair,
                else:
                    if isinstance(pair[2], list):
                        if not pair[2]:
                            tuple += (pair[0], pair[1], '---'),
                            print(tuple)
                        else:
                            string = '; '.join(map(str, pair[2]))
                            tuple += (pair[0], pair[1], string),
        dct = defaultdict(dict)
        for k, v, v2 in tuple:
            dct[k][v] = v2
        dct = dict(dct)
        #print(tuple)

    ###### Dictionary cromprehension --> replace key in dicts
        #replace key simple dict
        #dct = {
        #    key.replace("id", "ID"): value for key, value in dct.items()
        #}
        #replace key nested dict
        #dct = {outer_k: {inner_k.replace("id", "ID"): inner_v for (inner_k, inner_v) in outer_v.items()} for (outer_k, outer_v) in dct.items()}
        #dct = {outer_k: {inner_k.replace("userName", "Name"): inner_v for (inner_k, inner_v) in outer_v.items()} for (outer_k, outer_v) in dct.items()}
    ###### Dictionary cromprehension --> replace key in dicts

    #### Get current columns
        for i in dct.keys():
            for j in dct[i].keys():
                if j not in my_list:
                    my_list.append(j)
    #### Get current columns

        print('Länge Liste:', len(my_list))
        print(my_list)

        # change column names
        for i in range(len(my_list)):
            for key, value in changes.items():
                if key == my_list[i]:
                    my_list[i] = value   
                else:
                    pass
##### CLEANUP FÜR FIREWALL POLICY RULES ####### IN BEARBEITUNG
    else:
        test={}
        for a, b in enumerate(result):
            test[a] = b
        #print(test)
        tuple = ()
        for pair in nested_dict_pairs_iterator(test):
            #print(pair)
            cleanup, changes = admin_keywords() 
            if pair[1] == 'role':
                if pair[2] == 'name':
                    tuple += (pair[0],pair[1],pair[3]),
                if pair[3] == 'roleType':
                    tuple += (pair[0],'type',pair[4]),             
            else:
                if pair[1] not in cleanup:
                    tuple += pair, 
        dct = defaultdict(dict)
        for k, v, v2 in tuple:
            dct[k][v] = v2
        dct = dict(dct)

    ###### Dictionary cromprehension --> replace key in dicts
        #replace key simple dict
        #dct = {
        #    key.replace("id", "ID"): value for key, value in dct.items()
        #}
        #replace key nested dict
        #dct = {outer_k: {inner_k.replace("id", "ID"): inner_v for (inner_k, inner_v) in outer_v.items()} for (outer_k, outer_v) in dct.items()}
        #dct = {outer_k: {inner_k.replace("userName", "Name"): inner_v for (inner_k, inner_v) in outer_v.items()} for (outer_k, outer_v) in dct.items()}
    ###### Dictionary cromprehension --> replace key in dicts

    #### Get current columns
        for i in dct.keys():
            for j in dct[i].keys():
                if j not in my_list:
                    my_list.append(j)
    #### Get current columns

        print('Länge Liste:', len(my_list))
        print(my_list)

        # change column names
        for i in range(len(my_list)):
            for key, value in changes.items():
                if key == my_list[i]:
                    my_list[i] = value   
                else:
                    pass
    
    return result, my_list, dct



def create_csv(file, my_list, dct, result):

    # set indices in dataframe from dictionary
    df = pd.DataFrame.from_dict(dct, orient='index')

    df.columns = my_list
    df.to_csv(r"/home/nea/zscaler/files/"+file +".csv", index = True, header=True)

    return result, file + ".csv"

#### Hilffkt ######
def nested_dict_pairs_iterator(dict_obj):
    ''' This function accepts a nested dictionary as argument
        and iterate over all values of nested dictionaries
    '''
    # Iterate over all key-value pairs of dict argument
    for key, value in dict_obj.items():
        # Check if value is of dict type
        if isinstance(value, dict):
            # If value is dict then iterate over all its values
            for pair in  nested_dict_pairs_iterator(value):
                yield (key, *pair)
        else:
            # If value is not dict type then yield the value
            yield (key, value)

def admin_keywords():
    cleanup = ['adminScopeScopeEntities','email', 'pwdLastModifiedTime', 'name', 'id', 
    'isDeprecatedDefaultAdmin', 'isExecMobileAppEnabled', 'isSecurityReportCommEnabled', 
    'isServiceUpdateCommEnabled', 'isProductUpdateCommEnabled', 'adminScopescopeGroupMemberEntities']

    change_col_names = {'loginName':'LoginID',
    'userName':'Name', 
    'role':'Role',
    'type':'Role Type',
    'adminScopeType': 'Scope', 
    'isPasswordLoginAllowed': 'Password Enabled',
    'comments':'Comment', 
    'isDefaultAdmin':'Default Admin',
    'disabled':'Admin Disabled',
    'execMobileAppTokens':'Execute Mobile App Token Enabled'}

    return cleanup, change_col_names

def url_keywords():
    #### Werte anpassen ####
    cleanup = ['editable','val', 'customUrlsCount','urlsRetainingParentCategoryCount','customIpRangesCount',
    'ipRangesRetainingParentCategoryCount', 'keywords', 'keywordsRetainingParentCategory']

    change_col_names = {'urls':'URLs',
    'dbCategorizedUrls':'Categorized URLs', 
    'customCategory':'Customized Category?',
    'description':'Description',
    'type':'Role Type',
    'configuredName': 'Configured Name',
    'id': 'Categoy ID'}

    return cleanup, change_col_names

def fw_keywords():
    #### Werte anpassen ####
    cleanup = ['adminScopeScopeEntities','email', 'pwdLastModifiedTime', 'name', 'id', 
    'isDeprecatedDefaultAdmin', 'isExecMobileAppEnabled', 'isSecurityReportCommEnabled', 
    'isServiceUpdateCommEnabled', 'isProductUpdateCommEnabled']

    change_col_names = {'loginName':'LoginID',
    'userName':'Name', 
    'role':'Role',
    'type':'Role Type',
    'adminScopeType': 'Scope', 
    'isPasswordLoginAllowed': 'Password Enabled',
    'comments':'Comment', 
    'isDefaultAdmin':'Default Admin',
    'disabled':'Admin Disabled',
    'execMobileAppTokens':'Execute Mobile App Token Enabled'}

    return cleanup, change_col_names