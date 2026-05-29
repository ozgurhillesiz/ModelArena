document.addEventListener('DOMContentLoaded', function() {

    // Kart scroll animasyonu - flip kartları hariç
    const cards = document.querySelectorAll('.card:not(.flip-card-front):not(.flip-card-back)');
    if (cards.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry, index) => {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        entry.target.classList.add('visible');
                        entry.target.style.transform = 'translateY(0)';
                        entry.target.style.opacity = '1';
                    }, index * 80);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.05 });

        cards.forEach(card => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'opacity 0.5s ease, transform 0.5s ease, box-shadow 0.3s ease';
            observer.observe(card);
        });
    }

    // Hero stat kartları sayı sayma animasyonu
    const statNumbers = document.querySelectorAll('.stat-number');
    statNumbers.forEach(el => {
        const text = el.innerText;
        const num = parseFloat(text.replace(/[^0-9.]/g, ''));
        if (!isNaN(num) && num > 0 && num < 10000) {
            const prefix = text.match(/^[^0-9]*/)[0];
            const suffix = text.match(/[^0-9.]*$/)[0];
            let start = 0;
            const duration = 1500;
            const step = num / (duration / 16);
            const timer = setInterval(() => {
                start += step;
                if (start >= num) {
                    start = num;
                    clearInterval(timer);
                }
                el.innerText = prefix + (Number.isInteger(num) ? Math.floor(start) : start.toFixed(2)) + suffix;
            }, 16);
        }
    });

    // Navbar scroll efekti
    window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        if (navbar) {
            if (window.scrollY > 50) {
                navbar.style.backdropFilter = 'blur(20px)';
                navbar.style.background = 'rgba(10,10,26,0.95)';
                navbar.style.boxShadow = '0 4px 20px rgba(108,99,255,0.15)';
            } else {
                navbar.style.backdropFilter = '';
                navbar.style.background = '';
                navbar.style.boxShadow = '';
            }
        }
    });

    // Sayfa yükleme fade-in
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.3s ease';
    setTimeout(() => {
        document.body.style.opacity = '1';
    }, 50);

    // Flip kartların animasyonu sıfırla
    document.querySelectorAll('.flip-card-front, .flip-card-back').forEach(el => {
        el.style.opacity = '1';
        el.style.transform = '';
        el.style.transition = '';
    });

});

const style = document.createElement('style');
style.textContent = `
    @keyframes ripple {
        0% { transform: scale(1); opacity: 1; }
        100% { transform: scale(30); opacity: 0; }
    }
`;
document.head.appendChild(style);