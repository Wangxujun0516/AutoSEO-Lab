import csv  # Python's built-in tool for managing standard tabular data
import time

# 💡 Full English dataset simulating crawled raw HTML chunks
raw_html_payload = [
    "<html><title>  12V Electric RV Leveling Jacks | High Capacity </title></html>",
    "<html>\n<TITLE>\n   Heavy-Duty Hydraulic Valve Durability Specs   \n</TITLE>\n</html>",
    "<html><TiTlE>B2B Sourcing Matrix 2026 | Henghong Intelligent</title></html>",
    "<html>Malformed HTML structure without title tag</html>"
]

def extract_title_node(html_data: str) -> str:
    """Parses raw HTML and returns a sanitized, whitespace-stripped title string."""
    shadow_copy = html_data.lower()
    start_locator, end_locator = "<title>", "</title>"
    
    if start_locator in shadow_copy and end_locator in shadow_copy:
        start_pos = shadow_copy.find(start_locator) + len(start_locator)
        end_pos = shadow_copy.find(end_locator)
        # Slicing from the original case-sensitive string and stripping whitespaces
        return html_data[start_pos:end_pos].strip()
    return "STATUS_ERROR: Missing Meta Title"

def export_to_seo_sheet(dataset: list, filename: str) -> None:
    """Iterates through the payload and exports clean SEO titles into a structured CSV."""
    total_records = len(dataset)
    print(f"🏭 SEO Pipeline Initialized. Exporting target file: {filename}\n" + "="*60)
    
    # open(..., mode="w", newline="") is the industrial standard for writing CSVs safely without breaking row indices
    with open(filename, mode="w", newline="", encoding="utf-8") as csv_file:
        # Define standard English headers for SEO technical audits
        fieldnames = ["Task_ID", "Status", "Extracted_Meta_Title"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        # Write the header row to the sheet
        writer.writeheader()
        
        for current_id, raw_html in enumerate(dataset, start=1):
            print(f"⚙️ Processing record [{current_id}/{total_records}]...")
            
            clean_title = extract_title_node(raw_html)
            status_flag = "SUCCESS" if "STATUS_ERROR" not in clean_title else "FAILED"
            
            # Writing structured rows mapping directly to the CSV headers
            writer.writerow({
                "Task_ID": f"SEO-TASK-{current_id:03d}", # Generates standard IDs like SEO-TASK-001
                "Status": status_flag,
                "Extracted_Meta_Title": clean_title
            })
            
            if current_id < total_records:
                time.sleep(0.3)
                
    print("="*60 + f"\n🎉 Operation completed. Open '{filename}' to inspect your clean SEO assets.")

if __name__ == "__main__":
    export_to_seo_sheet(raw_html_payload, "seo_audit_report.csv")