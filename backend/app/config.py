import os

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "")      # set in Render env
ADMIN_ACCESS_KEY = os.getenv("ADMIN_ACCESS_KEY", "")  # set in Render env

# DB later
DATABASE_URL = os.getenv("DATABASE_URL", "")
