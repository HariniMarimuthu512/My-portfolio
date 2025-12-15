/**
 * Main JavaScript for Portfolio Website
 * Handles dynamic content loading, form submission, and interactions
 * Updated: 2024 - Custom category ordering
 */

// Navigation functionality
const navbar = document.getElementById('navbar');
const hamburger = document.getElementById('hamburger');
const navMenu = document.getElementById('navMenu');
const navLinks = document.querySelectorAll('.nav-link');

// Mobile menu toggle
if (hamburger) {
    hamburger.addEventListener('click', () => {
        navMenu.classList.toggle('active');
    });
}

// Close mobile menu when clicking on a link
navLinks.forEach(link => {
    link.addEventListener('click', () => {
        navMenu.classList.remove('active');
    });
});

// Navbar scroll effect
window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }

    // Update active nav link based on scroll position
    updateActiveNavLink();
});

// Update active navigation link based on scroll position
function updateActiveNavLink() {
    const sections = document.querySelectorAll('section[id]');
    const scrollY = window.pageYOffset;

    sections.forEach(section => {
        const sectionHeight = section.offsetHeight;
        const sectionTop = section.offsetTop - 100;
        const sectionId = section.getAttribute('id');
        const navLink = document.querySelector(`.nav-link[href="#${sectionId}"]`);

        if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
            navLinks.forEach(link => link.classList.remove('active'));
            if (navLink) {
                navLink.classList.add('active');
            }
        }
    });
}

// Load skills from API
async function loadSkills() {
    try {
        const response = await fetch('/api/skills');
        const skills = await response.json();
        const skillsGrid = document.getElementById('skillsGrid');

        if (!skillsGrid) return;

        // Group skills by category
        const skillsByCategory = {};
        skills.forEach(skill => {
            const category = skill.category || 'Other';
            if (!skillsByCategory[category]) {
                skillsByCategory[category] = [];
            }
            skillsByCategory[category].push(skill);
        });

        // Define custom category order - DO NOT CHANGE ORDER
        const categoryOrder = [
            'Programming Languages',
            'Frameworks',
            'Database Systems',
            'Domain Expertise',
            'Technical Libraries',
            'Web Development',
            'Tools & Platforms',
            'Development Environment'
        ];
        
        // Force execution - ensure order is applied
        console.log('Applying custom category order:', categoryOrder);

        // Sort categories based on custom order, then add any remaining categories
        const sortedCategories = [];
        categoryOrder.forEach(cat => {
            if (skillsByCategory[cat] && skillsByCategory[cat].length > 0) {
                sortedCategories.push(cat);
            }
        });
        
        const remainingCategories = Object.keys(skillsByCategory)
            .filter(cat => !categoryOrder.includes(cat))
            .sort();
        const allCategories = [...sortedCategories, ...remainingCategories];

        // Debug: Verify category order
        console.log('Available categories:', Object.keys(skillsByCategory));
        console.log('Ordered categories:', allCategories);

        // Generate HTML with category sections
        let html = '';
        allCategories.forEach(category => {
            html += `<div class="skill-category-section">
                <h3 class="skill-category-title">${escapeHtml(category)}</h3>
                <div class="skill-category-grid">
            `;
            
            skillsByCategory[category].forEach(skill => {
                const levelMap = {
                    'basic': 30,
                    'beginner': 30,
                    'intermediate': 60,
                    'advanced': 85,
                    'expert': 100
                };
                const progress = levelMap[skill.level] || 50;
                
                // Capitalize first letter of level
                const levelDisplay = skill.level.charAt(0).toUpperCase() + skill.level.slice(1);
                
                // Get level color
                const levelColors = {
                    'basic': '#94a3b8',
                    'beginner': '#94a3b8',
                    'intermediate': '#3b82f6',
                    'advanced': '#10b981',
                    'expert': '#8b5cf6'
                };
                const levelColor = levelColors[skill.level] || '#6b7280';

                html += `
                    <div class="skill-card">
                        <div class="skill-header">
                            <div class="skill-name">${escapeHtml(skill.name)}</div>
                            <div class="skill-level-badge" style="background: ${levelColor}20; color: ${levelColor};">
                                ${escapeHtml(levelDisplay)}
                            </div>
                        </div>
                        <div class="skill-bar-container">
                            <div class="skill-bar">
                                <div class="skill-progress" style="width: ${progress}%; background: ${levelColor};"></div>
                            </div>
                            <span class="skill-percentage">${progress}%</span>
                        </div>
                    </div>
                `;
            });
            
            html += `</div></div>`;
        });

        skillsGrid.innerHTML = html;

        // Animate skill bars on scroll
        animateSkillBars();
    } catch (error) {
        console.error('Error loading skills:', error);
    }
}

