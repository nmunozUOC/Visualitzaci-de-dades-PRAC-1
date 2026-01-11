# Visualitzaci-de-dades-PRAC-1
Visualització de dades PRAC 1 Natalia Muñoz

Aquest projecte presenta un conjunt de visualitzacions interactives per analitzar factors de risc associats a la malaltia cardíaca, utilitzant dades clíniques i d’estil de vida.

Les visualitzacions es generen mitjançant Dash i Plotly i es mostren en format HTML.
Totes les visualitzacions es troben a l’HTML generat per l’aplicació Dash.
Aquest HTML inclou:
- Diagrames Sankey
- Coordenades paral·leles
- Heatmap de correlacions
- Ridgeline plot
- Matriu de dispersió
- Gràfics de barres

Per generar i visualitzar l’HTML, cal executar:

```bash
python app.py
```
Un cop executat:
- S’iniciarà un servidor local
- S’obrirà l’aplicació al navegador (normalment a http://127.0.0.1:8050)
- Allà es podran veure totes les visualitzacions interactives

**Nota important:**  
El fitxer MHTML que es troba penjat correspon a una versió *frozen* (estàtica) de l’aplicació.  
Aquesta versió **no és completa** i **algunes visualitzacions poden no mostrar-se correctament** a causa de les limitacions del renderitzat estàtic. Per accedir a totes les funcionalitats i visualitzacions interactives, cal executar l’aplicació amb Python.
