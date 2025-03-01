import flet as ft
import time
import requests
import json
from datetime import datetime, timedelta
import os
def main(page: ft.Page):
    page.title = 'TikTok Free Viewers'
    page.window.width = 370
    page.window.height = 650
    page.on_route_change = lambda e: route_change(page)
    
    # تحديد الصفحة الافتراضية
    page.go('/home')
API_KEY = "1YHzPe0UKOe1AwwYtvQpkMKzF04DKtQYpKzRxAM3rTQu8unAS8tQl5JjPBkh"
API_URL = "https://smmeg.shop/api/v2"

def send_view_request(video_url, quantity):
    """ إرسال طلب المشاهدات إلى API موقع SMMEG """
    payload = {
        "key": API_KEY,
        "action": "add",
        "service": "1972",  # ضع ID الخدمة الصحيحة هنا
        "link": video_url,
        "quantity": quantity
    }
    
    response = requests.post(API_URL, data=payload)
    return response.json()
def home():
    return ft.View(
        "/home",
        controls=[
            # ✅ شريط التطبيق (AppBar)
            ft.AppBar(
                title=ft.Text("TikTok Free Views", color="white", size=22, weight=ft.FontWeight.BOLD),
                bgcolor="#ff0050",
                center_title=True,
                actions=[
                    # 🔹 زر التحديث (يفتح نافذة واتساب بدلًا من التحديث)
                    ft.IconButton(ft.icons.REFRESH, tooltip="Refresh", on_click=lambda e: show_whatsapp_dialog(e)),
                    
                    # 🔹 زر القائمة المنبثقة
                    ft.PopupMenuButton(
                        icon=ft.icons.MORE_VERT,
                        items=[
                            ft.PopupMenuItem("Contact on WhatsApp", on_click=show_whatsapp_dialog),
                            ft.PopupMenuItem("About", on_click=lambda e: e.page.go('/home')),
                        ]
                    )
                ],
            ),

            # ✅ محتوى الصفحة
            ft.Container(
                expand=True,
                bgcolor="#181818",
                content=ft.Column(
                    [
                        ft.Icon(ft.icons.TIKTOK, size=100, color="#ff0050"),
                        ft.Text(
                            "رشق تيك توك مجانا",
                            size=24,
                            color="white",
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER
                        ),

                        # ✅ شبكة الأزرار (GridView)
                        ft.GridView(
                            expand=True,
                            runs_count=2,
                            spacing=15,
                            run_spacing=15,
                            controls=[
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            ft.Icon(ft.icons.REMOVE_RED_EYE, size=40, color="white"),
                                            ft.Text("مشاهدات", size=16, color="white", text_align=ft.TextAlign.CENTER),
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                    ),
                                    bgcolor="#ff0050",
                                    border_radius=15,
                                    padding=20,
                                    on_click=lambda e: e.page.go('/View'),
                                    ink=True
                                ),

                                ft.Container(
                                    content=ft.Column(
                                        [
                                            ft.Text("لايكات", size=16, color="white", text_align=ft.TextAlign.CENTER),
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                    ),
                                    bgcolor="#ff9800",
                                    border_radius=15,
                                    padding=20,
                                    on_click=lambda e: e.page.go('/likes'),
                                    ink=True
                                )
                            ]
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20
                )
            )
        ]
    )

def showupdate(e):
    """ دالة لعرض نافذة تحتوي على رقم الهاتف وزر النسخ """
    
    whatsapp_number = "+201008125431"  # ضع رقمك هنا
    
    def copy_number(e):
        e.page.set_clipboard(whatsapp_number)  # نسخ الرقم إلى الحافظة
        e.page.open(ft.SnackBar(content=ft.Text("Number copied! ✅"), bgcolor="green"))  # ✅ الطريقة الجديدة
    
    dialog = ft.AlertDialog(
        title=ft.Text("قريبا", size=18, weight=ft.FontWeight.BOLD),
        content=ft.Column(
            [
                ft.Text("اهلا بيك ي غالي لو معاك مشكله تواصل معيا فورا عادي اخي تم نزول تحديث جديد تواصل معيا عشان تحدث التطبيق ", size=14),
                ft.Row(
                    [
                        ft.Text(whatsapp_number, size=16, color="blue"),
                        ft.IconButton(ft.icons.CONTENT_COPY, tooltip="Copy Number", on_click=copy_number)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
            ],
            tight=True
        ),
        actions=[
            ft.TextButton("Close", on_click=lambda e: close_dialog(e))  # ✅ تصحيح الإغلاق
        ]
    )

    e.page.overlay.append(dialog)  # ✅ الطريقة الجديدة لعرض الـ Dialog
    e.page.update()  # تحديث الصفحة لإضافة الـ Dialog
    e.page.open(dialog)  # ✅ فتح الـ Dialog

def close_dialog(e):
    """ دالة لإغلاق الـ Dialog """
    for control in e.page.overlay:
        if isinstance(control, ft.AlertDialog):
            control.open = False
    e.page.update()  # تحديث الصفحة بعد الإغلاق


def likes():
    """ صفحة تزويد اللايكات على فيديوهات تيك توك """
    selected_value = ft.Ref[ft.Dropdown]()
    button_state = ft.Ref[ft.AnimatedSwitcher]()

    def process_likes(e):
        """ دالة لتغيير الزر عند الضغط """
        button_state.current.content = ft.ProgressRing(color="white")
        e.page.update()

        time.sleep(2)  # محاكاة معالجة البيانات

        # إعادة الزر الأصلي
        button_state.current.content = ft.ElevatedButton(
            "Get Likes",
            on_click=process_likes,
            bgcolor="#ff9800",
            color="white",
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=10,
                elevation=5
            ),
        )
        e.page.update()

    return ft.View(
        "/likes",
        controls=[
            ft.AppBar(
                title=ft.Text("TikTok Free Likes", color="white", size=22, weight=ft.FontWeight.BOLD),
                bgcolor="#ff9800",
                center_title=True,
                leading=ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda e: e.page.go('/home')),
                actions=[
                    ft.IconButton(ft.icons.REFRESH, tooltip="Refresh", on_click=lambda e: show_whatsapp_dialog(e)),
                    ft.PopupMenuButton(
                        icon=ft.icons.MORE_VERT,
                        items=[
                            ft.PopupMenuItem("Contact on WhatsApp", on_click=show_whatsapp_dialog),
                            ft.PopupMenuItem("About", on_click=lambda e: e.page.go('/home')),
                        ]
                    )
                ],
            ),

            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "Boost Your TikTok Likes Instantly!",
                            size=20,
                            color="white",
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER
                        ),

                        ft.TextField(
                            label="Enter TikTok Video Link",
                            hint_text="Paste your video link here...",
                            border_color="#ff9800",
                            text_style=ft.TextStyle(color="white"),
                            bgcolor="#282828",
                            border_radius=10
                        ),

                        ft.Dropdown(
                            ref=selected_value,
                            label="Select Like Count",
                            hint_text="Choose the number of likes...",
                            options=[
                                ft.dropdown.Option("1000"),
                            ],
                            border_color="#ff9800",
                            text_style=ft.TextStyle(color="white"),
                            bgcolor="#282828",
                            border_radius=10
                        ),

                        ft.AnimatedSwitcher(
                            ref=button_state,
                            duration=500,
                            transition=ft.AnimatedSwitcherTransition.FADE,
                            content=ft.ElevatedButton(
                                "Get Likes",
                                on_click=showupdate,
                                bgcolor="#ff9800",
                                color="white",
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    padding=10,
                                    elevation=5
                                ),
                            ),
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15
                ),
                expand=True,
                bgcolor="#181818",
                padding=20
            )
        ]
    )

