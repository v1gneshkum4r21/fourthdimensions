// DOM Elements
const tabs = document.querySelectorAll('.tab');
const playButton = document.getElementById('playButton');
const videoModal = document.getElementById('videoModal');
const closeButton = document.getElementById('closeButton');
const backgroundVideo = document.getElementById('backgroundVideo');
const scrollButton = document.getElementById('scrollButton');
const contentSection = document.getElementById('contentSection');

// Background Video Functionality
function initBackgroundVideo() {
    if (backgroundVideo) {
        // Ensure video plays automatically
        backgroundVideo.play().catch(function(error) {
            console.log('Video autoplay failed:', error);
            // Fallback: try to play on user interaction
            document.addEventListener('click', function() {
                backgroundVideo.play().catch(function(e) {
                    console.log('Video play failed:', e);
                });
            }, { once: true });
        });

        // Handle video loading
        backgroundVideo.addEventListener('loadeddata', function() {
            console.log('Background video loaded successfully');
        });

        // Handle video errors
        backgroundVideo.addEventListener('error', function() {
            console.log('Background video failed to load');
            // You could add a fallback image here
            const videoBackground = document.querySelector('.video-background');
            if (videoBackground) {
                videoBackground.style.background = 'linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)';
            }
        });

        // Ensure video loops properly
        backgroundVideo.addEventListener('ended', function() {
            backgroundVideo.currentTime = 0;
            backgroundVideo.play();
        });
    }
}

// Initialize background video when page loads
document.addEventListener('DOMContentLoaded', function() {
    initBackgroundVideo();
    initImageAnimations();
});

// Image Animation Functionality
function initImageAnimations() {
    const primaryImage = document.querySelector('.primary-image');
    const secondaryImage = document.querySelector('.secondary-image');
    
    if (primaryImage && secondaryImage) {
        // Add mouse movement parallax effect
        document.querySelector('.why-us-section').addEventListener('mousemove', function(e) {
            const xAxis = (window.innerWidth / 2 - e.pageX) / 25;
            const yAxis = (window.innerHeight / 2 - e.pageY) / 25;
            
            primaryImage.style.transform = `translateX(${xAxis}px) translateY(${yAxis}px)`;
            secondaryImage.style.transform = `translateX(${-xAxis}px) translateY(${-yAxis}px)`;
        });
        
        // Reset transform when mouse leaves the section
        document.querySelector('.why-us-section').addEventListener('mouseleave', function() {
            primaryImage.style.transform = 'translateX(0) translateY(0)';
            secondaryImage.style.transform = 'translateX(0) translateY(0)';
        });
        
        // Add scroll-based animation
        window.addEventListener('scroll', function() {
            const whyUsSection = document.querySelector('.why-us-section');
            const rect = whyUsSection.getBoundingClientRect();
            const isInView = (
                rect.top <= (window.innerHeight || document.documentElement.clientHeight) && 
                rect.bottom >= 0
            );
            
            if (isInView) {
                const scrollPosition = window.scrollY;
                const sectionTop = whyUsSection.offsetTop;
                const scrollOffset = scrollPosition - sectionTop + window.innerHeight/2;
                
                if (scrollOffset > 0) {
                    // Calculate parallax effect based on scroll position
                    const moveY = scrollOffset * 0.05;
                    
                    // Apply different movements to each image
                    if (primaryImage.style.animation !== 'none') {
                        primaryImage.style.animation = 'none';
                        secondaryImage.style.animation = 'none';
                    }
                    
                    primaryImage.style.transform = `translateY(${-moveY}px) rotate(${moveY * 0.05}deg)`;
                    secondaryImage.style.transform = `translateY(${moveY}px) rotate(${-moveY * 0.05}deg)`;
                }
            }
        });
        
        // Add image swap functionality on click
        let imagesSwapped = false;
        const whyUsImage = document.querySelector('.why-us-image');
        
        if (whyUsImage) {
            whyUsImage.addEventListener('click', function() {
                // Stop any existing animations
                primaryImage.style.animation = 'none';
                secondaryImage.style.animation = 'none';
                
                // Apply transition for smooth swap
                primaryImage.style.transition = 'all 1s cubic-bezier(0.34, 1.56, 0.64, 1)';
                secondaryImage.style.transition = 'all 1s cubic-bezier(0.34, 1.56, 0.64, 1)';
                
                if (!imagesSwapped) {
                    // Save original classes to restore later
                    primaryImage.dataset.originalClass = primaryImage.className;
                    secondaryImage.dataset.originalClass = secondaryImage.className;
                    
                    // Swap positions and sizes
                    primaryImage.style.transform = 'translateY(150px) translateX(-40px)';
                    primaryImage.style.zIndex = '1';
                    primaryImage.style.width = '55%';
                    primaryImage.style.height = '280px';
                    primaryImage.style.bottom = '0';
                    primaryImage.style.top = 'auto';
                    primaryImage.style.left = '0';
                    primaryImage.style.right = 'auto';
                    primaryImage.style.border = '10px solid white';
                    
                    secondaryImage.style.transform = 'translateY(-150px) translateX(40px)';
                    secondaryImage.style.zIndex = '2';
                    secondaryImage.style.width = '75%';
                    secondaryImage.style.height = '340px';
                    secondaryImage.style.top = '0';
                    secondaryImage.style.bottom = 'auto';
                    secondaryImage.style.right = '0';
                    secondaryImage.style.left = 'auto';
                    secondaryImage.style.border = 'none';
                } else {
                    // Return to original positions and sizes
                    primaryImage.style.transform = '';
                    primaryImage.style.zIndex = '2';
                    primaryImage.style.width = '75%';
                    primaryImage.style.height = '340px';
                    primaryImage.style.top = '0';
                    primaryImage.style.bottom = 'auto';
                    primaryImage.style.right = '0';
                    primaryImage.style.left = 'auto';
                    primaryImage.style.border = 'none';
                    
                    secondaryImage.style.transform = '';
                    secondaryImage.style.zIndex = '1';
                    secondaryImage.style.width = '55%';
                    secondaryImage.style.height = '280px';
                    secondaryImage.style.bottom = '0';
                    secondaryImage.style.top = 'auto';
                    secondaryImage.style.left = '0';
                    secondaryImage.style.right = 'auto';
                    secondaryImage.style.border = '10px solid white';
                }
                
                imagesSwapped = !imagesSwapped;
            });
        }
    }
}

