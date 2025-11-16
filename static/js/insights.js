// Insights page specific JavaScript
function insights() {
    return {
        filters: {
            category: 'all',
            timeRange: '30',
            rating: 'all'
        },

        charts: {
            sentimentTrend: null,
            categoryDistribution: null
        },

        init() {
            this.initCharts();
            this.loadInsights();
        },

        async loadInsights() {
            try {
                const response = await api.getInsights();
                if (response.success) {
                    this.updateCharts(response.insights);
                } else {
                    notifications.error('Failed to load insights');
                }
            } catch (error) {
                notifications.error('Error loading insights: ' + error.message);
            }
        },

        applyFilters() {
            // Apply filters and reload data
            this.loadInsights();
        },

        initCharts() {
            // Sentiment Trend Chart
            const sentimentCtx = document.getElementById('sentimentTrendChart').getContext('2d');
            this.charts.sentimentTrend = new Chart(sentimentCtx, {
                type: 'line',
                data: {
                    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                    datasets: [
                        {
                            label: 'Positive',
                            data: [65, 68, 66, 70, 68, 72],
                            borderColor: 'rgba(40, 167, 69, 1)',
                            backgroundColor: 'rgba(40, 167, 69, 0.1)',
                            fill: true,
                            tension: 0.4
                        },
                        {
                            label: 'Negative',
                            data: [35, 32, 34, 30, 32, 28],
                            borderColor: 'rgba(220, 53, 69, 1)',
                            backgroundColor: 'rgba(220, 53, 69, 0.1)',
                            fill: true,
                            tension: 0.4
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'top',
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100,
                            ticks: {
                                callback: function(value) {
                                    return value + '%';
                                }
                            }
                        }
                    }
                }
            });

            // Category Distribution Chart
            const categoryCtx = document.getElementById('categoryChart').getContext('2d');
            this.charts.categoryDistribution = new Chart(categoryCtx, {
                type: 'bar',
                data: {
                    labels: ['Electronics', 'Books', 'Clothing', 'Home & Kitchen', 'Sports', 'Toys'],
                    datasets: [
                        {
                            label: 'Positive',
                            data: [72, 68, 65, 70, 58, 75],
                            backgroundColor: 'rgba(40, 167, 69, 0.8)',
                        },
                        {
                            label: 'Negative',
                            data: [28, 32, 35, 30, 42, 25],
                            backgroundColor: 'rgba(220, 53, 69, 0.8)',
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: {
                            stacked: true,
                        },
                        y: {
                            stacked: true,
                            beginAtZero: true,
                            max: 100,
                            ticks: {
                                callback: function(value) {
                                    return value + '%';
                                }
                            }
                        }
                    }
                }
            });
        },

        updateCharts(data) {
            // Update sentiment trend chart
            if (this.charts.sentimentTrend && data.trend_data) {
                this.charts.sentimentTrend.data.labels = data.trend_data.labels;
                this.charts.sentimentTrend.data.datasets[0].data = data.trend_data.positive;
                this.charts.sentimentTrend.data.datasets[1].data = data.trend_data.negative;
                this.charts.sentimentTrend.update();
            }

            // Update category distribution chart
            if (this.charts.categoryDistribution && data.category_data) {
                this.charts.categoryDistribution.data.labels = data.category_data.labels;
                this.charts.categoryDistribution.data.datasets[0].data = data.category_data.positive;
                this.charts.categoryDistribution.data.datasets[1].data = data.category_data.negative;
                this.charts.categoryDistribution.update();
            }
        }
    }
}
