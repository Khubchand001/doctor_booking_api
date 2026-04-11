import secrets
import os

def generate_and_update_env():
    # Generate a secure 32-byte secret key
    secret_key = secrets.token_hex(32)
    print(f"Generated Secret Key: {secret_key}")

    env_path = ".env"
    if not os.path.exists(env_path):
        with open(env_path, "w") as f:
            f.write(f"SECRET_KEY={secret_key}\n")
        print("Created .env and added SECRET_KEY.")
    else:
        with open(env_path, "r") as f:
            lines = f.readlines()
        
        updated = False
        new_lines = []
        for line in lines:
            if line.startswith("SECRET_KEY="):
                new_lines.append(f"SECRET_KEY={secret_key}\n")
                updated = True
            else:
                new_lines.append(line)
        
        if not updated:
            new_lines.append(f"SECRET_KEY={secret_key}\n")
        
        with open(env_path, "w") as f:
            f.writelines(new_lines)
        print("Updated SECRET_KEY in .env.")

if __name__ == "__main__":
    generate_and_update_env()
