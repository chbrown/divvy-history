import os
import glob
import requests
import base64
from pprint import pprint
from hashlib import sha1

github_token = os.environ['GITHUB_TOKEN']
headers = {'Authorization': 'token %s' % github_token}
api_root = 'https://api.github.com'
# github_name = os.environ['GITHUB_NAME']
# github_email = os.environ['GITHUB_EMAIL']
repo = dict(owner='chbrown', repo='divvy-history', branch='dates')


def api(url, method='GET', **params):
    return requests.request(method, api_root + url, headers=headers, params=params)


def push():
    # repo = gh.get_repo('chbrown/divvy-history')
    for filename in glob.glob('*/**.json'):
        file_size = os.path.getsize(filename)
        with open(filename) as fp:
            file_data = fp.read()
        file_sha = sha1('blob ' + file_size + '\0' + file_data)

        url = '/repos/{owner}/{repo}/contents/{path}'.format(path=filename, **repo)
        r = api(url, 'GET')

        # upload the file
        file_data_base64 = base64.b64encode(file_data)

        # PUT /repos/:owner/:repo/contents/:path
        url = '/repos/{owner}/{repo}/contents/{path}'.format(path=filename, **repo)
        message = ''
        params = {
            'message': message,
            'content': file_data_base64,
            # 'author.name': github_name,
            # 'author.email': github_email
        }

        if r.status_code != 404:
            # if the file already exists, we must update it by also providing the previous sha
            params['sha'] = r['sha']

        r = api(url, 'PUT', **params)
        pprint(r.headers)
        pprint(r.text)



            # Optional Parameters

            # The author section is optional and is filled in with the committer information if omitted. If the committer information is omitted, the authenticated user’s information is used.

            # You must provide values for both name and email, whether you choose to use author or committer. Otherwise, you’ll receive a 500 status code.

            # author.name
            #     string - The name of the author of the commit
            # author.email
            #     string - The email of the author of the commit
            # committer.name
            #     string - The name of the committer of the commit
            # committer.email
            #     string - The email of the committer of the commit


        # if r.headers.status.
        # try:
            # contents = repo.get_contents()
        # except UnknownObjectException:

        # git commit -a -m "epoch=`date +%s`"
        # git push

        # push_file(filename)
        # pprint(r.json())


def api_print(url, method='GET', **params):
    response = api(url, method, **params)

    pprint(response.json())
    return

# api_print('/user')
# api_print('/user/emails')
# api_print('/users/dssg')
# api_print('/users/shirini721')
# api_print('/users/chbrown/events/orgs/dssg')
# api_print('/repos/chbrown/sv/issues', state='closed')
# api_print('/repos/dssg/dssg-twitter-disaster/issues', state='open')
# api_print('/user/issues')
# /orgs/dssg/members

if __name__ == '__main__':
    push()
