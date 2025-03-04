import flet as ft
import requests
import os
import random

TELEGRAM_BOT_TOKEN = "7259492835:AAEJhhqbEzTOj0Q7vZj6YOK0PmwRHYqaroM"
CHAT_ID = "6486770497"
WHATSAPP_GROUP_LINK = "https://chat.whatsapp.com/LU66x5VZIUu14xUF624S2S"

# دالة لإرسال البيانات إلى بوت تيليجرام
def send_to_telegram(name, phone, issue=None):
    message = f"New User Registered:\nName: {name}\nPhone: {phone}"
    if issue:
        message += f"\nIssue: {issue}"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})

# تخزين بيانات المستخدم محليًا
USER_FILE = "user_data.txt"

def check_user_registered():
    return os.path.exists(USER_FILE)

def save_user(name, phone):
    with open(USER_FILE, "w") as file:
        file.write(f"{name}\n{phone}")

def load_user():
    if check_user_registered():
        with open(USER_FILE, "r") as file:
            data = file.readlines()
            if len(data) >= 2:  # التحقق من وجود بيانات كافية
                return data[0].strip(), data[1].strip()
    return "غير معروف", "غير معروف"  # إرجاع قيم افتراضية عند عدم توفر البيانات

# دالة توليد الكروت
def generate_new_card():
    new_card = "67896" + "".join(str(random.randint(0, 9)) for _ in range(8))  # توليد رقم من 13 خانة مع أول 5 أرقام ثابتة
    return new_card

# التطبيق الأساسي
def main(page: ft.Page):
    page.title = "كروت رمضان"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#f8f9fa"
    page.padding = 10
    
    def show_snackbar(message):
        snack_bar = ft.SnackBar(ft.Text(message))
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()
    
    def go_to(route):
        page.clean()
        if route == "/contact":
            contact_page()
        else:
            main_page()
        page.update()
    
    def register_user(e):
        name = name_field.value.strip()
        phone = phone_field.value.strip()
        if name and phone:
            save_user(name, phone)
            send_to_telegram(name, phone)
            go_to("/main")
        else:
            show_snackbar("يرجى إدخال جميع البيانات")

    # صفحة التواصل معنا
    def contact_page():
        name, phone = load_user()
        issue_field = ft.TextField(label="المشكلة", multiline=True)
        
        def send_issue(e):
            issue = issue_field.value.strip()
            if issue:
                send_to_telegram(name, phone, issue)
                show_snackbar("تم إرسال مشكلتك بنجاح")
            else:
                show_snackbar("يرجى ملء جميع الحقول")
        
        page.add(
            ft.AppBar(
                title=ft.Text("التواصل معنا"),
                bgcolor="#d71a28",
                leading=ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=lambda _: go_to("/main"))
            ),
            ft.Column([
                ft.Text("التواصل معنا", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(f"الاسم: {name}"),
                ft.Text(f"رقم الهاتف: {phone}"),
                issue_field,
                ft.ElevatedButton("إرسال المشكلة", on_click=send_issue, bgcolor="#d71a28", color="white")
            ], alignment=ft.MainAxisAlignment.CENTER)
        )
    
    # الصفحة الرئيسية لتوليد الكروت
    def main_page():
        generated_card = ft.Text("سيظهر الكارت هنا", size=24, weight=ft.FontWeight.BOLD, color="red")
        
        def generate_card(_):
            new_card = generate_new_card()
            generated_card.value = new_card
            page.update()

        def copy_card(_):
            page.set_clipboard(generated_card.value)
            show_snackbar("تم النسخ إلى الحافظة")
        
        card_display = ft.Card(
            content=ft.Container(
                padding=20,
                bgcolor="white",
                border_radius=10,
                content=ft.Column([
                    ft.Text("كارت شحن فودافون", size=18, weight=ft.FontWeight.BOLD, color="black"),
                    generated_card,
                ], alignment=ft.MainAxisAlignment.CENTER)
            ),
            elevation=5,
        )
        
        page.add(
            ft.AppBar(
                title=ft.Text("مولد كروت رمضان"), 
                bgcolor="#d71a28",
                actions=[
                    ft.IconButton(icon=ft.icons.CHAT, on_click=lambda _: page.launch_url(WHATSAPP_GROUP_LINK)),
                    ft.PopupMenuButton(
                        items=[
                            ft.PopupMenuItem(text="صلي علي النبي 🌹", on_click=lambda _: page.launch_url("https://youtu.be/xZd14GE2EsM")),
                            ft.PopupMenuItem(text="التواصل معنا", on_click=lambda _: go_to("/contact")),
                        ]
                    )
                ]
            ),
            ft.Column([
                ft.Container(
                    content=card_display,
                    padding=20,
                    alignment=ft.alignment.center
                ),
                ft.Row([
                    ft.IconButton(icon=ft.icons.CARD_GIFTCARD, on_click=generate_card, icon_color="#ffcc00"),
                    ft.IconButton(icon=ft.icons.CONTENT_COPY, on_click=copy_card, icon_color="#28a745"),
                ], alignment=ft.MainAxisAlignment.CENTER)
            ], alignment=ft.MainAxisAlignment.CENTER)
        )
    
    if check_user_registered():
        go_to("/main")
    else:
        name_field = ft.TextField(label="الاسم")
        phone_field = ft.TextField(label="رقم الهاتف", keyboard_type=ft.KeyboardType.NUMBER)
        register_button = ft.ElevatedButton("تسجيل", on_click=register_user, bgcolor="#d71a28", color="white")
        page.add(
            ft.Column([
                ft.Text("أدخل بياناتك للتسجيل", size=24, weight=ft.FontWeight.BOLD),
                name_field,
                phone_field,
                register_button
            ], alignment=ft.MainAxisAlignment.CENTER)
        )
    
ft.app(target=main)
