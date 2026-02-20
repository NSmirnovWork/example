mkdir $1
cd $1
python3 -m venv venv
mkdir requirements
touch ./requirements/base.in
touch ./requirements/dev.in
echo "-r base.in\npytest\nruff\npre-commit" > ./requirements/dev.in

source ./venv/bin/activate
pip install pip-compile-multi
pip install uv
