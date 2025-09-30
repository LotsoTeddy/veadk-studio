from veadk import Agent
from veadk.tools.demo_tools import get_city_weather

root_agent = Agent(
    name="mocked_name",
    description="An intelligent agent",
    instruction="You are an agent",
    tools=[get_city_weather],
)
