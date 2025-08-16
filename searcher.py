#!/usr/bin/env python3

__version__ = '1.0.0'
__author__ = 'root616C6578'
__license__ = 'MIT'
__description__ = 'A script to fetch and display onion services from Ahmia'

notice = '''
Disclaimer:
    This script is intended for educational and legal use only.
    The author takes no responsibility for any misuse or illegal activity.
    Use at your own risk.
    Stay safe and ethical.
    root616C6578 - https://github.com/root616C6578
'''

import sys
sys.dont_write_bytecode = True

from bs4 import BeautifulSoup
import requests
import os
import subprocess
import socket
import time 
import argparse

parser = argparse.ArgumentParser(description='Onion Services Search')
parser.add_argument('-v','--version', action='version', version=f'%(prog)s {__version__}')
parser.add_argument('-n', '--number', type=int, default=5, help='Number of results to display (default: 5)')
parser.add_argument('search', nargs='?', help='Search term (default prompt:sudo searcher xmpp -n 5)')
args = parser.parse_args()
if args.search is None:
    print("Please input name url!(exaple: searcher xmpp )")
    os._exit(0)
    
def wait_for_tor(host="127.0.0.1", port=9050, timeout=60):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=2):
                print("Tor готовий!")
                return True
        except (OSError, ConnectionRefusedError):
            time.sleep(1)
    print("Tor не запустився вчасно!")
    return False
tor_process = subprocess.Popen(['tor --SocksPort 9050 --ControlPort 9051'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
time.sleep(5)  # Wait for Tor to start


if not wait_for_tor():
    print("Не вдалося підключитися до Tor. Перевірте, чи запущено Tor.")
    sys.exit(1)

# This script fetches and displays information about XMPP-related onion services from Ahmia's search API.
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'

    RED = '\033[31m'
    GREEN = '\033[32m'
    ORANGE = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    GRAY = '\033[37m'


url_api= f"https://ahmia.fi/search/?q={args.search}"
proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}
response = requests.get(url_api, proxies=proxies, timeout=10)
soup = BeautifulSoup(response.content, 'html.parser')

def check_tor_running(self, proxies):
    test_url = "http://api.ipify.org"
    try:
        response = requests.get(test_url, proxies=proxies, timeout=10)
        if response.status_code == 200:
            print(f'{Colors.BOLD}{Colors.GREEN}Currect IP Address via Tor: {Colors.RESET}{response.text}')
            return True
    except requests.RequestException as e:
        print(f'{Colors.BOLD}{Colors.RED}Error connecting to Tor: {e}{Colors.RESET}')

resultat = soup.find_all(class_='result')
number_of_results = args.number if args.number > 0 else None
if number_of_results is not None and isinstance(number_of_results, int):
    if number_of_results < 1:
        print(f'{Colors.BOLD}{Colors.RED}Error: The number of results must be a positive integer.{Colors.RESET}')
        sys.exit(1)
    if number_of_results > len(resultat):
        print(f'{Colors.BOLD}{Colors.ORANGE}Warning: Requested number of results exceeds available results. Displaying all available results.{Colors.RESET}')
        number_of_results = len(resultat)
if number_of_results > 0:
    resultat = resultat[:number_of_results]



def name(resultat,response):
    for cite in resultat:
        time.sleep(1)  # невелика затримка, щоб не спамити

        # Отримуємо span
        span = ''
        for span_tag in cite.find_all('span'):
            span = span_tag.get_text()

        # Отримуємо посилання
        cite_tag = cite.find('cite')
        link = cite_tag.get_text().strip()

        # Отримуємо опис
        description = ''
        for paragraph in cite.find_all('p'):
            description += paragraph.get_text() + " "

        # Перевірка online/offline
        try:
            if ".onion" in link:
                response = requests.get(f"http://{link}", proxies=proxies, timeout=20)
            else:
                response = requests.get(link, timeout=20)

            if 200 <= response.status_code < 400:
                status = f'{Colors.BOLD}{Colors.GREEN}Online{Colors.RESET}'
            else:
                status = f'{Colors.BOLD}{Colors.RED}Offline{Colors.RESET}'
        except requests.Timeout:
            status = f'{Colors.BOLD}{Colors.RED}Timeout{Colors.RESET}'
        except requests.ConnectionError:
            status = f'{Colors.BOLD}{Colors.RED}Connection Failed{Colors.RESET}'
        except requests.RequestException:
            status = f'{Colors.BOLD}{Colors.RED}Offline{Colors.RESET}'

        # Вивід для одного результату
        print('\n')
        print(f'| Description: {Colors.BOLD}{Colors.PURPLE}{description.strip()}{Colors.RESET}')
        print(f'| Status: {status}')
        print(f'| Onion Link: {Colors.BOLD}{Colors.GREEN}{link} {span}{Colors.RESET}')
        print('\n')
        print(f'{Colors.BOLD}{Colors.GREEN}---------------------------------------------------------------{Colors.RESET}')
    

def main():
    print("\n")
    print(f'{Colors.BOLD}{Colors.GREEN}Onion Services Search{Colors.RESET}')
    print(f'{Colors.BOLD}{Colors.ORANGE}Fetching data from Ahmia...{Colors.RESET}')
    print(f"{Colors.BOLD}{Colors.CYAN}{notice}{Colors.RESET}")
    print(f'{Colors.BOLD}{Colors.CYAN}Search Term: {args.search} | Number of Results: {args.number}{Colors.RESET}')
    print(f'{Colors.BOLD}{Colors.GRAY}Fetching results...{Colors.RESET}')

    check_tor_running(None, proxies)
    name(resultat, response)
    tor_process.terminate()
    print(f'{Colors.BOLD}{Colors.RED}Tor process terminated.{Colors.RESET}')
    print(f'{Colors.BOLD}{Colors.CYAN}Thank you for using Onion Services Search!{Colors.RESET}')
    print(f'{Colors.BOLD}{Colors.GRAY}Version: {__version__}    {Colors.RESET}')
    print(f'{Colors.BOLD}{Colors.GRAY}Author: {__author__}    {Colors.RESET}')
    print(f'{Colors.BOLD}{Colors.GRAY}License: {__license__}    {Colors.RESET}')
    print(f'{Colors.BOLD}{Colors.GRAY}Description: {__description__}    {Colors.RESET}')
    print("\n")
    print(f'{Colors.BOLD}{Colors.GREEN}Exiting...{Colors.RESET}')
    print("\n")
    os._exit(0)
main()
