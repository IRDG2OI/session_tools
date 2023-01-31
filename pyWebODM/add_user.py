'''
This Source Code Form is subject to the terms of GPLv3 License
'''
# How to add users to WebODM

import requests, sys, os, glob, json, time
import status_codes
import settings

res = requests.post(settings.SERVER + '/api/token-auth/', 
                    data={'username': settings.USERNAME,
                          'password': settings.PASSWORD}).json()

if 'token' in res:
    print("Successfully logged-in !")
    token = res['token']
    
    print("Put user information below, fieds with '*' are mandadory")
    username = input("Username*: ")
    first_name = input("First Name: ")
    last_name = input("Last Name*: ")
    password = input("Password*: ")
    group = input("Groups* (e.g: 1, 2): ")
    permission = input("User permissions* (e.g: 1, 2, 3): ")
    email = input("email: ")
    res = requests.post(settings.SERVER + '/api/admin/users/', 
                        headers={'Authorization': 'JWT {}'.format(token)},
                        data={'username': username,
                              'first_name': first_name,
                              'last_name': last_name,
                              'password': password,
                              'groups': group.split(','),
                              'user_permissions': permission.split(','),
                              'email': email,
                              'is_active': 'True'
                              }).json()
    res
    
else:
    print("Invalid credentials!")

