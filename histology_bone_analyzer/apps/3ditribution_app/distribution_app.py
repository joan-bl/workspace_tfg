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

class FemurOsteonaDistributor:
    def __init__(self, root):
        self.root = root
        self.root.title("Femur Osteona Distributor")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f0f0")
        
        # Configurar estilo
        self.configure_style()
        
        # Variables
        self.femur_length = tk.DoubleVar(value=45.0)  # Valor por defecto en cm
        self.epiphysis_proximal_percent = tk.DoubleVar(value=15.0)
        self.metaphysis_proximal_percent = tk.DoubleVar(value=10.0)
        self.diaphysis_percent = tk.DoubleVar(value=50.0)
        self.metaphysis_distal_percent = tk.DoubleVar(value=10.0)
        self.epiphysis_distal_percent = tk.DoubleVar(value=15.0)
        
        # Densidades aproximadas de osteonas por sección (número/cm²)
        self.density_epiphysis_proximal = tk.DoubleVar(value=25.0)
        self.density_metaphysis_proximal = tk.DoubleVar(value=40.0)
        self.density_diaphysis = tk.DoubleVar(value=60.0)
        self.density_metaphysis_distal = tk.DoubleVar(value=40.0)
        self.density_epiphysis_distal = tk.DoubleVar(value=25.0)
        
        # Dimensiones de las osteonas por sección (diámetro en micrómetros)
        self.osteona_size_epiphysis_proximal = tk.DoubleVar(value=200.0)
        self.osteona_size_metaphysis_proximal = tk.DoubleVar(value=180.0)
        self.osteona_size_diaphysis = tk.DoubleVar(value=150.0)
        self.osteona_size_metaphysis_distal = tk.DoubleVar(value=180.0)
        self.osteona_size_epiphysis_distal = tk.DoubleVar(value=200.0)
        
        # Factor de variabilidad en la distribución (0.0 = regular, 1.0 = muy irregular)
        self.variability_epiphysis_proximal = tk.DoubleVar(value=0.7)
        self.variability_metaphysis_proximal = tk.DoubleVar(value=0.5)
        self.variability_diaphysis = tk.DoubleVar(value=0.3)
        self.variability_metaphysis_distal = tk.DoubleVar(value=0.5)
        self.variability_epiphysis_distal = tk.DoubleVar(value=0.7)
        
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
        sections_frame = ttk.LabelFrame(self.tab_params, text="Proporciones de Secciones (%)")
        sections_frame.pack(fill="both", expand=False, padx=10, pady=10)
        
        # Etiquetas de columnas
        ttk.Label(sections_frame, text="Sección").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Label(sections_frame, text="% Longitud").grid(row=0, column=1, padx=5, pady=5, sticky="w")
        ttk.Label(sections_frame, text="Densidad (osteonas/cm²)").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        ttk.Label(sections_frame, text="Tamaño (μm)").grid(row=0, column=3, padx=5, pady=5, sticky="w")
        ttk.Label(sections_frame, text="Variabilidad (0-1)").grid(row=0, column=4, padx=5, pady=5, sticky="w")
        
        # Epífisis proximal
        ttk.Label(sections_frame, text="Epífisis Proximal").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(sections_frame, textvariable=self.epiphysis_proximal_percent, width=10).grid(row=1, column=1, padx=5, pady=5, sticky="w")
        ttk.Entry(sections_frame, textvariable=self.density_epiphysis_proximal, width=10).grid(row=1, column=2, padx=5, pady=5, sticky="w")
        ttk.Entry(sections_frame, textvariable=self.osteona_size_epiphysis_proximal, width=10).grid(row=1, column=3, padx=5, pady=5, sticky="w")
        ttk.Entry(sections_frame, textvariable=self.variability_epiphysis_proximal, width=10).grid(row=1, column=4, padx=5, pady=5, sticky="w")
        
        # Metáfisis proximal
        ttk.Label(sections_frame, text="Metáfisis Proximal").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(sections_frame, textvariable=self.metaphysis_proximal_percent, width=10).grid(row=2, column=1, padx=5, pady=5, sticky="w")
        ttk.Entry(sections_frame, textvariable=self.density_metaphysis_proximal, width=10).grid(row=2, column=2, padx=5, pady=5, sticky="w")
        ttk.Entry(sections_frame, textvariable=self.osteona_size_metaphysis_proximal, width=10).grid(row=2, column=3, padx=5, pady=5, sticky="w")
        ttk.Entry(sections_frame, textvariable=self.variability_metaphysis_proximal, width=10).grid(row=2, column=4, padx=5, pady=5, sticky="w")
        
        # Diáfisis
        ttk.Label(sections_frame, text="Diáfisis").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(sections_frame, textvariable=self.diaphysis_percent, width=10).grid(row=3, column=1, padx=5, pady=5, sticky="w")
        ttk.Entry(sections_frame, textvariable=self.density_diaphysis, width=10).grid(row=3, column=2, padx=5, pady=5, sticky="w")
        ttk.Entry(sections_frame, textvariable=self.osteona_size_diaphysis, width=10).grid(row=3, column=3, padx=5, pady=5, sticky="w")
        ttk.Entry(sections_frame, textvariable=self.variability_diaphysis, width=10).grid(row=3, column=4, padx=5, pady=5, sticky="w")
        
        # Metáfisis distal
        ttk.Label(sections_frame, text="Metáfisis Distal").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(sections_frame, textvariable=self.metaphysis_distal_percent, width=10).grid(row=4, column=1, padx=5, pady=5, sticky="w")
        ttk.Entry(sections_frame, textvariable=self.density_metaphysis_distal, width=10).grid(row=4, column=2, padx=5, pady=5, sticky="w")
        ttk.Entry(sections_frame, textvariable=self.osteona_size_metaphysis_distal, width=10).grid(row=4, column=3, padx=5, pady=5, sticky="w")
        ttk.Entry(sections_frame, textvariable=self.variability_metaphysis_distal, width=10).grid(row=4, column=4, padx=5, pady=5, sticky="w")
        
        # Epífisis distal
        ttk.Label(sections_frame, text="Epífisis Distal").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(sections_frame, textvariable=self.epiphysis_distal_percent, width=10).grid(row=5, column=1, padx=5, pady=5, sticky="w")
        ttk.Entry(sections_frame, textvariable=self.density_epiphysis_distal, width=10).grid(row=5, column=2, padx=5, pady=5, sticky="w")
        ttk.Entry(sections_frame, textvariable=self.osteona_size_epiphysis_distal, width=10).grid(row=5, column=3, padx=5, pady=5, sticky="w")
        ttk.Entry(sections_frame, textvariable=self.variability_epiphysis_distal, width=10).grid(row=5, column=4, padx=5, pady=5, sticky="w")
        
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
            
            # Almacenar datos de secciones
            self.sections_data = {
                "total_length_cm": total_length,
                "sections": [
                    {
                        "name": "Epífisis Proximal",
                        "start_cm": ep_prox_start,
                        "end_cm": ep_prox_end,
                        "length_cm": ep_prox_length,
                        "percent": self.epiphysis_proximal_percent.get(),
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
    
    def generate_osteona_distribution(self):
        """Genera la distribución de osteonas basada en los parámetros definidos"""
        distribution_data = []
        
        # Para cada sección, generar las osteonas
        for section in self.sections_data["sections"]:
            # Calcular número aproximado de osteonas por sección
            # Asumimos un ancho medio de 3 cm para el hueso para este cálculo aproximado
            avg_width = 3.0  # cm
            section_area = section["length_cm"] * avg_width  # área aproximada en cm²
            num_osteonas = int(section_area * section["density_per_cm2"])
            
            section_osteonas = []
            
            # Generar posiciones aleatorias con distribución específica para cada sección
            for i in range(num_osteonas):
                # Posición longitudinal (relativa al inicio de la sección)
                pos_z = self.generate_position(
                    0, 
                    section["length_cm"], 
                    section["variability"]
                )
                
                # Posición absoluta en el hueso
                abs_pos_z = section["start_cm"] + pos_z
                
                # Posición angular (alrededor del hueso, 0-360 grados)
                angle = random.uniform(0, 360)
                
                # Calcular tamaño aleatorio de la osteona (variación del 20% alrededor del tamaño definido)
                size_variation = 0.2
                size = section["osteona_size_um"] * (1 + random.uniform(-size_variation, size_variation))
                
                # Añadir a la lista
                section_osteonas.append({
                    "section_name": section["name"],
                    "position_z_cm": abs_pos_z,
                    "angle_degrees": angle,
                    "size_um": size
                })
            
            distribution_data.extend(section_osteonas)
        
        # Guardar los datos
        self.distribution_data = distribution_data
    
    def generate_position(self, min_val, max_val, variability):
        """
        Genera una posición aleatoria con mayor concentración hacia los bordes o centro
        según el valor de variabilidad.
        
        Args:
            min_val: Valor mínimo del rango
            max_val: Valor máximo del rango
            variability: Factor de variabilidad (0.0 = regular, 1.0 = muy irregular)
            
        Returns:
            Posición generada
        """
        # Para variabilidad baja (cerca de 0), distribución más uniforme
        if variability < 0.3:
            return random.uniform(min_val, max_val)
        
        # Para variabilidad media, distribución normal centrada
        elif variability < 0.7:
            mean = (max_val + min_val) / 2
            std_dev = (max_val - min_val) / 6  # 99.7% de los valores caen dentro del rango
            val = np.random.normal(mean, std_dev)
            # Asegurar que el valor está dentro del rango
            return max(min_val, min(max_val, val))
        
        # Para variabilidad alta, más concentración en los bordes
        else:
            # Distribuir entre bordes y centro
            if random.random() < 0.7:  # 70% en los bordes
                if random.random() < 0.5:  # 50% en cada borde
                    return random.uniform(min_val, min_val + (max_val - min_val) * 0.25)
                else:
                    return random.uniform(max_val - (max_val - min_val) * 0.25, max_val)
            else:  # 30% en el centro
                center = (max_val + min_val) / 2
                return random.uniform(center - (max_val - min_val) * 0.15, center + (max_val - min_val) * 0.15)
    
    def display_results(self):
        """Muestra los resultados en el área de texto"""
        if not self.sections_data:
            return
            
        # Limpiar el área de texto
        self.results_text.delete(1.0, tk.END)
        
        # Mostrar información general
        self.results_text.insert(tk.END, f"Longitud total del fémur: {self.sections_data['total_length_cm']:.2f} cm\n\n")
        
        # Mostrar información de cada sección
        for section in self.sections_data["sections"]:
            self.results_text.insert(tk.END, f"Sección: {section['name']}\n")
            self.results_text.insert(tk.END, f"  - Inicio: {section['start_cm']:.2f} cm\n")
            self.results_text.insert(tk.END, f"  - Fin: {section['end_cm']:.2f} cm\n")
            self.results_text.insert(tk.END, f"  - Longitud: {section['length_cm']:.2f} cm ({section['percent']:.1f}%)\n")
            self.results_text.insert(tk.END, f"  - Densidad: {section['density_per_cm2']:.1f} osteonas/cm²\n")
            self.results_text.insert(tk.END, f"  - Tamaño medio: {section['osteona_size_um']:.1f} μm\n")
            self.results_text.insert(tk.END, f"  - Variabilidad: {section['variability']:.2f}\n\n")
        
        # Mostrar estadísticas de la distribución
        if self.distribution_data:
            num_osteonas = len(self.distribution_data)
            self.results_text.insert(tk.END, f"Total de osteonas generadas: {num_osteonas}\n")
            
            # Contar osteonas por sección
            section_counts = {}
            for osteona in self.distribution_data:
                section = osteona["section_name"]
                if section not in section_counts:
                    section_counts[section] = 0
                section_counts[section] += 1
            
            self.results_text.insert(tk.END, "Distribución por sección:\n")
            for section, count in section_counts.items():
                self.results_text.insert(tk.END, f"  - {section}: {count} osteonas ({count/num_osteonas*100:.1f}%)\n")
    
    def update_visualization(self):
        """Actualiza los gráficos de visualización"""
        if not self.sections_data or not self.distribution_data:
            return
            
        # Limpiar los ejes
        self.ax1.clear()
        self.ax2.clear()
        
        # Colores para las secciones
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0']
        
        # Gráfico 1: Perfil del hueso con secciones
        x_bone = np.linspace(0, self.sections_data["total_length_cm"], 1000)
        y_bone = np.zeros_like(x_bone)
        
# Forma aproximada del fémur (simplificada)
        for i, x in enumerate(x_bone):
            # Anchura relativa a lo largo del hueso
            rel_pos = x / self.sections_data["total_length_cm"]
            
            # Forma de botella con bulbos en los extremos
            if rel_pos < 0.15:  # Epífisis proximal
                y_bone[i] = 2.5 * (1 - rel_pos/0.15) + 1
            elif rel_pos < 0.25:  # Metáfisis proximal
                y_bone[i] = 1 + (2.5 - 1) * (0.25 - rel_pos) / 0.1
            elif rel_pos < 0.75:  # Diáfisis
                y_bone[i] = 1
            elif rel_pos < 0.85:  # Metáfisis distal
                y_bone[i] = 1 + (3 - 1) * (rel_pos - 0.75) / 0.1
            else:  # Epífisis distal
                y_bone[i] = 3 + (rel_pos - 0.85) * 0.5 / 0.15
                
        # Dibujar el perfil del hueso (simétrico respecto al eje x)
        self.ax1.fill_between(x_bone, y_bone, -y_bone, color='#e0e0e0', alpha=0.5, label='Perfil del fémur')
        
        # Sombrear las diferentes secciones
        current_pos = 0
        for i, section in enumerate(self.sections_data["sections"]):
            end_pos = section["end_cm"]
            section_mask = (x_bone >= current_pos) & (x_bone <= end_pos)
            
            self.ax1.fill_between(
                x_bone[section_mask], 
                y_bone[section_mask], 
                -y_bone[section_mask], 
                color=colors[i], 
                alpha=0.7, 
                label=section["name"]
            )
            
            # Dibujar líneas de separación
            if current_pos > 0:
                self.ax1.axvline(x=current_pos, color='black', linestyle='--', alpha=0.5)
            
            current_pos = end_pos
        
        # Configurar gráfico 1
        self.ax1.set_title('Perfil del Fémur y Secciones')
        self.ax1.set_xlabel('Longitud (cm)')
        self.ax1.set_ylabel('Ancho (cm)')
        self.ax1.grid(True, linestyle='--', alpha=0.7)
        self.ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)
        
        # Gráfico 2: Distribución de osteonas a lo largo del hueso
        positions = [osteona["position_z_cm"] for osteona in self.distribution_data]
        sizes = [osteona["size_um"] / 100 for osteona in self.distribution_data]  # Normalizar tamaños para visualización
        colors_scatter = []
        
        # Asignar colores según la sección
        for osteona in self.distribution_data:
            section_name = osteona["section_name"]
            idx = next(i for i, s in enumerate(self.sections_data["sections"]) if s["name"] == section_name)
            colors_scatter.append(colors[idx])
        
        # Dibujamos las osteonas como puntos
        self.ax2.scatter(positions, [0]*len(positions), c=colors_scatter, s=sizes, alpha=0.7)
        
        # Línea representando el hueso
        self.ax2.axhline(y=0, color='black', linestyle='-', alpha=0.5)
        
        # Líneas para separar secciones
        for section in self.sections_data["sections"]:
            if section["start_cm"] > 0:
                self.ax2.axvline(x=section["start_cm"], color='black', linestyle='--', alpha=0.5)
        
        # Configurar gráfico 2
        self.ax2.set_title('Distribución de Osteonas a lo largo del Fémur')
        self.ax2.set_xlabel('Posición Longitudinal (cm)')
        self.ax2.set_yticks([])  # Ocultar eje y
        self.ax2.set_xlim(0, self.sections_data["total_length_cm"])
        self.ax2.grid(True, linestyle='--', alpha=0.7, axis='x')
        
        # Ajustar diseño y mostrar
        self.figure.tight_layout()
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
        """Actualiza la previsualización de datos en la pestaña de exportación"""
        if not self.distribution_data:
            return
            
        # Limpiar el área de previsualización
        self.preview_text.delete(1.0, tk.END)
        
        # Mostrar los primeros 20 registros (o menos si hay menos)
        num_preview = min(20, len(self.distribution_data))
        
        self.preview_text.insert(tk.END, "Previsualización de los datos (primeros 20 registros):\n\n")
        self.preview_text.insert(tk.END, "section_name, position_z_cm, angle_degrees, size_um\n")
        
        for i in range(num_preview):
            osteona = self.distribution_data[i]
            self.preview_text.insert(
                tk.END, 
                f"{osteona['section_name']}, {osteona['position_z_cm']:.2f}, {osteona['angle_degrees']:.2f}, {osteona['size_um']:.2f}\n"
            )
        
        self.preview_text.insert(tk.END, f"\n... (Total: {len(self.distribution_data)} registros)")
    
    def export_data(self, format_type):
        """Exporta los datos en el formato especificado"""
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
                df.to_csv(file_path, index=False)
            else:  # JSON
                # Guardar como JSON
                data = {
                    "femur_info": self.sections_data,
                    "osteonas": self.distribution_data
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
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            project_name = f"femur_report_{timestamp}"
            project_folder = os.path.join(folder_path, project_name)
            
            # Crear carpeta del proyecto
            os.makedirs(project_folder, exist_ok=True)
            
            # 1. Guardar los datos en CSV
            csv_path = os.path.join(project_folder, "osteonas_data.csv")
            df = pd.DataFrame(self.distribution_data)
            df.to_csv(csv_path, index=False)
            
            # 2. Guardar la configuración en JSON
            config_path = os.path.join(project_folder, "configuration.json")
            with open(config_path, 'w') as f:
                json.dump(self.sections_data, f, indent=4)
            
            # 3. Guardar la visualización
            viz_path = os.path.join(project_folder, "visualization.png")
            self.figure.savefig(viz_path, dpi=300, bbox_inches='tight')
            
            # 4. Generar un informe HTML
            html_path = os.path.join(project_folder, "report.html")
            self.generate_html_report(html_path)
            
            messagebox.showinfo("Éxito", f"Informe completo generado en {project_folder}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar el informe: {str(e)}")
    
    def generate_html_report(self, html_path):
        """Genera un informe HTML con los resultados"""
        # Contar osteonas por sección
        section_counts = {}
        for osteona in self.distribution_data:
            section = osteona["section_name"]
            if section not in section_counts:
                section_counts[section] = 0
            section_counts[section] += 1
        
        # Crear el contenido HTML
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Informe de Distribución de Osteonas en Fémur</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1, h2, h3 {{ color: #3366cc; }}
                table {{ border-collapse: collapse; width: 100%; margin-top: 10px; margin-bottom: 20px; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .section {{ margin-bottom: 30px; }}
                .visualization {{ text-align: center; margin: 20px 0; }}
                .visualization img {{ max-width: 100%; }}
            </style>
        </head>
        <body>
            <h1>Informe de Distribución de Osteonas en Fémur</h1>
            <p>Fecha de generación: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            
            <div class="section">
                <h2>Parámetros del Fémur</h2>
                <p>Longitud total: {self.sections_data['total_length_cm']:.2f} cm</p>
                
                <h3>Secciones del Fémur</h3>
                <table>
                    <tr>
                        <th>Sección</th>
                        <th>Inicio (cm)</th>
                        <th>Fin (cm)</th>
                        <th>Longitud (cm)</th>
                        <th>Porcentaje</th>
                        <th>Densidad (ost/cm²)</th>
                        <th>Tamaño (μm)</th>
                        <th>Variabilidad</th>
                    </tr>
        """
        
        # Añadir filas para cada sección
        for section in self.sections_data["sections"]:
            html_content += f"""
                    <tr>
                        <td>{section['name']}</td>
                        <td>{section['start_cm']:.2f}</td>
                        <td>{section['end_cm']:.2f}</td>
                        <td>{section['length_cm']:.2f}</td>
                        <td>{section['percent']:.1f}%</td>
                        <td>{section['density_per_cm2']:.1f}</td>
                        <td>{section['osteona_size_um']:.1f}</td>
                        <td>{section['variability']:.2f}</td>
                    </tr>
            """
        
        html_content += """
                </table>
            </div>
            
            <div class="section">
                <h2>Estadísticas de Distribución</h2>
        """
        
        # Añadir estadísticas
        total_osteonas = len(self.distribution_data)
        html_content += f"""
                <p>Total de osteonas generadas: {total_osteonas}</p>
                
                <h3>Distribución por Sección</h3>
                <table>
                    <tr>
                        <th>Sección</th>
                        <th>Número de Osteonas</th>
                        <th>Porcentaje</th>
                    </tr>
        """
        
        # Añadir filas para cada sección
        for section, count in section_counts.items():
            html_content += f"""
                    <tr>
                        <td>{section}</td>
                        <td>{count}</td>
                        <td>{count/total_osteonas*100:.1f}%</td>
                    </tr>
            """
        
        html_content += """
                </table>
            </div>
            
            <div class="visualization">
                <h2>Visualización</h2>
                <img src="visualization.png" alt="Visualización de la distribución de osteonas">
            </div>
            
            <div class="section">
                <h2>Información para Grasshopper</h2>
                <p>Para importar estos datos en Grasshopper, utilice el archivo CSV generado ('osteonas_data.csv').
                Este archivo contiene la siguiente información para cada osteona:</p>
                <ul>
                    <li><strong>section_name</strong>: Nombre de la sección donde se encuentra la osteona</li>
                    <li><strong>position_z_cm</strong>: Posición longitudinal en cm desde el inicio del fémur</li>
                    <li><strong>angle_degrees</strong>: Ángulo en grados (0-360) alrededor del eje del hueso</li>
                    <li><strong>size_um</strong>: Tamaño de la osteona en micrómetros</li>
                </ul>
                <p>Para crear la geometría en Grasshopper, siga estos pasos:</p>
                <ol>
                    <li>Importe el archivo CSV utilizando el componente "Read File"</li>
                    <li>Parse los datos con el componente "Construct Point" usando las columnas position_z_cm y angle_degrees</li>
                    <li>Utilice el tamaño de la osteona para generar la geometría apropiada</li>
                    <li>Use los valores de section_name para aplicar diferentes propiedades según la sección</li>
                </ol>
            </div>
            
        </body>
        </html>
        """
        
        # Escribir el contenido a un archivo
        with open(html_path, 'w') as f:
            f.write(html_content)


if __name__ == "__main__":
    root = tk.Tk()
    app = FemurOsteonaDistributor(root)
    root.mainloop()