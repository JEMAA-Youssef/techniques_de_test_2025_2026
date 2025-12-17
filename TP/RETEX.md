# RETEX.md — Retour d’expérience  
_Auteur : **Youssef Jemaa**_  
_Module : Techniques de Test — M1 ILSEN — 2025/2026_

---

## 1. Contexte et objectif du projet

Le projet consistait à développer et tester un microservice appelé **Triangulator**, dont le rôle est de calculer une triangulation à partir d’un ensemble de points fourni par un service externe (`PointSetManager`).  
L’objectif principal du TP n’était pas la complexité de l’algorithme, mais la mise en place d’une **stratégie de tests pertinente**, couvrant les comportements normaux et les cas d’erreur.

Une approche **Test First** était demandée, ainsi qu’une attention particulière à la qualité du code, à la gestion des erreurs, à la couverture et à la documentation.

---

## 2. Ce que j’ai bien fait

J’ai commencé par rédiger un **plan de tests structuré**, distinguant clairement les tests unitaires, les tests d’API, les tests d’intégration et les tests de performance.  
Ce plan m’a servi de guide tout au long du projet et m’a permis de garder une vision globale du comportement attendu du service.

L’utilisation de **mocks et de monkeypatch** m’a permis de tester le Triangulator de manière isolée, sans dépendre réellement du `PointSetManager`. Cela a facilité la vérification des scénarios d’erreur comme les réponses 404 ou 503.

J’ai également porté une attention particulière à la **gestion des codes HTTP**, afin que chaque type d’erreur soit correctement mappé et conforme à la spécification OpenAPI.

Enfin, tous les outils demandés (`pytest`, `coverage`, `ruff`, `pdoc3`, `make`) ont été correctement intégrés et automatisés.

---

## 3. Ce que j’ai mal fait ou trouvé difficile

### Compréhension du format binaire

La manipulation du format binaire des structures `PointSet` et `Triangles` a été l’une des principales difficultés, notamment la gestion des tailles, de l’endianness et de la cohérence entre l’en-tête et le contenu réel.  
Plusieurs corrections ont été nécessaires après la mise en place des tests.

### Validation des identifiants

Un point délicat a été la validation des identifiants (`UUID`). Certains tests nécessitaient de laisser passer des identifiants non standards afin de simuler des erreurs côté service externe, ce qui m’a obligé à ajuster la logique de validation dans la couche API.

### Ruff et contraintes de style

Les règles imposées par **Ruff**, en particulier sur les docstrings, ont demandé un temps d’adaptation important.  
Même si cela a été contraignant au départ, cela a permis d’améliorer la lisibilité et la documentation du code.

### Mocks et monkeypatch

L’utilisation du monkeypatch a nécessité une bonne compréhension des chemins d’imports.  
Au début, certaines simulations ne touchaient pas le bon code, ce qui m’a obligé à mieux comprendre la structure interne du projet.

---

## 4. Couverture de code

La première mesure de couverture incluait les bibliothèques externes, ce qui donnait un pourcentage global trompeur.  
Après avoir restreint l’analyse au **code du Triangulator**, la couverture atteint environ **93 %**, comme le montre le rapport suivant :

```bash
youssef@DESKTOP-OG1MBNI:/mnt/c/Users/Youssef/Desktop/M1/Technique_De_Test/techniques_de_test_2025_2026/TP$ coverage report
Name                           Stmts   Miss  Cover
--------------------------------------------------
triangulator/__init__.py           2      0   100%
triangulator/api.py               27      2    93%
triangulator/binary_utils.py      23      0   100%
triangulator/core.py              44      5    89%
--------------------------------------------------
TOTAL                             96      7    93%
youssef@DESKTOP-OG1MBNI:/mnt/c/Users/Youssef/Desktop/M1/Technique_De_Test/techniques_de_test_2025_2026/TP$
```

Les lignes non couvertes correspondent principalement à des branches d’erreur rares ou difficiles à déclencher sans tests artificiels, ce qui ne remet pas en cause la robustesse globale du service.

---

## 5. Qualité du plan initial

Le plan de tests initial était globalement pertinent, car il identifiait dès le départ les différents niveaux de tests (unitaires, API, intégration et performance) ainsi que les principaux scénarios d’erreur.  
En revanche, certains aspects ont été sous-estimés, notamment la complexité du format binaire et l’impact des contraintes de qualité imposées par le linter, qui auraient mérité d’être anticipés plus précisément.

---

## 6. Ce que je ferais autrement

Avec le recul, je prendrais en compte les règles du linter dès le début du projet afin d’éviter des corrections tardives.  
Je renforcerais également les tests basés sur des propriétés, par exemple pour vérifier la bijection entre encodage et décodage binaire sur un plus grand nombre de cas.

---

## 7. Conclusion

Ce projet m’a permis de mieux comprendre l’importance d’une **stratégie de tests réfléchie**, au-delà de la simple implémentation du code.  
J’ai appris à structurer un microservice autour de tests pertinents, à gérer correctement les erreurs et à utiliser des outils d’automatisation pour garantir la qualité et la maintenabilité du projet.

Le Triangulator final est fonctionnel, bien testé et conforme aux attentes du module.
