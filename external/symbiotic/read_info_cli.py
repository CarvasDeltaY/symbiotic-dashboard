import subprocess
import polars as pl
import re
from datetime import datetime

def run_cli_command(command) -> list[str]:
    """Runs a CLI command and returns the output as a list of lines."""
    print(f"Running command: {command}")  
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        if result.returncode == 0:
            output = result.stdout.strip().split("\n")
            print(f"Output:\n{output}\n")  
            return output
        else:
            print(f"Error running command: {command}\n{result.stderr}")
            return []
    except Exception as e:
        print(f"Exception while running command: {command}\n{e}")
        return []

def get_staking_data(command: str) -> pl.DataFrame:
    """Get the staking data from the CLI command."""

    avs_output = run_cli_command(command)
    avs_list = []
    for line in avs_output:
        if "Network:" in line:
            avs_address = line.split("Network: ")[1].strip().lower()
            avs_list.append(avs_address)

    if not avs_list:
        print("❌ No valid AVS (network) addresses found. Exiting...")
        exit()

    print(f"✅ Found {len(avs_list)} AVS addresses.")

    # Step 2: Fetch operators and stake per AVS
    stake_data = []

    for avs_address in avs_list:

        # Get Stake & Collateral for this AVS
        stakes_output = run_cli_command(f"python symb.py netstakes {avs_address}")

        current_operator = None
        collateral_asset_address = None
        collateral_asset_symbol = None
        stake_amount = None
        timestamp = datetime.now().replace(minute=0, second=0, microsecond=0)

        for line in stakes_output:
            if "Operator:" in line:
                current_operator = line.split(": ")[1].strip().lower()
            
            if "Collateral:" in line:
                collateral_asset_symbol = line.split("(")[-1].strip(")").lower()
                match = re.search(r"Collateral:\s+(0x[a-fA-F0-9]+)", line)
                if match:
                    collateral_asset_address = match.group(1).strip()

            if "Stake:" in line and "Total stake:" not in line:
                try:
                    stake_amount = float(line.split(": ")[1].strip().replace(",", ""))
                    if stake_amount > 0:
                        stake_data.append([avs_address, current_operator, collateral_asset_address, collateral_asset_symbol, stake_amount, timestamp])
                except ValueError:
                    print(f"❌ Error parsing stake amount: {line}")

    if not stake_data:
        print("⚠️ No non-zero stake data found. Saving empty CSV for reference.")
        return None
    else:
        df_staking_data = pl.DataFrame(stake_data, schema=["network_address", "node_operator_address", "collateral_asset_address", "collateral_asset_symbol", "amount_staked", "timestamp"])
        return df_staking_data