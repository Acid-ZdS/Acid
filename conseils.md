**CAUTION : This page is in french only**

### La "compilation" en AST Python (par [nohar](https://zestedesavoir.com/membres/voir/nohar/))

> Vous pouvez tout à fait écrire votre langage et son compilateur *de telle manière qu'il soit convertit en bytecode Python*, et ainsi qu'il s'exécute dans l'interpréteur CPython.
> 
> Les avantages à cela sont multiples : 
> 
> - se concentrer dans un premier temps sur la syntaxe et la sémantique du langage, donc uniquement la partie *frontale* du compilateur, sans s'emmerder à écrire un interpréteur en parallèle, donc se concentrer sur l'essentiel, la sortie du compilateur étant un AST python standard,
> - Pouvoir tirer partie des builtins de Python et des modules de sa bibliothèque standard le temps de développer la bibliothèque de votre langage dans votre langage,
> - Rendre votre langage immédiatement compatible avec C, C++, Rust, etc. en vous servant du mécanisme de binding ou du module `ctypes` de Python, sans vous péter les dents sur une passerelle codée a la mano.
> 
> En somme, l'idée est de se servir de Python comme échafaudage.
Source:[nohar](https://zestedesavoir.com/forums/sujet/6129/acid-le-lisp-like-de-la-communaute/?page=2#p111562)

En résumé :

> L'idée est en-gros de convertir le code Acid en AST Python, de manière à qu'il soit possible de l'exécuter dans l'interpréteur Python. Dans ce cas, peut importe les implémentations (qui ne feraient "que" traduire Acid en AST Python) l'exécution aurait toujours lieu au même endroit.
Source:[the_new_sky](https://zestedesavoir.com/forums/sujet/6129/acid-le-lisp-like-de-la-communaute/?page=3#p111708)

