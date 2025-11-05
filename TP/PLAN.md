# Plan de tests – Projet Triangulator
Objectif
Ce plan définit la stratégie de tests pour valider la fiabilité, la justesse, la performance et la qualité du microservice Triangulator, selon une approche test first.
* les tests à réaliser *
1. Tests unitaires

on Vérifie les fonctions internes :
-Calcul de triangulation.
-Conversion binaire et  structures Python.
-Gestion des entrées invalides.
But : assurer la justesse et la stabilité des fonctions de base.

2. Tests d’intégration

on Vérifie le fonctionnement global via l’API HTTP :
Interaction avec le PointSetManager .
Cas valides et erreurs (404, 503, etc.).
But : s’assurer du bon comportement du service de bout en bout.

3. Tests de performance

on doit Mesurer le temps de calcul et de conversion pour différents volumes de données.

Objectif : Mesurer la rapidité et la consommation de ressources.

Scénarios :
-Triangulation avec 10, 100, 1 000, 10 000 points.
-Mesure du temps moyen d’exécution et du taux de croissance.
-Mesure du temps de conversion binaire pour différents volumes.



* Outils et organisation *

pytest : exécution des tests
coverage : mesure de couverture
ruff : qualité du code
pdoc3 : documentation
Makefile : automatisation (make test, make unit_test, make perf_test, etc.)

* Critères de réussite *

-Tous les tests passent.
-Couverture > 90 %.
-Aucun warning ruff.
-Documentation générée sans erreur.

