import csv
import os
from sdr_generator import SDRGenerator


INPUT_CSV = "prospects.csv"
OUTPUT_CSV = "generated_emails.csv"

# Required CSV Headers
REQUIRED_COLUMNS = [
    "caseStudy", "ICP", "companyName", "activity", "companyWebsite",
    "senderCompany", "ourWebsite", "meetingLink",
    "senderName", "senderTitle",
    "firstName", "lastName", "linkedinURL"
]
def main():
def load_prospects(file_path):
    prospects = []
    with open(file_path, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not all(col in row for col in REQUIRED_COLUMNS):
                raise ValueError("CSV missing required columns.")
            prospects.append(row)
    return prospects

def save_results(results):
    with open(OUTPUT_CSV, "w", newline='', encoding="utf-8") as f:
        fieldnames = REQUIRED_COLUMNS + ["generated_email"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            writer.writerow(r)

def main():
    generator = SDRGenerator()
    prospects = load_prospects(INPUT_CSV)
    results = []

    for prospect in prospects:
        print(f"Generating email for {prospect['firstName']} {prospect['lastName']} ({prospect['companyName']})...")
        email = generator.generate_email(prospect)
        prospect["generated_email"] = email
        results.append(prospect)

    save_results(results)
    print(f"✅ Batch generation complete! Emails saved to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
