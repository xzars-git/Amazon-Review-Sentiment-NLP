# Amazon Review Sentiment Analysis

Proyek ini bertujuan untuk melakukan analisis sentimen pada ulasan produk Amazon menggunakan teknik NLP (Natural Language Processing). Dataset yang digunakan berasal dari Kaggle: [Amazon Reviews Dataset](https://www.kaggle.com/datasets/kritanjalijain/amazon-reviews).

## Tentang Dataset

Dataset ini berisi ulasan produk dari Amazon dengan informasi berikut:
- ID Ulasan
- ID Produk
- ID Pengguna
- Nama Profil Pengguna
- Nilai Bantuan (Helpfulness Numerator)
- Total Bantuan (Helpfulness Denominator)
- Skor (Rating 1-5)
- Waktu Ulasan (Timestamp)
- Ringkasan Ulasan
- Teks Ulasan

Dataset ini memiliki dua kategori:
1. Train: 40.000 ulasan
2. Test: 10.000 ulasan

## Struktur Proyek

```
Amazon Review Sentiment/
├── data/              # Dataset
│   ├── train.csv      # Data pelatihan
│   └── test.csv       # Data pengujian
├── notebooks/         # Jupyter notebooks untuk eksplorasi data
│   ├── data_exploration.ipynb
│   ├── sentiment_analysis.ipynb
│   ├── kaggle_data_exploration.ipynb
│   ├── kaggle_sentiment_analysis.ipynb
│   ├── kaggle_data_exploration_fixed.ipynb
│   └── kaggle_sentiment_analysis_fixed.ipynb
├── src/               # Kode sumber untuk model dan utilitas
│   ├── __init__.py
│   ├── data_preprocessing.py
│   ├── model.py
│   ├── train_model.py
│   ├── train_model_kaggle.py
│   └── visualization.py
├── templates/         # Template HTML untuk aplikasi web
│   ├── index.html
│   └── result.html
├── app.py            # Aplikasi web Flask
├── requirements.txt   # Dependensi Python
└── README.md         # Dokumentasi proyek
```

## Cara Menjalankan Proyek

### 1. Unduh Dataset

Unduh dataset dari Kaggle:
1. Kunjungi [Amazon Reviews Dataset](https://www.kaggle.com/datasets/kritanjalijain/amazon-reviews)
2. Unduh file `train.csv` dan `test.csv`
3. Simpan file-file tersebut di direktori `data/`

### 2. Instalasi Dependensi

Instal semua dependensi yang diperlukan dengan menjalankan:

```bash
pip install -r requirements.txt
```

### 3. Eksplorasi Data

Jalankan notebook eksplorasi data untuk memahami dataset:

```bash
jupyter notebook notebooks/kaggle_data_exploration_fixed.ipynb
```

Atau gunakan notebook versi asli:

```bash
jupyter notebook notebooks/data_exploration.ipynb
```

### 4. Pelatihan Model

Latih model analisis sentimen dengan menjalankan:

```bash
python src/train_model_kaggle.py --data_path data/train.csv --text_column Text --rating_column Score --model_type logistic_regression --output_dir models --visualize
```

Atau gunakan versi asli jika Anda sudah memiliki dataset dengan format yang berbeda:

```bash
python src/train_model.py --data_path data/amazon_reviews.csv --text_column reviewText --rating_column overall --model_type logistic_regression --output_dir models --visualize
```

Parameter:
- `--data_path`: Path ke file CSV data
- `--text_column`: Nama kolom teks (default: Text)
- `--rating_column`: Nama kolom rating (default: Score)
- `--model_type`: Jenis model (logistic_regression, naive_bayes, svm, random_forest)
- `--output_dir`: Direktori untuk menyimpan model
- `--visualize`: Generate visualisasi data
- `--compare`: Bandingkan berbagai jenis model

### 5. Analisis Sentimen dengan Notebook

Jalankan notebook analisis sentimen untuk eksperimen lebih lanjut:

```bash
jupyter notebook notebooks/kaggle_sentiment_analysis_fixed.ipynb
```

Atau gunakan notebook versi asli:

```bash
jupyter notebook notebooks/sentiment_analysis.ipynb
```

### 6. Menjalankan Aplikasi Web

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

## Label Sentimen

Dalam proyek ini, sentimen ditentukan berdasarkan rating:
- Rating 1-2: Sentimen Negatif (0)
- Rating 3: Sentimen Netral (dikecualikan dalam klasifikasi biner)
- Rating 4-5: Sentimen Positif (1)

## Catatan

Pastikan Anda telah mengunduh dataset Amazon Review dari Kaggle dan menyimpan file `train.csv` dan `test.csv` di direktori `data/`. Dataset ini menggunakan kolom `Text` untuk teks ulasan dan `Score` untuk rating produk.

Untuk informasi lebih lanjut tentang dataset, kunjungi [Amazon Reviews Dataset di Kaggle](https://www.kaggle.com/datasets/kritanjalijain/amazon-reviews).

