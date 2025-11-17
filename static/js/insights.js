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
            this.$nextTick(() => {
                this.initCharts();
                this.loadInsights();
            });
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
            // Show loading state
            const button = event.target;
            const originalText = button.innerHTML;
            button.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Applying...';
            button.disabled = true;

            // Simulate API call
            setTimeout(() => {
                // Update charts with new data based on filters
                this.updateChartsData();

                // Reset button
                button.innerHTML = originalText;
                button.disabled = false;

                // Show success notification
                notifications.success('Filters applied successfully');
            }, 1000);
        },

        updateChartsData() {
            // Generate new data based on filters
            const categoryIndex = this.filters.category !== 'all' ? 
                ['Electronics', 'Books', 'Clothing', 'Home & Kitchen', 'Sports', 'Toys'].indexOf(this.filters.category) : -1;

            // Update sentiment trend chart
            if (this.charts.sentimentTrend) {
                const newPositiveData = categoryIndex >= 0 ? 
                    [65, 68, 66, 70, 68, 72].map(v => v + Math.random() * 10 - 5) :
                    [65, 68, 66, 70, 68, 72];

                const newNegativeData = newPositiveData.map(v => 100 - v);

                this.charts.sentimentTrend.data.datasets[0].data = newPositiveData;
                this.charts.sentimentTrend.data.datasets[1].data = newNegativeData;
                this.charts.sentimentTrend.update();
            }

            // Update category chart
            if (this.charts.categoryDistribution) {
                const newPositiveData = [72, 68, 65, 70, 58, 75].map(v => v + Math.random() * 10 - 5);
                const newNegativeData = newPositiveData.map(v => 100 - v);

                this.charts.categoryDistribution.data.datasets[0].data = newPositiveData;
                this.charts.categoryDistribution.data.datasets[1].data = newNegativeData;
                this.charts.categoryDistribution.update();
            }
        },

        initCharts() {
            try {
                // Sentiment Trend Chart
                const sentimentCtx = document.getElementById('sentimentTrendChart');
                if (sentimentCtx) {
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
                }

                // Category Distribution Chart
                const categoryCtx = document.getElementById('categoryChart');
                if (categoryCtx) {
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
                }
            } catch (error) {
                console.error('Error initializing charts:', error);
                notifications.error('Failed to initialize charts: ' + error.message);
            }
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