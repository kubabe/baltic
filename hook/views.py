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

### Github integration

@require_POST
@csrf_exempt
def update_server(request):

    #Verify the request signature

	w_secret = os.environ['WEBHOOK_SECRET']
	x_hub_signature = request.headers.get('X-Hub-Signature')

	if x_hub_signature is None:
	    print('Permission denied.')
	    return HttpResponseForbidden('Permission denied.')

	elif not is_valid_signature(x_hub_signature, request.body, w_secret):
	    print('Deploy signature failed.')
	    return HttpResponse('Unauthorized secret key.', status=401)

	elif is_valid_signature(x_hub_signature, request.body, w_secret):
	    print('Deploy signature worked')

	    git_pull()

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