// Scroll Down Button Functionality
if (scrollButton && contentSection) {
    scrollButton.addEventListener('click', function() {
        contentSection.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    });
}

// Tab Switching Functionality
tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        // Remove active class from all tabs
        tabs.forEach(t => t.classList.remove('active'));
        
        // Add active class to clicked tab
        tab.classList.add('active');
        
        // Get the category data
        const category = tab.getAttribute('data-category');
        
        // Add a subtle animation effect
        tab.style.transform = 'scale(0.95)';
        setTimeout(() => {
            tab.style.transform = '';
        }, 150);
        
        // Here you can add logic to show different content based on category
        console.log(`Switched to ${category} category`);
    });
});

// Video Modal Functionality
playButton.addEventListener('click', () => {
    videoModal.style.display = 'block';
    document.body.style.overflow = 'hidden'; // Prevent background scrolling
    
    // Add entrance animation
    const modalContent = videoModal.querySelector('.modal-content');
    modalContent.style.animation = 'modalSlideIn 0.3s ease-out';
});

// Close modal when clicking the close button
closeButton.addEventListener('click', () => {
    videoModal.style.display = 'none';
    document.body.style.overflow = 'auto'; // Restore scrolling
});

// Close modal when clicking outside the modal content
videoModal.addEventListener('click', (e) => {
    if (e.target === videoModal) {
        videoModal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
});

// Close modal with Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && videoModal.style.display === 'block') {
        videoModal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
});

// Add hover effects for better interactivity
tabs.forEach(tab => {
    tab.addEventListener('mouseenter', () => {
        if (!tab.classList.contains('active')) {
            tab.style.transform = 'translateY(-2px)';
        }
    });
    
    tab.addEventListener('mouseleave', () => {
        if (!tab.classList.contains('active')) {
            tab.style.transform = '';
        }
    });
});

// Add a subtle parallax effect to the hero section
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const hero = document.querySelector('.hero');
    const rate = scrolled * -0.5;
    
    if (hero) {
        hero.style.transform = `translateY(${rate}px)`;
    }
});

// Add loading animation
window.addEventListener('load', () => {
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.5s ease-in';
    
    setTimeout(() => {
        document.body.style.opacity = '1';
    }, 100);
});

