# Copyright 2024 F. Dorfner
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the “Software”),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software
# is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
###-----------------------------------------------------------------#

from sys import argv
from random import *
from math import sqrt,factorial
import numpy as np

def reader(filepath):
    file = open(filepath)
    rows = file.read().split("\n")
    pts = []

    n = int(rows[0])
    for row in rows[1:-1]:
        point = [e for e in
                row.replace("\t"," ").split(" ") if e != '']
        pts += [ [ int(point[1]) , int(point[2]) ] ]

    return pts,n

###-----------------------------------------------------------------#

# Returns a copy of t with elements of index i & j swapped
def swap(t, i, j):
    copy = t.copy()
    copy[i], copy[j] = copy[j], copy[i]
    return copy

# i < j
# pops element of index j from t and inserts it at index i
def reinsert(t, i, j):
    item = t[j]
    for k in reversed(range(i, j)):
        t[k+1] = t[k]
    t[i] = item

def dist(p1, p2):
    x1,y1 = p1[0],p1[1]
    x2,y2 = p2[0],p2[1]
    return sqrt( (x1-x2)**2 + (y1-y2)**2 )

# x < size!
# Associe à tout nombre x <size! une permutation de (0,1,...size)
# (Bijection de [0, size!] vers toutes les permutations de (0,1...size))
def int_to_permutation(x, size):
    p = []
    set = list(range( size ))

    for i in reversed(range(size)):
        d = factorial(i)

        index = x // d
        p += [ set[index] ]
        x %= d
        del set[index]

    return p

###-----------------------------------------------------------------#

def new_init_sol(n):
    s = list(range(n))
    for i in range(n):
        j = randint(0,n-1)
        s[i], s[j] = s[j], s[i]
    return s

def value(s, pts, n):
    sum = dist([0,0], pts[ s[0] ])

    for i in range(n-1):
        index_from = s[i]
        index_to = s[ i+1 ]
        sum += dist( pts[index_from] , pts[index_to] ) 

    sum += dist(pts[ s[-1] ], [0,0])
    return sum

# NB: On s'arrete avant n-2 au lieu de avant n-1 dans "for i..." car
#  lors de la dernière itération (cad lorsque i == n-2), j va itérer
#  de n-2+1 == n-1 à n non inclus, donc il n'y aura à chaque fois
#  qu'une itération de la boucle de j.
#   On utilise alors cette dernière itération comme valeur initiale
#  de min.
def best_neighbor_swap(s, pts, n, taboo=[]):
    neigh = swap(s, n-2, n-1)
    min = value(neigh, pts, n)
    best_neigh = neigh

    nb_neigh = (n**2 - n)//2
    nb_skipped_neigh = 0

    for i in range(n-2):
        for j in range(i+1, n):
            neigh = swap(s,i,j)

            if any(n == neigh for n in taboo):
                nb_skipped_neigh +=1
                if (nb_skipped_neigh == nb_neigh):
                    return []
                continue

            neigh_val = value(neigh, pts, n)
#            print(neigh)
            if ( neigh_val < min ):
                min = neigh_val
                best_neigh = neigh

    return best_neigh

# NB: même explication que pour best_neighbor_swap()
# NB2: Comme on garde le dernier voisin (cur_neigh) durant toute
#  la boucle qui itère sur j, il suffit de réinsérer l'élément de
#  l'indexe j à l'indexe i, et tout le reste de la séquence est déjà
#  inversée sur le segment.
def best_neighbor_opt(s, pts, n, taboo=[]):
    cur_neigh = s.copy()
    reinsert(cur_neigh, n-2, n-1)

    min = value(cur_neigh, pts, n)
    best_neigh = cur_neigh.copy()

    nb_neigh = (n**2 - n)//2
    nb_skipped_neigh = 0

    for i in range(n-2):
        cur_neigh = s.copy()
        for j in range(i+1, n):
            # update de cur_neigh
            reinsert(cur_neigh, i, j)

            if any(n == cur_neigh for n in taboo):
                # print(cur_neigh, "skipped")
                nb_skipped_neigh +=1
                if (nb_skipped_neigh == nb_neigh):
                    return []
                continue

            neigh_val = value(cur_neigh, pts, n)
            # print("------Voisin de", s, cur_neigh, int(neigh_val))
            if ( neigh_val < min ):
                min = neigh_val
                best_neigh = cur_neigh.copy()

    return best_neigh

def steepest_hill_climbing(pts, n, max_depl,
                           best_neigh_fct=best_neighbor_swap, initial_sol=[]):
    # pour simplifier la lecture
    def f(sol): return value(sol, pts, n)

    # pour shc_restart()
    if (initial_sol == []):
        s = new_init_sol(n)
    else:
        s = initial_sol

    for i in range(max_depl):
        sp = best_neigh_fct(s, pts, n)

        if ( f(sp) < f(s) ):
            s = sp
        else:
            break
    
    return s,i

###-----------------------------------------------------------------#

# Renvoies un batch de solutions aléatoires toutes uniques
def rand_initial_sols(num, size):
    # Si la taille des sol est de plus de 24, sélectionner des
    # vals aléatoires parmis 2^solsize (> 10E6) solutions
    # sera trop long, mais alors, il est aussi raisonnable
    # de s'attendre à ce qu'en sélectionnant indépendemment numsample 
    # échantillon parmis 2^solsize vals possible
    # nous n'aurons très probablement pas de doublons
    # (car numsample << 2^solsize)
    if (size > 24):
        sols = []
        for i in range(num):
            isol = new_init_sol(size)
