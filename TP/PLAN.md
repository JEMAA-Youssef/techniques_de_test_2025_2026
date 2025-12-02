# PLAN DE TESTS 
_Auteur : Youssef Jemaa_   
---

## 1. Introduction et objectifs

Le présent document décrit la stratégie de tests mise en œuvre pour le microservice **Triangulator**, dans le cadre du module *Techniques de Test*.  
L’objectif principal est de concevoir un **ensemble complet, cohérent et pertinent de tests** visant à valider le bon fonctionnement, la fiabilité et la performance du service, tout en respectant une approche **Test First** (rédaction des tests avant l’implémentation effective du code).

Le service Triangulator a pour mission de :
- récupérer un ensemble de points (`PointSet`) auprès d’un service externe ;
- effectuer le calcul de **triangulation** ;
- renvoyer le résultat sous forme binaire (`Triangles`) via une API REST.

L’enjeu de ce plan est donc de garantir que le composant est **juste, robuste, performant et bien testé**, sans se limiter à un taux de couverture mais en assurant la **pertinence des scénarios**.

---

## 2. Portée et périmètre des tests

### 2.1 Composants concernés
Les tests s’appliqueront exclusivement au **microservice Triangulator**, qui regroupe :
- la logique interne de calcul (algorithme de triangulation) ;
- les fonctions d’encodage/décodage binaire (`PointSet` ↔ `Triangles`) ;
- les endpoints Flask exposés pour les requêtes clientes.

### 2.2 Composants simulés
Certains éléments seront simulés pour isoler le Triangulator :
- **PointSetManager** : remplacé par un mock HTTP (simule ses réponses) ;
- **Base de données** et **Client** : exclus du périmètre.

### 2.3 Objectifs principaux
Les tests visent à :
1. Vérifier la validité des résultats de triangulation ;
2. Contrôler le respect du contrat API (spécification OpenAPI) ;
3. Mesurer les performances selon la taille des jeux de données ;
4. Garantir la résistance du service face aux erreurs d’entrée ou de communication.

---

## 3. Stratégie de test

Les tests sont répartis en cinq catégories principales afin de couvrir les aspects fonctionnels, techniques et qualitatifs du service.

---

### 3.1 Tests unitaires

#### Objectif
Vérifier le comportement des fonctions élémentaires de manière isolée, sans dépendance externe.

#### Axes testés
- **Encodage / décodage binaire**
  - Lecture et écriture cohérente des structures `PointSet` et `Triangles` ;
  - Gestion des cas particuliers : flux vide, longueur incorrecte, index hors borne ;
  - Vérification de la symétrie `encode → decode → encode`.
- **Algorithme de triangulation**
  - Cas nominaux : 
    - 3 points → 1 triangle attendu,  
    - 4 points formant un carré → 2 triangles.  
  - Cas limites : ensemble vide, points colinéaires, doublons.
- **Gestion interne des erreurs**
  - Validation des exceptions levées sur données invalides ;
  - Vérification de la cohérence des messages de logs et du format d’erreur interne.

---

### 3.2 Tests d’intégration (mock PointSetManager)

#### Objectif
Valider le comportement global du Triangulator lors d’échanges simulés avec le service `PointSetManager`.

#### Méthode
Utilisation d’un mock HTTP qui reproduit les réponses du PointSetManager.

#### Scénarios principaux
| Cas | Description | Résultat attendu |
|------|-------------|------------------|
|  Succès | Le mock renvoie un `PointSet` valide | 200 OK + contenu binaire cohérent |
|  PointSet introuvable | Mock → 404 | 404 Not Found propagé |
|  Service indisponible | Mock → 503 | 503 Service Unavailable |
|  Données corrompues | Mock renvoie binaire tronqué | 500 Internal Server Error |
|  Requête invalide | ID mal formé | 400 Bad Request |

---

### 3.3 Tests d’API (End-to-End)

#### Objectif
Vérifier la conformité du service à sa spécification OpenAPI (`triangulator.yml`).

#### Détails
- Validation des **routes et méthodes HTTP** ;
- Vérification des **codes de retour** et des **Content-Type** (`application/octet-stream`, `application/json`) ;
- Analyse de la structure binaire (longueur, types `float`/`unsigned long`, endianness) ;
- Tests automatisés via :
  - `flask.testing` pour l’exécution locale ;
  - `schemathesis` ou `openapi-core` pour la validation contractuelle.