// Enhanced smooth scrolling for anchor links
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                // Get header height for offset calculation
                const headerHeight = document.querySelector('.main-header') ? 
                    document.querySelector('.main-header').offsetHeight : 0;
                
                // Calculate position with offset for header
                const targetPosition = targetElement.getBoundingClientRect().top + 
                    window.pageYOffset - headerHeight - 20;
                
                // Smooth scroll to target
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
                
                // If this is a navigation link for content sections
                if (targetId === '#interior' || targetId === '#construction' || targetId === '#consultancy') {
                    // Deactivate all nav links
                    document.querySelectorAll('.nav-link').forEach(link => {
                        link.classList.remove('active');
                    });
                    
                    // Activate the corresponding nav link
                    document.querySelector(`a[href="${targetId}"]`).classList.add('active');
                    
                    // Hide all content sections
                    document.querySelectorAll('.content-section').forEach(section => {
                        section.style.display = 'none';
                    });
                    
                    // Show the target section
                    targetElement.style.display = 'block';
                }
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    // Background Video Functionality
    const backgroundVideo = document.getElementById('backgroundVideo');
    
    if (backgroundVideo) {
        // Ensure video plays automatically
        backgroundVideo.play().catch(function(error) {
            console.log('Video autoplay failed:', error);
            // Fallback: try to play on user interaction
            document.addEventListener('click', function() {
                backgroundVideo.play().catch(function(e) {
                    console.log('Video play failed:', e);
                });
            }, { once: true });
        });

        // Handle video loading
        backgroundVideo.addEventListener('loadeddata', function() {
            console.log('Background video loaded successfully');
        });

        // Handle video errors
        backgroundVideo.addEventListener('error', function() {
            console.log('Background video failed to load');
            // Fallback to gradient background
            const videoBackground = document.querySelector('.video-background');
            if (videoBackground) {
                videoBackground.style.background = 'linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)';
            }
        });
    }

    // Navigation Functionality
    const navLinks = document.querySelectorAll('.nav-link');
    const contentSections = document.querySelectorAll('.content-section');

    navLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            
            // Only handle content section navigation
            if (href === '#interior' || href === '#construction' || href === '#consultancy') {
                e.preventDefault();

                // Deactivate all links
                navLinks.forEach(l => l.classList.remove('active'));
                // Hide all sections
                contentSections.forEach(s => s.style.display = 'none');

                // Activate clicked link
                this.classList.add('active');

                // Show corresponding content section
                const targetSection = document.querySelector(href);
                if (targetSection) {
                    targetSection.style.display = 'block';
                    
                    // Smooth scroll to content section
                    const headerHeight = document.querySelector('.main-header').offsetHeight;
                    const offsetTop = targetSection.offsetTop - headerHeight - 20;
                    
                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });

    // Sub Navigation Functionality
    const subNavLinks = document.querySelectorAll('.sub-nav-link');
    
    subNavLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            
            // Remove active class from all sub-nav links
            subNavLinks.forEach(l => l.classList.remove('active'));
            
            // Add active class to clicked link
            this.classList.add('active');
            
            // Here you can add functionality for sub-navigation items
            console.log(`Clicked on ${this.textContent} sub-navigation item`);
        });
    });
    
    // Contact Form Functionality
    const contactForm = document.getElementById('contactForm');
    const refreshCaptchaButton = document.querySelector('.refresh-captcha');
    const captchaImage = document.querySelector('.captcha-image');
    
    // Generate random captcha
    function generateCaptcha() {
        const characters = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
        let captcha = '';
        for (let i = 0; i < 4; i++) {
            captcha += characters.charAt(Math.floor(Math.random() * characters.length));
        }
        return captcha;
    }
    
    // Refresh captcha on button click
    if (refreshCaptchaButton && captchaImage) {
        refreshCaptchaButton.addEventListener('click', function() {
            captchaImage.textContent = generateCaptcha();
        });
    }
    
    // Form submission
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Basic form validation
            const name = document.getElementById('name').value.trim();
            const email = document.getElementById('email').value.trim();
            const phone = document.getElementById('phone').value.trim();
            const requirements = document.getElementById('requirements').value.trim();
            const captchaInput = document.getElementById('captcha').value.trim();
            const captchaValue = captchaImage.textContent;
            
            // Check if all fields are filled
            if (!name || !email || !phone || !requirements || !captchaInput) {
                alert('Please fill in all required fields.');
                return;
            }
            
            // Check if captcha is correct
            if (captchaInput.toUpperCase() !== captchaValue) {
                alert('Captcha verification failed. Please try again.');
                captchaImage.textContent = generateCaptcha();
                document.getElementById('captcha').value = '';
                return;
            }
            
            // If all validation passes, you would typically send the form data to a server
            alert('Form submitted successfully!');
            contactForm.reset();
            captchaImage.textContent = generateCaptcha();
        });
    }
});

