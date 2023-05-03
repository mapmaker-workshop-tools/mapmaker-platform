![mapmaker_logo](https://user-images.githubusercontent.com/71013416/235667781-5f015188-a834-4409-be82-df9ca07680ed.png)


[![📈 Autoscale](https://github.com/two-trick-pony-NL/mapmaker/actions/workflows/autoscale.yml/badge.svg?branch=master)](https://github.com/two-trick-pony-NL/mapmaker/actions/workflows/autoscale.yml)
[![🚀 Production deployment](https://github.com/two-trick-pony-NL/mapmaker/actions/workflows/productiondeploy.yml/badge.svg)](https://github.com/two-trick-pony-NL/mapmaker/actions/workflows/productiondeploy.yml)
[![License: CC BY-NC-ND 4.0](https://img.shields.io/badge/License-CC_BY--NC--ND_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-nd/4.0/)
![Response time](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fupptime%2Fupptime%2Fmaster%2Fapi%2Fgoogle%2Fresponse-time.json)
![Uptime](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fupptime%2Fupptime%2Fmaster%2Fapi%2Fgoogle%2Fuptime.json)


<img width="1613" alt="Schermafbeelding 2023-04-25 om 19 31 58" src="https://user-images.githubusercontent.com/71013416/234356599-8273b213-1533-49d1-abf3-1c6fd0315caf.png">

<img width="1305" alt="Schermafbeelding 2023-04-25 om 19 34 44" src="https://user-images.githubusercontent.com/71013416/234357045-882da973-53bc-4dfc-973b-b2f5fcc49ff2.png">

# Mapmaker
Mapmaker is a workshop platform consisting of a unique cardset, a methodology and a online collaboration platform.
This repository contains all the assets, instructions and the cardset designs. For more information visit: mapmaker.nl

### Learn more
#### About our offering
This page on Github is meant to share our workshop materials and document issues. If you want to learn more about our offering check out our  [Website](https://mapmaker.nl).


#### About the code
We documented the code of the platform in this repository under 'src'. For more information check out this  [README](https://github.com/two-trick-pony-NL/mapmaker/tree/master/src)


# Open Source and Creative Commons
The collection of works are published on Github and under the BY-NC-ND creative commons license.  This is because we value transparency, as well as want others to benefit from our work. This means you'll be able to host your own sessions using the materials, code and methodology we developed. Restrictions do apply: we do not permit: using the works for commercial purposes, redistribution and modification. If you do want to use these materials send us a message at mapmaker.nl/contact to work out a license agreement.

#### How does Creative commons work?
=======
![banner](https://user-images.githubusercontent.com/71013416/235923153-98dfe26f-e4b1-4577-bed3-493384429f4b.png)

# Mapmaker -- Platform
Mapmaker is the online platform for the Mapmaker methodology. We open sourced the project so we can be transparant on what we do. It also allows you to run the platform on your own hardware if you choose to do so. 

## TL:DR:
- Our [platform](https://mapmaker.nl) -- and our homepage 
- Our development [platform](https://triage.mapmaker.nl) -- for testing new versions
- Upptime status [platform](https://status.mapmaker.nl) -- Is our server up or down

## Help I can't code: is there a way to use the platform without knowing how to code?
Yes definetly drop us a [message](https://mapmaker.nl/contact) and we'll work something out. We use our version of the platform for all our workshops and it runs very smooth.  

## I'm a developer - How do I run the code? 
Great to hear! Easy: the project is a fairly typical Django project. This means that all you need to do is:
1. clone the repository
2. Create a .env file in src/core with parameters for your Django server to run: here is an example:

```
#Email settings
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
#Django settings
DJANGO_SECRET_KEY=
DEBUG=False
# S3 storage keys
S3_AWS_STORAGE_BUCKET_NAME=
S3_ACCESS_KEY=
S3_SECRET_KEY=
# For creating images -- These help you generate a image of the workshop
HCTI_API_KEY=
HCTI_API_USER_ID=

#Analytics
MIXPANEL_TOKEN=
ENVIRONMENT=

# DEV DATABASE
DB_NAME=
DB_USER=
DB_HOST=
DB_PASSWORD=
DB_PORT=3306
```

3. From here it should be smooth sailing and you should be able to run all the typical Django commands such as: 
`python src/manage.py runserver`
or
`python src/manage.py makemigrations` or `python src/manage.py migrate` for migrations
4. The repository also includes workflows to deploy to production. This requires you also have a Lightsail account with the correct names. 

# How to contribute:
If you want to add features or fix bugs then by all means open a pullrequest for us to review your code. 


# License, Open Source and Creative Commons
The collection of works are published on Github and under the BY-NC-ND creative commons license.  This is because we value transparency, as well as want others to benefit from our work. This means you'll be able to host your own sessions using the materials, code and methodology we developed. Restrictions do apply: we do not permit: using the works for commercial purposes, redistribution and modification. If you do want to use these materials send us a [message](https://mapmaker.nl/contact) to work out a license agreement.
