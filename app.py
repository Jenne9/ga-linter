from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import yaml
import os

app = Flask(__name__)
CORS(app)

# Chemin absolu du fichier YAML contenant la liste des tâches
DATA_FILE = "data/todolist.yaml"
absolute_path = os.path.abspath(DATA_FILE)

# Vérifie si le fichier existe, le créer s'il n'existe pas, sinon il charge le fichier des tâches
        def load_todolist():
            try:
                with open(DATA_FILE, 'r') as file:
                    todo_list = yaml.safe_load(file)
                    if todo_list is None:
                        return []
                    else:
                        return todo_list
            except FileNotFoundError:
                return []

# Sauvegarde la liste des tâches dans le fichier YAML
def save_todolist(todo_list):
    with open(DATA_FILE, 'w') as file:
        yaml.dump(todo_list, file)

# Obtient la liste complète des tâches
@app.route('/getall')
@cross_origin()
def get_todolist():
    todo_list = load_todolist()
    return jsonify(todo_list)

# Charge la liste des tâches, vérifie si l'ID existe, change son statut à DONE et renvoie la liste mise à jour
@app.route('/done/<int:todo_id>', methods=['POST'])
def set_done(todo_id):
    todo_list = load_todolist()
    if todo_id >= 0 and todo_id < len(todo_list):
        todo_list[todo_id]['status'] = 'DONE'
        save_todolist(todo_list)
        return '', 204
    else:
        return 'Invalid todo ID', 400

# Récupère les données du front, charge la liste des tâches, ajoute la nouvelle tâche et sauvegarde la liste
@app.route('/new', methods=['POST'])
@cross_origin()
def add_todo():
    todo_data = request.json
    todo_list = load_todolist()
    todo_list.append(
        {'date': todo_data['date'], 'name': todo_data['name'], 'description': todo_data['description'], 'status': 'TODO'})
    save_todolist(todo_list)
    return '', 204


@app.route('/healthz')
def healthz():
    return jsonify(status="OK")

@app.route('/readiness')
def readiness():
    return jsonify(status="OK")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)







