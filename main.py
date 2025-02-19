import sqlite3
import flet as ft
import webbrowser
# تعريف التطبيق
def main(page: ft.Page):
    page.title = 'SafePass - إدارة كلمات المرور'
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.full_screen = True
    page.scroll = "auto"

    page.on_route_change = lambda _: route_change(page)
    page.go("/login")  # بدء التطبيق بصفحة تسجيل الدخول

# إنشاء اتصال بقاعدة البيانات
conn = sqlite3.connect('password_list.db', check_same_thread=False)
cursor = conn.cursor()

# إنشاء جدول حفظ كلمات المرور إذا لم يكن موجودًا
cursor.execute('''
    CREATE TABLE IF NOT EXISTS passwords(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        site TEXT NOT NULL,
        username TEXT NOT NULL, 
        password TEXT NOT NULL
    )
''')

# إنشاء جدول الأدمن إذا لم يكن موجودًا
cursor.execute('''
    CREATE TABLE IF NOT EXISTS admin(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL, 
        password TEXT NOT NULL
    )
''')

# إضافة مستخدم الأدمن الافتراضي إذا لم يكن موجودًا
cursor.execute("INSERT OR IGNORE INTO admin (id, name, password) VALUES (1, 'admin', '1234')")
conn.commit()

# دالة عرض رسالة خطأ أو نجاح
def show_snackbar(page, message, color=ft.colors.RED):
    page.snack_bar = ft.SnackBar(
        content=ft.Text(message, color=ft.colors.WHITE),
        bgcolor=color
    )
    page.snack_bar.open = True
    page.update()
def open_whatsapp(e):
    webbrowser.open("https://wa.me/+201552825549")
# AppBar مخصص للصفحات
def custom_app_bar(title, page):
    return ft.AppBar(
        title=ft.Text(title, size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
        center_title=True,
        bgcolor=ft.colors.BLUE_GREY_900,
        leading=ft.IconButton(
                icon=ft.icons.HOME,
                icon_color=ft.colors.WHITE,
                tooltip="الصفحة الرئيسية",
                on_click=lambda e: page.go("/home"),
            ),

        actions=[
            ft.PopupMenuButton(
                icon=ft.icons.MORE_VERT,
                icon_color=ft.colors.WHITE,
                tooltip="المزيد",
                items=[
                    ft.PopupMenuItem(
                        text="تواصل مع المطور احمد",
                        on_click=open_whatsapp
                    ),

                    ft.PopupMenuItem(
                        text="تسجيل الخروج",
                        on_click=lambda e: page.go("/login")
                    ),
                ]
            )
        ]
    )

# شاشة تسجيل الدخول
def login_page(page):
    username_field = ft.TextField(label="اسم المستخدم", prefix_icon=ft.icons.PERSON, width=300)
    password_field = ft.TextField(label="كلمة المرور", prefix_icon=ft.icons.LOCK, password=True, width=300)

    def login(e):
        username = username_field.value.strip()
        password = password_field.value.strip()

        if not username or not password:
            show_snackbar(page, "❌ يرجى إدخال جميع الحقول", ft.colors.ORANGE)
            return

        cursor.execute("SELECT * FROM admin WHERE name = ? AND password = ?", (username, password))
        user = cursor.fetchone()

        if user:
            show_snackbar(page, "✅ تم تسجيل الدخول بنجاح", ft.colors.GREEN)
            page.go("/home")  # الانتقال إلى الصفحة الرئيسية
        else:
            show_snackbar(page, "❌ اسم المستخدم أو كلمة المرور غير صحيحة", ft.colors.RED)

    login_button = ft.ElevatedButton("تسجيل الدخول", on_click=login)

    return ft.View(
        "/login",
        [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("🔐 تسجيل الدخول", size=30, weight=ft.FontWeight.BOLD, text_align="center"),
                        username_field,
                        password_field,
                        login_button
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.center,
                expand=True
            )
        ]
    )

# دالة لحساب الإحصائيات من قاعدة البيانات
def get_statistics():
    cursor.execute("SELECT COUNT(*) FROM passwords")
    total_accounts = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT site) FROM passwords")
    unique_sites = cursor.fetchone()[0]

    return total_accounts, unique_sites