#            while any(isol.all == s.all for s in sols):
#                isol = new_init_sol(size)
            sols += [ isol ]

        return sols
    ###-------------------------------------------------------------#

    range_solutions = range( factorial(size) )

    #random.choice nous permet d'avoir num solutions différentes
    # mais que sous forme d'entiers
    integer_sols = np.random.choice(range_solutions,
                size = num, replace=False)
    
    # on convertit ces entiers en séqences
    sols = []
    for sol in integer_sols:
        sols += [ int_to_permutation(sol, size) ]

    return sols

# Steepest hill climbing avec redémarrage
def shc_restart(pts, n, max_depl, max_essais,
                best_neigh_fct=best_neighbor_swap,
                output=False):
    # pour simplifier la lecture
    def f(sol): return value(sol, pts, n)

    # pour simplifier la lecture
    def output_info(code):
        if (not output):
            return

        match code:
            case 0:
                print("SHC with restart")
                print("First solution:", best_sol)
                print()
                output_info.cpt = 0
            case 1:
                print("Essai no", output_info.cpt)
                print("Sol initiale :", initial_sol)
                print("Sol atteinte :", s)
                print("Valeur :", f(s))
                print("Nb de déplacements :", nb_depl)
                print("---")
                output_info.cpt +=1
            case 2:
                print()
                print("Meilleure solution trouvée :", best_sol)
                print("Valeur :", f(best_sol))
                print("Distance parcourue :", best_nb_depl)
                print()
            case _: return
    
    initial_sols = rand_initial_sols(max_essais+1, n)

    best_sol = initial_sols[0]
    best_nb_depl = -1

    output_info(0)

    for initial_sol in (initial_sols[1:]):
        s,nb_depl = steepest_hill_climbing(pts, n, max_depl,
                                     best_neigh_fct, initial_sol)

        output_info(1)

        if (f(s) < f(best_sol)):
            best_sol = s
            best_nb_depl = nb_depl
    
    output_info(2)

    return best_sol

###-----------------------------------------------------------------#

# Steepest hill climbing avec une liste tabou
def shc_taboo(pts, n, max_depl, taboo_size,
                           best_neigh_fct=best_neighbor_opt,
                           initial_sol=[]):
    # pour simplifier la lecture
    def f(sol): return value(sol, pts, n)

    tab = []
    
    # pour shc_restart()
    if (initial_sol == []):
        s = new_init_sol(n)
    else:
        s = initial_sol

    # print("Depart", s, f(s))
    for i in range(max_depl):
        # print("Deplacement", i)
        sp = best_neigh_fct(s, pts, n, taboo=tab)

        # best_neigh_opt et best_neigh_swap renvoient une séquence vide si
        # aucun voisin non tabou n'a été trouvé
        if (sp == []):
            break
        
        tab += [ s ]
        if (len(tab) > taboo_size):
            del tab[0]
        
        if ( f(sp) < f(s) ):
            s = sp
        else:
            break

    return s,i,tab




###-----------------------------------------------------------------#

### pour du debug, n'est plus à jour
# def test_shc(pts, n, nb_it, with_restart=True,
#             best_neigh_fct=best_neighbor_swap, nb_restart=10):
#     print("======== Tests avec", best_neigh_fct.__name__, "===========\n")
#     for max_depl in nb_it:
#         if with_restart:
#             # On initialise sols, une liste de solutions initiales toutes
#             # différentes
#             sols = rand_initial_sols(nb_restart, n)
#             sol = shc_restart(pts,n,max_depl,
#                                            best_neigh_fct=best_neigh_fct,
#                                            nb_restart=nb_restart,
#                                            initial_sols=sols,
#                                            output=True)

#         else: sol,nb_depl = steepest_hill_climbing(pts,n,max_depl,
#                                            best_neigh_fct=best_neigh_fct)

#         print("SHC avec", max_depl, "max déplacements")
#         print("Résultat :", sol)
#         print(value(sol,pts,n))
#         if (not with_restart): print("\tArreté après", nb_depl, "deplacements")
#         print()

if __name__ == '__main__':
    if (len(argv) != 2):
        print("usage: python3", argv[0], "<filepath>")
        exit()
    
    points,n = reader(argv[1])
    
    # output_everything = True
    output_everything = False
    if (output_everything):
        print("Points :")
        for p in points: print(p)
        print()

        s = new_init_sol(n)
        print(value(s,points,n))
        print()
        
        # s = list(range(n))
        # print("------ swap")
        # print("best val =", best_neighbor_swap(s, points, n) )
        # print()
        # print("------ opt")
        # print("best val =", best_neighbor_opt(s, points, n) )
    
    #-------------------------------------------#
    ### Tests SHC avec restart #

    # MAX_essais = 30
    # shc_restart(points, n, 100, MAX_essais,
    #             best_neigh_fct =best_neighbor_opt, output =True)

    #-------------------------------------------#
    ### Tests SHC avec liste tabou #

    taille_tabou = n//3
    sol,nb_deplacements,tabou = shc_taboo(points, n, 100, taille_tabou,
                                          best_neighbor_opt)

    print("Solution trouvée :", sol)
    print("Valeur de la solution :", value(sol,points,n))
    print("Nb de déplacements :", nb_deplacements)
    print("Liste tabou (taille max", taille_tabou, ") à la fin :")
    for seq in tabou:
        print("\t", seq)

    #-------------------------------------------#
    ## (debug)

    # for s in rand_initial_sols(6, 4):
    #     print(s)
    # test_shc(points,n,[ 1, 5, 10, 100 , 1000 ],
    #         with_restart=True, best_neigh_fct=best_neighbor_swap)
    # test_shc(points,n,[ 1, 5, 10, 100 , 1000 ],
    #         with_restart=True, best_neigh_fct=best_neighbor_opt)