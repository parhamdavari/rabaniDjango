document.addEventListener("DOMContentLoaded", function() {
    let lazyImages = [].slice.call(document.querySelectorAll("img.lazy"));

    if ("IntersectionObserver" in window) {
        let lazyImageObserver = new IntersectionObserver(function(entries, observer) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    let lazyImage = entry.target;
                    lazyImage.src = lazyImage.dataset.src;
                    lazyImage.classList.remove("lazy");
                    lazyImage.classList.add("lazy-loaded");
                    lazyImageObserver.unobserve(lazyImage);
                }
            });
        });

        lazyImages.forEach(function(lazyImage) {
            lazyImageObserver.observe(lazyImage);
        });
    } else {
        // Fallback for browsers that do not support IntersectionObserver
        let lazyLoad = function() {
            lazyImages.forEach(function(lazyImage) {
                if (lazyImage.getBoundingClientRect().top < window.innerHeight && lazyImage.getBoundingClientRect().bottom > 0) {
                    lazyImage.src = lazyImage.dataset.src;
                    lazyImage.classList.remove("lazy");
                    lazyImage.classList.add("lazy-loaded");
                }
            });

            if (lazyImages.length === 0) {
                document.removeEventListener("scroll", lazyLoad);
                window.removeEventListener("resize", lazyLoad);
                window.removeEventListener("orientationchange", lazyLoad);
            }
        };

        document.addEventListener("scroll", lazyLoad);
        window.addEventListener("resize", lazyLoad);
        window.addEventListener("orientationchange", lazyLoad);
    }
});

document.addEventListener("DOMContentLoaded", function() {
    let lazyBackgrounds = [].slice.call(document.querySelectorAll(".lazy-bg"));

    if ("IntersectionObserver" in window) {
        let lazyBackgroundObserver = new IntersectionObserver(function(entries, observer) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    let lazyBackground = entry.target;
                    lazyBackground.style.backgroundImage = `url(${lazyBackground.dataset.bg})`;
                    lazyBackground.classList.remove("lazy-bg");
                    lazyBackground.classList.add("lazy-bg-loaded");
                    lazyBackgroundObserver.unobserve(lazyBackground);
                }
            });
        });

        lazyBackgrounds.forEach(function(lazyBackground) {
            lazyBackgroundObserver.observe(lazyBackground);
        });
    } else {
        // Fallback for browsers that do not support IntersectionObserver
        let lazyLoadBackgrounds = function() {
            lazyBackgrounds.forEach(function(lazyBackground) {
                if (lazyBackground.getBoundingClientRect().top < window.innerHeight && lazyBackground.getBoundingClientRect().bottom > 0) {
                    lazyBackground.style.backgroundImage = `url(${lazyBackground.dataset.bg})`;
                    lazyBackground.classList.remove("lazy-bg");
                    lazyBackground.classList.add("lazy-bg-loaded");
                }
            });

            if (lazyBackgrounds.length === 0) {
                document.removeEventListener("scroll", lazyLoadBackgrounds);
                window.removeEventListener("resize", lazyLoadBackgrounds);
                window.removeEventListener("orientationchange", lazyLoadBackgrounds);
            }
        };

        document.addEventListener("scroll", lazyLoadBackgrounds);
        window.addEventListener("resize", lazyLoadBackgrounds);
        window.addEventListener("orientationchange", lazyLoadBackgrounds);
    }
});

