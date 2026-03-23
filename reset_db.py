from app.database import Base, engine

print("🧨 Dropping old Postgres vault...")
Base.metadata.drop_all(bind=engine)
print("✅ Demolition complete. The plot is empty.")