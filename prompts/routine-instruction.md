# Instrucción principal para Claude Routine

Cada día a las 8:00 AM, hora de Ciudad de México, ejecuta el prompt ubicado en:

`prompts/daily-market-radar.md`

Usa también:

- `config/rules.md`
- `config/sources.md`
- `watchlist/watchlist.md`

Genera un reporte breve y claro con:

1. Resumen ejecutivo del mercado.
2. Indicadores principales.
3. Top activos que más subieron.
4. Top activos que más cayeron.
5. Posibles oportunidades para estudiar.
6. Activos que evitaría por ahora.
7. Watchlist final.

Archivos obligatorios de salida:

- `reports/YYYY-MM-DD-market-radar.md`
- `reports/YYYY-MM-DD-market-radar.pdf`

Procedimiento:

1. Crea primero el archivo Markdown en `reports/YYYY-MM-DD-market-radar.md`.
2. Después ejecuta:

```bash
python scripts/markdown_to_pdf.py reports/YYYY-MM-DD-market-radar.md reports/YYYY-MM-DD-market-radar.pdf
```

3. Verifica que ambos archivos existan.
4. Si el PDF falla, conserva el `.md` y escribe en el resultado de la rutina cuál fue el error.

No des recomendaciones directas de compra. Presenta hipótesis, riesgos y condiciones de confirmación.

Si no puedes verificar una causa, indícalo explícitamente.
