import re

def limpiar_string(s):
   return re.sub(r'[^\w\s]', '', s, flags=re.UNICODE)
    # return re.sub(r'[^a-zA-Z0-9\s]', '', s)

    
v = 'cása & homre 123 / * +`´çñ 23jkhf'

print(limpiar_string(v))