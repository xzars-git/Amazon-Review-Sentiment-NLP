// Dashboard JavaScript with Alpine.js and Chart.js

document.addEventListener('alpine:init', () => {
    // Global data store for reviews
    Alpine.store('reviews', {
        history: [],
        currentReview: null,

        addReview(review) {
            this.history.unshift(review);
            // Keep only last 100 reviews in memory
            if (this.history.length > 100) {
                this.history.pop();
            }
        },

        getReview(id) {
            return this.history.find(review => review.id === id);
        },

        deleteReview(id) {
            this.history = this.history.filter(review => review.id !== id);
        }
    });
});

// Dashboard component
function dashboard() {
    return {
        charts: {
            sentiment: null,
            rating: null
        },
        recentAnalysis: [],
        recentAnalysisHtml: '',

        init() {
            this.$nextTick(() => {
                this.loadRecentAnalysis();
                this.initCharts();
            });
        },

        async loadRecentAnalysis() {
            try {
                // Get review history from API
                const response = await api.getReviewHistory();

                if (response.success && response.history && response.history.length > 0) {
                    this.recentAnalysis = response.history.slice(0, 5); // Get only the 5 most recent
                    this.updateRecentAnalysisHtml();
                } else {
                    // Use mock data if no history is available
                    this.recentAnalysis = [
                        {
                            id: 1,
                            text: "This product exceeded my expectations! The quality is outstanding.",
                            category: "Electronics",
                            rating: 5,
                            sentiment: "Positive",
                            confidence: 0.92,
                            timestamp: new Date().toISOString()
                        },
                        {
                            id: 2,
                            text: "I'm very disappointed with this purchase. Poor quality materials.",
                            category: "Home & Kitchen",
                            rating: 2,
                            sentiment: "Negative",
                            confidence: 0.87,
                            timestamp: new Date(Date.now() - 86400000).toISOString()
                        },
                        {
                            id: 3,
                            text: "Average product, nothing special. The price is too high.",
                            category: "Sports",
                            rating: 3,
                            sentiment: "Negative",
                            confidence: 0.78,
                            timestamp: new Date(Date.now() - 172800000).toISOString()
                        },
                        {
                            id: 4,
                            text: "Absolutely love it! Best purchase I've made this year.",
                            category: "Clothing",
                            rating: 5,
                            sentiment: "Positive",
                            confidence: 0.95,
                            timestamp: new Date(Date.now() - 259200000).toISOString()
                        },
                        {
                            id: 5,
                            text: "Not worth the money. The product looks cheap.",
                            category: "Books",
                            rating: 1,
                            sentiment: "Negative",
                            confidence: 0.89,
                            timestamp: new Date(Date.now() - 345600000).toISOString()
                        }
                    ];
                    this.updateRecentAnalysisHtml();
                }
            } catch (error) {
                console.error("Error loading recent analysis:", error);
                // Use mock data as fallback
                this.recentAnalysis                    {
                        id: 1,
                        text: "This product exceeded my expectations! The quality is outstanding.",
                        category: "Electronics",
                        rating: 5,
                        sentiment: "Positive",
                        confidence: 0.92,
                        timestamp: new Date().toISOString()
                    },
                    {
                        id: 2,
                        text: "I'm very disappointed with this purchase. Poor quality materials.",
                        category: "Home & Kitchen",
                        rating: 2,
                        sentiment: "Negative",
                        confidence: 0.87,
                        timestamp: new Date(Date.now() - 86400000).toISOString()
                    }
                ];
                this.updateRecentAnalysisHtml();
            }
        },

        updateRecentAnalysisHtml() {
            let html = '';

            this.recentAnalysis.forEach(review => {
                const date = new Date(review.timestamp).toLocaleDateString();
                const sentimentClass = review.sentiment === 'Positive' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800';
                const sentimentColor = review.sentiment === 'Positive' ? 'text-green-500' : 'text-red-500';
                const truncatedText = review.text.length > 50 ? review.text.substring(0, 50) + '...' : review.text;

                html += `
                    <tr>
                        <td class="px-6 py-4">
                            <div class="text-sm text-gray-900">${truncatedText}</div>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <div class="text-sm text-gray-900">${review.category}</div>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <div class="flex items-center">
                                <div class="flex">
                                    ${utils.getStarRating(review.rating)}
                                </div>
                                <span class="ml-2 text-sm text-gray-900">${review.rating}/5</span>
                            </div>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${sentimentClass}">
                                ${review.sentiment}
                            </span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <div class="w-full bg-gray-200 rounded-full h-2">
                                <div class="h-2 rounded-full ${sentimentColor}" style="width: ${review.confidence * 100}%"></div>
                            </div>
                            <div class="text-xs text-gray-500 mt-1">${Math.round(review.confidence * 100)}%</div>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            ${date}
                        </td>
                    </tr>
                `;
            });

            this.recentAnalysisHtml = html;
        },

        initCharts() {
            // Sentiment Distribution Chart
            const sentimentCtx = document.getElementById('sentimentChart');
            if (sentimentCtx) {
                this.charts.sentiment = new Chart(sentimentCtx, {
                    type: 'doughnut',
                    data: {
                        labels: ['Positive', 'Negative'],
                        datasets: [{
                            data: [68, 32],
                            backgroundColor: [
                                'rgba(40, 167, 69, 0.8)',
                                'rgba(220, 53, 69, 0.8)'
                            ],
                            borderWidth: 0
                        }]
                    },
                    options: {
                        ...chartConfig.defaultOptions,
                        cutout: '70%',
                        plugins: {
                            legend: {
                                position: 'bottom',
                                labels: {
                                    padding: 20,
                                    usePointStyle: true
                                }
                            }
                        }
                    }
                });
            }

            // Rating Distribution Chart
            const ratingCtx = document.getElementById('ratingChart');
            if (ratingCtx) {
                this.charts.rating = new Chart(ratingCtx, {
                    type: 'bar',
                    data: {
                        labels: ['1 Star', '2 Stars', '3 Stars', '4 Stars', '5 Stars'],
                        datasets: [{
                            label: 'Number of Reviews',
                            data: [10, 15, 25, 30, 20],
                            backgroundColor: [
                                'rgba(220, 53, 69, 0.8)',
                                'rgba(255, 193, 7, 0.8)',
                                'rgba(255, 193, 7, 0.8)',
                                'rgba(40, 167, 69, 0.8)',
                                'rgba(40, 167, 69, 0.8)'
                            ],
                            borderWidth: 0
                        }]
                    },
                    options: {
                        ...chartConfig.defaultOptions,
                        scales: {
                            y: {
                                beginAtZero: true,
                                ticks: {
                                    precision: 0
                                }
                            }
                        }
                    }
                });
            }
        }
    };
}

