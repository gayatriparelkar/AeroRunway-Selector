import pytest
from runway_selector import (
    get_airport_info,
    get_weather_data,
    get_current_utc_time,
    get_runways,
    format_runway,
    select_best_runway,
)
from unittest.mock import patch


# Test for get_airport_info function
def test_get_airport_info():
    name, icao, city, timezone = get_airport_info("JFK")
    assert name is not None
    assert icao == "KJFK"
    assert city == "New York"
    assert timezone == "UTC"


# Test for get_weather_data function (mocking API request)
@patch("runway_selector.requests.get")
def test_get_weather_data(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "wind": {"deg": 180},
        "main": {"temp": 25},
        "weather": [{"description": "clear sky"}],
    }
    wind, temp, condition = get_weather_data("New York")
    assert wind == 180
    assert temp == 25
    assert condition == "Clear sky"


# Test for get_current_utc_time function
def test_get_current_utc_time():
    utc_time = get_current_utc_time("UTC")
    assert "UTC" in utc_time


# Test for get_runways function
def test_get_runways():
    runways = get_runways("KJFK")  # Example ICAO Code
    assert isinstance(runways, list)


# Test for format_runway function
def test_format_runway():
    assert format_runway(90) == "09/27"
    assert format_runway(360) == "36/18"
    assert format_runway(0) == "36/18"
    assert format_runway(180) == "18/36"


# Test for select_best_runway function
def test_select_best_runway():
    runways = [[90, 270], [180, 360], [10, 190]]
    assert select_best_runway(100, runways) == 90
    assert select_best_runway(200, runways) == 180
    assert select_best_runway(5, runways) == 10
    assert select_best_runway(350, runways) == 360



from project import select_best_runway

def test_select_best_runway():
    runways = [[90, 270], [180, 360]]
    assert select_best_runway(100, runways) == 90
    assert select_best_runway(200, runways) == 180
    assert select_best_runway(350, runways) == 360

    if __name__ == "__main__":
    pytest.main()
