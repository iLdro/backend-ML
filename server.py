import flask
import joblib
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

app = flask.Flask(__name__)

# Charger le modèle et le scaler
reg = joblib.load('random_forest_model.joblib')
scaler = MinMaxScaler()

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/predict', methods=['GET'])
def make_prediction():
    # Récupérer les paramètres de la requête
    weekday = flask.request.args.get('weekday', type=int)
    startingAirport = flask.request.args.get('startingAirport')
    destinationAirport = flask.request.args.get('destinationAirport')
    segmentsAirlineName = flask.request.args.get('segmentsAirlineName')
    segmentsEquipmentDescription = flask.request.args.get('segmentsEquipmentDescription')
    
    # Vérifier que tous les paramètres sont présents
    if not all([weekday, startingAirport, destinationAirport, segmentsAirlineName, segmentsEquipmentDescription]):
        return flask.jsonify({'error': 'Missing parameter(s)'}), 400

    # Effectuer la prédiction
    prediction = predict(weekday, startingAirport, destinationAirport, segmentsAirlineName, segmentsEquipmentDescription)
    return flask.jsonify({'prediction': prediction})

def predict(weekday, startingAirport, destinationAirport, segmentsAirlineName, segmentsEquipmentDescription):
    df = pd.DataFrame({
        'weekday': [weekday],
        'startingAirport': [startingAirport],
        'destinationAirport': [destinationAirport],
        'segmentsAirlineName': [segmentsAirlineName],
        'segmentsEquipmentDescription': [segmentsEquipmentDescription]
    })

    # Normaliser les données
    df['weekday'] = scaler.fit_transform(df[['weekday']])

    # Mapping and Normalizing categorical features
    df['startingAirport'] = df['startingAirport'].apply(lambda x: hash(x) % 1000) / 999.0
    df['destinationAirport'] = df['destinationAirport'].apply(lambda x: hash(x) % 1000) / 999.0
    df['segmentsAirlineName'] = df['segmentsAirlineName'].apply(lambda x: hash(x) % 1000) / 999.0
    df['segmentsEquipmentDescription'] = df['segmentsEquipmentDescription'].apply(lambda x: hash(x) % 1000) / 999.0

    res = reg.predict(df)
    return res[0]*10000

if __name__ == '__main__':
    app.run(debug=True, port=5000)
