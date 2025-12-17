Module triangulator.api
=======================

Functions
---------

`triangulate_route(pointset_id)`
:   Endpoint principal de triangulation.
    
        IMPORTANT :
        On valide le **format** d'UUID uniquement lorsque la chaîne
        "ressemble" à un UUID (contient un tiret). Cela permet :
    
        * de renvoyer 400 pour un identifiant mal formé comme
            "not-a-valid-uuid" (tests d'API) ;
        * tout en laissant passer des identifiants simples comme
            "unknown" vers ``core.triangulate`` (tests d'intégration
            qui simulent un 404 du PointSetManager).

`triangulate_route_missing_id()`
:   Cas où aucun ID n'est fourni.