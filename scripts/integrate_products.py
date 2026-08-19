from pathlib import Path

INDEX = Path('index.html')
PRODUCTS = Path('products/index.html')

html = INDEX.read_text(encoding='utf-8')

# Add Products navigation only if not already present.
if 'href="#products"' not in html and 'href="products/"' not in html:
    nav_old = '''          <li class="nav-item">\n            <a class="nav-link nav-link-custom" href="#portfolio">Portfolio</a>\n          </li>'''
    nav_new = '''          <li class="nav-item">\n            <a class="nav-link nav-link-custom" href="#products">Products</a>\n          </li>\n          <li class="nav-item">\n            <a class="nav-link nav-link-custom" href="#portfolio">Portfolio</a>\n          </li>'''
    if nav_old not in html:
        raise SystemExit('Could not find Portfolio navigation item.')
    html = html.replace(nav_old, nav_new, 1)

# Add Supabase client.
supabase_tag = '  <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>'
bootstrap_tag = '  <!-- Bootstrap JS -->'
if supabase_tag not in html:
    if bootstrap_tag not in html:
        raise SystemExit('Could not find Bootstrap JS marker.')
    html = html.replace(bootstrap_tag, '  <!-- Supabase -->\n' + supabase_tag + '\n\n' + bootstrap_tag, 1)

css = r'''

    /* ── Dynamic Products Showcase ── */
    .products-section{position:relative;overflow:hidden;background:linear-gradient(180deg,#f8fbff 0%,#eef7ff 48%,#f8fcff 100%)}
    .products-section:before,.products-section:after{content:'';position:absolute;border-radius:50%;pointer-events:none;filter:blur(70px)}
    .products-section:before{width:360px;height:360px;right:-160px;top:80px;background:rgba(37,99,235,.10)}
    .products-section:after{width:300px;height:300px;left:-150px;bottom:40px;background:rgba(6,182,212,.09)}
    .products-heading{position:relative;z-index:2}.products-heading .section-title{margin-bottom:12px}.products-heading .section-subtitle{margin:0 auto}
    .products-grid-home{position:relative;z-index:2;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px}
    .product-card-home{position:relative;background:rgba(255,255,255,.90);border:1px solid rgba(37,99,235,.10);border-radius:22px;overflow:hidden;box-shadow:0 12px 38px rgba(15,23,42,.07);transition:transform .45s cubic-bezier(.2,.8,.2,1),box-shadow .45s ease,border-color .45s ease;backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px)}
    .product-card-home:hover{transform:translateY(-10px);box-shadow:0 24px 55px rgba(37,99,235,.16);border-color:rgba(37,99,235,.24)}
    .product-image-home{height:205px;position:relative;overflow:hidden;background:linear-gradient(135deg,#eaf2ff,#e8fbff)}
    .product-image-home:after{content:'';position:absolute;inset:0;background:linear-gradient(120deg,transparent 35%,rgba(255,255,255,.48) 50%,transparent 65%);background-size:220% 100%;opacity:0;transition:opacity .35s ease}
    .product-card-home:hover .product-image-home:after{opacity:1;animation:productShine 1.15s ease forwards}@keyframes productShine{from{background-position:-120% 0}to{background-position:120% 0}}
    .product-image-home img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .65s cubic-bezier(.2,.8,.2,1)}.product-card-home:hover .product-image-home img{transform:scale(1.055)}
    .product-category-home{position:absolute;left:14px;top:14px;z-index:2;padding:6px 11px;border-radius:999px;background:rgba(255,255,255,.92);color:var(--primary);font-size:.68rem;font-weight:700;letter-spacing:.5px;box-shadow:0 7px 20px rgba(15,23,42,.10)}
    .product-content-home{padding:21px 21px 20px}.product-content-home h3{font-size:1.12rem;font-weight:700;margin:0 0 7px;color:var(--dark)}
    .product-content-home p{color:var(--gray);font-size:.83rem;line-height:1.65;margin:0 0 16px;min-height:55px;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
    .product-meta-home{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:17px}.product-tag-home{font-size:.65rem;font-weight:600;padding:5px 8px;border-radius:7px;background:#eff5ff;color:#526079}
    .product-link-home{display:inline-flex;align-items:center;gap:8px;color:var(--primary);font-size:.82rem;font-weight:700;text-decoration:none;transition:var(--transition)}.product-link-home i{transition:transform .3s ease}.product-link-home:hover{color:var(--primary-dark)}.product-link-home:hover i{transform:translateX(5px)}
    .products-empty-home{grid-column:1/-1;text-align:center;padding:40px 20px;color:var(--gray)}.products-cta-home{position:relative;z-index:2;margin-top:36px;text-align:center}.products-cta-home .btn-outline-custom{display:inline-flex;align-items:center;gap:9px}
    .products-loader-home{grid-column:1/-1;display:flex;justify-content:center;padding:42px}.products-loader-home span{width:32px;height:32px;border:3px solid #dbe7fb;border-top-color:var(--primary);border-radius:50%;animation:productSpin .8s linear infinite}@keyframes productSpin{to{transform:rotate(360deg)}}
    @media(max-width:991.98px){.products-grid-home{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:575.98px){.products-grid-home{grid-template-columns:1fr;gap:18px}.product-image-home{height:210px}.product-content-home p{min-height:auto}}
'''
if '/* ── Dynamic Products Showcase ── */' not in html:
    html = html.replace('</style>', css + '\n  </style>', 1)

