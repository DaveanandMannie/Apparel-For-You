document.addEventListener("DOMContentLoaded", function () {

    // ------------------- Menu logic start ----------------------//
    const urlParams = new URLSearchParams(window.location.search);
    const queryValue = urlParams.get('query');
    const filterButtons = document.querySelectorAll('.filter-button');
    console.log(queryValue)
    filterButtons.forEach(button => {
        if (queryValue === button.value) {
            button.classList.add('selected')
        }
    });

    // ------------------- Menu logic end ----------------------//
    // ------------------- gallery logic start ------------------ //
    const gallery = document.querySelector(".gallery");
    const prevButton = document.querySelector(".prev-button");
    const nextButton = document.querySelector(".next-button");

    let currentIndex = 0;

    function highlightThumbnail(index) {
        const thumbnails = document.querySelectorAll('.gallery-thumbnail img');
        const colorButtons = document.querySelectorAll('.color-button');
        thumbnails.forEach((thumbnail,i) => {
            thumbnail.addEventListener('click', function (){
            currentIndex = i;
            showImage(currentIndex);
            updateInfoByIndex(currentIndex);
            });
            if (i === index) {
             thumbnail.classList.add('selected');
            } else {
             thumbnail.classList.remove('selected');
            }
        });
        colorButtons.forEach((button, i ) => {
            if (i === index) {
                button.classList.add('selected');
            } else {
                button.classList.remove('selected');
            }
        });

    }

    function showImage(index) {
        highlightThumbnail(index);
        const translateValue = -index * 100 + "%";
        const images = gallery.querySelectorAll("img");
        images.forEach((img) => {
            img.style.transform = `translateX(${translateValue})`;
        });
    }

    function updateGalleryIndex(colorIndex) {
        currentIndex = colorIndex;
        showImage(currentIndex);
    }

    function nextImage() {
        currentIndex = (currentIndex + 1) % gallery.children.length;
        showImage(currentIndex);
        updateInfoByIndex(currentIndex);
    }

    function prevImage() {
        currentIndex = (currentIndex - 1 + gallery.children.length) % gallery.children.length;
        showImage(currentIndex);
        updateInfoByIndex(currentIndex);
    }

    nextButton.addEventListener("click", nextImage);
    prevButton.addEventListener("click", prevImage);
    //------------- gallery logic end -------------------//
    // ------------- add to cart logic  start ------------------ //
    const colorButtons = document.querySelectorAll('.color-button');
    const sizeButtons = document.querySelectorAll('.size-button');
    const colorInput = document.getElementById('color-input');
    const sizeInput = document.getElementById('size-input');

    function handleColorButtonClick(button, index) {
        colorInput.value = button.dataset.color;
        colorButtons.forEach(btn => btn.classList.remove('selected'));
        button.classList.add('selected');
        updateGalleryIndex(index);
    }


    function updateInfoByIndex(index) {
        colorInput.value = colorButtons[index].dataset.color;
        colorButtons.forEach(btn => btn.classList.remove('selected'));
        colorButtons[index].classList.add('selected');
    }

    function handleSizeButtonClick(button) {
        sizeInput.value = button.dataset.size;
        sizeButtons.forEach(btn => btn.classList.remove('selected'));
        button.classList.add('selected');
    }

    colorButtons.forEach((button, index) => {
        button.addEventListener('click', function() {
            handleColorButtonClick(button, index);
        });
    });

    sizeButtons.forEach(button => {
        button.addEventListener('click', function () {
            handleSizeButtonClick(button);
        });
    });
    // initialize item page functions //
    showImage(currentIndex);
    updateInfoByIndex(currentIndex);
    // ---------------- add to cart logic end --------------------- //

    // ---------------- message card logic start ----------------- //
    const messageCards = document.querySelectorAll('.message-card');
        messageCards.forEach(messageCard => {
            setTimeout(() => {
                messageCard.classList.add('hidden');
            }, 2000);
            messageCard.addEventListener('click', function(){
                messageCard.classList.add('hidden')
            });
    });
});
// ---------------- Checkout pop out logic start ----------- //
document.addEventListener("DOMContentLoaded",function () {
    const checkoutButton = document.querySelector('#checkout-button');
    const card = document.querySelector('#post-checkout-card');

    checkoutButton.addEventListener("click", function (){
        setTimeout( () => {
            card.classList.add("show");
        },5);
        setTimeout( () => {
            card.classList.remove("show")
        },20000);
    });
});
    // ---------------- Checkout pop out logic end ----------- //