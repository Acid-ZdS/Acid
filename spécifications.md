# Généralités

**(1)** La présente spécification d’Acid n’intègre que les fonctionnalités de base, indispensables au fonctionnement du langage. Un ensemble de syntaxes améliorant la lisibilité, appelé sucre syntaxique, sera défini ultérieurement.

**(2)** Un code source Acid est composé d’une succession d’expressions, dont l’ordre n’est pas significatif. Une expression est entourée de parenthèses, et peut être constituée de :

- au plus un mot-clé, nécessairement en première position de l’expression, par exemple `lambda` ;
- des identifiants, par exemple `acid` ;
- des valeurs littérales, par exemple `42` ;
- des expressions.

Lorsqu’une expression ne contient qu’un seul élément, ne contenant lui-même pas d’espace, les parenthèses qui l’entourent peuvent être omises.

Voici un exemple de code source Acid, contenant deux expressions.

```lisp
(hastype if (lambda (Bool a a) a))

(define if (lambda (cond if_true if_false) (
    match cond (
        (True if_true)
        (False if_false)
    )
)))
```

**(3)** Les implémentations Acid sont tenues d’accepter les codes sources encodés en UTF-8.

**(4)** Tout code contenu entre les caractères `/*` et `*/` ou entre les caractères `//` et la fin de la ligne est ignoré.

# Lambdas

**(5)** Une lambda est un objet prenant aucun, un ou plusieurs arguments et renvoyant une valeur de retour, selon un traitement toujours identique, et défini dans le corps de la lambda.

**(6)** Une lambda est définie au moyen d’une expression comprenant trois éléments : le mot-clé **`lambda`**, une expression contenant la liste des identifiants des arguments de la lambda, et une expression décrivant le corps de la lambda.

**(7)** Si la lambda ne prend aucun argument, le mot-clé et la liste d’arguments peuvent être omis. S’ils sont conservés, la liste d’arguments est représentée comme une simple paire de parenthèses.

**(8)** Une lambda est appelée au moyen d’une expression contenant la définition de la lambda, ou son identifiant lorsqu’il existe, suivie par les différents arguments que l’on veut lui passer, chacun sous la forme d’une expression.

Voici un exemple de définition d’une lambda, qui appelle une lambda nommée, et un exemple de lambda directement appelée.

```lisp
// Lambda non nommée.
(lambda x (lambdanommée x 42))

/* Appel direct de lambda non nommée. */
((lambda (x y) (+ x y)) 34 57)
```

# Types

**(9)** Acid possède une liste limitée de types natifs.  
**(9.1)** Les types entiers se répartissent en trois catégories :

- le type `Int`, qui correspond à un entier signé sans limite de taille ;
- les types `Int8`, `Int16`, `Int32` et `Int64`, qui correspondent à des entiers signés tenant respectivement dans 8, 16, 32 et 64 bits ;
- les types `Word8`, `Word16`, `Word32` et `Word64`, qui correspondent aux équivalents non signés des précédents.

**(9.2)** Les types flottants sont `Float` pour les flottants simple précision, et `Double` pour les flottants double précision.  
**(9.3)** Les caractères, de type `Char`, peuvent couvrir l’ensemble des caractères Unicode.  
**(9.4)** Les tuples sont la réunion ordonnée d’un nombre fixe de valeurs de types potentiellement différents. L’identifiant de leur type est composé du mot-clé **`tuple`** suivi de chacun des identifiants des types inclus, le tout entre parenthèses, par exemple `(tuple Int Char (tuple Char Char))`. Un tuple vide a par conséquent le type `(tuple)`.  
**(9.5)** L’identifiant du type des lambdas est composé du mot-clé **`lambda`**, suivi d’une expression contenant la liste des identifiants des types des arguments, puis de l’identifiant du type de la valeur de retour, le tout entre parenthèses, par exemple `(lambda (Char Char) Int)`. Dans le cas d’une lambda sans paramètre, n’ayant qu’une valeur de retour, la lambda a le même identifiant de type que sa valeur de retour.

**(10)** Dans les valeurs littérales de type flottant, la séparation entre partie entière et partie décimale est marquée par un point.

**(11)** Les valeurs littérales de type `Char` sont entourées de guillemets droits simples, par exemple `'a'`.

**(12)** Les tuples sont des expressions, définies par le mot-clé `tuple`, suivi d’expressions ou de valeurs littérales, par exemple `(tuple 'a' 'b' (+ 1 41))`.

