import re
import secrets
import string
import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk


MIN_LENGTH = 7
MAX_LENGTH = 72
SYMBOLS = "!@#$%^&*()=-+[]{}|"

BG_COLOR = "#0f172a"
CARD_COLOR = "#1e293b"
ACCENT_COLOR = "#06b6d4"
ACCENT_HOVER = "#0891b2"
TEXT_PRIMARY = "#e2e8f0"
TEXT_MUTED = "#94a3b8"
ENTRY_BG = "#0b1220"
FONT_FAMILY = "DejaVu Sans"

I18N = {
    "es": {
        "app_title": "Generador de Passwords",
        "language": "Idioma",
        "headline": "Generador de Passwords",
        "subtitle": "Configura opciones, genera y copia en un clic.",
        "length": "Longitud:",
        "include_chars": "Incluye estos caracteres:",
        "lower": "Minusculas (a-z)",
        "upper": "Mayusculas (A-Z)",
        "digits": "Digitos (0-9)",
        "symbols": "Simbolos (!@#...)",
        "generate": "Generar Password",
        "show_password": "Mostrar password",
        "copy": "Copiar al portapapeles",
        "copied": "Copiada",
        "strength_prefix": "Nivel",
        "strength_very_weak": "Muy debil",
        "strength_weak": "Debil",
        "strength_medium": "Media",
        "strength_strong": "Fuerte",
        "strength_very_strong": "Muy fuerte",
        "warn_title": "Aviso",
        "error_title": "Error",
        "warn_select_chars": "Debes habilitar al menos un tipo de caracter.",
        "warn_generate_first": "Primero genera una password.",
        "error_generate": "No se pudo generar la password",
        "error_copy": "No se pudo copiar",
    },
    "en": {
        "app_title": "Password Generator",
        "language": "Language",
        "headline": "Password Generator",
        "subtitle": "Pick options, generate, and copy in one click.",
        "length": "Length:",
        "include_chars": "Include these characters:",
        "lower": "Lowercase (a-z)",
        "upper": "Uppercase (A-Z)",
        "digits": "Digits (0-9)",
        "symbols": "Symbols (!@#...)",
        "generate": "Generate Password",
        "show_password": "Show password",
        "copy": "Copy to clipboard",
        "copied": "Copied",
        "strength_prefix": "Strength",
        "strength_very_weak": "Very weak",
        "strength_weak": "Weak",
        "strength_medium": "Medium",
        "strength_strong": "Strong",
        "strength_very_strong": "Very strong",
        "warn_title": "Warning",
        "error_title": "Error",
        "warn_select_chars": "You must enable at least one character type.",
        "warn_generate_first": "Generate a password first.",
        "error_generate": "Could not generate password",
        "error_copy": "Could not copy",
    },
}


def generate_password(
    length=16,
    use_lowercase=True,
    use_uppercase=True,
    use_digits=True,
    use_symbols=False,
):
    pool = ""

    if use_lowercase:
        pool += string.ascii_lowercase
    if use_uppercase:
        pool += string.ascii_uppercase
    if use_digits:
        pool += string.digits
    if use_symbols:
        pool += SYMBOLS

    if not pool:
        raise ValueError("no_charset_selected")

    return "".join(secrets.choice(pool) for _ in range(length))


def evaluate_password_strength(password):
    if not password:
        return 0, "very_weak", "#ef4444"

    score = 0
    length = len(password)

    if length >= 8:
        score += 20
    if length >= 12:
        score += 20
    if length >= 16:
        score += 20

    if re.search(r"[a-z]", password):
        score += 10
    if re.search(r"[A-Z]", password):
        score += 10
    if re.search(r"\d", password):
        score += 10
    if re.search(r"[^A-Za-z0-9]", password):
        score += 10

    score = min(score, 100)

    if score < 40:
        return score, "weak", "#ef4444"
    if score < 70:
        return score, "medium", "#f59e0b"
    if score < 90:
        return score, "strong", "#22c55e"
    return score, "very_strong", "#10b981"


