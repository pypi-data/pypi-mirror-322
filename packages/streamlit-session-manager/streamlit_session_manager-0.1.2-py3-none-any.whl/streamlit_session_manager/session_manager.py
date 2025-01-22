import extra_streamlit_components as stx
from typing import Optional, Dict, Any
import time

class SessionManager:
    """
    A library to manage user session data from cookies in Streamlit apps
    """
    def __init__(self):
        print("Session manager initialized")
        self._cookie_manager = stx.CookieManager()

    def get_user(self) -> Optional[Dict[str, Any]]:
        """
        Fetch user details from cookies
        Returns: Dict with user details or None if not found
        """
        max_retries = 3  # Maximum number of retries
        retry_delay = 0.5  # Delay in seconds between retries
        for attempt in range(max_retries):
            try:
                # Get basic user details
                email = self._cookie_manager.get('email')
                first_name = self._cookie_manager.get('firstName')
                last_name = self._cookie_manager.get('lastName')
                
                # If we have any valid data, return it
                if any([email, first_name, last_name]):
                    print(f"Email: {email}")
                    print(f"First name: {first_name}")
                    print(f"Last name: {last_name}")
                    
                    user_data = {
                        'email': email,
                        'first_name': first_name,
                        'last_name': last_name
                    }
                    return {k: v for k, v in user_data.items() if v is not None}
                
                # If no valid data and not last attempt, wait and retry
                if attempt < max_retries - 1:
                    print(f"Attempt {attempt + 1}: No data found, retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                
            except Exception as e:
                print(f"Error fetching user details: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
        
        return None  # Return None if all retries failed

    def get_email(self) -> Optional[str]:
        """
        Fetch only user email from cookies
        Returns: Email string or None if not found
        """
        try:
            return self._cookie_manager.get('email')
        except Exception as e:
            print(f"Error fetching email: {str(e)}")
            return None

    def get_full_name(self) -> Optional[str]:
        """
        Fetch and combine first and last name
        Returns: Full name string or None if neither found
        """
        try:
            first_name = self._cookie_manager.get('firstName')
            last_name = self._cookie_manager.get('lastName')
            
            if first_name or last_name:
                return ' '.join(filter(None, [first_name, last_name]))
            return None
            
        except Exception as e:
            print(f"Error fetching full name: {str(e)}")
            return None