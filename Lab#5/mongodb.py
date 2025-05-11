import os
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from pymongo.collection import Collection


MONGODB_URI = os.environ.get("MONGODB_URI")
MONGODB_DATABASE_NAME = os.environ.get("MONGODB_DATABASE_NAME", "mydatabase")  # Default db name
client: MongoClient = None # Declare client as a global variable
reviews_ar_collection: Collection = None
products_collection: Collection = None
reviews_en_collection: Collection = None

async def get_database():
    """
    Dependency function to get the database connection.
    """
    global client
    if client is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database connection not initialized.")
    db = client[MONGODB_DATABASE_NAME]
    return db

async def connect_to_mongo():
    """
    Startup event handler to connect to MongoDB.
    """
    global client
    if client is None:
        try:
            # Use the MONGODB_URI from the environment, with encoding
            uri = MONGODB_URI
            if not uri:
                raise ValueError("MONGODB_URI is not set in the environment.")
            client = MongoClient(uri)
            client.admin.command('ping')  # Check connection
            print("Connected to MongoDB Atlas")
        except PyMongoError as e:
            print(f"Failed to connect to MongoDB: {e}")
            client = None  # Reset to None to prevent further attempts
            raise  # Re-raise the exception to prevent app startup

async def close_mongo_connection():
    """
    Shutdown event handler to close the MongoDB connection.
    """
    global client
    if client:
        client.close()
        client = None
        print("Disconnected from MongoDB Atlas")

async def get_arabic_reviews():
    """Retrieves all reviews from the MongoDB collection."""
    if reviews_ar_collection is None:
        raise Exception(detail="MongoDB not connected.")
    try:
        # Fetch all documents from the collection
        reviews = list(reviews_ar_collection.find())
        # Convert MongoDB ObjectId to string for JSON serialization
        for review in reviews:
            review['_id'] = str(review['_id'])
        return reviews
    except Exception as e:
        raise Exception(detail="Couldn't retrieve Arabic reviews.")