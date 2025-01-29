# Simple Currency Converter API

A minimal FastAPI project demonstrating API calls to convert USD to other currencies using the [ExchangeRate-API](https://www.exchangerate-api.com/).

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- A free API key from [ExchangeRate-API](https://www.exchangerate-api.com/) (1,500 free requests/month).

### Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/currency-api-demo.git
   cd currency-api-demo
Install dependencies:

2. **Set up requirements**:
pip install -r requirements.txt
Create a .env file:
EXCHANGE_RATE_API_KEY=your-api-key-here

3. **Run the server**:
uvicorn main:app --reload