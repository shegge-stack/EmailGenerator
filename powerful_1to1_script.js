/**
 * Powerful 1:1 Email Generator - JavaScript
 */

class EmailGenerator {
    constructor() {
        this.initializeEventListeners();
        this.initializeCharacterCounts();
        this.lastGeneratedEmail = null;
        this.currentView = 'preview';
    }

    initializeEventListeners() {
        // LinkedIn URL enrichment
        const enrichBtn = document.getElementById('enrichBtn');
        const linkedinUrl = document.getElementById('linkedinUrl');
        
        enrichBtn.addEventListener('click', () => this.enrichFromLinkedIn());
        linkedinUrl.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                this.enrichFromLinkedIn();
            }
        });

        // Drag and drop for LinkedIn URL
        const dropZone = document.getElementById('linkedinDropZone');
        this.initializeDragDrop(dropZone);

        // Form submission
        const form = document.getElementById('emailForm');
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.generateEmail();
        });

        // Output view controls
        const viewButtons = document.querySelectorAll('[data-view]');
        viewButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const view = e.target.dataset.view;
                this.switchView(view);
            });
        });

        // Copy button
        const copyBtn = document.getElementById('copyBtn');
        copyBtn.addEventListener('click', () => this.copyToClipboard());

        // Real-time validation
        const requiredInputs = document.querySelectorAll('input[required], textarea[required]');
        requiredInputs.forEach(input => {
            input.addEventListener('input', () => this.validateForm());
        });
    }

    initializeCharacterCounts() {
        const textareas = [
            { element: 'textarea[name="activity"]', counter: 'activityCount', max: 500 },
            { element: 'textarea[name="caseStudy"]', counter: 'caseStudyCount', max: 300 },
            { element: 'textarea[name="ICP"]', counter: 'icpCount', max: 200 }
        ];

        textareas.forEach(({ element, counter, max }) => {
            const textarea = document.querySelector(element);
            const counterElement = document.getElementById(counter);

            textarea.addEventListener('input', () => {
                const length = textarea.value.length;
                counterElement.textContent = `${length}/${max} characters`;
                counterElement.style.color = length > max * 0.9 ? '#ef4444' : '#6b7280';
            });
        });
    }

    initializeDragDrop(dropZone) {
        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.classList.add('dragover');
        });

        dropZone.addEventListener('dragleave', () => {
            dropZone.classList.remove('dragover');
        });

        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.classList.remove('dragover');

            const text = e.dataTransfer.getData('text/plain');
            if (this.isLinkedInUrl(text)) {
                document.getElementById('linkedinUrl').value = text;
                this.enrichFromLinkedIn();
            }
        });
    }

    isLinkedInUrl(url) {
        const linkedinPattern = /https?:\/\/(www\.)?linkedin\.com\/in\/([^/?]+)/i;
        return linkedinPattern.test(url);
    }

    async enrichFromLinkedIn() {
        const linkedinUrl = document.getElementById('linkedinUrl').value.trim();
        const enrichBtn = document.getElementById('enrichBtn');
        const statusElement = document.getElementById('enrichmentStatus');

        if (!linkedinUrl) {
            this.showStatus('Please enter a LinkedIn URL', 'error');
            return;
        }

        if (!this.isLinkedInUrl(linkedinUrl)) {
            this.showStatus('Please enter a valid LinkedIn URL', 'error');
            return;
        }

        // Show loading state
        enrichBtn.disabled = true;
        enrichBtn.innerHTML = '⏳ Auto-Filling...';
        statusElement.style.display = 'block';
        statusElement.className = 'enrichment-status manual';
        statusElement.textContent = 'Processing LinkedIn URL...';

        try {
            // Simulate API call (replace with your actual enrichment API)
            const enrichedData = await this.callEnrichmentAPI(linkedinUrl);
            
            if (enrichedData.success) {
                this.fillFormWithData(enrichedData.data);
                statusElement.className = 'enrichment-status enriched';
                statusElement.textContent = `✅ Auto-filled from ${enrichedData.source || 'LinkedIn'}`;
                this.showStatus('Successfully auto-filled prospect information!', 'success');
            } else {
                // Partial data or manual input required
                this.fillFormWithData(enrichedData.data || {});
                statusElement.className = 'enrichment-status manual';
                statusElement.textContent = '⚠️ Manual input required - no API enrichment available';
                this.showStatus('LinkedIn URL validated. Please complete the missing fields manually.', 'warning');
            }
        } catch (error) {
            console.error('Enrichment error:', error);
            statusElement.className = 'enrichment-status manual';
            statusElement.textContent = '❌ Enrichment failed - please fill manually';
            this.showStatus('Unable to auto-fill. Please complete the form manually.', 'error');
        } finally {
            enrichBtn.disabled = false;
            enrichBtn.innerHTML = '🚀 Auto-Fill';
        }
    }

    async callEnrichmentAPI(linkedinUrl) {
        // Simulate API call - replace with your actual API endpoint
        return new Promise((resolve) => {
            setTimeout(() => {
                // Mock enrichment logic
                const username = linkedinUrl.split('/in/')[1]?.split(/[/?]/)[0];
                
                // Mock database of known profiles
                const mockData = {
                    'samuel-hegge': {
                        firstName: 'Samuel',
                        lastName: 'Hegge',
                        companyName: 'Singular',
                        companyWebsite: 'https://singular.net',
                        title: 'Founder & CEO',
                        industry: 'Mobile Marketing Technology',
                        activity: 'Leading mobile attribution and marketing analytics platform serving top mobile apps like TikTok and Airbnb'
                    },
                    'john-doe': {
                        firstName: 'John',
                        lastName: 'Doe',
                        companyName: 'TechCorp',
                        companyWebsite: 'https://techcorp.com',
                        title: 'VP of Sales',
                        industry: 'B2B SaaS',
                        activity: 'Recently expanded sales team by 40% and launched new enterprise features'
                    }
                };

                if (mockData[username]) {
                    resolve({
                        success: true,
                        data: { ...mockData[username], linkedinURL: linkedinUrl },
                        source: 'Mock API'
                    });
                } else {
                    // Parse basic info from username
                    const nameParts = username.split('-');
                    resolve({
                        success: false,
                        data: {
                            firstName: nameParts[0]?.charAt(0).toUpperCase() + nameParts[0]?.slice(1) || '',
                            lastName: nameParts[1]?.charAt(0).toUpperCase() + nameParts[1]?.slice(1) || '',
                            linkedinURL: linkedinUrl
                        },
                        source: 'URL parsing'
                    });
                }
            }, 1500); // Simulate API delay
        });
    }

    fillFormWithData(data) {
        const form = document.getElementById('emailForm');
        
        Object.entries(data).forEach(([key, value]) => {
            const input = form.querySelector(`[name="${key}"]`);
            if (input && value) {
                input.value = value;
                // Trigger input event for validation
                input.dispatchEvent(new Event('input'));
            }
        });

        this.validateForm();
    }

    async generateEmail() {
        const form = document.getElementById('emailForm');
        const generateBtn = document.getElementById('generateBtn');
        const statusIndicator = document.getElementById('statusIndicator');

        // Collect form data
        const formData = new FormData(form);
        const data = {};
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }

        // Add LinkedIn URL if available
        const linkedinUrl = document.getElementById('linkedinUrl').value.trim();
        if (linkedinUrl) {
            data.linkedinURL = linkedinUrl;
        }

        // Show generating state
        generateBtn.disabled = true;
        generateBtn.innerHTML = '🔄 Generating Email...';
        statusIndicator.className = 'status-indicator status-generating';
        statusIndicator.innerHTML = 'Generating your powerful email<span class="loading-dots"></span>';

        try {
            const response = await this.callEmailGenerationAPI(data);
            
            if (response.success) {
                this.lastGeneratedEmail = response;
                this.displayEmail(response);
                statusIndicator.className = 'status-indicator status-ready';
                statusIndicator.textContent = '✅ Email generated successfully!';
            } else {
                throw new Error(response.error || 'Generation failed');
            }
        } catch (error) {
            console.error('Email generation error:', error);
            statusIndicator.className = 'status-indicator status-error';
            statusIndicator.textContent = '❌ Generation failed. Please try again.';
            this.displayError(error.message);
        } finally {
            generateBtn.disabled = false;
            generateBtn.innerHTML = '✨ Generate Powerful Email';
        }
    }

    async callEmailGenerationAPI(data) {
        // Replace with your actual API endpoint
        const API_ENDPOINT = '/api/generate-email';
        
        try {
            const response = await fetch(API_ENDPOINT, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    ...data,
                    enhanced: true,
                    includeAnalysis: true
                })
            });

            if (!response.ok) {
                throw new Error(`API Error: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            // Fallback to mock generation for demo
            console.log('Using mock generation (no API available)');
            return this.mockEmailGeneration(data);
        }
    }

    mockEmailGeneration(data) {
        // Mock email generation for demo purposes
        return new Promise((resolve) => {
            setTimeout(() => {
                const mockEmail = {
                    success: true,
                    email: {
                        subject: `${data.companyName}: Partnership Opportunity`,
                        body: `Dear ${data.firstName},

I've been following ${data.companyName}'s impressive growth and thought you'd be interested in how we've helped similar companies scale their operations.

${data.caseStudy}

Given ${data.companyName}'s focus on ${data.industry}, I believe our solution could complement your current efforts and help you achieve similar results.

Would you be open to a brief conversation to explore this further?

Book time [here](${data.meetingLink}) at your convenience.

Best regards,
${data.senderName}
${data.senderTitle}
${data.senderCompany}`
                    },
                    analysis: {
                        wordCount: 89,
                        sentiment: 'Professional',
                        personalization: ['Company name', 'Industry', 'First name'],
                        callToAction: 'Meeting booking link'
                    },
                    prospect: `${data.firstName} ${data.lastName} at ${data.companyName}`
                };
                resolve(mockEmail);
            }, 2000);
        });
    }

    displayEmail(response) {
        const outputElement = document.getElementById('emailOutput');
        const copyBtn = document.getElementById('copyBtn');

        copyBtn.style.display = 'block';

        if (this.currentView === 'preview') {
            this.displayPreview(response.email);
        } else if (this.currentView === 'text') {
            this.displayPlainText(response.email);
        } else if (this.currentView === 'analysis') {
            this.displayAnalysis(response.analysis);
        }
    }

    displayPreview(email) {
        const outputElement = document.getElementById('emailOutput');
        
        const formattedBody = email.body
            .replace(/\n\n/g, '</p><p>')
            .replace(/\n/g, '<br>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" style="color: #4f46e5;">$1</a>');

        outputElement.innerHTML = `
            <div class="subject-line">
                <strong>Subject:</strong> ${email.subject}
            </div>
            <div class="email-body">
                <p>${formattedBody}</p>
            </div>
            <button class="copy-btn" id="copyBtn" onclick="emailGenerator.copyToClipboard()">📋 Copy</button>
        `;
    }

    displayPlainText(email) {
        const outputElement = document.getElementById('emailOutput');
        
        const plainText = `Subject: ${email.subject}\n\n${email.body}`;
        
        outputElement.innerHTML = `
            <pre style="font-family: 'SF Mono', Monaco, monospace; font-size: 14px; line-height: 1.5; white-space: pre-wrap; margin: 0;">${plainText}</pre>
            <button class="copy-btn" id="copyBtn" onclick="emailGenerator.copyToClipboard()">📋 Copy</button>
        `;
    }

    displayAnalysis(analysis) {
        const outputElement = document.getElementById('emailOutput');
        
        outputElement.innerHTML = `
            <div style="space-y: 16px;">
                <h3 style="color: #374151; margin-bottom: 16px;">📊 Email Analysis</h3>
                
                <div style="background: #f3f4f6; padding: 16px; border-radius: 8px; margin-bottom: 16px;">
                    <div style="font-weight: 600; margin-bottom: 8px;">Metrics</div>
                    <div>Word Count: ${analysis.wordCount} words</div>
                    <div>Sentiment: ${analysis.sentiment}</div>
                </div>
                
                <div style="background: #f3f4f6; padding: 16px; border-radius: 8px; margin-bottom: 16px;">
                    <div style="font-weight: 600; margin-bottom: 8px;">Personalization Elements</div>
                    <ul style="margin: 0; padding-left: 20px;">
                        ${analysis.personalization.map(item => `<li>${item}</li>`).join('')}
                    </ul>
                </div>
                
                <div style="background: #f3f4f6; padding: 16px; border-radius: 8px;">
                    <div style="font-weight: 600; margin-bottom: 8px;">Call to Action</div>
                    <div>${analysis.callToAction}</div>
                </div>
            </div>
            <button class="copy-btn" id="copyBtn" onclick="emailGenerator.copyToClipboard()">📋 Copy</button>
        `;
    }

    displayError(message) {
        const outputElement = document.getElementById('emailOutput');
        
        outputElement.innerHTML = `
            <div style="text-align: center; color: #ef4444; padding: 40px 20px;">
                <div style="font-size: 48px; margin-bottom: 16px;">❌</div>
                <h3>Generation Failed</h3>
                <p>${message}</p>
                <p style="font-size: 14px; color: #6b7280; margin-top: 16px;">
                    Please check your inputs and try again.
                </p>
            </div>
        `;
    }

    switchView(view) {
        const buttons = document.querySelectorAll('[data-view]');
        buttons.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.view === view);
        });

        this.currentView = view;

        if (this.lastGeneratedEmail) {
            this.displayEmail(this.lastGeneratedEmail);
        }
    }

    async copyToClipboard() {
        if (!this.lastGeneratedEmail) return;

        let textToCopy;
        if (this.currentView === 'preview' || this.currentView === 'text') {
            textToCopy = `Subject: ${this.lastGeneratedEmail.email.subject}\n\n${this.lastGeneratedEmail.email.body}`;
        } else {
            textToCopy = JSON.stringify(this.lastGeneratedEmail.analysis, null, 2);
        }

        try {
            await navigator.clipboard.writeText(textToCopy);
            this.showStatus('Email copied to clipboard!', 'success');
            
            // Visual feedback
            const copyBtn = document.getElementById('copyBtn');
            const originalText = copyBtn.innerHTML;
            copyBtn.innerHTML = '✅ Copied!';
            copyBtn.style.background = '#10b981';
            
            setTimeout(() => {
                copyBtn.innerHTML = originalText;
                copyBtn.style.background = '#4f46e5';
            }, 2000);
        } catch (error) {
            this.showStatus('Failed to copy to clipboard', 'error');
        }
    }

    validateForm() {
        const form = document.getElementById('emailForm');
        const generateBtn = document.getElementById('generateBtn');
        const requiredInputs = form.querySelectorAll('input[required], textarea[required]');
        
        let isValid = true;
        requiredInputs.forEach(input => {
            if (!input.value.trim()) {
                isValid = false;
            }
        });

        generateBtn.disabled = !isValid;
        generateBtn.style.opacity = isValid ? '1' : '0.6';
    }

    showStatus(message, type) {
        // You could implement a toast notification system here
        console.log(`${type.toUpperCase()}: ${message}`);
    }
}

// Initialize the email generator when the page loads
let emailGenerator;
document.addEventListener('DOMContentLoaded', () => {
    emailGenerator = new EmailGenerator();
});