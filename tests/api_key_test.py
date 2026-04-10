#from keycove import generate_token, hash
from keycove import encrypt, decrypt, generate_secret_key
import hashlib


def main() -> None:
    #api_key = generate_token()
    #hashed = hash(value_to_hash=api_key)
    #print(api_key)
    #print(hashed)
    secret_key = generate_secret_key() 
    encrypted_key = encrypt(value_to_encrypt=hashlib.sha512().hexdigest(), secret_key=secret_key)
    decrypted_key = decrypt(encrypted_value=encrypted_key, secret_key=secret_key)
    print("Encrypted key", encrypted_key)
    print("Decrypted key", decrypted_key)

if __name__ == '__main__':
    main()
