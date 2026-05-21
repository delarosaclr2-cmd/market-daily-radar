# Cómo subir esta estructura a GitHub

## Opción recomendada: subir desde navegador

### 1. Crear repositorio

1. Entra a GitHub.
2. Presiona el botón `+` en la esquina superior derecha.
3. Selecciona `New repository`.
4. En `Repository name`, escribe:

   `market-daily-radar`

5. En `Description`, puedes poner:

   `Rutina diaria de análisis de mercado con Claude.`

6. Selecciona `Private`.
7. No agregues README, .gitignore ni license si vas a subir este paquete completo.
8. Presiona `Create repository`.

### 2. Subir archivos

1. Entra al repositorio `market-daily-radar`.
2. Presiona `Add file`.
3. Selecciona `Upload files`.
4. Descomprime el ZIP descargado.
5. Abre la carpeta `market-daily-radar`.
6. Arrastra todo el contenido de esa carpeta al navegador:
   - README.md
   - config/
   - docs/
   - prompts/
   - reports/
   - watchlist/
7. En `Commit message`, escribe:

   `Initial market radar structure`

8. Selecciona `Commit directly to the main branch`.
9. Presiona `Commit changes`.

## Después de subirlo

Cuando Claude te pida repositorio, selecciona:

`market-daily-radar`

Cuando Claude te pida environment, crea o selecciona:

`market-research-env`

## Configuración sugerida de la rutina

- Tipo: Remote
- Frecuencia: Lunes a viernes
- Hora: 8:00 AM
- Zona horaria: America/Mexico_City
- Modelo: Sonnet
- Repositorio: market-daily-radar
- Environment: market-research-env

## Network access sugerido para el environment

Usa acceso Custom y agrega estos dominios:

- finance.yahoo.com
- query1.finance.yahoo.com
- query2.finance.yahoo.com
- tradingview.com
- www.tradingview.com
- marketwatch.com
- www.marketwatch.com
- cnbc.com
- www.cnbc.com
- reuters.com
- www.reuters.com
- bloomberg.com
- www.bloomberg.com
- investing.com
- www.investing.com
- coinmarketcap.com
- www.coinmarketcap.com
- coingecko.com
- www.coingecko.com
- fred.stlouisfed.org
- cmegroup.com
- www.cmegroup.com
- sec.gov
- www.sec.gov
