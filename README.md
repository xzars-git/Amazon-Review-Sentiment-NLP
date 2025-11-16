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
1. Train: 1.600.000 ulasan (dari total 34.686.770 ulasan)
2. Test: 400.000 ulasan
3. Total dataset tersedia: 34.686.770 ulasan dari 6.643.669 pengguna pada 2.441.053 produk

## Struktur Proyek

```
Amazon Review Sentiment/
├── data/              # Dataset
│   ├── train.csv      # Data pelatihan (1.6M+ samples)
│   └── test.csv       # Data pengujian (400K+ samples)
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
├── models/            # Model yang telah dilatih
│   ├── best_sentiment_model.pkl
│   ├── logistic_regression_model.pkl
│   ├── logistic_regression_model_large.pkl
│   └── visualizations/
├── templates/         # Template HTML untuk aplikasi web
│   ├── index.html
│   ├── result.html
│   └── dashboard.html
├── static/           # File statis untuk aplikasi web
│   ├── css/
│   └── js/
├── app.py            # Aplikasi web Flask
├── train_model_large_fixed.py  # Pelatihan dengan dataset besar
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

#### Pelatihan Standar
Latih model analisis sentimen dengan dataset standar:

```bash
python src/train_model_kaggle.py --data_path data/train.csv --text_column Text --rating_column Score --model_type logistic_regression --output_dir models --visualize
```

#### Pelatihan dengan Dataset Besar
Untuk pelatihan dengan dataset yang lebih besar (hingga 2 juta sampel):

```bash
python train_model_large_fixed.py --data_path data/train.csv --max_samples 2000000 --max_features 20000
```

Parameter tambahan untuk pelatihan besar:
- `--max_samples`: Jumlah maksimum sampel yang akan digunakan (default: 2.000.000)
- `--max_features`: Jumlah maksimum fitur untuk TF-IDF (default: 20.000)
- `--batch_size`: Ukuran batch untuk pemrosesan data (default: 100.000)

#### Format Dataset Lain
Gunakan versi asli jika Anda sudah memiliki dataset dengan format yang berbeda:

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

## Performa Model

Model terbaru yang dilatih dengan 1.6 juta sampel dan 20.000 fitur:
- Akurasi: 87.25%
- Precision (Positive): 0.87
- Precision (Negative): 0.88
- Recall (Positive): 0.88
- Recall (Negative): 0.87
- F1-Score (Positive): 0.87
- F1-Score (Negative): 0.87

Confusion Matrix:
- True Negative: 172.929
- False Positive: 26.447
- False Negative: 24.569
- True Positive: 176.055

## Model Comparison

| Model | Training Samples | Max Features | Accuracy | Training Time |
|-------|----------------|-------------|----------|---------------|
| Logistic Regression (Standard) | 720.000 | 10.000 | 87.05% | 18.42s |
| Logistic Regression (Large) | 1.600.000 | 20.000 | 87.25% | 24.79s |

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

