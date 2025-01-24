# DYNAMIC Fire risk indicator implementation

This repository contains the implementation of the dynamic fire risk indicator is based upon the research paper:

R.D. Strand and L.M. Kristensen: *An implementation, evaluation and validation of a dynamic fire and conflagration risk indicator for wooden homes*. In volume 238 of Procedia Computer Science, pp. 49-56, 2024. Proceedings of the 15th International Conference on Ambient Systems, Networks and Technologies Networks (ANT). Online:  https://www.sciencedirect.com/science/article/pii/S187705092401233X

The fire risk indicator uses forecast and weather data observation for computing fire risk indication in the form of time-to-flash-over (ttf) for wooden houses. 

# Weather Data Sources

The implementation has been designed to be independent of any particular cloud-based weather data service. 

This library contains an implementation that use the weather data services provided by the Norwegian Meteorological Institute (MET):

- MET Frost API for weather data observations: https://frost.met.no/index.html
- MET Forecasting API for weather data forecasts: https://api.met.no/weatherapi/locationforecast/2.0/documentation 

To use these pre-implemented clients a file name `.env` must be place in your project folder having the following content:

```
MET_CLIENT_ID = '<INSERT CLIENT ID HERE>'
MET_CLIENT_SECRET = '<INSERT CLIENT SECRET HERE>'
```

Credentials for using the MET APIs can be obtained via: https://frost.met.no/auth/requestCredentials.html

Please make sure that you conform to the terms of service which includes restrictions on the number of API calls.

# Example usage

The following example shows how to use the `FireRiskPrediction` class to compute fire risks for a given location:


```python
import datetime

from frcm.frcapi import METFireRiskAPI
from frcm.datamodel.model import Location

# sample code illustrating how to use the Fire Risk Computation API (FRCAPI)
if __name__ == "__main__":

    frc = METFireRiskAPI()

    location = Location(latitude=60.383, longitude=5.3327)  # Bergen
    # location = Location(latitude=59.4225, longitude=5.2480)  # Haugesund

    obs_delta = datetime.timedelta(days=2)

    predictions = frc.compute_now(location, obs_delta)

    print(predictions)
```

and should result in an output similar to what is listed below showing hourly computed fire risks for the given location.

```
FireRiskPrediction[latitude=60.383 longitude=5.3327]
FireRisks[2025-01-20 00:00:00+00:00 TTF(6.072481167177002) WindSpeed(3.1)]
FireRisks[2025-01-20 01:00:00+00:00 TTF(5.99332738001279) WindSpeed(2.4)]
FireRisks[2025-01-20 02:00:00+00:00 TTF(5.967689363087894) WindSpeed(2.7)]
FireRisks[2025-01-20 03:00:00+00:00 TTF(5.9478787329422635) WindSpeed(2.1)]
FireRisks[2025-01-20 04:00:00+00:00 TTF(5.928838874113078) WindSpeed(2.8)]
FireRisks[2025-01-20 05:00:00+00:00 TTF(5.912460820817552) WindSpeed(3.4)]

[ ... ]

FireRisks[2025-01-31 23:00:00+00:00 TTF(6.273135517647007) WindSpeed(4.566666666666666)]
FireRisks[2025-02-01 00:00:00+00:00 TTF(6.290499308219714) WindSpeed(4.6)]
FireRisks[2025-02-01 01:00:00+00:00 TTF(6.303115875685305) WindSpeed(4.533333333333333)]
FireRisks[2025-02-01 02:00:00+00:00 TTF(6.30566616713959) WindSpeed(4.466666666666667)]
FireRisks[2025-02-01 03:00:00+00:00 TTF(6.301802227245228) WindSpeed(4.3999999999999995)]
FireRisks[2025-02-01 04:00:00+00:00 TTF(6.2932319226402) WindSpeed(4.333333333333333)]
FireRisks[2025-02-01 05:00:00+00:00 TTF(6.281008572496977) WindSpeed(4.266666666666667)]
FireRisks[2025-02-01 06:00:00+00:00 TTF(6.265861044817225) WindSpeed(4.2)]
```

# API and implementation

The following methods are the main services currently being provided by the API:

- `get_weatherdata_now(location: Location, obs_delta: datetime.timedelta) -> WeatherData` - which provided with a location and a weather data observation time delta fetches weather data observations `obs_delta` into the past and concatenates this with the weather data from the current weather forecast for the location.
- `compute(wd: WeatherData) -> FireRiskPrediction` - which computes a fire risk predication based on the provided weather data.
- `compute_now(location: Location, obs_delta: datetime.timedelta) -> FireRiskPrediction` - which computes a fire risk predication for the current point in time using weather data observations `obs_delta` into the past. 

The source code for the library is available at via the `Download files` and is organised into the following main folders:

- `datamodel` - contains an implementation of the data model used for weather data and fire risk indications
- `weatherdata` contains an client implementations and interfaces for fetching weather data from cloud services.
- `fireriskmodel` contains an implementation of the underlying fire risk model
T
The main API for the implementation is in the file `frcapi.py`



