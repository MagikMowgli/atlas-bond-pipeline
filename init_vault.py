from app.database import init_db

if __name__ == "__main__":
    
    try:
        init_db()
        print(f"Vault Built successfully")
    except Exception as e:
        print(f"Construction failed: {e}")
