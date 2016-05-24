acid
====

Ce module est la racine de notre compilateur. Il définit des opérations et des
types pour les différentes étapes du processus:

- *Tokenizing*: il s'agit du découpage du code en une liste de lexèmes.
- *Parsing*: cela consiste à regrouper nos lexèmes en un AST.

Rappel:

**Un lexème** est un bout de chaine de caractère auquel on associe un type. Ici
Je représente mes lexèmes par la classe `Token`, et leur types par l'énumération
`TokenType`.

**Un AST** (de l'anglais *Abstract Syntax Tree*, arbre de syntaxe abstraite)
est la représentation du programme avant sa compilation ou son exécution.
On appelle ça un arbre car on représente souvent le résultat sous cette forme:

```
                                                +
                     +--------+                / \
(+ (* 3 2) 7)     ---| parser |-->            *   7
                     +--------+              / \
                                            3   2
```
