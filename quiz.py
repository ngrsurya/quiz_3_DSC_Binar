from flask import Flask, jsonify, request #import objects from the Flask model
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from

import re
app = Flask(__name__) #define app using Flask
app.json_encoder = LazyJSONEncoder


swagger_template = dict(
    info = {
        'title': LazyString(lambda:'API Documentation for QUIZ 3 Binar Language API'),
        'version': LazyString(lambda:'1.0.0'),
        'description': LazyString(lambda:'Dokumentasi API untuk Data Processing dan Modeling')
        }, host = LazyString(lambda: request.host)
    )

swagger_config = {
        "headers":[],
        "specs":[
            {
            "endpoint":'docs',
            "route":'/docs.json'
            }
        ],
        "static_url_path":"/flasgger_static",
        "swagger_ui":True,
        "specs_route":"/docs/"
    }
swagger = Swagger(app, template=swagger_template, config=swagger_config)

languages = [{'name' : 'JavaScript'}, {'name' : 'Python'}, {'name' : 'Ruby'}]

@swag_from("docs/get.yml", methods=['GET'])
@app.route('/', methods=['GET'])
def test():
    return jsonify({'message' : 'It works!'})

@swag_from("docs/lang.yml", methods=['GET'])
@app.route('/lang', methods=['GET'])
def returnAll():
    return jsonify({'languages' : languages})


@swag_from("docs/lang_get.yml", methods=['GET'])
@app.route('/lang/<string:name>', methods=['GET'])
def returnOne(name):
    langs = [language for language in languages if language['name'] == name]
    return jsonify({'language' : langs[0]})

@swag_from("docs/lang_post.yml", methods=['POST'])
@app.route('/lang', methods=['POST'])
def addOne():
    name = request.form.get('name')
    language = {'name' : name}
    languages.append(language)
    return jsonify({'languages' : languages})

@swag_from("docs/lang_put.yml", methods=['PUT'])
@app.route('/lang/<string:name>', methods=['PUT'])
def editOne(name):
    nameToChange = request.form.get('nameToChange')
    langs = [language for language in languages if language['name'] == name]
    langs[0]['name'] = nameToChange
    return jsonify({'language' : langs[0]})

@swag_from("docs/lang_delete.yml", methods=['DELETE'])
@app.route('/lang/<string:name>', methods=['DELETE','POST'])
def removeOne(name):
    lang = [language for language in languages if language['name'] == name]
    languages.remove(lang[0])
    return jsonify({'languages' : languages})

if __name__ == '__main__':
    app.run() #run app on port 8080 in debug mode