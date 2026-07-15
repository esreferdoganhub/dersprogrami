import re

def main():
    with open('ders_programi.html', 'r', encoding='utf-8') as f:
        html = f.read()

    old_code = """                // Sync scheduleData courses to courses array
                const uniqueCourseCodes = new Set(courses.map(c => c.kod));"""
    
    new_code = """                // Sync scheduleData courses to courses array
                courses = []; // Clear old courses and strictly rebuild from scheduleData
                const uniqueCourseCodes = new Set();"""

    html = html.replace(old_code, new_code)

    with open('ders_programi.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Courses strict sync logic added.")

if __name__ == '__main__':
    main()
