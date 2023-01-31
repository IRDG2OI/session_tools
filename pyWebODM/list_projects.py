'''
This Source Code Form is subject to the terms of GPLv3 License
'''
# How to list projects in WebODM

import requests, sys, os, glob, json, time
import status_codes
import settings

user = 'my_user'

res = requests.post(settings.SERVER + '/api/token-auth/', 
                    data={'username': settings.USERNAME,
                          'password': settings.PASSWORD}).json()

if 'token' in res:
    print("Successfully Logged-in!")
    token = res['token']

    projects = requests.get(settings.SERVER + '/api/projects/', 
                        headers={'Authorization': 'JWT {}'.format(token)}).json()
    print("########")
    print("id", "name", "permissions")
    print("----------")
    ## Raw out:
    proj_id = []
    for i in range(len(projects)):
        proj_id.append(projects[i]['id'])
        print(projects[i]['id'], projects[i]['name'])
    ## Or list:
    #list_projects=[]
    #for i in range(projects["count"]):
    #   project = projects[i]['id'], projects[i]['name']
    #   list_projects.append(project)
    #print(list_projects)
    
    # WIP Update new users to view all projects
    # for i in proj_id:
    #     perm_proj = requests.post(settings.SERVER + '/api/projects/{}/permissions/'.format(i), 
    #                         headers={'Authorization': 'JWT {}'.format(token)},
    #                         data={
    #                             'username': user, 'owner': False, 'permissions': ['view']
    #                         }).json()
    #     print("Update project " + proj_id)
    #     proj_updated = requests.get(settings.SERVER + '/api/projects/{}/permissions/'.format(i), 
    #                         headers={'Authorization': 'JWT {}'.format(token)}).json()
    #     print(proj_updated)
    
 
else:
    print("Invalid credentials!")
