// History page specific JavaScript
function reviewHistory() {
    return {
        filterSentiment: '',
        filterCategory: '',
        currentPage: 1,
        itemsPerPage: 10,
        history: [],
        filteredHistory: [],

        init() {
            this.loadHistory();
            this.filterHistory();
        },

        async loadHistory() {
            try {
                const response = await api.getReviewHistory();
                if (response.success && response.history && response.history.length > 0) {
                    this.history = response.history.map(review => ({
                        ...review,
                        expanded: false
                    }));
                } else {
                    // Use mock data if no history is available
                    this.history = [
                        {
                            id: 1,
                            text: "This product exceeded my expectations! The quality is outstanding and it arrived earlier than expected. Highly recommend!",
                            category: "Electronics",
                            rating: 5,
                            sentiment: "Positive",
                            confidence: 0.92,
                            date: new Date().toLocaleDateString()
                        },
                        {
                            id: 2,
                            text: "I'm very disappointed with this purchase. The product broke after just one week of use. Poor quality materials.",
                            category: "Home & Kitchen",
                            rating: 2,
                            sentiment: "Negative",
                            confidence: 0.87,
                            date: new Date(Date.now() - 86400000).toLocaleDateString()
                        },
                        {
                            id: 3,
                            text: "Average product, nothing special. It does what it's supposed to do but the price is too high for what you get.",
                            category: "Sports",
                            rating: 3,
                            sentiment: "Negative",
                            confidence: 0.78,
                            date: new Date(Date.now() - 172800000).toLocaleDateString()
                        },
                        {
                            id: 4,
                            text: "Absolutely love it! Best purchase I've made this year. The design is elegant and it works perfectly.",
                            category: "Clothing",
                            rating: 5,
                            sentiment: "Positive",
                            confidence: 0.95,
                            date: new Date(Date.now() - 259200000).toLocaleDateString()
                        },
                        {
                            id: 5,
                            text: "Not worth the money. The product looks cheap and doesn't match the description at all.",
                            category: "Books",
                            rating: 1,
                            sentiment: "Negative",
                            confidence: 0.89,
                            date: new Date(Date.now() - 345600000).toLocaleDateString()
                        }
                    ];
                }
                this.filterHistory();
            } catch (error) {
                notifications.error('Error loading history: ' + error.message);
                // Use mock data as fallback
                this.history = [
                    {
                        id: 1,
                        text: "This product exceeded my expectations! The quality is outstanding.",
                        category: "Electronics",
                        rating: 5,
                        sentiment: "Positive",
                        confidence: 0.92,
                        date: new Date().toLocaleDateString()
                    },
                    {
                        id: 2,
                        text: "I'm very disappointed with this purchase. Poor quality materials.",
                        category: "Home & Kitchen",
                        rating: 2,
                        sentiment: "Negative",
                        confidence: 0.87,
                        date: new Date(Date.now() - 86400000).toLocaleDateString()
                    }
                ];
                this.filterHistory();
            }
        },

        filterHistory() {
            let filtered = [...this.history];

            if (this.filterSentiment) {
                filtered = filtered.filter(review => review.sentiment === this.filterSentiment);
            }

            if (this.filterCategory) {
                filtered = filtered.filter(review => review.category === this.filterCategory);
            }

            this.filteredHistory = filtered;
            this.currentPage = 1;
        },

        get totalPages() {
            return Math.ceil(this.filteredHistory.length / this.itemsPerPage);
        },

        get paginatedHistory() {
            const start = (this.currentPage - 1) * this.itemsPerPage;
            const end = start + this.itemsPerPage;
            return this.filteredHistory.slice(start, end);
        },

        nextPage() {
            if (this.currentPage < this.totalPages) {
                this.currentPage++;
            }
        },

        prevPage() {
            if (this.currentPage > 1) {
                this.currentPage--;
            }
        },

        goToPage(page) {
            this.currentPage = page;
        },

        viewDetails(review) {
            // Navigate to review details or show modal
            console.log('View details for review:', review);
        },

        async deleteReview(id) {
            if (confirm('Are you sure you want to delete this review?')) {
                try {
                    const response = await api.deleteReview(id);
                    if (response.success) {
                        notifications.success('Review deleted successfully');
                        await this.loadHistory();
                        this.filterHistory();
                    } else {
                        notifications.error('Failed to delete review');
                    }
                } catch (error) {
                    notifications.error('Error: ' + error.message);
                }
            }
        },

        exportHistory() {
            // Generate CSV from history data
            const csv = this.generateCSV(this.filteredHistory);
            const blob = new Blob([csv], { type: 'text/csv' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'review_history.csv';
            a.click();
            URL.revokeObjectURL(url);
        },

        generateCSV(data) {
            const headers = ['ID', 'Text', 'Category', 'Rating', 'Sentiment', 'Confidence', 'Date'];
            const rows = data.map(review => [
                review.id,
                `"${review.text.replace(/"/g, '""')}"`,
                review.category,
                review.rating,
                review.sentiment,
                review.confidence,
                review.date
            ]);

            return [headers, ...rows].map(row => row.join(',')).join('\n');
        },

        get summary() {
            const total = this.filteredHistory.length;
            const positive = this.filteredHistory.filter(r => r.sentiment === 'Positive').length;
            const negative = this.filteredHistory.filter(r => r.sentiment === 'Negative').length;
            const avgConfidence = total > 0 
                ? Math.round(this.filteredHistory.reduce((sum, r) => sum + r.confidence, 0) / total * 100)
                : 0;

            return {
                total,
                positive,
                negative,
                avgConfidence
            };
        }
    }
}