section = '''

  <!-- ═══════════════════ OUR PRODUCTS ═══════════════════ -->
  <section class="products-section section-padding" id="products">
    <div class="container">
      <div class="products-heading text-center animate-on-scroll">
        <span class="section-label">Our Products</span>
        <h2 class="section-title">Digital Solutions We've <span class="gradient-text">Built</span></h2>
        <p class="section-subtitle mx-auto">Explore real-world web applications and digital products created by HOPIX Tech Solutions.</p>
      </div>
      <div id="homeProductsGrid" class="products-grid-home mt-5"><div class="products-loader-home"><span></span></div></div>
      <div class="products-cta-home animate-on-scroll"><a href="products/" class="btn btn-outline-custom">Explore All Products <i class="bi bi-arrow-right"></i></a></div>
    </div>
  </section>
'''
if 'id="homeProductsGrid"' not in html:
    marker = '  <!-- ═══════════════════ WHY CHOOSE US ═══════════════════ -->'
    if marker not in html:
        raise SystemExit('Could not find Why Choose Us insertion point.')
    html = html.replace(marker, section + '\n' + marker, 1)

js = r'''

    /* ── Dynamic Products Showcase ── */
    (async function loadHomeProducts(){
      const grid=document.getElementById('homeProductsGrid');if(!grid||!window.supabase)return;
      const client=window.supabase.createClient('https://zfgjhunmdpqzpmdnqtyv.supabase.co','sb_publishable_grTmssZ9sTu5YKXrH0ET6A_8wDNP2IT');
      const esc=value=>String(value??'').replace(/[&<>"']/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[ch]));
      const tags=value=>Array.isArray(value)?value:String(value??'').split(/[,\n]+/).map(v=>v.trim()).filter(Boolean);
      try{
        const {data,error}=await client.from('products').select('*').eq('status','published').order('created_at',{ascending:false}).limit(3);if(error)throw error;
        if(!data?.length){grid.innerHTML='<div class="products-empty-home">Our newest products are coming soon.</div>';return;}
        grid.innerHTML=data.map(product=>{const name=product.name||'HOPIX Product',category=product.category||'Digital Product',description=product.short_description||product.description||'A digital solution built by HOPIX Tech Solutions.',image=product.image_url||'',technologies=tags(product.technologies).slice(0,3);return `<article class="product-card-home animate-on-scroll"><div class="product-image-home">${image?`<img src="${esc(image)}" alt="${esc(name)}" loading="lazy">`:'<div style="height:100%;display:flex;align-items:center;justify-content:center;font-size:48px;color:rgba(37,99,235,.22)"><i class="bi bi-window-stack"></i></div>'}<span class="product-category-home">${esc(category)}</span></div><div class="product-content-home"><h3>${esc(name)}</h3><p>${esc(description)}</p><div class="product-meta-home">${technologies.map(t=>`<span class="product-tag-home">${esc(t)}</span>`).join('')}</div><a href="products/" class="product-link-home">View Product <i class="bi bi-arrow-right"></i></a></div></article>`}).join('');
      }catch(error){console.error('Home products error:',error);grid.innerHTML='<div class="products-empty-home">Products are temporarily unavailable. Please try again shortly.</div>'}
    })();
'''
if 'loadHomeProducts' not in html:
    needle = '    /* ── Consultation form ── */'
    if needle not in html:
        raise SystemExit('Could not find consultation script insertion point.')
    html = html.replace(needle, js + '\n' + needle, 1)

INDEX.write_text(html, encoding='utf-8')

if PRODUCTS.exists():
    phtml = PRODUCTS.read_text(encoding='utf-8')
    phtml = phtml.replace(".eq('is_published',true)", ".eq('status','published')")
    phtml = phtml.replace("val(p,'live_url','website_url','demo_url','url')", "val(p,'product_url','live_url','website_url','demo_url','url')")
    PRODUCTS.write_text(phtml, encoding='utf-8')

print('HOPIX Products integration applied successfully.')
