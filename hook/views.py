#from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

import os
import hmac
import hashlib
from dotenv import load_dotenv
load_dotenv()

import git
import subprocess
import sys

### Github integration

@require_POST
@csrf_exempt
def update_server(request):

    #Load non-public variables

	w_secret = os.environ['WEBHOOK_SECRET']
	requirements_command = os.environ['BASH_REQ_COMMAND']
	reload_command = os.environ['BASH_REL_COMMAND']
	x_hub_signature = request.headers.get('X-Hub-Signature')

	#Verify the request signature

	if x_hub_signature is None:
	    print('Permission denied.')
	    return HttpResponseForbidden('Permission denied.')

	elif not is_valid_signature(x_hub_signature, request.body, w_secret):
	    print('Deploy signature failed.')
	    return HttpResponse('Unauthorized secret key.', status=401)

	elif is_valid_signature(x_hub_signature, request.body, w_secret):
	    print('Deploy signature worked')

    #Pull up-to-date repository from github

	    git_pull()

	#Install new requirements from requirements.txt (WATCH OUT this command is heavily hard-coded)

	    subprocess.check_call(requirements_command, shell=True, executable='/bin/bash')

	    subprocess.check_call(reload_command, shell=True, executable='/bin/bash')

        # > /home/kubabartosiewicz/baltic/log.txt 2>&1

	    return HttpResponse('Webhook reached and update pulled.')

	return HttpResponse('Done.')

def is_valid_signature(x_hub_signature, body, private_key):

    hash_algorithm, github_signature = x_hub_signature.split('=', 1)
    algorithm = hashlib.__dict__.get(hash_algorithm)
    encoded_key = bytes(private_key, 'latin-1')
    mac = hmac.new(encoded_key, msg=body, digestmod=algorithm)

    return hmac.compare_digest(mac.hexdigest(), github_signature)

def git_pull():

	path = os.getcwd()
	print(path)
	repo = git.Repo(path)
	origin = repo.remotes.origin

	origin.pull()
