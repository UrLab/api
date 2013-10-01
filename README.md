UrLab/api est une API web pour gérer le hackerspace.
Elle permettra de récupérer plein d'infos sur le status physique du hackerspace et lui fournir des ordres (domotique)

UrLab/api est fortement lié à UrLab/hal qui sera le contrôleur (surement un arduino relié à un RPi) qui exécutera les ordres de l'api et qui lui renverra des données

Install:
---------

	virtualenv --distribute --no-site-packages ve
	source ve/bin/ activate
    pip install -r requirements.txt -i http://pypi.urlab.be/simple
    ./manage.py syncdb