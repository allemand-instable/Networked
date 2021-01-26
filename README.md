# Networked

## Description

A Toolbox to manage network settings on Windows written in Python 3



![MENU](/img/01.png)



### Tools

there are currently 6 tools available :

- Reboot the Network Interface
- Change the Network Interface
  - Pick a network interface to be the only one active
- Enable a Network Interface
- Disable a Network Interface
- Change a Network Interface's DNS
  - 1.1.1.1
  - 1.1.1.1 FAMILY
  - OPEN DNS
  - Google Public DNS
  - Setting a custom DNS
> Includes both IPV4 and IPV6


** NOTE **
> Requires system elevation to apply changes to network interfaces


### dependencies


- [Colorama](https://github.com/tartley/colorama)
  - `pip install colorama`
- WMI
  - `pip install wmi`
- [elevate](https://github.com/barneygale/elevate)
  - `pip install elevate`
- [PyInquirer2](https://github.com/zeusxs/PyInquirer2)
  - `pip install inquirer2`
- [pyfiglet](https://github.com/pwaller/pyfiglet)
  - `pip install pyfiglet`
- regex
  - `pip install regex`


## To Be Done

Migrate from lists to Dictonaries for better code readability
