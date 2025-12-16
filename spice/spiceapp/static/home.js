document.addEventListener('DOMContentLoaded', function() {
    // Mobile Menu Toggle
    const mobileMenu = document.querySelector('.mobile-menu');
    const navLinks = document.querySelector('.nav-links');
  
    mobileMenu.addEventListener('click', function() {
        navLinks.style.display = navLinks.style.display === 'flex' ? 'none' : 'flex';
        this.classList.toggle('active');
    });
  
    // Hero Slider
    const slides = document.querySelectorAll('.slide');
    const dots = document.querySelectorAll('.dot');
    let currentSlide = 0;
  
    function showSlide(n) {
        slides.forEach(slide => slide.classList.remove('active'));
        dots.forEach(dot => dot.classList.remove('active'));
        
        slides[n].classList.add('active');
        dots[n].classList.add('active');
    }
  
    function nextSlide() {
        currentSlide = (currentSlide + 1) % slides.length;
        showSlide(currentSlide);
    }
  
    // Add click event to dots
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            currentSlide = index;
            showSlide(currentSlide);
        });
    });
  
    // Auto slide
    setInterval(nextSlide,5000);
  
    // Auction Timers
    // const timers = document.querySelectorAll('.auction-timer');
    
    // function updateTimers() {
    //     timers.forEach(timer => {
    //         const time = timer.textContent.split(':');
    //         let hours = parseInt(time[0]);
    //         let minutes = parseInt(time[1]);
    //         let seconds = parseInt(time[2]);
  
    //         seconds--;
  
    //         if (seconds < 0) {
    //             seconds = 59;
    //             minutes--;
    //             if (minutes < 0) {
    //                 minutes = 59;
    //                 hours--;
    //                 if (hours < 0) {
    //                     timer.textContent = "Auction Ended";
    //                     return;
    //                 }
    //             }
    //         }
  
    //         timer.textContent = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    //     });
    // }
  
    // setInterval(updateTimers, 1000);
  
    // Smooth Scroll for Navigation Links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
  
    // Scroll Animation for Features
    const features = document.querySelectorAll('.feature');
    
    function checkScroll() {
        features.forEach(feature => {
            const featureTop = feature.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (featureTop < windowHeight * 0.8) {
                feature.style.opacity = '1';
                feature.style.transform = 'translateY(0)';
            }
        });
    }
  
    window.addEventListener('scroll', checkScroll);
    checkScroll(); // Initial check
  
    // Add hover effect to auction cards
    const auctionCards = document.querySelectorAll('.auction-card');
    
    auctionCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
  });