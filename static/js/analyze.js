// Analyze page specific JavaScript
function analyzeReview() {
    return {
        reviewText: '',
        category: 'Electronics',
        rating: 5,
        isAnalyzing: false,
        results: null,

        sampleReviews: [
            {
                id: 1,
                text: 'This product exceeded my expectations! The quality is outstanding and it arrived earlier than expected. Highly recommend!',
                category: 'Electronics',
                rating: 5
            },
            {
                id: 2,
                text: 'I\'m very disappointed with this purchase. The product broke after just one week of use. Poor quality materials.',
                category: 'Home & Kitchen',
                rating: 2
            },
            {
                id: 3,
                text: 'Average product, nothing special. It does what it\'s supposed to do but the price is too high for what you get.',
                category: 'Sports',
                rating: 3
            },
            {
                id: 4,
                text: 'Absolutely love it! Best purchase I\'ve made this year. The design is elegant and it works perfectly.',
                category: 'Clothing',
                rating: 5
            },
            {
                id: 5,
                text: 'Not worth the money. The product looks cheap and doesn\'t match the description at all.',
                category: 'Books',
                rating: 1
            }
        ],

        init() {
            // Initialize any required components
        },

        async analyzeReview() {
            if (!this.reviewText.trim()) {
                notifications.warning('Please enter a review text to analyze');
                return;
            }

            this.isAnalyzing = true;

            try {
                const response = await api.analyzeReview({
                    text: this.reviewText,
                    category: this.category,
                    rating: this.rating
                });

                if (response.success) {
                    this.results = {
                        sentiment: response.sentiment,
                        confidence: response.confidence,
                        category: this.category,
                        rating: this.rating,
                        timestamp: new Date().toLocaleString()
                    };

                    notifications.success('Analysis completed successfully');
                } else {
                    notifications.error('Analysis failed: ' + response.error);
                }
            } catch (error) {
                notifications.error('Error: ' + error.message);
            } finally {
                this.isAnalyzing = false;
            }
        },

        useSample(sample) {
            this.reviewText = sample.text;
            this.category = sample.category;
            this.rating = sample.rating;
        }
    }
}
