# Stock Sentinel
## Description 
Stock Sentinel is a Web-App for analyzing stocks using AI for sentiment analysis.

## Installation
git clone https://github.com/nughnugh/BCN-2024SS-TeamRot-StockSentinel.git

## Setup
- cd **sys-src**
- !!! copy .env.example file, save as .env !!!
- optional: change parameters such as POSTGRES_PASSWORD in .env

## Run
- cd **sys-src**
- docker compose up

# View
This application was deployed using Hetzner. As of right now (July 2024), you can view the page with this link: https://t1p.de/StockSentinel

## Copyright and Licenses
Copyright (c) 2024 Ostbayerische Technische Hochschule Amberg-Weiden. All rights reserved.

This software is licensed under the MIT.
For detailed license information, see the LICENSE file in the project root.

## Used
- SvelteKit
- express.js
- nltk VADER sentiment
- yahoo.finance
- google news rss
