pushd "$elproject_path/server" > /dev/null
source ../.venv/Scripts/activate
flask run --reload
deactivate
popd > /dev/null
