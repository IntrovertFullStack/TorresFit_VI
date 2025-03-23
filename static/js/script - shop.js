$(document).on('click', '.btn-outline-dark', function(e){
    e.preventDefault();
    var producto_id = $(this).attr('data-producto-id');
    var cantidad = $('#inputQuantity').val();

    $.ajax({
        type: 'POST',
        url: '{% url "cart_add" %}',  // Use the correct URL name from cart app
        data: {
            producto_id: producto_id,
            cantidad: cantidad,
            csrfmiddlewaretoken: '{{ csrf_token }}',
            action: 'post'
        },
        success: function(json){
            // Update the cart quantity displayed on the page
            document.getElementById("cart_quantity").textContent = json.qty;
            // Redirect to the cart summary page
            window.location.href = "{% url 'cart_summary' %}";
        },
        error: function(xhr, errmsg, err){
            console.log(xhr.status + ": " + xhr.responseText); // Log any errors
        }
    });
});