import re

def main():
    with open('ders_programi.html', 'r', encoding='utf-8') as f:
        html = f.read()

    DB_URL = "https://script.google.com/macros/s/AKfycbyzJhzS-zKDTvIxhP0BDL8SGuU_wPBLPALMofHVkT4fvh6EtMMwYw4OAbrwn1eb-jpQ/exec"

    # 1. Update saveSchedule
    old_save = """            window.saveSchedule = function () {
                window.autoSave();
                window.showToast('💾 Tarayıcıya Kaydedildi!');
            };"""
            
    new_save = f"""            window.saveSchedule = async function () {{
                window.showToast('Buluta Kaydediliyor... ⏳');
                window.autoSave(); // Yerel yedek
                
                try {{
                    const payload = JSON.stringify({{
                        schedule: scheduleData,
                        courses: courses
                    }});
                    
                    await fetch("{DB_URL}", {{
                        method: "POST",
                        headers: {{
                            "Content-Type": "text/plain;charset=utf-8"
                        }},
                        body: payload
                    }});
                    
                    window.showToast('✅ Buluta Kalıcı Olarak Kaydedildi!');
                }} catch(e) {{
                    console.error("Save error:", e);
                    window.showToast('❌ Kaydetme Hatası!');
                }}
            }};"""
    html = html.replace(old_save, new_save)

    # 2. Add fetchFromCloud and loading UI
    # Replace window.onload
    old_onload = """            window.onload = function () {
                window.init();
            };"""
            
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
                        // Use setTimeout so it doesn't block loading
                        setTimeout(() => window.saveSchedule(), 1000);
                        return true;
                    }}
                }} catch(e) {{
                    console.error("Cloud fetch failed", e);
                }}
                return false;
            }};

            window.onload = async function () {{
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
            }};"""
            
    html = html.replace(old_onload, new_onload)
    
    # 3. Change "Verileri Yedekle" to "🐙 Buluta Kaydet" and use it as a manual save fallback
    # Wait, the user wanted an automatic save? Or do they just press the Save button?
    # Actually, the action bar has a "💾 Tarayıcıya Kaydet" button. Let's rename it to "💾 Buluta Kaydet".
    html = html.replace("💾 Tarayıcıya Kaydet", "💾 Buluta Kaydet")
    
    # Hide the "Verileri Yedekle (Kopyala)" button since it's no longer needed, 
    # but keep it in code just in case.
    html = html.replace('id="copy-data-btn" onclick="copyDataToClipboard()" style="display:none; background:#e17055;">', 'id="copy-data-btn" onclick="copyDataToClipboard()" style="display:none; background:#e17055;">')

    with open('ders_programi.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Sheets DB integrated.")

if __name__ == '__main__':
    main()
