# InvestmentIdeas

This is a repo for getting data and testing investment ideas. Will also try to build simple analysis and visualition tools.

Code structure

investment-ideas/
│
├── data/
│   ├── __init__.py
│   ├── data_scraper.py        # Code for scraping data
│   └── utils.py               # Utility functions for data handling
│
├── signals/
│   ├── __init__.py
│   ├── signal_generator.py     # Code for generating signals
│   └── backtester.py           # Code for backtesting signals
│
├── analysis/
│   ├── __init__.py
│   ├── performance_analysis.py  # Code for analyzing performance
│   └── visualizations.py        # Code for visualizing results
│
├── tests/
│   ├── __init__.py
│   ├── test_data_scraper.py     # Unit tests for data scraping
│   ├── test_signal_generator.py   # Unit tests for signal generation
│   └── test_performance_analysis.py # Unit tests for performance analysis
│
├── notebooks/                    # Jupyter notebooks for exploratory analysis
│   └── exploratory_analysis.ipynb
│
├── requirements.txt              # Python package requirements
├── README.md                     # Project documentation
└── main.py                       # Main entry point for running the project