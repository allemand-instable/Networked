"""
LIBRAIRIES
"""

from __future__ import print_function, unicode_literals


#   PRESENTATION
#       Couleurs

from colorama import Fore, Back, Style

#   DEBUG FUNCTIONS
#       os.sys("pause")

"""
Windows Adapter Lib
"""
import wmi

"""
GENERAL
"""
# Sleep
import time
# OS
import os
# UAC
from elevate import elevate

"""
????????????
"""

import regex

"""
CLI Libraries
"""

from PyInquirer import style_from_dict, Token, prompt, Separator
from PyInquirer import Validator, ValidationError
from pprint import pprint



"""
COOL INSANE TITLE
"""

from pyfiglet import Figlet


"""
CLEAR FUNCTION
"""

clear = lambda: os.system('cls')


"""
Cartes Dispos
"""

def ListAvailableNetworkCards():
    return [conn.NetConnectionID for conn in wmi.WMI().query("select * from Win32_NetworkAdapter") if conn.NetConnectionID ]




"""
MENU
"""



def menu():
    style = style_from_dict({
        Token.QuestionMark: '#E91E63 bold',
        Token.Selected: '#673AB7 bold',
        Token.Instruction: '',  # default
        Token.Answer: '#2196f3 bold',
        Token.Question: '',
    })


    cartes_dispo = ListAvailableNetworkCards()
    cartes_dispo.sort()
    cartes_dispo.append('CANCEL')

    #  print(cartes_dispo)

    questions=[

    {
        'type': 'list',
        'name': 'app_choice',
        'message': 'What do you want to do ?',
        'choices': ['Reboot Network Card', 'Change Network Card', 'Choose a Network Card', 'Enable a Network Card', 'Disable a Network Card','Quit']


    },




    # >>>> Adapter List <<<<


    # Redémarrer

    {
        'type': 'list',
        'name': 'adapter name',
        'message': 'Pick the Network Card you want to reboot : (entrer CANCEL to quit)',
        'choices': cartes_dispo,
        #'default': cartes_dispo[1],
        'when': lambda answers: answers['app_choice'] == 'Reboot Network Card'
    },


    #
    {
        'type': 'list',
        'name': 'choose_adapter',
        'message': 'Pick the Network Card you want to enable :',
        'choices': cartes_dispo,
        'when': lambda answers: answers['app_choice'] == 'Choose a Network Card'
    },


    # Changer


    {
        'type': 'list',
        'name': 'change_adapter_old',
        'message': 'pick the Network Card you want to disable : ',
        'choices': cartes_dispo,
        'when': lambda answers: answers['app_choice'] == 'Change Network Card'
    },

    {
        'type': 'list',
        'name': 'change_adapter_new',
        'message': 'pick the Network Card you want to enable : ',
        'choices': cartes_dispo,
        'when': lambda answers: answers['app_choice'] == 'Change Network Card' and answers['change_adapter_old'] != 'CANCEL'
    },


    # Eteindre

    {
        'type': 'list',
        'name': 'adapter_off',
        'message': 'pick the Network Card you want to disable : ',
        'choices': cartes_dispo,
        'when': lambda answers: answers['app_choice'] == 'Disable a Network Card'
    },


    # Allumer

    {
        'type': 'list',
        'name': 'adapter_on',
        'message': 'pick the Network Card you want to enable',
        'choices': cartes_dispo,
        'when': lambda answers: answers['app_choice'] == 'Enable a Network Card'
    },

    # >>>> Confirms <<<<

    {
        'type': 'confirm',
        'name': 'change_confirm',
        'message': 'Are you sure you want to reboot it ?',
        'default': False,
        'when': lambda answers: answers['app_choice'] == 'Change Network Card' and answers['change_adapter_old'] != 'CANCEL' and answers['change_adapter_new'] != 'CANCEL'
    },



    #{
    #    'type': 'confirm',
    #    'name': 'relancer_confirm',
    #    'message': 'souhaitez vous redémarrer la carte réseau ?',
    #    'default': False,
    #    'when': lambda answers: answers['app_choice'] == 'Reboot Network Card' and answers['adapter name'] != 'CANCEL'
    #},

    {
        'type': 'confirm',
        'name': 'quit_confirm',
        'message': 'Do you want to Exit ?',
        'default': False,
        'when': lambda answers: answers['app_choice'] == 'Quit'
    }



    ]

    answers = prompt(questions, style=style)

    return answers

