// Utility functions
const utils = {
    formatDate(date) {
        const options = { 
            year: 'numeric', 
            month: 'short', 
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        };
        return new Date(date).toLocaleDateString(undefined, options);
    },

    truncateText(text, maxLength) {
        if (text.length <= maxLength) return text;
        return text.substring(0, maxLength) + '...';
    },

    getStarRating(rating) {
        let stars = '';
        for (let i = 1; i <= 5; i++) {
            stars += `<i class="fas fa-star ${i <= rating ? 'text-yellow-400' : 'text-gray-300'}"></i>`;
        }
        return stars;
    },

    animateValue(element, start, end, duration) {
        const range = end - start;
        const increment = end > start ? 1 : -1;
        const stepTime = Math.abs(Math.floor(duration / range));
        let current = start;

        const timer = setInterval(() => {
            current += increment;
            element.textContent = current;
            if (current === end) {
                clearInterval(timer);
            }
        }, stepTime);
    }
};

// Chart configurations
const chartConfig = {
    sentimentColors: {
        positive: 'rgba(40, 167, 69, 0.8)',
        negative: 'rgba(220, 53, 69, 0.8)',
        neutral: 'rgba(255, 193, 7, 0.8)'
    },

    defaultOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom',
            }
        }
    }
};

// API service
const api = {
    async analyzeReview(reviewData) {
        const formData = new FormData();
        formData.append('review_text', reviewData.text);
        formData.append('category', reviewData.category);
        formData.append('rating', reviewData.rating);

        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Server responded with status: ${response.status}`);
        }

        return await response.json();
    },

    async getReviewHistory() {
        const response = await fetch('/history');
        if (!response.ok) {
            throw new Error(`Server responded with status: ${response.status}`);
        }
        return await response.json();
    },

    async deleteReview(id) {
        const response = await fetch(`/history/${id}`, {
            method: 'DELETE'
        });

        if (!response.ok) {
            throw new Error(`Server responded with status: ${response.status}`);
        }

        return await response.json();
    },

    async getInsights() {
        const response = await fetch('/insights/data');
        if (!response.ok) {
            throw new Error(`Server responded with status: ${response.status}`);
        }
        return await response.json();
    }
};

// Notification system
const notifications = {
    show(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `fixed bottom-4 right-4 p-4 rounded-lg shadow-lg z-50 transform transition-all duration-500 ${
            type === 'success' ? 'bg-green-500' : 
            type === 'error' ? 'bg-red-500' : 
            type === 'warning' ? 'bg-yellow-500' : 'bg-blue-500'
        } text-white`;
        notification.textContent = message;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.opacity = '0';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 500);
        }, 3000);
    },

    success(message) {
        this.show(message, 'success');
    },

    error(message) {
        this.show(message, 'error');
    },

    warning(message) {
        this.show(message, 'warning');
    },

    info(message) {
        this.show(message, 'info');
    }
};
