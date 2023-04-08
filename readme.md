[![🏗 Build and deploy containers to AWS](https://github.com/two-trick-pony-NL/mapmaker/actions/workflows/deploy.yml/badge.svg)](https://github.com/two-trick-pony-NL/mapmaker/actions/workflows/deploy.yml)
![logo](https://user-images.githubusercontent.com/71013416/223648375-3462132b-9e69-4ce6-b8d6-3ace8256adbd.png)

# Mapmaker
Mapmaker saves your workshop when the physical session is over
![demo](https://user-images.githubusercontent.com/71013416/223648277-8662e657-6e8e-42ae-b34f-c9070de68917.jpeg)

# How to run: 
- Install dependancies pip install -r requirements.txt
- on DEV `python3 src/manage.py runserver`
- on PROD `gunicorn-b 0.0.0.0:8000 core.wsgi`

# License:
![by-nc-nd](https://user-images.githubusercontent.com/71013416/230729888-010487e6-f7ea-4a55-9ae8-ea670e57e7a0.png)
