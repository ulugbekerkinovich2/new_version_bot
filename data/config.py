from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()
# DSN = "postgresql://postgres:0852@localhost:5432/order_bot"
# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = os.environ.get('TOKEN')  # Bot toekn
# ADMINS = env.list("ADMINS")  # adminlar ro'yxati
ADMINS = os.environ.get("ADMINS")  # adminlar ro'yxati

DB_USER = env.str("DB_USER")
DB_PASS = env.str("DB_PASS")
DB_NAME = env.str("DB_NAME")
DB_HOST = env.str("DB_HOST")
DB_PORT = env.str("DB_PORT")
