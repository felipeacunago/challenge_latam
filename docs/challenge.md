# Documentation

This file is not intended to be a proper documentation, I just try to give a little explanation of why I did things the way I did it and give a little of context.

### Part I

Model was made by completing the missing functions. In the instruction it's asked to argue what model to pick and why. The answer is:

I picked LogisticRegression because of the following reasons:
- It's stated that there's no noticeable difference in results between XGBoost and LogisticRegression
- It allows me to not install additional libraries
- LogisticRegression is easier to explain to the business

### Part II

Validation for the input was done using pydantic. The code would be a little cleaner if everything related to pydantic models was on a separate file, but I didn't do it that way because I didn't want to modify the structure of the challenge.

### Part III & Part IV

#### Docker

Docker image has a pretrained model saved. This is not a very good practice as the service should be able to load it dynamically from an external source in case there's need for updating the model parameters. This could be implemented easily using GCS, but as it wasn't required and I didn't want to make this more complex I did it this way.

#### Google Cloud Platform

GCP was picked as I'm more familiar with the suite. CI/CD was implemented by relying on a service account with these permissions:

```bash
ROLE: roles/artifactregistry.admin
ROLE: roles/cloudbuild.builds.editor
ROLE: roles/cloudbuild.serviceAgent
ROLE: roles/iam.serviceAccountUser
ROLE: roles/run.admin
ROLE: roles/serviceusage.serviceUsageConsumer
ROLE: roles/storage.objectAdmin
```

The following Repository Secrets were set, so they can be called using secrets.VARIABLE_NAME :

```
GCP_CREDENTIALS: service key account JSON key
PROJECT_ID: GCP project_id
SERVICE_NAME: Cloud Run service name
SERVICE_REGION: Region
```
It's done this way so there's no sensitive information hardcoded in the CI/CD files.

#### Workflow
To be honest I'm 100% sure of what is the good practice using gitflow + CI/CD, and it depends on the team. It was done in this way:

- CI: It's a simple linting+pytest process and it's triggered on any push on the develop and feature branches:
```yml
on:
  push:
    branches:
      - develop
      - 'feature/**'

    ...
```
- CD: It's a test+deploy process (test job must be successful) triggered on any push/pull request of the main branch:
```yml
on:
  push:
    branches: [ "main" ]

jobs:
  test:
    ...
  deploy:
    needs: test
```

#### Makefile
Makefile doesn't have the API url as I don't want to expose it in the public repository.