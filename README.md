 
# Telangana Industrial Land Availability Scraper

Web scraper to collect data on vacant industrial plots across Telangana from the Telangana State Industrial Infrastructure Corporation (TGIIC) website.

## Project Overview

This project uses Scrapy to scrape hierarchical data about industrial land availability in Telangana. The scraper navigates through multiple levels (Zones → Districts → Industrial Parks → Individual Plots) and consolidates all information into a structured dataset.

## Data Collected

The scraper extracts information at four levels:

1. **Zone level**: Zone name, number of plots, number of sheds, plotted area
2. **District level**: District-wise breakdown of plots and sheds
3. **Industrial Park level**: Park details including land rates, purpose, and layout links
4. **Plot level**: Individual vacant plot details including plot number, area, property type, and rates

## Tools Used

- **Python** (Scrapy framework for web scraping)
- **XPath** for HTML parsing

## How to Run

1. Install Scrapy:
```bash
pip install scrapy
```

2. Navigate to your project directory and run:
```bash
scrapy crawl telangana -o output.json
```

This will save the scraped data to `output.json`.

## Data Source

- Website: [TGIIC Vacant Plots](https://www.tgiic.telangana.gov.in/PMVacantPlots)
- Scraping done in April 2025

## Key Features

- **Hierarchical scraping**: Navigates through 4 levels of nested pages
- **Metadata preservation**: Carries forward zone and district information to plot-level data
- **Comprehensive data**: Captures 25+ attributes per vacant plot
- **Clean structure**: Well-commented code  

## Output Structure

Each record contains complete information from all hierarchy levels:
- Zone details (6 fields)
- District details (5 fields)  
- Industrial Park details (9 fields)
- Vacant plot details (8 fields)

## Use Cases

This data can be used for:
- Industrial investment analysis in Telangana
- Land rate comparisons across zones and districts
- Identifying available industrial land for specific purposes
- Spatial analysis of industrial development
```

 
