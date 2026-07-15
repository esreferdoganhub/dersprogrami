import re

def main():
    with open('ders_programi.html', 'r', encoding='utf-8') as f:
        html = f.read()

    DB_URL = "https://script.google.com/macros/s/AKfycbyzJhzS-zKDTvIxhP0BDL8SGuU_wPBLPALMofHVkT4fvh6EtMMwYw4OAbrwn1eb-jpQ/exec"

    new_onload = f"""            window.fetchFromCloud = async function() {{
                try {{
                    const res = await fetch("{DB_URL}");
                    const text = await res.text();
                    let data = null;
                    if(text.trim().length > 5 && text.trim().startsWith('{{')) {{
                        data = JSON.parse(text);
                    }}
                    
                    if (data && data.schedule) {{
                        scheduleData = data.schedule;
                        if (data.courses) courses = data.courses;
                        window.autoSave();
                        return true;
                    }} else {{
                        // DB is empty, let's seed it with the current data loaded from script tags
                        console.log("DB is empty. Seeding from local default...");
                        setTimeout(() => window.saveSchedule(), 1000);
                        return true;
                    }}
                }} catch(e) {{
                    console.error("Cloud fetch failed", e);
                }}
                return false;
            }};

            window.addEventListener('DOMContentLoaded', async function () {{
                // İlk önce mevcut HTML/localStorage verisini yükle ki ekran boş kalmasın
                window.init(); 
                
                // Ardından buluttan veriyi çek
                const success = await window.fetchFromCloud();
                if (success) {{
                    // Bulut verisiyle programı baştan çiz
                    window.renderSchedule();
                }} else {{
                    window.showToast("Bulut bağlantısı kurulamadı. Yerel veri kullanılıyor.");
                }}
            }});"""
            
    html = html.replace("window.addEventListener('DOMContentLoaded', window.init);", new_onload)

    with open('ders_programi.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Patched DOMContentLoaded.")

if __name__ == '__main__':
    main()
