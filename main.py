from datetime import datetime
import json
import time
from colorama import Fore
import requests


class monsterkombat:
    BASE_URL = "https://api.monsterkombat.io/"
    HEADERS = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9,id;q=0.8",
        "authorization": "",
        "content-type": "application/json",
        "origin": "https://game.monsterkombat.io",
        "priority": "u=1, i",
        "referer": "https://game.monsterkombat.io/",
        "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    }

    def __init__(self):
        self.query_list = self.load_query("query.txt")
        self.token = None
        self.config = self.load_config()

    def banner(self) -> None:
        """Displays the banner for the bot."""
        self.log("🎉 Monster Kombat Free Bot", Fore.CYAN)
        self.log("🚀 Created by LIVEXORDS", Fore.CYAN)
        self.log("📢 Channel: t.me/livexordsscript\n", Fore.CYAN)

    def log(self, message, color=Fore.RESET):
        safe_message = message.encode("utf-8", "backslashreplace").decode("utf-8")
        print(
            Fore.LIGHTBLACK_EX
            + datetime.now().strftime("[%Y:%m:%d ~ %H:%M:%S] |")
            + " "
            + color
            + safe_message
            + Fore.RESET
        )

    def load_config(self) -> dict:
        """
        Loads configuration from config.json.

        Returns:
            dict: Configuration data or an empty dictionary if an error occurs.
        """
        try:
            with open("config.json", "r") as config_file:
                config = json.load(config_file)
                self.log("✅ Configuration loaded successfully.", Fore.GREEN)
                return config
        except FileNotFoundError:
            self.log("❌ File not found: config.json", Fore.RED)
            return {}
        except json.JSONDecodeError:
            self.log(
                "❌ Failed to parse config.json. Please check the file format.",
                Fore.RED,
            )
            return {}

    def load_query(self, path_file: str = "query.txt") -> list:
        """
        Loads a list of queries from the specified file.

        Args:
            path_file (str): The path to the query file. Defaults to "query.txt".

        Returns:
            list: A list of queries or an empty list if an error occurs.
        """
        self.banner()

        try:
            with open(path_file, "r") as file:
                queries = [line.strip() for line in file if line.strip()]

            if not queries:
                self.log(f"⚠️ Warning: {path_file} is empty.", Fore.YELLOW)

            self.log(f"✅ Loaded {len(queries)} queries from {path_file}.", Fore.GREEN)
            return queries

        except FileNotFoundError:
            self.log(f"❌ File not found: {path_file}", Fore.RED)
            return []
        except Exception as e:
            self.log(f"❌ Unexpected error loading queries: {e}", Fore.RED)
            return []

    def login(self, index: int) -> None:
        # Validasi index
        if index >= len(self.query_list):
            self.log("❌ Invalid login index. Please check again.", Fore.RED)
            return

        # Ambil token dari query_list dan pisahkan berdasarkan tanda '|'
        token = self.query_list[index]
        parts = token.split("|")
        if len(parts) < 3:
            self.log(
                "❌ Token format is incorrect. Expected format: signature|address|timestamp",
                Fore.RED,
            )
            return

        signature = parts[0]
        address = parts[1]
        timestamp = parts[2]

        # Buat payload untuk API sign-in
        payload = {
            "message": f"Login to the app. Connect time: {timestamp}",
            "signature": signature,
            "address": address,
            "refCode": "Y7zsu4qH",
        }

        sign_in_url = f"{self.BASE_URL}auth/sign-in"
        try:
            self.log("🔒 Attempting to sign in...", Fore.GREEN)
            sign_in_response = requests.post(
                sign_in_url, headers=self.HEADERS, json=payload
            )
            sign_in_response.raise_for_status()
            sign_in_data = sign_in_response.json()

            if sign_in_response.status_code in [200, 201]:
                # Simpan accessToken yang didapat dari API pertama
                self.token = sign_in_data["accessToken"]
                self.log("✅ Sign in successful!", Fore.GREEN)
            else:
                message = sign_in_data.get("message", "Unknown error")
                self.log(f"❌ Sign in failed: {message}", Fore.RED)
                self.log(f"📄 Response content: {sign_in_response.text}", Fore.RED)
                return

            # Panggil API kedua untuk mendapatkan info akun menggunakan token yang sudah didapat
            user_info_url = f"{self.BASE_URL}users/me"
            # Header authorization diisi dengan format Bearer self.token
            headers = {**self.HEADERS, "Authorization": f"Bearer {self.token}"}
            self.log("📡 Fetching user account info...", Fore.CYAN)
            user_info_response = requests.get(user_info_url, headers=headers)
            user_info_response.raise_for_status()
            user_info_data = user_info_response.json()

            if user_info_data:
                self.log("✅ Account info fetched successfully!", Fore.GREEN)
                # Tampilkan informasi penting agar user lebih mudah mengetahui akunnya
                self.log(
                    f"👤 Username: {user_info_data.get('username', 'Unknown')}",
                    Fore.CYAN,
                )
                self.log(
                    f"🆔 User ID: {user_info_data.get('_id', 'Unknown')}", Fore.CYAN
                )
                self.log(
                    f"📍 Address: {user_info_data.get('address', 'Unknown')}", Fore.CYAN
                )
                self.log(
                    f"⭐ Level: {user_info_data.get('level', 'Unknown')}", Fore.CYAN
                )
                self.log(
                    f"🏷 Referral Code: {user_info_data.get('referralCode', 'Unknown')}",
                    Fore.CYAN,
                )
                self.log(
                    f"💰 Token Balance: {user_info_data.get('token_balance', 'Unknown')}",
                    Fore.CYAN,
                )
                self.log(
                    f"💎 Gem Balance: {user_info_data.get('gem_balance', 'Unknown')}",
                    Fore.CYAN,
                )
                self.log(
                    f"⚡ Power: {user_info_data.get('power', 'Unknown')}", Fore.CYAN
                )
            else:
                self.log("❌ Failed to fetch account info: Empty response", Fore.RED)

        except requests.exceptions.RequestException as e:
            self.log(f"❌ Request failed: {e}", Fore.RED)
            if "sign_in_response" in locals():
                self.log(f"📄 Response content: {sign_in_response.text}", Fore.RED)
            if "user_info_response" in locals():
                self.log(f"📄 Response content: {user_info_response.text}", Fore.RED)
        except ValueError as e:
            self.log(f"❌ Data error (JSON decode issue): {e}", Fore.RED)
            if "sign_in_response" in locals():
                self.log(f"📄 Response content: {sign_in_response.text}", Fore.RED)
            if "user_info_response" in locals():
                self.log(f"📄 Response content: {user_info_response.text}", Fore.RED)
        except KeyError as e:
            self.log(f"❌ Key error: {e}", Fore.RED)
            if "sign_in_response" in locals():
                self.log(f"📄 Response content: {sign_in_response.text}", Fore.RED)
            if "user_info_response" in locals():
                self.log(f"📄 Response content: {user_info_response.text}", Fore.RED)
        except Exception as e:
            self.log(f"❌ Unexpected error: {e}", Fore.RED)
            if "sign_in_response" in locals():
                self.log(f"📄 Response content: {sign_in_response.text}", Fore.RED)
            if "user_info_response" in locals():
                self.log(f"📄 Response content: {user_info_response.text}", Fore.RED)

    def task(self) -> None:
        # Gunakan headers dengan Authorization sesuai fungsi login
        headers = {**self.HEADERS, "Authorization": f"Bearer {self.token}"}

        self.log("📡 Starting mission tasks...", Fore.CYAN)
        # Daftar tipe mission yang akan di-fetch
        task_types = ["DAILY_TASK", "BASIC_TASK", "PARTNER_TASK"]
        all_tasks = []

        # Ambil tasks dari masing-masing endpoint
        for t in task_types:
            url = f"{self.BASE_URL}mission/client?type={t}"
            try:
                self.log(f"📡 Fetching {t} tasks...", Fore.CYAN)
                response = requests.get(url, headers=headers)
                if response.status_code != 200:
                    self.log(
                        f"❌ Request failed with status code {response.status_code} for {t} tasks.",
                        Fore.RED,
                    )
                    continue
                data = response.json()
                tasks = data.get("missionTasks", [])
                self.log(f"🔍 Found {len(tasks)} {t} tasks.", Fore.BLUE)
                all_tasks.extend(tasks)
            except Exception as e:
                self.log(f"❌ Request error while fetching {t} tasks: {e}", Fore.RED)

        if not all_tasks:
            self.log("ℹ️ No mission tasks found.", Fore.YELLOW)
            return

        # Proses setiap mission task yang didapat
        for task_item in all_tasks:
            mission_code = task_item.get("mission_code")
            mission_name = task_item.get("mission_name")
            is_claim = task_item.get("is_claim", False)
            current_collect = task_item.get("current_collect", 0)
            mission_target = task_item.get("mission_target", 0)

            self.log(
                f"🚀 Processing Mission: {mission_code} - {mission_name}", Fore.CYAN
            )
            if is_claim:
                self.log(f"ℹ️ Mission {mission_code} is already claimed.", Fore.YELLOW)
                continue

            # 1. Update Progress Task (PATCH)
            update_url = f"{self.BASE_URL}mission/update-progress/{mission_code}"
            try:
                update_response = requests.patch(update_url, headers=headers)
                update_response.raise_for_status()
                update_result = update_response.json()
                if update_result.get("status") == 200:
                    self.log(
                        f"👍 Mission progress updated for {mission_code}.", Fore.GREEN
                    )
                else:
                    self.log(
                        f"❌ Update progress failed for Mission {mission_code}: {update_result.get('message')}",
                        Fore.RED,
                    )
                    continue
            except Exception as e:
                self.log(
                    f"❌ Request error during update progress for Mission {mission_code}: {e}",
                    Fore.RED,
                )
                continue

            # 2. Claim Mission Reward (POST, tanpa payload)
            claim_url = f"{self.BASE_URL}users/claim-mission-reward/{mission_code}"
            try:
                claim_response = requests.post(claim_url, headers=headers)
                claim_response.raise_for_status()
                claim_result = claim_response.json()
                if claim_result.get("success"):
                    self.log(
                        f"🏆 Mission Reward Claimed for {mission_code}: {claim_result.get('message')}",
                        Fore.GREEN,
                    )
                else:
                    self.log(
                        f"❌ Claim mission reward failed for {mission_code}: {claim_result.get('message')}",
                        Fore.RED,
                    )
            except Exception as e:
                self.log(
                    f"❌ Request error during claim mission reward for Mission {mission_code}: {e}",
                    Fore.RED,
                )
                continue

            self.log(
                "⏳ Waiting 2 seconds before processing the next mission...", Fore.BLUE
            )
            time.sleep(2)

    def fight(self) -> None:
        headers = {**self.HEADERS, "Authorization": f"Bearer {self.token}"}
        self.log("📡 Starting battle loop...", Fore.CYAN)

        # Function to fetch monsters data
        def fetch_monsters():
            monsters_url = f"{self.BASE_URL}battles/monsters"
            try:
                resp = requests.get(monsters_url, headers=headers)
                resp.raise_for_status()
                return resp.json()
            except Exception as e:
                self.log(f"❌ Error fetching monsters: {e}", Fore.RED)
                return None

        # Function to fetch pets data
        def fetch_pets():
            pets_url = f"{self.BASE_URL}pokemons/my-pets?sortField=tier&sortDirection=desc&keyword="
            try:
                resp = requests.get(pets_url, headers=headers)
                resp.raise_for_status()
                return resp.json()
            except Exception as e:
                self.log(f"❌ Error fetching pets: {e}", Fore.RED)
                return None

        while True:
            monsters_data = fetch_monsters()
            if not monsters_data:
                break

            # Get the monsters list and the refresh count
            monster_obj = monsters_data.get("monster", {})
            monsters_list = monster_obj.get("monsters", [])
            refresh_remaining = monsters_data.get("refresh_monster_remaining", 0)

            # Filter monsters with win_rate > 50%
            eligible_monsters = [m for m in monsters_list if m.get("win_rate", 0) > 50]

            # If no eligible monsters, try upgrading a pet
            if not eligible_monsters:
                self.log(
                    "ℹ️ No monsters with win rate > 50% found. Attempting to upgrade pet...",
                    Fore.YELLOW,
                )
                pets_data = fetch_pets()
                if not pets_data:
                    break
                pet_items = pets_data.get("pokemons", {}).get("items", [])
                if not pet_items:
                    self.log("ℹ️ No pets available to upgrade.", Fore.YELLOW)
                    break

                # Select the best pet based on power
                best_pet = max(pet_items, key=lambda pet: pet.get("power", 0))
                pet_id = best_pet.get("_id")
                current_level = best_pet.get("level", 0)
                self.log(
                    f"👾 Best pet: {best_pet.get('name')} (Power: {best_pet.get('power')}, Level: {current_level})",
                    Fore.CYAN,
                )

                # Attempt to upgrade the pet via the level-up API
                upgrade_url = f"{self.BASE_URL}pokemons/{pet_id}/level-up"
                try:
                    upgrade_resp = requests.post(upgrade_url, headers=headers)
                    upgrade_resp.raise_for_status()
                    upgrade_result = upgrade_resp.json()
                    new_level = upgrade_result.get("level")
                    if new_level and new_level > current_level:
                        self.log(
                            f"👍 Pet upgraded successfully to level {new_level}.",
                            Fore.GREEN,
                        )
                    else:
                        self.log(
                            "❌ Pet upgrade did not increase level. Attempting to refresh monsters...",
                            Fore.YELLOW,
                        )
                        # If upgrade fails to improve level, refresh monsters
                        refresh_url = f"{self.BASE_URL}battles/monsters/refresh"
                        try:
                            refresh_resp = requests.post(refresh_url, headers=headers)
                            refresh_resp.raise_for_status()
                            self.log("🔄 Monsters refreshed.", Fore.GREEN)
                        except Exception as e:
                            self.log(f"❌ Failed to refresh monsters: {e}", Fore.RED)
                            break
                except Exception as e:
                    self.log(f"❌ Error during pet upgrade: {e}", Fore.RED)
                    self.log("ℹ️ Attempting to refresh monsters...", Fore.YELLOW)
                    refresh_url = f"{self.BASE_URL}battles/monsters/refresh"
                    try:
                        refresh_resp = requests.post(refresh_url, headers=headers)
                        refresh_resp.raise_for_status()
                        self.log("🔄 Monsters refreshed.", Fore.GREEN)
                    except Exception as e:
                        self.log(f"❌ Failed to refresh monsters: {e}", Fore.RED)
                        break

                # After upgrade/refresh, fetch monsters again
                time.sleep(2)
                monsters_data = fetch_monsters()
                if not monsters_data:
                    break
                monsters_list = monsters_data.get("monster", {}).get("monsters", [])
                eligible_monsters = [
                    m for m in monsters_list if m.get("win_rate", 0) > 50
                ]
                # If still no eligible monsters, exit the loop
                if not eligible_monsters:
                    self.log(
                        "ℹ️ No eligible monsters after upgrade/refresh. Exiting battle loop.",
                        Fore.YELLOW,
                    )
                    break

            # If eligible monsters exist, select the one with the highest win_rate
            selected_monster = max(
                eligible_monsters, key=lambda m: m.get("win_rate", 0)
            )
            monster_win_rate = selected_monster.get("win_rate")
            self.log(
                f"🎯 Selected Monster: {selected_monster.get('monster')} with win rate {monster_win_rate}%",
                Fore.CYAN,
            )

            # Fetch pet data again to choose the best available pet for battle
            pets_data = fetch_pets()
            if not pets_data:
                break
            pet_items = pets_data.get("pokemons", {}).get("items", [])
            if not pet_items:
                self.log("ℹ️ No pets available for battle.", Fore.YELLOW)
                break

            # Filter pets that have battles_remaining > 0
            available_pets = [
                pet for pet in pet_items if pet.get("battles_remaining", 0) > 0
            ]
            if not available_pets:
                self.log(
                    "ℹ️ No pets with remaining battles. Exiting fight.", Fore.YELLOW
                )
                return

            # Select the best pet based on power
            best_pet = max(available_pets, key=lambda pet: pet.get("power", 0))
            pet_id = best_pet.get("_id")
            self.log(
                f"👾 Selected Pokemon for fight: {best_pet.get('name')} (Power: {best_pet.get('power')}, Battles remaining: {best_pet.get('battles_remaining')})",
                Fore.CYAN,
            )

            # Execute the fight by calling the battles/fight API
            fight_url = f"{self.BASE_URL}battles/fight"
            fight_payload = {"monsterWinRate": monster_win_rate, "pokemonIds": [pet_id]}
            try:
                fight_resp = requests.post(
                    fight_url, headers=headers, json=fight_payload
                )
                fight_resp.raise_for_status()
                fight_result = fight_resp.json()
                self.log("⚔️ Fight executed successfully.", Fore.GREEN)
                details = fight_result.get("details", [])
                for detail in details:
                    is_win = detail.get("is_win")
                    earned_token = detail.get("earned_token")
                    earned_gem = detail.get("earned_gem")
                    self.log(
                        f"   -> Pokemon {detail.get('pokemon_id')} | Win: {is_win} | Earned Token: {earned_token} | Earned Gem: {earned_gem}",
                        Fore.GREEN,
                    )
            except Exception as e:
                self.log(f"❌ Error during fight: {e}", Fore.RED)
                break

            # After the fight, refresh the monster list to update data
            self.log("🔄 Refreshing monster list after fight...", Fore.CYAN)
            try:
                refresh_resp = requests.get(
                    f"{self.BASE_URL}battles/monsters", headers=headers
                )
                refresh_resp.raise_for_status()
                self.log("🔄 Monster list refreshed.", Fore.GREEN)
            except Exception as e:
                self.log(f"❌ Error refreshing monster list: {e}", Fore.RED)
                break

            self.log("⏳ Waiting 2 seconds before next battle...", Fore.BLUE)
            time.sleep(2)

    def load_proxies(self, filename="proxy.txt"):
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

        If a chosen proxy fails the connectivity test, it will try another proxy
        until a working one is found. If no proxies work or the list is empty, it
        will return a session with a direct connection.

        Args:
            proxies (list): A list of proxy addresses (e.g., "http://proxy_address:port").

        Returns:
            requests.Session: A session object configured with a working proxy,
                            or a direct connection if none are available.
        """
        # If no proxies are provided, use a direct connection.
        if not proxies:
            self.log("⚠️ No proxies available. Using direct connection.", Fore.YELLOW)
            self.proxy_session = requests.Session()
            return self.proxy_session

        # Copy the list so that we can modify it without affecting the original.
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
                self.log(
                    f"✅ Using Proxy: {proxy_url} | Your IP: {origin_ip}", Fore.GREEN
                )
                return self.proxy_session
            except requests.RequestException as e:
                self.log(f"❌ Proxy failed: {proxy_url} | Error: {e}", Fore.RED)
                # Remove the failed proxy and try again.
                available_proxies.remove(proxy_url)

        # If none of the proxies worked, use a direct connection.
        self.log("⚠️ All proxies failed. Using direct connection.", Fore.YELLOW)
        self.proxy_session = requests.Session()
        return self.proxy_session

    def override_requests(self):
        """Override requests functions globally when proxy is enabled."""
        if self.config.get("proxy", False):
            self.log("[CONFIG] 🛡️ Proxy: ✅ Enabled", Fore.YELLOW)
            proxies = self.load_proxies()
            self.set_proxy_session(proxies)

            # Override request methods
            requests.get = self.proxy_session.get
            requests.post = self.proxy_session.post
            requests.put = self.proxy_session.put
            requests.delete = self.proxy_session.delete
        else:
            self.log("[CONFIG] proxy: ❌ Disabled", Fore.RED)
            # Restore original functions if proxy is disabled
            requests.get = self._original_requests["get"]
            requests.post = self._original_requests["post"]
            requests.put = self._original_requests["put"]
            requests.delete = self._original_requests["delete"]


if __name__ == "__main__":
    monster = monsterkombat()
    index = 0
    max_index = len(monster.query_list)
    config = monster.load_config()
    if config.get("proxy", False):
        proxies = monster.load_proxies()

    monster.log(
        "🎉 [LIVEXORDS] === Welcome to Monster Kombat Automation === [LIVEXORDS]",
        Fore.YELLOW,
    )
    monster.log(f"📂 Loaded {max_index} accounts from query list.", Fore.YELLOW)

    while True:
        current_account = monster.query_list[index]
        display_account = (
            current_account[:10] + "..."
            if len(current_account) > 10
            else current_account
        )

        monster.log(
            f"👤 [ACCOUNT] Processing account {index + 1}/{max_index}: {display_account}",
            Fore.YELLOW,
        )

        if config.get("proxy", False):
            monster.override_requests()
        else:
            monster.log("[CONFIG] Proxy: ❌ Disabled", Fore.RED)

        monster.login(index)

        monster.log("🛠️ Starting task execution...")
        tasks = {
            "task": "Automatically solving tasks 🤖",
            "fight": "Auto Fight ⚔️ - Engage in epic battles with your best monsters and pets for awesome rewards! 🔥🏆",
        }

        for task_key, task_name in tasks.items():
            task_status = config.get(task_key, False)
            monster.log(
                f"[CONFIG] {task_name}: {'✅ Enabled' if task_status else '❌ Disabled'}",
                Fore.YELLOW if task_status else Fore.RED,
            )

            if task_status:
                monster.log(f"🔄 Executing {task_name}...")
                getattr(monster, task_key)()

        if index == max_index - 1:
            monster.log("🔁 All accounts processed. Restarting loop.")
            monster.log(
                f"⏳ Sleeping for {config.get('delay_loop', 30)} seconds before restarting."
            )
            time.sleep(config.get("delay_loop", 30))
            index = 0
        else:
            monster.log(
                f"➡️ Switching to the next account in {config.get('delay_account_switch', 10)} seconds."
            )
            time.sleep(config.get("delay_account_switch", 10))
            index += 1
