# Stock Sentinel
## Description 
Stock Sentinel is a Web-App for analyzing stocks using AI for sentiment analysis.

## Installation
git clone https://github.com/nughnugh/BCN-2024SS-TeamRot-StockSentinel.git

## Setup
- cd **sys-src**
- !!! copy .env.example file, save as .env !!!
- optional: change parameters such as POSTGRES_PASSWORD in .env
- for linux you might need to change "host.docker.internal" to "172.17.0.1"

## Run
- cd **sys-src**
- docker compose up

## View in action
This application was deployed using Hetzner. As of right now (July 2024), you can view the page with this link: https://t1p.de/StockSentinel

## Copyright and Licenses
This software is licensed under the MIT.
For detailed license information, see the LICENSE file in the project root.

## Used Tech
- SvelteKit
- express.js
- PostgreSQL
- nltk VADER
- yahoo.finance
- google news rss
