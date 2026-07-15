import sys

def main():
    with open('ders_programi.html', 'r', encoding='utf-8') as f:
        content = f.read()

    btn_html = """            <button class="action-btn" id="course-management-btn" onclick="openCourseManagement()" style="display:none; background:#6c5ce7;">📚 Dersleri Yönet</button>
            <button class="action-btn" id="copy-data-btn" onclick="copyDataToClipboard()" style="display:none; background:#e17055;">💾 Verileri Yedekle (Kopyala)</button>"""

    content = content.replace(
        '<button class="action-btn" id="course-management-btn" onclick="openCourseManagement()" style="display:none; background:#6c5ce7;">📚 Dersleri Yönet</button>',
        btn_html
    )

    js_code = """
            window.copyDataToClipboard = function() {
                const data = {
                    schedule: scheduleData,
                    courses: courses
                };
                const str = JSON.stringify(data);
                navigator.clipboard.writeText(str).then(() => {
                    alert("Tüm ders programı verileri panoya kopyalandı! Lütfen şimdi bu veriyi yapay zekaya (bana) yapıştırarak gönderin ki kalıcı olarak siteye ekleyebileyim.");
                }).catch(err => {
                    alert("Kopyalama başarısız oldu. Lütfen manuel olarak alın.");
                });
            };
"""
    content = content.replace("window.openCourseManagement = function() {", js_code + "\n            window.openCourseManagement = function() {")
    
    # Also make sure the button becomes visible when admin logs in
    content = content.replace("document.getElementById('course-management-btn').style.display = 'block';", "document.getElementById('course-management-btn').style.display = 'block';\n                if(document.getElementById('copy-data-btn')) document.getElementById('copy-data-btn').style.display = 'block';")

    with open('ders_programi.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added copy button.")

if __name__ == '__main__':
    main()
