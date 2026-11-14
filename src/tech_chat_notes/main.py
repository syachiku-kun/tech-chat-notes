"""デスクトップアプリの起動口。"""

import customtkinter


def main() -> None:
    """開発用のメインウィンドウを表示する。"""
    window = customtkinter.CTk()
    window.title("tech-chat-notes")
    window.geometry("800x600")

    message = customtkinter.CTkLabel(
        window,
        text="tech-chat-notes の開発用起動画面",
    )
    message.pack(expand=True)
    window.mainloop()


if __name__ == "__main__":
    main()
