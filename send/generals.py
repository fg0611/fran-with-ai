from dotenv import load_dotenv
import os
import enum
from supabase import create_client

# Define el ENUM para los estados del lead
class Status(str, enum.Enum):
    contacted = "contacted"
    responded = "responded"
    completed = "completed"
    quoted = "quoted"
    signed = "signed"

    # Configuración
load_dotenv(dotenv_path=r"C:\Users\Francisco\Desktop\DEV_STUFF\00_OPTIBOT\automatizacion-wp\fran-with-ai\send\.env")

env_vars = {
"url" : os.environ.get("SUPABASE_URL"),
"key": os.environ.get("SUPABASE_KEY"),
"admin_phone" : os.environ.get("ADMIN_PHONE")
}

supabase_client = create_client(env_vars['url'], env_vars['key'])
