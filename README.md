<h1 align="center">Welcome to Myriade 👋</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-1.0.0-blue.svg?cacheSeconds=2592000" />
  <a href="/" target="_blank">
    <img alt="Documentation" src="https://img.shields.io/badge/documentation-yes-brightgreen.svg" />
  </a>
</p>

> Le projet vise à créer un moteur de recherche du futur en combinant l'indexation classique des moteurs de recherche avec l'intelligence artificielle générative dans une interface unifiée et open-source, offrant une expérience utilisateur améliorée tout en préservant la confidentialité des données.

### 🏠 [Homepage]
<img src="public/first_preview.png" alt="preview" width="100%"/>

## Install

### 1 - Optionnel (mais recommandé) : Créer un environnement virtuel

```sh
python -m venv venv
source venv/bin/activate // Linux and MacOS
venv\Scripts\activate // Windows
```

### 2 - Install dependencies:

```sh
 pip install -r crawler/requirements.txt
```


## Usage

### 1 - Crawl datas
  
  ```sh
  python crawler/run_spiders.py
  ```

  ### 2 - Run the server

  ```sh
  cd api
  pip install -r requirements.txt
  uvicorn main:app --reload
  ```

  ### 3 - Run the frontend

  ```sh
  cd app
  npm install
  npm run dev
  ```

## Author

👤 **Raphaël Plassart**

* Website: raph-portfolio.fr
* Github: [@raphplt](https://github.com/raphplt)

## Show your support

Give a ⭐️ if this project helped you!
