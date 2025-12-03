import os
import sys
from dotenv import load_dotenv

# Add the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Load environment variables
load_dotenv()

try:
    from app.db.supabase import get_client
except ImportError as e:
    print(f"Error importing app.db.supabase: {e}")
    sys.exit(1)

def check_connection():
    print("Checking Supabase connection...")
    
    # Check if env vars are set
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")
    
    if not url:
        print("Error: SUPABASE_URL is not set in environment.")
    else:
        print(f"SUPABASE_URL: {url}")
        
    if not key:
        print("Error: SUPABASE_SERVICE_KEY is not set in environment.")
    else:
        print("SUPABASE_SERVICE_KEY: [Present]")

    if not url or not key:
        print("Missing configuration. Exiting.")
        return

    try:
        client = get_client()
        print("Client initialized.")
        
        print("Attempting to query 'desserts' table...")
        response = client.table("desserts").select("count", count="exact").limit(1).execute()
        
        print("Query successful!")
        print(f"Data: {response.data}")
        print(f"Count: {response.count}")
        
    except Exception as e:
        print(f"Connection failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_connection()
