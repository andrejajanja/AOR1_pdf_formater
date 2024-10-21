if [ ! -d "temp_files" ]; then
    echo "Created directory for temp files"
    mkdir temp_files  
fi
source ./formater_venv/bin/activate
python3 ./generator/__init__.py
deactivate
rm -rf ./temp_files