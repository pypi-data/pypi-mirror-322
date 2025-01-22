import hashlib
import logging
import datetime
import requests


class APIClient:
    def __init__(self, base_url: str, api_token: str):
        """
        Initialize the API client.

        Parameters:
            base_url (str): The base URL of the API (e.g., 'http://localhost:8080').
            api_token (str): hvmnd-api API token
        """
        self.base_url = base_url
        self.logger = logging.getLogger("hvmnd_api_client")
        self.token = api_token

    def get_nodes(
            self,
            id_: int = None,
            renter: int = None,
            status: str = None,
            any_desk_address: str = None,
            software: str = None
    ):
        """
        Retrieve nodes based on provided filters.

        Parameters:
            id_ (int): Node ID.
            renter (int): Renter ID. If 'non_null', returns nodes with a non-null renter.
            status (str): Node status.
            any_desk_address (str): AnyDesk address.
            software (str): Software name to filter nodes that have it installed.

        Returns:
            List of nodes matching the criteria.
        """
        url = f"{self.base_url}/telegram/nodes"
        params = {
            'id': id_,
            'renter': renter,
            'status': status,
            'any_desk_address': any_desk_address,
            'software': software,
        }
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        response = self._handle_response(
            requests.get(
                url,
                params=params,
                headers={"Authorization": f"Bearer {self.token}"}
            )
        )

        nodes = response['data']
        for node in nodes:
            self._parse_timestamptz_field(node, 'rent_start_time')
            self._parse_timestamptz_field(node, 'last_balance_update_timestamp')
        response['data'] = nodes

        return response

    def update_node(self, node: dict):
        """
        Update a node.

        Parameters:
            node (dict): Node data to update.

        Returns:
            Confirmation message.
        """

        url = f"{self.base_url}/telegram/nodes"

        if node['rent_start_time']:
            node['rent_start_time'] = node['rent_start_time'].isoformat().replace('+00:00', 'Z')
        if node['last_balance_update_timestamp']:
            node['last_balance_update_timestamp'] = node['last_balance_update_timestamp'].isoformat().replace('+00:00',
                                                                                                              'Z')

        response = requests.patch(url, json=node, headers={"Authorization": f"Bearer {self.token}"})
        return self._handle_response(response)

    def get_payments(self, id_: int = None, user_id: int = None, status: str = None, limit: int = None):
        """
        Retrieve payments based on provided filters.

        Parameters:
            id_ (int): Payment ID.
            user_id (int): User ID.
            status (str): Payment status.
            limit (int): Limit the number of results.

        Returns:
            List of payments matching the criteria.
        """
        url = f"{self.base_url}/telegram/payments"
        params = {
            'id': id_,
            'user_id': user_id,
            'status': status,
            'limit': limit,
        }
        params = {k: v for k, v in params.items() if v is not None}

        response = self._handle_response(
            requests.get(
                url,
                params=params,
                headers={"Authorization": f"Bearer {self.token}"}
            )
        )

        payments = response['data']
        for payment in payments:
            self._parse_timestamptz_field(payment, 'datetime')
        response['data'] = payments

        return response

    def create_payment_ticket(self, user_id: int, amount: float):
        """
        Create a payment ticket.

        Parameters:
            user_id (int): User ID.
            amount (float): Amount for the payment.

        Returns:
            Payment ticket ID.
        """
        url = f"{self.base_url}/telegram/payments"
        payload = {"user_id": user_id, "amount": amount}
        response = requests.post(url, json=payload, headers={"Authorization": f"Bearer {self.token}"})
        return self._handle_response(response)

    def complete_payment(self, id_: int):
        """
        Complete a payment.

        Parameters:
            id_ (int): Payment ID.

        Returns:
            Confirmation of payment completion.
        """
        url = f"{self.base_url}/telegram/payments/complete/{id_}"
        response = requests.patch(url, headers={"Authorization": f"Bearer {self.token}"})
        return self._handle_response(response)

    def cancel_payment(self, id_: int):
        """
        Cancel a payment.

        Parameters:
            id_ (int): Payment ID.

        Returns:
            Confirmation of payment cancellation.
        """
        url = f"{self.base_url}/telegram/payments/cancel/{id_}"
        response = requests.patch(url, headers={"Authorization": f"Bearer {self.token}"})
        return self._handle_response(response)

    def get_users(
            self,
            id_: int = None,
            telegram_id: int = None,
            username: str = None,
            limit: int = None
    ):
        """
        Retrieve users based on provided filters.

        Parameters:
            id_ (int): User ID.
            telegram_id (int): Telegram ID.
            username (str): Telegram Username.
            limit (int): Limit the number of results.

        Returns:
            List of users matching the criteria.
        """
        url = f"{self.base_url}/telegram/users"
        params = {
            'id': id_,
            'telegram_id': telegram_id,
            'username': username,
            'limit': limit
        }
        params = {k: v for k, v in params.items() if v is not None}
        response = requests.get(url, params=params, headers={"Authorization": f"Bearer {self.token}"})
        return self._handle_response(response)

    def create_user(
        self,
        user_data: dict
    ):
        """
        Create a new user.

        Parameters:
            user_data (dict): A dictionary representing the user entity with the following keys:
                - telegram_id (int): Telegram ID of the user to update.
                - total_spent (float, optional): Updated total spent by the user.
                - balance (float, optional): Updated balance of the user.
                - first_name (str, optional): Updated first name of the user.
                - last_name (str, optional): Updated last name of the user.
                - username (str, optional): Updated username of the user.
                - language_code (str, optional): Updated language code of the user.
                - banned (bool, optional): Updated ban status of the user.

        Returns:
            dict: Created user data.
        
        Raises:
            ValueError: If 'telegram_id' is not provided in the user_data.
        """

        if 'telegram_id' not in user_data:
            raise ValueError("telegram_id is required to update a user")

        url = f"{self.base_url}/telegram/users"
        
        payload = {k: v for k, v in user_data.items() if v is not None}
        response = requests.post(url, json=payload, headers={"Authorization": f"Bearer {self.token}"})
        return self._handle_response(response)

    def update_user(self, user_data: dict):
        """
        Update an existing user.

        Parameters:
            user_data (dict): A dictionary representing the user entity with the following keys:
                - telegram_id (int): Telegram ID of the user to update.
                - total_spent (float, optional): Updated total spent by the user.
                - balance (float, optional): Updated balance of the user.
                - first_name (str, optional): Updated first name of the user.
                - last_name (str, optional): Updated last name of the user.
                - username (str, optional): Updated username of the user.
                - language_code (str, optional): Updated language code of the user.
                - banned (bool, optional): Updated ban status of the user.

        Returns:
            dict: Updated user data.

        Raises:
            ValueError: If 'telegram_id' is not provided in the user_data.
        """
        if 'telegram_id' not in user_data:
            raise ValueError("telegram_id is required to update a user")

        url = f"{self.base_url}/telegram/users"

        # Remove keys with None values from the dictionary
        payload = {k: v for k, v in user_data.items() if v is not None}

        response = requests.put(url, json=payload, headers={"Authorization": f"Bearer {self.token}"})
        return self._handle_response(response)

    def ping(self):
        """
        Ping the API.

        Returns:
            True if the API is reachable.
        """
        url = f"{self.base_url}/ping"
        response = requests.get(url)
        return response.status_code == 200

    def save_hash_mapping(self, question: str, answer: str):
        """
        Save a hash mapping for a question and answer.

        Parameters:
            question (str): The question text.
            answer (str): The answer text.

        Returns:
            dict: Response data, including the hash.
        """
        url = f"{self.base_url}/telegram/quiz/save-hash"
        payload = {"question": question, "answer": answer}
        response = requests.post(url, json=payload, headers={"Authorization": f"Bearer {self.token}"})
        return self._handle_response(response)

    def get_question_answer_by_hash(self, answer_hash: str):
        """
        Retrieve a question and answer using the hash.

        Parameters:
            answer_hash (str): The hash value.

        Returns:
            dict: The question and answer.
        """
        url = f"{self.base_url}/telegram/quiz/get-question-answer"
        params = {"hash": answer_hash}
        response = requests.get(url, params=params, headers={"Authorization": f"Bearer {self.token}"})
        return self._handle_response(response)

    def save_user_answer(self, telegram_id: int, question: str, answer: str):
        """
        Save a user's answer to a question.

        Parameters:
            telegram_id (int): The Telegram ID of the user.
            question (str): The question text.
            answer (str): The answer text.

        Returns:
            dict: Response data.
        """
        url = f"{self.base_url}/telegram/quiz/save-answer"
        payload = {
            "telegram_id": telegram_id,
            "question": question,
            "answer": answer
        }
        response = requests.post(url, json=payload, headers={"Authorization": f"Bearer {self.token}"})
        return self._handle_response(response)

    def create_login_token(self, id_: int, telegram_id: int, status: str | None = None):
        """
        Create or retrieve a login token for a user based on their Telegram ID.

        Parameters:
            id_ (int): The user's ID in the 'users' table.
            telegram_id (int): The user's Telegram ID.
            status (str): Token status.
        """
        url = f"{self.base_url}/telegram/tokens"
        payload = {
            "user_id": id_,
            "telegram_id": telegram_id,
            "status": status
        }

        if not status:
            del payload['status']

        response = requests.post(url, json=payload, headers={"Authorization": f"Bearer {self.token}"})
        return self._handle_response(response)

    def get_login_token(self, id_: int | None = None, telegram_id: int | None = None):
        """
        Create or retrieve a login token for a user based on their Telegram ID.

        Parameters:
            id_ (int): The user's ID in the 'users' table.
            telegram_id (int): The user's Telegram ID.
        """
        url = f"{self.base_url}/telegram/tokens"
        query_params = {}
        if id_:
            query_params = {
                "user_id": id_
            }
        if telegram_id:
            query_params = {
                "telegram_id": telegram_id
            }

        response = requests.get(url, params=query_params, headers={"Authorization": f"Bearer {self.token}"})
        return self._handle_response(response)

    def get_notifications(
            self,
            user_id: int = None,
            notification_platform: str = None,
            is_read: bool = None,
            is_sent: bool = None
    ):
        """
        Fetch notifications based on filters.

        Args:
            user_id (int, optional): The ID of the user to filter notifications.
            notification_platform (str, optional): The platform to filter notifications (e.g., "text").
            is_read (bool, optional): Filter by read status (True for read, False for unread).
            is_sent (bool, optional): Filter by sent status (True for sent, False for not sent).

        Returns:
            dict: Parsed response from the API, typically including a list of notifications.

        Raises:
            HTTPError: If the request fails or returns an error status code.
        """
        url = f"{self.base_url}/common/notifications"
        query_params = {}

        # Add query parameters only if they are provided
        if user_id is not None:
            query_params["user_id"] = user_id
        if notification_platform:
            query_params["notification_platform"] = notification_platform
        if is_read is not None:
            query_params["is_read"] = str(is_read).lower()  # Convert bool to "true"/"false"
        if is_sent is not None:
            query_params["is_sent"] = str(is_sent).lower()  # Convert bool to "true"/"false"

        # Send the GET request
        response = requests.get(url, params=query_params, headers={"Authorization": f"Bearer {self.token}"})

        # Handle and return the response
        return self._handle_response(response)

    def create_notification(
            self,
            user_id: int,
            notification_text: str,
            notification_platform: str = "all"
    ):
        """
        Create a new notification.

        Args:
            user_id (int): The ID of the user for whom the notification is created.
            notification_text (str): The text of the notification.
            notification_platform (str, optional): The platform of the notification. Defaults to "all".

        Returns:
            dict: Parsed response from the API, typically including the created notification data.

        Raises:
            HTTPError: If the request fails or returns an error status code.
        """
        url = f"{self.base_url}/common/notifications"
        payload = {
            "user_id": user_id,
            "notification_text": notification_text,
            "notification_platform": notification_platform
        }

        response = requests.post(url, json=payload, headers={"Authorization": f"Bearer {self.token}"})
        return self._handle_response(response)

    def update_notification(
            self,
            notification_id: int,
            user_id: int = None,
            notification_text: str = None,
            notification_platform: str = None,
            is_read: bool = None,
            is_sent: bool = None
    ):
        """
        Update an existing notification.

        Args:
            notification_id (int): The ID of the notification to update.
            user_id (int, optional): The ID of the user. If not provided, the existing value remains unchanged.
            notification_text (str, optional): The new text for the notification. Defaults to None.
            notification_platform (str, optional): The platform for the notification. Defaults to None.
            is_read (bool, optional): Whether the notification has been read. Defaults to None.
            is_sent (bool, optional): Whether the notification has been sent. Defaults to None.

        Returns:
            dict: Parsed response from the API, typically including the updated notification data.

        Raises:
            HTTPError: If the request fails or returns an error status code.
        """
        url = f"{self.base_url}/common/notifications"
        payload = {
            "id": notification_id,
            "user_id": user_id,
            "notification_text": notification_text,
            "notification_platform": notification_platform,
            "is_read": is_read,
            "is_sent": is_sent
        }

        # Remove None values from the payload
        payload = {key: value for key, value in payload.items() if value is not None}

        response = requests.put(url, json=payload, headers={"Authorization": f"Bearer {self.token}"})
        return self._handle_response(response)

    # --- Utility Methods ---

    def _parse_timestamptz_field(self, data: dict, field_name: str):
        """
        Convert a timestamptz field in ISO 8601 format to a datetime object with timezone support.

        Parameters:
            data (dict): The dictionary containing the field.
            field_name (str): The name of the field to convert.

        Returns:
            None: Modifies the `data` dictionary in place.
        """
        if field_name in data and data[field_name]:
            try:
                data[field_name] = datetime.datetime.fromisoformat(data[field_name])
            except Exception as e:
                self.logger.debug(f"Failed to parse field {field_name} ('{data[field_name]}'): {e}")
                data[field_name] = None

    @staticmethod
    def generate_hash(question: str, answer: str) -> str:
        """
        Generate a hash for a question and answer.

        Parameters:
            question (str): The question text.
            answer (str): The answer text.

        Returns:
            str: A 32-character hash.
        """
        data = question + answer
        hash_object = hashlib.sha256(data.encode())
        return hash_object.hexdigest()[:32]

    def _handle_response(self, response):
        """
        Handle the API response.

        Parameters:
            response (requests.Response): The response object.

        Returns:
            Parsed JSON data if successful.

        Raises:
            Exception: If the API returns an error or invalid response.
        """
        try:
            json_data = response.json()
        except ValueError:
            # Response is not JSON
            response.raise_for_status()
            raise Exception(f"Invalid response: {response.text}")

        if 200 <= response.status_code < 300:
            if not json_data.get('success', False):
                error_message = json_data.get('error', 'Unknown error')
                raise Exception(f"API Error: {error_message}")
            else:
                return json_data
        if 404 == response.status_code:
            self.logger.debug(json_data.get('error', response.reason))
            return {
                'success': False,
                'error': json_data.get('error', response.reason),
                'data': []
            }
        else:
            error_message = json_data.get('error', response.reason)
            self.logger.debug(error_message)
            raise Exception(f"API Error: {error_message}")
