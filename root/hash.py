from werkzeug.security import generate_password_hash

hashf = input('Enter the string you want the hash of :')

print(f' This is the genereated hasg for your string - {generate_password_hash(hashf)}')