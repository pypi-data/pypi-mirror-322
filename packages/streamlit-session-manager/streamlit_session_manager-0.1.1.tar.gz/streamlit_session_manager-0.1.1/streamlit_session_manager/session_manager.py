import extra_streamlit_components as stx
from typing import Optional, Dict, Any

class SessionManager:
    """
    A library to manage user session data from cookies in Streamlit apps
    """
    def __init__(self):
        self._cookie_manager = stx.CookieManager()

    def get_user(self) -> Optional[Dict[str, Any]]:
        """
        Fetch user details from cookies
        Returns: Dict with user details or None if not found
        """
        try:
            # Get basic user details
            email = self._cookie_manager.get('email')
            print(f"Email: {email}")
            if not email:
                return None

            # Get additional user details if available
            first_name = self._cookie_manager.get('firstName')
            print(f"First name: {first_name}")
            last_name = self._cookie_manager.get('lastName')
            print(f"Last name: {last_name}")
            
            user_data = {
                'email': email,
                'first_name': first_name,
                'last_name': last_name
            }
            
            # Remove None values
            return {k: v for k, v in user_data.items() if v is not None}
            
        except Exception as e:
            print(f"Error fetching user details: {str(e)}")
            return None

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
            first_name = self._cookie_manager.get('first_name')
            last_name = self._cookie_manager.get('last_name')
            
            if first_name or last_name:
                return ' '.join(filter(None, [first_name, last_name]))
            return None
            
        except Exception as e:
            print(f"Error fetching full name: {str(e)}")
            return None