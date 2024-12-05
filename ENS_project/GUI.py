
from Calling_API import *

import pandas as pd
from pandastable import Table
import numpy as np


# used for gui
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json


class APIClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("API Client GUI")
        self.selected_category = None
        self.selected_schedule = None
        self.selected_entity = None
        self.selected_asset = None
        self.entities_list = None

        # Create a frame to hold the canvas and the vertical scrollbar
        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(side="top", fill="both", expand=True)

        # Create the canvas and vertical scrollbar
        self.canvas = tk.Canvas(self.canvas_frame)
        self.scroll_y = ttk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scroll_y.set)

        # Create the scrollable frame inside the canvas
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Pack the canvas and vertical scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll_y.pack(side="right", fill="y")

        # Configure the canvas to adjust its scroll region
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        # Create the horizontal scrollbar and attach it to the canvas
        self.scroll_x = ttk.Scrollbar(self.root, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.scroll_x.set)

        # Pack the horizontal scrollbar at the bottom of the main window
        self.scroll_x.pack(side="bottom", fill="x")




        ###### categories frame #######
        # Set frame in page
        self.categories_frame = ttk.LabelFrame(self.scrollable_frame, text="Categories")
        self.categories_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Configure grid with defined sizes
        self.categories_frame.columnconfigure(0, minsize=600)  # Define size for output column
        self.categories_frame.columnconfigure(1, minsize=600)  # Define size for input column (even if empty)
        self.categories_frame.columnconfigure(2, minsize=600)  # Define size for buttons column

        # Category Output Frame
        self.categories_output_frame = ttk.LabelFrame(self.categories_frame, text="Category Output")
        self.categories_output_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Fetch Categories Button
        self.categories_button = ttk.Button(self.categories_output_frame, text="Fetch Categories",
                                            command=self.fetch_categories)
        self.categories_button.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Category Output Text
        self.categories_output = tk.Text(self.categories_output_frame, height=20, width=70)
        self.categories_output.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Category Input Frame (Empty)
        self.categories_input_frame = ttk.LabelFrame(self.categories_frame, text="Category Inputs")
        self.categories_input_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Category Buttons Frame
        self.categories_buttons_frame = ttk.LabelFrame(self.categories_frame, text="Category Buttons")
        self.categories_buttons_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        # Category Buttons Frame (Additional buttons can be added here)
        self.categories_button_frame = ttk.Frame(self.categories_buttons_frame)
        self.categories_button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        ###### Entities Frame #######
        # Set frame in page
        self.entities_frame = ttk.LabelFrame(self.scrollable_frame, text="Entities")
        self.entities_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Configure grid with defined sizes
        self.entities_frame.columnconfigure(0, minsize=600)  # Define size for output column
        self.entities_frame.columnconfigure(1, minsize=600)  # Define size for input column
        self.entities_frame.columnconfigure(2, minsize=600)  # Define size for buttons column

        # Entities Output Frame
        self.entities_output_frame = ttk.LabelFrame(self.entities_frame, text="Entities Output")
        self.entities_output_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Fetch Entities Button
        self.entities_button = ttk.Button(self.entities_output_frame, text="Fetch Entities",
                                          command=self.fetch_entities)
        self.entities_button.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Entities Output Text
        self.entities_output = tk.Text(self.entities_output_frame, height=20, width=70)
        self.entities_output.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Category Input Frame
        self.entities_input_frame = ttk.LabelFrame(self.entities_frame, text="Entities Inputs")
        self.entities_input_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Category Input Label
        self.entities_cat_label = ttk.Label(self.entities_input_frame, text="Category:")
        self.entities_cat_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        # Category Input Entry
        self.entities_cat_entry = ttk.Entry(self.entities_input_frame)
        self.entities_cat_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Entities Buttons Frame
        self.entities_buttons_frame = ttk.LabelFrame(self.entities_frame, text="Entities Buttons")
        self.entities_buttons_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")


        ###### Schedules Frame #######
        # Set frame in page
        self.schedules_frame = ttk.LabelFrame(self.scrollable_frame, text="Schedules")
        self.schedules_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        # Configure grid with defined sizes
        self.schedules_frame.columnconfigure(0, minsize=600)  # Define size for output column
        self.schedules_frame.columnconfigure(1, minsize=600)  # Define size for input column
        self.schedules_frame.columnconfigure(2, minsize=600)  # Define size for buttons column

        # Schedules Output Frame
        self.schedules_output_frame = ttk.LabelFrame(self.schedules_frame, text="Schedules Output")
        self.schedules_output_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Fetch Schedules Button
        self.schedules_button = ttk.Button(self.schedules_output_frame, text="Fetch Schedules",
                                           command=self.fetch_schedules)
        self.schedules_button.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Schedules Output Text
        self.schedules_output = tk.Text(self.schedules_output_frame, height=20, width=70)
        self.schedules_output.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Schedules Input Frame
        self.schedules_input_frame = ttk.LabelFrame(self.schedules_frame, text="Schedules Inputs")
        self.schedules_input_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Schedules Buttons Frame
        self.schedules_buttons_frame = ttk.LabelFrame(self.schedules_frame, text="Schedules Buttons")
        self.schedules_buttons_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        # Schedules Buttons Frame (Additional buttons can be added here)
        self.schedules_button_frame = ttk.Frame(self.schedules_buttons_frame)
        self.schedules_button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        ###### Forecasts Frame #######
        # Set frame in page
        self.forecasts_frame = ttk.LabelFrame(self.scrollable_frame, text="Forecasts")
        self.forecasts_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        # Configure grid with defined sizes
        self.forecasts_frame.columnconfigure(0, minsize=600)  # Define size for output column
        self.forecasts_frame.columnconfigure(1, minsize=600)  # Define size for input column
        self.forecasts_frame.columnconfigure(2, minsize=600)  # Define size for buttons column

        # Forecasts Output Frame
        self.forecasts_output_frame = ttk.LabelFrame(self.forecasts_frame, text="Forecasts Output")
        self.forecasts_output_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Fetch Forecasts Button
        self.forecasts_button = ttk.Button(self.forecasts_output_frame, text="Fetch Forecasts",
                                           command=self.fetch_forecasts)
        self.forecasts_button.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Forecasts Output Text
        self.forecasts_output = tk.Text(self.forecasts_output_frame, height=20, width=80)
        self.forecasts_output.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Forecasts Input Frame
        self.forecasts_input_frame = ttk.LabelFrame(self.forecasts_frame, text="Forecasts Inputs")
        self.forecasts_input_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Forecasts Input Fields (Entity ID, Entity Asset ID, Schedule ID)
        self.forecasts_entity_id_label = ttk.Label(self.forecasts_input_frame, text="Entity's Identifier:")
        self.forecasts_entity_id_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.forecasts_entity_id_entry = ttk.Entry(self.forecasts_input_frame)
        self.forecasts_entity_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.forecasts_entity_asset_id_label = ttk.Label(self.forecasts_input_frame, text="Entity's Asset Identifier:")
        self.forecasts_entity_asset_id_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.forecasts_entity_asset_id_entry = ttk.Entry(self.forecasts_input_frame)
        self.forecasts_entity_asset_id_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.forecasts_entity_name_label = ttk.Label(self.forecasts_input_frame, text="Entity Name:")
        self.forecasts_entity_name_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.forecasts_entity_name_entry = ttk.Entry(self.forecasts_input_frame)
        self.forecasts_entity_name_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        self.forecasts_schedule_id_label = ttk.Label(self.forecasts_input_frame, text="Schedule Identifier:")
        self.forecasts_schedule_id_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.forecasts_schedule_id_entry = ttk.Entry(self.forecasts_input_frame)
        self.forecasts_schedule_id_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        self.forecasts_schedule_type_label = ttk.Label(self.forecasts_input_frame, text="Schedule Type:")
        self.forecasts_schedule_type_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.forecasts_schedule_type_entry = ttk.Entry(self.forecasts_input_frame)
        self.forecasts_schedule_type_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        # Forecasts Buttons Frame
        self.forecasts_buttons_frame = ttk.LabelFrame(self.forecasts_frame, text="Forecasts Buttons")
        self.forecasts_buttons_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        # Forecasts Buttons Frame (Additional buttons can be added here)
        self.forecasts_button_frame = ttk.Frame(self.forecasts_buttons_frame)
        self.forecasts_button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        ###### CSV Browser Frame #######
        # Set frame in page
        self.csv_browser_frame = ttk.LabelFrame(self.scrollable_frame, text="CSV Browser")
        self.csv_browser_frame.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        # Configure grid with defined sizes
        self.csv_browser_frame.columnconfigure(0, minsize=600)  # Define size for output column
        self.csv_browser_frame.columnconfigure(1, minsize=600)  # Define size for input column
        self.csv_browser_frame.columnconfigure(2, minsize=600)  # Define size for buttons column

        # CSV Output Frame
        self.csv_output_frame = ttk.LabelFrame(self.csv_browser_frame, text="CSV Output")
        self.csv_output_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Browse CSV Button
        self.browse_csv_button = ttk.Button(self.csv_output_frame, text="Browse CSV", command=self.browse_csv)
        self.browse_csv_button.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        # Create CSV button
        self.create_csv_button = ttk.Button(self.csv_output_frame, text="Create CSV", command=self.create_csv)
        self.create_csv_button.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Listbox to display selected CSV files
        self.csv_output = tk.Text(self.csv_output_frame, height=20, width=80)
        self.csv_output.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # CSV Input Frame
        self.csv_input_frame = ttk.LabelFrame(self.csv_browser_frame, text="CSV Inputs")
        self.csv_input_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.csv_path_label = ttk.Label(self.csv_input_frame, text="Data Path:")
        self.csv_path_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.csv_path_entry = ttk.Entry(self.csv_input_frame)
        self.csv_path_entry.grid(row=1, column=1, columnspan=8, padx=5, pady=5, sticky="w")
        self.csv_col_label = ttk.Label(self.csv_input_frame, text="Selected Producer:")
        self.csv_col_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.csv_col_entry = ttk.Entry(self.csv_input_frame)
        self.csv_col_entry.grid(row=2, column=1, columnspan=5, padx=5, pady=5, sticky="w")

        # CSV Buttons Frame
        self.csv_buttons_frame = ttk.LabelFrame(self.csv_browser_frame, text="CSV Buttons")
        self.csv_buttons_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")


        ###### Submit Forecast Frame #######
        # Set frame in page
        self.submit_frame = ttk.LabelFrame(self.scrollable_frame, text="Submit Forecast")
        self.submit_frame.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

        # Configure grid with defined sizes
        self.submit_frame.columnconfigure(0, minsize=600)  # Define size for output column
        self.submit_frame.columnconfigure(1, minsize=600)  # Define size for input column
        self.submit_frame.columnconfigure(2, minsize=600)  # Define size for buttons column

        # Submit Output Frame
        self.submit_output_frame = ttk.LabelFrame(self.submit_frame, text="Submit Output")
        self.submit_output_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Submit Forecast Button
        self.submit_button = ttk.Button(self.submit_output_frame, text="Submit Forecast", command=self.submit_forecast)
        self.submit_button.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Submit Output Text
        self.submit_output = tk.Text(self.submit_output_frame, height=20, width=70)
        self.submit_output.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Submit Input Frame
        self.submit_input_frame = ttk.LabelFrame(self.submit_frame, text="Submit Inputs")
        self.submit_input_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Submit Input Fields (Category ID, Schedule ID, Entity ID, Entity Asset ID, Power Values, Forecast Type)
        self.submit_category_id_label = ttk.Label(self.submit_input_frame, text="Category Identifier:")
        self.submit_category_id_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.submit_category_id_entry = ttk.Entry(self.submit_input_frame)
        self.submit_category_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.submit_schedule_id_label = ttk.Label(self.submit_input_frame, text="Schedule Identifier:")
        self.submit_schedule_id_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.submit_schedule_id_entry = ttk.Entry(self.submit_input_frame)
        self.submit_schedule_id_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.submit_schedule_type_label = ttk.Label(self.submit_input_frame, text="Schedule Type:")
        self.submit_schedule_type_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.submit_schedule_type_entry = ttk.Entry(self.submit_input_frame)
        self.submit_schedule_type_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")


        self.submit_entity_asset_id_label = ttk.Label(self.submit_input_frame, text="Entity's Asset Identifier:")
        self.submit_entity_asset_id_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.submit_entity_asset_id_entry = ttk.Entry(self.submit_input_frame)
        self.submit_entity_asset_id_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        self.submit_entity_name_label = ttk.Label(self.submit_input_frame, text="Entity Name:")
        self.submit_entity_name_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.submit_entity_name_entry = ttk.Entry(self.submit_input_frame)
        self.submit_entity_name_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        self.submit_power_values_label = ttk.Label(self.submit_input_frame, text="Power Values:")
        self.submit_power_values_label.grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.submit_power_values_entry = ttk.Entry(self.submit_input_frame)
        self.submit_power_values_entry.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        self.submit_forecast_type_label = ttk.Label(self.submit_input_frame, text="Forecast Type:")
        self.submit_forecast_type_label.grid(row=6, column=0, padx=5, pady=5, sticky="e")
        self.submit_forecast_type_entry = ttk.Entry(self.submit_input_frame)
        self.submit_forecast_type_entry.grid(row=6, column=1, padx=5, pady=5, sticky="w")

        # Submit Buttons Frame
        self.submit_buttons_frame = ttk.LabelFrame(self.submit_frame, text="Submit Buttons")
        self.submit_buttons_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        # Submit Buttons Frame (Additional buttons can be added here)
        self.submit_button_frame = ttk.Frame(self.submit_buttons_frame)
        self.submit_button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")


    def fetch_categories(self):
        try:
            result = make_request_categories(client)
            self.categories_output.delete(1.0, tk.END)

            # Clear previous buttons
            for widget in self.categories_buttons_frame.winfo_children():
                widget.destroy()

            if result is not None and isinstance(result, list):
                num_categories = len(result)
                num_columns = 1  # Set a fixed number of columns
                num_rows = (num_categories + num_columns - 1) // num_columns

                for i, category in enumerate(result):
                    category_info = f"Identifier: {category['identifier']}\n"
                    category_info += f"Name: {category['name']}\n"
                    category_info += f"Description: {category['description']}\n"
                    category_info += "-" * 40 + "\n"
                    self.categories_output.insert(tk.END, category_info)

                    row = i // num_columns
                    col = i % num_columns
                    button = ttk.Button(self.categories_buttons_frame, text=category['identifier'],
                                        command=lambda cat=category['identifier']: self.set_selected_category(cat))
                    button.grid(row=row, column=col, padx=5, pady=5, sticky='ew')

                # Configure the grid to ensure buttons expand to fill the space
                for col in range(num_columns):
                    self.categories_buttons_frame.columnconfigure(col, weight=1)
                for row in range(num_rows):
                    self.categories_buttons_frame.rowconfigure(row, weight=1)
        except Exception as e:
            print(f"An error occurred: {e}")

    def set_selected_category(self, category_identifier):
        self.selected_category = category_identifier
        self.entities_cat_entry.delete(0, tk.END)
        self.entities_cat_entry.insert(0, category_identifier)
        self.submit_category_id_entry.delete(0, tk.END)
        self.submit_category_id_entry.insert(0, category_identifier)


    def fetch_schedules(self):
        try:
            result = make_request_schedules(client)
            self.schedules_output.delete(1.0, tk.END)

            # Clear previous buttons
            for widget in self.schedules_buttons_frame.winfo_children():
                widget.destroy()

            if result is not None and isinstance(result, list):
                num_schedules = len(result)
                num_columns = 1  # Set a fixed number of columns
                num_rows = (num_schedules + num_columns - 1) // num_columns

                for i, schedule in enumerate(result):
                    schedule_info = f"Identifier: {schedule['identifier']}\n"
                    schedule_info += f"Name: {schedule['name']}\n"
                    schedule_info += f"Description: {schedule['description']}\n"
                    schedule_info += "-" * 40 + "\n"
                    self.schedules_output.insert(tk.END, schedule_info)

                    row = i // num_columns
                    col = i % num_columns
                    description = schedule['description']
                    label = description.split('.')[0].split('computed')[0]
                    if "Availability" in label:
                        label2 = label + " (Read/ Write)"
                    else:
                        label2 = label + " (Read Only)"
                    button = ttk.Button(self.schedules_buttons_frame, text=label2,
                                        command=lambda sched=schedule['identifier'], schname=schedule['name']: self.set_selected_schedule(sched, schname))
                    button.grid(row=row, column=col, padx=5, pady=5, sticky='ew')

                # Configure the grid to ensure buttons expand to fill the space
                for col in range(num_columns):
                    self.schedules_buttons_frame.columnconfigure(col, weight=1)
                for row in range(num_rows):
                    self.schedules_buttons_frame.rowconfigure(row, weight=1)

            else:
                self.schedules_output.insert(tk.END, "No schedules found or an error occurred.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def select_schedule(self, schedule_name):
        if schedule_name == "HRLYWPFA-MW":
            self.selected_forecast_type = 'Hourly Wind'
        elif schedule_name == "HRLYSPFA-MW":
            self.selected_forecast_type = 'Hourly Solar'
        elif schedule_name == "DLYWPFA-MW":
            self.selected_forecast_type = 'Daily Wind'
        elif schedule_name == "DLYSPFA-MW":
            self.selected_forecast_type = 'Daily Solar'
        else:
            self.selected_forecast_type = 'Non Writeable Forecast'

        self.submit_forecast_type_entry.delete(0, tk.END)
        self.submit_forecast_type_entry.insert(0, self.selected_forecast_type)

    def set_selected_schedule(self, schedule_identifier, schedule_name):
        self.selected_schedule = schedule_identifier
        self.forecasts_schedule_id_entry.delete(0, tk.END)
        self.forecasts_schedule_id_entry.insert(0, schedule_identifier)
        self.select_schedule(schedule_name)
        self.forecasts_schedule_type_entry.delete(0, tk.END)
        self.forecasts_schedule_type_entry.insert(0, schedule_name)
        self.submit_schedule_id_entry.delete(0, tk.END)
        self.submit_schedule_id_entry.insert(0, schedule_identifier)
        self.submit_schedule_type_entry.delete(0, tk.END)
        self.submit_schedule_type_entry.insert(0, schedule_name)


    def fetch_entities(self):
        try:
            cat = self.entities_cat_entry.get()
            print(f"Fetching entities for category: {cat}")
            result = make_request_entities(client, cat)
            self.entities_output.delete(1.0, tk.END)
            # Clear previous buttons
            for widget in self.entities_buttons_frame.winfo_children():
                widget.destroy()

            if result is not None:
                entities = result['Entities']['Entity']
                if isinstance(entities, list) and entities:
                    num_entities = len(entities)
                    num_columns = 1  # Set a fixed number of columns
                    num_rows = (num_entities + num_columns - 1) // num_columns

                    entities_list = []

                    for i, entity in enumerate(entities):
                        entity_info = f"Identifier: {entity['identifier']}\n"
                        entity_info += f"Asset Identifier: {entity['assetIdentifier']}\n"
                        entity_info += f"Name: {entity['name']}\n"
                        entity_info += f"Description: {entity['description']}\n"
                        entity_info += f"Read Only: {'Yes' if entity['isReadOnly'] else 'No'}\n"
                        entity_info += "-" * 40 + "\n"
                        self.entities_output.insert(tk.END, entity_info)

                        row = i // num_columns
                        col = i % num_columns

                        button = ttk.Button(self.entities_buttons_frame,
                                            text=f"{entity['description']}",
                                            command=lambda ent=entity: self.set_selected_entity(ent))
                        button.grid(row=row, column=col, padx=5, pady=5, sticky='ew')

                        entities_list.append(entity['description'])

                    self.entities_list = entities_list

                    # Configure the grid to ensure buttons expand to fill the space
                    for col in range(num_columns):
                        self.entities_buttons_frame.columnconfigure(col, weight=1)
                    for row in range(num_rows):
                        self.entities_buttons_frame.rowconfigure(row, weight=1)

                else:
                    self.entities_output.insert(tk.END, "No entities found for the selected category.")
            else:
                self.entities_output.insert(tk.END, "No entities found or an error occurred.")
        except Exception as e:
            self.entities_output.insert(tk.END, f"An error occurred: {str(e)}")
            messagebox.showerror("Error", str(e))

    def set_selected_entity(self, entity):
        self.selected_entity = entity['identifier']
        self.selected_asset = entity['assetIdentifier']
        self.forecasts_entity_id_entry.delete(0, tk.END)
        self.forecasts_entity_id_entry.insert(0, entity['identifier'])
        self.forecasts_entity_asset_id_entry.delete(0, tk.END)
        self.forecasts_entity_asset_id_entry.insert(0, entity['assetIdentifier'])
        self.submit_entity_asset_id_entry.delete(0, tk.END)
        self.submit_entity_asset_id_entry.insert(0, entity['assetIdentifier'])
        self.forecasts_entity_name_entry.delete(0, tk.END)
        self.forecasts_entity_name_entry.insert(0, entity['name'])
        self.submit_entity_name_entry.delete(0, tk.END)
        self.submit_entity_name_entry.insert(0, entity['name'])




    def format_power_entries(self, response):
        entry = response[0]['Entities']['Entity'][0]
        data = entry['Power']
        dict = {'time': [], 'value': []}
        for item in data:
            # Convert string representation to a dictionary
            time = item['time']
            value = item['value']


            # Format the time and value
            time_str = time.strftime("%Y-%m-%d %H:%M:%S %Z")
            value_str = float(value)


            dict['time'].append(time_str)
            dict['value'].append(value_str)

        df = pd.DataFrame.from_dict(dict)
        return df

    def display_dataframe(self, df, frame):
        # Create a Treeview widget show='headings'
        tree = ttk.Treeview(frame, columns=list(df.columns))
        tree.pack(side='left', fill='both', expand=True)
        tree.column("#0", width=0, stretch=tk.NO)

        # Add columns
        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, anchor='center')

        # Add rows
        for index, row in df.iterrows():
            tree.insert('', 'end', values=list(row))



    def fetch_forecasts(self):
        for widget in self.forecasts_output.winfo_children():
            widget.destroy()
        try:
            entityAssetID = self.forecasts_entity_asset_id_entry.get()
            scheduleID = self.forecasts_schedule_id_entry.get()
            scheduleType = self.forecasts_schedule_type_entry.get()
            catType = self.selected_category
            if (((scheduleType in ['STWPFCST-MW', 'MTWPFCST-MW', 'LTWPFCST-MW', "HRLYWPFA-MW", "DLYWPFA-MW"]) and catType == 'WPLANT') or
                    ((scheduleType in ['STFCST_S-MW', 'MTFCST_S-MW', 'LTFCST_S-MW', "HRLYSPFA-MW", "DLYSPFA-MW"]) and catType == 'SPLANT')):
                result = make_request_forecasts(client, entityAssetID, scheduleID)
                self.forecasts_output.delete(1.0, tk.END)
                if result is not None:
                    power_entries = self.format_power_entries(result)
                    self.display_dataframe(power_entries, self.forecasts_output)
                else:
                    self.forecasts_output.insert(tk.END, "No forecasts found or an error occurred.")
            else:
                messagebox.showerror("Incorrect Parameters", "Forecast type non readable or not in agreeance with Entity Type")


        except Exception as e:
            self.forecasts_output.insert(tk.END, f"An error occurred: {str(e)}")
            messagebox.showerror("Error", str(e))

    def display_dataframe_csv(self, df, frame, column):
        # Create a Treeview widget show='headings'
        tree = ttk.Treeview(frame, columns=['Time', column])
        tree.pack(side='left', fill='both', expand=True)
        tree.column("#0", width=0, stretch=tk.NO)

        # Add columns
        for col in ['Time', column]:
            tree.heading(col, text=col)
            tree.column(col, anchor='center')

        # Add rows
        for index, row in df.iterrows():
            tree.insert('', 'end', values=list(row))

    def browse_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.csv_path_entry.insert(tk.END, file_path)
            self.load_csv(file_path)

    def create_csv(self):
        try:
            generate_sample_power_data(self.entities_list)
            # Show success message using showinfo
            messagebox.showinfo("Success", "CSV with sample data has been successfully created!")
        except Exception as e:
            # Show error message using showerror
            messagebox.showerror("Error", str(e))

    def load_csv(self, file_path):
        try:
            self.df = pd.read_csv(file_path)
            self.create_column_buttons()
        except Exception as e: (
            messagebox.showerror("Error", f"Failed to load CSV: {e}"))

    def create_column_buttons(self):
        for widget in self.csv_buttons_frame.winfo_children():
            widget.destroy()

        for i, column in enumerate(self.df.columns):
            if column != 'Time':
                button = ttk.Button(self.csv_buttons_frame, text=column,
                                                           command=lambda col=column: self.select_column(col))
                button.grid(row=i-1, column=0, padx=5, pady=5, sticky='ew')

        for col in range(1):
            self.csv_buttons_frame.columnconfigure(col, weight=1)
        for row in range(0,5):
            self.csv_buttons_frame.rowconfigure(row, weight=1)

    def select_column(self, column):
        for widget in self.csv_output.winfo_children():
            widget.destroy()
        try:
            column_data = self.df[column].dropna().tolist()
            power_values = ",".join(map(str, column_data))
            self.submit_power_values_entry.delete(0, tk.END)
            self.submit_power_values_entry.insert(0, power_values)
            self.csv_col_entry.delete(0, tk.END)
            self.csv_col_entry.insert(0, column)
            self.display_dataframe(self.df.loc[:,['Time', column]], self.csv_output)
        except Exception as e: (
            messagebox.showerror("Error",f"Failed to process column: {e}"))



    def submit_forecast(self):
        try:
            # Retrieve power values from the input field
            power_values = list(map(float, self.submit_power_values_entry.get().split(',')))

            # Retrieve time values from the "Time" column of the dataframe
            time_values = [
                pd.to_datetime(t).strftime("%Y-%m-%dT%H:%M:%S%z")
                for t in self.df["Time"]
            ]

            time_values = [
                time[:-2] + ':' + time[-2:] if '+' in time or '-' in time else time
                for time in time_values
            ]

            # Retrieve additional input values
            category_id = self.submit_category_id_entry.get()
            schedule_id = self.submit_schedule_id_entry.get()
            entity_asset_id = self.submit_entity_asset_id_entry.get()
            forecast_type = self.submit_forecast_type_entry.get()

            # Validate forecast type and category
            if not ((('Wind' in forecast_type) and (category_id == 'WPLANT')) or
                    (('Solar' in forecast_type) and (category_id == 'SPLANT'))):
                messagebox.showerror("Incorrect Parameters",
                                     "Forecast type not writeable or not in agreement with Entity Type")
                return

            # Call the updated submit_forecast function
            result = submit_forecast(client, category_id, schedule_id, entity_asset_id, power_values, time_values)

            # Display the result
            self.submit_output.delete(1.0, tk.END)
            if result is not None:
                formatted = f"Success! Here is your transaction id: \n\n\t{result['transactionId']}"
                self.submit_output.insert(tk.END, formatted)
            else:
                self.submit_output.insert(tk.END, "Query did not succeed")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    if ENDPOINT_URL == "https://smd.iso-ne.com/wpfmui/webservices/WindPlantLeadParticipant/1_0/?wsdl":
        print("Error: You cannot use the production URL in the GUI.")
        print("Change the 'ENDPOINT_URL' variable in the 'Properties.py' file to the sandbox URL.")
        exit(1)  # Exit the program with an error code
    else:
        root = tk.Tk()
        app = APIClientGUI(root)
        root.mainloop()