---

### 3.4 Tests de performance

#### Objectif
Évaluer la rapidité et la scalabilité du service.

#### Scénarios
- Jeux de données croissants : 10 → 100 → 1 000 → 10 000 points.  
- Mesures :
  - Temps d’encodage/décodage ;
  - Temps de triangulation.  
- Test de charge : 50 à 100 requêtes simultanées (`pytest-benchmark`).

#### Critères de validation
- Aucune erreur 500 ;
- Temps moyen par triangulation inférieur au seuil défini ;
- Variation de temps stable entre exécutions.

Les tests de performance seront séparés des autres via :
```bash
pytest -m "performance"
```
### 3.5 Tests de robustesse et de tolérance aux erreurs

####  Objectif
S’assurer que le service reste **stable et prévisible** face à des entrées ou contextes imprévus.

---

####  Cas envisagés

- **Requête sans `PointSetID`** → renvoyer **HTTP 400 (Bad Request)**  
- **`PointSetID` non conforme** (UUID invalide) → renvoyer **HTTP 400 (Bad Request)**  
- **Données binaires tronquées ou incohérentes** → renvoyer **HTTP 400 ou 500** selon la gravité  
- **Service `PointSetManager` injoignable** → renvoyer **HTTP 503 (Service Unavailable)**  
- **Triangulation impossible** (ex. points identiques) → renvoyer **HTTP 500 (Internal Server Error)** avec un message explicite

---

####  Résultat attendu

Aucune exception non gérée.  
Chaque erreur doit renvoyer une **réponse JSON formelle** respectant le format suivant :

```json
{
  "error": "message explicite",
  "code": <HTTP>
}
```
### 4. Organisation et structure des tests

L’organisation suit une structure modulaire afin de maintenir une bonne lisibilité :

```text
/tests
│
├── unit/
│ ├── test_binary_codec.py
│ ├── test_triangulation_core.py
│ ├── test_internal_errors.py
│
├── integration/
│ ├── test_mock_pointsetmanager.py
│
├── api/
│ ├── test_routes_openapi.py
│ ├── test_end_to_end_flow.py
│
└── performance/
├── test_benchmark_triangulation.py
```

Chaque répertoire correspond à une famille de tests, exécutables via des commandes make dédiées.

### 5. Outils et automatisation

| Outil     | Rôle |
|------------|---------------------------------------------|
| **pytest** | Exécution des tests et gestion des catégories |
| **coverage** | Mesure du taux de couverture global |
| **ruff** | Vérification du style et de la qualité de code |
| **pdoc3** | Génération automatique de la documentation |
| **make** | Centralisation des commandes d’exécution |

---

####  Cibles Makefile prévues

```bash
make test          # Tous les tests
make unit_test     # Sans performance
make perf_test     # Tests de performance seuls
make coverage      # Rapport de couverture
make lint          # Vérification qualité de code
make doc           # Génération documentation
```
### 6. Critères de validation

Pour considérer le projet comme validé, les conditions suivantes devront être remplies :

| Critère | Attendu |
|----------|----------|
|  Tous les tests passent | 100 % vert sous pytest |
|  Couverture minimale | ≥ 90 % du code |
|  Aucune erreur de style | `ruff check` sans avertissement |
|  Documentation générée | `pdoc3` sans erreur |
|  Performance acceptable | Temps de calcul stable sur gros jeux de points |
|  Robustesse | Aucune erreur non interceptée |


### 7. Jeux de données de test

Pour garantir la variété et la fiabilité des tests :

####  Déterministes :
- Ensemble vide  
- 1, 2, 3 points *(triangle de base)*  
- Carré *(4 points → 2 triangles)*  
- Polygones réguliers *(5 à 8 sommets)*  

####  Aléatoires :
- Nuages de **100**, **500**, **1 000** et **10 000** points générés dynamiquement

### 8. Conclusion

Ce plan définit la stratégie complète de validation du **microservice Triangulator**.  
Il vise à garantir une implémentation **fiable**, **performante** et **conforme à la spécification**, tout en maintenant un **haut niveau de qualité logicielle**.  

Les tests seront progressivement **enrichis au fur et à mesure du développement**, conformément à l’approche **Test First** adoptée pour ce projet.

