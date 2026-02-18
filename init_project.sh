mkdir $1
cd $1
python3 -m venv venv
mkdir requirements
touch ./base.in
touch ./dev.in
echo "pytest\nruff\pre-commit" > ./dev.in

source ./venv/bin/activate
pip install pip-compile-multi
pip install uv
