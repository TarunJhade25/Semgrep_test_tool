
import subprocess
import json
import pandas as pd
import os

def semgrep_scan_to_excel(repo_path, output_excel):
    try:
        # Run Semgrep scan and get JSON output
        result = subprocess.run(
            ["semgrep", "--config", "p/ci", "--json", repo_path],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print("Error running Semgrep:", result.stderr)
            return

        # Parse JSON output
        semgrep_results = json.loads(result.stdout)
        findings = semgrep_results.get("results", [])

        # Prepare data for Excel
        data = []
        for finding in findings:
            data.append({
                "Rule ID": finding.get("check_id"),
                "Severity": finding.get("extra", {}).get("severity"),
                "Message": finding.get("extra", {}).get("message"),
                "Path": finding.get("path"),
                "Start Line": finding.get("start", {}).get("line"),
                "End Line": finding.get("end", {}).get("line"),
                "Code Snippet": finding.get("extra", {}).get("lines")
            })

        # Convert to DataFrame
        df = pd.DataFrame(data)

        # Save to Excel
        df.to_excel(output_excel, index=False)
        print(f"Scan completed. Results saved to {output_excel}")

    except Exception as e:
        print("Error:", str(e))


# Example usage:
repo_path = "/path/to/your/local/repo"
output_excel = "semgrep_results.xlsx"
semgrep_scan_to_excel(repo_path, output_excel)