// Service Filters Functionality
document.addEventListener('DOMContentLoaded', function() {
    const serviceFilters = document.querySelectorAll('.service-filter');
    const serviceItems = document.querySelectorAll('.service-item');
    
    if (serviceFilters.length > 0) {
        serviceFilters.forEach(filter => {
            filter.addEventListener('click', function() {
                // Remove active class from all filters
                serviceFilters.forEach(f => f.classList.remove('active'));
                
                // Add active class to clicked filter
                this.classList.add('active');
                
                // Get the filter value
                const filterValue = this.getAttribute('data-filter');
                
                // Hide all service items with fade-out effect
                serviceItems.forEach(item => {
                    item.classList.remove('active');
                    item.style.opacity = '0';
                    item.style.transform = 'translateY(20px)';
                });
                
                // Show the filtered service item with delay for animation
                setTimeout(() => {
                    serviceItems.forEach(item => {
                        if (item.getAttribute('data-service') === filterValue) {
                            item.classList.add('active');
                            // Trigger reflow for animation
                            void item.offsetWidth;
                            item.style.opacity = '1';
                            item.style.transform = 'translateY(0)';
                        }
                    });
                }, 300);
            });
        });
    }
});

// Interior Category and Thumbnail Gallery
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM loaded - checking for category items and galleries");
    
    // Category switching functionality
    const categoryItems = document.querySelectorAll('.category-item');
    const categoryGalleries = document.querySelectorAll('.category-gallery');
    
    console.log("Found category items:", categoryItems.length);
    console.log("Found category galleries:", categoryGalleries.length);
    
    if (categoryItems.length > 0) {
        categoryItems.forEach(item => {
            item.addEventListener('click', function() {
                // Get the category value
                const categoryValue = this.getAttribute('data-category');
                console.log("Category clicked:", categoryValue);
                
                // Update active state for category items
                categoryItems.forEach(cat => cat.classList.remove('active'));
                this.classList.add('active');
                
                // Hide all galleries with fade-out effect
                categoryGalleries.forEach(gallery => {
                    gallery.style.opacity = '0';
                    setTimeout(() => {
                        gallery.classList.remove('active');
                    }, 300);
                });
                
                // Show the selected gallery with fade-in effect
                const targetGallery = document.querySelector(`.category-gallery[data-gallery="${categoryValue}"]`);
                console.log("Target gallery found:", targetGallery ? true : false);
                
                if (targetGallery) {
                    setTimeout(() => {
                        targetGallery.classList.add('active');
                        setTimeout(() => {
                            targetGallery.style.opacity = '1';
                        }, 50);
                    }, 350);
                }
            });
        });
    }
    
    // Thumbnail gallery functionality for all category galleries
    const allThumbnails = document.querySelectorAll('.thumbnail');
    console.log("Found thumbnails:", allThumbnails.length);
    
    if (allThumbnails.length > 0) {
        allThumbnails.forEach(thumbnail => {
            thumbnail.addEventListener('click', function() {
                console.log("Thumbnail clicked");
                
                // Find the parent gallery
                const parentGallery = this.closest('.category-gallery');
                if (!parentGallery) {
                    console.log("No parent gallery found");
                    return;
                }
                
                // Get the main image in this gallery
                const mainImage = parentGallery.querySelector('.showcase-main img');
                if (!mainImage) {
                    console.log("No main image found");
                    return;
                }
                
                console.log("Found main image:", mainImage.src);
                
                // Get the clicked thumbnail's image source
                const newImageSrc = this.querySelector('img').getAttribute('src');
                const currentMainSrc = mainImage.getAttribute('src');
                
                console.log("Swapping images:", currentMainSrc, "with", newImageSrc);
                
                // Add fade-out effect to main image
                mainImage.style.opacity = '0';
                
                // After fade out, swap the images and fade in
                setTimeout(() => {
                    // Swap the images
                    mainImage.setAttribute('src', newImageSrc);
                    this.querySelector('img').setAttribute('src', currentMainSrc);
                    
                    // Fade in the new main image
                    mainImage.style.opacity = '1';
                }, 300);
                
                // Add active class to clicked thumbnail within this gallery
                const galleryThumbnails = parentGallery.querySelectorAll('.thumbnail');
                galleryThumbnails.forEach(t => t.classList.remove('active-thumb'));
                this.classList.add('active-thumb');
            });
        });
    }
});

