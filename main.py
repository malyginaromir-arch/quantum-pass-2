import flet as ft
import secrets 
import string
import time
import datetime

def main(page: ft.Page):
    page.title = "Y&W QUANTUM CORE AI"
    page.bgcolor = "#0D0D0D"
    page.theme_mode = "dark"
    page.padding = 15

    result_field = ft.Text("ОЖИДАНИЕ КОМАНДЫ...", size=15, color="#555555", weight="bold", selectable=True)
    log_list = ft.Column(spacing=2, scroll="auto")
    
    def add_log(msg):
        t = datetime.datetime.now().strftime("%H:%M:%S")
        log_list.controls.insert(0, ft.Text(f">>{t} {msg}", color="#555555", size=10))
        page.update()

    len_slider = ft.Slider(min=8, max=32, value=16, divisions=24, label="{value} симв.")
    chk_letters = ft.Checkbox(label="БУКВЫ (A-z)", value=True)
    chk_numbers = ft.Checkbox(label="ЦИФРЫ (0-9)", value=True)
    chk_spec = ft.Checkbox(label="СПЕЦСИМВОЛЫ", value=True)

    def apply_preset(e):
        site = preset_dropdown.value
        if site == "Google":
            len_slider.value = 12
            chk_letters.value = True
            chk_numbers.value = True
            chk_spec.value = False
            add_log("ПРОТОКОЛ: Google (12 знаков, без спецзнаков)")
        elif site == "Apple ID":
            len_slider.value = 12
            chk_letters.value = True
            chk_numbers.value = True
            chk_spec.value = False
            add_log("ПРОТОКОЛ: Apple ID (Буквы + Цифры)")
        elif site == "Microsoft":
            len_slider.value = 16
            chk_letters.value = True
            chk_numbers.value = True
            chk_spec.value = True
            add_log("ПРОТОКОЛ: Microsoft (Повышенная сложность)")
        elif site == "Банки (Max Sec)":
            len_slider.value = 24
            chk_letters.value = True
            chk_numbers.value = True
            chk_spec.value = True
            add_log("ПРОТОКОЛ: Банк (Максимальная защита)")
        else:
            add_log("ПРОТОКОЛ: Ручные настройки")
        page.update()

    preset_dropdown = ft.Dropdown(
        label="СТАНДАРТЫ БЕЗОПАСНОСТИ",
        options=[
            ft.dropdown.Option("Свой вариант"),
            ft.dropdown.Option("Google"),
            ft.dropdown.Option("Apple ID"),
            ft.dropdown.Option("Microsoft"),
            ft.dropdown.Option("Банки (Max Sec)"),
        ],
        value="Свой вариант"
    )
    preset_dropdown.on_change = apply_preset

    btn_gen = ft.ElevatedButton(
        content=ft.Text("ЗАПУСТИТЬ ИИ-ГЕНЕРАЦИЮ", color="black", weight="bold"),
        bgcolor="#00FF41",
        height=50
    )
    
    def generate_hard_password(e):
        result_field.value = "АНАЛИЗ ТРЕБОВАНИЙ..."
        result_field.color = "#FDDA0D"
        btn_gen.disabled = True
        page.update()
        time.sleep(0.8)

        length = int(len_slider.value)
        chars = ""
        if chk_letters.value: chars += string.ascii_letters
        if chk_numbers.value: chars += string.digits
        if chk_spec.value: chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"

        if not chars:
            result_field.value = "ОШИБКА: НЕТ СИМВОЛОВ"
            result_field.color = "red"
            btn_gen.disabled = False
            page.update()
            return

        password = "".join(secrets.choice(chars) for _ in range(length))
        result_field.value = password
        result_field.color = "#00FF41"
        btn_gen.disabled = False
        add_log(f"УСПЕХ: Ключ ({preset_dropdown.value})")
        page.update()

    btn_gen.on_click = generate_hard_password

    def copy_pass(e):
        if result_field.value and "..." not in result_field.value:
            page.set_clipboard(result_field.value)
            add_log("СИСТЕМА: Ключ скопирован")
            
    btn_copy = ft.FilledButton(
        content=ft.Text("СКОПИРОВАТЬ КЛЮЧ", color="black", weight="bold"),
        bgcolor="#00FF41",
        on_click=copy_pass
    )

    page.add(
        ft.Text("QUANTUM CORE AI", size=24, weight="bold", color="#00FF41"),
        ft.Divider(height=10, color="transparent"),
        preset_dropdown,
        ft.Divider(height=10, color="transparent"),
        ft.Container(
            content=result_field, 
            bgcolor="#111111", padding=12, border_radius=8, 
            border=ft.Border(top=ft.BorderSide(1, "#00FF41"), bottom=ft.BorderSide(1, "#00FF41"), left=ft.BorderSide(1, "#00FF41"), right=ft.BorderSide(1, "#00FF41"))
        ),
        btn_copy,
        ft.Divider(height=10, color="transparent"),
        len_slider,
        ft.Row([chk_letters, chk_numbers, chk_spec], wrap=True),
        ft.Divider(height=10, color="transparent"),
        btn_gen,
        ft.Divider(height=10, color="transparent"),
        ft.Container(
            content=log_list, 
            bgcolor="#050505", padding=10, border_radius=5, height=100, 
            border=ft.Border(top=ft.BorderSide(1, "#222222"), bottom=ft.BorderSide(1, "#222222"), left=ft.BorderSide(1, "#222222"), right=ft.BorderSide(1, "#222222"))
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
