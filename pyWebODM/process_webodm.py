'''
This Source Code Form is subject to the terms of the Mozilla 
Public License, v. 2.0. If a copy of the MPL was not 
distributed with this file, You can obtain one at 
https://mozilla.org/MPL/2.0/.
'''

# How to authenticate and process drone images using WebODM
import requests, sys, os, glob, json, time
import status_codes
import settings

if len(sys.argv) < 2:
    print("Usage: ./{} <path_to_images>".format(sys.argv[0]))
    sys.exit(1)

# Get folder name before DCIM folder
path = os.path.normpath(sys.argv[1])
input = path.split(os.sep)[-2]

# List images files (png for masks)
types = ("*.jpg", "*.jpeg", "*.JPG", "*.JPEG", "*.png", "*.PNG")
images_list = []
for t in types:
    images_list.extend(glob.glob(os.path.join(sys.argv[1], t)))

if len(images_list) < 2:
    print("Need at least 2 images")
    sys.exit(1)
else:
    print("Found {} images".format(len(images_list)))

res = requests.post(settings.SERVER + '/api/token-auth/', 
                    data={'username': settings.USERNAME,
                          'password': settings.PASSWORD}).json()

if 'token' in res:
    print("Logged-in!")
    token = res['token']

    res = requests.post(settings.SERVER + '/api/projects/', 
                        headers={'Authorization': 'JWT {}'.format(token)},
                        data={'name': 'PyWebODM - ' + input }).json()
    if 'id' in res:
        print("Created project: {}".format(res)) 
        project_id = res['id']

        images = [('images', (os.path.basename(file), open(file, 'rb'), 'image/jpg')) for file in images_list]
        options = json.dumps([
            {'name': "orthophoto-resolution", 'value': 1},
            {'name': "auto-boundary", 'value': True},
            {'name': "auto-boundary-distance", 'value': 50},
            {'name': "camera-lens", 'value': 'brown'},
            {'name': "crop", 'value': '0'},
            {'name': "dem-resolution", 'value': '2.0'},
            {'name': "dsm", 'value': True},
            {'name': "ignore-gsd", 'value': True},
            {"name": "pc-quality", "value": 'high'},
            # {'name': "resize_to", 'value': 2048},
            {'name': "rolling-shutter", 'value': True},
            {'name': "rolling-shutter-readout", 'value': 56},
            {'name': "use-fixed-camera-params", 'value': True}
        ])
        res = requests.post(settings.SERVER + '/api/projects/{}/tasks/'.format(project_id), 
                    headers={'Authorization': 'JWT {}'.format(token)},
                    files=images,
                    data={
                        'options': options
                    }).json()

        print("Created task: {}".format(res))
        task_id = res['id']
        
        # Change task name to folder name: same as project name
        requests.patch(settings.SERVER + '/api/projects/{}/tasks/{}/'.format(project_id, task_id),
                        headers={'Authorization': 'JWT {}'.format(token)},
                        data={'name': input }).json()

        while True:
            time.sleep(3)
            res = requests.get(settings.SERVER + '/api/projects/{}/tasks/{}/'.format(project_id, task_id), 
                        headers={'Authorization': 'JWT {}'.format(token)}).json()
            
            if res['status'] == status_codes.COMPLETED:
                print("Task has completed!")
                break
            elif res['status'] == status_codes.FAILED:
                print("Task failed: {}".format(res))
                # print("Cleaning up...")
                print("No results: bad dataset or bad processing options")
                #requests.delete(settings.SERVER + "/api/projects/{}/".format(project_id), 
                #    headers={'Authorization': 'JWT {}'.format(token)})
                print("Data kept on platform, please check on web interface: "+ settings.SERVER)
                sys.exit(1)
            else:
                seconds = res['processing_time'] / 1000
                if seconds < 0: 
                    seconds = 0
                m, s = divmod(seconds, 60)
                h, m = divmod(m, 60)
                sys.stdout.write("\rProcessing... [%02d:%02d:%02d]" % (h, m, s))
                sys.stdout.flush()

        res = requests.get(settings.SERVER + "/api/projects/{}/tasks/{}/download/orthophoto.tif".format(project_id, task_id), 
                        headers={'Authorization': 'JWT {}'.format(token)},
                        stream=True)
        with open("orthophoto.tif", 'wb') as f:
            for chunk in res.iter_content(chunk_size=1024): 
                if chunk:
                    f.write(chunk)

        file_newname = "ortho_" + input + ".tif"
        os.rename("orthophoto.tif", file_newname)
        print("Saved " + file_newname)

        # print("Cleaning up...")
        # requests.delete(settings.SERVER + "/api/projects/{}/".format(project_id), 
        #                headers={'Authorization': 'JWT {}'.format(token)})
    else:
        print("Cannot create project: {}".format(res))
else:
    print("Invalid credentials!")

