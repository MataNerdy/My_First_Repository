import os
from environs import Env

env = Env()
env.read_env(override=True)
bot_token = env("BOT_TOKEN")
admin_id = env("ADMIN_ID")

print(f"Bot token: {bot_token}")
print(f"Admin ID: {admin_id}")
print()

print(os.getenv("BOT_TOKEN"))
print(os.getenv("ADMIN_ID"))