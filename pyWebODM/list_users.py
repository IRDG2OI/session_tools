'''
This Source Code Form is subject to the terms of GPLv3 License
'''
# How to list users in WebODM

import requests, sys, os, glob, json, time
import status_codes
import settings

res = requests.post(settings.SERVER + '/api/token-auth/', 
                    data={'username': settings.USERNAME,
                          'password': settings.PASSWORD}).json()

if 'token' in res:
    print("Successfully Logged-in!")
    token = res['token']

    users = requests.get(settings.SERVER + '/api/admin/users/?page=1', 
                        headers={'Authorization': 'JWT {}'.format(token)}).json()
    print("########")
    print("id", "user")
    print("----------")
    ## Raw out:
### /!\ Need refactor to append pages /!\ ###
#    print(users["next"])
#    print(users["results"])
#    for i in range(users["count"]):
#        try:
#            print(users["results"][i]['id'], users["results"][i]['username'])
#        else:
#            pass
    ## Or list:
    list_users=[]
    for i in range(users["count"]):
       try:
           user = users["results"][i]['id'], users["results"][i]['username']
           list_users.append(user)
       except:
            pass

    if users["next"] != 'null':
        #try:
        pageid = users["next"].split('=')[1]
        users = requests.get(settings.SERVER + '/api/admin/users/?page=' + pageid,
                             headers={'Authorization': 'JWT {}'.format(token)}).json()
        for i in range(users["count"]):
            try:
                user = users["results"][i]['id'], users["results"][i]['username']
                list_users.append(user)
            except:
                pass

    print(list_users)


else:
    print("Invalid credentials!")

