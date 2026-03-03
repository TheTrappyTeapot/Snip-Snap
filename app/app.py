from flask import Flask, render_template, jsonify, abort
from db import get_user_promo

def create_app():
    app = Flask(__name__)

    @app.get("/")
    def welcome():
        return render_template("welcome.html", title="Welcome Page")

    @app.get("/discover")
    def discover():
        return render_template("discover.html", title="Discover Page")

    @app.get("/barber_dashboard")
    def barber_dashboard():
        return render_template("barber_dashboard.html", title="Barber Dashboard")

    @app.route('/api/users/<int:user_id>/promo', methods=['GET'])
    def user_promo(user_id):
        user_data = get_user_promo(user_id)
        if user_data is None:
            abort(404, description="User not found")
        return jsonify(user_data)

    return app

if __name__ == "__main__":
    create_app().run(debug=True)