# الصفحة الرئيسية بعد تسجيل الدخول (بتصميم أكثر جاذبية)
def home_page(page):
    total_accounts, unique_sites = get_statistics()

    return ft.View(
        "/home",
        [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("🔒 SafePass - إدارة كلمات المرور", size=30, weight=ft.FontWeight.BOLD, text_align="center", color=ft.colors.BLUE_900),

                        ft.Container(  
                            content=ft.Image("https://blog.1password.com/articles/are-password-managers-safe/header.svg", width=300, height=300),
                            alignment=ft.alignment.center
                        ),

                        ft.Divider(thickness=2, color=ft.colors.BLUE_GREY_300),

                        ft.Text("📊 إحصائيات الحسابات", size=26, weight=ft.FontWeight.BOLD, text_align="center", color=ft.colors.BLACK87),

                        ft.Row(
                            [
                                ft.Card(
                                    content=ft.Container(
                                        content=ft.Column(
                                            [
                                                ft.Icon(ft.icons.LOCK, size=60, color=ft.colors.BLUE),
                                                ft.Text(f"إجمالي الحسابات المخزنة", size=20, weight=ft.FontWeight.BOLD),
                                                ft.Text(f"{total_accounts}", size=25, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900)
                                            ],
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        ),
                                        padding=20
                                    ),
                                    elevation=5
                                ),

                                ft.Card(
                                    content=ft.Container(
                                        content=ft.Column(
                                            [
                                                ft.Icon(ft.icons.LINK, size=60, color=ft.colors.GREEN),
                                                ft.Text(f"عدد المواقع الفريدة", size=20, weight=ft.FontWeight.BOLD),
                                                ft.Text(f"{unique_sites}", size=25, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_900)
                                            ],
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            scroll='auto'
                                        ),
                                        padding=20
                                    ),
                                    elevation=5
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=20,
                            scroll='auto'
                        ),

                        ft.Divider(thickness=2, color=ft.colors.BLUE_GREY_300),

                        ft.ElevatedButton(
                            "📂 إدارة الحسابات",
                            icon=ft.icons.ACCOUNT_BOX,
                            bgcolor=ft.colors.BLUE_700,
                            color=ft.colors.WHITE,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12), elevation=5),
                            on_click=lambda e: page.go("/acount")
                        ),
                    ],
                    spacing=20,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll="auto"  # ← تمكين التمرير داخل العمود
                ),
                alignment=ft.alignment.center,
                expand=True,
                padding=20,
                bgcolor=ft.colors.GREY_100
            )
        ]
    )

# Page لإدارة الحسابات
def acount_page(page):
    page.scroll = "auto"
    
    def load_accounts():
        """تحميل الحسابات من قاعدة البيانات وتحديث الجدول فورًا"""
        cursor.execute("SELECT id, site, username, password FROM passwords")
        accounts = cursor.fetchall()

        account_list.controls.clear()  # تفريغ الجدول لإعادة تحميله
        account_list.controls.append(table_header)  # إضافة العنوان من جديد

        for index, account in enumerate(accounts):
            row_color = ft.colors.GREY_200 if index % 2 == 0 else ft.colors.WHITE

            account_list.controls.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(account[1], width=150),
                            ft.Text(account[2], width=150),
                            ft.Text(account[3], width=150),

                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                icon_color=ft.colors.WHITE,
                                bgcolor=ft.colors.RED_700,
                                tooltip="حذف الحساب",
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), elevation=3),
                                on_click=lambda e, id=account[0]: delete_account(id)
                            ),

                            ft.IconButton(
                                icon=ft.icons.CONTENT_COPY,
                                icon_color=ft.colors.WHITE,
                                bgcolor=ft.colors.BLUE_700,
                                tooltip="نسخ كلمة المرور",
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), elevation=3),
                                on_click=lambda e, pw=account[3]: copy_password(pw)
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        scroll='auto',
                    ),
                    bgcolor=row_color,
                    border_radius=10,
                    padding=8
                )
            )
        
        page.update()  # تحديث الصفحة بعد تحميل البيانات

    # ترويسة الجدول
    table_header = ft.Row(
        [
            ft.Text("🔗 الموقع", weight=ft.FontWeight.BOLD, width=150, color=ft.colors.WHITE),
            ft.Text("👤 اسم المستخدم", weight=ft.FontWeight.BOLD, width=150, color=ft.colors.WHITE),
            ft.Text("🔑 كلمة المرور", weight=ft.FontWeight.BOLD, width=150, color=ft.colors.WHITE),
            ft.Text("🗑️", width=50, color=ft.colors.WHITE),
            ft.Text("📋", width=50, color=ft.colors.WHITE),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10
    )

    account_list = ft.Column([table_header], spacing=5)

    def delete_account(account_id):
        cursor.execute("DELETE FROM passwords WHERE id = ?", (account_id,))
        conn.commit()
        load_accounts()  # تحديث البيانات مباشرة

    site_field = ft.TextField(label="الموقع", width=600)
    username_field = ft.TextField(label="اسم المستخدم", width=600)
    password_field = ft.TextField(label="كلمة المرور", width=600)

    def add_account(e):
        site, username, password = site_field.value.strip(), username_field.value.strip(), password_field.value.strip()

        if not site or not username or not password:
            show_snackbar(page, "❌ جميع الحقول مطلوبة", ft.colors.ORANGE)
            return

        cursor.execute("INSERT INTO passwords (site, username, password) VALUES (?, ?, ?)", (site, username, password))
        conn.commit()
        show_snackbar(page, "✅ تم إضافة الحساب بنجاح", ft.colors.GREEN)

        site_field.value = username_field.value = password_field.value = ""  # مسح الحقول بعد الإدخال
        page.update()
        load_accounts()  # تحديث الجدول مباشرة

    def copy_password(password):
        page.set_clipboard(password)
        show_snackbar(page, "✅ تم نسخ كلمة المرور بنجاح", ft.colors.BLUE)

    # تحميل البيانات عند فتح الصفحة
    load_accounts()

    return ft.View(
        "/acount",
        [
            custom_app_bar("📂 إدارة الحسابات", page),  # إضافة الــ App Bar هنا
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("➕ إضافة حساب جديد", size=20, weight=ft.FontWeight.BOLD),
                        site_field, username_field, password_field,

                        ft.ElevatedButton(
                            "إضافة الحساب",
                            icon=ft.icons.ADD,
                            bgcolor=ft.colors.GREEN_700,
                            color=ft.colors.WHITE,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), elevation=5),
                            on_click=add_account
                        ),

                        ft.Divider(thickness=3),

                        ft.Text("📂 إدارة الحسابات", size=24, weight=ft.FontWeight.BOLD, text_align="center"),
                        
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Container(
                                        content=table_header,
                                        bgcolor=ft.colors.BLUE_GREY_700,
                                        border_radius=10,
                                        padding=10
                                    ),
                                    ft.Container(
                                        content=account_list,
                                        border=ft.border.all(1, ft.colors.GREY_400),
                                        border_radius=10,
                                        padding=10,
                                        bgcolor=ft.colors.GREY_100,
                                        shadow=ft.BoxShadow(blur_radius=5, spread_radius=1, color=ft.colors.GREY_400)
                                    )
                                ],
                                spacing=10
                            ),
                            padding=15,
                            alignment=ft.alignment.center
                        ),

                        ft.Divider(thickness=3),
                    ],
                    spacing=20,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll='auto'
                ),
                alignment=ft.alignment.center,
                expand=True
            )
        ]
    )
