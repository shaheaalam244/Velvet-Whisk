document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.add-to-cart').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const id = e.target.dataset.id;
      alert('Add to cart clicked for cake id: ' + id + '\n(Backend route will be implemented later.)');
      // later: submit POST form to /add_to_cart or use a small form submission
    });
  });
});
