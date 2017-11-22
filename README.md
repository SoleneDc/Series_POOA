PYHTON GROUPE 7 : Notes d’installation pour le projet SeriesPOOA
============================================================================================================================

•	Prérequis : avoir installé pyCharm et Django, et posséder un compte github (sinon utiliser user : TimGuez et mdp temporaire : pooa2017)
•	Dans pycharm, faire VCS > checkout from version control > GitHub
•	Remplir ses accès à gitHub et cloner le repository : https://github.com/SoleneDc/Series_POOA.git

============================================================================================================================
ATTENTION : bien vérifier qu’un interpréteur est renseigné dans les run configurations
============================================================================================================================

•	Une fois le projet ajouté, effectuer un run de la configuration Django « Migrate »
•	Effectuer un run de la configuration Django « createMixedTables »
•	Pour lancer le server, effectuer un run de la configuration « seriesPOOA »
•	Se connecter à localhost :8000/index pour voir le résultat


============================================================================================================================
Enfin il existe une dernière configuration qui peut servir : « weekly_mail » .
Elle est destinée à être activée par un cron hebdomadaire pour lancer un envoi de mail une fois par semaine.
Vous pouvez la lancer manuellement pour essayer.

L'application web peut encore être amélioré graphiquement, et il existe un bug lorsque l'on effectue deux recherches consécutives sans rafraichir la page.
La structure est déjà là et toutes les différentes techniques à utiliser ont déjà servie : gestion d'exceptions, bootstrap, etc.

============================================================================================================================
Auteurs : Solène Duchamp | Pauline Feray | Timothée Guez
