# Documentation des Logs de Sécurité - Version Avancée
## Importance du Suivi des Adresses IP et MAC pour l'Audit de Sécurité

### Introduction
Le système de logging avancé des utilisateurs intègre désormais le suivi des adresses IP (logiques) et MAC (physiques) pour une sécurité renforcée de l'application Antoine Calculator. Cette documentation explique la différence technique entre ces deux types d'adresses et leur importance respective dans un environnement réseau local (Intranet).

### Différence Technique : IP vs MAC

#### Adresse IP (Internet Protocol)
- **Nature** : Adresse logique, configurable et changeable
- **Format** : IPv4 (192.168.1.100) ou IPv6 (2001:0db8:85a3:0000:0000:8a2e:0370:7334)
- **Assignation** : Attribuée par le serveur DHCP ou configurée manuellement
- **Changement** : Peut changer à chaque connexion (DHCP) ou être modifiée manuellement
- **Portée** : Routable sur Internet (publique) ou locale (privée)
- **Spoofing** : Relativement facile à falsifier

#### Adresse MAC (Media Access Control)
- **Nature** : Adresse physique, gravée dans le matériel réseau
- **Format** : XX:XX:XX:XX:XX:XX (ex: 3D:F2:C9:A6:B3:4F)
- **Assignation** : Définie par le fabricant de la carte réseau
- **Changement** : Très difficile à modifier (nécessite des techniques avancées)
- **Portée** : Locale uniquement (commutation de couche 2)
- **Spoofing** : Théoriquement possible mais techniquement complexe

### Avantages du Suivi MAC en Environnement Local

#### 1. Identification Physique
- **Tracement matériel** : Identification unique de chaque machine
- **Détection de spoofing** : Comparaison entre IP et MAC pour détecter les tentatives de falsification
- **Profilage d'équipement** : Création de profils basés sur les adresses MAC connues

#### 2. Sécurité Renforcée
- **Authentification multi-niveaux** : Combinaison IP+MAC pour une vérification robuste
- **Détection d'intrusion** : Alertes lorsque des adresses MAC inconnues apparaissent sur le réseau
- **Contrôle d'accès physique** : Restriction basée sur les adresses MAC autorisées

#### 3. Audit Complexe
- **Corrélation d'événements** : Liaison entre activités réseau et utilisateurs spécifiques
- **Analyse comportementale** : Détection des schémas anormaux d'utilisation
- **Preuves matérielles** : Éléments de preuve plus difficiles à contester

### Scénarios d'Utilisation en Entreprise

#### 1. Environnement de Bureau
- **Postes de travail fixes** : Suivi des ordinateurs de bureau avec adresses MAC stables
- **Contrôle d'accès** : Autorisation basée sur les adresses MAC des employés
- **Détection de mouvements** : Alertes lorsque des employés utilisent des postes non autorisés

#### 2. Réseau Sans Fil (WiFi)
- **Accès WiFi sécurisé** : Filtrage MAC pour le contrôle d'accès au réseau
- **Détection de rogue AP** : Identification des points d'accès non autorisés
- **Monitoring des connexions** : Suivi des appareils mobiles connectés

#### 3. Environnement Industriel
- **Équipements spécialisés** : Suivi des machines et capteurs connectés
- **Sécurité IoT** : Contrôle des appareils Internet des Objets
- **Conformité réglementaire** : Documentation des accès aux systèmes critiques

### Types d'Actions Enregistrées avec MAC

#### 1. Connexions Réussies
- `Login Success` : Connexion réussie avec IP et MAC valides
- Métadonnées : IP source, MAC source, timestamp, utilisateur

#### 2. Échecs de Connexion
- `Login Failed - Invalid Credentials` : Identifiants incorrects
- `Login Failed - Email Not Verified` : Email non vérifié
- `Login Failed - System Error` : Erreur système
- Métadonnées : IP, MAC, username tenté, raison de l'échec

#### 3. Analyse Avancée
- **Corrélation IP-MAC** : Détection des incohérences
- **Profils temporels** : Habitudes de connexion par adresse MAC
- **Géolocalisation réseau** : Position des appareils sur le réseau local

### Implémentation Technique

#### 1. Capture de l'Adresse MAC
```python
from getmac import get_mac_address

# Capture depuis l'adresse IP du client
mac_address = get_mac_address(ip=request.remote_addr, network_request=True)
```

#### 2. Stockage en Base de Données
```sql
ALTER TABLE user_log 
ADD COLUMN mac_address VARCHAR(17) NULL 
AFTER ip_address;
```

#### 3. Indexation Optimisée
```sql
CREATE INDEX idx_user_log_mac_address ON user_log(mac_address);
CREATE INDEX idx_user_log_ip_mac ON user_log(ip_address, mac_address);
```

### Analyse et Monitoring Avancé

#### 1. Tableaux de Bord de Sécurité
- **Carte réseau** : Visualisation des appareils connectés par adresse MAC
- **Timeline des connexions** : Historique détaillé avec IP et MAC
- **Alertes en temps réel** : Notifications pour les activités suspectes

#### 2. Détection d'Anomalies
- **Nouvelles adresses MAC** : Alertes pour les appareils inconnus
- **Changements IP-MAC** : Détection des tentatives de spoofing
- **Schémas anormaux** : Identification des comportements suspects

#### 3. Rapports d'Audit
- **Rapports quotidiens** : Résumé des connexions avec adresses MAC
- **Analyse hebdomadaire** : Tendances et patterns d'utilisation
- **Audit mensuel** : Conformité et incidents de sécurité

### Bonnes Pratiques de Sécurité

#### 1. Protection des Données
- **Chiffrement** : Protection des adresses MAC dans la base de données
- **Contrôle d'accès** : Restriction d'accès aux logs de sécurité
- **Réduction de données** : Anonymisation après la période d'analyse

#### 2. Performance Optimale
- **Indexation stratégique** : Optimisation des requêtes fréquentes
- **Nettoyage régulier** : Archivage des anciens logs
- **Monitoring de performance** : Surveillance de l'impact sur les performances

#### 3. Conformité Réglementaire
- **RGPD** : Respect de la vie privée et protection des données
- **Normes industrielles** : Conformité avec les standards de sécurité
- **Documentation légale** : Maintien des preuves pour les enquêtes

### Limitations et Considérations

#### 1. Limites Techniques
- **Réseau local uniquement** : Les adresses MAC ne traversent pas les routeurs
- **VPN et proxys** : Peuvent masquer l'adresse MAC réelle
- **Virtualisation** : Machines virtuelles avec adresses MAC virtuelles

#### 2. Considérations Éthiques
- **Vie privée** : Respect de la vie privée des employés
- **Transparence** : Information claire sur le suivi effectué
- **Consentement** : Accord des utilisateurs pour le tracking

### Conclusion
L'intégration du suivi des adresses MAC avec les adresses IP crée un système de sécurité robuste et complet pour les environnements réseau locaux. Cette approche permet une détection précoce des menaces, une authentification renforcée et un audit détaillé des activités réseau.

Le système Antoine Calculator bénéficie désormais d'une couche de sécurité supplémentaire essentielle pour protéger les données utilisateur et maintenir un environnement de confiance dans les réseaux d'entreprise.
