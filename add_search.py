import re

def main():
    with open('ders_programi.html', 'r', encoding='utf-8') as f:
        html = f.read()

    old_code = """                let html = `<h3>Ders Seçin</h3><div class="ders-grid">`;
                html += `<div class="ders-option" style="background:#b2bec3" onclick="window.closeModal()">
                <div class="ders-kod">❌</div><div class="ders-ad">İPTAL ET</div>
             </div>`;
                html += `<div class="ders-option hoca-bos" style="background:#ff7675" onclick="window.selectCourseAction('empty')">
                <div class="ders-kod">—</div><div class="ders-ad">BOŞ BIRAK</div>
             </div>`;

                courses.forEach(c => {
                    if (isElektronik && c.kod.startsWith('ELT')) return;
                    if (!isElektronik && c.kod.startsWith('ELO')) return;

                    html += `<div class="ders-option hoca-${c.hoca}" onclick="window.selectCourseAction('${c.kod}')">"""

    new_code = """                let html = `<h3>Ders Seçin</h3>
                <input type="text" id="course-select-search" class="search-input" placeholder="Ders Ara..." onkeyup="window.filterCourseSelect()" style="width:100%; box-sizing:border-box; margin-bottom:15px; padding:8px; border-radius:6px; border:1px solid #ddd;">
                <div class="ders-grid" id="course-select-grid">`;
                
                html += `<div class="ders-option" style="background:#b2bec3" onclick="window.closeModal()">
                <div class="ders-kod">❌</div><div class="ders-ad">İPTAL ET</div>
             </div>`;
                html += `<div class="ders-option hoca-bos" style="background:#ff7675" onclick="window.selectCourseAction('empty')">
                <div class="ders-kod">—</div><div class="ders-ad">BOŞ BIRAK</div>
             </div>`;

                courses.forEach(c => {
                    if (isElektronik && c.kod.startsWith('ELT')) return;
                    if (!isElektronik && c.kod.startsWith('ELO')) return;

                    html += `<div class="ders-option selectable-course hoca-${c.hoca}" onclick="window.selectCourseAction('${c.kod}')" data-kod="${c.kod.toLowerCase()}" data-ad="${c.ad.toLowerCase()}">"""

    html = html.replace(old_code, new_code)
    
    # Add window.filterCourseSelect function right after openCourseModal
    func_insert = """
            window.filterCourseSelect = function() {
                const search = document.getElementById('course-select-search').value.toLowerCase();
                const items = document.querySelectorAll('#course-select-grid .selectable-course');
                items.forEach(item => {
                    const kod = item.getAttribute('data-kod');
                    const ad = item.getAttribute('data-ad');
                    if(kod.includes(search) || ad.includes(search)) {
                        item.style.display = 'flex';
                    } else {
                        item.style.display = 'none';
                    }
                });
            };
"""
    html = html.replace("window.selectCourseAction = function (action) {", func_insert + "\n            window.selectCourseAction = function (action) {")

    with open('ders_programi.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Search bar added to course select modal.")

if __name__ == '__main__':
    main()
