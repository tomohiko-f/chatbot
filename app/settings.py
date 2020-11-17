import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env")
load_dotenv()

channel_access_token = os.environ.get("CHANNEL_ACCESS_TOKEN")
channel_secret = os.environ.get("CHANNEL_SECRET")
