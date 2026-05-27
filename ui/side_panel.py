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

        self.captured_white_label = tk.Label(root, text="Captured White: ", font=("Arial", 12))
        self.captured_white_label.grid(row=3, column=8, padx=10, sticky="nw")

        self.captured_black_label = tk.Label(root, text="Captured Black: ", font=("Arial", 12))
        self.captured_black_label.grid(row=4, column=8, padx=10, sticky="nw")

        self.move_log_title = tk.Label(root, text="Move Log:", font=("Arial", 12, "bold"))
        self.move_log_title.grid(row=5, column=8, padx=10, pady=(10, 0), sticky="nw")

        self.move_log_frame = tk.Frame(root)
        self.move_log_frame.grid(row=6, column=8, rowspan=3, padx=10, pady=5, sticky="nsew")

        self.move_log_scrollbar = tk.Scrollbar(self.move_log_frame)

        self.move_log_text = tk.Text(
            self.move_log_frame,
            width=28,
            height=10,
            font=("Arial", 10),
            state="disabled",
            wrap="word",
            yscrollcommand=self.move_log_scrollbar.set,
        )

        self.move_log_scrollbar.config(command=self.move_log_text.yview)
        self.move_log_text.pack(side="left", fill="both", expand=True)
        self.move_log_scrollbar.pack(side="right", fill="y")

        self.jog_title = tk.Label(root, text="Manual Jog:", font=("Arial", 12, "bold"))
        self.jog_title.grid(row=9, column=8, padx=10, pady=(10, 0), sticky="nw")

        self.jog_frame = tk.Frame(root)
        self.jog_frame.grid(row=10, column=8, padx=10, pady=5, sticky="nw")

        self.btn_x_neg = tk.Button(self.jog_frame, text="X-", width=5)
        self.btn_x_pos = tk.Button(self.jog_frame, text="X+", width=5)
        self.btn_y_neg = tk.Button(self.jog_frame, text="Y-", width=5)
        self.btn_y_pos = tk.Button(self.jog_frame, text="Y+", width=5)
        self.btn_z_neg = tk.Button(self.jog_frame, text="Z-", width=5)
        self.btn_z_pos = tk.Button(self.jog_frame, text="Z+", width=5)
        self.btn_stop = tk.Button(self.jog_frame, text="STOP", width=12)

        self.btn_x_neg.grid(row=0, column=0, padx=2, pady=2)
        self.btn_x_pos.grid(row=0, column=1, padx=2, pady=2)
        self.btn_y_neg.grid(row=1, column=0, padx=2, pady=2)
        self.btn_y_pos.grid(row=1, column=1, padx=2, pady=2)
        self.btn_z_neg.grid(row=2, column=0, padx=2, pady=2)
        self.btn_z_pos.grid(row=2, column=1, padx=2, pady=2)
        self.btn_stop.grid(row=3, column=0, columnspan=2, padx=2, pady=5)

    def connect_jog_buttons(
        self,
        x_neg_callback,
        x_pos_callback,
        y_neg_callback,
        y_pos_callback,
        z_neg_callback,
        z_pos_callback,
        stop_callback,
    ):
        self.btn_x_neg.config(command=x_neg_callback)
        self.btn_x_pos.config(command=x_pos_callback)
        self.btn_y_neg.config(command=y_neg_callback)
        self.btn_y_pos.config(command=y_pos_callback)
        self.btn_z_neg.config(command=z_neg_callback)
        self.btn_z_pos.config(command=z_pos_callback)
        self.btn_stop.config(command=stop_callback)

    def update_status(self, text):
        self.status_label.config(text=text)

    def update_captured(self, captured_white, captured_black):
        self.captured_white_label.config(text="Captured White: " + " ".join(captured_white))
        self.captured_black_label.config(text="Captured Black: " + " ".join(captured_black))

    def update_move_log(self, move_log):
        self.move_log_text.config(state="normal")
        self.move_log_text.delete("1.0", tk.END)

        for i, entry in enumerate(move_log, start=1):
            self.move_log_text.insert(tk.END, f"{i}. {entry}\n")

        self.move_log_text.see(tk.END)
        self.move_log_text.config(state="disabled")