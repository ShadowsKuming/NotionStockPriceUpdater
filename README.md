# 📈 Notion Asset Price Updater

This project automatically updates the current price of stocks, ETFs, and cryptocurrencies to a Notion database using the Alpaca Market Data API and the Notion API.

## ✅ Features

- Pulls live price data for:
  - US stocks and ETFs
  - Crypto pairs like BTC/USD
- Updates your Notion database with the latest prices
- Supports GitHub Actions for automated scheduled updates

## 🔧 Tech Stack

- Python 3.10
- Notion SDK (`notion-client`)
- Alpaca Market Data SDK (`alpaca-py`)
- GitHub Actions (for automation)

## 📁 Project Structure

.
├── main.py                  # Main script
├── requirements.txt         # Python dependencies
└── .github/
    └── workflows/
        └── update_price.yml # GitHub Actions workflow

## 📝 Notion Database Setup

Create a Notion database with these fields:

| Field Name     | Type    | Required? | Description                         |
|----------------|---------|-----------|-------------------------------------|
| Name           | Title   | Yes       | Asset name or symbol                |
| Type           | Select  | Yes       | Either `stock`, `etf`, or `crypto`  |
| Current Price  | Number  | Yes       | Field to update with latest price   |

## 🔐 GitHub Secrets Setup

Add these to your repo under `Settings → Secrets and Variables → Actions`:

- `ALPACA_API_KEY`
- `ALPACA_SECRET_KEY`
- `NOTION_API_KEY`
- `NOTION_DATABASE_ID`

## 🚀 Local Development

1. Clone this repo:
