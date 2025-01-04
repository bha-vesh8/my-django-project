const productcont = document.querySelector('.product-container');
const nxtbtn = document.querySelector('.nxt-btn');
const prebtn = document.querySelector('.pre-btn');

productcont.addEventListener("wheel", (evt) => {
    evt.preventDefault();
    productcont.scrollLeft += evt.deltaY;
    productcont.style.scrollBehavior = "auto"
});

nxtbtn.addEventListener("click", () => {
    productcont.style.scrollBehavior = "smooth";
    productcont.scrollLeft -= 900;
});

prebtn.addEventListener("click", () => {
    productcont.style.scrollBehavior = "smooth";
    productcont.scrollLeft += 900;
});

const productcont1 = document.querySelector('.product-container1');
const nxtbtn1 = document.querySelector('.nxt-btn1');
const prebtn1 = document.querySelector('.pre-btn1');

productcont1.addEventListener("wheel", (evt) => {
    evt.preventDefault();
    productcont1.scrollLeft += evt.deltaY;
    productcont1.style.scrollBehavior = "auto"
});

nxtbtn1.addEventListener("click", () => {
    productcont1.style.scrollBehavior = "smooth";
    productcont1.scrollLeft -= 900;
});

prebtn1.addEventListener("click", () => {
    productcont1.style.scrollBehavior = "smooth";
    productcont1.scrollLeft += 900;
});

const productcont2 = document.querySelector('.product-container2');
const nxtbtn2 = document.querySelector('.nxt-btn2');
const prebtn2 = document.querySelector('.pre-btn2');

productcont2.addEventListener("wheel", (evt) => {
    evt.preventDefault();
    productcont2.scrollLeft += evt.deltaY;
    productcont2.style.scrollBehavior = "auto"
});

nxtbtn2.addEventListener("click", () => {
    productcont2.style.scrollBehavior = "smooth";
    productcont2.scrollLeft -= 900;
});

prebtn2.addEventListener("click", () => {
    productcont2.style.scrollBehavior = "smooth";
    productcont2.scrollLeft += 900;
});

document.addEventListener("DOMContentLoaded", function () {
    // Select all "Add to Cart" buttons
    const addToCartButtons = document.querySelectorAll(".add-to-cart");
  
    // Initialize an empty array to store cart items
    let cart = [];
  
    // Function to handle adding items to the cart
    function addToCartHandler(event) {
      // Get the parent element of the clicked button, which contains product information
      const productContainer = event.target.closest(".product-container");
  
      // Extract product details from the container
      const productName = productContainer.querySelector("h1").textContent;
      const productPrice = parseFloat(productContainer.querySelector(".price").textContent.replace(/[^\d.]/g, ''));
      // Replace non-numeric characters with empty string and convert to float
  
      // Create an object representing the product
      const product = {
        name: productName,
        price: productPrice
      };
  
      // Add the product to the cart array
      cart.push(product);
  
      // Optionally, update UI to indicate item has been added to cart
      alert(`${productName} added to cart!`);
  
      // You can also update the cart UI, for example:
      // const cartCount = document.querySelector("#cart-count");
      // cartCount.textContent = cart.length;
    }
  
    // Attach click event listener to each "Add to Cart" button
    addToCartButtons.forEach(button => {
      button.addEventListener("click", addToCartHandler);
    });
  });
  