"""
Ce fichier contient une banque de questions en français pour le générateur de questions.
Il sera utilisé pour créer un fichier de questions en français pour l'application Quiz TikTok Live.
"""

# Banque de questions prédéfinies par thème
questions_data = {
    "Culture générale": [
        {"text": "Quelle est la capitale de la France?", "answer": "Paris"},
        {"text": "Qui a peint la Joconde?", "answer": "Léonard de Vinci"},
        {"text": "Quel est l'élément chimique le plus abondant dans l'univers?", "answer": "Hydrogène"},
        {"text": "Combien de jours y a-t-il dans une année bissextile?", "answer": "366"},
        {"text": "Dans quel pays se trouve la tour de Pise?", "answer": "Italie"},
        {"text": "Qui a écrit 'Les Misérables'?", "answer": "Victor Hugo"},
        {"text": "Quel est le plus grand océan du monde?", "answer": "Pacifique"},
        {"text": "Quelle est la monnaie du Japon?", "answer": "Yen"},
        {"text": "Qui était le premier homme à marcher sur la Lune?", "answer": "Neil Armstrong"},
        {"text": "Quel est le nom du plus grand désert chaud du monde?", "answer": "Sahara"},
        {"text": "Combien y a-t-il de joueurs dans une équipe de football?", "answer": "11"},
        {"text": "Quelle est la planète la plus proche du Soleil?", "answer": "Mercure"},
        {"text": "Quel est le symbole chimique de l'or?", "answer": "Au"},
        {"text": "Quel est le plus grand mammifère terrestre?", "answer": "Éléphant"},
        {"text": "Dans quelle ville se trouve le Colisée?", "answer": "Rome"},
        {"text": "Quelle est la monnaie européenne?", "answer": "Euro"},
        {"text": "Combien de côtés a un hexagone?", "answer": "6"},
        {"text": "Qui a découvert la pénicilline?", "answer": "Fleming"},
        {"text": "Qui a inventé l'ampoule électrique?", "answer": "Edison"},
        {"text": "Quel est l'animal emblème des États-Unis?", "answer": "Aigle"}
    ],
    
    "Géographie": [
        {"text": "Quel est le plus grand désert du monde?", "answer": "Antarctique"},
        {"text": "Quel est le plus long fleuve du monde?", "answer": "Nil"},
        {"text": "Quelle est la capitale de l'Australie?", "answer": "Canberra"},
        {"text": "Combien de continents y a-t-il sur Terre?", "answer": "7"},
        {"text": "Quel est le plus grand lac d'Afrique?", "answer": "Victoria"},
        {"text": "Quelle ville est connue comme la 'Ville Lumière'?", "answer": "Paris"},
        {"text": "Quelle est la capitale du Canada?", "answer": "Ottawa"},
        {"text": "Sur quel continent se trouve l'Égypte?", "answer": "Afrique"},
        {"text": "Quel est le plus petit pays du monde?", "answer": "Vatican"},
        {"text": "Quelle mer sépare l'Europe de l'Afrique?", "answer": "Méditerranée"},
        {"text": "Quelle est la capitale du Brésil?", "answer": "Brasilia"},
        {"text": "Quel est le plus haut sommet du monde?", "answer": "Everest"},
        {"text": "Dans quel océan se trouve Madagascar?", "answer": "Indien"},
        {"text": "Quelle est la plus grande île du monde?", "answer": "Groenland"},
        {"text": "Quel est le pays le plus peuplé du monde?", "answer": "Chine"},
        {"text": "Quelle chaîne de montagnes traverse l'Amérique du Sud?", "answer": "Andes"},
        {"text": "Quelle est la capitale de la Russie?", "answer": "Moscou"},
        {"text": "Quel fleuve traverse Paris?", "answer": "Seine"},
        {"text": "Dans quel pays se trouve le Taj Mahal?", "answer": "Inde"},
        {"text": "Quel pays a la forme d'une botte?", "answer": "Italie"}
    ],
    
    "Histoire": [
        {"text": "En quelle année l'homme a-t-il marché sur la Lune?", "answer": "1969"},
        {"text": "Qui était le premier président des États-Unis?", "answer": "Washington"},
        {"text": "En quelle année a commencé la Première Guerre mondiale?", "answer": "1914"},
        {"text": "Quel pays a inventé le papier?", "answer": "Chine"},
        {"text": "Qui a découvert la pénicilline?", "answer": "Fleming"},
        {"text": "En quelle année est tombé le mur de Berlin?", "answer": "1989"},
        {"text": "Quel empereur a construit le Colisée de Rome?", "answer": "Vespasien"},
        {"text": "Qui était Cléopâtre?", "answer": "Reine d'Égypte"},
        {"text": "Quelle était la civilisation des pharaons?", "answer": "Égyptienne"},
        {"text": "En quelle année Christophe Colomb a-t-il découvert l'Amérique?", "answer": "1492"},
        {"text": "Qui a écrit 'L'Art de la Guerre'?", "answer": "Sun Tzu"},
        {"text": "En quelle année a eu lieu la Révolution française?", "answer": "1789"},
        {"text": "Quel roi a signé la Magna Carta?", "answer": "Jean sans Terre"},
        {"text": "Qui était Jeanne d'Arc?", "answer": "Héroïne française"},
        {"text": "Quelle était la monnaie française avant l'euro?", "answer": "Franc"},
        {"text": "En quelle année a eu lieu la Révolution russe?", "answer": "1917"},
        {"text": "Qui était le premier empereur de Chine?", "answer": "Qin Shi Huang"},
        {"text": "Quelle guerre s'est déroulée entre 1939 et 1945?", "answer": "Seconde Guerre mondiale"},
        {"text": "En quelle année la déclaration d'indépendance américaine a-t-elle été signée?", "answer": "1776"},
        {"text": "Qui était Napoléon Bonaparte?", "answer": "Empereur français"}
    ],
    
    "Sciences": [
        {"text": "Qui a formulé la théorie de la relativité?", "answer": "Einstein"},
        {"text": "Quel est le symbole chimique de l'or?", "answer": "Au"},
        {"text": "Quelle est la plus petite planète du système solaire?", "answer": "Mercure"},
        {"text": "Quelle est la vitesse de la lumière?", "answer": "300000 km/s"},
        {"text": "Quel organe pompe le sang dans le corps?", "answer": "Cœur"},
        {"text": "Quelle est la particule élémentaire du noyau atomique?", "answer": "Nucléon"},
        {"text": "Qui a découvert la radioactivité?", "answer": "Marie Curie"},
        {"text": "Quel est le symbole chimique du fer?", "answer": "Fe"},
        {"text": "Comment s'appelle le processus par lequel les plantes fabriquent leur nourriture?", "answer": "Photosynthèse"},
        {"text": "Qui a inventé l'ampoule électrique?", "answer": "Edison"},
        {"text": "Quelle est la forme géométrique de l'ADN?", "answer": "Double hélice"},
        {"text": "Quel est l'os le plus long du corps humain?", "answer": "Fémur"},
        {"text": "Quelle est la neuvième planète déclassée du système solaire?", "answer": "Pluton"},
        {"text": "Quelle est la force qui maintient les planètes en orbite autour du Soleil?", "answer": "Gravitation"},
        {"text": "Quel est le métal conducteur le plus courant dans les fils électriques?", "answer": "Cuivre"},
        {"text": "Quel élément a le symbole chimique 'O'?", "answer": "Oxygène"},
        {"text": "Qu'est-ce que la photosynthèse produit comme gaz?", "answer": "Oxygène"},
        {"text": "Quel est le plus petit os du corps humain?", "answer": "Étrier"},
        {"text": "Combien d'éléments chimiques y a-t-il dans le tableau périodique?", "answer": "118"},
        {"text": "Quel scientifique a découvert la théorie de l'évolution?", "answer": "Darwin"}
    ],
    
    "Cinéma": [
        {"text": "Qui a réalisé le film 'Titanic'?", "answer": "James Cameron"},
        {"text": "Quel acteur joue Iron Man dans l'univers Marvel?", "answer": "Robert Downey Jr"},
        {"text": "Dans quel film peut-on entendre 'Je suis ton père'?", "answer": "Star Wars"},
        {"text": "Quel est le nom du sorcier principal dans 'Harry Potter'?", "answer": "Harry Potter"},
        {"text": "Quelle actrice joue Katniss Everdeen dans 'Hunger Games'?", "answer": "Jennifer Lawrence"},
        {"text": "Combien y a-t-il de films dans la trilogie originale 'Star Wars'?", "answer": "3"},
        {"text": "Quel film a gagné l'Oscar du meilleur film en 2020?", "answer": "Parasite"},
        {"text": "Dans quelle série retrouve-t-on les personnages de Ross et Rachel?", "answer": "Friends"},
        {"text": "Quel acteur joue Jack Dawson dans 'Titanic'?", "answer": "Leonardo DiCaprio"},
        {"text": "Qui est le réalisateur de 'Pulp Fiction'?", "answer": "Tarantino"},
        {"text": "Quel acteur a joué le rôle du Joker en 2008?", "answer": "Heath Ledger"},
        {"text": "Dans quelle ville se déroule 'Breaking Bad'?", "answer": "Albuquerque"},
        {"text": "Qui a réalisé 'E.T.'?", "answer": "Spielberg"},
        {"text": "Quel est le nom du vaisseau spatial dans 'Alien'?", "answer": "Nostromo"},
        {"text": "Qui a joué Forrest Gump?", "answer": "Tom Hanks"},
        {"text": "Quel acteur incarne James Bond dans 'Casino Royale'?", "answer": "Daniel Craig"},
        {"text": "Quel film raconte l'histoire d'un pianiste juif pendant la Seconde Guerre mondiale?", "answer": "Le Pianiste"},
        {"text": "Qui a réalisé 'Inception'?", "answer": "Christopher Nolan"},
        {"text": "Quel est le nom du personnage principal dans 'Matrix'?", "answer": "Neo"},
        {"text": "Dans quel film un lingot d'or est-il volé à Turin?", "answer": "L'or se barre"}
    ],
    
    "Sport": [
        {"text": "Quel pays a remporté le plus de Coupes du Monde de football?", "answer": "Brésil"},
        {"text": "Combien de joueurs y a-t-il dans une équipe de basket?", "answer": "5"},
        {"text": "Dans quel sport utilise-t-on un volant?", "answer": "Badminton"},
        {"text": "Quelle ville a accueilli les Jeux Olympiques de 2016?", "answer": "Rio"},
        {"text": "Qui détient le record du monde du 100m?", "answer": "Usain Bolt"},
        {"text": "Quel pays a inventé le judo?", "answer": "Japon"},
        {"text": "Combien de temps dure un match de football?", "answer": "90 minutes"},
        {"text": "Dans quel sport utilise-t-on un green?", "answer": "Golf"},
        {"text": "Qui est considéré comme le meilleur joueur de basketball?", "answer": "Michael Jordan"},
        {"text": "Quel pays a gagné la Coupe du Monde de football 2018?", "answer": "France"},
        {"text": "Combien de temps dure un match de rugby?", "answer": "80 minutes"},
        {"text": "Quel est le tournoi de tennis le plus ancien?", "answer": "Wimbledon"},
        {"text": "Quel est le sport national du Japon?", "answer": "Sumo"},
        {"text": "Quelle est la distance d'un marathon?", "answer": "42,195 km"},
        {"text": "Qui a gagné le plus de Grand Chelem au tennis?", "answer": "Novak Djokovic"},
        {"text": "Dans quel sport pratique-t-on un dribble?", "answer": "Basketball"},
        {"text": "Combien de joueurs composent une équipe de volley-ball?", "answer": "6"},
        {"text": "Qui est le meilleur buteur de l'histoire du football?", "answer": "Cristiano Ronaldo"},
        {"text": "En quelle année se sont déroulés les premiers Jeux Olympiques modernes?", "answer": "1896"},
        {"text": "Quel nageur a gagné 8 médailles d'or aux JO de 2008?", "answer": "Michael Phelps"}
    ],
    
    "Musique": [
        {"text": "Qui est l'artiste avec le plus de Grammy Awards?", "answer": "Beyoncé"},
        {"text": "Quel groupe a sorti l'album 'Abbey Road'?", "answer": "Beatles"},
        {"text": "Qui a chanté 'Billie Jean'?", "answer": "Michael Jackson"},
        {"text": "Quel groupe a chanté 'Bohemian Rhapsody'?", "answer": "Queen"},
        {"text": "Quelle chanteuse est connue comme la 'Reine de la Pop'?", "answer": "Madonna"},
        {"text": "De quel pays est originaire le groupe ABBA?", "answer": "Suède"},
        {"text": "Combien de membres comptait le groupe The Beatles?", "answer": "4"},
        {"text": "Qui a chanté 'Like a Rolling Stone'?", "answer": "Bob Dylan"},
        {"text": "Quel instrument joue principalement Yo-Yo Ma?", "answer": "Violoncelle"},
        {"text": "Qui est le chanteur du groupe U2?", "answer": "Bono"},
        {"text": "Quel artiste français a chanté 'La vie en rose'?", "answer": "Édith Piaf"},
        {"text": "Quel groupe a sorti l'album 'Dark Side of the Moon'?", "answer": "Pink Floyd"},
        {"text": "Qui a composé 'Les Quatre Saisons'?", "answer": "Vivaldi"},
        {"text": "Dans quel pays est né Mozart?", "answer": "Autriche"},
        {"text": "Quel artiste est connu pour le tube 'Shape of You'?", "answer": "Ed Sheeran"},
        {"text": "Quel groupe de rock a pour chanteur Mick Jagger?", "answer": "Rolling Stones"},
        {"text": "Qui a chanté 'Imagine'?", "answer": "John Lennon"},
        {"text": "Quel artiste est surnommé 'The King'?", "answer": "Elvis Presley"},
        {"text": "Qui a composé 'La Neuvième Symphonie'?", "answer": "Beethoven"},
        {"text": "Quel genre musical est né à la Nouvelle-Orléans?", "answer": "Jazz"}
    ],
    
    "Littérature": [
        {"text": "Qui a écrit '1984'?", "answer": "Orwell"},
        {"text": "Qui a écrit 'Le Petit Prince'?", "answer": "Saint-Exupéry"},
        {"text": "Qui est l'auteur de la saga 'Harry Potter'?", "answer": "Rowling"},
        {"text": "Quel personnage dit 'Être ou ne pas être'?", "answer": "Hamlet"},
        {"text": "Qui a écrit 'Les Trois Mousquetaires'?", "answer": "Dumas"},
        {"text": "De quel pays est originaire Cervantes, l'auteur de Don Quichotte?", "answer": "Espagne"},
        {"text": "Quel animal est Baloo dans 'Le Livre de la Jungle'?", "answer": "Ours"},
        {"text": "Quelle est la nationalité de Gabriel García Márquez?", "answer": "Colombienne"},
        {"text": "Qui a écrit 'Crime et Châtiment'?", "answer": "Dostoïevski"},
        {"text": "Quel poète français a écrit 'Les Fleurs du Mal'?", "answer": "Baudelaire"},
        {"text": "Qui est l'auteur de 'Notre-Dame de Paris'?", "answer": "Victor Hugo"},
        {"text": "Quel est le prénom du capitaine Achab dans 'Moby Dick'?", "answer": "Achab"},
        {"text": "Qui a écrit 'La Métamorphose'?", "answer": "Kafka"},
        {"text": "Dans quelle ville se déroule 'Roméo et Juliette'?", "answer": "Vérone"},
        {"text": "Qui est l'auteur de 'L'Étranger'?", "answer": "Camus"},
        {"text": "Qui a écrit 'Les Misérables'?", "answer": "Victor Hugo"},
        {"text": "Quel écrivain français est l'auteur de 'Madame Bovary'?", "answer": "Flaubert"},
        {"text": "Qui a écrit 'Orgueil et Préjugés'?", "answer": "Jane Austen"},
        {"text": "Quel écrivain russe a écrit 'Guerre et Paix'?", "answer": "Tolstoï"},
        {"text": "Dans quelle œuvre trouve-t-on le personnage de Jean Valjean?", "answer": "Les Misérables"}
    ],
    
    "Animaux": [
        {"text": "Quel est l'animal le plus rapide du monde?", "answer": "Guépard"},
        {"text": "Quel animal est le roi de la jungle?", "answer": "Lion"},
        {"text": "Quel est le plus grand animal terrestre?", "answer": "Éléphant"},
        {"text": "Quel est le plus grand animal marin?", "answer": "Baleine bleue"},
        {"text": "Quelle est la durée de gestation d'un éléphant?", "answer": "22 mois"},
        {"text": "Quel insecte produit du miel?", "answer": "Abeille"},
        {"text": "Quel animal peut vivre jusqu'à 150 ans?", "answer": "Tortue"},
        {"text": "Quel animal est le symbole de la Chine?", "answer": "Panda"},
        {"text": "Quelle est la vitesse maximale d'un guépard?", "answer": "120 km/h"},
        {"text": "Quel oiseau ne peut pas voler?", "answer": "Autruche"},
        {"text": "Quel est le seul mammifère capable de voler?", "answer": "Chauve-souris"},
        {"text": "Combien d'estomacs a une vache?", "answer": "4"},
        {"text": "Quel animal change de couleur selon son environnement?", "answer": "Caméléon"},
        {"text": "Quel animal est connu comme le meilleur ami de l'homme?", "answer": "Chien"},
        {"text": "Quel animal dort suspendu à l'envers?", "answer": "Chauve-souris"},
        {"text": "Quel oiseau est le symbole de la paix?", "answer": "Colombe"},
        {"text": "Quel est le plus grand félin?", "answer": "Tigre"},
        {"text": "Quelle est la vitesse maximale d'un cheval?", "answer": "70 km/h"},
        {"text": "Quel animal vit dans une ruche?", "answer": "Abeille"},
        {"text": "Quel animal est le roi des animaux?", "answer": "Lion"}
    ],
    
    "Art": [
        {"text": "Qui a peint 'La Joconde'?", "answer": "Léonard de Vinci"},
        {"text": "Quel mouvement artistique a été fondé par Breton?", "answer": "Surréalisme"},
        {"text": "Qui a peint 'La Nuit Étoilée'?", "answer": "Van Gogh"},
        {"text": "Dans quelle ville se trouve le musée du Louvre?", "answer": "Paris"},
        {"text": "Qui a sculpté 'Le Penseur'?", "answer": "Rodin"},
        {"text": "Quel artiste est connu pour ses mobiles?", "answer": "Calder"},
        {"text": "Qui a peint 'Guernica'?", "answer": "Picasso"},
        {"text": "Quel mouvement artistique est caractérisé par des points de couleur?", "answer": "Pointillisme"},
        {"text": "Qui a peint 'Les Nymphéas'?", "answer": "Monet"},
        {"text": "Dans quel musée est exposée 'La Vénus de Milo'?", "answer": "Louvre"},
        {"text": "Qui a peint le plafond de la chapelle Sixtine?", "answer": "Michel-Ange"},
        {"text": "Quel peintre s'est coupé l'oreille?", "answer": "Van Gogh"},
        {"text": "Quel est le style architectural de Notre-Dame de Paris?", "answer": "Gothique"},
        {"text": "Qui a créé 'La Persistance de la Mémoire' avec des montres molles?", "answer": "Dali"},
        {"text": "Quel mouvement artistique est caractérisé par des formes géométriques?", "answer": "Cubisme"},
        {"text": "Qui a peint 'Le Cri'?", "answer": "Munch"},
        {"text": "Quel artiste a créé 'La Fontaine', un urinoir signé?", "answer": "Duchamp"},
        {"text": "Qui a peint 'Les Demoiselles d'Avignon'?", "answer": "Picasso"},
        {"text": "Dans quel musée est exposé 'Le Radeau de la Méduse'?", "answer": "Louvre"},
        {"text": "Quel artiste est connu pour ses 'Campbell's Soup Cans'?", "answer": "Warhol"}
    ],
    
    "Mythologie": [
        {"text": "Qui est le dieu grec de la mer?", "answer": "Poséidon"},
        {"text": "Quel héros grec a tué le Minotaure?", "answer": "Thésée"},
        {"text": "Comment s'appelle le roi des dieux dans la mythologie grecque?", "answer": "Zeus"},
        {"text": "Qui a ouvert la boîte contenant tous les maux de l'humanité?", "answer": "Pandore"},
        {"text": "Quel demi-dieu grec a réalisé 12 travaux?", "answer": "Hercule"},
        {"text": "Qui est le dieu romain équivalent à Hermès?", "answer": "Mercure"},
        {"text": "Quelle créature a des serpents à la place des cheveux?", "answer": "Méduse"},
        {"text": "Qui est le dieu nordique du tonnerre?", "answer": "Thor"},
        {"text": "Quel est l'instrument de musique d'Apollon?", "answer": "Lyre"},
        {"text": "Qui est la déesse grecque de la sagesse?", "answer": "Athéna"},
        {"text": "Quel est le royaume des morts dans la mythologie grecque?", "answer": "Hadès"},
        {"text": "Qui a tué Achille pendant la guerre de Troie?", "answer": "Pâris"},
        {"text": "Quel animal a allaité Romulus et Rémus?", "answer": "Louve"},
        {"text": "Qui est la déesse égyptienne de la maternité?", "answer": "Isis"},
        {"text": "Quel dieu égyptien a la tête d'un faucon?", "answer": "Horus"},
        {"text": "Quel animal mythique renaît de ses cendres?", "answer": "Phénix"},
        {"text": "Qui est le dieu hindou destructeur?", "answer": "Shiva"},
        {"text": "Quelle créature mythique est mi-homme mi-taureau?", "answer": "Minotaure"},
        {"text": "Qui est le dieu aztèque de la pluie?", "answer": "Tlaloc"},
        {"text": "Qui est le père d'Odin dans la mythologie nordique?", "answer": "Bor"}
    ],
    
    "Gastronomie": [
        {"text": "Quel fromage utilise-t-on traditionnellement pour une raclette?", "answer": "Fromage à raclette"},
        {"text": "De quel pays est originaire la paella?", "answer": "Espagne"},
        {"text": "Quel est l'ingrédient principal du guacamole?", "answer": "Avocat"},
        {"text": "Quelle est la base d'un cocktail Mojito?", "answer": "Rhum"},
        {"text": "Dans quelle ville française a été inventée la tarte Tatin?", "answer": "Lamotte-Beuvron"},
        {"text": "Quel est l'aliment principal dans un couscous?", "answer": "Semoule"},
        {"text": "De quel pays est originaire la vodka?", "answer": "Russie"},
        {"text": "Quel légume est la base du gratin dauphinois?", "answer": "Pomme de terre"},
        {"text": "Quel fromage est utilisé pour préparer une véritable pizza margherita?", "answer": "Mozzarella"},
        {"text": "Dans quelle région française trouve-t-on la bouillabaisse?", "answer": "Provence"},
        {"text": "Quel est l'ingrédient principal du houmous?", "answer": "Pois chiches"},
        {"text": "De quel pays est originaire le sushi?", "answer": "Japon"},
        {"text": "Quel fruit est la spécialité de Menton?", "answer": "Citron"},
        {"text": "Quelle est la base d'une sauce béarnaise?", "answer": "Beurre clarifié"},
        {"text": "De quel pays est originaire le tiramisu?", "answer": "Italie"},
        {"text": "Quel fruit entre dans la composition du clafoutis traditionnel?", "answer": "Cerise"},
        {"text": "Quelle est la principale épice du curry?", "answer": "Curcuma"},
        {"text": "De quelle région française est originaire le cassoulet?", "answer": "Languedoc"},
        {"text": "Quel alcool est utilisé pour flamber une crêpe Suzette?", "answer": "Grand Marnier"},
        {"text": "De quel pays est originaire la sauce chimichurri?", "answer": "Argentine"}
    ],
    
    "Jeux vidéo": [
        {"text": "Quel personnage est la mascotte de Nintendo?", "answer": "Mario"},
        {"text": "Dans quel jeu trouve-t-on les Sims?", "answer": "Les Sims"},
        {"text": "Quel est le jeu vidéo le plus vendu de tous les temps?", "answer": "Minecraft"},
        {"text": "Comment s'appelle la princesse que Mario doit sauver?", "answer": "Peach"},
        {"text": "De quelle couleur est Sonic le hérisson?", "answer": "Bleu"},
        {"text": "Quel jeu de tir a été créé par Epic Games en 2017?", "answer": "Fortnite"},
        {"text": "Quel est le nom du protagoniste de The Legend of Zelda?", "answer": "Link"},
        {"text": "Quel jeu consiste à capturer des créatures dans des Poké Balls?", "answer": "Pokémon"},
        {"text": "Quelle compagnie a créé la PlayStation?", "answer": "Sony"},
        {"text": "Dans quel jeu le personnage principal s'appelle Kratos?", "answer": "God of War"},
        {"text": "Quelle série de jeux vidéo met en scène Master Chief?", "answer": "Halo"},
        {"text": "Quel jeu de simulation de vie a été créé par Will Wright?", "answer": "Les Sims"},
        {"text": "Quel était le premier jeu vidéo de l'histoire?", "answer": "Pong"},
        {"text": "Qui est le rival de Mario?", "answer": "Bowser"},
        {"text": "Quel célèbre jeu mobile consiste à lancer des oiseaux sur des cochons?", "answer": "Angry Birds"},
        {"text": "Dans quel jeu trouve-t-on le personnage de Lara Croft?", "answer": "Tomb Raider"},
        {"text": "Quel jeu d'aventure propose de construire virtuellement avec des blocs?", "answer": "Minecraft"},
        {"text": "Quelle est la console la plus vendue de tous les temps?", "answer": "PlayStation 2"},
        {"text": "Dans quel jeu vidéo le personnage principal s'appelle Cloud Strife?", "answer": "Final Fantasy VII"},
        {"text": "Quel jeu de course propose des bananes comme armes?", "answer": "Mario Kart"}
    ]
}

