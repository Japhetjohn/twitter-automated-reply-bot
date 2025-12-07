import requests
import time
import json


class GrokClient:
    """
    LLM API client for generating tweets.

    Supports Hugging Face Inference API (free tier) and other OpenAI-compatible APIs.
    Handles API communication with retry logic, rate limiting, and comprehensive error handling.
    """

    def __init__(self, api_key, model="meta-llama/Llama-3.3-70B-Instruct", temperature=0.7, max_tokens=100, api_endpoint=None):
        """
        Initialize LLM API client.

        Args:
            api_key: API key (HF_TOKEN for Hugging Face)
            model: Model to use (default: meta-llama/Llama-3.3-70B-Instruct)
            temperature: Creativity level 0.0-1.0 (default: 0.7)
            max_tokens: Maximum tokens to generate (default: 100)
            api_endpoint: API endpoint URL (default: Hugging Face)
        """
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.api_endpoint = api_endpoint or "https://router.huggingface.co/v1/chat/completions"
        self.timeout = 60  # seconds (HF can be slower)

    def generate_tweet(self, system_prompt, user_prompt, max_retries=3):
        """
        Generate a tweet using LLM API.

        Args:
            system_prompt: System instructions (brand voice, rules)
            user_prompt: Specific tweet request
            max_retries: Number of retry attempts on failure

        Returns:
            str: Generated tweet text

        Raises:
            Exception: If all retry attempts fail
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        for retry_count in range(max_retries):
            try:
                response = self._make_request(messages, retry_count)

                # Extract tweet from response
                if response and 'choices' in response and len(response['choices']) > 0:
                    tweet = response['choices'][0]['message']['content'].strip()
                    return tweet
                else:
                    raise Exception("Invalid response structure from API")

            except Exception as e:
                error_message = str(e)

                # Check if we should retry
                if retry_count < max_retries - 1:
                    wait_time = self._handle_api_error(error_message, retry_count)
                    if wait_time > 0:
                        print(f"   Waiting {wait_time}s before retry...")
                        time.sleep(wait_time)
                else:
                    # Final attempt failed
                    raise Exception(f"LLM API failed after {max_retries} attempts: {error_message}")

    def _make_request(self, messages, retry_count):
        """
        Make HTTP request to Grok API.

        Args:
            messages: List of message objects
            retry_count: Current retry attempt number

        Returns:
            dict: API response JSON
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stream": False
        }

        try:
            response = requests.post(
                self.api_endpoint,
                headers=headers,
                json=payload,
                timeout=self.timeout
            )

            # Check for HTTP errors
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                raise Exception("Invalid API key (401 Unauthorized)")
            elif response.status_code == 429:
                # Rate limit hit
                retry_after = response.headers.get('Retry-After', '60')
                raise Exception(f"Rate limit exceeded (429). Retry after {retry_after}s")
            elif response.status_code == 503:
                raise Exception("Service unavailable (503). Model may be overloaded")
            else:
                raise Exception(f"HTTP {response.status_code}: {response.text}")

        except requests.exceptions.Timeout:
            raise Exception(f"Request timeout after {self.timeout}s")
        except requests.exceptions.ConnectionError:
            raise Exception("Network connection error")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    def _handle_api_error(self, error_message, retry_count):
        """
        Determine retry strategy based on error type.

        Args:
            error_message: Error message string
            retry_count: Current retry number

        Returns:
            int: Seconds to wait before retry (0 = don't retry)
        """
        # Rate limit error
        if "429" in error_message or "rate limit" in error_message.lower():
            # Parse retry-after if available
            try:
                if "Retry after" in error_message:
                    seconds = int(error_message.split("Retry after ")[1].split("s")[0])
                    return min(seconds, 120)  # Cap at 2 minutes
            except:
                pass
            return 60  # Default 60s wait for rate limits

        # Service unavailable
        if "503" in error_message:
            return 30  # Wait 30s for service recovery

        # Invalid API key - don't retry
        if "401" in error_message:
            return 0

        # Network/timeout errors - exponential backoff
        if "timeout" in error_message.lower() or "connection" in error_message.lower():
            return 2 ** retry_count  # 2s, 4s, 8s...

        # Generic error - short backoff
        return 5

    def test_connection(self):
        """
        Test API connectivity with a simple request.

        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            system_prompt = "You are a helpful assistant."
            user_prompt = "Say 'Hello' in one word."

            response = self.generate_tweet(system_prompt, user_prompt, max_retries=1)

            if response and len(response) > 0:
                print(f"[OK] LLM API connection successful!")
                print(f"   Model: {self.model}")
                print(f"   Test response: {response}")
                return True
            else:
                print("[ERROR] LLM API test failed: Empty response")
                return False

        except Exception as e:
            print(f"[ERROR] LLM API test failed: {e}")
            return False
