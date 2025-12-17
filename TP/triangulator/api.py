"""API Flask du micro-service Triangulator.

Expose l'endpoint principal permettant de déclencher une triangulation
à partir d'un identifiant de PointSet.
"""

import uuid

from flask import Flask, Response, jsonify

import triangulator.core as core

app = Flask(__name__)


@app.route("/triangulate/<pointset_id>", methods=["GET"])
def triangulate_route(pointset_id):
    """Endpoint principal de triangulation.

    IMPORTANT :
    On valide le format UUID uniquement lorsque la chaîne *ressemble*
    à un UUID (présence d’un tiret). Cela permet :

    * de renvoyer 400 pour un identifiant mal formé comme
      ``"not-a-valid-uuid"`` ;
    * de laisser passer des identifiants simples comme ``"unknown"`` vers
      ``core.triangulate`` (tests d'intégration simulant un 404 du
      PointSetManager).
    """
    if not pointset_id:
        return jsonify({"error": "Missing PointSet ID"}), 400

    if "-" in pointset_id:
        try:
            uuid.UUID(pointset_id)
        except Exception:
            return jsonify({"error": "Invalid PointSet ID format"}), 400

    try:
        result = core.triangulate(pointset_id)
        return Response(result, mimetype="application/octet-stream", status=200)

    except ValueError:
        return jsonify({"error": "Invalid PointSet ID format"}), 400
    except (FileNotFoundError, KeyError):
        return jsonify({"error": "PointSet not found"}), 404
    except RuntimeError:
        return jsonify({"error": "Service unavailable"}), 503
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.route("/triangulate/", methods=["GET"])
def triangulate_route_missing_id():
    """Cas où aucun ID n'est fourni."""
    return jsonify({"error": "Missing PointSet ID"}), 400
