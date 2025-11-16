// Initialize charts
let sentimentChart = null;
let categoryChart = null;
let confidenceChart = null;

// DOM elements
const dashboardView = document.getElementById('dashboard-view');
const analyzeView = document.getElementById('analyze-view');
const historyView = document.getElementById('history-view');
const modelInfoView = document.getElementById('model-info-view');

const dashboardLink = document.getElementById('dashboard-link');
const analyzeLink = document.getElementById('analyze-link');
const historyLink = document.getElementById('history-link');
const modelInfoLink = document.getElementById('model-info-link');

// Form elements
const analyzeForm = document.getElementById('analyze-form');
const reviewTextInput = document.getElementById('review-text');
const reviewCategorySelect = document.getElementById('review-category');
const reviewRatingSelect = document.getElementById('review-rating');

// Result elements
const resultSection = document.getElementById('result-section');
const originalReviewText = document.getElementById('original-review-text');
const resultCategory = document.getElementById('result-category');
const resultRating = document.getElementById('result-rating');
const sentimentResult = document.getElementById('sentiment-result');

// History elements
const historyList = document.getElementById('history-list');
const clearHistoryBtn = document.getElementById('clear-history');

// Recent reviews element
const recentReviews = document.getElementById('recent-reviews');

// Metrics elements
const totalReviewsElement = document.getElementById('total-reviews');
const positivePercentElement = document.getElementById('positive-percent');
const negativePercentElement = document.getElementById('negative-percent');

// Initialize the dashboard
document.addEventListener('DOMContentLoaded', function() {
    setupNavigation();
    setupForm();
    loadMetrics();
    loadHistory();

    // Initialize charts
    initSentimentChart();
    initCategoryChart();
});

// Setup navigation
function setupNavigation() {
    dashboardLink.addEventListener('click', function(e) {
        e.preventDefault();
        showView('dashboard');
        setActiveLink('dashboard-link');
        loadMetrics();
        loadHistory();
    });

    analyzeLink.addEventListener('click', function(e) {
        e.preventDefault();
        showView('analyze');
        setActiveLink('analyze-link');
    });

    historyLink.addEventListener('click', function(e) {
        e.preventDefault();
        showView('history');
        setActiveLink('history-link');
        loadHistory();
    });

    modelInfoLink.addEventListener('click', function(e) {
        e.preventDefault();
        showView('model-info');
        setActiveLink('model-info-link');
    });

    clearHistoryBtn.addEventListener('click', function(e) {
        e.preventDefault();
        if (confirm('Are you sure you want to clear all review history?')) {
            clearHistory();
        }
    });
}

// Setup form submission
function setupForm() {
    analyzeForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const reviewText = reviewTextInput.value.trim();
        const category = reviewCategorySelect.value;
        const rating = reviewRatingSelect.value;

        if (!reviewText) {
            alert('Please enter a review text');
            return;
        }

        // Create form data
        const formData = new FormData();
        formData.append('review_text', reviewText);
        formData.append('category', category);
        formData.append('rating', rating);

        // Send to server
        fetch('/predict', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Server responded with status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                displayResult(data);
                loadMetrics();
                loadHistory();
            } else {
                // Display specific error message from server
                alert(`Error: ${data.error || 'Unknown error occurred'}`);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert(`Error analyzing review: ${error.message}`);
        });
    });
}

// Display analysis result
function displayResult(data) {
    originalReviewText.textContent = data.review.text;
    resultCategory.textContent = data.review.category;
    resultRating.textContent = data.review.rating + ' / 5';

    // Use the sentiment_text from server if available, otherwise fall back to sentiment
    const sentimentValue = data.sentiment_text || data.sentiment || 'Unknown';
    const sentimentClass = sentimentValue === 'Positive' ? 'sentiment-positive' : 'sentiment-negative';
    const sentimentIcon = sentimentValue === 'Positive' ? '😊' : '😞';
    const sentimentText = sentimentValue === 'Positive' ? 'Positive Sentiment' : 'Negative Sentiment';

    sentimentResult.innerHTML = `
        <div class="${sentimentClass} text-center">
            <div style="font-size: 3rem;">${sentimentIcon}</div>
            <h3>${sentimentText}</h3>
            <p>Confidence: ${data.confidence * 100}%</p>
        </div>
    `;

    // Update confidence chart
    updateConfidenceChart(data.confidence);

    // Show result section
    resultSection.style.display = 'block';

    // Scroll to result
    resultSection.scrollIntoView({ behavior: 'smooth' });
}

