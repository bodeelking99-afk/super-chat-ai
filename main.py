import flet as ft
import urllib.request
import urllib.parse
import threading
import html


def ask_ai(prompt: str) -> str:
    safe_prompt = html.escape(prompt, quote=True)
    system_prompt = (
        "أنت مساعد ذكي ومفيد، وعاوز تجاوب بشكل عربي واضح ومريح، "
        "بأسلوب مصري لطيف وودود، بدون أي أخطاء إملائية، "
        f"والسؤال هو: {safe_prompt}"
    )
    encoded = urllib.parse.quote(system_prompt)
    url = f"https://text.pollinations.ai/{encoded}"
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "text/plain, */*",
            },
        )
        with urllib.request.urlopen(req, timeout=60) as response:
            return response.read().decode("utf-8", errors="replace").strip()
    except Exception:
        return "معلش يا زميلي، فيه مشكل�� في الاتصال، حاول مرة تانية بعد شويه."


def create_message_bubble(text: str, sender: str, is_user: bool):
    bg_color = ft.colors.RED_700 if is_user else ft.colors.BLACK
    align = ft.MainAxisAlignment.END if is_user else ft.MainAxisAlignment.START
    text_color = ft.colors.WHITE

    return ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    sender,
                    size=11,
                    weight=ft.FontWeight.BOLD,
                    color=ft.colors.WHITE70,
                ),
                ft.Text(
                    text,
                    selectable=True,
                    color=text_color,
                    size=14,
                    weight=ft.FontWeight.W_500,
                    max_lines=50,
                    overflow=ft.TextOverflow.VISIBLE,
                    spans=[],
                ),
            ],
            tight=True,
            spacing=4,
        ),
        padding=12,
        border_radius=14,
        bgcolor=bg_color,
        width=650,
        alignment=ft.alignment.center_left if not is_user else ft.alignment.center_right,
        margin=ft.Margin(0, 6, 0, 6),
        border=ft.border.all(1, ft.colors.WHITE24),
    )


def main(page: ft.Page):
    page.title = "Super Chat AI"
    page.bgcolor = "#1E0205"
    page.padding = 12
    page.window_width = 430
    page.window_height = 800
    page.vertical_alignment = ft.MainAxisAlignment.START

    page.theme = ft.Theme(color_scheme_seed="#F8012F")
    page.update()

    app_title = ft.Row(
        [
            ft.Text("⚡", size=34),
            ft.Text("Super Chat AI", size=26, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    chat_column = ft.Column(spacing=8, expand=True)
    chat_scroll = ft.ScrollMode.AUTO

    welcome = create_message_bubble(
        "أهلاً بيك! أنا Super Chat AI، تقدر تسألني أي حاجة وعاوز أجاوبك بسرعة وبلُغة حلوة ومريحة. 😎",
        "AI",
        False,
    )
    chat_column.controls.append(welcome)

    status_text = ft.Text("جاهز للاستقبال", color=ft.colors.GREEN_200, size=12)
    status_row = ft.Row([ft.Icon(ft.icons.CIRCLE, color=ft.colors.GREEN_300, size=12), status_text])

    input_field = ft.TextField(
        hint_text="اكتب سؤالك هنا...",
        expand=True,
        bgcolor="#2A060A",
        border_color="#FF4D4D",
        text_style=ft.TextStyle(color=ft.colors.WHITE),
        hint_style=ft.TextStyle(color=ft.colors.WHITE70),
        value="",
        on_submit=lambda e: None,
    )

    loading = ft.Row(
        [
            ft.ProgressRing(width=18, height=18, stroke_width=2, color=ft.colors.WHITE),
            ft.Text("جارٍ تجهيز الرد...", color=ft.colors.WHITE, size=12),
        ],
        visible=False,
        spacing=10,
    )

    def append_user_message(text: str):
        chat_column.controls.append(create_message_bubble(text, "أنت", True))
        page.update()

    def append_ai_message(text: str):
        chat_column.controls.append(create_message_bubble(text, "AI", False))
        page.update()

    def set_loading(is_loading: bool):
        loading.visible = is_loading
        page.update()

    def send_message(e):
        text = input_field.value.strip()
        if not text:
            return

        append_user_message(text)
        input_field.value = ""
        set_loading(True)
        page.update()

        def worker():
            reply = ask_ai(text)
            page.run_task(lambda: _show_reply(reply))

        def _show_reply(reply: str):
            set_loading(False)
            append_ai_message(reply)
            page.scroll_to(end=True)
            page.update()

        threading.Thread(target=worker, daemon=True).start()

    send_button = ft.ElevatedButton(
        "إرسال",
        on_click=send_message,
        icon=ft.icons.SEND,
        bgcolor="#D90429",
        color=ft.colors.WHITE,
        height=50,
    )

    clear_button = ft.OutlinedButton(
        "مسح",
        on_click=lambda e: (
            chat_column.controls.clear(),
            chat_column.controls.append(create_message_bubble("تم مسح المحادثة. ابدأ سؤال جديد!", "AI", False)),
            page.update(),
        ),
        icon=ft.icons.DELETE_SWEEP_ROUNDED,
        fg_color=ft.colors.WHITE,
        border_color=ft.colors.WHITE24,
    )

    input_row = ft.Row([
        input_field,
        send_button,
    ], expand=True, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    controls_row = ft.Row([
        clear_button,
    ], alignment=ft.MainAxisAlignment.END)

    chat_panel = ft.Container(
        content=ft.Column([
            app_title,
            status_row,
            ft.Container(
                content=ft.Column(chat_column.controls, expand=True, scroll=ft.ScrollMode.AUTO),
                bgcolor="#2A060A",
                padding=12,
                border_radius=18,
                border=ft.border.all(1, "#FF4D4D"),
                expand=True,
                height=560,
            ),
            loading,
            input_row,
            controls_row,
        ], spacing=12, expand=True),
        expand=True,
    )

    page.add(chat_panel)
    page.update()


if __name__ == "__main__":
    ft.app(target=main)
