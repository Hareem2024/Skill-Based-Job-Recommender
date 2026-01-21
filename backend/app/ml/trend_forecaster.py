"""
Time-series forecasting for skill demand trends.
"""
from typing import Dict, List, Any
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

class TrendForecaster:
    """Forecast skill demand trends."""
    
    async def forecast(
        self,
        dates: List[datetime],
        values: List[int],
        days_ahead: int
    ) -> Dict[str, Any]:
        """Forecast future values using simple moving average and trend."""
        if len(values) < 7:
            return {"error": "Insufficient data"}
        
        # Convert to pandas for easier manipulation
        df = pd.DataFrame({
            'date': dates,
            'value': values
        })
        df = df.sort_values('date')
        df = df.set_index('date')
        
        # Resample to daily if needed
        df = df.resample('D').mean().fillna(method='ffill')
        
        # Simple forecasting: moving average + trend
        window = min(7, len(df))
        ma = df['value'].rolling(window=window).mean().iloc[-1]
        
        # Calculate trend
        if len(df) >= 2:
            recent_values = df['value'].tail(7).values
            trend = (recent_values[-1] - recent_values[0]) / len(recent_values)
        else:
            trend = 0
        
        # Generate forecast
        forecast_dates = []
        forecast_values = []
        last_date = df.index[-1]
        last_value = df['value'].iloc[-1]
        
        for i in range(1, days_ahead + 1):
            forecast_date = last_date + timedelta(days=i)
            forecast_value = max(0, last_value + (trend * i))
            forecast_dates.append(forecast_date.isoformat())
            forecast_values.append(round(forecast_value, 2))
        
        return {
            "dates": forecast_dates,
            "values": forecast_values,
            "current_value": float(last_value),
            "trend": "increasing" if trend > 0 else "decreasing" if trend < 0 else "stable"
        }

