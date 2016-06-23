# -*- coding: utf-8 -*- 
#owquery.py
#Command line to get various information about a Overwatch account.
#Author: mpmsimo
#Created: 6/21/16

import json

import click
import requests
import tabulate

import config as c

#API url creation
def create_pn_api_url():
    """Creates API url for patch notes."""
    pn_api_url = c.api_url + 'patch_notes'
    return pn_api_url

def create_platform_api_url(platform, region, tag, path, hero=None):
    """Creates API urls based on information provided."""
    platform_api_url  = c.api_url + '{0}/{1}/{2}/'.format(platform, region, tag)
    if path == 'hero':
        customized_url = platform_api_url + 'hero/{0}/'.format(hero)
    else:
        customized_url = platform_api_url + path
    return customized_url

#API calls
def get_patch_notes():
    """Returns patch notes data"""
    #api_call = 
    header = {'content-type': 'application/json'}
    api_url = create_pn_api_url()
    r = requests.get(api_url, headers=header)
    return json.dumps(r.json(), indent=4)

def get_platform_stats(platform, region, tag, path):
    """Returns either: achievements, allHeroes, get-platforms, heroes, or profile."""
    header = {'content-type': 'application/json'}
    api_url = create_platform_api_url(platform, region, tag, path)
    r = requests.get(api_url, headers=header)
    return json.dumps(r.json(), indent=4)

def get_hero_stats(platform, region, tag, path, hero):
    """Returns hero stats"""
    header = {'content-type': 'application/json'}
    api_url = create_platform_api_url(platform, region, tag, path, hero)
    r = requests.get(api_url, headers=header)
    return json.dumps(r.json(), indent=4)

#JSON data manipulation
def get_hero_list(heroes_json):
    """Returns a list of all Overwatch heroes."""
    hero_list = []
    hlj = json.loads(heroes_json)
    for i in hlj:
       hero_list.append((i["name"]))
       #hero_list.append((str(i["name"])))
       #hero_list.append(unicode(str(i["name"])))

    name = 'Torbj&#xF6;rn'
    #substring starts at & and ends at ;
    #count index of &:
    #remove HTML code from string
    #decode/encode to proper character
    #insert back into string
    #lu = unichr(ord(u'\xFA').encode('utf-8')
    #lu = unichr(ord('\xFA')).encode('utf-8')
    #to = unichr(ord(u'\xF6')).encode('utf-8')
    #n = ord(u'\xFA').decode('utf-8')
    #to = ord(u'\xF6').decode('utf-8')
    #print(n, to)
    return hero_list

### CLI
@click.group()
def cli1():
    """patch_notes - Prints patch notes."""
    pass

@cli1.command()

def patch_notes():
    """Gets achievements for a Battle.net user"""
    pnj = get_patch_notes()
    print(pnj)

@click.group()
def cli2():
    """achievements - Prints achivements for a user."""
    pass

@cli2.command()
@click.option('--platform', type = str, default = c.platform, help = "The platform type (pc, xbl, psn) - Default: pc")
@click.option('--region', type = str, default = c.region, help = "The region name (us, eu, kr, cn) - Default: us")
@click.option('--tag', type = str, help = "The Battle.net battletag of the user (replace s/#/-/) - Example: Reulan-1746")

def achievements(platform, region, tag, hero):
    """Gets achievements for a Battle.net user"""
    path = 'achievements'
    aj = get_platform_stats(platform, region, tag, path)
    print(aj)

@click.group()
def cli3():
    """all_heroes - Prints all hero statistics for a user."""
    pass

@cli3.command()
@click.option('--platform', type = str, default = c.platform, help = "The platform type (pc, xbl, psn) - Default: pc")
@click.option('--region', type = str, default = c.region, help = "The region name (us, eu, kr, cn) - Default: us")
@click.option('--tag', type = str, help = "The Battle.net battletag of the user (replace s/#/-/) - Example: Reulan-1746")

def all_heroes(platform, region, tag):
    """Gets all hero stats for a Battle.net user"""
    path = 'allHeroes/'
    ahj = get_platform_stats(platform, region, tag, path)
    print(ahj)

@click.group()
def cli4():
    """get_platforms - Prints platforms where the user owns Overwatch."""
    pass

@cli4.command()
@click.option('--platform', type = str, default = c.platform, help = "The platform type (pc, xbl, psn) - Default: pc")
@click.option('--region', type = str, default = c.region, help = "The region name (us, eu, kr, cn) - Default: us")
@click.option('--tag', type = str, help = "The Battle.net battletag of the user (replace s/#/-/) - Example: Reulan-1746")

def get_platforms(platform, region, tag):
    """Gets platforms for a Battle.net user"""
    path = 'get-platforms'
    gpj = get_platform_stats(platform, region, tag, path)
    print(gpj)

@click.group()
def cli5():
    """hero - Prints specific hero stats for a user. Some hero names have been modified: Torbjörn = Torbjoern, Lúcio = Lucio, Soldier: 76 = Soldier76"""
    pass

@cli5.command()
@click.argument('hero')
@click.argument('tag')
@click.option('--platform', type = str, default = c.platform, help = "The platform type (pc, xbl, psn) - Default: pc")
@click.option('--region', type = str, default = c.region, help = "The region name (us, eu, kr, cn) - Default: us")
@click.option
def hero(hero, platform, region, tag):
    """Gets achievements for a Battle.net user"""
    path = 'hero'
    hero_list = ['Mercy']
    if hero in hero_list:
        hj = get_hero_stats(platform, region, tag, path, hero)
        print(hj)
    else:
        print('\'{0}\' is not a valid Overwatch hero, please see command information.'.format(hero))

@click.group()
def cli6():
    """heroes - Prints all hero statistics for a user."""
    pass

@cli6.command()
@click.argument('tag')
@click.option('--platform', type = str, default = c.platform, help = "The platform type (pc, xbl, psn) - Default: pc")
@click.option('--region', type = str, default = c.region, help = "The region name (us, eu, kr, cn) - Default: us")
@click.option('--hlist', is_flag = True, help = "Prints a list of heroes in Overwatch.")

def heroes(platform, region, tag, hlist):
    """Gets hero stats for a Battle.net user"""
    path = 'heroes'
    hsj = get_platform_stats(platform, region, tag, path)
    if hlist:
        print(get_hero_list(hsj))
    else:
        print(hsj)

@click.group()
def cli7():
    """profile - Prints Overwatch profile for a user."""
    pass

@cli7.command()
@click.option('--platform', type = str, default = c.platform, help = "The platform type (pc, xbl, psn) - Default: pc")
@click.option('--region', type = str, default = c.region, help = "The region name (us, eu, kr, cn) - Default: us")
@click.option('--tag', type = str, help = "The Battle.net battletag of the user (replace s/#/-/) - Example: Reulan-1746")

def profile(platform, region, tag):
    """Gets a Battle.net user's profile."""
    path = 'profile'
    pj = get_platform_stats(platform, region, tag, path)
    print(pj)

cli = click.CommandCollection(sources = [cli1, cli2, cli3, cli4, cli5, cli6, cli7])

if __name__ == "__main__":
    """Logic that will be executed on runtime"""
    cli()
