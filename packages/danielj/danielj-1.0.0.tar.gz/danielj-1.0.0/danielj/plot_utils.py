import matplotlib.pyplot as plt

def plot_forecast(forecast):
    """Plot a simple weather forecast."""
    days = [f.split(":")[0] for f in forecast]
    temperatures = [20 + i for i in range(len(forecast))]  # Mock temperatures
    
    plt.plot(days, temperatures, marker='o', label='Temperature (°C)')
    plt.xticks(rotation=45)
    plt.ylabel('Temperature (°C)')
    plt.title('7-Day Weather Forecast')
    plt.legend()
    plt.tight_layout()
    plt.show()
