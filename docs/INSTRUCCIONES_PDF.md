# Cómo hacer que Claude genere PDF además de Markdown

## 1. Subir los archivos nuevos al repositorio

Sube estos archivos al repositorio `market-daily-radar`:

- `scripts/markdown_to_pdf.py`
- `requirements.txt`
- `prompts/daily-market-radar.md`
- `prompts/routine-instruction.md`
- `README.md`

Puedes subir el ZIP completo si prefieres reemplazar todo.

## 2. Configurar el environment

En Claude, edita o crea el environment:

`market-research-env`

En el campo `Setup script`, pega:

```bash
#!/bin/bash
python -m pip install --upgrade pip
python -m pip install reportlab
```

Guarda los cambios.

## 3. Modificar la instrucción de la rutina

En la rutina, usa el contenido de:

`prompts/routine-instruction.md`

Lo importante es que incluya esta instrucción:

```bash
python scripts/markdown_to_pdf.py reports/YYYY-MM-DD-market-radar.md reports/YYYY-MM-DD-market-radar.pdf
```

## 4. Probar la rutina

Después de guardar cambios:

1. Entra a la rutina.
2. Presiona `Run now`.
3. Revisa si Claude generó:
   - `reports/YYYY-MM-DD-market-radar.md`
   - `reports/YYYY-MM-DD-market-radar.pdf`

## 5. Si falla el PDF

Posibles causas:

- No se instaló `reportlab`.
- El environment no tiene acceso a PyPI.
- El setup script falló.
- El archivo `.md` no se creó antes de ejecutar el script.

En ese caso, revisa el log de la rutina y vuelve a correrla.
