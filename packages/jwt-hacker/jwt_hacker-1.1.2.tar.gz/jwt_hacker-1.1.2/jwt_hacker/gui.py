from tkinter import ttk, Tk, Text, Frame, Scrollbar, END, VERTICAL, filedialog, Label, PhotoImage
from tkinter.ttk import Style
import threading
import os
import logging
from jwt_hacker.decoder import operations


# Setup logging
logging.basicConfig(
    filename="jwt_hacker_gui.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_icon_path(icon_name):
    """Resolve the path to an icon based on the platform."""
    import platform
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if platform.system() == "Windows":
        return os.path.join(base_dir, f"resources/{icon_name}.ico")
    elif platform.system() == "Darwin":  # macOS
        return os.path.join(base_dir, f"resources/{icon_name}.icns")
    else:
        return os.path.join(base_dir, f"resources/{icon_name}.png")


def add_tooltip(widget, text):
    """Add a tooltip to a widget."""
    tooltip = Label(widget, text=text, bg="black", fg="lime", font=("Courier", 10), relief="solid", bd=1)
    tooltip.place_forget()

    def on_enter(_):
        tooltip.place(relx=0.5, rely=1.1, anchor="center")

    def on_leave(_):
        tooltip.place_forget()

    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)


def main():
    root = Tk()
    root.title("JWT Hacker - Powered by Grey Node Security")
    root.geometry("1920x1080")
    root.configure(bg="black")

    try:
        icon_path = get_icon_path("icon")
        root.iconbitmap(icon_path)
    except Exception as e:
        logging.warning(f"Icon load error: {e}")

    # Style configuration
    style = Style()
    style.configure("TLabel", background="black", foreground="lime", font=("Courier", 12))
    style.configure("TButton", background="black", foreground="lime", font=("Courier", 12), borderwidth=2)
    style.map("TButton", background=[("active", "lime")], foreground=[("active", "black")])

    # Header Section
    header_frame = Frame(root, bg="black")
    header_frame.pack(fill="x", pady=10)

    try:
        logo_path = get_icon_path("icon")
        logo_img = PhotoImage(file=logo_path).subsample(10, 10)
        logo_label = Label(header_frame, image=logo_img, bg="black")
        logo_label.image = logo_img
        logo_label.pack(side="left", padx=10)
    except Exception as e:
        logging.warning(f"Logo load error: {e}")

    org_label = Label(header_frame, text="Grey Node Security", fg="lime", bg="black", font=("Courier", 16, "bold"))
    org_label.pack(side="left", padx=10)

    org_label = Label(header_frame, text="JWT Hacker v1.1.1", fg="lime", bg="black", font=("Courier", 16, "bold"))
    org_label.pack(side="center", padx=10)    

    coder_label = Label(header_frame, text="Programmed by: Z3r0 S3c", fg="lime", bg="black", font=("Courier", 12, "italic"))
    coder_label.pack(side="right", padx=10)

    # Input Frame
    input_frame = Frame(root, bg="black")
    input_frame.pack(pady=10)

    ttk.Label(input_frame, text="Input JWT Token (Required):", style="TLabel").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    input_text = Text(input_frame, height=5, width=80, bg="black", fg="lime", insertbackground="lime", font=("Courier", 12), wrap="word")
    input_text.grid(row=1, column=0, padx=5, pady=5, columnspan=2)

    ttk.Label(input_frame, text="JWT Key (Optional):", style="TLabel").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    key_text = Text(input_frame, height=1, width=40, bg="black", fg="lime", insertbackground="lime", font=("Courier", 12))
    key_text.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(input_frame, text="Private Key (Optional):", style="TLabel").grid(row=3, column=0, padx=5, pady=5, sticky="w")
    private_key_text = Text(input_frame, height=5, width=80, bg="black", fg="lime", insertbackground="lime", font=("Courier", 12), wrap="word")
    private_key_text.grid(row=4, column=0, padx=5, pady=5, columnspan=2)

    ttk.Label(input_frame, text="Public Key (Optional):", style="TLabel").grid(row=5, column=0, padx=5, pady=5, sticky="w")
    public_key_text = Text(input_frame, height=5, width=80, bg="black", fg="lime", insertbackground="lime", font=("Courier", 12), wrap="word")
    public_key_text.grid(row=6, column=0, padx=5, pady=5, columnspan=2)

    # Output Frame
    output_frame = Frame(root, bg="black")
    output_frame.pack(pady=10)

    ttk.Label(output_frame, text="Decoded Output:", style="TLabel").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    output_text = Text(output_frame, height=15, width=80, bg="black", fg="lime", insertbackground="lime", font=("Courier", 12), wrap="word")
    output_text.grid(row=1, column=0, padx=5, pady=5, columnspan=2)

    scrollbar = Scrollbar(output_frame, orient=VERTICAL, command=output_text.yview)
    scrollbar.grid(row=1, column=2, sticky="ns")
    output_text["yscrollcommand"] = scrollbar.set

    # Status Bar
    status_bar = Label(root, text="Ready", bg="black", fg="lime", anchor="w", font=("Courier", 10))
    status_bar.pack(fill="x", side="bottom")

    # Decoding Functionality
    def decode_input():
        jwt_token = input_text.get("1.0", END).strip()
        jwt_key = key_text.get("1.0", END).strip() or None
        private_key = private_key_text.get("1.0", END).strip() or None
        public_key = public_key_text.get("1.0", END).strip() or None

        if not jwt_token:
            status_bar.config(text="Error: No JWT token provided!")
            return

        parts = jwt_token.split('.')
        if len(parts) != 3:
            status_bar.config(text="Error: Invalid JWT structure!")
            return

        header, payload, signature = parts
        output_text.delete("1.0", END)

        for part, label in zip([header, payload], ["Header", "Payload"]):
            output_text.insert(END, f"{label}:\n")
            for name, func in operations.items():
                try:
                    if name in ["HS256 Verify"] and jwt_key:
                        result = func(jwt_token, jwt_key)
                    elif name in ["RS256 Verify", "PS256 Verify", "ECDSA Verify"] and public_key:
                        result = func(jwt_token, public_key)
                    else:
                        result = func(part)

                    if result:
                        output_text.insert(END, f"  {name}:\n{result}\n\n")
                except Exception as e:
                    output_text.insert(END, f"  {name}: Error - {e}\n\n")
                    logging.error(f"Error in {name}: {e}")

        output_text.insert(END, f"Signature (Base64):\n{signature}\n")
        status_bar.config(text="Decoding Complete!")

    # Save Output
    def save_output():
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(output_text.get("1.0", END))
            status_bar.config(text=f"Output saved to {file_path}")

    # Buttons
    button_frame = Frame(root, bg="black")
    button_frame.pack(pady=10)

    ttk.Button(button_frame, text="Decode", command=lambda: threading.Thread(target=decode_input).start(), style="TButton").grid(row=0, column=0, padx=10, pady=5)
    ttk.Button(button_frame, text="Save Output", command=save_output, style="TButton").grid(row=0, column=1, padx=10, pady=5)
    ttk.Button(button_frame, text="Clear", command=lambda: [input_text.delete("1.0", END), key_text.delete("1.0", END), private_key_text.delete("1.0", END), public_key_text.delete("1.0", END), output_text.delete("1.0", END), status_bar.config(text="Ready")], style="TButton").grid(row=0, column=2, padx=10, pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()