// Initialize sentiment distribution chart
function initSentimentChart() {
    const ctx = document.getElementById('sentimentChart').getContext('2d');
    sentimentChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Positive', 'Negative'],
            datasets: [{
                data: [0, 0],
                backgroundColor: [
                    'rgba(40, 167, 69, 0.7)',
                    'rgba(220, 53, 69, 0.7)'
                ],
                borderColor: [
                    'rgba(40, 167, 69, 1)',
                    'rgba(220, 53, 69, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

// Initialize category distribution chart
function initCategoryChart() {
    const ctx = document.getElementById('categoryChart').getContext('2d');
    categoryChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: 'Number of Reviews',
                data: [],
                backgroundColor: 'rgba(255, 153, 0, 0.7)',
                borderColor: 'rgba(255, 153, 0, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        precision: 0
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

// Update confidence chart
function updateConfidenceChart(confidence) {
    const ctx = document.getElementById('sentiment-confidence').getContext('2d');

    // Destroy previous chart if exists
    if (confidenceChart) {
        confidenceChart.destroy();
    }

    confidenceChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Confidence', ''],
            datasets: [{
                data: [confidence, 1 - confidence],
                backgroundColor: [
                    'rgba(255, 153, 0, 0.7)',
                    'rgba(200, 200, 200, 0.3)'
                ],
                borderColor: [
                    'rgba(255, 153, 0, 1)',
                    'rgba(200, 200, 200, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: false,
            cutout: '70%',
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: false
                }
            }
        }
    });
}

// Load dashboard metrics
function loadMetrics() {
    fetch('/api/metrics')
        .then(response => response.json())
        .then(data => {
            // Update metric cards
            totalReviewsElement.textContent = data.total_reviews;
            positivePercentElement.textContent = data.positive_percent + '%';
            negativePercentElement.textContent = data.negative_percent + '%';

            // Update sentiment chart
            if (sentimentChart) {
                sentimentChart.data.datasets[0].data = [
                    data.sentiments.Positive,
                    data.sentiments.Negative
                ];
                sentimentChart.update();
            }

            // Update category chart
            if (categoryChart) {
                const categories = Object.keys(data.categories);
                const counts = Object.values(data.categories);

                categoryChart.data.labels = categories;
                categoryChart.data.datasets[0].data = counts;
                categoryChart.update();
            }

            // Update recent reviews
            updateRecentReviews();
        })
        .catch(error => {
            console.error('Error loading metrics:', error);
        });
}

// Load review history
function loadHistory() {
    fetch('/api/history')
        .then(response => response.json())
        .then(data => {
            const reviews = data.reviews;

            if (reviews.length === 0) {
                historyList.innerHTML = '<p class="text-muted">No reviews in history yet.</p>';
                return;
            }

            let html = '';
            reviews.reverse().forEach(review => {
                const sentimentClass = review.sentiment === 'Positive' ? 'sentiment-positive' : 'sentiment-negative';
                const sentimentIcon = review.sentiment === 'Positive' ? '😊' : '😞';

                html += `
                    <div class="history-item">
                        <div class="d-flex justify-content-between align-items-start">
                            <div class="flex-grow-1">
                                <p class="mb-1">${review.text.substring(0, 100)}${review.text.length > 100 ? '...' : ''}</p>
                                <div class="d-flex align-items-center">
                                    <span class="badge bg-secondary me-2">${review.category}</span>
                                    <span class="badge bg-warning text-dark me-2">Rating: ${review.rating}/5</span>
                                    <span class="${sentimentClass} me-2">${sentimentIcon} ${review.sentiment}</span>
                                    <small class="text-muted">${review.timestamp}</small>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            });

            historyList.innerHTML = html;
        })
        .catch(error => {
            console.error('Error loading history:', error);
        });
}

// Update recent reviews in dashboard
function updateRecentReviews() {
    fetch('/api/history')
        .then(response => response.json())
        .then(data => {
            const reviews = data.reviews.slice(-5).reverse(); // Get last 5 reviews

            if (reviews.length === 0) {
                recentReviews.innerHTML = '<p class="text-muted">No reviews analyzed yet.</p>';
                return;
            }

            let html = '';
            reviews.forEach(review => {
                const sentimentClass = review.sentiment === 'Positive' ? 'sentiment-positive' : 'sentiment-negative';
                const sentimentIcon = review.sentiment === 'Positive' ? '😊' : '😞';

                html += `
                    <div class="history-item">
                        <div class="d-flex justify-content-between align-items-start">
                            <div class="flex-grow-1">
                                <p class="mb-1">${review.text.substring(0, 100)}${review.text.length > 100 ? '...' : ''}</p>
                                <div class="d-flex align-items-center">
                                    <span class="badge bg-secondary me-2">${review.category}</span>
                                    <span class="${sentimentClass} me-2">${sentimentIcon} ${review.sentiment}</span>
                                    <small class="text-muted">${review.timestamp}</small>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            });

            recentReviews.innerHTML = html;
        })
        .catch(error => {
            console.error('Error updating recent reviews:', error);
        });
}

// Clear review history
function clearHistory() {
    fetch('/api/clear_history', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            loadMetrics();
            loadHistory();
            alert('Review history cleared successfully');
        } else {
            alert('Failed to clear review history');
        }
    })
    .catch(error => {
        console.error('Error clearing history:', error);
        alert('Failed to clear review history');
    });
}

// Show specific view
function showView(viewName) {
    // Hide all views
    dashboardView.style.display = 'none';
    analyzeView.style.display = 'none';
    historyView.style.display = 'none';
    modelInfoView.style.display = 'none';

    // Show selected view
    switch(viewName) {
        case 'dashboard':
            dashboardView.style.display = 'block';
            break;
        case 'analyze':
            analyzeView.style.display = 'block';
            break;
        case 'history':
            historyView.style.display = 'block';
            break;
        case 'model-info':
            modelInfoView.style.display = 'block';
            break;
    }
}

// Set active navigation link
function setActiveLink(linkId) {
    // Remove active class from all links
    dashboardLink.classList.remove('active');
    analyzeLink.classList.remove('active');
    historyLink.classList.remove('active');
    modelInfoLink.classList.remove('active');

    // Add active class to selected link
    document.getElementById(linkId).classList.add('active');
}
