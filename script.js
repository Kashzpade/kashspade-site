/* =====================================================
   VELOURA CHOCOLATE
   INTERACTION SYSTEM
===================================================== */


/* =====================================================
   CONFIG
===================================================== */

// GANTI DENGAN EMAIL ASLI TUJUAN CONTACT FORM
const CONTACT_EMAIL = "hello@veloura.example";


/* =====================================================
   DOM
===================================================== */

const body = document.body;

const navbar =
    document.getElementById("navbar");

const scrollProgress =
    document.getElementById("scrollProgress");

const loader =
    document.getElementById("loader");

const menuButton =
    document.getElementById("menuButton");

const mobileMenu =
    document.getElementById("mobileMenu");

const navLinks =
    document.querySelectorAll(".nav-link");

const sections =
    document.querySelectorAll("section[id]");


/* =====================================================
   PRELOADER
===================================================== */

window.addEventListener("load", () => {

    setTimeout(() => {

        loader.classList.add("hide");

    }, 700);

});


/* =====================================================
   NAVBAR
===================================================== */

function updateNavbar() {

    if (window.scrollY > 40) {

        navbar.classList.add("scrolled");

    } else {

        navbar.classList.remove("scrolled");

    }

}


window.addEventListener(
    "scroll",
    updateNavbar,
    { passive: true }
);

updateNavbar();


/* =====================================================
   SCROLL PROGRESS
===================================================== */

function updateScrollProgress() {

    const scrollTop =
        window.scrollY;

    const documentHeight =
        document.documentElement.scrollHeight
        - window.innerHeight;

    if (documentHeight <= 0) return;

    const progress =
        (scrollTop / documentHeight) * 100;

    scrollProgress.style.height =
        `${progress}%`;

}


window.addEventListener(
    "scroll",
    updateScrollProgress,
    { passive: true }
);

updateScrollProgress();


/* =====================================================
   MOBILE MENU
===================================================== */

menuButton.addEventListener(
    "click",
    () => {

        mobileMenu.classList.toggle("open");

        body.classList.toggle(
            "no-scroll"
        );

    }
);


document
    .querySelectorAll(".mobile-menu a")
    .forEach(link => {

        link.addEventListener(
            "click",
            () => {

                mobileMenu.classList.remove(
                    "open"
                );

                body.classList.remove(
                    "no-scroll"
                );

            }
        );

    });


/* =====================================================
   SMOOTH ANCHOR
===================================================== */

document
    .querySelectorAll('a[href^="#"]')
    .forEach(link => {

        link.addEventListener(
            "click",
            event => {

                const targetId =
                    link.getAttribute("href");

                if (
                    !targetId ||
                    targetId === "#"
                ) {
                    return;
                }

                const target =
                    document.querySelector(
                        targetId
                    );

                if (!target) return;

                event.preventDefault();

                target.scrollIntoView({
                    behavior: "smooth"
                });

            }
        );

    });


/* =====================================================
   ACTIVE NAVIGATION
===================================================== */

const sectionObserver =
    new IntersectionObserver(
        entries => {

            entries.forEach(entry => {

                if (!entry.isIntersecting)
                    return;

                const id =
                    entry.target.id;

                navLinks.forEach(link => {

                    link.classList.toggle(
                        "active",
                        link.getAttribute(
                            "href"
                        ) === `#${id}`
                    );

                });

            });

        },
        {
            rootMargin:
                "-35% 0px -55% 0px"
        }
    );


sections.forEach(section => {

    sectionObserver.observe(section);

});


/* =====================================================
   REVEAL ON SCROLL
===================================================== */

const revealElements =
    document.querySelectorAll(".reveal");


const revealObserver =
    new IntersectionObserver(
        entries => {

            entries.forEach(entry => {

                if (!entry.isIntersecting)
                    return;

                entry.target.classList.add(
                    "visible"
                );

                revealObserver.unobserve(
                    entry.target
                );

            });

        },
        {
            threshold: .12
        }
    );


revealElements.forEach(element => {

    revealObserver.observe(element);

});


/* =====================================================
   HERO PARALLAX
===================================================== */

const hero =
    document.querySelector(".hero");

const heroProduct =
    document.querySelector(".hero-product");


if (
    hero &&
    heroProduct &&
    window.matchMedia(
        "(pointer:fine)"
    ).matches
) {

    hero.addEventListener(
        "mousemove",
        event => {

            const rect =
                hero.getBoundingClientRect();

            const x =
                (event.clientX - rect.left)
                / rect.width
                - .5;

            const y =
                (event.clientY - rect.top)
                / rect.height
                - .5;

            heroProduct.style.transform =
                `translateY(-50%)
                 translate(${x * 15}px, ${y * 15}px)`;

        }
    );


    hero.addEventListener(
        "mouseleave",
        () => {

            heroProduct.style.transform =
                "translateY(-50%)";

        }
    );

}


/* =====================================================
   CUSTOM CURSOR
===================================================== */

