from datetime import datetime
from meteostat import Daily, Point

nairobi = Point(-1.286389, 36.817223)

start = datetime(2019, 1, 1)
end = datetime(2025, 10, 5)

data = Daily(nairobi, start, end)
data = data.fetch()
data.to_csv("../weather/app/nairobi_weather.csv")
