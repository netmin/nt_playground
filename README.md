# Nautilus Trader Playground

This repository provides practical examples and step-by-step tutorials to help you learn and experiment with [Nautilus Trader](https://github.com/nautechsystems/nautilus_trader)—an event-driven algorithmic trading platform.

## 🗂 Repository Structure

```
nautilus-trader-playground/
├── examples/
│   ├── actors/            # Examples of custom actors and market monitors
│   ├── strategies/        # Examples of trading strategies
│   ├── indicators/        # Custom indicators implementations
│   └── data/              # Data loading and processing utilities
├── notebooks/
│   ├── actors/            # Jupyter notebooks for actor tutorials
│   ├── strategies/        # Tutorials on developing trading strategies
│   └── indicators/        # Indicator development and examples
├── data/                  # Raw and processed market data
├── utils/                 # Common utility functions and helpers
├── Dockerfile             # Docker configuration
└── README.md              # Documentation and instructions
```

## 🚀 Getting Started

### Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/netmin/nautilus-trader-playground.git
cd nautilus-trader-playground
```

### 2. Running with Docker
Pull the latest docker image:

```bash
docker pull ghcr.io/nautechsystems/jupyterlab:nightly --platform linux/amd64
```
Start the Docker container, mounting your local directories:
```bash
docker run --rm -it -p 8888:8888 \
  -v $(pwd)/notebooks:/opt/pysetup/tutorials \
  ghcr.io/nautechsystems/jupyterlab:nightly
```

Then open [http://localhost:8888](http://localhost:8888) in your browser and follow the instructions to access the Jupyter Notebook.

## 🎓 Tutorials and Examples

Explore step-by-step examples and tutorials:

- **Actors**: Creating custom components to monitor and interact with market data.
- **Strategies**: Building and backtesting algorithmic trading strategies.
- **Indicators**: Implementing and customizing technical indicators.
- **Data Utilities**: Loading, preprocessing, and handling market data.

## 📌 Contributing

- Add new concepts and examples into their corresponding directories.
- Keep examples simple, clear, and focused on single concepts or components.
- Ensure code examples are fully commented, easy to understand, and runnable.

#### Happy Trading! 🚀📈