class PasswordGeneratorApp:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.geometry("620x760")
        self.root.minsize(520, 620)
        self.root.resizable(False, False)
        self.root.configure(fg_color=BG_COLOR)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.language_var = tk.StringVar(value="es")
        self.length_var = tk.StringVar(value="16")
        self.length_slider_var = tk.DoubleVar(value=16)
        self.lower_var = tk.BooleanVar(value=True)
        self.upper_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=False)
        self.show_password_var = tk.BooleanVar(value=False)
        self.password_var = tk.StringVar(value="")
        self.strength_text_var = tk.StringVar(value="")

        self._build_ui()
        self._apply_language()
        self.password_var.trace_add("write", self._update_strength_ui)

    def _tr(self, key):
        lang = self.language_var.get()
        return I18N.get(lang, I18N["es"]).get(key, key)

    def _build_ui(self):
        frame = ctk.CTkFrame(
            self.root,
            fg_color=CARD_COLOR,
            corner_radius=16,
            border_width=1,
            border_color="#334155",
        )
        frame.grid(row=0, column=0, sticky="nsew", padx=18, pady=18)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        inner = ctk.CTkFrame(frame, fg_color="transparent")
        inner.grid(row=0, column=0, padx=16, pady=16, sticky="nsew")
        inner.grid_columnconfigure(1, weight=1)

        self.language_label = ctk.CTkLabel(
            inner,
            text="",
            font=(FONT_FAMILY, 11),
            text_color=TEXT_MUTED,
        )
        self.language_label.grid(row=0, column=0, sticky="w", pady=(0, 4))

        self.language_buttons_frame = ctk.CTkFrame(inner, fg_color="transparent")
        self.language_buttons_frame.grid(row=0, column=1, sticky="e", pady=(0, 4))

        self.language_es_button = ctk.CTkButton(
            self.language_buttons_frame,
            text="ES",
            width=42,
            height=28,
            command=lambda: self._set_language("es"),
            font=(FONT_FAMILY, 11, "bold"),
        )
        self.language_es_button.grid(row=0, column=0, padx=(0, 6))

        self.language_en_button = ctk.CTkButton(
            self.language_buttons_frame,
            text="EN",
            width=42,
            height=28,
            command=lambda: self._set_language("en"),
            font=(FONT_FAMILY, 11, "bold"),
        )
        self.language_en_button.grid(row=0, column=1)

        self.headline_label = ctk.CTkLabel(
            inner,
            text="",
            font=(FONT_FAMILY, 24, "bold"),
            text_color=TEXT_PRIMARY,
            wraplength=520,
            justify="left",
        )
        self.headline_label.grid(row=1, column=0, columnspan=2, pady=(0, 12), sticky="w")

        self.subtitle_label = ctk.CTkLabel(
            inner,
            text="",
            font=(FONT_FAMILY, 12),
            text_color=TEXT_MUTED,
            wraplength=520,
            justify="left",
        )
        self.subtitle_label.grid(row=2, column=0, columnspan=2, pady=(0, 18), sticky="w")

        self.length_label = ctk.CTkLabel(
            inner,
            text="",
            font=(FONT_FAMILY, 13),
            text_color=TEXT_PRIMARY,
        )
        self.length_label.grid(row=3, column=0, sticky="w", pady=4)
        ctk.CTkEntry(
            inner,
            textvariable=self.length_var,
            width=90,
            fg_color=ENTRY_BG,
            border_color="#334155",
            text_color=TEXT_PRIMARY,
            justify="center",
            font=(FONT_FAMILY, 13),
        ).grid(row=3, column=1, sticky="w", pady=4)

        self.length_slider = ctk.CTkSlider(
            inner,
            from_=MIN_LENGTH,
            to=MAX_LENGTH,
            number_of_steps=MAX_LENGTH - MIN_LENGTH,
            variable=self.length_slider_var,
            command=self._on_slider_change,
            progress_color=ACCENT_COLOR,
            button_color=ACCENT_COLOR,
            button_hover_color=ACCENT_HOVER,
            fg_color=ENTRY_BG,
        )
        self.length_slider.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(4, 12))

        self.include_label = ctk.CTkLabel(
            inner,
            text="",
            font=(FONT_FAMILY, 12),
            text_color=TEXT_MUTED,
        )
        self.include_label.grid(row=5, column=0, columnspan=2, sticky="w", pady=(4, 6))

        self.lower_check = ctk.CTkCheckBox(
            inner,
            text="",
            variable=self.lower_var,
            text_color=TEXT_PRIMARY,
            fg_color=ACCENT_COLOR,
            hover_color=ACCENT_HOVER,
            font=(FONT_FAMILY, 12),
        )
        self.lower_check.grid(row=6, column=0, columnspan=2, sticky="w", pady=2)

        self.upper_check = ctk.CTkCheckBox(
            inner,
            text="",
            variable=self.upper_var,
            text_color=TEXT_PRIMARY,
            fg_color=ACCENT_COLOR,
            hover_color=ACCENT_HOVER,
            font=(FONT_FAMILY, 12),
        )
        self.upper_check.grid(row=7, column=0, columnspan=2, sticky="w", pady=2)

        self.digits_check = ctk.CTkCheckBox(
            inner,
            text="",
            variable=self.digits_var,
            text_color=TEXT_PRIMARY,
            fg_color=ACCENT_COLOR,
            hover_color=ACCENT_HOVER,
            font=(FONT_FAMILY, 12),
        )
        self.digits_check.grid(row=8, column=0, columnspan=2, sticky="w", pady=2)

        self.symbols_check = ctk.CTkCheckBox(
            inner,
            text="",
            variable=self.symbols_var,
            text_color=TEXT_PRIMARY,
            fg_color=ACCENT_COLOR,
            hover_color=ACCENT_HOVER,
            font=(FONT_FAMILY, 12),
        )
        self.symbols_check.grid(row=9, column=0, columnspan=2, sticky="w", pady=2)

        self.generate_button = ctk.CTkButton(
            inner,
            text="",
            command=self.on_generate,
            fg_color=ACCENT_COLOR,
            hover_color=ACCENT_HOVER,
            text_color="#082f49",
            font=(FONT_FAMILY, 13, "bold"),
            height=40,
        )
        self.generate_button.grid(row=10, column=0, columnspan=2, pady=(16, 10), sticky="ew")

        self.password_entry = ctk.CTkEntry(
            inner,
            textvariable=self.password_var,
            width=380,
            justify="center",
            fg_color=ENTRY_BG,
            border_color="#334155",
            text_color=TEXT_PRIMARY,
            font=(FONT_FAMILY, 14),
            height=40,
            show="*",
        )
        self.password_entry.grid(row=11, column=0, columnspan=2, pady=6, sticky="ew")

        self.show_password_check = ctk.CTkCheckBox(
            inner,
            text="",
            variable=self.show_password_var,
            command=self._toggle_password_visibility,
            text_color=TEXT_MUTED,
            fg_color=ACCENT_COLOR,
            hover_color=ACCENT_HOVER,
            font=(FONT_FAMILY, 11),
        )
        self.show_password_check.grid(row=12, column=0, columnspan=2, sticky="w", pady=(0, 6))

        self.strength_label = ctk.CTkLabel(
            inner,
            textvariable=self.strength_text_var,
            font=(FONT_FAMILY, 12),
            text_color=TEXT_PRIMARY,
        )
        self.strength_label.grid(row=13, column=0, columnspan=2, sticky="w", pady=(4, 2))

        self.strength_bar = ctk.CTkProgressBar(
            inner,
            progress_color="#22c55e",
            fg_color=ENTRY_BG,
            height=14,
        )
        self.strength_bar.set(0)
        self.strength_bar.grid(row=14, column=0, columnspan=2, sticky="ew", pady=(0, 12))

        self.copy_button = ctk.CTkButton(
            inner,
            text="",
            command=self.on_copy,
            fg_color="#334155",
            hover_color="#475569",
            text_color=TEXT_PRIMARY,
            font=(FONT_FAMILY, 12),
            height=36,
        )
        self.copy_button.grid(row=15, column=0, columnspan=2, pady=(2, 0), sticky="ew")

        self.length_var.trace_add("write", self._sync_slider_from_length)

    def _apply_language(self):
        self.root.title(self._tr("app_title"))
        self.language_label.configure(text=self._tr("language"))
        self.headline_label.configure(text=self._tr("headline"))
        self.subtitle_label.configure(text=self._tr("subtitle"))
        self.length_label.configure(text=self._tr("length"))
        self.include_label.configure(text=self._tr("include_chars"))
        self.lower_check.configure(text=self._tr("lower"))
        self.upper_check.configure(text=self._tr("upper"))
        self.digits_check.configure(text=self._tr("digits"))
        self.symbols_check.configure(text=self._tr("symbols"))
        self.generate_button.configure(text=self._tr("generate"))
        self.show_password_check.configure(text=self._tr("show_password"))
        self.copy_button.configure(text=self._tr("copy"))
        self._update_language_buttons_style()
        self._update_strength_ui()

    def _set_language(self, lang):
        self.language_var.set(lang)
        self._apply_language()

    def _update_language_buttons_style(self):
        active_lang = self.language_var.get()
        if active_lang == "es":
            self.language_es_button.configure(
                fg_color=ACCENT_COLOR,
                hover_color=ACCENT_HOVER,
                text_color="#082f49",
            )
            self.language_en_button.configure(
                fg_color="#334155",
                hover_color="#475569",
                text_color=TEXT_PRIMARY,
            )
        else:
            self.language_en_button.configure(
                fg_color=ACCENT_COLOR,
                hover_color=ACCENT_HOVER,
                text_color="#082f49",
            )
            self.language_es_button.configure(
                fg_color="#334155",
                hover_color="#475569",
                text_color=TEXT_PRIMARY,
            )

    def _update_strength_ui(self, *_):
        pwd = self.password_var.get()
        score, strength_key, color = evaluate_password_strength(pwd)
        label = self._tr(f"strength_{strength_key}")
        self.strength_text_var.set(f"{self._tr('strength_prefix')}: {label} ({score}%)")
        self.strength_bar.set(score / 100)
        self.strength_bar.configure(progress_color=color)
        self.strength_label.configure(text_color=color)

    def _on_slider_change(self, value):
        self.length_var.set(str(round(value)))

    def _sync_slider_from_length(self, *_):
        raw = self.length_var.get().strip()
        if not raw.isdigit():
            return
        value = int(raw)
        value = max(MIN_LENGTH, min(MAX_LENGTH, value))
        if round(self.length_slider_var.get()) != value:
            self.length_slider_var.set(value)

    def _toggle_password_visibility(self):
        if self.show_password_var.get():
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="*")

    def _parse_length(self):
        raw = self.length_var.get().strip()
        try:
            length = int(raw)
        except ValueError:
            length = 16
        length = max(length, MIN_LENGTH)
        length = min(length, MAX_LENGTH)
        self.length_var.set(str(length))
        self.length_slider_var.set(length)
        return length

    def on_generate(self):
        try:
            length = self._parse_length()
            pwd = generate_password(
                length=length,
                use_lowercase=self.lower_var.get(),
                use_uppercase=self.upper_var.get(),
                use_digits=self.digits_var.get(),
                use_symbols=self.symbols_var.get(),
            )
            self.password_var.set(pwd)
            self._update_strength_ui()
        except ValueError as err:
            if str(err) == "no_charset_selected":
                messagebox.showwarning(self._tr("warn_title"), self._tr("warn_select_chars"))
            else:
                messagebox.showwarning(self._tr("warn_title"), str(err))
        except Exception as err:
            messagebox.showerror(self._tr("error_title"), f"{self._tr('error_generate')}: {err}")

    def on_copy(self):
        pwd = self.password_var.get().strip()
        if not pwd:
            messagebox.showwarning(self._tr("warn_title"), self._tr("warn_generate_first"))
            return

        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(pwd)
            self.root.update()
            self.copy_button.configure(text=self._tr("copied"))
            self.root.after(1200, lambda: self.copy_button.configure(text=self._tr("copy")))
        except Exception as err:
            messagebox.showerror(self._tr("error_title"), f"{self._tr('error_copy')}: {err}")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    PasswordGeneratorApp().run()