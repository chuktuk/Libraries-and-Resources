# Python Model Deployment

Proof of Concept for Creating, Deploying, and Monitoring an ML model using RStudio Connect and Flask

## call to api from python
import requests<br>
new_data = [[5.0, 3.4, 1.5, 0.2], [7.8, 3.1 , 6.2, 2.4], [7., 3.1, 5.5, 2.2]]<br>
url = 'http://localhost:5000/api/model/predict'<br>
response = requests.post(url, json=new_data)<br>

## call from command line using httpie (must pip install httpie)
http --json POST http://localhost:5000/api/model/predict new_data="[[5.0, 3.4, 1.5, 0.2], [7.8, 3.1 , 6.2, 2.4], [7., 3.1, 5.5, 2.2]]"<br>

## labeling function
http --json POST http://localhost:5000/api/model/label request_data="[{'_id': '60af9cb1760fbd92d06365a6', 'label': 'setosa'}, {'_id': '60af9cb1760fbd92d06365a7', 'label': 'virginica'}, {'_id': '60af9cb1760fbd92d06365a8', 'label': 'virginica'}]"<br>

## get model performance
http --json POST http://localhost:5000/api/model/eval request_data=latest<br>

http --json POST http://localhost:5000/api/model/eval request_data="{'mode': 'all'}"<br>

