#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask

app = Flask(__name__,
 	static_folder = './public',
 	template_folder="./static")

from .views import hello_blueprint
app.register_blueprint(hello_blueprint)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 3000), debug=True)