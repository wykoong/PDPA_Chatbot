const { createApp } = Vue

createApp({
    data() {
        return {
            messages: [],
            newMessage: '',
            loading: false
        }
    },
    methods: {
        async sendMessage() {
            if (!this.newMessage.trim()) return

            // Add user message
            this.messages.push({
                type: 'user',
                content: this.newMessage
            })

            const question = this.newMessage
            this.newMessage = ''
            this.loading = true

            // Reset textarea height after sending
            this.$nextTick(() => {
                this.adjustTextareaHeight();
            });

            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ question })
                })
                const data = await response.json()

                // Add bot message
                this.messages.push({
                    type: 'bot',
                    content: data.response
                })

                // Highlight code blocks
                this.$nextTick(() => {
                    document.querySelectorAll('pre code').forEach((block) => {
                        hljs.highlightBlock(block)
                    })
                })
            } catch (error) {
                this.messages.push({
                    type: 'bot',
                    content: 'Sorry, there was an error processing your request.'
                })
            } finally {
                this.loading = false
                this.scrollToBottom()
            }
        },
        scrollToBottom() {
            this.$nextTick(() => {
                const container = this.$refs.chatMessages;
                container.scrollTop = container.scrollHeight;
                // Force scroll after a short delay to ensure content is rendered
                setTimeout(() => {
                    container.scrollTop = container.scrollHeight;
                }, 100);
            });
        },
        adjustTextareaHeight() {
            // Auto-grow the textarea as user types
            const textarea = this.$refs.userInput;
            if (textarea) {
                textarea.style.height = 'auto';
                textarea.style.height = textarea.scrollHeight + 'px';
            }
        }
    },
    mounted() {
        // Add welcome message
        this.messages.push({
            type: 'bot',
            content: 'Hello! I can help you with questions about personal data privacy and AI governance. What would you like to know?'
        });
        // Ensure the textarea is the right height on load
        this.$nextTick(() => {
            this.adjustTextareaHeight();
        });

        // Maximize button functionality
        const maximizeBtn = document.getElementById('maximizeBtn');
        const card = document.querySelector('.card');
        maximizeBtn.addEventListener('click', () => {
            card.classList.toggle('maximized');
            if (card.classList.contains('maximized')) {
                maximizeBtn.innerHTML = '<i class="fas fa-compress"></i>';
            } else {
                maximizeBtn.innerHTML = '<i class="fas fa-expand"></i>';
            }
        });
    }
}).mount('#app')
