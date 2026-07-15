import sys

def main():
    with open('ders_programi.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Add overlay click events for both features and course management modals
    click_script = """
            // Overlay click to close
            document.getElementById('features-modal').addEventListener('click', function(e) {
                if(e.target === this) window.closeFeaturesModal();
            });
            document.getElementById('course-management-modal').addEventListener('click', function(e) {
                if(e.target === this) window.closeCourseManagement();
            });
"""
    if "features-modal').addEventListener('click'" not in content:
        content = content.replace("window.closeFeaturesModal = function() {", click_script + "\n            window.closeFeaturesModal = function() {")

    # Add closeCourseManagement to Escape key
    if "window.closeCourseManagement();" not in content.split("e.key === 'Escape'")[1].split("}")[0]:
        content = content.replace("window.closeFeaturesModal();", "window.closeFeaturesModal();\n                    if(typeof window.closeCourseManagement === 'function') window.closeCourseManagement();")

    with open('ders_programi.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("JS fixes applied.")

if __name__ == '__main__':
    main()
