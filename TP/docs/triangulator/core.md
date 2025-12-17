Module triangulator.core
========================

Functions
---------

`triangulate(pointset_id: str) ‑> bytes`
:   Fonction principale du Triangulator.
    
    C'est cette fonction qui est *monkeypatchée* dans les tests API
    → elle doit donc être la seule à regrouper toute la logique.
    
    Elle doit :
    1. valider l'UUID
    2. récupérer le pointset binaire
    3. décoder → liste de points
    4. trianguler
    5. encoder en binaire Triangles
    
    Exceptions attendues par les tests :
    - ValueError → HTTP 400
    - FileNotFoundError → HTTP 404
    - RuntimeError → HTTP 503
    - Exception générique → HTTP 500