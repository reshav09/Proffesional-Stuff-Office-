import os
import pandas as pd

server_dir = "/home/reshavsharma/Downloads/code/"  # Update this with the actual path
server_stats = []

for server_name in os.listdir(server_dir):
    server_path = os.path.join(server_dir, server_name)
    
    if not os.path.isdir(server_path):
        continue

    stats = {"Server Name": server_name}

    # 1. CPU Load
    cpu_file = os.path.join(server_path, "CPU_Load.csv")
    if os.path.exists(cpu_file):
        df_cpu = pd.read_csv(cpu_file)
        if 'Total(RAW)' in df_cpu.columns:
            stats["CPU Min (%)"] = round(df_cpu['Total(RAW)'].min(), 2)
            stats["CPU Avg (%)"] = round(df_cpu['Total(RAW)'].mean(), 2)
            stats["CPU Max (%)"] = round(df_cpu['Total(RAW)'].max(), 2)

        else:
            print(f"Warning: 'Total(RAW)' not found in {cpu_file}")
    else:
        print(f"Warning: Missing CPU file for {server_name}")

    # 2. Memory Utilization
    memory_file = os.path.join(server_path, "Memory.csv")
    if os.path.exists(memory_file):
        df_mem = pd.read_csv(memory_file)
        if 'Percent Available Memory(RAW)' in df_mem.columns:
            df_mem['Memory Utilized (%)'] = 100 - df_mem['Percent Available Memory(RAW)']
            stats["Memory Min (%)"] = round(df_mem['Memory Utilized (%)'].min(), 2)
            stats["Memory Avg (%)"] = round(df_mem['Memory Utilized (%)'].mean(), 2)
            stats["Memory Max (%)"] = round(df_mem['Memory Utilized (%)'].max(), 2)

        else:
            print(f"Warning: 'Percent Available Memory(RAW)' not found in {memory_file}")
    else:
        print(f"Warning: Missing Memory file for {server_name}")

    # 3. Storage
    storage_file = os.path.join(server_path, "Storage.csv")
    if os.path.exists(storage_file):
        df_storage = pd.read_csv(storage_file)
        if all(col in df_storage.columns for col in ['Free Bytes(RAW)', 'Total(RAW)']):
            last_record = df_storage.iloc[-2]
            total_gb = last_record['Total(RAW)'] / (1024**3)
            free_gb = last_record['Free Bytes(RAW)'] / (1024**3)
            used_gb = total_gb - free_gb
            stats["Storage Total (GB)"] = round(total_gb, 2)
            stats["Storage Used (GB)"] = round(used_gb, 2)
            stats["Storage Avail (GB)"] = round(free_gb, 2)
        else:
            print(f"Warning: Required storage columns not found in {storage_file}")
    else:
        print(f"Warning: Missing Storage file for {server_name}")

    # 4. Uptime
    uptime_file = os.path.join(server_path, "uptime.csv")
    if os.path.exists(uptime_file):
        df_uptime = pd.read_csv(uptime_file)
        if 'System Uptime(RAW)' in df_uptime.columns:
            last_uptime_seconds = df_uptime['System Uptime(RAW)'].iloc[-2]
            uptime_days = last_uptime_seconds / (24 * 3600)
            stats["Uptime (Days)"] = round(uptime_days, 0)
        else:
            print(f"Warning: 'System Uptime(RAW)' not found in {uptime_file}")
    else:
        print(f"Warning: Missing Uptime file for {server_name}")

    server_stats.append(stats)

# Create and save final DataFrame
stats_df = pd.DataFrame(server_stats)
output_file = "Server_full_stats.csv"
stats_df.to_csv(output_file, index=False)
print(f"All server stats have been saved to {output_file}")
