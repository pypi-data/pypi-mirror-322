from tkinter import ttk, Tk, Text, Frame, Scrollbar, END, VERTICAL, filedialog, Label, PhotoImage
from tkinter.ttk import Style
import threading
import os
from jwt_hacker.decoder import operations

# Create the GUI
def main():
    # Initialize the main window
    root = Tk()
    root.title("JWT Hacker - Powered by Grey Node Security")
    root.geometry("1920x1080")
    root.configure(bg="black")
    
    # Dynamically resolve icon path
    base_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(base_dir, "icon.ico")

    try:
        root.iconbitmap(icon_path)
    except Exception as e:
        print(f"Error loading icon: {e}")


    # Style configuration for a hacker-themed vibe
    style = Style()
    style.configure("TLabel", background="black", foreground="lime", font=("Courier", 12))
    style.configure("TButton", background="black", foreground="lime", font=("Courier", 12), borderwidth=2)
    style.map("TButton", background=[("active", "lime")], foreground=[("active", "black")])

    # Header section
    header_frame = Frame(root, bg="black")
    header_frame.pack(fill="x", pady=10)

    # Logo
    logo_path = os.path.abspath("icon.png")
    if os.path.exists(logo_path):
        logo_img = PhotoImage(file=logo_path).subsample(10, 10)  # Resize for display
        logo_label = Label(header_frame, image=logo_img, bg="black")
        logo_label.image = logo_img  # Keep a reference to prevent garbage collection
        logo_label.pack(side="left", padx=10)

    # Organization Name
    org_label = Label(header_frame, text="Grey Node Security", fg="lime", bg="black", font=("Courier", 16, "bold"))
    org_label.pack(side="left", padx=10)

    # Coder Information
    coder_label = Label(header_frame, text="Programmed by: Z3r0 S3c", fg="lime", bg="black", font=("Courier", 12, "italic"))
    coder_label.pack(side="right", padx=10)

    # Input frame
    input_frame = Frame(root, bg="black")
    input_frame.pack(pady=10)

    ttk.Label(input_frame, text="Input JWT Token:", style="TLabel").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    input_text = Text(input_frame, height=5, width=80, bg="black", fg="lime", insertbackground="lime", font=("Courier", 12), wrap="word")
    input_text.grid(row=1, column=0, padx=5, pady=5, columnspan=2)

    # Output frame
    output_frame = Frame(root, bg="black")
    output_frame.pack(pady=10)

    ttk.Label(output_frame, text="Decoded Output:", style="TLabel").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    output_text = Text(output_frame, height=15, width=80, bg="black", fg="lime", insertbackground="lime", font=("Courier", 12), wrap="word")
    output_text.grid(row=1, column=0, padx=5, pady=5, columnspan=2)

    scrollbar = Scrollbar(output_frame, orient=VERTICAL, command=output_text.yview)
    scrollbar.grid(row=1, column=2, sticky="ns")
    output_text["yscrollcommand"] = scrollbar.set

    # Status bar
    status_bar = Label(root, text="Ready", bg="black", fg="lime", anchor="w", font=("Courier", 10))
    status_bar.pack(fill="x", side="bottom")

    # Function to decode input
    def decode_input():
        jwt_token = input_text.get("1.0", END).strip()
        if not jwt_token:
            output_text.insert(END, "No input provided!\n")
            status_bar.config(text="Error: No input provided!")
            return

        parts = jwt_token.split('.')
        if len(parts) != 3:
            output_text.insert(END, "Invalid JWT structure!\n")
            status_bar.config(text="Error: Invalid JWT structure!")
            return

        header, payload, signature = parts
        output_text.delete("1.0", END)

        for part, label in zip([header, payload], ["Header", "Payload"]):
            output_text.insert(END, f"{label}:\n")
            for name, func in operations.items():
                result = func(part)
                if result:
                    output_text.insert(END, f"  {name}:\n{result}\n\n")

        output_text.insert(END, f"Signature (Base64):\n{signature}\n")
        status_bar.config(text="Decoding Complete!")

    # Save output function
    def save_output():
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(output_text.get("1.0", END))
            status_bar.config(text=f"Output saved to {file_path}")

    # Buttons
    button_frame = Frame(root, bg="black")
    button_frame.pack(pady=10)

    decode_button = ttk.Button(button_frame, text="Decode", command=lambda: threading.Thread(target=decode_input).start(), style="TButton")
    decode_button.grid(row=0, column=0, padx=10, pady=5)

    save_button = ttk.Button(button_frame, text="Save Output", command=save_output, style="TButton")
    save_button.grid(row=0, column=1, padx=10, pady=5)

    clear_button = ttk.Button(button_frame, text="Clear", command=lambda: [input_text.delete("1.0", END), output_text.delete("1.0", END), status_bar.config(text="Ready")], style="TButton")
    clear_button.grid(row=0, column=2, padx=10, pady=5)

    # Run the GUI
    root.mainloop()
