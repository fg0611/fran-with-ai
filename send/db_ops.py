from generals import supabase_client, env_vars, Status

def buscar_lead(numero_contacto):
    try:
        response = supabase_client.table("leads").select("*").eq("id", numero_contacto).limit(1).execute()
        data = response.data
        if data:
            print("ℹ️ Lead encontrado:", data[0])
            return data[0]  # lead existente
        else:
            print("ℹ️ El Lead no existe aún")
            return None  # lead no encontrado
    except Exception as e:
        print("❌ Error al buscar lead:", e)
        return None

# Función para insertar contacto
def insertar_lead(numero_contacto, nombre):
    nuevo_lead = {
        "id": numero_contacto,
        "is_active": True,
        "origin": env_vars["admin_phone"],
        "name": nombre,
        "current_step": "greeting",
        "status": Status.contacted
    }
    try:
        response = supabase_client.table("leads").insert(nuevo_lead).execute()
        print("✅ Lead insertado correctamente:", response.data)
        return True
    except Exception as e:
        print("❌ Error al insertar lead:", e)
        return False

# Insertar mensaje en chats
def insertar_chat(numero_contacto, mensaje):
    nuevo_chat = {
        "session_id": numero_contacto,
        "message": mensaje,
        "is_from_user": False,
        "metadata": {}
    }
    try:
        response = supabase_client.table("chats").insert(nuevo_chat).execute()
        print("✅ mensaje guardado en chats", response.data)
        return True
    except Exception as e:
        print("❌ Error al insertar chat:", e)
        return False