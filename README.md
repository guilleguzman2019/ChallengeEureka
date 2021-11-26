#Python Flask api-rest

 Simple ejemplo de python flask que usa sqlite
 

 
### Instalacion (for windows)

Abrir la terminal donde quiera alojar el proyecto.


```
git clone https://github.com/gurkanakdeniz/example-flask-crud.git
```
```
cd example-flask-crud/
```
```
python3 -m venv venv
```
```
source venv/bin/activate
```
```
pip install --upgrade pip
```
```
pip install -r requirements.txt
```
```
export FLASK_APP=crudapp.py
```
```
flask db init
```
```
flask db migrate -m "entries table"
```
```
flask db upgrade
```
```
flask run
```

Una vez obtenida la clave-key accede al sercicio con:

http://127.0.0.1:5000/price?symbol={}&key={}

symbols disponibles: FB, AAPL, MSFT, GOOGL, AMZN

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
