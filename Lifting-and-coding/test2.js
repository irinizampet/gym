var inputs = document.querySelector('form.input_field input');
      quantity = document.querySelector('quantity');
      quantityText = <span> Number of skills: </span>;



let listArray = []
inputs.forEach(input => {
       input.addEventListener('click', () => {
            input.classList.toggle('checked')
            var checked = document.querySelectorAll('.checked')
            quantity.innerHTML = quantityText + checked.length

       })

})