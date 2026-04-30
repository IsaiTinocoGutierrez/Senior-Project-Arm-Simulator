import tkinter as tk


class SidePanel:
    def __init__(self, root, reset_callback):
        self.root = root

        self.status_label = tk.Label(
            root,
            text="Your turn: click a piece, then click destination.",
            font=("Arial", 12),
        )
        self.status_label.grid(row=0, column=0, columnspan=8, pady=10)

        self.reset_button = tk.Button(
            root,
            text="Reset Game",
            font=("Arial", 12),
            command=reset_callback,
        )
        self.reset_button.grid(row=1, column=8, rowspan=2, padx=10)

        self.captured_white_label = tk.Label(
            root,
            text="Captured White: ",
            font=("Arial", 12),
            anchor="w",
            justify="left",
        )
        self.captured_white_label.grid(row=3, column=8, padx=10, sticky="nw")

        self.captured_black_label = tk.Label(
            root,
            text="Captured Black: ",
            font=("Arial", 12),
            anchor="w",
            justify="left",
        )
        self.captured_black_label.grid(row=4, column=8, padx=10, sticky="nw")

        self.move_log_title = tk.Label(
            root,
            text="Move Log:",
            font=("Arial", 12, "bold"),
            anchor="w",
            justify="left",
        )
        self.move_log_title.grid(row=5, column=8, padx=10, pady=(10, 0), sticky="nw")

        self.move_log_frame = tk.Frame(root)
        self.move_log_frame.grid(row=6, column=8, rowspan=3, padx=10, pady=5, sticky="nsew")

        self.move_log_scrollbar = tk.Scrollbar(self.move_log_frame)

        self.move_log_text = tk.Text(
            self.move_log_frame,
            width=28,
            height=15,
            font=("Arial", 10),
            state="disabled",
            wrap="word",
            yscrollcommand=self.move_log_scrollbar.set,
        )

        self.move_log_scrollbar.config(command=self.move_log_text.yview)

        self.move_log_text.pack(side="left", fill="both", expand=True)
        self.move_log_scrollbar.pack(side="right", fill="y")

    def update_status(self, text):
        self.status_label.config(text=text)

    def update_captured(self, captured_white, captured_black):
        white_text = "Captured White: " + " ".join(captured_white)
        black_text = "Captured Black: " + " ".join(captured_black)

        self.captured_white_label.config(text=white_text)
        self.captured_black_label.config(text=black_text)

    def update_move_log(self, move_log):
        self.move_log_text.config(state="normal")
        self.move_log_text.delete("1.0", tk.END)

        for i, entry in enumerate(move_log, start=1):
            self.move_log_text.insert(tk.END, f"{i}. {entry}\n")

        self.move_log_text.see(tk.END)
        self.move_log_text.config(state="disabled")