"""
MENU CONSEQUENCES / LAUNCHER
"""















def action():

    clear()
    # print([conn.NetConnectionID for conn in wmi.WMI().query("select * from Win32_NetworkAdapter") if conn.NetConnectionID ])
    f = Figlet(font='slant')
    print(f.renderText('NETWORKED'))

    print(Fore.CYAN + "A simple toolbox to manage network cards, written in Python 3\n\n " + Fore.WHITE)

    print("---   " + Fore.YELLOW + "Github/allemand-instable" + Fore.WHITE + "   ---\n\n\n")

    answer = menu()

    print(answer)
    if answer['app_choice'] == 'Reboot Network Card' :
        if answer['adapter name'] != 'CANCEL':  #and answer['relancer_confirm'] == True :
            carte = answer['adapter name']
            relancer_carte(carte)


    if answer['app_choice'] == 'Enable a Network Card' and answer['adapter_on'] != 'CANCEL' :
        carte = answer['adapter_on']
        activer_carte(carte)


    if answer['app_choice'] == 'Disable a Network Card' and answer['adapter_off'] != 'CANCEL' :
        carte = answer['adapter_off']
        desactiver_carte(carte)


    # CHANGER LA CARTE RESEAU

    if answer['app_choice'] == 'Change Network Card' :
        if answer['change_adapter_old'] != 'CANCEL' :
            if answer['change_adapter_new'] != 'CANCEL' :
                if answer['change_confirm'] == True :
                    ancienne_carte = answer['change_adapter_old']
                    nouvelle_carte = answer['change_adapter_new']
                    changer_carte(ancienne_carte, nouvelle_carte)

    if answer['app_choice'] == 'Quit' and answer['quit_confirm'] == False :
        return True

    if answer['app_choice'] == 'Choose a Network Card' and answer['choose_adapter'] == 'CANCEL' :
        return True

    if answer['app_choice'] == 'Choose a Network Card' and answer['choose_adapter'] != 'CANCEL' :
        carte = answer["choose_adapter"]
        choisir_carte(carte)


    if answer["app_choice"] == 'Quit' and answer["quit_confirm"] == True  :
        clear()
        return False


    return True













"""
LOOP FUNCTION
"""






def run():
    running = True
    while running :
        #print(running)
        running = action()
        print(running)
    return
























"""
FONCTIONS CARTE RESEAU
"""



def changer_carte(ancienne_carte, nouvelle_carte):
    desactiver_carte(ancienne_carte)
    activer_carte(nouvelle_carte)
    return

def desactiver_carte(carte):
    c=wmi.WMI()
    o=c.query("select * from Win32_NetworkAdapter")
    #print(c)
    #print(o)
    for conn in o :
        #print(conn.NetConnectionID)
        #print(conn.Caption + " - " + conn.Description)
        if conn.NetConnectionID == carte:
            if conn.NetEnabled:
                conn.Disable()

            else:
                print(carte,  ' est déjà désactivée')
                # conn.Enable()
    return

def activer_carte(carte):
    c=wmi.WMI()
    o=c.query("select * from Win32_NetworkAdapter")
    #print(c)
    #print(o)
    for conn in o :
        #print(conn.NetConnectionID)
        #print(conn.Caption + " - " + conn.Description)
        if conn.NetConnectionID == carte:
            if conn.NetEnabled:
                #conn.Disable()
                print(carte, ' est déjà activée')
            else:
                conn.Enable()
    return



def relancer_carte(carte):
    print("ok")
    desactiver_carte(carte)
    activer_carte(carte)
    return




def choisir_carte(carte_choisie):
    list = [conn.NetConnectionID for conn in wmi.WMI().query("select * from Win32_NetworkAdapter") if conn.NetConnectionID ]
    for carte in list :
        if carte != carte_choisie :
            desactiver_carte(carte)
        else :
            activer_carte(carte)
    return









"""
MAIN FUNCTION
"""


def main():
    run()
    return 0

# Définie la main
if __name__ == "__main__" :
    elevate()
    main()
