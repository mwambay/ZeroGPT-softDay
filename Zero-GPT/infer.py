"""
This code a slight modification of perplexity by hugging face
https://huggingface.co/docs/transformers/perplexity

Both this code and the orignal code are published under the MIT license.

by Burhan Ul tayyab and Nicholas Chua
"""

from model import GPT2PPL

# initialize the model
model = GPT2PPL()

sentence = """"

Introduction
 Compléments	VBA	et	compléments	Office
 Avec	Office	2013,	Microsoft	a	introduit	un	nouveau	type	de	compléments,	les
 compléments	Office.	Contrairement	à	ceux	développés	en	VBA,	les
 compléments	Office	ne	sont	pas	installés	sur	l’ordinateur	de	l’utilisateur,	mais
 hébergés	sur	un	serveur	distant	à	partir	duquel	ils	s’exécutent.	Ils	sont
 développés	à	partir	de	technologies	Web,	telles	que	HTML	5,	JavaScript,	CSS
 3,	XML	et	des	API	REST.
 En	termes	d’expérience	utilisateur,	les	compléments	Office	s’apparentent	à	des
 applications	mobiles	auxquelles	on	s’abonne	via	l’Office	store	et	s’exécutent
 systématiquement	dans	un	panneau	qui	leur	est	dédié.	Cependant,	si	vous
 souhaitez	développer	des	solutions	professionnelles	dans	le	cadre	d’une
 entreprise	et	non	dans	le	but	de	les	commercialiser	via	l’Office	store,	VBA
 reste	presque	toujours	la	solution	la	plus	simple	et	la	plus	souple	à	mettre	en
 œuvre	et	à	déployer.
 VBA,	pour	quoi	faire	?
 Excel	offre	des	possibilités	très	étendues.	Pourtant,	quelle	que	soit	la	puissance
 de	ses	fonctions,	elles	ne	peuvent	répondre	à	toutes	les	situations.	La
 programmation	VBA	est	la	solution	de	personnalisation	offerte	par	Excel,	afin
 d’ajouter	des	caractéristiques,	des	fonctions	et	des	commandes	qui	répondent
 précisément	à	vos	besoins.
 La	programmation	VBA	peut	être	définie	comme	la	personnalisation	d’un
 logiciel	afin	de	s’assurer	gain	de	temps,	qualité	des	documents	et	simplification
 des	tâches	complexes	ou	fastidieuses.	Voici	quelques	exemples	de	ce	que
 permettent	les	programmes	VBA	:
 • Combiner	un	nombre	indéterminé	de	commandes.	Nous	sommes	souvent
 amenés	à	répéter	ou	à	associer	certaines	commandes	plutôt	que	d’autres	et	à
 ignorer	certaines	fonctionnalités	selon	l’usage	personnel	que	nous	avons
 d’un	logiciel.	VBA	permet	d’associer	un	nombre	illimité	de	commandes	à
 une	seule.	Vous	pouvez	ainsi	ouvrir	simultanément	plusieurs	documents
 Excel	stockés	dans	des	dossiers	ou	sur	des	serveurs	différents,	y	insérer	des
"""

with open("teste_NoGPT.txt", "r") as f:
    sentence = f.read()
    f.close()
    
print(model(sentence))
