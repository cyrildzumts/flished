
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'UA-189272780-1');
  gtag('config', 'GTM-5CLRZBG');
  gtag('config', 'AW-460426366');
  gtag('config', 'G-GZEWSF8YCE');
  let product = document.getElementById('product');
  gtag('event', 'view_item', {
    'send_to': 'AW-460426366',
    'value': product.dataset.price,
    'items': [{
      'id': product.dataset.id,
      'title': product.dataset.name,
      'name': product.dataset.name,
      'brand': product.dataset.brand,
      'category': product.dataset.category,
      'price': product.dataset.price,
      'url': product.dataset.url,
      'image': product.dataset.image,
      'google_business_vertical': 'custom'
    }]
  });