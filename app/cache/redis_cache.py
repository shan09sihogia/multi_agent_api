import redis
import json
import hashlib
import logging 
from app.core.config import REDIS_URL


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


try:
    r = redis.Redis.from_url(REDIS_URL, decode_responses=True)
    r.ping()
    logging.info("Successfully connected to Redis at startup.")
except redis.exceptions.ConnectionError as e:
    logging.error(f"Initial Redis connection failed: {e}. Please check REDIS_URL and server status.")
    r = None 
except Exception as e:
    logging.error(f"An unexpected error occurred during Redis client initialization: {e}")
    r = None

def _get_redis_client():
    """
    Ensures a valid and connected Redis client instance is returned.
    Attempts to reconnect if the global client is None or the connection is stale.
    """
    global r
    if r is None:
        logging.warning("Redis client is not initialized. Attempting to reconnect...")
        try:
            r = redis.Redis.from_url(REDIS_URL, decode_responses=True)
            r.ping()
            logging.info("Successfully reconnected to Redis.")
        except redis.exceptions.ConnectionError as e:
            logging.error(f"Redis reconnection failed: {e}. Further operations will fail.")
            r = None 
            raise 
        except Exception as e:
            logging.error(f"An unexpected error occurred during Redis reconnection: {e}")
            r = None
            raise

    
    try:
        r.ping()
    except redis.exceptions.ConnectionError as e:
        logging.error(f"Redis connection lost during ping check: {e}. Attempting to re-establish.")
        r = None 
        return _get_redis_client()
    except Exception as e:
        logging.error(f"An unexpected error occurred during Redis ping check: {e}")
        r = None
        raise 
        
    return r


def _cache_key(session_id: str, prompt: str):
    """Generates a hashed key for the exact prompt cache."""
    h = hashlib.sha256(prompt.encode('utf-8')).hexdigest()
    return f"cache:{session_id}:{h}" 

def get_cached(session_id: str, prompt: str):
    """
    Retrieves cached response for a given session ID and exact prompt.
    """
    try:
        client = _get_redis_client()
        data = client.get(_cache_key(session_id, prompt))
        if data:
           
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                return data 
        return None
    except redis.exceptions.ConnectionError as e:
        logging.error(f"Redis connection error in get_cached: {e}")
        return None
    except Exception as e:
        logging.error(f"Error getting from exact prompt cache: {e}", exc_info=True) 
        return None

def set_cached(session_id: str, prompt: str, response: str, ttl: int = 300):
    """
    Caches a response for a given session ID and exact prompt with a Time-To-Live (TTL).
    """
    try:
        client = _get_redis_client()
       
        value_to_store = json.dumps(response) if isinstance(response, (dict, list)) else str(response)
        client.setex(_cache_key(session_id, prompt), ttl, value_to_store)
    except redis.exceptions.ConnectionError as e:
        logging.error(f"Redis connection error in set_cached: {e}")
    except Exception as e:
        logging.error(f"Error setting exact prompt cache: {e}", exc_info=True)

def _history_key(session_id: str):
    """Generates a key for conversational history."""
    return f"history:{session_id}"

def get_conversation_history(session_id: str, limit: int = 5):
    """
    Retrieves the last 'limit' turns of conversation history for a given session ID.
    Returns a list of dictionaries like [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
    """
    try:
        client = _get_redis_client()
        raw_history = client.lrange(_history_key(session_id), -limit, -1) 
        history = []
        for item in raw_history:
            try:
                history.append(json.loads(item))
            except json.JSONDecodeError:
                logging.warning(f"Warning: Could not decode history item (not valid JSON): '{item}'. Skipping.")
                pass 
        return history
    except redis.exceptions.ConnectionError as e:
        logging.error(f"Redis connection error in get_conversation_history: {e}")
        return []
    except Exception as e:
        logging.error(f"Error getting conversation history: {e}", exc_info=True)
        return []

def add_to_conversation_history(session_id: str, role: str, content: str, max_length: int = 10, ttl: int = 3600):
    """
    Adds a new turn to the conversation history for a given session ID.
    Keeps the history limited to max_length turns and sets a TTL for the entire list.
    """
    try:
        client = _get_redis_client()
        turn = {"role": role, "content": content}
        client.rpush(_history_key(session_id), json.dumps(turn))
        

        client.ltrim(_history_key(session_id), -max_length, -1) 
        
        client.expire(_history_key(session_id), ttl)

    except redis.exceptions.ConnectionError as e:
        logging.error(f"Redis connection error in add_to_conversation_history: {e}")
    except Exception as e:
        logging.error(f"Error adding to conversation history: {e}", exc_info=True)