const cursor =
    document.querySelector(".cursor");

const cursorFollower =
    document.querySelector(
        ".cursor-follower"
    );


if (
    cursor &&
    cursorFollower &&
    window.matchMedia(
        "(pointer:fine)"
    ).matches
) {

    let mouseX = 0;
    let mouseY = 0;

    let followerX = 0;
    let followerY = 0;


    window.addEventListener(
        "mousemove",
        event => {

            mouseX = event.clientX;
            mouseY = event.clientY;

            cursor.style.left =
                `${mouseX}px`;

            cursor.style.top =
                `${mouseY}px`;

        }
    );


    function animateCursor() {

        followerX +=
            (mouseX - followerX) * .12;

        followerY +=
            (mouseY - followerY) * .12;

        cursorFollower.style.left =
            `${followerX}px`;

        cursorFollower.style.top =
            `${followerY}px`;

        requestAnimationFrame(
            animateCursor
        );

    }


    animateCursor();


    document
        .querySelectorAll(
            "a, button, input, textarea"
        )
        .forEach(element => {

            element.addEventListener(
                "mouseenter",
                () => {

                    cursor.classList.add(
                        "active"
                    );

                    cursorFollower.classList.add(
                        "active"
                    );

                }
            );


            element.addEventListener(
                "mouseleave",
                () => {

                    cursor.classList.remove(
                        "active"
                    );

                    cursorFollower.classList.remove(
                        "active"
                    );

                }
            );

        });

}


/* =====================================================
   PRODUCT DATABASE
===================================================== */

const products = {

    milk: {

        title: "Velvet Milk",

        category: "42% CACAO",

        price: "Rp45.000",

        description:
            "Smooth milk chocolate with creamy caramel notes and a delicate finish."

    },


    noir: {

        title: "Midnight Noir",

        category: "72% CACAO",

        price: "Rp50.000",

        description:
            "Intense dark cacao balanced with roasted notes and a long elegant finish."

    },


    almond: {

        title: "Almond Éclat",

        category: "55% CACAO",

        price: "Rp55.000",

        description:
            "Rich chocolate combined with roasted almond pieces and subtle sea salt."

    }

};


/* =====================================================
   PRODUCT MODAL
===================================================== */

const modal =
    document.getElementById(
        "productModal"
    );

const modalClose =
    document.getElementById(
        "modalClose"
    );

const modalTitle =
    document.getElementById(
        "modalTitle"
    );

const modalCategory =
    document.getElementById(
        "modalCategory"
    );

const modalPrice =
    document.getElementById(
        "modalPrice"
    );

const modalDescription =
    document.getElementById(
        "modalDescription"
    );

const modalCart =
    document.getElementById(
        "modalCart"
    );


let selectedProduct = null;


function openProduct(productId) {

    const product =
        products[productId];

    if (!product) return;

    selectedProduct =
        productId;

    modalTitle.textContent =
        product.title;

    modalCategory.textContent =
        product.category;

    modalPrice.textContent =
        product.price;

    modalDescription.textContent =
        product.description;

    modal.classList.add("open");

    modal.setAttribute(
        "aria-hidden",
        "false"
    );

    body.classList.add(
        "no-scroll"
    );

}


function closeProduct() {

    modal.classList.remove(
        "open"
    );

    modal.setAttribute(
        "aria-hidden",
        "true"
    );

    body.classList.remove(
        "no-scroll"
    );

}


document
    .querySelectorAll(
        "[data-open-product]"
    )
    .forEach(button => {

        button.addEventListener(
            "click",
            () => {

                openProduct(
                    button.dataset.openProduct
                );

            }
        );

    });


modalClose.addEventListener(
    "click",
    closeProduct
);


document
    .querySelector(".modal-backdrop")
    .addEventListener(
        "click",
        closeProduct
    );


document.addEventListener(
    "keydown",
    event => {

        if (event.key === "Escape") {

            closeProduct();

            closeSearch();

        }

    }
);


/* =====================================================
   CART
===================================================== */

const cartCount =
    document.getElementById(
        "cartCount"
    );

let cartItems = 0;


function addToCart() {

    cartItems++;

    cartCount.textContent =
        cartItems;

    modalCart.innerHTML =
        "Added ✓";

    modalCart.style.background =
        "var(--gold-light)";


    setTimeout(() => {

        modalCart.innerHTML =
            'Add to collection <span>+</span>';

        modalCart.style.background =
            "";

    }, 1500);

}


modalCart.addEventListener(
    "click",
    addToCart
);


document
    .getElementById("cartButton")
    .addEventListener(
        "click",
        () => {

            if (cartItems === 0) {

                alert(
                    "Your collection is empty."
                );

            } else {

                alert(
                    `You have ${cartItems} item(s) in your collection.`
                );

            }

        }
    );


/* =====================================================
   SEARCH
===================================================== */

const searchModal =
    document.getElementById(
        "searchModal"
    );