// Add direct click handlers to category items
document.addEventListener('DOMContentLoaded', function() {
    // Direct click handlers for category items
    document.querySelectorAll('.category-item').forEach(item => {
        item.onclick = function() {
            const categoryValue = this.getAttribute('data-category');
            console.log("Direct click on category:", categoryValue);
            
            // Update active states
            document.querySelectorAll('.category-item').forEach(cat => cat.classList.remove('active'));
            this.classList.add('active');
            
            // Hide all galleries
            document.querySelectorAll('.category-gallery').forEach(gallery => {
                gallery.style.opacity = '0';
                setTimeout(() => {
                    gallery.classList.remove('active');
                }, 300);
            });
            
            // Show selected gallery
            const targetGallery = document.querySelector(`.category-gallery[data-gallery="${categoryValue}"]`);
            if (targetGallery) {
                setTimeout(() => {
                    targetGallery.classList.add('active');
                    setTimeout(() => {
                        targetGallery.style.opacity = '1';
                    }, 50);
                }, 350);
            }
        };
    });
    
    // Direct click handlers for thumbnails
    document.querySelectorAll('.thumbnail').forEach(thumb => {
        thumb.onclick = function() {
            const parentGallery = this.closest('.category-gallery');
            if (!parentGallery) return;
            
            const mainImage = parentGallery.querySelector('.showcase-main img');
            if (!mainImage) return;
            
            const thumbImg = this.querySelector('img');
            const newImageSrc = thumbImg.getAttribute('src');
            const currentMainSrc = mainImage.getAttribute('src');
            
            console.log("Direct thumbnail click - swapping images");
            
            // Fade out
            mainImage.style.opacity = '0';
            
            // Swap images
            setTimeout(() => {
                mainImage.setAttribute('src', newImageSrc);
                thumbImg.setAttribute('src', currentMainSrc);
                
                // Fade in
                mainImage.style.opacity = '1';
            }, 300);
            
            // Update active state
            parentGallery.querySelectorAll('.thumbnail').forEach(t => t.classList.remove('active-thumb'));
            this.classList.add('active-thumb');
        };
    });
});

// Features Slider Functionality
document.addEventListener('DOMContentLoaded', function() {
    const featuresTrack = document.querySelector('.features-slider .features-track');
    const featuresPrevButton = document.querySelector('.features-slider .prev-feature');
    const featuresNextButton = document.querySelector('.features-slider .next-feature');
    const featuresDots = document.querySelectorAll('.features-slider .dot');
    
    if (featuresTrack && featuresPrevButton && featuresNextButton && featuresDots.length > 0) {
        let currentFeatureSlide = 0;
        const totalFeatureSlides = featuresDots.length;
        
        // Function to update features slider position
        function updateFeaturesSlider() {
            featuresTrack.style.transform = `translateX(-${currentFeatureSlide * 25}%)`;
            
            // Update active dot
            featuresDots.forEach((dot, index) => {
                dot.classList.toggle('active', index === currentFeatureSlide);
            });
        }
        
        // Previous slide button
        featuresPrevButton.addEventListener('click', function() {
            currentFeatureSlide = (currentFeatureSlide - 1 + totalFeatureSlides) % totalFeatureSlides;
            updateFeaturesSlider();
        });
        
        // Next slide button
        featuresNextButton.addEventListener('click', function() {
            currentFeatureSlide = (currentFeatureSlide + 1) % totalFeatureSlides;
            updateFeaturesSlider();
        });
        
        // Dot navigation
        featuresDots.forEach((dot, index) => {
            dot.addEventListener('click', function() {
                currentFeatureSlide = index;
                updateFeaturesSlider();
            });
        });
        
        // Auto-slide functionality
        let autoFeaturesInterval = setInterval(function() {
            currentFeatureSlide = (currentFeatureSlide + 1) % totalFeatureSlides;
            updateFeaturesSlider();
        }, 5000); // Change slide every 5 seconds
        
        // Pause auto-slide on hover
        featuresTrack.addEventListener('mouseenter', function() {
            clearInterval(autoFeaturesInterval);
        });
        
        // Resume auto-slide on mouse leave
        featuresTrack.addEventListener('mouseleave', function() {
            autoFeaturesInterval = setInterval(function() {
                currentFeatureSlide = (currentFeatureSlide + 1) % totalFeatureSlides;
                updateFeaturesSlider();
            }, 5000);
        });
        
        // Touch swipe functionality
        let touchFeaturesStartX = 0;
        let touchFeaturesEndX = 0;
        
        featuresTrack.addEventListener('touchstart', function(e) {
            touchFeaturesStartX = e.changedTouches[0].screenX;
        }, { passive: true });
        
        featuresTrack.addEventListener('touchend', function(e) {
            touchFeaturesEndX = e.changedTouches[0].screenX;
            handleFeaturesSwipe();
        }, { passive: true });
        
        function handleFeaturesSwipe() {
            const swipeThreshold = 50; // Minimum distance required for a swipe
            
            if (touchFeaturesEndX < touchFeaturesStartX - swipeThreshold) {
                // Swipe left - next slide
                currentFeatureSlide = (currentFeatureSlide + 1) % totalFeatureSlides;
                updateFeaturesSlider();
            } else if (touchFeaturesEndX > touchFeaturesStartX + swipeThreshold) {
                // Swipe right - previous slide
                currentFeatureSlide = (currentFeatureSlide - 1 + totalFeatureSlides) % totalFeatureSlides;
                updateFeaturesSlider();
            }
        }
    }
});

