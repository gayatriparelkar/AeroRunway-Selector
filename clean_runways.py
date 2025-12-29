import pandas as pd

def clean_runway_data():
    try:
        # Load the dataset
        df = pd.read_csv("runways.csv")

        # Drop rows where runway headings are missing
        df = df.dropna(subset=["le_heading_degT", "he_heading_degT"])

        # Round runway headings to the nearest whole number and convert to int
        df["le_heading_degT"] = df["le_heading_degT"].round().astype(int)
        df["he_heading_degT"] = df["he_heading_degT"].round().astype(int)

        # Save cleaned data
        df.to_csv("runways_cleaned.csv", index=False)
        print("✅ Runway dataset cleaned and saved as runways_cleaned.csv")

    except FileNotFoundError:
        print("❌ Error: runways.csv not found in the project folder.")

if __name__ == "__main__":
    clean_runway_data()

