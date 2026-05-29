document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('input[name="search"]');
    const modelGrid = document.getElementById('model-grid');
    let searchTimeout;

    if (!searchInput) return;

    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(function() {
            const query = searchInput.value;
            fetch(`/api/models/search/?q=${query}`)
                .then(res => res.json())
                .then(data => {
                    modelGrid.innerHTML = '';
                    if (data.length === 0) {
                        modelGrid.innerHTML = `
                            <div class="col-12 text-center text-secondary py-5">
                                <i class="bi bi-search" style="font-size:3rem"></i>
                                <p class="mt-3">Model bulunamadı.</p>
                            </div>`;
                        return;
                    }
                    data.forEach(model => {
                        modelGrid.innerHTML += `
                        <div class="col-md-6 col-lg-4">
                            <div class="card h-100 p-3">
                                <div class="d-flex justify-content-between align-items-start mb-3">
                                    <div class="d-flex align-items-center gap-2">
                                        <img src="${model.image_url}" alt="${model.name}"
                                             style="width:36px;height:36px;object-fit:contain;border-radius:8px;"
                                             onerror="this.style.display='none'">
                                        <div>
                                            <h5 class="fw-bold mb-0">${model.name}</h5>
                                            <small class="text-secondary">${model.company}</small>
                                        </div>
                                    </div>
                                    <div class="d-flex gap-1">
                                        ${model.is_multimodal ? '<span class="badge-multimodal">Multimodal</span>' : ''}
                                        ${model.is_free ? '<span class="badge-free">Ücretsiz</span>' : ''}
                                    </div>
                                </div>
                                <p class="text-secondary small mb-3">${model.description ? model.description.split(' ').slice(0,20).join(' ') + '...' : ''}</p>
                                <div class="mb-3">
                                    ${model.input_price ? `<div class="price-tag"><i class="bi bi-arrow-down-circle"></i> $${(model.input_price * 1000000).toFixed(2)} / 1M token</div>` : ''}
                                    ${model.context_window ? `<small class="text-secondary"><i class="bi bi-window"></i> ${model.context_window}k context</small>` : ''}
                                </div>
                                <div class="d-flex gap-2 mt-auto">
                                    <a href="/model/${model.id}/" class="btn btn-primary btn-sm flex-grow-1">
                                        <i class="bi bi-info-circle"></i> Detay
                                    </a>
                                    <a href="/compare/?models=${model.id}" class="btn btn-outline-primary btn-sm">
                                        <i class="bi bi-bar-chart"></i>
                                    </a>
                                </div>
                            </div>
                        </div>`;
                    });
                })
                .catch(err => console.error('Arama hatası:', err));
        }, 400);
    });
});