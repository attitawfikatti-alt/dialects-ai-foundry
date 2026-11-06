#!/data/data/com.termux/files/usr/bin/bash
set -e
REPO_DIR="$HOME/dialects-ai-foundry"
cd "$REPO_DIR" || exit 1

show_menu() {
    clear
    echo "====================================================="
    echo "       🎙️  لوحة تحكم dialects-ai-foundry"
    echo "====================================================="
    echo " 1) 🎙️  تسجيل عينة مباشرة (recorder.py)"
    echo " 2) 📥 استيراد تسجيلات الهاتف الخارجية (ingest.py)"
    echo " 3) ✂️  تقطيع وتسجيل ملف طويل آلياً (segmenter.py)"
    echo " 4) 🔍 مراجعة وتدقيق العينات (reviewer.py)"
    echo " 5) 📊 عرض إحصائيات البيانات (stats.py)"
    echo " 6) 📦 تصدير وتقسيم البيانات لـ AI (export_dataset.py)"
    echo " 7) 🚀 مزامنة ورفع التغييرات إلى GitHub"
    echo " 8) 🚪 خروج"
    echo "====================================================="
    echo -n "اختر رقماً [1-8]: "
}

sync_github() {
    git status -s
    read -p "رفع التغييرات إلى GitHub؟ [Y/n]: " c
    if [[ "${c:-y}" =~ ^[Yy]$ ]]; then
        read -p "وصف التحديث: " msg
        git add .
        git commit -m "${msg:-Update dataset and tools}" || true
        git push origin $(git branch --show-current || echo "main")
    fi
}

while true; do
    show_menu
    read -r choice
    case $choice in
        1) python recorder.py; read -p "اضغط Enter..." ;;
        2) python ingest.py; read -p "اضغط Enter..." ;;
        3) python segmenter.py; read -p "اضغط Enter..." ;;
        4) python reviewer.py; read -p "اضغط Enter..." ;;
        5) python stats.py; read -p "اضغط Enter..." ;;
        6) python export_dataset.py; read -p "اضغط Enter..." ;;
        7) sync_github; read -p "اضغط Enter..." ;;
        8) exit 0 ;;
        *) sleep 1 ;;
    esac
done
