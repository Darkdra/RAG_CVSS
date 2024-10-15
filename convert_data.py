import json
import os
import shutil

DATA_PATH = "./data/cves"
CONVERTED_PATH = "./data/cves_text"


def main():

    if os.path.exists(CONVERTED_PATH):
        shutil.rmtree(CONVERTED_PATH)

    # convert json format into text (natural language format)
    for year_dir in os.listdir(DATA_PATH):
        os.makedirs(os.path.join(CONVERTED_PATH, year_dir))
        print(year_dir)
        for tag_dir in os.listdir(os.path.join(DATA_PATH, year_dir)):
            for json_file in os.listdir(os.path.join(DATA_PATH, year_dir, tag_dir)):
                with open(
                    os.path.join(DATA_PATH, year_dir, tag_dir, json_file), "r"
                ) as f:
                    js = json.loads(f.read())

                if js.get("cveMetadata", {}).get("state") == "REJECTED":
                    continue

                cve_id = js.get("cveMetadata", {}).get("cveId")

                adp = js.get("containers", {}).get("adp", [])

                if len(adp) == 0:
                    continue

                metrics = adp[0].get("metrics", [])

                if not metrics:
                    continue

                for me in metrics:
                    if me.get("cvssV3_1", {}):
                        cvss3_1 = me.get("cvssV3_1", {})
                        break
                else:
                    continue

                descriptions = (
                    js.get("containers", {}).get("cna", {}).get("descriptions", [])
                )
                en_description = ""
                for desc in descriptions:
                    if desc.get("lang") == "en":
                        en_description = desc.get("value")
                        break
                else:
                    continue

                with open(
                    os.path.join(CONVERTED_PATH, json_file.replace(".json", ".txt")),
                    "w",
                ) as tx:
                    tx.write(f"CVE ID: {cve_id}\n")
                    tx.write("Description: \n")
                    tx.write(en_description + "\n")
                    tx.write(f"vector string: {cvss3_1['vectorString']}\n")
                    tx.write(f"attack vector: {cvss3_1['attackVector']}\n")
                    tx.write(f"attack complexity: {cvss3_1['attackComplexity']}\n")
                    tx.write(f"privileges required: {cvss3_1['privilegesRequired']}\n")
                    tx.write(f"user interaction: {cvss3_1['userInteraction']}\n")
                    tx.write(f"scope: {cvss3_1['scope']}\n")
                    tx.write(
                        f"confidentiality impact: {cvss3_1['confidentialityImpact']}\n"
                    )
                    tx.write(f"integrity impact: {cvss3_1['integrityImpact']}\n")
                    tx.write(f"availability impact: {cvss3_1['availabilityImpact']}\n")
                    tx.write(f"base severity: {cvss3_1['baseSeverity']}\n")
                    tx.write(f"base score: {cvss3_1['baseScore']}\n")


if __name__ == "__main__":
    main()
