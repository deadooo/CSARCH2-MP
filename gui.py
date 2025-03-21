import tkinter as tk
from tkinter import messagebox, ttk
from cache import Cache
import random

class CacheGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CSARCH2 Group 6 Cache Simulation - 2-Way BSA + LRU")
        
        self.cache = Cache()
        self.setup_ui()

    def setup_ui(self):
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.grid(row=0, column=0, sticky="ew")

        tk.Label(frame, text="Number of Memory Blocks:").grid(row=0, column=0, sticky="w")
        self.block_entry = tk.Entry(frame)
        self.block_entry.grid(row=0, column=1, padx=5)

        self.run_button = tk.Button(frame, text="Run Simulation", command=self.run_simulation)
        self.run_button.grid(row=1, columnspan=2, pady=10)

        result_frame = tk.Frame(self.root)
        result_frame.grid(row=1, column=0, padx=10, pady=10)

        scrollbar = tk.Scrollbar(result_frame, orient="vertical")
        self.output_text = tk.Text(result_frame, width=60, height=20, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.output_text.yview)

        self.output_text.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        result_frame.grid_rowconfigure(0, weight=1)
        result_frame.grid_columnconfigure(0, weight=1)

    def run_simulation(self):
        try:
            num_blocks = int(self.block_entry.get())
            if num_blocks < 1024:
                messagebox.showerror("Error", "Number of blocks must be at least 1024!")
                return

            self.cache.reset_cache()
            self.run_test_cases(num_blocks)
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Enter an integer value for memory blocks.")

    def run_test_cases(self, num_blocks):
        self.output_text.delete(1.0, tk.END)
        
        self.output_text.insert(tk.END, "Running Sequential Test Case...\n")
        self.run_sequence(list(range(2 * self.cache.num_blocks)) * 4)

        self.output_text.insert(tk.END, "Running Random Test Case...\n")
        random_blocks = random.sample(range(4 * self.cache.num_blocks), 4 * self.cache.num_blocks)
        self.run_sequence(random_blocks)

        self.output_text.insert(tk.END, "Running Mid-Repeat Test Case...\n")
        mid_repeat = list(range(self.cache.num_blocks)) + list(range(1, self.cache.num_blocks)) * 2 + list(range(self.cache.num_blocks, 2 * self.cache.num_blocks)) * 4
        self.run_sequence(mid_repeat)

    def run_sequence(self, sequence):
        for block in sequence:
            hit = self.cache.access_block(block)
            status = "Hit" if hit else "Miss"
            self.output_text.insert(tk.END, f"Accessing block {block}: {status}\n")

        stats = self.cache.get_stats()
        self.output_text.insert(tk.END, f"\n\n\n\n\n\n\n\n\n\nStats:\n")
        for key, value in stats.items():
            self.output_text.insert(tk.END, f"{key}: {value:.2f}\n")
        self.output_text.insert(tk.END, "-" * 50 + "\n")
