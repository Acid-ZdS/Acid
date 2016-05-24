**CAUTION : This page is in french only**

# Acid : Spec V1 (par [Dominus Carnufex](https://zestedesavoir.com/membres/voir/Dominus%20Carnufex/))

> ## Les lambdas
> 
> À mon avis, le cœur d'un langage essentiellement fonctionnel, et donc la première chose à définir, ce sont les lambdas, ou fonctions anonymes. Une lambda serait définie par le mot-clé `lambda`, une liste d'arguments, et un corps de fonction. Par exemple, une lambda qui additionne les carrés de deux nombres prendrait la forme suivante.
> 
> ```lisp
> (lambda (x y) (
>     (+ (* x x) (* y y))
> ))
> ```
> 
> Pourquoi définir des lambdas plutôt que des fonctions ? Pour deux raisons. Premièrement, parce qu'un langage fonctionnel puissant se doit de pouvoir passer une fonction en argument à une autre fonction, et renvoyer des fonctions : ces fonctions n'ont pas nécessairement besoin d'être nommées, et il est plus simple d'avoir un mot-clé pour définir une lambda, et un autre pour donner un nom à un objet, qu'un mot-clé pour les fonctions avec un nom, et un autre pour les fonctions anonymes.
> 
> Deuxièmement, parce que par leur seul présence, on donne la possibilité d'utiliser des fonctions curryfiées (c'est-à-dire ayant déjà reçu une partie de leurs arguments). Par exemple, la fonction curryfiée `(-1)` de Haskell se traduirait en Acid par ce code.
> 
> ```lisp
> (lambda x (- x 1))
> ```
> 
> ## Le nommage
> 
> Ce n'est pas tout de dire qu'on va avoir des fonctions nommées, encore faut-il avoir le mot-clé pour le faire. Celui-ci est tout trouvé : `define`, suivi d'un nom, puis d'un objet à nommer (qui pour l'instant, ne peut être qu'une lambda).
> 
> ```lisp
> (define carrédelhypothénuse (lambda (x y) (
>     (+ (* x x) (* y y))
> )))
> ```
> 
> ## Les types natifs
> 
> Pour un certain nombre de types, il est plus facile de les définir nativement. À priori, les types natifs suivants suffisent :
> 
> - `Int` ;
> - `Int8`, `Word8`, `Int16`, etc. ;
> - `Float` et `Double` ;
> - `Char` (qui représente un caractère Unicode, par un entier sur 8 bits) ;
> - `tuple …` (par exemple, `(tuple Int Char Word64)`).
> 
> Comme on le verra un peu plus loin, on peut se passer de définir des booléens nativement, on pourra le faire dans la bibliothèque standard. Idem pour les chaînes de caractères, qui seront définis à partir du type liste chaînée qu'on définira dans la bibliothèque standard.
> 
> ## Les types algébriques
> 
> Pour ceux qui ne seraient pas familiers de la programmation fonctionnelle, les types algébriques sont un moyen de définir n'importe quel type très simplement par une combinaison de deux procédés :
> 
> - les types produits, qui ne sont rien d'autre que des tuples nommés, par exemple `Point Double Double` (c'est du Haskell, comprendre, un `Point` est la réunion de deux `Double`) ;
> - les types sommes, qui permettent à un type de prendre plusieurs formes (on dit qu'il a plusieurs constructeurs). D'où l'exemple suivant, toujours en Haskell.
> 
> ```haskell
> data Bool = False | True
> ```
> 
> Il faut comprendre, un `Bool` peut-être soit un `False`, soit un `True`. Et là où cela devient vraiment puissant, c'est qu'on peut combiner les deux. Voici comment une liste chaînée est usuellement définie.
> 
> ```haskell
> data List a = Nil | Cons a (List a)
> ```
> 
> En français : une liste de `a` (`List` est un type paramétré, on peut mettre n'importe quoi dedans) est, soit une liste vide appelée `Nil`, soit un `Cons`, qui est la réunion d'un `a` et d'une liste de `a`.
> 
> Pour définir un type, on doit définir un ou plusieurs constructeurs, prenant des types en paramètres. Le type lui-même peut prendre des paramètres, qui peuvent ensuite être utilisés dans les constructeurs. Voici le type `Option` du Rust, tel qu'il serait défini en Acid.
> 
> ```lisp
> (define Option (type a (
>     None
>     (Some a)
> )))
> ```
> 
> ## Le filtrage par motifs
> 
> Pas de grande difficulté là-dedans, une commande `match`, qui prend une expression, et une série de combinaisons valeur / motif + corps de fonction. Par exemple, une fonction qui fait la somme des éléments d'une liste.
> 
> ```lisp
> (define somme (lambda liste (
>     match liste (
>         (Nil 0)
>         ((Cons val suite) (+ val (somme suite)))
>     )
> )))
> ```
> 
> C'est pour cette raison qu'on peut se contenter de définir dans la bibliothèque standard un type `Bool` plutôt que d'en faire un type natif. Ce qui en Haskell s'exprimerait comme `if x < 3 then x + 2 else x - 6` peut s'exprimer en zLang comme suit.
> 
> ```lisp
> match (< x 3) (
>     (True (+ x 2))
>     (False (- x 6))
> )
> ```
> 
> Une question qui reste posée est la suivante : faut-il qualifier les constructeurs ? C'est-à-dire que, quand on l'utilise en dehors de sa définition même, doit-on écrire `Bool::True` (syntaxe de Rust) ou simplement `True` (syntaxe de Haskell) ? Dans la plupart des cas, la première solution est la plus pratique : ça permet d'avoir plusieurs types qui ont un constructeur portant le même nom, comme `None`. Mais pour quelques types (comme les booléens), c'est vraiment plus simple de donner le constructeur directement.
> 
> Quatre solutions possibles.
> 
> 1. Les constructeurs sont toujours qualifiés.
> 2. Les constructeurs ne sont jamais qualifiés (Haskell).
> 3. Les constructeurs sont qualifiés par défaut et un mot-clé supplémentaire permet de déqualifier les constructeurs d'un type donné.
> **4. Les constructeurs sont qualifiés par défaut mais le mot-clé permettant d'importer dans l'espace de nom courant le contenu d'un module permet d'importer les constructeurs d'un type donné, traité comme s'il était un module (Rust).** (Solution choisie d'office)
> 
> Je préfère la dernière solution, même si le mot-clé en question ne deviendra vraiment utile que si l'on finit par ajouter un système de modules.
> 
> ## Les contraintes de types
> 
> Comment dire qu'une fonction doit avoir un type donné ? Ou qu'une expression donnée au sein d'une expression plus vaste doit avoir un type donné ? À l'aide du mot-clé `hastype`, qui s'utilisera de deux façons différentes, comme par exemple, ce qui suit.
> 
> ```lisp
> (hastype (Double -> Double -> Double) carrédelhypothénuse)
> 
> (lambda x (+ x (hastype Word8 42)))
> ```
> 
> Le premier est pour les éléments qui ont un nom, le second pour les éléments anonymes.
> 
> ## Les entrées-sorties
> 
> Si on reste très basiques, on peut se contenter de deux fonctions, `getchar` et `putchar`. La principale difficulté, c'est quel type donner à ces fonctions ? Comment faire pour exécuter plusieurs de ces instructions à la suite, comme dans un langage impératif. Il existe une multitude de solutions possibles, n'impliquant pas nécessairement une monade. Je vous laisse y réfléchir. :)
> 
> ## Un peu de méta
> 
> Bon, c'est cool le filtrage par motif, mais la syntaxe utilisée pour une simple condition n'est vraiment pas intuitive, on préférerait avoir `if condition cas_true cas_false`. Eh bien, c'est tout à fait possible. On pourrait définir ceci dans la bibliothèque standard.
> 
> ```lisp
> (hastype (Bool -> a -> a -> a) if)
> 
> (define if (lambda (cond cas_true cas_false) (
>     match cond (
>         (True cas_true)
>         (False cas_false)
>     )
> )))
> ```
> 
> Mais ce n'est pas toujours possible ainsi. Comment définir un mot-clé `function` qui prend un nom, une liste d'arguments et un corps de fonction, et qui en fait une combinaison de `define` et de `lambda` ? Je n'ai pas encore trouvé de solution satisfaisante, alors je vous invite à y réfléchir. ([Merci de donner votre avis sur le forum](https://zestedesavoir.com/forums/sujet/6129/acid-le-lisp-like-de-la-communaute/))
> 
> ## Des commentaires
> 
> Le système du C/C++ avec `//` et `/* */` me paraît très bien.
> 
> # Ce que doit faire l'interpréteur / compilateur
> 
> - Vérifier qu'il n'y a aucune erreur de syntaxe pure (manque une parenthèse, etc.).
> - Vérifier que tous les noms utilisés ont été définis à un endroit qui les rend visibles à l'endroit où ils sont utilisés.
> - Vérifier que toutes les fonctions définies au niveau du programme ont une déclaration de type quelque part.
> - Vérifier que les déclarations de type sont cohérente entre elles.
> - Interpréter / compiler.
Source:[Dominus Carnufex](https://zestedesavoir.com/forums/sujet/6065/un-petit-langage-zds/?page=7#p111399)

Le message original à été annoté et les évocations à un autre nom de langage ont été remplacées par Acid. Cette proposition à été choisie comme base à la réalisation de Acid.

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

