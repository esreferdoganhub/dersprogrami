import sys

def main():
    with open('ders_programi.html', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Find start of SİSTEM ÖZELLİKLERİ MODALI (line 1734)
    start_idx = -1
    for i, line in enumerate(lines):
        if '<!-- SİSTEM ÖZELLİKLERİ MODALI -->' in line:
            start_idx = i
            break

    # Find end of DERS YÖNETİM MODALI (around line 1820)
    end_idx = -1
    for i in range(start_idx, len(lines)):
        if '<script id="schedule-data"' in lines[i]:
            end_idx = i - 1  # the empty line before script
            break

    if start_idx == -1 or end_idx == -1:
        print("Could not find blocks.")
        return

    # extract blocks
    modals_block = lines[start_idx:end_idx]
    
    # remove them from original position
    lines = lines[:start_idx] + lines[end_idx:]

    # find toast
    toast_idx = -1
    for i, line in enumerate(lines):
        if '<!-- Toast -->' in line:
            toast_idx = i
            break

    if toast_idx == -1:
        print("Could not find toast.")
        return

    # insert before toast
    lines = lines[:toast_idx] + modals_block + lines[toast_idx:]

    with open('ders_programi.html', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("Modals moved successfully.")

if __name__ == '__main__':
    main()