// Load projects from API
async function loadProjects() {
    try {
        const response = await fetch('/api/projects');
        const projects = await response.json();
        const projectsGrid = document.getElementById('projectsGrid');

        if (!projectsGrid) return;

        projectsGrid.innerHTML = projects.map((project, index) => {
            const technologies = project.technologies.map(tech => 
                `<span class="tech-tag">${escapeHtml(tech)}</span>`
            ).join('');

            const links = [];
            if (project.github_url) {
                links.push(`<a href="${escapeHtml(project.github_url)}" target="_blank" rel="noopener noreferrer" class="project-link">GitHub →</a>`);
            }
            if (project.live_url) {
                links.push(`<a href="${escapeHtml(project.live_url)}" target="_blank" rel="noopener noreferrer" class="project-link">Live Demo →</a>`);
            }

            // Add class for last odd item to center it
            const isLastOdd = projects.length % 2 !== 0 && index === projects.length - 1;
            const cardClass = isLastOdd ? 'project-card center-odd' : 'project-card';

            return `
                <div class="${cardClass}">
                    <div class="project-image">
                        <span>🐍</span>
                    </div>
                    <div class="project-content">
                        <h3 class="project-title">${escapeHtml(project.title)}</h3>
                        <p class="project-description">${escapeHtml(project.description)}</p>
                        <div class="project-technologies">
                            ${technologies}
                        </div>
                        <div class="project-links">
                            ${links.join('')}
                        </div>
                    </div>
                </div>
            `;
        }).join('');
    } catch (error) {
        console.error('Error loading projects:', error);
    }
}

// Animate skill bars when they come into view
function animateSkillBars() {
    const skillBars = document.querySelectorAll('.skill-progress');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const progressBar = entry.target;
                const width = progressBar.style.width;
                progressBar.style.width = '0%';
                setTimeout(() => {
                    progressBar.style.width = width;
                }, 100);
                observer.unobserve(progressBar);
            }
        });
    }, { threshold: 0.5 });

    skillBars.forEach(bar => observer.observe(bar));
}

// Animate statistics
function animateStats() {
    const stats = document.querySelectorAll('.stat-number');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const stat = entry.target;
                const target = parseInt(stat.getAttribute('data-target'));
                animateValue(stat, 0, target, 2000);
                observer.unobserve(stat);
            }
        });
    }, { threshold: 0.5 });

    stats.forEach(stat => observer.observe(stat));
}

// Animate number value
function animateValue(element, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const current = Math.floor(progress * (end - start) + start);
        element.textContent = current;
        if (progress < 1) {
            window.requestAnimationFrame(step);
        } else {
            element.textContent = end;
        }
    };
    window.requestAnimationFrame(step);
}