// Showcase Slider Functionality
document.addEventListener('DOMContentLoaded', function() {
    const showcaseTrack = document.querySelector('.showcase-slider .showcase-track');
    const showcasePrevButton = document.querySelector('.showcase-slider .prev-slide');
    const showcaseNextButton = document.querySelector('.showcase-slider .next-slide');
    const showcaseDots = document.querySelectorAll('.showcase-slider .dot');
    
    if (showcaseTrack && showcasePrevButton && showcaseNextButton && showcaseDots.length > 0) {
        let currentShowcaseSlide = 0;
        const totalShowcaseSlides = showcaseDots.length;
        
        // Function to update showcase slider position
        function updateShowcaseSlider() {
            showcaseTrack.style.transform = `translateX(-${currentShowcaseSlide * 33.333}%)`;
            
            // Update active dot
            showcaseDots.forEach((dot, index) => {
                dot.classList.toggle('active', index === currentShowcaseSlide);
            });
        }
        
        // Previous slide button
        showcasePrevButton.addEventListener('click', function() {
            currentShowcaseSlide = (currentShowcaseSlide - 1 + totalShowcaseSlides) % totalShowcaseSlides;
            updateShowcaseSlider();
        });
        
        // Next slide button
        showcaseNextButton.addEventListener('click', function() {
            currentShowcaseSlide = (currentShowcaseSlide + 1) % totalShowcaseSlides;
            updateShowcaseSlider();
        });
        
        // Dot navigation
        showcaseDots.forEach((dot, index) => {
            dot.addEventListener('click', function() {
                currentShowcaseSlide = index;
                updateShowcaseSlider();
            });
        });
        
        // Auto-slide functionality
        let autoShowcaseInterval = setInterval(function() {
            currentShowcaseSlide = (currentShowcaseSlide + 1) % totalShowcaseSlides;
            updateShowcaseSlider();
        }, 6000); // Change slide every 6 seconds
        
        // Pause auto-slide on hover
        showcaseTrack.addEventListener('mouseenter', function() {
            clearInterval(autoShowcaseInterval);
        });
        
        // Resume auto-slide on mouse leave
        showcaseTrack.addEventListener('mouseleave', function() {
            autoShowcaseInterval = setInterval(function() {
                currentShowcaseSlide = (currentShowcaseSlide + 1) % totalShowcaseSlides;
                updateShowcaseSlider();
            }, 6000);
        });
        
        // Touch swipe functionality
        let touchShowcaseStartX = 0;
        let touchShowcaseEndX = 0;
        
        showcaseTrack.addEventListener('touchstart', function(e) {
            touchShowcaseStartX = e.changedTouches[0].screenX;
        }, { passive: true });
        
        showcaseTrack.addEventListener('touchend', function(e) {
            touchShowcaseEndX = e.changedTouches[0].screenX;
            handleShowcaseSwipe();
        }, { passive: true });
        
        function handleShowcaseSwipe() {
            const swipeThreshold = 50; // Minimum distance required for a swipe
            
            if (touchShowcaseEndX < touchShowcaseStartX - swipeThreshold) {
                // Swipe left - next slide
                currentShowcaseSlide = (currentShowcaseSlide + 1) % totalShowcaseSlides;
                updateShowcaseSlider();
            } else if (touchShowcaseEndX > touchShowcaseStartX + swipeThreshold) {
                // Swipe right - previous slide
                currentShowcaseSlide = (currentShowcaseSlide - 1 + totalShowcaseSlides) % totalShowcaseSlides;
                updateShowcaseSlider();
            }
        }
    }
}); 