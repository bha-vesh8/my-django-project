document.querySelector("button").addEventListener("click", () => {
    let query = document.querySelector('.inpt').value;
    let url = `https://www.google.com/search?q=${query}`;
    window.open(url, '_blank');
    document.querySelector('.inpt').value = '';
  });
  
  