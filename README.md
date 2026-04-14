# PVP Bot

Bot per il scraping e la ricerca di aste sul portale delle vendite pubbliche della giustizia italiana (https://pvp.giustizia.it/pvp/).

## Descrizione

Questo progetto automatizza la ricerca di aste immobiliari sul sito PVP (Portale Vendite Pubbliche) del Ministero della Giustizia. Utilizza Selenium con Firefox WebDriver per navigare il sito, compilare i form di ricerca e scaricare i risultati.

## Requisiti

- Python 3.8+
- Firefox browser installato
- GeckoDriver (gestito automaticamente da webdriver-manager)

## Installazione

1. Clona il repository:
```bash
git clone https://github.com/IsraelSal/pvpBot.git
cd pvpBot
```

2. Installa le dipendenze:
```bash
pip install -r requirements.txt
```

## Utilizzo

### Ricerca Aste

Importa e utilizza la funzione `astaSearch` dal modulo `scrapingSearch`:

```python
from scrapingSearch import astaSearch

# Esempio di ricerca
results = astaSearch(
    localita="Roma",
    prezzo_min=100000,
    prezzo_max=500000
)
```

Parametri:
- `localita`: Città o località da cercare (obbligatorio)
- `prezzo_min`: Prezzo minimo dell'immobile (opzionale, default: None)
- `prezzo_max`: Prezzo massimo dell'immobile (opzionale, default: None)

La funzione restituisce una lista di dizionari contenenti i dati delle aste trovate.

## Testing

Esegui i test per verificare il corretto funzionamento:

```bash
pytest test_pvp_website.py -v
```

I test verificano:
- Caricamento del sito PVP
- Presenza degli elementi principali (modal popup, form di ricerca)
- Funzionalità dei campi di input
- Corretto funzionamento della funzione `astaSearch`

## Struttura del Progetto

```
pvpBot/
├── scrapingSearch.py    # Modulo principale per il scraping
├── test_pvp_website.py  # Suite di test
├── requirements.txt     # Dipendenze Python
└── README.md           # Questo file
```

## Note Importanti

- Il browser Firefox viene avviato in modalità headless durante i test
- Il webdriver-manager gestisce automaticamente il download di GeckoDriver
- Assicurati di avere una connessione internet stabile durante l'esecuzione
- Rispetta i termini di servizio del sito PVP quando utilizzi questo bot

## Browser Support

Attualmente supportato:
- ✅ Firefox (consigliato)

Precedentemente supportato:
- ❌ Chrome (rimosso nel refactoring)

## License

MIT License

## Contributing

1. Crea un branch per la tua feature (`git checkout -b feature/AmazingFeature`)
2. Commit delle modifiche (`git commit -m 'Add some AmazingFeature'`)
3. Push sul branch (`git push origin feature/AmazingFeature`)
4. Apri una Pull Request

## Disclaimer

Questo strumento è fornito a solo scopo educativo e di automazione personale. L'utente è responsabile dell'uso conforme ai termini di servizio del sito PVP e alle leggi vigenti.