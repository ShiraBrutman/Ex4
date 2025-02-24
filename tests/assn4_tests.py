import pytest
import requests
import random

BASE_URL = "http://localhost:5001"  # Stocks service
HEADERS = {"Content-Type": "application/json"}

@pytest.fixture
def create_stock():
    """Helper function to create a stock entry with a unique symbol and return its ID."""
    unique_symbol = f"TEST{random.randint(1000, 9999)}"  # Generate a unique stock symbol
    stock_data = {
        "name": "Test Stock",
        "symbol": unique_symbol,
        "purchase price": 134.66,
        "purchase date": "18-06-2024",
        "shares": 7
    }

    response = requests.post(f"{BASE_URL}/stocks", json=stock_data, headers=HEADERS)
    print("Response Status:", response.status_code)
    print("Response Body:", response.text)
    assert response.status_code == 201, f"Unexpected response: {response.text}"
    return response.json().get("id")

def test_add_stock():
    """Test adding a new stock."""
    stock_data = {
        "name": "Apple Inc.",
        "symbol": "AAPL",
        "purchase price": 183.63,
        "purchase date": "22-02-2024",
        "shares": 19
    }
    response = requests.post(f"{BASE_URL}/stocks", json=stock_data, headers=HEADERS)
    assert response.status_code == 201
    assert "id" in response.json()

def test_get_stock_by_id(create_stock):
    """Test retrieving a stock by ID."""
    stock_id = create_stock  # This ID is from the fixture
    response = requests.get(f"{BASE_URL}/stocks/{stock_id}", headers=HEADERS)
    assert response.status_code == 200

    stock_data = response.json()
    print("Fetched stock data:", stock_data)  # Debugging output

    # Ensure we get the same symbol we created
    assert stock_data["symbol"].startswith("TEST")  # Check dynamic stock symbol

def test_get_all_stocks():
    """Test retrieving all stocks."""
    response = requests.get(f"{BASE_URL}/stocks", headers=HEADERS)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_stock_value(create_stock):
    """Test retrieving the value of a stock."""
    stock_id = create_stock
    response = requests.get(f"{BASE_URL}/stocks/stock-value/{stock_id}", headers=HEADERS)
    assert response.status_code == 200
    assert "stock_value" in response.json()

def test_portfolio_value():
    """Test getting portfolio value."""
    response = requests.get(f"{BASE_URL}/stocks/portfolio-value", headers=HEADERS)
    assert response.status_code == 200
    assert "portfolio_value" in response.json()

def test_missing_symbol():
    """Test adding a stock without a required field (symbol)."""
    stock_data = {
        "name": "Amazon.com, Inc.",
        "purchase price": 134.66,
        "purchase date": "18-06-2024",
        "shares": 7
    }
    response = requests.post(f"{BASE_URL}/stocks", json=stock_data, headers=HEADERS)
    assert response.status_code == 400  # Bad request

def test_delete_stock(create_stock):
    """Test deleting a stock."""
    stock_id = create_stock
    delete_response = requests.delete(f"{BASE_URL}/stocks/{stock_id}", headers=HEADERS)
    assert delete_response.status_code == 204  # No content

    # Verify it no longer exists
    get_response = requests.get(f"{BASE_URL}/stocks/{stock_id}", headers=HEADERS)
    assert get_response.status_code == 404  # Not found

def test_invalid_purchase_date():
    """Test adding a stock with an incorrect date format."""
    stock_data = {
        "name": "Alphabet Inc.",
        "symbol": "GOOG",
        "purchase price": 140.12,
        "purchase date": "INVALID_DATE",
        "shares": 14
    }
    response = requests.post(f"{BASE_URL}/stocks", json=stock_data, headers=HEADERS)
    assert response.status_code == 400  # Expecting failure due to invalid date format
