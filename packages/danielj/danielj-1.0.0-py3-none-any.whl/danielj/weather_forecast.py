import datetime

def predict_weather():
    """Generate a mock weather forecast for the next 7 days."""
    forecast = []
    for i in range(7):
        day = datetime.date.today() + datetime.timedelta(days=i)
        forecast.append(f"{day}: Sunny with a chance of rain.")
    return forecast
