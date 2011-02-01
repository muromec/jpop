# $Id:$

clean:
	-rm -rf *~*
	-find . -name '*.pyc' -exec rm {} \;

run_server:
	bin/python spydaap.py

run_scanner:
	bin/python scan.py

install:
	virtualenv --no-site-packages .
	bin/pip install -r requirements.txt

drop_env:
	rm -r bin/ include/ lib/

reinstall: drop_env install
