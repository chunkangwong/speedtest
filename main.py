import speedtest
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import time

# Duration settings
INTERVAL = 10  # seconds
DURATION = 3600  # 1 hour in seconds
NUM_TESTS = DURATION // INTERVAL

# Data storage
results = []

print(f"Starting speed test every {INTERVAL} seconds for 1 hour...")

try:
    st = speedtest.Speedtest()
    st.get_best_server()
    for i in range(NUM_TESTS):
        timestamp = datetime.now()

        print(f"Test {i+1}/{NUM_TESTS} at {timestamp.strftime('%H:%M:%S')}...")

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

# Save to CSV
df.to_csv("internet_speed_log.csv", index=False)
print("Data saved to 'internet_speed_log.csv'.")

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
plt.savefig("internet_speed_plot.png")
plt.show()
print("Plot saved as 'internet_speed_plot.png'.")
