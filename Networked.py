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
Inquirer 2 requirement
"""

import regex

"""
CLI Libraries
"""

from inquirer2 import prompt, Separator
from prompt_toolkit.validation import Validator, ValidationError
from pprint import pprint
from prompt_toolkit.styles import Style

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
Liste des DNS
"""

# name, IPV4 (first, secondary), IPV6 (first, secondary)

# 1.1.1.1
# 1.1.1.1 Family - no porn
# OPEN DNS
# Google Public DNS

DNS_list = [

('Automatic (DHCP)', None, None),

('1.1.1.1', ('1.1.1.1', '1.0.0.1'), ('2606:4700:4700::1111', '2606:4700:4700::1001') ),

('1.1.1.1 FAMILY', ('1.1.1.3', '1.0.0.3'), ('2606:4700:4700::1113', '2606:4700:4700::1003') ),

('OPEN DNS', ('208.67.222.222', '208.67.220.220'), ('2620:119:35::35', '2620:119:53::53') ),

('Google Public DNS', ( '8.8.8.8' , '8.8.4.4' ), ('2001:4860:4860::8888' , '2001:4860:4860::8844' ) ),

('CUSTOM', None, None),

('CANCEL', None, None)


]





"""
MENU
"""




def menu():

    """
    orange = '#F19066'
    pink = '#f78fb3'
    yellow = '#f5cd79'
    cyan = '#63CDDA'
    """

    style = Style.from_dict({
        'separator': '#E91E63',
        'questionmark': '#E91E63',
        'focus': '#2196f3',
        'checked': '#2196f3',  # default
        'pointer': '#ff8700',  # AWS orange
        'instruction': '#ff8700',  # default
        'answer': '#00ffd7',  # AWS orange
        'question': '#2196f3',
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
        'choices': ['Reboot Network Card', 'Change Network Card', 'Choose a Network Card', 'Enable a Network Card', 'Disable a Network Card', 'Change DNS', 'Quit']


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

    # Change DNS

    {
        'type' : 'list',
        'name' : 'choose_dns_first',
        'message' : 'Choisis la carte Réseau concernée :',
        'choices' : cartes_dispo,
        'when': lambda answers: answers['app_choice'] == 'Change DNS'
    },


    {
        'type' : 'list',
        'name' : 'choose_dns_second',
        'message' : 'Choisis le DNS à appliquer : ',
        'choices' : [ DNS_list[k][0] for k in range(len(DNS_list)) ],
        'when' : lambda answers: answers['app_choice'] == 'Change DNS' and answers['choose_dns_first'] != 'CANCEL'
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

    answers = prompt.prompt(questions, style=style)

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


    elif answer['app_choice'] == 'Enable a Network Card' and answer['adapter_on'] != 'CANCEL' :
        carte = answer['adapter_on']
        activer_carte(carte)


    elif answer['app_choice'] == 'Disable a Network Card' and answer['adapter_off'] != 'CANCEL' :
        carte = answer['adapter_off']
        desactiver_carte(carte)


    # CHANGER LA CARTE RESEAU

    elif answer['app_choice'] == 'Change Network Card' :
        if answer['change_adapter_old'] != 'CANCEL' :
            if answer['change_adapter_new'] != 'CANCEL' :
                if answer['change_confirm'] == True :
                    ancienne_carte = answer['change_adapter_old']
                    nouvelle_carte = answer['change_adapter_new']
                    changer_carte(ancienne_carte, nouvelle_carte)

    elif answer['app_choice'] == 'Quit' and answer['quit_confirm'] == False :
        return True

    elif answer['app_choice'] == 'Choose a Network Card' and answer['choose_adapter'] == 'CANCEL' :
        return True

    elif answer['app_choice'] == 'Choose a Network Card' and answer['choose_adapter'] != 'CANCEL' :
        carte = answer["choose_adapter"]
        choisir_carte(carte)


    # CHANGE DNS SERVERS


    elif answer['app_choice'] == 'Change DNS' and answer['choose_dns_first'] != 'CANCEL' :
        wait = input("PRESS ENTER TO CONTINUE.")
        if answer['choose_dns_second'] != 'CANCEL' :

            if answer['choose_dns_second'] == 'Automatic (DHCP)' :

                carte = answer['choose_dns_first']

                set_to_default_DNS(carte)
                return True
            elif answer['choose_dns_second'] != 'CUSTOM' :
                # wait = input("PRESS ENTER TO CONTINUE.")
                # l'outil pour l'interface CLI renvoie une chaine de caractère : le nom
                # sauf que avec seulement le nom, on ne peut savoir quels couples d IP sélectionner
                # on doit donc check quel est le couple qui correspond au nom renvoyé
                dns_number = None
                for k in range(len(DNS_list)):
                    print(answer['choose_dns_second'])
                    print(DNS_list[k][0])
                    print('\n')
                    # wait = input("PRESS ENTER TO CONTINUE.")
                    if answer['choose_dns_second'] == DNS_list[k][0] :
                        dns_number = k
                print(dns_number)
                # wait = input("PRESS ENTER TO CONTINUE.")

                carte = answer['choose_dns_first']

                # print(carte)
                # wait = input("PRESS ENTER TO CONTINUE.")

                DNS_IP_TUPLE_V4 = DNS_list[dns_number][1]

                DNS_IP_TUPLE_V6 = DNS_list[dns_number][2]

            elif answer['choose_dns_second'] == 'CUSTOM' :
                SettingsTuple = add_Custom_DNS()

                DNS_IP_TUPLE_V4 = SettingsTuple[0]

                DNS_IP_TUPLE_V6 = SettingsTuple[1]

            # print(DNS_IP_TUPLE_V4)

            # wait = input("PRESS ENTER TO CONTINUE.")
            Change_DNS( 'ipv4', carte, DNS_IP_TUPLE_V4)
            Change_DNS( 'ipv6', carte, DNS_IP_TUPLE_V6)
            return True
        else :
            return True





    elif answer["app_choice"] == 'Quit' and answer["quit_confirm"] == True  :
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
FONCTIONS DNS
"""

# netsh interface ip set dnsservers name="Wi-Fi" source=dhcp

def Change_DNS( standard , network_card, DNS_IP_TUPLE ):
    if (standard == 'ipv4') or (standard == 'ipv6'):

        network_card_word = '\"' + network_card + '\"'

        primary_dns = 'static ' + DNS_IP_TUPLE[0]
        secondary_dns = DNS_IP_TUPLE[1]

        os.system('netsh interface ' + standard + ' set dns ' + network_card_word + ' ' + primary_dns)
        os.system('netsh interface ' + standard + ' add dns ' + network_card_word + ' ' + secondary_dns + ' Index=2')
        os.system('ipconfig/flushdns')
    else :
        raise Exception('You must set a correct standard :\n \n either :\nipv4\n\nOR\n\nipv6 !')
    return




def add_Custom_DNS():
    print('please give it a name : ')
    name = input('name : ')
    print(Fore.YELLOW + 'IPv4 DNS server information' + Fore.WHITE +' : ')
    ipv4_primary = input('Primary : ')
    ipv4_secondary = input('Secondary : ')
    print(Fore.YELLOW + 'IPv6 DNS server information' + Fore.WHITE +' : ')
    ipv6_primary = input('Primary : ')
    ipv6_secondary = input('Secondary : ')

    if ( ipv4_primary.isalpha() or ipv4_primary.isalnum() ):
        pass
    else :
        ipv4_primary = input('please ensure to type it correctly, Primary : ')




    ipv4_tuple = (ipv4_primary, ipv4_secondary)
    ipv6_tuple = (ipv6_primary, ipv6_secondary)
    Tuple = (name, ipv4_tuple, ipv6_tuple)

    DNS_list.append(Tuple)

    return [ ipv4_tuple, ipv6_tuple ]



def set_to_default_DNS(network_card):
    network_card_word = '\"' + network_card + '\"'
    os.system( 'netsh interface ipv4 set dnsservers name=' + network_card_word + " source=dhcp" )
    os.system( 'netsh interface ipv6 set dnsservers name=' + network_card_word + " source=dhcp" )
    os.system('ipconfig/flushdns')
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
