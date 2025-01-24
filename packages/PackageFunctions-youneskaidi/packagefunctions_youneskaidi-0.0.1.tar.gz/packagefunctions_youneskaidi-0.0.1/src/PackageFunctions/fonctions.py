def Supprume_d(liste):
    if len(liste) == 0:
        return None
    supp_element = liste[-1]
    liste = liste[:-1]
    return supp_element, liste

def Ajouter_f(liste, element):
    new_list = liste + [element]
    return new_list

def P_occurence(liste, element):
    for i in range(len(liste)):
        if liste[i] == element:
            return i
    return -1

def Trier(liste):
    n = len(liste)
    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):
            if liste[j] > liste[j+1]:
                liste[j], liste[j+1] = liste[j+1], liste[j]
                swapped = True
        if not swapped:
            break
    return liste
