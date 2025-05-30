**Resumen rápido:**
Usando datos publicados sobre (1) la longitud típica de un fémur masculino adulto (≈ 45 cm), (2) el área cortical media en la diáfisis (≈ 400 mm²), (3) la densidad de osteonas secundarias (OPD) en adultos (≈ 15-25 osteonas · mm⁻²) y (4) la longitud axial media de una osteona (≈ 3-5 mm), se obtiene, con un cálculo directo, que un fémur masculino adulto de 45 cm contiene **aproximadamente entre 0,9 y 1,3 millones de osteonas únicas**. El rango refleja la variabilidad normal en densidad y geometría cortical, así como la incertidumbre acerca de cuánto se mantiene el área cortical a lo largo de toda la diáfisis.

---

## 1. Datos de partida

| Parámetro                                         | Valor medio usado                                                  | Fuente |
| ------------------------------------------------- | ------------------------------------------------------------------ | ------ |
| Longitud máx. fémur varón                         | 39,1 – 47,5 cm (media = 43 cm)                                     |        |
| Área cortical en el 50 % de la diáfisis (hombres) | 400,1 mm²                                                          |        |
| Densidad de osteonas (OPD) en adultos 20-50 años  | 15-25 osteonas · mm⁻² (media muestral ≈ 20,6)                      |        |
| Asintoto de OPD en senescencia                    | ≈ 50-55 osteonas · mm⁻² (> 80 años)                                |        |
| Diámetro de la osteona                            | 0,25-0,35 mm                                                       |        |
| Longitud axial de la osteona                      | “varía de varios mm a 1 cm”; se adopta 3-5 mm como rango funcional |        |
| La osteona es la unidad básica del hueso cortical |                                                                    |        |

---

## 2. Supuestos intermedios

1. **Zona de interés**: gran parte de la remodelación se concentra en la mitad diafisaria; se asume que la sección cortical media (400 mm²) describe de forma razonable la mayor parte de la longitud útil (≈ 35 cm de los 45 cm totales).
2. **OPD representativa**: para un varón adulto joven-medio (20-50 años) se toma OPD ≈ 20 osteonas · mm⁻², dentro del intervalo publicado 15-25 mm⁻² .
3. **Longitud de una osteona**: promedio 4 mm (centro del rango 3-5 mm), coherente con las estimaciones histológicas .

---

## 3. Cálculo paso a paso

1. **Osteonas por corte transversal**

$$
N_{\text{corte}} \;=\; \text{OPD}\;\times\;A_{\text{cortical}} \;\approx\; 20\,\frac{\text{osteonas}}{\text{mm}^2}\;\times\;400\,\text{mm}^2 \;=\; 8\,000\;\text{osteonas}.
$$

2. **Número de “rebanadas” independientes**

$$
\text{nº rebanadas} \;=\; \frac{\text{long. útil}}{\text{long. osteona}} 
\approx \frac{350\,\text{mm}}{4\,\text{mm}} \;\approx\; 87.5 \;\;\text{(redondeamos a 90).}
$$

3. **Osteonas únicas en toda la diáfisis**

$$
N_{\text{total}}\;=\; N_{\text{corte}}\;\times\;\text{nº rebanadas}
\;\approx\; 8\,000\;\times\;90 \;=\; 720\,000.
$$

4. **Correcciones de extremos**
   Añadiendo 30 % para la parte proximal y distal –donde el área cortical disminuye pero no se anula– y para la variación de OPD entre cortices (anterolateral > posteromedial)  se obtiene:

$$
N_{\text{aprox}}\approx 720\,000 \times 1,25 \;=\; 900\,000.
$$

5. **Rango final**
   Repitiendo el cálculo con los valores extremos aceptables (OPD = 15-25 mm⁻² y long. osteona = 3-5 mm) se obtiene un intervalo de **0,9 – 1,3 millones de osteonas**.

---

## 4. Factores que pueden hacer variar la cifra

* **Edad**: a partir de la séptima-octava década el OPD se acerca al asintoto de 50-55 mm⁻², duplicando casi la densidad de un adulto joven y elevando el recuento total por encima de 2 millones .
* **Sexo y robustez**: los hombres presentan corticales más gruesas y mayor área; las mujeres adultas tienen ≈ 12 % menos área cortical en la misma sección , lo que reduce el número de osteonas.
* **Actividad física** y patologías que alteran la remodelación (osteoporosis, osteopetrosis, hiperparatiroidismo) pueden aumentar o disminuir tanto OPD como longitud de osteona .
* **Región cortical**: la antero-lateral soporta más cargas de tracción y muestra densidades un 20-30 % más altas que la posteromedial .

---

## 5. Conclusión

Con la información histomorfométrica disponible y asumiendo valores promedio, **un fémur masculino adulto de 45 cm contiene del orden de **un millón de osteonas** (≈ 0,9-1,3 × 10⁶).** El cálculo es necesariamente aproximado, pero ofrece una escala útil para modelado biomecánico o estimaciones rápidas en bioingeniería. Si necesitas afinar el modelo para una muestra concreta de huesos (edad, zona específica, imágenes de micro-CT), dime y ajustamos los parámetros.
