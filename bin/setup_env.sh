python -m venv venv
activate(){
    .venv/Scripts/activate
    echo "installing requirements to virtul environment"
    pip install -r requirements.txt
}
activate