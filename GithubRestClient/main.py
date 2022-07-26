# ++++++++++++++++++++ GitHub REST API Client ++++++++++++++++++++
import sys
import os
import requests as req
import json
import datetime as dt
import yaml
from secrets import GITHUB_TOKEN

# Global variables
github_base_url = "https://api.github.com"


# ------------------ Functions for GitHub API calls -------------------------
# This function lists all Open PRs younger than given days for the given repo and the given owner
def get_open_prs(owner: str, repo: str, age: int):
    current_time = dt.datetime.utcnow()  # As GitHub returns the dates with 'Z' zeroth timezone - UTC
    aged_date_limit = current_time - dt.timedelta(days=age)
    query_url = f"{github_base_url}/repos/{owner}/{repo}/pulls"
    params_dict = {
        "state": "open"
    }
    headers_dict = {
        "Content-Type": "application/json",
        "Authorization": GITHUB_TOKEN
    }

    print("Requesting Github API to get PRs:")
    resp_json = req.get(url=query_url, params=params_dict, headers=headers_dict)
    print(f"Response code: {resp_json.status_code}")
    resp_json_list = json.loads(resp_json.content)

    filtered_pr_list = []
    for pr_dict in resp_json_list:
        pr_created_date = dt.datetime.strptime(pr_dict.get("created_at"), "%Y-%m-%dT%H:%M:%S%z").replace(tzinfo=None)
        if pr_created_date > aged_date_limit:
            filtered_pr_dict = {
                "number": "",
                "url": "",
                "title": "",
                "state": "",
                "created_at": "",
                "head": ""
            }
            for key in filtered_pr_dict.keys():
                if key == "head":
                    filtered_pr_dict.update({key: pr_dict.get(key).get("sha")})
                else:
                    filtered_pr_dict.update({key: pr_dict.get(key)})
            # print("-------------------------------------------------------------------")
            # print(filtered_pr_dict)
            # print("-------------------------------------------------------------------")
            filtered_pr_list.append(filtered_pr_dict)
    print(yaml.dump(filtered_pr_list))
    return filtered_pr_list


# This function returns all commit statuses of the given reference of  given repo and the given owner
def get_commit_status(owner: str, repo: str, ref: str):
    ref_commit_status_dict = {}
    query_url = f"{github_base_url}/repos/{owner}/{repo}/commits/{ref}/status"
    headers_dict = {
        "Content-Type": "application/json",
        "Authorization": GITHUB_TOKEN
    }
    print(f"Requesting Github API to get commit status for the reference: {ref}")
    resp_json = req.get(url=query_url, headers=headers_dict)
    print(f"Response code: {resp_json.status_code}")
    resp_json_dict = json.loads(resp_json.content)

    # Update required commit_status_dict keys and values from response json of GitHub API call
    ref_commit_status_dict.update({"state": resp_json_dict.get("state")})
    commit_status_list = []
    for commit_status in resp_json_dict.get("statuses"):
        required_commit_status_dict = {
            "state": "",
            "context": "",
            "updated_at": ""
        }
        for key in required_commit_status_dict.keys():
            required_commit_status_dict.update({key: commit_status.get(key)})
        commit_status_list.append(required_commit_status_dict)
    ref_commit_status_dict.update({"statuses": commit_status_list})
    return yaml.dump(ref_commit_status_dict)


# ------------------ Main function ------------------
def main():
    # Considering default repo_owner as 'argoproj' if not provided through environment variable - REPO_OWNER
    repo_owner = ({True: os.getenv('REPO_OWNER'), False: 'argoproj'}[os.getenv('REPO_OWNER') is not None])
    # Considering default repo_name as 'argo-cd' if not provided through environment variable - REPO_NAME
    repo_name = ({True: os.getenv('REPO_NAME'), False: 'argo-cd'}[os.getenv('REPO_NAME') is not None])
    # Considering default PR age as 3 if not provided through environment variable - PR_AGE
    pr_age = ({True: int(os.getenv('PR_AGE')), False: 3}[os.getenv('PR_AGE') is not None])

    try:
        print("--------------------Listing filtered PRs--------------------------")
        pr_list = get_open_prs(repo_owner, repo_name, pr_age)
        print("------------------------------------------------------------------")
    except req.exceptions.RequestException as req_err:
        print(f"Error while making request to the GitHub REST API url. Details: {str(req_err)}")
        sys.exit(1)
    except ValueError as err:
        print(f"Error while converting the GitHub API response into JSON objects. Details: {str(err)}")
        sys.exit(1)
    for pr in pr_list:
        try:
            print(f"-----------------------PR-{pr.get('number')} - Commit Status -------------------------")
            print(get_commit_status(repo_owner, repo_name, pr.get("head")))
            print("------------------------------------------------------------------")
        except Exception as exp:
            print(f"Error while making request to the GitHub REST API url. Details: {str(exp)}")
            print(f"Skipping PR-{pr.get('number')} and continue with the next PR")
            continue


if __name__ == '__main__':
    main()
