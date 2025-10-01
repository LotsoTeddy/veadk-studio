from veadk import Agent
from veadk.tools.demo_tools import get_city_weather

root_agent = Agent(
    name="weather_reporter",
    description="An agent for reporting weather.",
    instruction="You can invoke `get_city_weather` for fetching a city weather. If user does not ask information about weather, just answer user as usual.",
    tools=[get_city_weather],
)
