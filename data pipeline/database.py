from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pprint import pprint

def get_client(user,password):

    uri = f"mongodb+srv://{user}:{password}@mldatabase.36zie.mongodb.net/?retryWrites=true&w=majority&appName=MLDatabase"
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        return client
    except Exception as e:
        print(e)


def main():
    load_dotenv()
    # Initialize the ApifyClient with your API token
    USER = os.getenv("MONGODB_USER_NAME")
    PASSWORD = os.getenv("MONGODB_USER_PASSWORD")
    mongo_client = get_client(USER, PASSWORD)

    try:
        database = mongo_client.get_database("sample_mflix")
        movies = database.get_collection("movies")
        # Query for a movie that has the title 'Back to the Future'
        query = { "title": "Back to the Future" }
        movie = movies.find_one(query)
        pprint(movie)
        mongo_client.close()
    except Exception as e:
        raise Exception("Unable to find the document due to the following error: ", e)
    


