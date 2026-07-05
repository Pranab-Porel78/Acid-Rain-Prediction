from flask import Blueprint, jsonify, request

from services.pollution_service import (
    fetch_and_store_pollution,
    latest_pollution,
    pollution_history
)

pollution_bp = Blueprint(
    "pollution",
    __name__
)


# ==========================================
# Fetch New Pollution Data
# ==========================================

@pollution_bp.route("/pollution", methods=["GET"])
def fetch_pollution():

    try:

        city = request.args.get("city")

        latitude = request.args.get("lat", type=float)

        longitude = request.args.get("lon", type=float)

        if city is None or latitude is None or longitude is None:

            return jsonify({

                "status": "error",

                "message": "Missing city, latitude or longitude."

            }), 400

        pollution = fetch_and_store_pollution(

            city,
            latitude,
            longitude

        )

        return jsonify(pollution)

    except Exception as e:

        return jsonify({

            "status": "error",

            "message": str(e)

        }), 500


# ==========================================
# Latest Pollution Data
# ==========================================

@pollution_bp.route("/pollution/latest", methods=["GET"])
def latest():

    try:

        data = latest_pollution()

        return jsonify(data)

    except Exception as e:

        return jsonify({

            "status": "error",

            "message": str(e)

        }), 500


# ==========================================
# Pollution History
# ==========================================

@pollution_bp.route("/pollution/history", methods=["GET"])
def history():

    try:

        limit = request.args.get(

            "limit",

            default=20,

            type=int

        )

        data = pollution_history(limit)

        return jsonify(data)

    except Exception as e:

        return jsonify({

            "status": "error",

            "message": str(e)

        }), 500


# ==========================================
# Health Check
# ==========================================

@pollution_bp.route("/pollution/status", methods=["GET"])
def status():

    return jsonify({

        "status": "online",

        "service": "Pollution API",

        "history_endpoint": "/api/pollution/history",

        "latest_endpoint": "/api/pollution/latest"

    })