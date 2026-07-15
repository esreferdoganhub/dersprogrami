import sys

def main():
    with open('ders_programi.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add course sync logic to init()
    sync_code = """
                // Sync scheduleData courses to courses array
                const uniqueCourseCodes = new Set(courses.map(c => c.kod));
                ['elektrik', 'elektronik'].forEach(dept => {
                    if(scheduleData[dept]) {
                        Object.keys(scheduleData[dept]).forEach(cellIdx => {
                            scheduleData[dept][cellIdx].forEach(item => {
                                if(!uniqueCourseCodes.has(item.kod)) {
                                    courses.push({
                                        kod: item.kod,
                                        ad: item.ad || '',
                                        sinif: item.sinif || 1,
                                        hoca: item.hoca || 'ortak'
                                    });
                                    uniqueCourseCodes.add(item.kod);
                                }
                            });
                        });
                    }
                });
"""
    if "uniqueCourseCodes.has" not in content:
        content = content.replace("try {", sync_code + "\n                try {", 1) # first try after loading data

    # 2. Add search input html
    search_html = """                <div style="margin-bottom: 15px;">
                    <input type="text" id="course-search-input" class="course-form-input" placeholder="🔍 Ders Kodu, Adı veya Hoca Ara..." oninput="window.renderCourseList()">
                </div>
                <div class="course-list-container" id="course-list-container">"""
    
    if "id=\"course-search-input\"" not in content:
        content = content.replace("<div class=\"course-list-container\" id=\"course-list-container\">", search_html)

    # 3. Update renderCourseList
    old_render = """                // Sort by code for easy reading
                const sortedCourses = [...courses].sort((a,b) => a.kod.localeCompare(b.kod));
                
                sortedCourses.forEach(c => {"""
    
    new_render = """                const searchInput = document.getElementById('course-search-input');
                const filterText = searchInput ? searchInput.value.toLowerCase() : '';
                
                // Sort by sinif ascending, then by kod
                let sortedCourses = [...courses].sort((a,b) => {
                    if (a.sinif !== b.sinif) return a.sinif - b.sinif;
                    return a.kod.localeCompare(b.kod);
                });
                
                if (filterText) {
                    sortedCourses = sortedCourses.filter(c => 
                        c.kod.toLowerCase().includes(filterText) || 
                        c.ad.toLowerCase().includes(filterText) ||
                        getHocaRealName(c.hoca).toLowerCase().includes(filterText)
                    );
                }
                
                sortedCourses.forEach(c => {"""
    
    if "const searchInput = document.getElementById" not in content:
        content = content.replace(old_render, new_render)

    with open('ders_programi.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed courses.")

if __name__ == '__main__':
    main()
