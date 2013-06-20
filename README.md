Install:
---------

	virtualenv --distribute --no-site-packages ve
	source ve/bin/ activate
    pip install -r requirements.txt -i http://pypi.urlab.be/simple
    ./manage.py syncdb