def show_whatsapp_dialog(e):
    """ دالة لعرض نافذة تحتوي على رقم الهاتف وزر النسخ """
    
    whatsapp_number = "+201008125431"  # ضع رقمك هنا
    
    def copy_number(e):
        e.page.set_clipboard(whatsapp_number)  # نسخ الرقم إلى الحافظة
        e.page.open(ft.SnackBar(content=ft.Text("Number copied! ✅"), bgcolor="green"))  # ✅ الطريقة الجديدة
    
    dialog = ft.AlertDialog(
        title=ft.Text("تواصل مع المطور", size=18, weight=ft.FontWeight.BOLD),
        content=ft.Column(
            [
                ft.Text("اهلا بيك ي غالي لو معاك مشكله تواصل معيا فورا عادي اخي تم نزول تحديث جديد تواصل معيا عشان تحدث التطبيق ", size=14),
                ft.Row(
                    [
                        ft.Text(whatsapp_number, size=16, color="blue"),
                        ft.IconButton(ft.icons.CONTENT_COPY, tooltip="Copy Number", on_click=copy_number)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
            ],
            tight=True
        ),
        actions=[
            ft.TextButton("Close", on_click=lambda e: close_dialog(e))  # ✅ تصحيح الإغلاق
        ]
    )

    e.page.overlay.append(dialog)  # ✅ الطريقة الجديدة لعرض الـ Dialog
    e.page.update()  # تحديث الصفحة لإضافة الـ Dialog
    e.page.open(dialog)  # ✅ فتح الـ Dialog

def close_dialog(e):
    """ دالة لإغلاق الـ Dialog """
    for control in e.page.overlay:
        if isinstance(control, ft.AlertDialog):
            control.open = False
    e.page.update()  # تحديث الصفحة بعد الإغلاق




# ملف التخزين المحلي
STORAGE_FILE = "requests.json"

def load_requests():
    """ تحميل بيانات الطلبات من الملف """
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_requests(requests):
    """ حفظ بيانات الطلبات إلى الملف """
    with open(STORAGE_FILE, "w") as f:
        json.dump(requests, f, indent=4)

def can_place_order(user_id):
    """ التحقق مما إذا كان المستخدم يمكنه إرسال طلب جديد """
    requests = load_requests()
    now = datetime.now()
    
    # تحديث الطلبات بحذف القديمة (أكثر من 12 ساعة)
    if user_id in requests:
        requests[user_id] = [req for req in requests[user_id] if now - datetime.fromisoformat(req) < timedelta(hours=12)]
    else:
        requests[user_id] = []
    
    save_requests(requests)
    return len(requests[user_id]) < 4, 4 - len(requests[user_id])

def record_request(user_id):
    """ تسجيل طلب جديد للمستخدم """
    requests = load_requests()
    if user_id not in requests:
        requests[user_id] = []
    
    requests[user_id].append(datetime.now().isoformat())
    save_requests(requests)

def View():
    selected_value = ft.Ref[ft.Dropdown]()
    video_link_input = ft.Ref[ft.TextField]()
    button_state = ft.Ref[ft.AnimatedSwitcher]()
    user_id = "user_123"  # يجب تغييرها إلى معرف المستخدم الحقيقي

    def process_video(e):
        """ دالة إرسال الطلب عند الضغط على الزر """
        can_order, remaining_requests = can_place_order(user_id)
        if not can_order:
            e.page.open(ft.SnackBar(content=ft.Text("لقد نفذت المحاولات المجانيه يمكنك العوده مره الاخر بعد 12 ساعه للتجديد 4 اخري" , color=ft.colors.WHITE), bgcolor="red"))  # ✅ الطريقة الجديدة
            e.page.update()
            return
        
        video_url = video_link_input.current.value.strip()
        quantity = selected_value.current.value

        if not video_url:
            e.page.open(ft.SnackBar(content=ft.Text("❌ من فضلك ادخل رابط الفديو"), bgcolor="green"))  # ✅ الطريقة الجديدة
            e.page.update()
            return

        if not quantity:
            e.page.open(ft.SnackBar(content=ft.Text("❌ من فضلك ادخل الكميه"), bgcolor="green"))  # ✅ الطريقة الجديدة
            e.page.update()
            return

        button_state.current.content = ft.ProgressRing(color="white")
        e.page.update()

        # ⏳ إرسال الطلب إلى API (محاكاة استجابة ناجحة)
        response = {"order": "123456"}  # استبدلها بالاستجابة الفعلية

        if "order" in response:
            record_request(user_id)
            success_msg = f"✅ تم إرسال الطلب بنجاح! رقم الطلب: {response['order']} | الطلبات المتبقية: {remaining_requests - 1}"
            e.page.snack_bar = ft.SnackBar(ft.Text(success_msg, color="white"), bgcolor="green")
        else:
            error_msg = "❌ حدث خطأ أثناء الطلب!"
            e.page.snack_bar = ft.SnackBar(ft.Text(error_msg, color="white"), bgcolor="red")
        
        e.page.snack_bar.open = True
        e.page.update()

        button_state.current.content = ft.ElevatedButton(
            "Get Views",
            on_click=process_video,
            bgcolor="#ff0050",
            color="white",
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=10,
                elevation=5
            ),
        )
        e.page.update()

    return ft.View(
        "/View",
        controls=[
            ft.AppBar(
                title=ft.Text("TikTok Free Views", color="white", size=22, weight=ft.FontWeight.BOLD),
                bgcolor="#ff0050",
                center_title=True,
                leading=ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda e: e.page.go('/home')),
            ),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("احصل على مشاهدات تيك توك مجانًا!", size=20, color="white", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                        ft.TextField(ref=video_link_input, label="رابط الفيديو", hint_text="الصق الرابط هنا...", border_color="#ff0050", text_style=ft.TextStyle(color="white"), bgcolor="#282828", border_radius=10),
                        ft.Dropdown(ref=selected_value, label="اختر عدد المشاهدات", hint_text="حدد العدد...", options=[ft.dropdown.Option("1000"), ft.dropdown.Option("5000"), ft.dropdown.Option("10000")], border_color="#ff0050", text_style=ft.TextStyle(color="white"), bgcolor="#282828", border_radius=10),
                        ft.AnimatedSwitcher(ref=button_state, duration=500, transition=ft.AnimatedSwitcherTransition.FADE, content=ft.ElevatedButton("Get Views", on_click=process_video, bgcolor="#ff0050", color="white", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), padding=10, elevation=5))),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15
                ),
                expand=True,
                bgcolor="#181818",
                padding=20
            )
        ]
    )

# التعامل مع الانتقال بين الصفحات
def route_change(page):
    page.views.clear()
    if page.route == "/home":
        page.views.append(home())
    elif page.route == "/View":
        page.views.append(View())
    elif page.route == "/likes":
        page.views.append(likes())
    page.update()

ft.app(target=main)
