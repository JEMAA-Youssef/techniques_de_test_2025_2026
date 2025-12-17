"""Tests end-to-end de l'API Triangulator.

Ces tests vérifient le flux complet :

	client HTTP → endpoint Flask → core.triangulate

Le service externe PointSetManager est simulé via un monkeypatch de
``requests.get`` dans ``triangulator.core``.
"""

import uuid
import struct

from types import SimpleNamespace

from triangulator import api, binary_utils


def _build_fake_pointset_binary() -> bytes:
	"""Construit un PointSet binaire représentant un carré de 4 points."""

	points = [
		(0.0, 0.0),
		(1.0, 0.0),
		(1.0, 1.0),
		(0.0, 1.0),
	]
	return binary_utils.encode_pointset(points)


def test_end_to_end_triangulation_success(monkeypatch):
	"""Flux complet réussi : récupération du PointSet et triangulation."""

	pointset_binary = _build_fake_pointset_binary()

	def fake_requests_get(url: str):  
		# Simule une réponse HTTP 200 du PointSetManager.
		return SimpleNamespace(status_code=200, content=pointset_binary)

	# On monkeypatch la fonction requests.get utilisée dans core.
	import triangulator.core as core

	monkeypatch.setattr(core, "requests", SimpleNamespace(get=fake_requests_get))

	app = api.app
	app.testing = True

	client = app.test_client()
	pointset_id = str(uuid.uuid4())

	response = client.get(f"/triangulate/{pointset_id}")

	assert response.status_code == 200
	data = response.data

	# La première partie est le PointSet d'origine.
	assert data.startswith(pointset_binary)

	# On lit ensuite l'en-tête nombre de triangles.
	offset = len(pointset_binary)
	(triangle_count,) = struct.unpack(">I", data[offset : offset + 4])

	# Avec 4 points, l'algorithme en éventail doit produire 2 triangles.
	assert triangle_count == 2

