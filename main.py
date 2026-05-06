import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
from PIL import Image, ImageTk 

class PortfolioManagerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw() 
        self.records_file = "provider_records.json"
        self.show_title_page()

    def custom_input(self, title, prompt, initialvalue="", is_float=False):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("500x300") 
        dialog.configure(bg="#F5F5F5")

        label = tk.Label(dialog, text=prompt, bg="#F5F5F5", font=("Poppins", 12))
        label.pack(pady=10)

        entry = tk.Entry(dialog, width=40, font=("Poppins", 12))
        if initialvalue:
            entry.insert(0, initialvalue)
        entry.pack(pady=5)

        result = [None]

        def ok():
            value = entry.get()
            if is_float:
                try:
                    result[0] = float(value)
                except ValueError:
                    messagebox.showerror("Invalid Input", "Please enter a valid number.")
                    return
            else:
                result[0] = value
            dialog.destroy()

        def cancel():
            result[0] = None
            dialog.destroy()

        button_frame = tk.Frame(dialog, bg="#F5F5F5")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="OK", command=ok, bg="#E3A0B1", fg="#FFFFFF", width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancel", command=cancel, bg="#6D204D", fg="#FFFFFF", width=10).pack(side=tk.LEFT, padx=5)

        dialog.wait_window()
        return result[0]

    def show_title_page(self):
        self.title_window = tk.Toplevel(self.root)
        self.title_window.title("Servify - Title Page")
        self.title_window.state("zoomed")
        self.title_window.configure(bg="#F5F5F5")

        try:
            icon_img = Image.open("assets/logo.png")
            icon_img = icon_img.resize((64, 64))  # Resize the image for the icon
            icon_img = ImageTk.PhotoImage(icon_img)
            self.title_window.iconphoto(True, icon_img)  # Set the icon for the window
        except Exception as e:
            messagebox.showerror("Error", f"Icon loading error: {e}")

        try:
            logo_img = Image.open("assets/logo.png")
            logo_img = logo_img.resize((200, 200))
            logo_img = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(self.title_window, image=logo_img, bg="#F5F5F5")
            logo_label.image = logo_img
            logo_label.pack(pady=100)

        except Exception as e:
            messagebox.showerror("Error", f"Logo loading error: {e}")

        title_label = tk.Label(
            self.title_window,
            text="SERVIFY",
            font=("Poppins ExtraBold", 65, "bold"),
            fg="#6D204D",
            bg="#F5F5F5"
        )
        title_label.pack(pady=20)

        tagline_label = tk.Label(
            self.title_window,
            text="Showcase your skills and services.",
            font=("Poppins", 18),
            fg="#6D204D",
            bg="#F5F5F5"
        )
        tagline_label.pack(pady=10)

        start_button = tk.Button(
            self.title_window,
            text="Get Started",
            font=("Poppins", 18),
            command=self.open_homepage,
            bg="#E3A0B1",
            fg="#FFFFFF",
            width=20,
            height=2
        )
        start_button.pack(pady=30)

    def open_homepage(self):
        self.title_window.destroy()
        self.root.deiconify()
        self.root.title("Servify - Homepage")
        self.root.state("zoomed")
        self.root.configure(bg="#F5F5F5")


        self.body_frame = tk.Frame(self.root, bg="#F5F5F5", pady=20, padx=20)
        self.body_frame.pack(fill=tk.BOTH, expand=True)

        self.upper_frame = tk.Frame(self.body_frame, bg="#F5F5F5")
        self.upper_frame.pack(fill=tk.BOTH, expand=True)

        self.button_frame = tk.Frame(
            self.upper_frame,
            bg="#FFFFFF",
            padx=10,
            pady=10,
            relief=tk.RIDGE,
            borderwidth=1
        )
        self.button_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        try:
            self.add_provider_img = Image.open("assets/add_provider.png")
            self.add_provider_img = self.add_provider_img.resize((50, 50))
            self.add_provider_img = ImageTk.PhotoImage(self.add_provider_img)

            self.edit_provider_img = Image.open("assets/edit_provider.png")
            self.edit_provider_img = self.edit_provider_img.resize((50, 50))
            self.edit_provider_img = ImageTk.PhotoImage(self.edit_provider_img)

            self.delete_provider_img = Image.open("assets/delete_provider.png")
            self.delete_provider_img = self.delete_provider_img.resize((50, 50))
            self.delete_provider_img = ImageTk.PhotoImage(self.delete_provider_img)

            self.manage_services_img = Image.open("assets/manage_services.png")
            self.manage_services_img = self.manage_services_img.resize((50, 50))
            self.manage_services_img = ImageTk.PhotoImage(self.manage_services_img)

            self.exit_img = Image.open("assets/exit.png")
            self.exit_img = self.exit_img.resize((50, 50))
            self.exit_img = ImageTk.PhotoImage(self.exit_img)

            tk.Button(self.button_frame, image=self.add_provider_img, command=self.add_provider,
                      width=50, height=50).pack(pady=5)

            tk.Button(self.button_frame, image=self.edit_provider_img, command=self.edit_provider,
                      width=50, height=50).pack(pady=5)
            tk.Button(self.button_frame, image=self.delete_provider_img, command=self.delete_provider,
                      width=50, height=50).pack(pady=5)
            tk.Button(self.button_frame, image=self.manage_services_img, command=self.manage_services,
                      width=50, height=50).pack(pady=5)
            tk.Button(self.button_frame, image=self.exit_img, command=self.root.destroy,
                      width=50, height=50).pack(pady=5)

        except Exception as e:
            messagebox.showerror("Error", f"Image loading error: {e}")

        self.list_frame = tk.Frame(
            self.upper_frame,
            bg="#F5F5F5",
            padx=0,
            pady=0,
            relief=tk.FLAT,
            borderwidth=0
        )
        self.list_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=(0, 10))

        self.search_label = tk.Label(
            self.list_frame,
            text="Search Providers/Services:",
            font=("Poppins", 15),
            fg="#6D204D",
            bg="#F5F5F5"
        )
        self.search_label.pack(pady=(0, 10))

        self.search_frame = tk.Frame(self.list_frame, bg="#F5F5F5")
        self.search_frame.pack(fill=tk.X, pady=(0, 10))

        self.search_entry = tk.Entry(self.search_frame, font=("Poppins", 12), width=30)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.search_button = tk.Button(
            self.search_frame,
            text="Search",
            font=("Poppins", 14),
            bg="#E3A0B1",
            fg="#FFFFFF",
            command=self.search_provider_or_service,
            width=10
        )
        self.search_button.pack(side=tk.LEFT, padx=(10, 0))

        self.list_label = tk.Label(
            self.list_frame,
            text="Providers",
            font=("Poppins", 20, "bold"),
            fg="#6D204D",
            bg="#F5F5F5"
        )
        self.list_label.pack(anchor="w", pady=(10, 5))

        self.provider_listbox = tk.Listbox(
            self.list_frame,
            font=("Poppins", 12),
            bg="#F8D8E4",
            fg="#6D204D",
            selectbackground="#F1C6D2"
        )
        self.provider_listbox.pack(fill=tk.BOTH, expand=True, pady=(0, 0))

        self.provider_listbox.bind("<<ListboxSelect>>", self.display_selected_details)

        self.details_frame = tk.Frame(
            self.body_frame,
            bg="#FFFFFF",
            pady=18,
            padx=18,
            relief=tk.SUNKEN,
            borderwidth=1,
            height=760
        )
        self.details_frame.pack(fill=tk.BOTH, expand=True, pady=(14, 0), padx=(0, 0))

        self.details_label = tk.Label(
            self.details_frame,
            text="Details",
            font=("Poppins", 22, "bold"),
            fg="#6D204D",
            bg="#FFFFFF"
        )
        self.details_label.pack(pady=(0, 12))

        self.details_text = tk.Text(
            self.details_frame,
            height=40,
            font=("Poppins", 14),
            bg="#F8D8E4",
            fg="#6D204D",
            state=tk.DISABLED,
            wrap=tk.WORD
        )
        self.details_text.pack(fill=tk.BOTH, expand=True)

        self.load_data()
        self.refresh_provider_listbox()

    def load_data(self):
        if os.path.exists(self.records_file):
            try:
                with open(self.records_file, "r") as file:
                    self.providers = json.load(file)
            except:
                self.providers = {}
        else:
            self.providers = {}

    def refresh_provider_listbox(self):
        self.provider_listbox.delete(0, tk.END)
        for provider_id, provider_info in self.providers.items():
            self.provider_listbox.insert(tk.END, provider_info["name"])

    def get_selected_provider_id(self):
        selected_index = self.provider_listbox.curselection()

        if not selected_index:
            return None

        selected_text = self.provider_listbox.get(selected_index[0])
        selected_text = selected_text.strip()

        for provider_id, provider_info in self.providers.items():
            if provider_info["name"] == selected_text:
                return provider_id
            if selected_text.startswith(provider_info["name"] + " - "):
                return provider_id

        return None

    def display_selected_details(self, event):
        provider_id = self.get_selected_provider_id()

        if not provider_id:
            return

        provider = self.providers[provider_id]

        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete("1.0", tk.END)

        details = (
            f"Name: {provider['name']}\n"
            f"Contact: {provider['contact']}\n\n"
            f"Services/Products:\n"
        )

        if not provider["services"]:
            details += "- None\n"
        else:
            for service in provider["services"]:
                details += f"- {service['name']} (₱{service['price']: .2f}): {service['description']}\n"

        self.details_text.insert(tk.END, details)
        self.details_text.config(state=tk.DISABLED)

    def search_provider_or_service(self):
        search_query = self.search_entry.get().lower()
        self.provider_listbox.delete(0, tk.END)

        if search_query == "":
            self.refresh_provider_listbox()
        else:
            found = False
            for provider_id, provider_info in self.providers.items():
                if search_query in provider_info["name"].lower():
                    self.provider_listbox.insert(tk.END, provider_info["name"])
                    found = True
                else:
                    for service in provider_info["services"]:
                        if search_query in service["name"].lower() or search_query in service["description"].lower():
                            self.provider_listbox.insert(tk.END, provider_info["name"] + " - " + service["name"])
                            found = True

            if not found:
                messagebox.showinfo("No Matches", "No providers or services found matching your search.")

    def add_provider(self):
        form_window = tk.Toplevel(self.root)
        form_window.title("Add Provider")
        form_window.configure(bg="#F5F5F5")

        tk.Label(form_window, text="Name:", bg="#F5F5F5",
                 font=("Poppins", 12)).grid(row=0, column=0, padx=10, pady=5)

        name_entry = tk.Entry(form_window)
        name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_window, text="Contact:", bg="#F5F5F5",
                 font=("Poppins", 12)).grid(row=1, column=0, padx=10, pady=5)

        contact_entry = tk.Entry(form_window)
        contact_entry.grid(row=1, column=1, padx=10, pady=5)

        def save_provider():
            name = name_entry.get()
            contact = contact_entry.get()

            if not name or not contact:
                messagebox.showerror("Error", "All fields must be filled.")
                return

            self.providers[name] = {
                "name": name,
                "contact": contact,
                "services": []
            }

            self.refresh_provider_listbox()
            self.save_data()
            form_window.destroy()

        tk.Button(form_window, text="Save", command=save_provider,
                  font=("Poppins", 10), bg="#E3A0B1",
                  fg="#FFFFFF").grid(row=2, column=0, columnspan=2, pady=10)

    def save_data(self):
        with open(self.records_file, "w") as file:
            json.dump(self.providers, file, indent=4)

    def edit_provider(self):
        provider_id = self.get_selected_provider_id()

        if not provider_id:
            messagebox.showwarning("Warning", "Please select a provider to edit.")
            return

        provider = self.providers[provider_id]

        form_window = tk.Toplevel(self.root)
        form_window.title("Edit Provider")
        form_window.configure(bg="#F5F5F5")

        tk.Label(form_window, text="Name:", bg="#F5F5F5",
                 font=("Poppins", 10)).grid(row=0, column=0, padx=10, pady=5)

        name_entry = tk.Entry(form_window)
        name_entry.insert(0, provider["name"]) 
        name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_window, text="Contact:", bg="#F5F5F5",
                 font=("Poppins", 10)).grid(row=1, column=0, padx=10, pady=5)

        contact_entry = tk.Entry(form_window)
        contact_entry.insert(0, provider["contact"])
        contact_entry.grid(row=1, column=1, padx=10, pady=5)

        def save_changes():
            name = name_entry.get()
            contact = contact_entry.get()

            if not name or not contact:
                messagebox.showerror("Error", "All fields must be filled.")
                return

            self.providers[name] = {
                "name": name,
                "contact": contact,
                "services": provider["services"]
            }

            if provider["name"] != name:
                del self.providers[provider["name"]]

            self.refresh_provider_listbox()
            self.save_data()
            form_window.destroy()

        tk.Button(form_window, text="Save Changes", command=save_changes,
                  font=("Poppins", 10), bg="#E3A0B1",
                  fg="#FFFFFF").grid(row=2, column=0, columnspan=2, pady=10)

    def delete_provider(self):
        provider_id = self.get_selected_provider_id()

        if not provider_id:
            messagebox.showwarning("Warning", "Please select a provider to delete.")
            return

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this provider?"):
            del self.providers[provider_id]
            self.refresh_provider_listbox()
            self.save_data()

            self.details_text.config(state=tk.NORMAL)
            self.details_text.delete("1.0", tk.END)
            self.details_text.config(state=tk.DISABLED)

    def manage_services(self):
        form_window = tk.Toplevel(self.root)
        form_window.title("Manage Services")
        form_window.geometry("900x600")
        form_window.configure(bg="#F5F5F5")

        provider_label = tk.Label(form_window, text="Select Provider:", bg="#F5F5F5", font=("Poppins", 12))
        provider_label.pack(pady=(10, 5))

        provider_var = tk.StringVar(form_window)
        provider_options = list(self.providers.keys())
        if provider_options:
            provider_var.set(provider_options[0])  
        provider_menu = tk.OptionMenu(form_window, provider_var, *provider_options)
        provider_menu.config(bg="#FFFFFF", font=("Poppins", 10))
        provider_menu.pack(pady=(0, 10))

        service_listbox = tk.Listbox(form_window, font=("Poppins", 14), bg="#F8D8E4", fg="#6D204D")
        service_listbox.pack(fill=tk.BOTH, expand=True, pady=10)

        def refresh_service_listbox():
            service_listbox.delete(0, tk.END)
            selected_provider = provider_var.get()
            if selected_provider in self.providers:
                for service in self.providers[selected_provider]["services"]:
                    service_listbox.insert(tk.END, f"{service['name']} (₱{service['price']:.2f})")

        def on_provider_change(*args):
            refresh_service_listbox()

        provider_var.trace("w", on_provider_change)

        def add_service():
            selected_provider = provider_var.get()
            if not selected_provider:
                messagebox.showwarning("Warning", "Please select a provider.")
                return
            name = self.custom_input("Add Service", "Enter the service name:")
            description = self.custom_input("Add Service", "Enter the service description:")
            price = self.custom_input("Add Service", "Enter the service price:", is_float=True)

            if name and description and price is not None:
                self.providers[selected_provider]["services"].append({
                    "name": name,
                    "description": description,
                    "price": price
                })
                refresh_service_listbox()
                self.save_data()

        def edit_service():
            selected_provider = provider_var.get()
            if not selected_provider:
                messagebox.showwarning("Warning", "Please select a provider.")
                return
            selected_index = service_listbox.curselection()
            if not selected_index:
                messagebox.showwarning("Warning", "Please select a service to edit.")
                return

            index = selected_index[0]
            service = self.providers[selected_provider]["services"][index]

            name = self.custom_input("Edit Service", "Enter the service name:", initialvalue=service["name"])
            description = self.custom_input("Edit Service", "Enter the service description:", initialvalue=service["description"])
            price = self.custom_input("Edit Service", "Enter the service price:", initialvalue=str(service["price"]), is_float=True)

            if name and description and price is not None:
                self.providers[selected_provider]["services"][index] = {
                    "name": name,
                    "description": description,
                    "price": price
                }
                refresh_service_listbox()
                self.save_data()

        def delete_service():
            selected_provider = provider_var.get()
            if not selected_provider:
                messagebox.showwarning("Warning", "Please select a provider.")
                return
            selected_index = service_listbox.curselection()
            if not selected_index:
                messagebox.showwarning("Warning", "Please select a service to delete.")
                return

            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this service?"):
                index = selected_index[0]
                self.providers[selected_provider]["services"].pop(index)
                refresh_service_listbox()
                self.save_data()

        button_frame = tk.Frame(form_window, bg="#F5F5F5")
        button_frame.pack(fill=tk.X, pady=10)

        tk.Button(button_frame, text="Add Service", command=add_service, width=12, bg="#E3A0B1", fg="#FFFFFF").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Edit Service", command=edit_service, width=12, bg="#6D204D", fg="#FFFFFF").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Delete Service", command=delete_service, width=12, bg="#B33A5F", fg="#FFFFFF").pack(side=tk.LEFT, padx=5)

        refresh_service_listbox()

        form_window.mainloop()


if __name__ == "__main__":
    app = PortfolioManagerApp()
    tk.mainloop()