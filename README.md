# Synapsee-AI

Synapsee-AI is an AI-powered product research and business intelligence system that helps users analyze the market potential of a product idea.

Users provide inputs such as:

- Product name
- Product description / functionality
- Target age range
- Target budget
- Target country or state

The system uses **Gemini 2.5 Flash** to intelligently determine:

- Which keywords should be used for Google Trends analysis
- Which product keywords should be used for Amazon / Flipkart scraping
- Potential raw materials required for manufacturing

## Workflow

1. User enters product-related information.
2. Gemini analyzes the idea and generates relevant search parameters.
3. Google Trends data is fetched using **SerpAPI** to identify:
   - Product popularity
   - Seasonal demand trends
   - High-demand months
4. Similar products are scraped from platforms like:
   - Amazon
   - Flipkart
5. Product reviews, advantages, and disadvantages are extracted.
6. Suggested raw materials are sent to a **ChromaDB RAG pipeline** containing government datasets related to:
   - Historical raw material prices
   - Price growth trends over the years
7. All collected insights are combined into a final analytical PDF report.

## Features

- AI-driven market research
- Google Trends integration
- E-commerce competitor analysis
- Raw material cost forecasting using RAG
- Automated PDF report generation
- Modular multi-agent workflow

## Tech Stack

- Gemini 2.5 Flash
- SerpAPI
- ChromaDB
- RAG Pipeline
- Python

## Output

The final generated PDF includes:

- Market trend analysis
- Seasonal demand insights
- Competitor product comparison
- Product review summaries
- Raw material price trend analysis
- Manufacturing/business insights
