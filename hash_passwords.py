import bcrypt

passwords = ['Test1!', 'Test2!']
for pw in passwords:
    hashed = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
    print(hashed.decode())