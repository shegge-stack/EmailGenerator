import re
import csv
from hubspot_integration import create_sequence, enroll_contact

INPUT_FILE = "generated_sequences.csv"

def parse_sequence(raw_sequence):
    emails = []
    pattern = r'<email step="\d+">\s*Subject:\s*(.*?)\nBody:\s*(.*?)</email>'
    matches = re.findall(pattern, raw_sequence, re.DOTALL)

    for subject, body in matches:
        emails.append({"subject": subject.strip(), "body": body.strip()})
    return emails

def main():
    with open(INPUT_FILE, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sequence_name = f"Outbound Seq - {row['companyName']}"
            emails = parse_sequence(row["email_sequence"])

            seq_id = create_sequence(sequence_name, emails)
            if not seq_id:
                print(f"⚠️ Skipping enrollment for {row['companyName']} due to sequence creation failure.")
                continue

            contact_id = row.get("hubspotContactId")
            if contact_id:
                success = enroll_contact(contact_id, seq_id)
                if not success:
                    print(f"⚠️ Enrollment failed for contact {contact_id} - manual follow-up may be needed.")
            else:
                print(f"⚠️ No HubSpot Contact ID for {row['companyName']}, skipping enrollment.")

if __name__ == "__main__":
    main()
