import re
import sys

def verify_markdown_tables(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by exam periods (Markdown headers like #### 📅 2026年4月考期)
    periods = re.split(r'#### 📅 (\d{4}年\d{1,2}月考期)', content)
    
    conflicts = []
    
    for i in range(1, len(periods), 2):
        period_name = periods[i]
        table_content = periods[i+1]
        
        # Find all table rows
        rows = re.findall(r'\| (.*?) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \|', table_content)
        
        # Skip header rows
        data_rows = [row for row in rows if row[0].strip() and '-' not in row[0] and '时间' not in row[0]]
        
        time_slots = {}
        for row in data_rows:
            time_slot = row[0].strip()
            course_name = row[2].strip()
            
            if time_slot in time_slots:
                conflicts.append(f"CONFLICT in {period_name}: '{time_slot}' has both '{time_slots[time_slot]}' and '{course_name}'")
            else:
                time_slots[time_slot] = course_name
                
    return conflicts

if __name__ == "__main__":
    target_file = "C2=等待处理/2.4=日程/自考专本连读极速毕业计划_免考提速版.md"
    print(f"Verifying {target_file}...")
    results = verify_markdown_tables(target_file)
    
    if results:
        print("\n❌ Found scheduling conflicts:")
        for conflict in results:
            print(f"  - {conflict}")
        sys.exit(1)
    else:
        print("\n✅ No conflicts found in the schedule!")
        sys.exit(0)
