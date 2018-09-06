import os
from github import Github
from github import GithubException


GITHUB_API = 'api.github.com'
GITHUB_OWNER = 'mozilla-services'
#GITHUB_OWNER = 'rpappalax'
GITHUB_REPO = 'shavar-test-lists'

if os.environ['GITHUB_ACCESS_TOKEN']:
    GITHUB_ACCESS_TOKEN = os.environ['GITHUB_ACCESS_TOKEN']
else:
    GITHUB_ACCESS_TOKEN = ''


class JSONItemNotFoundException(Exception):
    """Item not found in JSON error"""


def github_repo():
    gh = Github(login_or_token=GITHUB_ACCESS_TOKEN,
                base_url='https://{0}'.format(GITHUB_API))

    try:
        my_name = gh.get_user().name
        print(my_name)
    except GithubException:
        print("Error: Authentication failed. Exiting...")
        exit(1)

    return gh.get_user().get_repo(GITHUB_REPO)


def json_update(repo, dest, message, decoded_json_new, json_file):
    return repo.update_file('/{0}'.format(dest),
                            message,
                            decoded_json_new,
                            json_file.sha)


def json_contents(repo, src):
    json_file_new = repo.get_file_contents(src)
    return json_file_new.decoded_content.decode('UTF-8')


def json_overwrite(repo, dest_name, new_contents,  message):
    """Write out contents_new to the file: dest_name"""
    json_file = repo.get_file_contents('/{0}'.format(dest_name))
    return json_update(repo, dest_name, message, new_contents, json_file)


if __name__ == '__main__':

    repo = github_repo()

    # ------------------------------------------------------------
    # TRACKWHITE
    # ------------------------------------------------------------

    new_name = 'trackwhite.json.EDITED'
    original_name = 'trackwhite.json'

    # save original contents for restore operation
    original_contents = json_contents(repo, original_name)

    # SETUP
    message = 'test: setup json for whitelist test'
    new_contents = json_contents(repo, new_name)
    resp = json_overwrite(repo, original_name, new_contents, message)
    print(resp)

    # RESTORE
    message = 'test: revert json for whitelist test'
    resp = json_overwrite(repo, original_name, original_contents, message)
    print(resp)

    # ------------------------------------------------------------
    # TRACK
    # ------------------------------------------------------------

    new_name = 'track.json.EDITED'
    original_name = 'track.json'

    # save original contents for restore operation
    original_contents = json_contents(repo, original_name)

    # SETUP
    message = 'test: setup json for blacklist test'
    new_contents = json_contents(repo, new_name)
    resp = json_overwrite(repo, original_name, new_contents, message)
    print(resp)

    # RESTORE
    message = 'test: revert json for blacklist test'
    resp = json_overwrite(repo, original_name, original_contents, message)
    print(resp)
