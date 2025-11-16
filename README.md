# Amazon Review Sentiment Analysis

Proyek ini bertujuan untuk melakukan analisis sentimen pada ulasan produk Amazon menggunakan teknik NLP (Natural Language Processing).

## Struktur Proyek

```
Amazon Review Sentiment/
├── data/              # Dataset
├── notebooks/         # Jupyter notebooks untuk eksplorasi data
│   ├── data_exploration.ipynb
│   └── sentiment_analysis.ipynb
├── src/               # Kode sumber untuk model dan utilitas
│   ├── __init__.py
│   ├── data_preprocessing.py
│   ├── model.py
│   ├── train_model.py
│   └── visualization.py
├── templates/         # Template HTML untuk aplikasi web
│   ├── index.html
│   └── result.html
├── app.py            # Aplikasi web Flask
├── requirements.txt   # Dependensi Python
└── README.md         # Dokumentasi proyek
```

## Cara Menjalankan Proyek

### 1. Instalasi Dependensi

Instal semua dependensi yang diperlukan dengan menjalankan:

```bash
pip install -r requirements.txt
```

### 2. Eksplorasi Data

Jalankan notebook eksplorasi data untuk memahami dataset:

```bash
jupyter notebook notebooks/data_exploration.ipynb
```

### 3. Pelatihan Model

Latih model analisis sentimen dengan menjalankan:

```bash
python src/train_model.py --data_path data/amazon_reviews.csv --text_column reviewText --rating_column overall --model_type logistic_regression --output_dir models --visualize
```

Parameter:
- `--data_path`: Path ke file CSV data
- `--text_column`: Nama kolom teks (default: reviewText)
- `--rating_column`: Nama kolom rating (default: overall)
- `--model_type`: Jenis model (logistic_regression, naive_bayes, svm, random_forest)
- `--output_dir`: Direktori untuk menyimpan model
- `--visualize`: Generate visualisasi data
- `--compare`: Bandingkan berbagai jenis model

### 4. Analisis Sentimen dengan Notebook

Jalankan notebook analisis sentimen untuk eksperimen lebih lanjut:

```bash
jupyter notebook notebooks/sentiment_analysis.ipynb
```

### 5. Menjalankan Aplikasi Web

Jalankan aplikasi web Flask untuk analisis sentimen interaktif:

```bash
python app.py
```

Kemudian buka browser dan akses http://127.0.0.1:5000

## Teknologi yang Digunakan

- Python
- Pandas
- NLTK
- Scikit-learn
- Matplotlib
- Seaborn
- WordCloud
- Jupyter Notebook
- Flask

## Contoh Penggunaan

1. **Preprocessing Teks**:
   ```python
   from src.data_preprocessing import TextPreprocessor

   preprocessor = TextPreprocessor()
   text = "This product is amazing! I would definitely buy it again."
   processed_text = preprocessor.preprocess_text(text)
   ```

2. **Pelatihan Model**:
   ```python
   from src.model import SentimentModel

   model = SentimentModel(model_type='logistic_regression')
   model.train(X_train, y_train)
   ```

3. **Prediksi Sentimen**:
   ```python
   prediction = model.predict("This is the best product I've ever bought!")
   sentiment = "positive" if prediction == 1 else "negative"
   ```

## Catatan

Pastikan Anda memiliki dataset Amazon Review yang disimpan di direktori `data/` dengan nama file `amazon_reviews.csv`. Dataset harus memiliki kolom teks dan rating untuk analisis sentimen.

Jika Anda tidak memiliki dataset, Anda dapat mengunduh dataset Amazon Review dari sumber publik seperti [Amazon Product Data](http://jmcauley.ucsd.edu/data/amazon/).

