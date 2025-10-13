from veadk import Agent
from veadk.knowledgebase import KnowledgeBase
from veadk.memory import ShortTermMemory
from veadk.memory.long_term_memory import LongTermMemory
from veadk.tools.builtin_tools.generate_image import image_generate
from veadk.tools.demo_tools import get_city_weather

root_agent = Agent(
    name="weather_reporter",
    description="An agent.",
    instruction="You are an agent.",
    short_term_memory=ShortTermMemory(),
    # long_term_memory=LongTermMemory(),
    # knowledgebase=KnowledgeBase(app_name="weather_reporter"),
    tools=[get_city_weather, image_generate],
)
