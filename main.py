import time
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import pandas as pd

import speedtest

# Duration settings
INTERVAL = 10  # seconds
DURATION = 3600  # 1 hour in seconds

# Data storage
results = []

print(f"Starting speed test every {INTERVAL} seconds for 1 hour...")

try:
    st = speedtest.Speedtest()
    st.get_best_server()
    
    # Record start time
    start_time = datetime.now()
    end_time = start_time + timedelta(seconds=DURATION)
    test_count = 0
    
    while datetime.now() < end_time:
        timestamp = datetime.now()
        test_count += 1

        print(f"Test {test_count} at {timestamp.strftime('%H:%M:%S')}...")

        download_speed = st.download() / 1_000_000  # Convert to Mbps
        upload_speed = st.upload() / 1_000_000  # Convert to Mbps

        results.append(
            {
                "timestamp": timestamp,
                "download_Mbps": round(download_speed, 2),
                "upload_Mbps": round(upload_speed, 2),
            }
        )

        print(
            f"  Download: {download_speed:.2f} Mbps | Upload: {upload_speed:.2f} Mbps"
        )

        # Sleep until next interval
        time.sleep(INTERVAL)

except KeyboardInterrupt:
    print("Testing interrupted by user.")

# Convert results to DataFrame
df = pd.DataFrame(results)

# Generate timestamp for filenames
timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")

# Save to CSV with timestamp
csv_filename = f"internet_speed_log_{timestamp_str}.csv"
df.to_csv(csv_filename, index=False)
print(f"Data saved to '{csv_filename}'.")

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(
    df["timestamp"],
    df["download_Mbps"],
    label="Download Speed (Mbps)",
    color="blue",
    marker="o",
)
plt.plot(
    df["timestamp"],
    df["upload_Mbps"],
    label="Upload Speed (Mbps)",
    color="green",
    marker="o",
)
plt.xlabel("Time")
plt.ylabel("Speed (Mbps)")
plt.title("Internet Speed Over 1 Hour")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.grid(True)

# Save plot with timestamp
plot_filename = f"internet_speed_plot_{timestamp_str}.png"
plt.savefig(plot_filename)
print(f"Plot saved as '{plot_filename}'.")
