document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('listingForm');
    const imageInput = document.getElementById('imageInput');
    const imagePreview = document.getElementById('imagePreview');
    const imageUpload = document.getElementById('imageUpload');

    // Handle drag and drop
    imageUpload.addEventListener('dragover', (e) => {
        e.preventDefault();
        imageUpload.classList.add('dragover');
    });

    imageUpload.addEventListener('dragleave', () => {
        imageUpload.classList.remove('dragover');
    });

    imageUpload.addEventListener('drop', (e) => {
        e.preventDefault();
        imageUpload.classList.remove('dragover');
        const files = e.dataTransfer.files;
        handleFiles(files);
    });

    // Handle file input change
    imageInput.addEventListener('change', (e) => {
        handleFiles(e.target.files);
    });

    function handleFiles(files) {
        imagePreview.innerHTML = '';
        Array.from(files).forEach(file => {
            if (file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    const img = document.createElement('img');
                    img.src = e.target.result;
                    img.classList.add('preview-image');
                    imagePreview.appendChild(img);
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // Form submission
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        
        // Validate form
        const startingPrice = parseFloat(document.getElementById('startingPrice').value);
        const reservePrice = parseFloat(document.getElementById('reservePrice').value);

        if (reservePrice && reservePrice < startingPrice) {
            alert('Reserve price cannot be less than starting price');
            return;
        }

        // Simulate form submission
        const formData = new FormData(form);
        const submitButton = form.querySelector('button[type="submit"]');
        submitButton.disabled = true;
        submitButton.textContent = 'Listing...';

        // Simulate API call
        setTimeout(() => {
            alert('Product listed successfully!');
            form.reset();
            imagePreview.innerHTML = '';
            submitButton.disabled = false;
            submitButton.textContent = 'List Product';
        }, 2000);
    });

    // Real-time validation
    const startingPriceInput = document.getElementById('startingPrice');
    const reservePriceInput = document.getElementById('reservePrice');

    reservePriceInput.addEventListener('input', () => {
        const startingPrice = parseFloat(startingPriceInput.value);
        const reservePrice = parseFloat(reservePriceInput.value);

        if (reservePrice && reservePrice < startingPrice) {
            reservePriceInput.setCustomValidity('Reserve price must be greater than or equal to starting price');
        } else {
            reservePriceInput.setCustomValidity('');
        }
    });
});
