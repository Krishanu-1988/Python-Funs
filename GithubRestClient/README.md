# GitHub REST API Client

This python script list all open PRs younger than a given days of a GitHub repo and their corresponding HEAD commit statuses. Currently, below default input params have been used to run the script:<br/>
Repo: **argo-cd**<br/>
Repo owner: **argoproj**<br/>
PRs younger than: **3 days**

**NOTE**<br/>
*secrects.py* should contain the GitHub Personal Access Token in order to connect to GitHub API

**Build Container for this script:**<br/>
Replace the 'latest' tags as per the requirement
```
sudo docker build -t githubpyclient:latest .
```
**Running as Container:**
Running with default input params:
```
docker run githubpyclient
```
Running with given input params:
```
docker run -e REPO_OWNER='flutter' \
-e REPO_NAME='flutter' \
-e PR_AGE=1 \
githubpyclient 
```
**Example Output**
```
docker run -e REPO_OWNER='argoproj' \
-e REPO_NAME='argo-cd' \
-e PR_AGE=1 \
githubpyclient

--------------------Listing filtered PRs--------------------------
Requesting Github API to get PRs:
Response code: 200
- created_at: '2022-04-19T18:36:54Z'
  head: 7db829367be875ae672c3ba2f550ac3b23b16b0c
  number: 9142
  state: open
  title: 'docs: upgrade notes for new RBAC resource in 2.4'
  url: https://api.github.com/repos/argoproj/argo-cd/pulls/9142

------------------------------------------------------------------
-----------------------PR-9142 - Commit Status -------------------------
Requesting Github API to get commit status for the reference: 7db829367be875ae672c3ba2f550ac3b23b16b0c
Response code: 200
state: success
statuses:
- context: security/snyk (Argoproj)
  state: success
  updated_at: '2022-04-19T18:53:16Z'
- context: license/snyk (Argoproj)
  state: success
  updated_at: '2022-04-19T18:53:16Z'
- context: docs/readthedocs.org:argo-cd
  state: success
  updated_at: '2022-04-19T18:54:53Z'

------------------------------------------------------------------
```