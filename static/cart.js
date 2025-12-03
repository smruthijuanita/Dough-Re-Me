(function(){
  const KEY = 'drm_cart_v1';
  function getCart(){
    try { return JSON.parse(localStorage.getItem(KEY)||'[]'); } catch { return []; }
  }
  function setCart(arr){ localStorage.setItem(KEY, JSON.stringify(arr)); }
  function updateBadge(){
    const badge = document.getElementById('cartBadge');
    if(!badge) return;
    const arr = getCart();
    const count = arr.reduce((s,i)=>s + (i.quantity||i.qty||0), 0);
    badge.textContent = count;
  }
  window.addEventListener('DOMContentLoaded', updateBadge);

  window.addItemToCart = function(item){
    const arr = getCart();
    const id = item.id;
    const qty = item.quantity || item.qty || 1;
    const found = arr.find(x => x.id === id);
    if(found){ found.quantity = (found.quantity||0) + qty; }
    else { arr.push({ id: id, name: item.name, price: item.price, quantity: qty, img: item.img, category: item.category, options: item.options }); }
    setCart(arr);
    updateBadge();
  };
})();