const searchButton =
    document.getElementById(
        "searchButton"
    );

const searchClose =
    document.getElementById(
        "searchClose"
    );

const searchInput =
    document.getElementById(
        "searchInput"
    );

const searchResults =
    document.getElementById(
        "searchResults"
    );


function openSearch() {

    searchModal.classList.add(
        "open"
    );

    setTimeout(() => {

        searchInput.focus();

    }, 300);

}


function closeSearch() {

    searchModal.classList.remove(
        "open"
    );

}


searchButton.addEventListener(
    "click",
    openSearch
);


searchClose.addEventListener(
    "click",
    closeSearch
);


const productEntries =
    Object.entries(products);


searchInput.addEventListener(
    "input",
    () => {

        const query =
            searchInput.value
                .toLowerCase()
                .trim();


        if (!query) {

            searchResults.innerHTML =
                "";

            return;

        }


        const results =
            productEntries.filter(
                ([id, product]) =>
                    product.title
                        .toLowerCase()
                        .includes(query)
                    ||
                    product.category
                        .toLowerCase()
                        .includes(query)
            );


        if (!results.length) {

            searchResults.innerHTML = `
                <div class="search-result">
                    <span>No products found.</span>
                </div>
            `;

            return;

        }


        searchResults.innerHTML =
            results
                .map(
                    ([id, product]) => `
                        <button
                            class="search-result"
                            data-search-product="${id}"
                        >
                            <strong>
                                ${product.title}
                            </strong>

                            <span>
                                ${product.price}
                            </span>
                        </button>
                    `
                )
                .join("");


        document
            .querySelectorAll(
                "[data-search-product]"
            )
            .forEach(button => {

                button.addEventListener(
                    "click",
                    () => {

                        closeSearch();

                        openProduct(
                            button.dataset.searchProduct
                        );

                    }
                );

            });

    }
);


/* =====================================================
   CONTACT FORM
===================================================== */

const contactForm =
    document.getElementById(
        "contactForm"
    );

const formStatus =
    document.getElementById(
        "formStatus"
    );


contactForm.addEventListener(
    "submit",
    event => {

        event.preventDefault();


        const name =
            document
                .getElementById("name")
                .value
                .trim();


        const email =
            document
                .getElementById("email")
                .value
                .trim();


        const message =
            document
                .getElementById("message")
                .value
                .trim();


        if (
            !name ||
            !email ||
            !message
        ) {

            formStatus.textContent =
                "Please complete all fields.";

            return;

        }


        const subject =
            encodeURIComponent(
                `Veloura Contact — ${name}`
            );


        const bodyText =
            encodeURIComponent(
                `Nama: ${name}

Email: ${email}

Pesan:
${message}`
            );


        const mailto =
            `mailto:${CONTACT_EMAIL}` +
            `?subject=${subject}` +
            `&body=${bodyText}`;


        formStatus.textContent =
            "Opening your email application...";


        window.location.href =
            mailto;

    }
);


/* =====================================================
   MAGNETIC BUTTON EFFECT
===================================================== */

const magneticButtons =
    document.querySelectorAll(
        ".button-primary, .nav-cta, .submit-button"
    );


magneticButtons.forEach(button => {

    button.addEventListener(
        "mousemove",
        event => {

            if (
                !window.matchMedia(
                    "(pointer:fine)"
                ).matches
            ) return;


            const rect =
                button.getBoundingClientRect();


            const x =
                event.clientX
                - rect.left
                - rect.width / 2;


            const y =
                event.clientY
                - rect.top
                - rect.height / 2;


            button.style.transform =
                `translate(
                    ${x * .08}px,
                    ${y * .08}px
                )`;

        }
    );


    button.addEventListener(
        "mouseleave",
        () => {

            button.style.transform =
                "";

        }
    );

});


/* =====================================================
   IMAGE-LIKE TILT EFFECT
===================================================== */

document
    .querySelectorAll(".product-image")
    .forEach(card => {

        card.addEventListener(
            "mousemove",
            event => {

                if (
                    !window.matchMedia(
                        "(pointer:fine)"
                    ).matches
                ) return;


                const rect =
                    card.getBoundingClientRect();


                const x =
                    (event.clientX - rect.left)
                    / rect.width
                    - .5;


                const y =
                    (event.clientY - rect.top)
                    / rect.height
                    - .5;


                card.style.transform =
                    `perspective(800px)
                     rotateX(${-y * 4}deg)
                     rotateY(${x * 4}deg)
                     translateY(-8px)`;

            }
        );


        card.addEventListener(
            "mouseleave",
            () => {

                card.style.transform =
                    "";

            }
        );

    });


/* =====================================================
   CONSOLE BRANDING
===================================================== */

console.log(
    "%cVELOURA CHOCOLATE",
    `
        font-size: 24px;
        font-weight: bold;
        color: #c8a46a;
    `
);

console.log(
    "Crafted for moments worth remembering."
);