**(13)** Un type algébrique est défini par une expression, contenant :

- le mot-clé **`type`** ;
- une liste de paramètres, qui peut être omise si elle est vide ;
- une liste de constructeurs, chacun constitué d’un identifiant et, si nécessaire, d’une liste d’identifiants de types que le constructeur prend en argument.

Par exemple, le code suivant définit une liste chaînée simple, avec un paramètre de type.

```lisp
(type a (
    Nil
    (Cons a (List a))
))
```

**(14)** En dehors de sa définition, un constructeur doit être précédé de l’identifiant de son type, et du caractère `::` ou `⸪`. Par exemple, si le type précédent s’appelle `List`, on n’écrira pas `Nil`, mais `List::Nil`.

**(15)** Il est possible de signaler explicitement le type d’un objet au moyen d’une contrainte de type. Celle-ci est une expression composée du mot-clé **`hastype`**, de l’objet ou de son identifiant, et d’un identifiant de type, par exemple, `(hastype 42 Word64)`.

**(16)** La présence d’une contrainte de type est obligatoire pour les lambdas nommées.

# Filtrage par motifs

**(17)** Un filtrage par motifs est une expression, composée de :

- le mot-clé **`match`** ;
- une expression dont la valeur sera comparée aux motifs ;
- une liste de motifs, composés eux-mêmes d’un constructeur ou d’une valeur, suivi d’une expression à évaluer si la valeur correspond au motif.

Voici un exemple de filtrage par motif sur le type de liste donné en exemple au point 13.

```lisp
match xs (
    (Nil 42)
    ((Cons x next) (+ x 79))
)
```

**(18)** Si l’on ne veut pas lier un élément d’un motif à un identifiant, on remplace ce dernier par le masque `_`.

Par exemple, dans le code précédent, `next` n’est pas utilisé dans l’expression à évaluer. Il serait donc plus judicieux d’écrire ce qui suit.

```lisp
match xs (
    (Nil 42)
    ((Cons x _) (+ x 79))
)
```

**(19)** Tous les motifs d’un filtrage doivent avoir le même type en entrée et en sortie. En outre, les motifs fournis doivent couvrir l’ensemble des valeurs possibles pour le type d’entrée. Si besoin, le motif générique `_` peut être utilisé pour obtenir cette complétude.

**(20)** Les motifs sont comparés à la valeur de référence successivement, dans l’ordre où ils apparaissent dans le code.

# Identifiants

**(21)** Associer un identifiant à un objet se fait au moyen d’une expression, composée du mot-clé **`define`**, de l’identifiant à associer, et de l’objet.

Voici un exemple de lambda nommée.

```lisp
(define neq (lambda (xs ys) (
    not (eq xs ys)
)))
```

Il est ainsi possible de créer des synonymes de types, comme suit.

```lisp
(define String (List Char))
```

**(22)** Un identifiant peut être composé de n’importe quelle suite de caractères Unicode, aux exceptions suivantes près.

- L’identifiant ne doit pas contenir de caractère d’espacement (sauf dans le cas des identifiants de types de tuples ou de lambdas, car ils sont entourés de parenthèses).
- L’identifiant ne doit pas contenir les caractères `(`, `)`, `//`, `/*`, `/*`.
- L’identifiant ne doit pas commencer et finir à la fois par le caractère `'`.
- L’identifiant ne doit pas être composé exclusivement de chiffres, ou de chiffres et d’un unique point.
- L’identifiant ne doit pas être un des mots-clés du langage, à savoir `abort`, `define`, `getchar` `hastype`, `lambda`, `match`, `putchar`, `tuple`, `type`, `_`, ni un des types prédéfinis.
- Les implémentations peuvent définir des mots-clés ou symboles de syntaxe supplémentaires, pour les besoins du sucre syntaxique, qui ne devront alors pas être utilisés comme identifiants.

**(23)** Un identifiant de lambda ou de type est visible dans l’intégralité du code source. Un identifiant de variable est visible dans l’expression où la variable a été définie et ses sous-expressions. Si un identifiant de variable existe déjà comme identifiant de lambda, il remplace celui-ci dans tout son champ de visibilité.

**(24)** Un module est constitué de l’ensemble des expressions contenues dans un fichier source donné. Il porte pour identifiant le nom du fichier, ou le nom du dossier qui le contient si le fichier s’appelle `mod.acid`.

