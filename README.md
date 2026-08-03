# lucide-roblox-direct

lucide-roblox-direct is a script that directly gives you a standalone file that contains all the Lucide icons in Roblox. (Found in source.lua)

## Usage

Example module found [here](https://github.com/notpoiu/cobalt/blob/main/Src/Utils/UI/Icons.luau)

## Building

To build lucide-roblox-direct, you need to have Python 3 installed on your system. You can download it from [python.org](https://www.python.org/downloads/). Once you have Python installed, you can run the following command in your terminal:

```bash
pip install -r requirements.txt
```

This will install all the required dependencies for the script.

Additionally, you will need install [rokit](https://github.com/rojo-rbx/rokit).
then open Powershell or the command-line shell of your liking and [cd to this repository](https://www.quora.com/What-does-it-mean-to-CD-into-a-directory-and-how-can-I-do-that-Can-someone-explain-it-in-a-laymans-term)

Run `rokit install` and wait for it to install all the dependencies

Before running the script, you need to setup your environement variables. Create a file named `.env` in the root directory of the project and add the following lines:

```
ROBLOX_API_KEY=your_api_key_here
ROBLOX_USER_ID=your_user_id_here
```

Replace `your_api_key_here` with your actual Roblox API key and `your_user_id_here` with your Roblox user ID.
(ROBLOX_API_KEY should have read & write permissions to the assets in roblox open cloud permissions and manage permissions for the legacy-assets)

and finally, run the following command to build the script:

```bash
sh scripts/build.sh
```
