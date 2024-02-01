# LinkedIn Job Scraper
## Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Future Improvements](#future-improvements)

## Overview
This repository contains the files and documentation of a small web scraping project I did while looking for jobs online to help me automate the process.

## Key Features
This project involves:
- Scraping job listing data from LinkedIn using a web browser.
- Creating a .csv file with all the data gathered.
- Finding the roles/positions most relevant to me that are being advertised on the site based on search terms and job requirements.

## Installation
The following packages should be installed:
- bs4
- pandas
- numpy
- selenium
- webdriver-manager

You can install these by running:
`pip install -r requirements.txt`

You should also have Google Chrome installed on your machine too as this project uses it to bypass certain anti-scraping techniques implemented by the website.

## Usage
Run `linkedin_scraper.py` as is for Entry-level Graduate Analyst roles in London, United Kingdom.

You can edit the constant variables in the code to fit the jobs you want to search for.

Once the program has finished running, you should have a .csv file in the same folder as the program which has all the information necessary for the roles that you searched for.

## Screenshots

## Future Improvements
- [ ] Gather links to listings for easier access.
- [ ] Ignore listings that do not contain at least one keyword that appears in the search term.
- [ ] Automatically create a Google Sheets document with all the info gathered.