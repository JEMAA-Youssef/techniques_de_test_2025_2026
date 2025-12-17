Module triangulator.binary_utils
================================

Functions
---------

`decode_pointset(binary_data)`
:   Décode un PointSet binaire.
    Retourne une liste de tuples [(x, y), ...]

`encode_pointset(points)`
:   Encode un ensemble de points au format binaire.
    Format :
        [4 bytes unsigned long: count]
        [4 bytes float x][4 bytes float y] * count