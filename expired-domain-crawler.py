import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import whois
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from fake_useragent import UserAgent
from termcolor import colored
import threading
import tldextract
import textwrap

def print_welcome_message():
    title = "Expired Domain Finder"
    colored_title = colored(title, 'red', attrs=['underline'])
    print(colored_title + "\n")
    
    message = ("Enter the starting URL to crawl (example: https://wkbw.com). "
               "Crawler will go through the entire site looking for links that lead "
               "to expired / non-registered domains.")
    
    wrapped_text = textwrap.fill(message, width=70)  # Adjust 'width' as per your preference
    print(wrapped_text + "\n")

def get_domain_name(url):
    extracted = tldextract.extract(url)
    return "{}.{}".format(extracted.domain, extracted.suffix)

def is_domain_skippable(domain):
    skippable_extensions = ['.edu', '.ny.us', '.nj.us']
    return any(domain.endswith(ext) for ext in skippable_extensions) or '.gov' in domain

def is_domain_expired(domain):
    if is_domain_skippable(domain):
        return False, None
    try:
        domain_info = whois.whois(domain)
        expiration_date = domain_info.expiration_date
        if isinstance(expiration_date, list):
            expiration_date = expiration_date[0]
        if expiration_date:
            return expiration_date < datetime.now(), domain_info.text
        else:
            return False, None
    except Exception as e:
        print(f"Error checking domain {domain}: {e}")
        return False, None

def check_and_log_domain(domain, found_on_url, expired_domains, checked_domains, stats, output_file):
    with stats['lock']:
        if domain in checked_domains:
            stats['duplicates'] += 1
            return
        stats['checked'] += 1
        checked_domains.add(domain)
    
    expired, _ = is_domain_expired(domain)
    if expired:
        with stats['lock']:
            expired_domains.append((domain, found_on_url))
            stats['expired'] += 1
        output_line = f"{domain} is expired! Found on: {found_on_url}\n"
        with open(output_file, 'a') as file:
            file.write(output_line)
        print(colored(f"Domain {domain} is expired! Saved to results file.", 'green'))

def crawl_website(start_url, executor, output_file, stats):
    domain = get_domain_name(start_url)
    external_links = set()
    visited = set()
    queue = [start_url]
    checked_domains = set()
    expired_domains = []

    while queue:
        current_url = queue.pop(0)
        if current_url not in visited:
            visited.add(current_url)
            with stats['lock']:
                stats['crawled'] += 1

            try:
                ua = UserAgent()
                headers = {'User-Agent': ua.random}
                response = requests.get(current_url, headers=headers, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')

                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if not href.startswith(('http:', 'https:')):
                        href = urljoin(current_url, href)
                    parsed_domain = get_domain_name(href)

                    if parsed_domain and parsed_domain != domain:
                        with stats['lock']:
                            if href not in external_links:
                                external_links.add(href)
                                stats['found'] += 1
                                executor.submit(check_and_log_domain, parsed_domain, href, expired_domains, checked_domains, stats, output_file)
                    elif parsed_domain == domain and href not in visited:
                        queue.append(href)

            except Exception as e:
                print(f"Error crawling {current_url}: {e}")

        with stats['lock']:
            print(f"Crawled: {stats['crawled']}, Found: {stats['found']}, Checked: {stats['checked']}, Duplicates: {stats['duplicates']}, ", end="")
            print(colored(f"Expired: {stats['expired']}", 'green'), end="")
            print(f" - {current_url}")

def main():
    print_welcome_message()
    start_url = input("Enter the starting URL to crawl: ")
    domain = get_domain_name(start_url)
    output_file = f"{domain}-expireddomains.txt"

    stats = {
        'crawled': 0,
        'found': 0,
        'checked': 0,
        'duplicates': 0,
        'expired': 0,
        'lock': threading.Lock()
    }

    with ThreadPoolExecutor(max_workers=10) as executor:
        crawl_website(start_url, executor, output_file, stats)

if __name__ == "__main__":
    main()
