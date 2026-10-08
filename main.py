import flet as ft
import urllib.request
import urllib.parse
import threading


def ask_ai(prompt):
    system_prompt = (
        "جاوب على السؤال التالي بلغة مصرية شعبية جدعة جداً "
        "وبأسلوب فرفوش وأخوي من الشارع المصري وبدون أخطاء إملائية: "
        f"{prompt}"
    )
    url = f"https://text.pollinations.ai/{urllib.parse.quote(system_prompt)}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=60)
        return response.read().decode('utf-8')
    except Exception:
        return "معلش يا زميلي، حصلت مشكلة في النت عندي، جرب تاني كده!"


def main(page: ft.Page):
    page.title = "Super Chat AI"
    page.bgcolor = "#8B0000"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 15

    logo_row = ft.Row(
        [
            ft.Text("⚡", size=42, color=ft.colors.BLACK),
            ft.Text("A", size=58, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
            ft.Text("Super Chat AI", size=22, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    chat_list = ft.ListView(expand=True, spacing=12, padding=10, auto_scroll=True)

    chat_list.controls.append(
        ft.Container(
            content=ft.Text(
                "Super Chat AI:\nأهلاً بك يا زميلي! أنا معاك وعلى أتم استعداد أرد على أي سؤال في العالم على الرايق.. اؤمرني! 😎",
                color=ft.colors.WHITE,
                size=14,
            ),
            bg_color="#5C0A10",
            padding=12,
            border_radius=12,
            border=ft.border.all(1, "#FF6B6B"),
        )
    )

    user_input = ft.TextField(
        hint_text="اكتب سؤالك هنا يا زميلي...",
        expand=True,
        border_color="#FF4D4D",
        bg_color="#2B0508",
        text_color=ft.colors.WHITE,
        border_radius=12,
    )

    def send_click(e):
        text = user_input.value.strip()
        if not text:
            return

        chat_list.controls.append(
            ft.Container(
                content=ft.Text(f"أنت:\n{text}", color=ft.colors.WHITE, size=14, weight=ft.FontWeight.BOLD),
                bg_color="#D90429",
                padding=12,
                border_radius=12,
                alignment=ft.alignment.center_right,
            )
        )
        user_input.value = ""
        page.update()

        def fetch_reply():
            reply = ask_ai(text)
            chat_list.controls.append(
                ft.Container(
                    content=ft.Text(f"Super Chat AI:\n{reply}", color=ft.colors.WHITE, size=14),
                    bg_color="#5C0A10",
                    padding=12,
                    border_radius=12,
                    border=ft.border.all(1, "#FF6B6B"),
                )
            )
            page.update()

        threading.Thread(target=fetch_reply, daemon=True).start()

    send_btn = ft.ElevatedButton(
        "إرسال ⚡",
        on_click=send_click,
        bgcolor=ft.colors.BLACK,
        color=ft.colors.WHITE,
        height=48,
    )

    chat_container = ft.Container(
        content=chat_list,
        bg_color="#3A080C",
        border_radius=18,
        padding=10,
        expand=True,
        border=ft.border.all(2, "#FF4D4D"),
    )

    input_row = ft.Row([user_input, send_btn])
    page.add(logo_row, chat_container, input_row)


if __name__ == "__main__":
    ft.app(target=main)