def about_page(page):

    return ft.View(
        "/acount",
        [
            custom_app_bar("📂 إدارة الحسابات", page),  # إضافة الــ App Bar هنا
            ft.Column(
                    [
                        # بطاقة تعريف المطور
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.CircleAvatar(
                                        content=ft.Image(src="https://www.pcworld.com/wp-content/uploads/2024/03/shutterstock_2268386621.jpg?resize=1024%2C576&quality=50&strip=all" , border_radius=60),  # استبدلها بصورتك
                                        radius=60,
                                        bgcolor=ft.colors.BLUE_GREY_800,
                                    ),
                                    ft.Text("أحمد - مطور برمجيات", 
                                            size=22, weight=ft.FontWeight.BOLD, 
                                            color=ft.colors.WHITE, text_align=ft.TextAlign.CENTER),
                                    ft.Text("متخصص في تطوير تطبيقات بايثون و Flet، وأعشق بناء الأنظمة المتكاملة! 🚀", 
                                            size=14, color=ft.colors.WHITE70, 
                                            text_align=ft.TextAlign.CENTER),
                                ],
                                spacing=10,
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                            padding=ft.padding.all(20),
                            width=350,
                            border_radius=20,
                            shadow=ft.BoxShadow(blur_radius=10, spread_radius=1, color=ft.colors.WHITE10),
                            bgcolor=ft.colors.BLUE_GREY_900
                        ),

                        # أزرار التواصل الاجتماعي
                        ft.Row(
                            [
                                ft.IconButton(
                                    icon=ft.icons.GET_APP, icon_color=ft.colors.GREEN,
                                    tooltip="تواصل عبر واتساب",
                                    icon_size=30,
                                    on_click=lambda e: open_link("https://wa.me/+201552825549")
                                ),
                                ft.IconButton(
                                    icon=ft.icons.TELEGRAM, icon_color=ft.colors.BLUE,
                                    tooltip="تواصل عبر تيليجرام",
                                    icon_size=30,
                                    on_click=lambda e: open_link("https://t.me/")
                                ),
                                ft.IconButton(
                                    icon=ft.icons.EMAIL, icon_color=ft.colors.RED,
                                    tooltip="راسلني عبر البريد",
                                    icon_size=30,
                                    on_click=lambda e: open_link("mailto:ahmedsmmeg@gmail.com")
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=15
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20
            )
        ]
    )

def open_link(url):
    webbrowser.open(url)


# التعامل مع الانتقال بين الصفحات
def route_change(page):
    page.views.clear()
    if page.route == "/login":
        page.views.append(login_page(page))
    elif page.route == "/home":
        page.views.append(home_page(page))
    elif page.route == "/acount":
        page.views.append(acount_page(page))
    elif page.route == "/about":
        page.views.append(about_page(page))
    page.update()

# تشغيل التطبيق
ft.app(target=main)