def compter_questions():
    """Compte le nombre total de questions dans la base de données"""
    total = 0
    for theme, questions in questions_data.items():
        total += len(questions)
    return total

def generer_questions_manquantes(limite=1500):
    """Génère un ensemble de questions françaises pour atteindre la limite demandée"""
    total_actuel = compter_questions()
    questions_a_generer = limite - total_actuel
    
    print(f"Base de données actuelle: {total_actuel} questions")
    print(f"Nombre de questions à générer pour atteindre {limite}: {questions_a_generer}")
    print(f"Thèmes disponibles: {len(questions_data.keys())}")
    
    # Si nous avons déjà suffisamment de questions, rien à faire
    if questions_a_generer <= 0:
        print("Nombre suffisant de questions disponibles!")
        return
        
    print(f"Pour atteindre {limite} questions, vous devez:")
    print(f"1. Ajouter environ {questions_a_generer // len(questions_data.keys())} questions par thème existant")
    print(f"2. Ou créer environ {questions_a_generer // 20} nouveaux thèmes avec 20 questions chacun")
    print(f"3. Ou utiliser l'API Open Trivia Database et traduire les questions avec l'API DeepL")

if __name__ == "__main__":
    total = compter_questions()
    print(f"Base de données actuelle: {total} questions françaises")
    print(f"Nombre de thèmes disponibles: {len(questions_data.keys())}")
    
    for theme, questions in questions_data.items():
        print(f"- {theme}: {len(questions)} questions") 