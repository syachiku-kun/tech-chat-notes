"""デスクトップアプリの起動口。"""

import customtkinter


def create_main_window() -> customtkinter.CTk:
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


def main() -> None:
    """アプリを起動し、ウィンドウを閉じるまで画面処理を続ける。"""
    # DB準備
    # apply_migrations(sqlite_path)
    # sqlite_repository = SqliteRepository(sqlite_path)
    # lancedb_repository = LanceDbRepository(lancedb_path)

    # BE準備
    # services = create_application_services(
    #     sqlite_repository=sqlite_repository,
    #     lancedb_repository=lancedb_repository,
    # )

    # FE と BE の境界部分
    # api = create_local_api(services)
    # api.start()

    # FE
    window = create_main_window()
    # configure_views(window, api_client)

    # 定期処理起動
    # scheduler = create_scheduler(services)
    # scheduler.start()

    window.mainloop()

    # 停止
    # scheduler.stop()
    # api.stop()
    # sqlite_repository.close()


if __name__ == "__main__":
    main()
