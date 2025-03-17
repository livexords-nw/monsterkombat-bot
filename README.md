---

<h1 align="center">Monster Kombat Bot</h1>

<p align="center">Automate tasks in Monster Kombat to enhance your efficiency and maximize your results!</p>

---

## 🚀 **About the Bot**

The Monster Kombat Bot is designed to automate various tasks in **Monster Kombat**, including:

- **Auto Task:** Automatically solve tasks 🤖
- **Auto Fight:** Engage in epic battles automatically! ⚔️🔥🏆  
  _(This feature also integrates auto-upgrade pet functionality for improved performance.)_

With this bot, you can save time and maximize your outcomes without manual intervention.

---

## 🌟 Version v1.1.0

### Updates

- **Extension Update:**  
  Added a Violent Monkey extension for capturing the query directly from the website.  
  _Note:_ This extension works only within the Violent Monkey environment.

### Future Updates

1. **Auto Buy Egg (Shop):**  
   An automatic egg purchasing system will be added to the shop for a smoother gameplay experience.
2. **Fight System Optimization:**  
   Further optimizations will be made to the fight system to improve battle performance.
3. **Combine System:**  
   A combine system will be introduced, allowing you to merge items or monsters for enhanced abilities.

---

### **Features in This Version:**

- **Auto Task:** Automatically solve tasks 🤖
- **Auto Fight:** Automatically engage in battles (includes auto-upgrade pet) ⚔️🔥🏆
- **Multi-Account Support:** Manage multiple accounts simultaneously.
- **Proxy Support:** Dynamically assign proxies to different accounts.
- **Delay Loop and Account Switching:** Set custom delays for looping tasks and switching between accounts.
- **Violent Monkey Extension:**  
  Capture the query directly from the website and save it as `signature|address|timestamp`.  
  _Note:_ This extension works only with Violent Monkey.  
  **Zip file:** `monester_kombat_extension_query.zip`

---

## ⚙️ **Configuration in `config.json`**

Below is the configuration table for the Monster Kombat Bot:

| **Function**           | **Description**                             | **Default** |
| ---------------------- | ------------------------------------------- | ----------- |
| `task`                 | Automatically solve tasks                   | `true`      |
| `fight`                | Auto Fight (includes auto-upgrade pet)      | `true`      |
| `delay_account_switch` | Delay between account switches (in seconds) | `10`        |
| `delay_loop`           | Delay before the next loop (in seconds)     | `3000`      |

And here is a sample `config.json`:

```json
{
  "fight": true,
  "task": true,
  "delay_account_switch": 10,
  "delay_loop": 3000
}
```

---

## 📖 **Installation Steps**

1. **Clone the Repository**  
   Copy the project to your local machine:

   ```bash
   git clone https://github.com/livexords-nw/monsterkombat-bot.git
   ```

2. **Navigate to the Project Folder**  
   Move to the project directory:

   ```bash
   cd monsterkombat-bot
   ```

3. **Install Dependencies**  
   Install the required libraries:

   ```bash
   pip install -r requirements.txt
   ```

---

## 🔍 **Configure Query**

1. **Create a Query File:**  
   Create a file named `query.txt` and add your Monster Kombat query data.  
   **Query format:**

   ```
   signature|address|timestamp
   ```

2. **How to Obtain Your Query:**  
   You can find this query by inspecting the website. Open your browser's Developer Tools, navigate to the **Network** tab, log in, and look for an API call named **sign-in**. Then, check its payload to copy the required query information.

   **Note:**  
   To make this process easier, please use my extension provided in the zip file **`monster_kombat_extension_query.zip`**. This extension will automatically capture the query from the website.

---

## 💻 **Tutorial: Install the Extension**

1. **Download the Extension:**  
   Download the zip file `monster_kombat_extension_query.zip` from this repository.  
   ![Download Image](download_placeholder.jpg)

2. **Install Violent Monkey Extension:**  
   Install the Violent Monkey extension in your browser using [this link](https://violentmonkey.github.io/get-it/).

3. **Import the Zip File:**  
   Open Violent Monkey, go to **Settings** → **Import from Zip**, and select the downloaded zip file.  
   ![Import Zip Image](import_placeholder.jpg)

4. **Activate the Extension on Monster Kombat Website:**  
   Open the Monster Kombat website. If you are still logged in, please log out and log in again to ensure the extension is active.  
   Make sure the extension is working correctly as shown below:  
   ![Extension Active Image](extension_active_placeholder.jpg)

5. **Capture and Copy the Query:**  
   Once logged in, click **Format & Copy** on the extension.  
   Then, paste the copied result into your `query.txt` file.

---

## ⚙️ **Tutorial: Running the Auto Reff Script**

1. **Install Dependencies:**  
   Ensure you have installed all required libraries:

   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up Referral Links:**  
   Create a file named `query_reff.txt` and add your referral links. You can include multiple links.

3. **Configure the Auto Reff Settings:**  
   Create or update the `config_reff.json` file with the following parameters:

   ```json
   {
     "proxy": true,
     "countGenerate": 20,
     "delayperGenerate": 3
   }
   ```

   - **proxy:** Set to `true` to use proxy. Ensure that the `proxy.txt` file is available if enabled.
   - **countGenerate:** Number of accounts to generate per referral link.
   - **delayperGenerate:** Delay (in seconds) after each account generation.

4. **Run the Auto Reff Script:**  
   Execute the script with the following command:

   ```bash
   python reff.py
   ```

5. **Optional - Run Referral Accounts in Main Script:**  
   If you wish to use the generated referral accounts in your main script, enable the feature `run_reff` by setting it to `true` in your configuration. This will trigger the execution of referral accounts automatically.

---

## 📥 **How to Register**

Start using Monster Kombat Bot by registering through the following link:

<div align="center">
  <a href="https://game.monsterkombat.io/?ref=Y7zsu4qH" target="_blank">
    <img src="https://img.shields.io/static/v1?message=Monster%20Kombat&logo=telegram&label=&color=2CA5E0&logoColor=white&labelColor=&style=for-the-badge" height="25" alt="register" />
  </a>
</div>

---

## 🛠️ **Contributing**

This project is developed by **Livexords**. If you have suggestions, questions, or would like to contribute, feel free to contact us:

<div align="center">
  <a href="https://t.me/livexordsscript" target="_blank">
    <img src="https://img.shields.io/static/v1?message=Livexords&logo=telegram&label=&color=2CA5E0&logoColor=white&labelColor=&style=for-the-badge" height="25" alt="telegram" />
  </a>
</div>
