from veadk import Agent
from veadk.knowledgebase import KnowledgeBase
from veadk.memory import ShortTermMemory
from veadk.memory.long_term_memory import LongTermMemory
from veadk.tools.demo_tools import get_city_weather

root_agent = Agent(
    name="weather_reporter",
    description="An agent for reporting weather.",
    instruction="You can invoke `get_city_weather` for fetching a city weather. If user does not ask information about weather, just answer user as usual.",
    short_term_memory=ShortTermMemory(),
    long_term_memory=LongTermMemory(),
    knowledgebase=KnowledgeBase(app_name="weather_reporter"),
    tools=[get_city_weather],
)
