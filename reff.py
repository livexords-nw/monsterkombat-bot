import requests
import time
import json
import random
from datetime import datetime
from eth_account import Account
from eth_account.messages import encode_defunct
from urllib.parse import urlparse, parse_qs
from colorama import Fore, init

# Initialize colorama for colored output
init(autoreset=True)

class MonsterKombatReff:
    def __init__(self):
        # Store original requests functions in case proxy is disabled
        self._original_requests = {
            "get": requests.get,
            "post": requests.post,
            "put": requests.put,
            "delete": requests.delete,
        }
        self.banner()
        self.config = self.load_config()  # load configuration from config_ref.json
        self.proxy_session = None
        # Override requests if proxy is enabled in configuration
        if self.config.get("proxy", False):
            self.override_requests()
        # Load referral codes from query_reff.txt (each line is a URL)
        self.ref_codes = self.load_query("query_reff.txt")
        if not self.ref_codes:
            self.log("⚠️ No referral codes found! Please check query_reff.txt", Fore.RED)

    def banner(self) -> None:
        """Displays the banner for the bot."""
        self.log("🎉 Monster Kombat Free Bot", Fore.CYAN)
        self.log("🚀 Created by LIVEXORDS", Fore.CYAN)
        self.log("📢 Channel: t.me/livexordsscript\n", Fore.CYAN)

    def log(self, message, color=Fore.RESET):
        safe_message = message.encode("utf-8", "backslashreplace").decode("utf-8")
        print(
            Fore.LIGHTBLACK_EX
            + datetime.now().strftime("[%Y-%m-%d ~ %H:%M:%S] |")
            + " "
            + color
            + safe_message
            + Fore.RESET
        )

    def load_config(self) -> dict:
        """
        Loads configuration from config_ref.json.
        Returns:
            dict: Configuration data or an empty dictionary if an error occurs.
        """
        try:
            with open("config_reff.json", "r") as config_file:
                config = json.load(config_file)
                self.log("✅ Configuration loaded successfully.", Fore.GREEN)
                return config
        except FileNotFoundError:
            self.log("❌ File not found: config_reff.json", Fore.RED)
            return {}
        except json.JSONDecodeError:
            self.log("❌ Failed to parse config_reff.json . Please check the file format.", Fore.RED)
            return {}

    def load_query(self, path_file: str = "query_reff.txt") -> list:
        """
        Loads referral codes from the specified file.
        Each line is expected to be a URL with a 'ref' query parameter.
        Returns:
            list: A list of referral codes.
        """
        try:
            with open(path_file, "r") as file:
                lines = [line.strip() for line in file if line.strip()]
            ref_codes = []
            for url in lines:
                parsed = urlparse(url)
                query_params = parse_qs(parsed.query)
                ref = query_params.get("ref", [None])[0]
                if ref:
                    ref_codes.append(ref)
            if not ref_codes:
                self.log(f"⚠️ Warning: No referral codes extracted from {path_file}.", Fore.YELLOW)
            else:
                self.log(f"✅ Loaded {len(ref_codes)} referral codes from {path_file}.", Fore.GREEN)
            return ref_codes
        except FileNotFoundError:
            self.log(f"❌ File not found: {path_file}", Fore.RED)
            return []
        except Exception as e:
            self.log(f"❌ Unexpected error loading queries: {e}", Fore.RED)
            return []

    def load_proxies(self, filename="proxy.txt") -> list:
        """
        Reads proxies from a file and returns them as a list.
        Args:
            filename (str): The path to the proxy file.
        Returns:
            list: A list of proxy addresses.
        """
        try:
            with open(filename, "r", encoding="utf-8") as file:
                proxies = [line.strip() for line in file if line.strip()]
            if not proxies:
                raise ValueError("Proxy file is empty.")
            return proxies
        except Exception as e:
            self.log(f"❌ Failed to load proxies: {e}", Fore.RED)
            return []

    def set_proxy_session(self, proxies: list) -> requests.Session:
        """
        Creates a requests session with a working proxy from the given list.
        Args:
            proxies (list): A list of proxy addresses.
        Returns:
            requests.Session: A session configured with a working proxy, or a direct connection if none work.
        """
        if not proxies:
            self.log("⚠️ No proxies available. Using direct connection.", Fore.YELLOW)
            self.proxy_session = requests.Session()
            return self.proxy_session

        available_proxies = proxies.copy()
        while available_proxies:
            proxy_url = random.choice(available_proxies)
            self.proxy_session = requests.Session()
            self.proxy_session.proxies = {"http": proxy_url, "https": proxy_url}
            try:
                test_url = "https://httpbin.org/ip"
                response = self.proxy_session.get(test_url, timeout=5)
                response.raise_for_status()
                origin_ip = response.json().get("origin", "Unknown IP")
                self.log(f"✅ Using Proxy: {proxy_url} | Your IP: {origin_ip}", Fore.GREEN)
                return self.proxy_session
            except requests.RequestException as e:
                self.log(f"❌ Proxy failed: {proxy_url} | Error: {e}", Fore.RED)
                available_proxies.remove(proxy_url)
        self.log("⚠️ All proxies failed. Using direct connection.", Fore.YELLOW)
        self.proxy_session = requests.Session()
        return self.proxy_session

    def override_requests(self):
        """Override requests functions globally when proxy is enabled."""
        if self.config.get("proxy", False):
            self.log("[CONFIG] 🛡️ Proxy: Enabled", Fore.YELLOW)
            proxies = self.load_proxies()
            self.set_proxy_session(proxies)
            # Override request methods
            requests.get = self.proxy_session.get
            requests.post = self.proxy_session.post
            requests.put = self.proxy_session.put
            requests.delete = self.proxy_session.delete
        else:
            self.log("[CONFIG] Proxy: Disabled", Fore.RED)
            # Restore original functions if proxy is disabled
            requests.get = self._original_requests["get"]
            requests.post = self._original_requests["post"]
            requests.put = self._original_requests["put"]
            requests.delete = self._original_requests["delete"]

    def generate_payload(self, ref_code: str) -> dict:
        """
        Generates a new wallet, creates a login message with timestamp, signs it, and returns the payload.
        Args:
            ref_code (str): Referral code to include in the payload.
        Returns:
            dict: Payload containing message, signature, address, and refCode.
        """
        account = Account.create()
        current_time = int(time.time() * 1000)
        message = f"Login to the app. Connect time: {current_time}"
        message_encoded = encode_defunct(text=message)
        signed_message = Account.sign_message(message_encoded, private_key=account.key)
        signature_hex = signed_message.signature.hex()
        if not signature_hex.startswith("0x"):
            signature_hex = "0x" + signature_hex
        payload = {
            "message": message,
            "signature": signature_hex,
            "address": account.address,
            "refCode": ref_code
        }
        return payload

    def send_sign_in_request(self, payload: dict) -> requests.Response:
        """
        Sends a POST request to the sign-in API.
        Returns:
            requests.Response: The response from the API if status code 200 or 201, else None.
        """
        url = "https://api.monsterkombat.io/auth/sign-in"
        # List of fake user agents
        fake_user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/109.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"
        ]
        user_agent = random.choice(fake_user_agents)
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json",
            "Origin": "https://game.monsterkombat.io",
            "Referer": "https://game.monsterkombat.io/",
            "Sec-CH-UA": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            "Sec-CH-UA-Mobile": "?0",
            "Sec-CH-UA-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "Priority": "u=1, i",
            "User-Agent": user_agent,
        }
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            if response.status_code in (200, 201):
                self.log("✅ Sign in successful!", Fore.GREEN)
                return response
            else:
                self.log(f"❌ Sign in failed. Status Code: {response.status_code}", Fore.RED)
                self.log(f"Response: {response.text}", Fore.RED)
        except Exception as e:
            self.log(f"❌ Error during sign in request: {e}", Fore.RED)
        return None

    def append_result(self, payload: dict):
        """
        Appends the sign-in result to result_reff.txt in the format:
        signature|address|timestamp
        Timestamp is extracted from the payload's message.
        """
        try:
            timestamp = payload["message"].split("Connect time:")[-1].strip()
        except Exception:
            timestamp = "unknown"
        result_line = f"{payload['signature']}|{payload['address']}|{timestamp}\n"
        try:
            with open("result_reff.txt", "a") as file:
                file.write(result_line)
            self.log("✅ Sign in result saved to result_reff.txt", Fore.GREEN)
        except Exception as e:
            self.log(f"❌ Failed to save sign in result: {e}", Fore.RED)

    def run(self):
        """
        Runs the bot: For each referral code loaded (in order), generates sign-in attempts
        as many times as specified in countGenerate.
        """
        count_generate = self.config.get("countGenerate", 1)
        delay_per_generate = self.config.get("delayperGenerate", 3)
        
        if not self.ref_codes:
            self.log("❌ No referral codes to process. Exiting...", Fore.RED)
            return
        
        self.log(f"🚀 Starting generation process: {count_generate} iterations per referral code.", Fore.CYAN)
        for ref_code in self.ref_codes:
            self.log(f"🔄 Processing referral code: {ref_code}", Fore.MAGENTA)
            for i in range(count_generate):
                self.log(f"    🔄 Iteration {i+1}/{count_generate} for referral code: {ref_code}", Fore.MAGENTA)
                payload = self.generate_payload(ref_code)
                self.log("    📨 Generated Payload:", Fore.CYAN)
                self.log(json.dumps(payload, indent=4), Fore.LIGHTBLUE_EX)
                response = self.send_sign_in_request(payload)
                if response and response.status_code in (200, 201):
                    self.append_result(payload)
                    resp_json = response.json()
                    self.log(f"    🔑 Access Token: {resp_json.get('accessToken')}", Fore.GREEN)
                    self.log(f"    🔑 Refresh Token: {resp_json.get('refreshToken')}", Fore.GREEN)
                else:
                    self.log("    ❌ Sign in attempt failed.", Fore.RED)
                self.log(f"    ⏳ Waiting {delay_per_generate} seconds before next iteration...\n", Fore.YELLOW)
                time.sleep(delay_per_generate)

if __name__ == "__main__":
    bot = MonsterKombatReff()
    bot.run()