**(25)** Un type ou une lambda nommée définis dans un module peuvent être utilisés dans un autre module, à condition de faire précéder son identifiant des identifiants de toute la hiérarchie de modules permettant d’y accéder, chacun séparé par le caractère `::` ou `⸪`.

Par exemple, si on a un fichier `Data/Bool.acid` contenant le code suivant…

```lisp
(hastype not (lambda Bool Bool))

(define not (lambda bool (
    match bool (
        (True False)
        (False True)
    )
)))
```

… dans un autre code source, on peut appeler cette lambda sous la forme `Data::Bool::not`. Il est ainsi possible de définir des lambdas et types ayant le même identifiant, mais dans des modules séparés, car chacun aura un identifiant qualifié différent.

**(26)** Si un type est défini dans un module portant le même identifiant, l’identifiant du module est omis dans l’identifiant qualifié du type et de ses constructeurs. Par exemple, si le type de liste précédemment défini se trouve dans un fichier `List.acid`, l’identifiant qualifié de son premier constructeur est `List::Nil` et non `List::List::Nil`. De même, dans ce module et dans lui seul, les constructeurs peuvent être utilisés seuls.

**(27)** Si une lambda utilise des types paramétrés (par exemple, `List a`), on peut appeler une fonction du module portant le même identifiant que le type d’identifiant inconnu (ici, `a`) à l’aide du préfixe `Type::identifiant_du_paramètre::`. Par exemple, pour une lambda qui prend en argument un `List a`, si on l’appelle sur un `List Bool`, alors `Type::a::eq` appellera `Bool::eq`.

**(28)** Un module peut être lié statiquement ou dynamiquement au code source principal. Dans ce dernier cas, le code source du module peut ne contenir que les définitions de type, et les contraintes de types des lambdas nommées. On parle alors de fichier d’en-tête.

**(29)** Les identifiants de module, de type et de constructeur doivent commencer par une majuscule. Les autres identifiants doivent commencer par une minuscule.

# Entrées-sorties

**(30)** La lambda `putchar` prend en entrée un caractère, affiche ce caractère, et renvoie un `(tuple)`. La lambda `getchar` lit un caractère fourni par l’utilisateur, et le renvoie sous la forme d’un `Char`.

**(31)** La lambda `abort` est particulière : aux yeux du vérificateur de types, elle renvoie n’importe quel type en sortie, en fonction de l’endroit où elle est appelée. Elle prend une chaîne de caractères en entrée, et met fin au programme en affichant cette chaîne de caractères.

**(32)** Tout programme destiné à être exécuté (donc pas une bibliothèque), contient une lambda nommée de type `(tuple)`, par laquelle l’exécution du programme commencera. Sauf indication contraire fournie au compilateur ou à l’interpréteur, cette lambda est appelée `main`.

**(33)** Un certain nombre de lambdas ne peuvent pas être raisonnablement décrites dans la bibliothèque standard d’Acid, et doivent donc être gérées nativement par l’implémentation.

- Les opérations d’égalité (`eq`) et inégalité (`neq`) sur tous les types prédéfinis, à l’exception des lambdas.
- Les opérations de comparaison (`lt` pour inférieur, `le` pour inférieur ou égal, `gt` pour supérieur, `ge` pour supérieur ou égal) pour ces mêmes types.
- Les opérations arithmétiques de base (`+`, `-`, `*`, `negate`) pour tous les types numériques.
- Les opérations de division et de modulo sous leurs nombreuses formes :
    - `/` prend deux entiers ou deux flottants et renvoie un flottant (un `Double` si des entiers sont fournis en entrée).
    - `div` et `quot` prennent deux entiers et procèdent à leur division entière : la première arrondit vers −∞, la seconde vers 0.
    - `mod` et `rem` renvoient le reste de la division entière, avec les mêmes arrondis que ci-dessus.
- Les opérations bit à bit (`and`, `or`, `xor`, `not`, `shiftL`, `shiftR`) pour tous les types entiers bornés.
- Les opérations sur les réels trop difficiles à calculer (`exp` l’exponentielle, `ln`, `sqrt`, `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `sinh`, `cosh`, `tanh`) pour tous les types flottants.
- Les opérations de conversion entre un caractère et sa représentation UTF-8 (`ord`, `chr`), pour les `Char` et les `Word32`, respectivement.

# Évolutions futures

Le système d’entrées-sorties est assez mauvais, et pourra être radicalement transformé dans une prochaine version du langage. D’autres éléments pourront être ajoutés, comme un système de FFI ou un système de macros.
