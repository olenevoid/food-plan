from environs import env


env.read_env()


BOT_TOKEN = env.str("BOT_TOKEN")
