import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import os
import json
from PIL import Image, ImageTk
import random
from datetime import datetime
import math

class FemurOsteonaDistributor:
    def __init__(self, root):
        self.root = root
        self.root.title("Femur Osteona Distributor - Anatomically Correct")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f0f0")
        
        # Configurar el comportamiento al cerrar la ventana
        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

        # Configurar estilo
        self.configure_style()
        
        # Variables de longitud y proporciones (sin cambios)
        self.femur_length = tk.DoubleVar(value=45.0)  # Valor por defecto en cm
        self.epiphysis_proximal_percent = tk.DoubleVar(value=15.0)
        self.metaphysis_proximal_percent = tk.DoubleVar(value=10.0)
        self.diaphysis_percent = tk.DoubleVar(value=50.0)
        self.metaphysis_distal_percent = tk.DoubleVar(value=10.0)
        self.epiphysis_distal_percent = tk.DoubleVar(value=15.0)
        
        # NUEVAS VARIABLES: Radios anatómicos por sección (en cm)
        self.radius_epiphysis_proximal = tk.DoubleVar(value=2.5)
        self.radius_metaphysis_proximal = tk.DoubleVar(value=1.5)
        self.radius_diaphysis = tk.DoubleVar(value=1.0)
        self.radius_metaphysis_distal = tk.DoubleVar(value=1.8)
        self.radius_epiphysis_distal = tk.DoubleVar(value=3.0)
        
        # DENSIDADES CORREGIDAS: Basadas en literatura científica (osteonas/cm²)
        self.density_epiphysis_proximal = tk.DoubleVar(value=1500.0)  # Era 25.0
        self.density_metaphysis_proximal = tk.DoubleVar(value=1800.0)  # Era 40.0
        self.density_diaphysis = tk.DoubleVar(value=2000.0)  # Era 60.0
        self.density_metaphysis_distal = tk.DoubleVar(value=1800.0)  # Era 40.0
        self.density_epiphysis_distal = tk.DoubleVar(value=1500.0)  # Era 25.0
        
        # Dimensiones de las osteonas por sección (diámetro en micrómetros)
        self.osteona_size_epiphysis_proximal = tk.DoubleVar(value=200.0)
        self.osteona_size_metaphysis_proximal = tk.DoubleVar(value=180.0)
        self.osteona_size_diaphysis = tk.DoubleVar(value=150.0)
        self.osteona_size_metaphysis_distal = tk.DoubleVar(value=180.0)
        self.osteona_size_epiphysis_distal = tk.DoubleVar(value=200.0)
        
        # Factor de variabilidad en la distribución - VALORES AJUSTADOS
        self.variability_epiphysis_proximal = tk.DoubleVar(value=0.05)  # Era 0.7
        self.variability_metaphysis_proximal = tk.DoubleVar(value=0.05)  # Era 0.5
        self.variability_diaphysis = tk.DoubleVar(value=0.05)  # Era 0.3
        self.variability_metaphysis_distal = tk.DoubleVar(value=0.05)  # Era 0.5
        self.variability_epiphysis_distal = tk.DoubleVar(value=0.05)  # Era 0.7
        
        # Crear la interfaz de usuario
        self.create_ui()
        
        # Datos calculados
        self.sections_data = None
        self.distribution_data = None
        
        # Calcular inicialmente
        self.calculate()
    
    def configure_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        # Configurar estilos de widget
        style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
        style.configure("TButton", font=("Arial", 10, "bold"))
        style.configure("TFrame", background="#f0f0f0")
        style.configure("Header.TLabel", font=("Arial", 12, "bold"))
        style.configure("Section.TLabel", font=("Arial", 11, "bold"), foreground="#3366cc")
        
        # Configurar pestañas
        style.configure("TNotebook", background="#f0f0f0", borderwidth=0)
        style.configure("TNotebook.Tab", background="#e0e0e0", padding=[10, 5], font=("Arial", 10))
        style.map("TNotebook.Tab", background=[("selected", "#f0f0f0")])
    
    def create_ui(self):
        # Crear notebook (pestañas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Pestaña 1: Parámetros
        self.tab_params = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_params, text="Parámetros")
        
        # Pestaña 2: Visualización
        self.tab_visualization = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_visualization, text="Visualización")
        
        # Pestaña 3: Exportación
        self.tab_export = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_export, text="Exportación")
        
        # Configurar las pestañas
        self.setup_params_tab()
        self.setup_visualization_tab()
        self.setup_export_tab()
    
    def setup_params_tab(self):
        # Marco para entrada de datos
        input_frame = ttk.LabelFrame(self.tab_params, text="Parámetros del Fémur")
        input_frame.pack(fill="both", expand=False, padx=10, pady=10)
        
        # Longitud del fémur
        ttk.Label(input_frame, text="Longitud del Fémur (cm):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(input_frame, textvariable=self.femur_length, width=10).grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        # Marco para porcentajes de secciones
        sections_frame = ttk.LabelFrame(self.tab_params, text="Proporciones y Propiedades Anatómicas")
        sections_frame.pack(fill="both", expand=False, padx=10, pady=10)
        
        # Etiquetas de columnas ACTUALIZADAS
        ttk.Label(sections_frame, text="Sección").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Label(sections_frame, text="% Longitud").grid(row=0, column=1, padx=5, pady=5, sticky="w")
        ttk.Label(sections_frame, text="Radio (cm)").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        ttk.Label(sections_frame, text="Densidad (ost/cm²)").grid(row=0, column=3, padx=5, pady=5, sticky="w")
        ttk.Label(sections_frame, text="Tamaño (μm)").grid(row=0, column=4, padx=5, pady=5, sticky="w")
        ttk.Label(sections_frame, text="Variabilidad (0-1)").grid(row=0, column=5, padx=5, pady=5, sticky="w")
        
        # Epífisis proximal
        ttk.Label(sections_frame, text="Epífisis Proximal").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(sections_frame, textvariable=self.epiphysis_proximal_percent, width=8).grid(row=1, column=1, padx=5, pady=5, sticky="w")
        ttk.Entry(sections_frame, textvariable=self.radius_epiphysis_proximal, width=8).grid(row=1, column=2, padx=5, pady=5, sticky="w")
        ttk.Entry(sections_frame, textvariable=self.density_epiphysis_proximal, width=8).grid(row=1, column=3, padx=5, pady=5, sticky="w")
        ttk.Entry(sections_frame, textvariable=self.osteona_size_epiphysis_proximal, width=8).grid(row=1, column=4, padx=5, pady=5, sticky="w")
        ttk.Entry(sections_frame, textvariable=self.variability_epiphysis_proximal, width=8).grid(row=1, column=5, padx=5, pady=5, sticky="w")
        
        # Metáfisis proximal
        ttk.Label(sections_frame, text="Metáfisis Proximal").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(sections_frame, textvariable=self.metaphysis_proximal_percent, width=8).grid(row=2, column=1, padx=5, pady=5, sticky="w")
        ttk.Entry(sections_frame, textvariable=self.radius_metaphysis_proximal, width=8).grid(row=2, column=2, padx=5, pady=5, sticky="w")
        ttk.Entry(sections_frame, textvariable=self.density_metaphysis_proximal, width=8).grid(row=2, column=3, padx=5, pady=5, sticky="w")
        ttk.Entry(sections_frame, textvariable=self.osteona_size_metaphysis_proximal, width=8).grid(row=2, column=4, padx=5, pady=5, sticky="w")
        ttk.Entry(sections_frame, textvariable=self.variability_metaphysis_proximal, width=8).grid(row=2, column=5, padx=5, pady=5, sticky="w")
        
        # Diáfisis
        ttk.Label(sections_frame, text="Diáfisis").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(sections_frame, textvariable=self.diaphysis_percent, width=8).grid(row=3, column=1, padx=5, pady=5, sticky="w")
        ttk.Entry(sections_frame, textvariable=self.radius_diaphysis, width=8).grid(row=3, column=2, padx=5, pady=5, sticky="w")
        ttk.Entry(sections_frame, textvariable=self.density_diaphysis, width=8).grid(row=3, column=3, padx=5, pady=5, sticky="w")
        ttk.Entry(sections_frame, textvariable=self.osteona_size_diaphysis, width=8).grid(row=3, column=4, padx=5, pady=5, sticky="w")
        ttk.Entry(sections_frame, textvariable=self.variability_diaphysis, width=8).grid(row=3, column=5, padx=5, pady=5, sticky="w")
        
        # Metáfisis distal
        ttk.Label(sections_frame, text="Metáfisis Distal").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(sections_frame, textvariable=self.metaphysis_distal_percent, width=8).grid(row=4, column=1, padx=5, pady=5, sticky="w")
        ttk.Entry(sections_frame, textvariable=self.radius_metaphysis_distal, width=8).grid(row=4, column=2, padx=5, pady=5, sticky="w")
        ttk.Entry(sections_frame, textvariable=self.density_metaphysis_distal, width=8).grid(row=4, column=3, padx=5, pady=5, sticky="w")
        ttk.Entry(sections_frame, textvariable=self.osteona_size_metaphysis_distal, width=8).grid(row=4, column=4, padx=5, pady=5, sticky="w")
        ttk.Entry(sections_frame, textvariable=self.variability_metaphysis_distal, width=8).grid(row=4, column=5, padx=5, pady=5, sticky="w")
        
        # Epífisis distal
        ttk.Label(sections_frame, text="Epífisis Distal").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(sections_frame, textvariable=self.epiphysis_distal_percent, width=8).grid(row=5, column=1, padx=5, pady=5, sticky="w")
        ttk.Entry(sections_frame, textvariable=self.radius_epiphysis_distal, width=8).grid(row=5, column=2, padx=5, pady=5, sticky="w")
        ttk.Entry(sections_frame, textvariable=self.density_epiphysis_distal, width=8).grid(row=5, column=3, padx=5, pady=5, sticky="w")
        ttk.Entry(sections_frame, textvariable=self.osteona_size_epiphysis_distal, width=8).grid(row=5, column=4, padx=5, pady=5, sticky="w")
        ttk.Entry(sections_frame, textvariable=self.variability_epiphysis_distal, width=8).grid(row=5, column=5, padx=5, pady=5, sticky="w")
        
        # Botón de cálculo
        calculate_button = ttk.Button(
            self.tab_params, 
            text="Calcular Distribución", 
            command=self.calculate
        )
        calculate_button.pack(pady=10)
        
        # Marco para resultados
        self.results_frame = ttk.LabelFrame(self.tab_params, text="Resultados del Cálculo")
        self.results_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Texto para mostrar resultados
        self.results_text = tk.Text(self.results_frame, height=10, width=80)
        self.results_text.pack(fill="both", expand=True, padx=5, pady=5)
    
    def setup_visualization_tab(self):
        # Crear figura y ejes para los gráficos
        self.figure, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(12, 6))
        self.figure.tight_layout(pad=3.0)
        
        # Canvas para mostrar la figura
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.tab_visualization)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)
        
        # Marco para controles
        controls_frame = ttk.Frame(self.tab_visualization)
        controls_frame.pack(fill="x", padx=10, pady=5)
        
        # Botones
        update_button = ttk.Button(
            controls_frame, 
            text="Actualizar Visualización", 
            command=self.update_visualization
        )
        update_button.pack(side="left", padx=5)
        
        save_button = ttk.Button(
            controls_frame, 
            text="Guardar Imagen", 
            command=self.save_visualization
        )
        save_button.pack(side="left", padx=5)
    
    def setup_export_tab(self):
        # Marco para opciones de exportación
        export_frame = ttk.LabelFrame(self.tab_export, text="Opciones de Exportación")
        export_frame.pack(fill="both", expand=False, padx=10, pady=10)
        
        # Botones de exportación
        ttk.Button(
            export_frame, 
            text="Exportar a CSV (Para Grasshopper)", 
            command=lambda: self.export_data("csv")
        ).pack(fill="x", padx=10, pady=5)
        
        ttk.Button(
            export_frame, 
            text="Exportar a JSON", 
            command=lambda: self.export_data("json")
        ).pack(fill="x", padx=10, pady=5)
        
        ttk.Button(
            export_frame, 
            text="Exportar Informe Completo", 
            command=self.export_report
        ).pack(fill="x", padx=10, pady=5)
        
        # Marco para previsualización
        preview_frame = ttk.LabelFrame(self.tab_export, text="Previsualización de Datos")
        preview_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Texto para mostrar previsualización
        self.preview_text = tk.Text(preview_frame, height=20, width=80)
        preview_scroll = ttk.Scrollbar(preview_frame, command=self.preview_text.yview)
        self.preview_text.configure(yscrollcommand=preview_scroll.set)
        
        self.preview_text.pack(side="left", fill="both", expand=True)
        preview_scroll.pack(side="right", fill="y")
    
    def calculate(self):
        try:
            # Obtener la longitud total
            total_length = self.femur_length.get()
            
            # Verificar que los porcentajes suman 100%
            total_percent = (
                self.epiphysis_proximal_percent.get() +
                self.metaphysis_proximal_percent.get() +
                self.diaphysis_percent.get() +
                self.metaphysis_distal_percent.get() +
                self.epiphysis_distal_percent.get()
            )
            
            if abs(total_percent - 100.0) > 0.01:
                messagebox.showwarning("Advertencia", 
                                      f"Los porcentajes de las secciones suman {total_percent}%, no 100%")
                return
            
            # Calcular longitudes absolutas de cada sección
            ep_prox_length = total_length * (self.epiphysis_proximal_percent.get() / 100)
            met_prox_length = total_length * (self.metaphysis_proximal_percent.get() / 100)
            dia_length = total_length * (self.diaphysis_percent.get() / 100)
            met_dist_length = total_length * (self.metaphysis_distal_percent.get() / 100)
            ep_dist_length = total_length * (self.epiphysis_distal_percent.get() / 100)
            
            # Calcular puntos de inicio y fin de cada sección
            ep_prox_start = 0
            ep_prox_end = ep_prox_length
            
            met_prox_start = ep_prox_end
            met_prox_end = met_prox_start + met_prox_length
            
            dia_start = met_prox_end
            dia_end = dia_start + dia_length
            
            met_dist_start = dia_end
            met_dist_end = met_dist_start + met_dist_length
            
            ep_dist_start = met_dist_end
            ep_dist_end = total_length
            
            # ALMACENAR DATOS DE SECCIONES CON RADIOS
            self.sections_data = {
                "total_length_cm": total_length,
                "sections": [
                    {
                        "name": "Epífisis Proximal",
                        "start_cm": ep_prox_start,
                        "end_cm": ep_prox_end,
                        "length_cm": ep_prox_length,
                        "percent": self.epiphysis_proximal_percent.get(),
                        "radius_cm": self.radius_epiphysis_proximal.get(),
                        "density_per_cm2": self.density_epiphysis_proximal.get(),
                        "osteona_size_um": self.osteona_size_epiphysis_proximal.get(),
                        "variability": self.variability_epiphysis_proximal.get()
                    },
                    {
                        "name": "Metáfisis Proximal",
                        "start_cm": met_prox_start,
                        "end_cm": met_prox_end,
                        "length_cm": met_prox_length,
                        "percent": self.metaphysis_proximal_percent.get(),
                        "radius_cm": self.radius_metaphysis_proximal.get(),
                        "density_per_cm2": self.density_metaphysis_proximal.get(),
                        "osteona_size_um": self.osteona_size_metaphysis_proximal.get(),
                        "variability": self.variability_metaphysis_proximal.get()
                    },
                    {
                        "name": "Diáfisis",
                        "start_cm": dia_start,
                        "end_cm": dia_end,
                        "length_cm": dia_length,
                        "percent": self.diaphysis_percent.get(),
                        "radius_cm": self.radius_diaphysis.get(),
                        "density_per_cm2": self.density_diaphysis.get(),
                        "osteona_size_um": self.osteona_size_diaphysis.get(),
                        "variability": self.variability_diaphysis.get()
                    },
                    {
                        "name": "Metáfisis Distal",
                        "start_cm": met_dist_start,
                        "end_cm": met_dist_end,
                        "length_cm": met_dist_length,
                        "percent": self.metaphysis_distal_percent.get(),
                        "radius_cm": self.radius_metaphysis_distal.get(),
                        "density_per_cm2": self.density_metaphysis_distal.get(),
                        "osteona_size_um": self.osteona_size_metaphysis_distal.get(),
                        "variability": self.variability_metaphysis_distal.get()
                    },
                    {
                        "name": "Epífisis Distal",
                        "start_cm": ep_dist_start,
                        "end_cm": ep_dist_end,
                        "length_cm": ep_dist_length,
                        "percent": self.epiphysis_distal_percent.get(),
                        "radius_cm": self.radius_epiphysis_distal.get(),
                        "density_per_cm2": self.density_epiphysis_distal.get(),
                        "osteona_size_um": self.osteona_size_epiphysis_distal.get(),
                        "variability": self.variability_epiphysis_distal.get()
                    }
                ]
            }
            
            # Generar distribución de osteonas
            self.generate_osteona_distribution()
            
            # Mostrar resultados
            self.display_results()
            
            # Actualizar visualización y previsualización
            self.update_visualization()
            self.update_preview()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en el cálculo: {str(e)}")
            raise e
        
    def close_app(self):
        import sys
        try:
            plt.close('all')
            self.root.quit()
            self.root.destroy()
        except:
            pass
        sys.exit()
        
    def generate_osteona_distribution(self):
        """Genera distribución anatómicamente correcta con transiciones suaves"""
        distribution_data = []
        
        # Para cada sección, generar las osteonas principales
        for i, section in enumerate(self.sections_data["sections"]):
            # Usar área circular real π*r²
            radius_cm = section["radius_cm"]
            section_area = math.pi * (radius_cm ** 2)
            
            # Calcular número de osteonas usando densidad real
            num_osteonas = int(section_area * section["density_per_cm2"])
            
            section_osteonas = []
            
            # Generar osteonas principales con distribución mejorada
            for j in range(num_osteonas):
                # Coordenadas X,Y dentro del radio
                x, y = self.generate_xy_position(radius_cm, section["variability"])
                
                # Posición longitudinal Z con distribución mejorada
                pos_z = self.generate_position_improved(
                    0, 
                    section["length_cm"], 
                    section["variability"]
                )
                
                # Posición absoluta en el hueso
                abs_pos_z = section["start_cm"] + pos_z
                
                # Calcular tamaño aleatorio de la osteona
                size_variation = 0.2
                size = section["osteona_size_um"] * (1 + random.uniform(-size_variation, size_variation))
                
                # Agregar osteona
                section_osteonas.append({
                    "section_name": section["name"],
                    "position_x_cm": x,
                    "position_y_cm": y,
                    "position_z_cm": abs_pos_z,
                    "size_um": size
                })
            
            distribution_data.extend(section_osteonas)
            
            # Añadir osteonas de transición entre secciones
            if i < len(self.sections_data["sections"]) - 1:  # Si no es la última sección
                next_section = self.sections_data["sections"][i + 1]
                transition_osteonas = self.generate_transition_osteonas(section, next_section)
                distribution_data.extend(transition_osteonas)
        
        # Guardar los datos
        self.distribution_data = distribution_data
    
    def generate_xy_position(self, radius_cm, variability):
        """
        Genera coordenadas X,Y dentro de un círculo de radio dado
        
        Args:
            radius_cm: Radio de la sección en cm
            variability: Factor de variabilidad para la distribución
            
        Returns:
            Tupla (x, y) en cm
        """
        # Para variabilidad baja, distribución más uniforme
        if variability < 0.3:
            # Distribución uniforme dentro del círculo
            angle = random.uniform(0, 2 * math.pi)
            r = radius_cm * math.sqrt(random.uniform(0, 1))  # Distribución uniforme en área
            
        elif variability < 0.7:
            # Distribución normal centrada (más osteonas hacia el centro)
            angle = random.uniform(0, 2 * math.pi)
            # Distribución normal truncada para el radio
            r = radius_cm * math.sqrt(random.uniform(0, 1))
            r = min(r, radius_cm)  # Asegurar que no exceda el radio
            
        else:
            # Variabilidad alta: más concentración en el borde cortical
            angle = random.uniform(0, 2 * math.pi)
            if random.random() < 0.7:  # 70% cerca del borde
                r = radius_cm * random.uniform(0.7, 1.0)
            else:  # 30% distribuido uniformemente
                r = radius_cm * math.sqrt(random.uniform(0, 1))
        
        # Convertir coordenadas polares a cartesianas
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        
        return x, y
    
    def generate_transition_osteonas(self, section1, section2):
        """
        Genera osteonas en la zona de transición entre dos secciones
        para crear transiciones suaves y eliminar espacios vacíos
        """
        transition_osteonas = []
        
        # Zona de transición: 0.5 cm antes y después del límite entre secciones
        transition_zone = 0.5  # cm
        transition_start = max(0, section1["end_cm"] - transition_zone)
        transition_end = min(self.sections_data["total_length_cm"], section2["start_cm"] + transition_zone)
        transition_length = transition_end - transition_start
        
        if transition_length <= 0:
            return transition_osteonas
        
        # Calcular radio de transición (promedio de ambas secciones)
        avg_radius = (section1["radius_cm"] + section2["radius_cm"]) / 2
        avg_density = (section1["density_per_cm2"] + section2["density_per_cm2"]) / 2
        avg_size = (section1["osteona_size_um"] + section2["osteona_size_um"]) / 2
        
        # Área de transición
        transition_area = math.pi * (avg_radius ** 2)
        
        # Número de osteonas de transición (30% de la densidad normal)
        num_transition = int(transition_area * avg_density * 0.3 * (transition_length / section1["length_cm"]))
        
        # Generar osteonas de transición
        for i in range(num_transition):
            # Coordenadas X,Y con radio de transición
            x, y = self.generate_xy_position(avg_radius, 0.2)  # Baja variabilidad para transición suave
            
            # Coordenada Z en la zona de transición
            pos_z = random.uniform(transition_start, transition_end)
            
            # Tamaño promedio
            size = avg_size * (1 + random.uniform(-0.1, 0.1))  # Menor variación
            
            # Determinar nombre de sección (más cercana)
            if pos_z < section1["end_cm"]:
                section_name = section1["name"]
            else:
                section_name = section2["name"]
            
            transition_osteonas.append({
                "section_name": f"{section_name} (transición)",
                "position_x_cm": x,
                "position_y_cm": y,
                "position_z_cm": pos_z,
                "size_um": size
            })
        
        return transition_osteonas
    
    def generate_position_improved(self, min_val, max_val, variability):
        """
        Genera una posición aleatoria con distribución más uniforme
        y menos concentración extrema en los bordes
        
        Args:
            min_val: Valor mínimo del rango
            max_val: Valor máximo del rango
            variability: Factor de variabilidad (0.0 = uniforme, 1.0 = variable)
            
        Returns:
            Posición generada
        """
        # Para variabilidad muy baja, distribución completamente uniforme
        if variability < 0.2:
            return random.uniform(min_val, max_val)
        
        # Para variabilidad baja-media, distribución normal centrada
        elif variability < 0.4:
            mean = (max_val + min_val) / 2
            std_dev = (max_val - min_val) / 8  # Más concentración hacia el centro
            val = np.random.normal(mean, std_dev)
            # Asegurar que el valor está dentro del rango
            return max(min_val, min(max_val, val))
        
        # Para variabilidad media-alta, distribución mixta más suave
        else:
            # 60% distribución normal centrada, 40% uniforme
            if random.random() < 0.6:
                mean = (max_val + min_val) / 2
                std_dev = (max_val - min_val) / 6
                val = np.random.normal(mean, std_dev)
                return max(min_val, min(max_val, val))
            else:
                return random.uniform(min_val, max_val)
    
    def generate_position(self, min_val, max_val, variability):
        """
        Función original mantenida para compatibilidad
        """
        return self.generate_position_improved(min_val, max_val, variability)
    
    def display_results(self):
        """Muestra los resultados incluyendo información de radios"""
        if not self.sections_data:
            return
            
        # Limpiar el área de texto
        self.results_text.delete(1.0, tk.END)
        
        # Mostrar información general
        self.results_text.insert(tk.END, f"FÉMUR ANATÓMICAMENTE CORRECTO\n")
        self.results_text.insert(tk.END, f"{'='*50}\n\n")
        self.results_text.insert(tk.END, f"Longitud total del fémur: {self.sections_data['total_length_cm']:.2f} cm\n\n")
        
        # Mostrar información de cada sección con áreas calculadas
        total_area = 0
        total_osteonas_calculated = 0
        
        for section in self.sections_data["sections"]:
            area_cm2 = math.pi * (section['radius_cm'] ** 2)
            osteonas_section = int(area_cm2 * section['density_per_cm2'])
            total_area += area_cm2
            total_osteonas_calculated += osteonas_section
            
            self.results_text.insert(tk.END, f"Sección: {section['name']}\n")
            self.results_text.insert(tk.END, f"  - Inicio: {section['start_cm']:.2f} cm\n")
            self.results_text.insert(tk.END, f"  - Fin: {section['end_cm']:.2f} cm\n")
            self.results_text.insert(tk.END, f"  - Longitud: {section['length_cm']:.2f} cm ({section['percent']:.1f}%)\n")
            self.results_text.insert(tk.END, f"  - Radio: {section['radius_cm']:.2f} cm\n")
            self.results_text.insert(tk.END, f"  - Área circular: {area_cm2:.2f} cm²\n")
            self.results_text.insert(tk.END, f"  - Densidad: {section['density_per_cm2']:.0f} osteonas/cm²\n")
            self.results_text.insert(tk.END, f"  - Osteonas calculadas: {osteonas_section:,}\n")
            self.results_text.insert(tk.END, f"  - Tamaño medio: {section['osteona_size_um']:.1f} μm\n")
            self.results_text.insert(tk.END, f"  - Variabilidad: {section['variability']:.2f}\n\n")
        
        # Mostrar estadísticas de la distribución
        self.results_text.insert(tk.END, f"ESTADÍSTICAS TOTALES\n")
        self.results_text.insert(tk.END, f"{'='*30}\n")
        self.results_text.insert(tk.END, f"Área cortical total: {total_area:.2f} cm²\n")
        self.results_text.insert(tk.END, f"Osteonas calculadas: {total_osteonas_calculated:,}\n")
        
        if self.distribution_data:
            num_osteonas = len(self.distribution_data)
            self.results_text.insert(tk.END, f"Osteonas generadas: {num_osteonas:,}\n")
            self.results_text.insert(tk.END, f"Densidad promedio: {num_osteonas/total_area:.0f} ost/cm²\n\n")
            
            # Contar osteonas por sección
            section_counts = {}
            for osteona in self.distribution_data:
                section = osteona["section_name"]
                if section not in section_counts:
                    section_counts[section] = 0
                section_counts[section] += 1
            
            self.results_text.insert(tk.END, "DISTRIBUCIÓN POR SECCIÓN:\n")
            for section, count in section_counts.items():
                self.results_text.insert(tk.END, f"  - {section}: {count:,} osteonas ({count/num_osteonas*100:.1f}%)\n")
    
    def update_visualization(self):
        """Visualización mejorada con forma anatómica"""
        if not self.sections_data or not self.distribution_data:
            return
            
        # Limpiar los ejes
        self.ax1.clear()
        self.ax2.clear()
        
        # Colores para las secciones
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0']
        
        # GRÁFICO 1: Perfil anatómico real del fémur con radios variables
        z_bone = np.linspace(0, self.sections_data["total_length_cm"], 1000)
        radius_bone = np.zeros_like(z_bone)
        
        # Crear forma anatómica real basada en los radios de cada sección
        for i, z in enumerate(z_bone):
            # Encontrar en qué sección estamos
            current_radius = 1.0  # valor por defecto
            for section in self.sections_data["sections"]:
                if section["start_cm"] <= z <= section["end_cm"]:
                    current_radius = section["radius_cm"]
                    break
            radius_bone[i] = current_radius
        
        # Dibujar el perfil del fémur con relleno
        self.ax1.fill_between(z_bone, radius_bone, -radius_bone, 
                            color='lightgray', alpha=0.3, label='Perfil del fémur')
        
        # Dibujar los contornos
        self.ax1.plot(z_bone, radius_bone, 'k-', linewidth=2)
        self.ax1.plot(z_bone, -radius_bone, 'k-', linewidth=2)
        
        # Sombrear las diferentes secciones con colores
        for i, section in enumerate(self.sections_data["sections"]):
            start_pos = section["start_cm"]
            end_pos = section["end_cm"]
            radius = section["radius_cm"]
            
            # Crear un relleno para cada sección
            z_section = np.linspace(start_pos, end_pos, 100)
            radius_section = np.full_like(z_section, radius)
            
            self.ax1.fill_between(
                z_section, 
                radius_section, 
                -radius_section, 
                color=colors[i], 
                alpha=0.7, 
                label=section["name"]
            )
            
            # Dibujar líneas de separación verticales
            if start_pos > 0:
                self.ax1.axvline(x=start_pos, color='black', linestyle='--', alpha=0.8, linewidth=1)
        
        # Configurar gráfico 1
        self.ax1.set_title('Perfil Anatómico del Fémur con Radios Variables', fontsize=12, fontweight='bold')
        self.ax1.set_xlabel('Longitud (cm)')
        self.ax1.set_ylabel('Radio (cm)')
        self.ax1.grid(True, linestyle='--', alpha=0.3)
        self.ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=3, fontsize=9)
        self.ax1.set_aspect('equal', adjustable='box')
        
        # GRÁFICO 2: Vista superior (distribución X,Y) por secciones
        x_positions = [osteona["position_x_cm"] for osteona in self.distribution_data]
        y_positions = [osteona["position_y_cm"] for osteona in self.distribution_data]
        colors_scatter = []
        
        # Asignar colores según la sección
        for osteona in self.distribution_data:
            section_name = osteona["section_name"]
            # Buscar color de la sección base (sin "(transición)")
            base_section_name = section_name.replace(" (transición)", "")
            idx = next((i for i, s in enumerate(self.sections_data["sections"]) if s["name"] == base_section_name), 0)
            colors_scatter.append(colors[idx])
        
        # Crear scatter plot de vista superior
        self.ax2.scatter(x_positions, y_positions, c=colors_scatter, s=1, alpha=0.6)
        
        # Dibujar círculos que representan los límites de cada sección
        for i, section in enumerate(self.sections_data["sections"]):
            circle = plt.Circle((0, 0), section["radius_cm"], 
                              fill=False, color=colors[i], linestyle='--', alpha=0.8, linewidth=2)
            self.ax2.add_patch(circle)
        
        # Configurar gráfico 2
        self.ax2.set_title('Vista Superior - Distribución Radial de Osteonas', fontsize=12, fontweight='bold')
        self.ax2.set_xlabel('Posición X (cm)')
        self.ax2.set_ylabel('Posición Y (cm)')
        self.ax2.set_aspect('equal', adjustable='box')
        self.ax2.grid(True, linestyle='--', alpha=0.3)
        
        # Establecer límites para mostrar la sección más grande
        max_radius = max(section["radius_cm"] for section in self.sections_data["sections"])
        self.ax2.set_xlim(-max_radius*1.1, max_radius*1.1)
        self.ax2.set_ylim(-max_radius*1.1, max_radius*1.1)
        
        # Añadir información estadística
        if self.distribution_data:
            stats_text = f'Total osteonas: {len(self.distribution_data):,}\n'
            stats_text += f'Rango radial: {max_radius:.1f} cm\n'
            stats_text += f'Densidad media: {len(self.distribution_data)/(math.pi * max_radius**2):.0f} ost/cm²'
            
            self.ax2.text(0.02, 0.98, stats_text, transform=self.ax2.transAxes, 
                        verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
                        fontsize=9)
        
        # Ajustar diseño para evitar solapamientos
        self.figure.tight_layout(pad=3.0)
        self.canvas.draw()
    
    def save_visualization(self):
        """Guarda los gráficos de visualización como imagen"""
        if not self.sections_data:
            messagebox.showwarning("Advertencia", "No hay datos para guardar.")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("PDF", "*.pdf")],
            title="Guardar Visualización"
        )
        
        if file_path:
            try:
                self.figure.savefig(file_path, dpi=300, bbox_inches='tight')
                messagebox.showinfo("Éxito", f"Visualización guardada en {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar la visualización: {str(e)}")
    
    def update_preview(self):
        """Previsualización con coordenadas X,Y,Z (sin ángulo)"""
        if not self.distribution_data:
            return
            
        # Limpiar el área de previsualización
        self.preview_text.delete(1.0, tk.END)
        
        # Mostrar los primeros 20 registros (o menos si hay menos)
        num_preview = min(20, len(self.distribution_data))
        
        self.preview_text.insert(tk.END, "PREVISUALIZACIÓN DE DATOS OPTIMIZADOS (primeros 20 registros):\n\n")
        self.preview_text.insert(tk.END, "section_name, position_x_cm, position_y_cm, position_z_cm, size_um\n")
        self.preview_text.insert(tk.END, "-" * 70 + "\n")
        
        for i in range(num_preview):
            osteona = self.distribution_data[i]
            self.preview_text.insert(
                tk.END, 
                f"{osteona['section_name']}, {osteona['position_x_cm']:.3f}, {osteona['position_y_cm']:.3f}, "
                f"{osteona['position_z_cm']:.3f}, {osteona['size_um']:.2f}\n"
            )
        
        self.preview_text.insert(tk.END, f"\n... (Total: {len(self.distribution_data):,} registros)\n\n")
        self.preview_text.insert(tk.END, "DATOS PARA GRASSHOPPER:\n")
        self.preview_text.insert(tk.END, "- position_x_cm, position_y_cm, position_z_cm: Coordenadas cartesianas 3D del centro\n")
        self.preview_text.insert(tk.END, "- size_um: Diámetro de la osteona en micrómetros\n")
        self.preview_text.insert(tk.END, "- Radio de osteona: size_um / 2\n")
    
    def export_data(self, format_type):
        """Exporta los datos incluyendo coordenadas X,Y,Z"""
        if not self.distribution_data:
            messagebox.showwarning("Advertencia", "No hay datos para exportar.")
            return
            
        # Determinar la ruta del archivo
        if format_type == "csv":
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV", "*.csv")],
                title="Exportar a CSV"
            )
        else:  # JSON
            file_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON", "*.json")],
                title="Exportar a JSON"
            )
        
        if not file_path:
            return
            
        try:
            if format_type == "csv":
                # Convertir a DataFrame y guardar como CSV
                df = pd.DataFrame(self.distribution_data)
                
                # Ordenar el DataFrame por position_z_cm de menor a mayor
                df = df.sort_values(by='position_z_cm', ascending=True)

                # Guardar como CSV
                df.to_csv(file_path, index=False)
            else:  # JSON
                # Ordenar la lista de osteonas por position_z_cm
                sorted_data = sorted(self.distribution_data, key=lambda x: x['position_z_cm'])

                # Guardar como JSON
                data = {
                    "femur_info": self.sections_data,
                    "osteonas": sorted_data  # Usar la lista ordenada
                }
                
                with open(file_path, 'w') as f:
                    json.dump(data, f, indent=4)
            
            messagebox.showinfo("Éxito", f"Datos exportados a {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar los datos: {str(e)}")
    
    def export_report(self):
        """Exporta un informe completo"""
        if not self.sections_data or not self.distribution_data:
            messagebox.showwarning("Advertencia", "No hay datos para generar un informe.")
            return
            
        # Determinar la ruta de la carpeta
        folder_path = filedialog.askdirectory(
            title="Seleccionar Carpeta para Informe"
        )
        
        if not folder_path:
            return
            
        try:
            # Crear un nombre de proyecto basado en la fecha y hora
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            project_name = f"femur_anatomico_report_{timestamp}"
            project_folder = os.path.join(folder_path, project_name)
            
            # Crear carpeta del proyecto
            os.makedirs(project_folder, exist_ok=True)
            
            # 1. Guardar los datos en CSV
            csv_path = os.path.join(project_folder, "osteonas_anatomicas.csv")
            df = pd.DataFrame(self.distribution_data)
            df.to_csv(csv_path, index=False)
            
            # 2. Guardar la configuración en JSON
            config_path = os.path.join(project_folder, "configuracion_anatomica.json")
            with open(config_path, 'w') as f:
                json.dump(self.sections_data, f, indent=4)
            
            # 3. Guardar la visualización
            viz_path = os.path.join(project_folder, "visualizacion_anatomica.png")
            self.figure.savefig(viz_path, dpi=300, bbox_inches='tight')
            
            # 4. Generar un informe HTML
            html_path = os.path.join(project_folder, "informe_anatomico.html")
            self.generate_html_report(html_path)
            
            messagebox.showinfo("Éxito", f"Informe anatómico completo generado en {project_folder}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar el informe: {str(e)}")
    
    def generate_html_report(self, html_path):
        """Genera un informe HTML con información anatómica"""
        # Contar osteonas por sección
        section_counts = {}
        for osteona in self.distribution_data:
            section = osteona["section_name"]
            if section not in section_counts:
                section_counts[section] = 0
            section_counts[section] += 1
        
        # Calcular estadísticas anatómicas
        total_area = sum(math.pi * (section['radius_cm'] ** 2) for section in self.sections_data["sections"])
        
        # Crear el contenido HTML
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Informe Anatómico - Distribución de Osteonas en Fémur</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1, h2, h3 {{ color: #3366cc; }}
                table {{ border-collapse: collapse; width: 100%; margin-top: 10px; margin-bottom: 20px; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .section {{ margin-bottom: 30px; }}
                .visualization {{ text-align: center; margin: 20px 0; }}
                .visualization img {{ max-width: 100%; }}
                .highlight {{ background-color: #ffffcc; font-weight: bold; }}
            </style>
        </head>
        <body>
            <h1>Informe Anatómico - Distribución de Osteonas en Fémur</h1>
            <p>Fecha de generación: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            <p class="highlight">Modelo anatómicamente correcto con ~{len(self.distribution_data):,} osteonas</p>
            
            <div class="section">
                <h2>Parámetros Anatómicos del Fémur</h2>
                <p>Longitud total: {self.sections_data['total_length_cm']:.2f} cm</p>
                <p>Área cortical total: {total_area:.2f} cm²</p>
                
                <h3>Secciones Anatómicas del Fémur</h3>
                <table>
                    <tr>
                        <th>Sección</th>
                        <th>Inicio (cm)</th>
                        <th>Fin (cm)</th>
                        <th>Longitud (cm)</th>
                        <th>Radio (cm)</th>
                        <th>Área (cm²)</th>
                        <th>Densidad (ost/cm²)</th>
                        <th>Tamaño (μm)</th>
                        <th>Variabilidad</th>
                    </tr>
        """
        
        # Añadir filas para cada sección
        for section in self.sections_data["sections"]:
            area_cm2 = math.pi * (section['radius_cm'] ** 2)
            html_content += f"""
                    <tr>
                        <td>{section['name']}</td>
                        <td>{section['start_cm']:.2f}</td>
                        <td>{section['end_cm']:.2f}</td>
                        <td>{section['length_cm']:.2f}</td>
                        <td>{section['radius_cm']:.2f}</td>
                        <td>{area_cm2:.2f}</td>
                        <td>{section['density_per_cm2']:.0f}</td>
                        <td>{section['osteona_size_um']:.1f}</td>
                        <td>{section['variability']:.2f}</td>
                    </tr>
            """
        
        html_content += """
                </table>
            </div>
            
            <div class="section">
                <h2>Guía para Grasshopper - Coordenadas 3D</h2>
                <p>Para importar estos datos anatómicos en Grasshopper, utilice el archivo CSV generado ('osteonas_anatomicas.csv').
                Este archivo contiene coordenadas 3D completas para cada osteona:</p>
                <ul>
                    <li><strong>section_name</strong>: Sección anatómica donde se encuentra la osteona</li>
                    <li><strong>position_x_cm</strong>: Coordenada X en cm (radial)</li>
                    <li><strong>position_y_cm</strong>: Coordenada Y en cm (radial)</li>
                    <li><strong>position_z_cm</strong>: Coordenada Z en cm (longitudinal desde cabeza femoral)</li>
                    <li><strong>size_um</strong>: Diámetro de la osteona en micrómetros</li>
                </ul>
            </div>
            
        </body>
        </html>
        """
        
        # Escribir el contenido a un archivo
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

if __name__ == "__main__":
    root = tk.Tk()
    app = FemurOsteonaDistributor(root)
    root.mainloop()