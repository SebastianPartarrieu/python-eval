from collections import Counter
import itertools
import heapq as hq
from functools import total_ordering


@total_ordering
class Node:

    def __init__(self, character, nb_oc):
        '''
        On implémente une class Node, qui correspond à l'objet Noeud qui contienT 4 informations:
        Le string correspondant, le nb d'occurences, le noeud à gauche et le noeud à droite
        '''
        self.character = character
        self.nb_oc = nb_oc
        self.left = None
        self.right = None

    def __eq__(self, other):
        '''
        Pour pouvoir comparer deux objets Node. 
        La comparaison est nécessaire pour établir des priorités dans nos stacks pour établir
        l'abre. Total ordering permet de ne que avoir à définir __eq__ __ne__ et __lt__ 
        au lieu de tous les comparateurs.
        '''
        if other == None:
            return -1
        elif not isinstance(other, Node):
            return -1
        return self.nb_oc == other.nb_oc

    def __ne__(self, other):
        return self.nb_oc != other.nb_oc

    def __lt__(self, other):
        return self.nb_oc < other.nb_oc

    def __repr__(self):
        '''
        Pas vraiment nécessaire
        '''
        return f'({self.character}, {self.nb_oc})'


class TreeBuilder:

    def __init__(self, text: str):
        self.text = text
        self.stack = []

    def dico_nb_oc(self):
        '''
        Renvoie le dictionnaire avec le nombre d'occurences de chaque caractère.
        '''
        res = Counter(self.text)
        dico_nb_oc = dict(res)
        return dico_nb_oc

    def creer_stack(self):
        '''
        On créer un stack, une pile en gros, mais le module heapq permet d'implémenter
        des priorités plus intéressante que FIFO ou FILO. Ce module nous permet de sortir
        les deux plus petits éléments, c'est pour cela qu'il a fallu définir la comparaison 
        entre Node!
        '''
        dico = self.dico_nb_oc()
        for x, y in dico.items():
            node = Node(x, y)
            hq.heappush(self.stack, node)

    def merge_noeuds(self, node1: Node, node2: Node):
        '''
        Vu qu'on va partir de notre dictionnaire de fréquence puis construire notre arbre en 
        remontant depuis les caractères à occurence la plus faible il faut pouvoir merger les
        noeuds entre eux pour construire un nouveau noeud.
        '''
        merge = Node(node1.character + node2.character,
                     node1.nb_oc + node2.nb_oc)
        merge.left = node1
        merge.right = node2
        return merge

    def tree(self):
        '''
        Construit un arbre binaire pour effectuer un codage de huffman sur le string du TreeBuiler.
        L'abre est une liste ordonnée de noeuds.
        '''
        self.creer_stack()
        final_tree = []
        while len(self.stack) > 1:
            node1 = hq.heappop(self.stack)
            node2 = hq.heappop(self.stack)
            hq.heappush(self.stack, self.merge_noeuds(node1, node2))
            final_tree.append(node1)
            final_tree.append(node2)
        a = hq.heappop(self.stack)
        final_tree.append(a)
        self.stack = []  # pour que plusieurs appels sur le même ojet TreeBuiler ne fausse rien
        return final_tree


pass


class Codec:

    def __init__(self, tree):
        self.encodage = {}
        self.reverse = {}
        # pour ne pas avoir des modif sur l'original.
        self.tree = [element for element in tree]

    def encode_prelim(self, noeud, encodage):
        '''
        Retourne le text encodé avec l'arbre binaire du codec.
        On utilise un algorithme récursif qui va aider à définir deux dictionnaires.
        Le premier aura en clé les caractères "de base" c'est à dire de longueur 1 et en valeur
        il aura l'encodage correspondant. Le deuxième aura l'inverse.
        '''
        if noeud is None:  # if not noeud
            return
        if noeud is not None:  # if noeud
            if len(noeud.character) == 1:
                self.encodage[noeud.character] = encodage
                self.reverse[encodage] = noeud.character
        self.encode_prelim(noeud.left, encodage + '0')
        self.encode_prelim(noeud.right, encodage + '1')

    def encode(self, text: str):
        self.encode_prelim(self.tree[-1], '')
        coded = ''
        for character in text:
            coded += self.encodage[character]
        return coded  # on aurait pu le passer en attribut pour encode_bin

    def decode(self, coded_text: str):
        decoded = ''
        code = ''
        for bit in coded_text:
            code += bit
            if code in self.reverse:
                decoded += self.reverse[code]
                code = ''
        return decoded

    def encode_bin(self, text: str):
        '''
        L'idée est que python store sur des bytes par défaut. Pour vraiment pouvoir compresser
        le fichier il faut donc prendre notre séquence encodée et la découper en portions de 8 bits
        qu'on assigne à un byte. On réduira ainsi la taille en mémoire par 8.
        Il faut cependant faire attention car notre la longueur de notre encodage n'est pas forcément 
        divisible par 8, auquel cas il faut ajouter des 0 à la fin qu'il faudra pas oublier d'enlever
        en décodant. Pour ne pas perdre l'information du nombre de 0 qu'on a rajouté, on ajoute un 
        byte à la fin avec des 0 et le nombre de 0 rajouté en binaire.
        '''
        coded = self.encode(text)
        length = len(coded)
        nb_zeros_rajoute = 8 - length % 8
        binary_encoded = bytearray()
        for _ in range(nb_zeros_rajoute):  # on rajoute les zéros au codage en string
            coded += '0'
        # le byte avec le nb de 0 rajouté
        byte_avec_info = "{0:08b}".format(nb_zeros_rajoute)
        coded = byte_avec_info + coded

        for i in range(0, len(coded)//8, 8):  # on passe en format byte
            current_byte = coded[i:i+8]
            # rajouter sur un seul byte
            binary_encoded.append(int(current_byte, base=2))
        return binary_encoded

    def decode_bin(self, code: bytearray):
        '''
        Le decodage est assez complexe.
        '''
        pass


pass
