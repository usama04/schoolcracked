from pymongo.mongo_client import MongoClient
# import settings

# uri = f"mongodb+srv://{settings.MONGODB_ADMIN_USER}:{settings.MONGODB_ADMIN_PASS}@cluster0.kbdig39.mongodb.net/?retryWrites=true&w=majority"

# uri = f"mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false"

uri = "mongodb://localhost:27017/"

# Create a new client and connect to the server
client = MongoClient(uri)
# Send a ping to confirm a successful connection
db = client["schoolcracked"]

collection_name = db["chats"]

if __name__ == "__main__":
    print("Connected to MongoDB Atlas!")
    for x in client.list_database_names():
        print(x)