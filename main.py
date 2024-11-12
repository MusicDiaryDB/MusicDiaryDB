from typing import Any
from flask import Flask, render_template, jsonify
from flask_cors import CORS

from helpers import execute_query
from helpers import (
    handle_request,
    delete_resource_with_multiple_keys,
    # update_resource_with_multiple_keys,
)

# import routes defined in other files
from routes.admin import bp as admin_routes
from routes.song import bp as song_routes
from routes.user import bp as user_routes
from routes.review import bp as review_routes
from routes.diaryreport import bp as report_routes
from routes.album import bp as album_routes
from routes.artist import bp as artist_routes
from routes.entry import bp as entry_routes
from routes.platform import bp as platform_routes
from routes.platformsongs import bp as platform_song_routes
from routes.aggregation import bp as aggregation_routes

app = Flask(__name__)
CORS(app)

#
# register endpoints defind in other files
#
app.register_blueprint(admin_routes)
app.register_blueprint(song_routes)
app.register_blueprint(user_routes)
app.register_blueprint(review_routes)
app.register_blueprint(report_routes)
app.register_blueprint(album_routes)
app.register_blueprint(artist_routes)
app.register_blueprint(entry_routes)
app.register_blueprint(platform_routes)
app.register_blueprint(platform_song_routes)
app.register_blueprint(aggregation_routes)


#
# routes for template files
#


@app.route("/graphs")
def graphs():
    return render_template("graph.html")


@app.route("/")
def index() -> Any:
    return render_template("index.html")


# Run application
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5400)
