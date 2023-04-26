# The code platform
This is the mapmaker code platform. It runs on Django (Python), through Dockercontainers hosted on AWS. The project heavily relies on HTMX and Django Templating. Other than that most Django conventions are followed, splitting the site up over several sub-apps.

# Deployment
We run 2 environments of mapmaker. A triage and production version. The triage version is updated after each codecommit and serves to test usability changes and check for any breaking changes. If the code is pushed to Triage succesfully a pull request is automatically opened on Github, if that request is merged the triage version will move to production.

# Dependancies and dockerasation: and infra as code
All to run this application is contained within the repository. There are several dockerfiles and AWS Settings files in the infrastructure folder. The Github Actions pipeline can dockerize all the code, install the dependancies and then host the containers on AWS Lightsail.

# Loadbalancing
AWS Lightsail does a pretty good job at keeping loads low. Under regular load the containers should not consume more than 10% of resources. Despite this there is a github action that runs every 5 minutes with the power to do autoscaling. It is running but not making any changes to the production environment to see how it performs.

# Databases
We host 2 databases at Kaashosting one for prod and one for development. These are regular MYSQL databases.

# Constructing pages
In Django convention we use a base.html template that contains all the scripts and styling. With the django templating engine we swap in the content necassary for the pages.
for styling we use Tailwind using a dedicated tailwind/django module.

# Secrets and ENV variables:
All of them are set through the github secrets in the workflows.
