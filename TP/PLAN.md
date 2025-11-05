# Plan de tests – Projet Triangulator

## Objectif

Ce document décrit la stratégie de tests adoptée pour valider la **fiabilité**, la **justesse**, la **performance** et la **qualité** du microservice `Triangulator`.  
L’approche suivie est **test-first** : les tests sont conçus **avant** toute implémentation de la logique métier, afin de guider le développement et garantir une couverture pertinente dès le départ.

---

## 1. Tests unitaires

### Objectif
Valider la justesse et la robustesse des fonctions internes du service, indépendamment de l’API ou des dépendances externes.

### Fonctionnalités à tester
- **Algorithme de triangulation**  
  - Sortie correcte pour des cas standards (3 points non colinéaires → 1 triangle).  
  - Comportement attendu pour les cas limites :  
    - Ensemble vide ou avec < 3 points → aucune triangulation.  
    - Points colinéaires ou dupliqués → robustesse de l’algorithme.  
- **Conversion binaire ↔ structures Python**  
  - Encodage/décodage exact des `PointSet` et `Triangles` selon la spécification binaire.  
  - Respect du format : taille, endianness, types (`unsigned long`, `float`).  
- **Gestion des entrées invalides**  
  - Données binaires tronquées, corrompues ou mal formatées.  
  - Points avec coordonnées infinies ou NaN (si pertinent).  

### Méthodologie
- Fonctions testées **en isolation** (sans dépendance réseau ou Flask).  
- Utilisation de `pytest` avec fixtures pour jeux de données réutilisables.  
- Mocks **non nécessaires** ici : les unités testées sont pures.

---

## 2. Tests d’intégration (API & interaction)

### Objectif
S’assurer que le service fonctionne correctement dans son **contexte réel** : via son API HTTP et en interaction avec le `PointSetManager`.

### Scénarios à tester
- **Cas nominal**  
  - Requête POST `/triangulate` avec un `PointSetID` valide → réponse `200` + payload binaire conforme.
- **Erreurs HTTP attendues**  
  - `404` si le `PointSetID` n’existe pas côté `PointSetManager`.  
  - `502` ou `503` si le `PointSetManager` est injoignable (ex. timeout, refus de connexion).  
  - `400` si l’ID fourni n’est pas un entier.
- **Mauvaises méthodes ou routes**  
  - GET sur `/triangulate` → `405 Method Not Allowed`.
- **Données incohérentes du PointSetManager**  
  - Réponse non binaire, binaire tronqué, nombre de points négatif → gestion sans crash.

### Méthodologie
- Lancement du service Flask en mode test (`app.test_client()`).  
- Mock de l’appel HTTP vers le `PointSetManager` à l’aide de `unittest.mock` ou `responses`.  
- Vérification stricte du **code HTTP**, du **Content-Type** (`application/octet-stream`) et du **corps binaire** de la réponse.

---

## 3. Tests de performance

### Objectif
Évaluer la scalabilité et l’efficacité du service en fonction de la taille des données traitées.

### Scénarios
- Triangulation de `PointSet` de tailles croissantes :  
  - 10 points → temps négligeable (< 10 ms)  
  - 100 points → < 100 ms  
  - 1 000 points → < 2 s  
  - 10 000 points → mesurer temps (attendu : croissance super-linéaire, mais pas de crash)  
- Mesure séparée du temps de :  
  - Désérialisation du `PointSet`  
  - Calcul de la triangulation  
  - Sérialisation du résultat (`Triangles`)

### Méthodologie
- Tests isolés avec décorateur `@pytest.mark.performance`.  
- Exécutés **seulement** via `make perf_test` (exclus de `make unit_test`).  
- Utilisation de `time.perf_counter()` pour mesures précises.  
- **Pas de seuil absolu imposé**, mais comparaisons relatives et documentation des résultats dans les commentaires de test.

---

## Outils et organisation

- **`pytest`** : framework principal pour tous les tests.  
- **`coverage`** : mesure la couverture du code par les tests (`make coverage`).  
- **`ruff`** : vérifie la qualité et la conformité du style (`make lint`).  
- **`pdoc3`** : génère automatiquement la documentation (`make doc`).  
- **`Makefile`** : fournit les commandes standardisées :  
  ```makefile
  make test          # tous les tests
  make unit_test     # tous sauf perf
  make perf_test     # uniquement perf
  make coverage
  make lint
  make doc