from config.config import Config, load_config

config: Config = load_config(".env")

print(f"Bot token: {config.bot.token}")
print(f"Admin IDs: {config.bot.admin_ids}")
print()