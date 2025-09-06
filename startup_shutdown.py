from .database import client

# @app.on_event("startup")
async def startup_event():
    """Initialize MongoDB connection on startup"""
    try:
        # Test the connection
        await client.admin.command('ping')
        print("Successfully connected to MongoDB")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")

# @app.on_event("shutdown")
async def shutdown_event():
    """Close MongoDB connection on shutdown"""
    client.close()
    print("MongoDB connection closed")