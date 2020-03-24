import numpy as np
from colorama import Fore, Style
# Pour pouvoir afficher en rouge sur le anaconda prompt, sinon même sans ces deux lignes ca marche
# sur le git bash.
import colorama
colorama.init()


class Ruler:

    def __init__(self, string_1: str, string_2: str):
        self.str_1 = string_1
        self.str_2 = string_2
        if max(len(string_1), len(string_2)) > 3000:
            raise ValueError(
                "Pas de string de longueur plus élevée que 3000 caractères")
        self._distance = int()
        self.has_computed = False  # pour tester si l'utilisateur a bien compute
        self.first_string = f''  # les strings finaux, qu'on renvoie pour report()
        self.second_string = f''

    @property
    def distance(self):
        if not self.has_computed:
            raise NotImplementedError(
                "Make sure to run compute method before asking for distance")
        return self._distance

    @property
    def matrice_cout(self):
        '''
        Cette fonction renvoie la matrice des coûts associée aux deux str considérés.
        On prend ici par défaut une distance de +1 pour deux lettres différentes et +0 sinon.
        En bioinformatique il est agréable de pouvoir modifier les valeurs considérées, 
        c'est à dire pénaliser une différence  A-T plus que A-G par exemple. Pour faire ceci
        le plus simple est d'utiliser un dictionnaire de dictionnaire avec pour chaque lettre en 
        clé un dictionnaire en valeur avec les coûts associés. Il suffirait de changer ensuite
        la boucle avec le coût trouvé dans le dictionnaire associé à self.str_1[j-1].
        On prend le même dimensionnement que la matrice_chemin, ainsi la première ligne et 
        la première colonne sont remplies de 0.
        '''
        matrice = np.array([[0 for j in range(len(self.str_1) + 1)]
                            for i in range(len(self.str_2) + 1)], dtype=int)
        for j in range(1, len(self.str_1) + 1):
            for i in range(1, len(self.str_2) + 1):
                # 1 si pas les mêmes strings et 0 si c'est les mêmes
                matrice[i, j] = int(self.str_1[j-1] != self.str_2[i-1])
        return matrice

    @property
    def matrice_chemin(self):
        '''
        La matrice créée est une matrice chemin qui nous permettra de mettre en oeuvre la
        programmation dynamique nécessaire à la résolution 
        du problème. On utilise la matrice coût pour créé la matrice chemin.
        '''
        S = self.matrice_cout
        M = np.array([[0 for j in range(len(self.str_1) + 1)]
                      for i in range(len(self.str_2) + 1)], dtype=int)  # np.zeros marche aussi
        M[0] = [j for j in range(len(self.str_1) + 1)]

        for i in range(len(self.str_2) + 1):
            M[i, 0] = i

        # si on s'autorise itertools on peut faire ça de manière plus économe en code
        for i in range(1, len(self.str_2) + 1):
            for j in range(1, len(self.str_1) + 1):
                M[i, j] = min(
                    [M[i-1, j-1] + S[i, j], M[i, j-1] + 1, M[i-1, j] + 1])
        return M

    def compute(self, cost_insertion=1, cost_substitution=1):
        '''
        Prend la matrice chemin et la parcours, en commençant à bas à droite puis en évoluant
        vers en haut à gauche en prennant la diagonale en cas d'égalité des valeurs diag, left ou 
        up. On rentre en paramètre définis le cout d'insertion et le cout de substitution, mais 
        ceux ci peuvent être appelé lors l'appel compute
        '''
        M = self.matrice_chemin
        n1, n2 = len(self.str_2), len(self.str_1)
        pos = [n1, n2]
        first_string, second_string = '', ''

        while pos != [0, 0]:
            left = M[pos[0], pos[1]-1]
            up = M[pos[0]-1, pos[1]]
            diag = M[pos[0]-1, pos[1]-1]

            if pos[1] == 0:
                pos = [pos[0] - 1, pos[1]]
                first_string += self.str_2[pos[0]]
                second_string += '='
                self._distance += cost_insertion

            elif pos[0] == 0:
                pos = [pos[0], pos[1] - 1]
                first_string += '='
                second_string += self.str_1[pos[1]]
                self._distance += cost_insertion

            elif left <= up and left < diag:
                pos = [pos[0], pos[1] - 1]
                first_string += '='
                second_string += self.str_1[pos[1]]
                self._distance += cost_insertion

            elif up < left and up < diag:
                pos = [pos[0] - 1, pos[1]]
                first_string += self.str_2[pos[0]]
                second_string += '='
                self._distance += cost_insertion

            else:
                pos = [pos[0] - 1, pos[1] - 1]
                first_string += self.str_2[pos[0]]
                second_string += self.str_1[pos[1]]

                if self.str_2[pos[0]] != self.str_1[pos[1]]:
                    self._distance += cost_substitution
        # Il faut renverser le string car on est partit de la fin du string
        self.second_string, self.first_string, self.has_computed = second_string[
            ::-1], first_string[::-1], True

    def red_text(self, text):
        return f"{Fore.RED}{text}{Style.RESET_ALL}"

    def report(self):
        '''
        Prend les deux strings fournis par la méthode compute et colore les bouts de string qui sont différents ou les =
        rajoutés lorsqu'il y a une insertion de str.
        '''
        new = f''
        also_new = f''
        # Les deux strings font la même taille grâce aux =
        for x, y in zip(self.first_string, self.second_string):
            if y != x:
                if y == f'=':
                    new += self.red_text('=')
                    also_new += x
                elif x == f'=':
                    also_new += self.red_text('=')
                    new += y
                else:
                    new += self.red_text(y)
                    also_new += self.red_text(x)
            else:
                new += y
                also_new += x
        return new, also_new


pass
