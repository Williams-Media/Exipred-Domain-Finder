
# Expired Domain Finder

This Python script crawls a specified website to find links that lead to expired or non-registered domains. It's designed to help SEO specialists, web developers, and digital marketers identify valuable expired domains that may be related to their niche or project. This is a quick and dirty script (no judgement) 

## Features

- Crawls a given website recursively, following internal links.
- Identifies external links and checks the domain registration status (expired).
- Skips subdomains and certain TLDs (e.g., `.gov`, `.edu`)
- Outputs expired domains to a text file for easy review.
- Provides real-time updates on the crawling and checking process.

## Requirements

- Python 3.6+
- Libraries: `requests`, `bs4` (BeautifulSoup), `whois`, `fake_useragent`, `termcolor`, `tldextract`, `concurrent.futures`
- A command-line interface (CLI) or terminal to run the script.

## Installation

First, ensure you have Python installed on your system. You can download Python from [python.org](https://www.python.org/downloads/).

Clone the repository to your local machine:

    git clone https://github.com/Williams-Media/expired-domain-finder.git
    cd expired-domain-finder

Install the required Python libraries:

    pip install -r requirements.txt

The `requirements.txt` file should contain:

    requests
    beautifulsoup4
    whois
    fake_useragent
    termcolor
    tldextract

## Running the Script

To run the script, use the following command in your terminal:

    python expired_domain_finder.py

Follow the on-screen prompts to enter the starting URL for the crawl. The script will then begin the crawling and checking process, providing real-time updates and saving found expired domains to a text file.

## Contribution

Contributions to the script are welcome! Please feel free to fork the repository, make your changes, and submit a pull request.

## License

This project is open-source and available under the MIT License.