// Contact form submission
const contactForm = document.getElementById('contactForm');
if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formMessage = document.getElementById('formMessage');
        const submitButton = contactForm.querySelector('button[type="submit"]');
        const originalButtonText = submitButton.textContent;

        // Get form data and trim whitespace
        const name = document.getElementById('name').value.trim();
        const email = document.getElementById('email').value.trim();
        const subject = document.getElementById('subject').value.trim();
        const message = document.getElementById('message').value.trim();

        // Validate required fields
        if (!name || !email || !message) {
            formMessage.className = 'form-message error';
            formMessage.textContent = 'Please fill in all required fields.';
            return;
        }

        // Build form data - only include subject if it's not empty
        const formData = {
            name: name,
            email: email,
            message: message
        };
        
        // Only add subject if it's not empty
        if (subject) {
            formData.subject = subject;
        }

        // Disable submit button
        submitButton.disabled = true;
        submitButton.textContent = 'Sending...';

        try {
            console.log('Sending form data:', formData);
            
            const response = await fetch('/api/contact', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            console.log('Response status:', response.status);
            console.log('Response ok:', response.ok);
            
            // Check response status first
            const contentType = response.headers.get('content-type') || '';
            console.log('Content-Type:', contentType);
            
            const text = await response.text();
            console.log('Response text (first 500 chars):', text.substring(0, 500));
            
            let result = null;
            
            // Try to parse as JSON
            if (contentType.includes('application/json') || text.trim().startsWith('{') || text.trim().startsWith('[')) {
                try {
                    result = JSON.parse(text);
                    console.log('Parsed JSON result:', result);
                } catch (parseError) {
                    console.error('Failed to parse JSON response:', parseError);
                    console.error('Full response text:', text);
                }
            } else {
                console.error('Non-JSON response received:');
                console.error('Content-Type:', contentType);
                console.error('Full response text:', text);
            }

            // Check if response is ok
            if (!response.ok) {
                // Handle validation errors (422) or server errors (500)
                let errorMessage = `Server error (${response.status})`;
                
                if (result && result.detail) {
                    if (Array.isArray(result.detail)) {
                        // Validation errors from FastAPI
                        errorMessage = result.detail.map(e => {
                            if (typeof e === 'object' && e.msg) {
                                return `${e.loc ? e.loc.join('.') + ': ' : ''}${e.msg}`;
                            }
                            return String(e);
                        }).join(', ');
                    } else {
                        errorMessage = String(result.detail);
                    }
                } else if (!result) {
                    // No valid JSON response
                    errorMessage = `Server error (${response.status}). Response: ${text.substring(0, 200)}`;
                }
                
                console.error('Server error details:', { status: response.status, result, text });
                throw new Error(errorMessage);
            }

            // Success response - check if we have valid result
            if (!result) {
                console.error('No valid result parsed from response');
                throw new Error('Invalid response from server. Please check console for details.');
            }

            if (result.success) {
                formMessage.className = 'form-message success';
                formMessage.textContent = result.message;
                contactForm.reset();
            } else {
                console.error('Response indicates failure:', result);
                throw new Error(result.message || 'Failed to send message');
            }
        } catch (error) {
            formMessage.className = 'form-message error';
            formMessage.textContent = error.message || 'Sorry, there was an error sending your message. Please try again later.';
            console.error('Error submitting form:', error);
            console.error('Error stack:', error.stack);
        } finally {
            submitButton.disabled = false;
            submitButton.textContent = originalButtonText;
        }
    });
}

// Utility function to escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const offsetTop = target.offsetTop - 80;
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    });
});

// Copy code functionality
function setupCodeCopy() {
    const copyButton = document.getElementById('copyCodeBtn');
    const codeContent = document.getElementById('codeContent');

    if (!copyButton || !codeContent) return;

    copyButton.addEventListener('click', async () => {
        try {
            const text = codeContent.textContent;
            await navigator.clipboard.writeText(text);
            
            // Visual feedback
            const copyText = copyButton.querySelector('.copy-text');
            const copyIcon = copyButton.querySelector('.copy-icon');
            const originalText = copyText.textContent;
            
            copyButton.classList.add('copied');
            copyIcon.style.display = 'none';
            copyText.textContent = '✓ Copied!';
            
            // Reset after 2 seconds
            setTimeout(() => {
                copyButton.classList.remove('copied');
                copyIcon.style.display = 'inline';
                copyText.textContent = originalText;
            }, 2000);
        } catch (err) {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = codeContent.textContent;
            textArea.style.position = 'fixed';
            textArea.style.opacity = '0';
            document.body.appendChild(textArea);
            textArea.select();
            
            try {
                document.execCommand('copy');
                copyButton.classList.add('copied');
                setTimeout(() => {
                    copyButton.classList.remove('copied');
                }, 2000);
            } catch (fallbackErr) {
                console.error('Failed to copy:', fallbackErr);
            }
            
            document.body.removeChild(textArea);
        }
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    loadSkills();
    loadProjects();
    setupCodeCopy();
});

