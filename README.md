**Install python >= 3.8.10** <br /><br />
**Windows** <br />
https://www.python.org/downloads/ <br />
**Linux** <br />
```
(sudo) apt-get update
(sudo) apt-get upgrade
(sudo) apt-get install python3
```


Optional:
```
mkdir <mydir>
cd <mydir>
```


Then:
```
git clone https://gitlab.devops.telekom.de/zscaler-automation/zscaler-flask-app.git
python3 -m venv my_venv
source ./my_venv/bin/activate
pip3 install -r ./requirements.txt
deactivate #Exit venv
```

