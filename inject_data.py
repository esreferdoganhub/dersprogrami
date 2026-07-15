import json
import re

def main():
    with open('new_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    schedule = data.get('schedule', {})
    courses = data.get('courses', [])
    
    with open('ders_programi.html', 'r', encoding='utf-8') as f:
        html = f.read()
        
    # Replace schedule-data
    schedule_str = json.dumps(schedule, ensure_ascii=False)
    html = re.sub(
        r'(<script id="schedule-data" type="application/json">).*?(</script>)',
        f'\\g<1>\n{schedule_str}\n\\g<2>',
        html,
        flags=re.DOTALL
    )
    
    # Replace courses-data
    courses_str = json.dumps(courses, ensure_ascii=False)
    html = re.sub(
        r'(<script id="courses-data" type="application/json">).*?(</script>)',
        f'\\g<1>\n{courses_str}\n\\g<2>',
        html,
        flags=re.DOTALL
    )
    
    with open('ders_programi.html', 'w', encoding='utf-8') as f:
        f.write(html)
        
    print("Data injected successfully.")

if __name__ == '__main__':
    main()
