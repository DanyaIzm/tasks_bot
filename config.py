from dataclasses import dataclass
from dotenv import load_dotenv
import os


@dataclass
class Config:
    BOT_TOKEN: str


def load_config() -> Config:
    load_dotenv(".env")

    return Config(
        BOT_TOKEN=os.getenv("BOT_TOKEN"),
    )
