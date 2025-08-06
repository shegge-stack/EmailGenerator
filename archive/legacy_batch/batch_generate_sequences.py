import csv
from sdr_sequence_generator import SDRSequenceGenerator


INPUT_CSV = "prospects.csv"
OUTPUT_CSV = "generated_sequences.csv"

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
            prospects.append(row)
    return prospects

def save_results(results):
    with open(OUTPUT_CSV, "w", newline='', encoding="utf-8") as f:
        fieldnames = REQUIRED_COLUMNS + ["email_sequence"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            writer.writerow(r)

def main():
    generator = SDRSequenceGenerator()
    prospects = load_prospects(INPUT_CSV)
    results = []

    for prospect in prospects:
        print(f"Generating sequence for {prospect['firstName']} ({prospect['companyName']})...")
        sequence = generator.generate_sequence(prospect)
        prospect["email_sequence"] = sequence
        results.append(prospect)

    save_results(results)
    print(f"✅ Sequences saved to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
