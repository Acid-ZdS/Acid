**Caution : this page is french only**

Contributeur : [Folaefolc (alias Loodoor)](https://github.com/Loodoor)

# Convention de nommage

On préférera l'usage de CamelCase pour les lambda, et de lowerCamelCase pour les variables (qui ne sont pas des lambda).
Les fonctions de la lib standart seront en lowerCamelCase pour les différencier des lambda créées par l'utilisateur.

# Commentaires

Un commentaire monoligne s'écrira ainsi : `;commentaire`
Et un commentaire multiligne de la sorte : `/* commentaire
                                               suite du commentaire */`

# Lambda

*desc*: Une lambda en ZLang est l'équivalent d'une fonction en Python (ie).

*syntaxe*: `(lambda args body)`

*note*: `args` peut prendre 2 formes : `(arg1 arg2 argN)` ou bien `arg1 arg2 argN`.
        Pour gérer le second cas, on procéderait ainsi :
        ```py
        if len(expression) > 3 or not isinstance(expression[1], list):
            args = expression[1:-1]
            body = expression[-1]
        ```
        une lambda peut avoir des arguments par défaut. Dans ce cas elle s'écrirait ainsi :
        `(lambda (arg1 valDef1) (arg2 valDef2) (argN valDefN) body)`
        mais on peut aussi l'écrire comme suit :
        `(lambda ((arg1 valDef1) (arg2 valDef2) (argN valDefN)) body)`

# Chaines de caractères

*desc*: Simple `string`

*syntaxe*: `(quote la_chaine_ici)`

# Nombres

*desc*: Nombre entier, flottant ou complexe

*syntaxe*: `1`, `42.12`, `1i44`

# Liste

*desc*: liste d'éléments hétérogènes

*syntaxe*: `(list 1 2 3 4)`

*note*: pour faciliter la création de grandes listes, on peut envisager la création d'une lambda (dans la lib standart) qui fonctionnerait comme suit :
        ```lisp
        ; fonction
        (new range
            (lambda start stop
                (begin
                    (new _iter (lambda _list _nb _stop
                        (if
                            (!= _nb _stop)
                            (begin
                                (cons _list _nb)
                                (_iter _list (+ nb 1) _stop))
                            )))
                    (_iter (list) start stop)
                    )))
        ; usage
        (new ma_liste (range 10 15))
        (ma_liste) ; affichera (10 11 12 13 14)
        ```

# Création de variables

*desc*: Une variable en ZLang peut être un nombre (entier, flottant, complexe), une chaine de caractères, une liste, une lambda

*syntaxe*: `(new var_name value)`

*note*: `value` peut prendre plusieurs formes : `1`, `-12.44`, `(quote hello)`, `(list 1 2 3)` ...

# Conditions

*desc*: Si un statement est vrai, on exécute la partie *vraie* de l'expression, sinon la partie *fausse*

*syntaxe*: `(if cond vrai faux)`

*note*: `cond` prendra une forme comme celle-ci : `(> 4 5)`
        `vrai` et `faux` peuvent être des blocs ou bien de simples valeurs comme dans cet exemple :
        ```lisp
        (if (> 4 5) 1 0)
        ```

# Matching

*desc*: match un motif à une série d'expressions

*syntaxe*: `(match motif expr1 expr2 exprN)`

*note*: le `motif` ainsi que les expressions (ou l'expression) peuvent être des blocs ou de simples valeurs

# Entrées-Sorties (ou I/O)

*desc*: permet d'afficher quelque chose à l'écran, d'écrire dans un fichier, de récupérer un caractère entré par l'utilisateur, de lire un fichier ...

*syntaxes*:

## Affichage à l'écran

*syntaxe*: `(say texte)`

## Ecriture dans un fichier

*syntaxe*: `(open-output-file (quote filename))`

## Lecture de caractère par l'utilisateur

*syntaxe*: `(getch)`

*note*: par extension, pour lire une chaine complète jusque ce que la touche `Entrée` soit enfoncée, on peut procéder comme suit :
        (sera sûrement inclus dans la lib standart)
        ```lisp
        (new readline
            (lambda _
                (begin
                    (new chaine (list))
                    (new _iter
                        (lambda _chr
                            (if
                                (!= (ord _chr) 10)
                                (begin
                                    (cons chaine _chr)
                                    (_iter (getch))
                                ))))
                    (join (quote) (_iter (getch)))
                    )))
        ```

## Lecture d'un fichier

*syntaxe*: `(open-input-file (quote filename))`
