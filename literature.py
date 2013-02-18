import humanize

novel_list = [("War and Peace", 587287),
	("Atlas Shrugged", 561996),
	("Lord of the Rings", 455125),
	("Gone with the Wind", 418053),
	("Bleak House", 377076),
	("Anna Karenina", 349736),
	("Middlemarch", 316059),
	("Ulysses", 262869),
	("The Idiot", 241427),
	("The Three Musketeers", 228402),
	("Crime and Punishment", 211591),
	("Moby Dick", 206052),
	("The Mill on the Floss", 205616),
	("Great Expectations", 195954),
	("Jane Eyre", 183858),
	("Catch-22", 174269),
	("The Grapes of Wrath", 169481),
	("Oliver Twist", 167543),
	("Dracula", 160363),
	("Watership Down", 156154),
	("Emma", 155887),
	("Moll Flanders", 138087),
	("Tale of Two Cities", 135420),
	("Pride and Prejudice", 120697),
	("Wuthering Heights", 107945),
	("Gulliver's Travels", 107349),
	("Anne of Green Gables", 97364),
	("The Hobbit", 95022),
	("Nineteen Eighty-Four", 561996),
	("Persuasion", 87979),
	("The Catcher in the Rye", 73404),
	("Lord of the Flies", 59900),
	("Slaughterhouse-Five", 49459),
	("The Great Gatsby", 47094),
	("Fahrenheit 451", 46118),
	("Heart of Darkness", 38098),
	("Charlie and the Chocolate Factory", 30644),
	("Animal Farm", 29966),]

def novel_text(novel, words):
	return "%s (%s)" % (novel, humanize.intcomma(words))

def readable_description(novels):
	if not novels: return "nothing"

	if len(novels) == 1:
		return novels[0]

	if len(novels) == 2:
		return "%s and %s" % (novels[0], novels[1])

	return ", ".join(novels[:-1]) + " and " + novels[-1]

def literature(total_words, novels = None):
	if not novels: novels = []

	for novel, words in novel_list:
		if words < total_words:
			novels.append(novel_text(novel, words))
			return literature(total_words - words, novels)

	return readable_description(novels)