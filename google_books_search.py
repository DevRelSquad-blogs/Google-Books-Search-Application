import requests
import tkinter as tk
from tkinter import messagebox, ttk

# Function to search books using the Google Books API
def search_books():
    book_name = search_entry.get()
    if not book_name:
        messagebox.showwarning("Input Error", "Please enter a book name.")
        return
    
    # Google Books API URL
    api_key = 'Your_API_KEY'  
    url = f"https://www.googleapis.com/books/v1/volumes?q={book_name}&key={api_key}"
    
    # Making a request to the API
    response = requests.get(url)
    
    # Checking if the request was successful
    if response.status_code == 200:
        data = response.json()
        display_results(data)
    else:
        messagebox.showerror("API Error", "Failed to retrieve data from Google Books API")

# Function to display the results in the GUI
def display_results(data):
    # Clear the tree view before displaying new results
    for item in results_tree.get_children():
        results_tree.delete(item)
    
    # Checking if any items were found
    if 'items' in data:
        for book in data['items']:
            volume_info = book.get('volumeInfo', {})
            title = volume_info.get('title', 'No title')
            authors = ', '.join(volume_info.get('authors', ['Unknown author']))
            publisher = volume_info.get('publisher', 'Unknown publisher')
            results_tree.insert("", "end", values=(title, authors, publisher))
    else:
        messagebox.showinfo("No Results", "No books found matching the search term.")

# Setting up the GUI
root = tk.Tk()
root.title("Google Books Search")


root.configure(bg="#ADD8E6")  

# Styling the widgets
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), padding=5)
style.configure("TLabel", background="#ADD8E6", font=("Arial", 14, "bold"))
style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
style.configure("Treeview", font=("Arial", 10))

# Search Label
search_label = tk.Label(root, text="Enter Book Name:", bg="#ADD8E6", fg="#000000")
search_label.pack(pady=10)

search_entry = tk.Entry(root, width=50, font=("Arial", 12))
search_entry.pack(pady=10)

search_button = ttk.Button(root, text="Search", command=search_books, style="TButton")
search_button.pack(pady=10)

results_label = tk.Label(root, text="Search Results:", bg="#ADD8E6", fg="#000000")
results_label.pack(pady=10)

columns = ("Title", "Authors", "Publisher")
results_tree = ttk.Treeview(root, columns=columns, show="headings", height=10)

results_tree.heading("Title", text="Title")
results_tree.heading("Authors", text="Authors")
results_tree.heading("Publisher", text="Publisher")

results_tree.tag_configure("evenrow", background="#E0FFFF") 
results_tree.tag_configure("oddrow", background="#F0F8FF")   

results_tree.pack(pady=20)

root.geometry("700x500")

root.mainloop()
