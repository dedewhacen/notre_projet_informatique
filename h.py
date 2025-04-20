import bcrypt

mot_de_passe = "1111"
hashed = bcrypt.hashpw(mot_de_passe.encode('utf-8'), bcrypt.gensalt())
print("Hash bcrypt à mettre dans la base :", hashed.decode('utf-8'))
