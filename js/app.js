// ========================================================
// 진주퀸공인중개사사무소 - Modern Interactive Real Estate App
// UI UX Pro Max & Taste Skill Standards
// ========================================================

let state = {
  category: 'ALL',
  transType: 'ALL',
  statusFilter: 'ALL', // 'ALL', 'ACTIVE', 'SOLD'
  searchQuery: '',
  sort: 'recommend',
  selectedPropertyId: null,
  viewMode: 'split',
  favorites: JSON.parse(localStorage.getItem('jinjuqueen_favs') || '[]')
};

let map = null;
let officeMap = null;
let markersMap = {};
let officeMarker = null;

// Initialize on DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
  initMap();
  initOfficeMap();
  loadLiveProperties();
  renderMediaSection();
  loadLiveNews();
  updateFavBadge();
  setupEventListeners();
  if (window.lucide) {
    lucide.createIcons();
  }
});

// 실시간 매물 로드 (관리자 등록 즉시 홈페이지 지도 및 목록 동기화)
async function loadLiveProperties() {
  try {
    const res = await fetch('/api/properties?t=' + Date.now());
    if (res.ok) {
      const data = await res.json();
      const props = data.properties || (Array.isArray(data) ? data : null);
      if (props && Array.isArray(props) && props.length > 0) {
        PROPERTIES_DATA = props;
        renderProperties();
        updateMapMarkers();
        return;
      }
    }
    // Fallback to static data/properties.json file
    const fileRes = await fetch('data/properties.json?t=' + Date.now());
    if (fileRes.ok) {
      const fileProps = await fileRes.json();
      if (Array.isArray(fileProps) && fileProps.length > 0) {
        PROPERTIES_DATA = fileProps;
        renderProperties();
        updateMapMarkers();
        return;
      }
    }
  } catch (err) {
    console.warn('Live properties fetch error, falling back to static data:', err);
  }
  renderProperties();
  updateMapMarkers();
}

function setupEventListeners() {
  const searchInput = document.getElementById('searchInput');
  if (searchInput) {
    searchInput.addEventListener('keyup', (e) => {
      if (e.key === 'Enter') {
        executeSearch();
      }
    });
  }

  // Mobile menu toggle
  const mobileMenuBtn = document.getElementById('mobileMenuBtn');
  const mobileMenuDropdown = document.getElementById('mobileMenuDropdown');
  if (mobileMenuBtn && mobileMenuDropdown) {
    mobileMenuBtn.addEventListener('click', () => {
      mobileMenuDropdown.classList.toggle('hidden');
    });
  }
}

// ----------------------------------------------------
// MAP INITIALIZATION (Google Maps Layer Integration)
// ----------------------------------------------------
const GOOGLE_ROADMAP_URL = 'https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}&hl=ko';
const GOOGLE_SATELLITE_URL = 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}&hl=ko';

let currentPropertyTileLayer = null;

function initMap() {
  const mapContainer = document.getElementById('propertyMap');
  if (!mapContainer) return;

  // Center on Jinju Chungmu-gong-dong (혁신도시)
  map = L.map('propertyMap', {
    center: [35.176734, 128.144606],
    zoom: 15,
    zoomControl: true,
    scrollWheelZoom: true
  });

  // Default: Google Roadmap with clean Korean labels
  currentPropertyTileLayer = L.tileLayer(GOOGLE_ROADMAP_URL, {
    attribution: '&copy; Google Maps',
    maxZoom: 20
  }).addTo(map);

  // Render markers
  updateMapMarkers();
}

function setMapLayer(type) {
  if (!map || !currentPropertyTileLayer) return;
  map.removeLayer(currentPropertyTileLayer);

  const btnRoad = document.getElementById('btnLayerRoad');
  const btnSat = document.getElementById('btnLayerSat');

  if (type === 'satellite') {
    currentPropertyTileLayer = L.tileLayer(GOOGLE_SATELLITE_URL, {
      attribution: '&copy; Google Maps Satellite',
      maxZoom: 20
    }).addTo(map);
    if (btnRoad) { btnRoad.className = 'px-2 py-1 rounded-md text-slate-500 font-medium hover:text-slate-800 transition'; }
    if (btnSat) { btnSat.className = 'px-2 py-1 rounded-md bg-white text-slate-900 font-bold shadow-sm transition'; }
    showToast('구글 고화질 위성지도로 전환되었습니다.');
  } else {
    currentPropertyTileLayer = L.tileLayer(GOOGLE_ROADMAP_URL, {
      attribution: '&copy; Google Maps',
      maxZoom: 20
    }).addTo(map);
    if (btnRoad) { btnRoad.className = 'px-2 py-1 rounded-md bg-white text-slate-900 font-bold shadow-sm transition'; }
    if (btnSat) { btnSat.className = 'px-2 py-1 rounded-md text-slate-500 font-medium hover:text-slate-800 transition'; }
    showToast('구글 일반지도로 전환되었습니다.');
  }
}

function initOfficeMap() {
  const officeMapContainer = document.getElementById('officeMap');
  if (!officeMapContainer) return;

  // Exact coordinates for 경남 진주시 에나로 146 라온프라이빗시티 105호
  const OFFICE_LAT = 35.176734;
  const OFFICE_LNG = 128.144606;

  officeMap = L.map('officeMap', {
    center: [OFFICE_LAT, OFFICE_LNG],
    zoom: 17, // Closer, crisp view of Raon Private City building
    zoomControl: true,
    scrollWheelZoom: true,
    dragging: true
  });

  // Google Maps Roadmap for Office
  L.tileLayer(GOOGLE_ROADMAP_URL, {
    attribution: '&copy; Google Maps',
    maxZoom: 20
  }).addTo(officeMap);

  const officeIcon = L.divIcon({
    className: 'office-pin',
    html: `
      <div style="background:#0F172A; color:#FFFFFF; padding:7px 15px; border-radius:24px; font-weight:800; font-size:12px; box-shadow:0 6px 20px rgba(15,23,42,0.5); border:2px solid #C29B38; display:flex; align-items:center; gap:6px; transform:translate(-50%, -100%); cursor:pointer;">
        <img src="images/logo.png" style="width:20px; height:20px; object-fit:contain;">
        <span>진주퀸공인중개사 (라온프라이빗시티 105호)</span>
      </div>
    `,
    iconSize: [230, 38],
    iconAnchor: [115, 38]
  });

  officeMarker = L.marker([OFFICE_LAT, OFFICE_LNG], { icon: officeIcon }).addTo(officeMap);

  // Informative Interactive Popup
  officeMarker.bindPopup(`
    <div style="font-family:'Pretendard',sans-serif; padding:5px; max-width:280px;">
      <div style="font-size:14px; font-weight:800; color:#0F172A; margin-bottom:4px; display:flex; align-items:center; gap:5px;">
        <span style="color:#C29B38; font-size:16px;">👑</span> 진주퀸공인중개사사무소
      </div>
      <div style="font-size:12px; color:#334155; line-height:1.45; margin-bottom:6px;">
        경상남도 진주시 에나로 146, 105호 (라온프라이빗시티)<br>
        <span style="color:#0D9488; font-weight:700;">LH 본사 공원 맞은편 · 탑마트 주변 중심상가 1층</span>
      </div>
      <div style="font-size:12px; font-weight:800; color:#C29B38; margin-bottom:8px;">
        직통 010-4670-7248 / 유선 055-761-7248
      </div>
      <div style="border-top:1px solid #E2E8F0; padding-top:8px; display:flex; items-center; justify-content:space-between; font-size:11px; font-weight:700;">
        <a href="https://map.naver.com/v5/search/%EC%A7%84%EC%A3%BC%EC%8B%9C%20%EC%97%90%EB%82%98%EB%A1%9C%20146%20%EB%9D%BC%EC%98%A8%ED%94%84%EB%9D%BC%EC%9D%B4%EB%B9%97%EC%8B%9C%ED%8B%B0" target="_blank" style="color:#03C75A; text-decoration:none;">
          네이버 지도 &rarr;
        </a>
        <a href="https://map.kakao.com/link/to/진주퀸공인중개사사무소,35.176734,128.144606" target="_blank" style="color:#3C1E1E; background:#FEE500; padding:2px 7px; border-radius:5px; text-decoration:none;">
          카카오 길찾기
        </a>
      </div>
    </div>
  `).openPopup();
}

function updateMapMarkers() {
  if (!map) return;

  // Clear existing markers
  Object.values(markersMap).forEach(marker => map.removeLayer(marker));
  markersMap = {};

  const filtered = getFilteredProperties();
  const bounds = [];
  const coordCounts = {};

  filtered.forEach(prop => {
    // Custom formatted pin label
    let priceLabel = '';
    if (prop.transactionType === '매매') {
      const p = prop.price || 0;
      priceLabel = p >= 10000 ? `매매 ${(p / 10000).toFixed(1)}억` : `매매 ${p}만`;
    } else if (prop.transactionType === '전세') {
      const p = prop.price || 0;
      priceLabel = p >= 10000 ? `전세 ${(p / 10000).toFixed(1)}억` : `전세 ${p}만`;
    } else {
      const dep = (prop.deposit !== undefined && prop.deposit !== null) ? prop.deposit : 0;
      const rent = (prop.monthlyRent !== undefined && prop.monthlyRent !== null) ? prop.monthlyRent : 0;
      if (dep > 0 || rent > 0) {
        priceLabel = `월 ${dep}/${rent}`;
      } else if (prop.priceFormatted) {
        priceLabel = prop.priceFormatted.replace('보증금 ', '월 ').replace('만원', '').trim();
      } else {
        priceLabel = '월세';
      }
    }

    // 동일 좌표 분산 (라온프라이빗시티 등 동일 단지/지번 매물들이 서로 가려지지 않고 선명하게 각각 노출되도록 미세 분산)
    let lat = Number(prop.lat) || 35.1764;
    let lng = Number(prop.lng) || 128.144606;
    const coordKey = `${lat.toFixed(4)},${lng.toFixed(4)}`;

    if (coordCounts[coordKey] === undefined) {
      coordCounts[coordKey] = 0;
    } else {
      coordCounts[coordKey] += 1;
      const count = coordCounts[coordKey];
      const angle = (count * 2 * Math.PI) / 6;
      const radius = 0.00035; // 약 35m fanning
      lat += Math.sin(angle) * radius;
      lng += Math.cos(angle) * radius;
    }

    const isSold = prop.status === 'SOLD';
    const customIcon = L.divIcon({
      className: `custom-map-pin ${state.selectedPropertyId === prop.id ? 'active' : ''} ${isSold ? 'sold-pin' : ''}`,
      html: `<span>${priceLabel}</span>`,
      iconSize: [85, 28],
      iconAnchor: [42, 34]
    });

    const marker = L.marker([lat, lng], { icon: customIcon }).addTo(map);
    
    marker.on('click', () => {
      highlightPropertyCard(prop.id, true);
    });

    markersMap[prop.id] = marker;
    bounds.push([lat, lng]);
  });

  // Fit bounds if markers exist
  if (bounds.length > 0) {
    map.fitBounds(bounds, { padding: [40, 40], maxZoom: 16 });
  }
}

function centerMapOnOffice() {
  if (!map) return;
  map.flyTo([35.176734, 128.144606], 16, { duration: 1.2 });
  showToast('진주퀸공인중개사사무소 (에나로 146) 위치로 이동했습니다.');
}

// ----------------------------------------------------
// PROPERTY FILTERING & SORTING
// ----------------------------------------------------
function getFilteredProperties() {
  return PROPERTIES_DATA.filter(item => {
    // Category filter
    if (state.category !== 'ALL' && item.category !== state.category) {
      return false;
    }
    // Transaction type filter
    if (state.transType !== 'ALL' && item.transactionType !== state.transType) {
      return false;
    }
    // Status filter (ACTIVE, SOLD, ALL)
    if (state.statusFilter === 'ACTIVE' && item.status === 'SOLD') {
      return false;
    }
    if (state.statusFilter === 'SOLD' && item.status !== 'SOLD') {
      return false;
    }
    // Search query
    if (state.searchQuery) {
      const q = state.searchQuery.toLowerCase();
      const matchTitle = item.title.toLowerCase().includes(q);
      const matchLoc = item.location.toLowerCase().includes(q);
      const matchTags = item.tags.some(t => t.toLowerCase().includes(q));
      if (!matchTitle && !matchLoc && !matchTags) return false;
    }
    return true;
  }).sort((a, b) => {
    if (state.sort === 'priceAsc') return a.price - b.price;
    if (state.sort === 'priceDesc') return b.price - a.price;
    if (state.sort === 'areaDesc') return b.exclusiveArea - a.exclusiveArea;
    // recommend default
    return (b.isRecommended ? 1 : 0) - (a.isRecommended ? 1 : 0);
  });
}

function setCategoryFilter(category) {
  state.category = category;
  document.querySelectorAll('#categoryTabGroup .category-btn').forEach(btn => {
    const isCur = btn.getAttribute('data-category') === category;
    btn.classList.toggle('active', isCur);
  });
  updateFilterDisplay();
  renderProperties();
  updateMapMarkers();
}

function setTransFilter(transType) {
  state.transType = transType;
  document.querySelectorAll('#transTypeGroup .trans-btn').forEach(btn => {
    const isCur = btn.getAttribute('data-trans') === transType;
    btn.classList.toggle('active', isCur);
  });
  updateFilterDisplay();
  renderProperties();
  updateMapMarkers();
}

function executeSearch() {
  const input = document.getElementById('searchInput');
  state.searchQuery = input ? input.value.trim() : '';
  updateFilterDisplay();
  renderProperties();
  updateMapMarkers();

  // Scroll smoothly down to properties section
  const section = document.getElementById('properties-section');
  if (section) {
    section.scrollIntoView({ behavior: 'smooth' });
  }
}

function applySorting(sortVal) {
  state.sort = sortVal;
  renderProperties();
}

function resetAllFilters() {
  state.category = 'ALL';
  state.transType = 'ALL';
  state.searchQuery = '';
  state.sort = 'recommend';
  const input = document.getElementById('searchInput');
  if (input) input.value = '';
  const sortSelect = document.getElementById('sortSelect');
  if (sortSelect) sortSelect.value = 'recommend';

  setCategoryFilter('ALL');
  setTransFilter('ALL');
  showToast('모든 검색 필터가 초기화되었습니다.');
}

function updateFilterDisplay() {
  const label = document.getElementById('activeFilterLabel');
  if (!label) return;
  const parts = [];
  if (state.category !== 'ALL') parts.push(state.category);
  if (state.transType !== 'ALL') parts.push(state.transType);
  if (state.searchQuery) parts.push(`"${state.searchQuery}"`);
  label.textContent = parts.length > 0 ? parts.join(' · ') : '전체 매물';
}

// ----------------------------------------------------
// PROPERTY RENDERING (Editorial Cards)
// ----------------------------------------------------
function renderProperties() {
  const container = document.getElementById('propertyCardsContainer');
  const countEl = document.getElementById('propertyCount');
  if (!container) return;

  const list = getFilteredProperties();
  if (countEl) countEl.textContent = list.length;

  if (list.length === 0) {
    container.innerHTML = `
      <div class="bg-white rounded-2xl p-12 text-center border border-slate-200">
        <div class="w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center mx-auto mb-3 text-slate-400">
          <i data-lucide="search-x" class="w-6 h-6"></i>
        </div>
        <h4 class="font-bold text-slate-800 text-base">조건에 일치하는 매물이 없습니다</h4>
        <p class="text-xs text-slate-500 mt-1 max-w-sm mx-auto">
          찾으시는 아파트나 상가 조건이 있으시면 황선숙 대표에게 전화 주시면 최적의 맞춤 매물을 즉시 찾아드립니다.
        </p>
        <button onclick="resetAllFilters()" class="mt-4 px-4 py-2 bg-brand-navy text-white text-xs font-bold rounded-xl hover:bg-slate-800 transition">
          검색조건 초기화
        </button>
      </div>
    `;
    if (window.lucide) lucide.createIcons();
    return;
  }

  container.innerHTML = list.map(prop => {
    const isFav = state.favorites.includes(prop.id);
    const badgeColor = prop.badge === '추천매물' ? 'bg-amber-100 text-amber-800 border-amber-200' :
                       prop.badge === '급전세' ? 'bg-rose-100 text-rose-800 border-rose-200' :
                       'bg-emerald-100 text-emerald-800 border-emerald-200';

    const isSold = prop.status === 'SOLD';
    const clickAction = isSold ? `openSoldNoticeModal('${prop.id}')` : `openPropertyModal('${prop.id}')`;
    const cardOpacity = isSold ? 'opacity-90 grayscale-[25%]' : '';

    return `
      <article id="card-${prop.id}" 
               onclick="${clickAction}"
               onmouseenter="onPropertyHover('${prop.id}')"
               class="property-card bg-white rounded-2xl border border-slate-200 overflow-hidden cursor-pointer flex flex-col sm:flex-row group ${cardOpacity}">
        
        <!-- Image Preview (High impact editorial thumbnail) -->
        <div class="sm:w-2/5 relative h-52 sm:h-auto overflow-hidden bg-slate-100 shrink-0">
          <img src="${prop.images[0]}" alt="${prop.title}" 
               loading="lazy"
               class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
          
          <!-- Sold Stamp Overlay -->
          ${isSold ? `
            <div class="absolute inset-0 bg-slate-950/70 backdrop-blur-[2px] flex flex-col items-center justify-center p-3 text-center z-10">
              <span class="px-3.5 py-1.5 rounded-full bg-rose-600 text-white font-extrabold text-xs shadow-xl tracking-wider border-2 border-white/90 transform -rotate-3 mb-1 flex items-center gap-1">
                <i data-lucide="check-circle" class="w-3.5 h-3.5"></i> 계약 체결 완료
              </span>
              <span class="text-[10px] text-slate-200 font-semibold">진주퀸 거래완료 성사실적</span>
            </div>
          ` : ''}

          <div class="absolute top-3 left-3 flex flex-wrap gap-1.5 z-20">
            <span class="text-[11px] font-bold px-2.5 py-0.5 rounded-full border shadow-sm backdrop-blur-sm ${isSold ? 'bg-slate-800 text-white border-slate-700' : badgeColor}">
              ${isSold ? '거래완료' : prop.badge}
            </span>
            <span class="text-[11px] font-semibold bg-slate-900/80 text-white px-2 py-0.5 rounded-full backdrop-blur-sm">
              ${prop.category}
            </span>
          </div>

          <!-- Favorite Button -->
          <button onclick="toggleFavorite(event, '${prop.id}')" 
                  class="absolute top-3 right-3 w-8 h-8 rounded-full bg-white/90 backdrop-blur-sm flex items-center justify-center text-slate-700 hover:text-rose-600 transition shadow-md" 
                  title="관심매물 저장">
            <i data-lucide="heart" class="w-4 h-4 ${isFav ? 'text-rose-600 fill-rose-600' : ''}"></i>
          </button>

          <!-- Photo count pill -->
          <div class="absolute bottom-2.5 right-2.5 bg-black/60 text-white text-[10px] font-semibold px-2 py-0.5 rounded-md backdrop-blur-sm flex items-center gap-1">
            <i data-lucide="camera" class="w-3 h-3"></i>
            <span>${prop.images.length}</span>
          </div>
        </div>

        <!-- Details Column -->
        <div class="p-5 flex-1 flex flex-col justify-between">
          <div>
            <!-- Location & Direction -->
            <div class="flex items-center justify-between text-xs text-slate-500 mb-1 gap-2">
              <span class="font-medium text-slate-600 shrink-0">${prop.location}</span>
              <span class="text-right">${[prop.floor, prop.direction].filter(Boolean).join(' ')}</span>
            </div>

            <!-- Title -->
            <h3 class="text-base font-bold text-slate-900 group-hover:text-amber-700 transition leading-snug line-clamp-1 mb-2">
              ${prop.title}
            </h3>

            <!-- Price (Prominent typography) -->
            <div class="flex items-baseline gap-2 mb-3">
              <span class="text-xl font-extrabold ${isSold ? 'text-slate-500 line-through' : 'text-amber-600'} tracking-tight">${prop.priceFormatted}</span>
              ${isSold ? '<span class="text-xs font-bold text-rose-600 bg-rose-50 border border-rose-200 px-2 py-0.5 rounded">거래완료</span>' : ''}
              <span class="text-xs font-semibold text-slate-500">
                전용 ${prop.exclusiveArea}㎡ (${prop.exclusiveAreaPyeong}평)
              </span>
            </div>

            <!-- Tags -->
            <div class="flex flex-wrap gap-1.5 mb-3">
              ${prop.tags.map(tag => `<span class="text-[11px] bg-slate-100 text-slate-600 px-2 py-0.5 rounded-md font-medium">#${tag}</span>`).join('')}
            </div>
          </div>

          <!-- Bottom Footer Row: Maintenance Fee & Direct Actions -->
          <div class="pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
            <span class="truncate max-w-[190px]">관리비 : ${prop.maintenanceFee}</span>
            <div class="flex items-center gap-2">
              ${isSold ? `
                <span class="text-rose-600 font-bold flex items-center gap-1 bg-rose-50 px-2.5 py-1 rounded-md border border-rose-200">
                  <i data-lucide="lock" class="w-3.5 h-3.5"></i> 열람제한 (거래완료)
                </span>
              ` : `
                <span class="text-brand-navy font-bold group-hover:translate-x-0.5 transition flex items-center gap-0.5">
                  상세보기 <i data-lucide="chevron-right" class="w-3.5 h-3.5"></i>
                </span>
              `}
            </div>
          </div>

        </div>
      </article>
    `;
  }).join('');

  if (window.lucide) {
    lucide.createIcons();
  }
}

function onPropertyHover(propId) {
  // Pan subtly to map marker if in split or map mode
  const marker = markersMap[propId];
  if (marker && map) {
    const prop = PROPERTIES_DATA.find(p => p.id === propId);
    if (prop) {
      // Don't fly immediately on fast hover, just highlight icon
      Object.keys(markersMap).forEach(id => {
        const el = markersMap[id].getElement();
        if (el) el.classList.toggle('active', id === propId);
      });
    }
  }
}

function highlightPropertyCard(propId, shouldScroll = false) {
  state.selectedPropertyId = propId;
  
  // Highlight map marker
  Object.keys(markersMap).forEach(id => {
    const el = markersMap[id].getElement();
    if (el) el.classList.toggle('active', id === propId);
  });

  // Highlight card
  document.querySelectorAll('.property-card').forEach(card => card.classList.remove('active-selected'));
  const card = document.getElementById(`card-${propId}`);
  if (card) {
    card.classList.add('active-selected');
    if (shouldScroll) {
      card.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }
}

// ----------------------------------------------------
// VIEW MODES (Split / List / Map)
// ----------------------------------------------------
function switchViewMode(mode) {
  state.viewMode = mode;
  const listCol = document.getElementById('listColumn');
  const mapCol = document.getElementById('mapColumn');
  const splitCont = document.getElementById('splitContainer');
  const btnSplit = document.getElementById('viewBtnSplit');
  const btnList = document.getElementById('viewBtnList');
  const btnMap = document.getElementById('viewBtnMap');

  // Reset button active classes
  [btnSplit, btnList, btnMap].forEach(btn => {
    if (btn) {
      btn.classList.remove('bg-white', 'text-slate-900', 'shadow-sm');
      btn.classList.add('text-slate-600');
    }
  });

  if (mode === 'split') {
    btnSplit.classList.add('bg-white', 'text-slate-900', 'shadow-sm');
    splitCont.className = 'grid grid-cols-1 lg:grid-cols-12 gap-6 items-start';
    listCol.className = 'lg:col-span-7 space-y-4 block';
    mapCol.className = 'lg:col-span-5 sticky top-24 block';
  } else if (mode === 'list') {
    btnList.classList.add('bg-white', 'text-slate-900', 'shadow-sm');
    splitCont.className = 'block';
    listCol.className = 'w-full space-y-4 block';
    mapCol.className = 'hidden';
  } else if (mode === 'map') {
    btnMap.classList.add('bg-white', 'text-slate-900', 'shadow-sm');
    splitCont.className = 'block';
    listCol.className = 'hidden';
    mapCol.className = 'w-full block';
  }

  // Trigger leaflet resize
  setTimeout(() => {
    if (map) map.invalidateSize();
  }, 200);
}

// ----------------------------------------------------
// PROPERTY DETAIL MODAL (12 Legal Mandatory Items)
// ----------------------------------------------------
function openPropertyModal(propId) {
  const prop = PROPERTIES_DATA.find(p => p.id === propId);
  if (!prop) return;

  const modal = document.getElementById('propertyDetailModal');
  if (!modal) return;

  // Set Modal Data
  document.getElementById('detailTitle').textContent = prop.title;
  document.getElementById('detailBadge').textContent = prop.badge;
  document.getElementById('detailCategory').textContent = `${prop.category} · ${prop.transactionType}`;
  document.getElementById('detailPrice').textContent = prop.priceFormatted;
  document.getElementById('detailAreaPyeong').textContent = `전용 ${prop.exclusiveArea}㎡ (${prop.exclusiveAreaPyeong}평) / 공급 ${prop.supplyArea}㎡ (${prop.supplyAreaPyeong}평)`;
  document.getElementById('detailLocation').querySelector('span').textContent = `${prop.location} (상세주소 법정 보안)`;

  const gmapLink = document.getElementById('detailGoogleMapLink');
  if (gmapLink) {
    gmapLink.href = `https://maps.google.com/?q=${prop.lat},${prop.lng}`;
  }

  // Main Image & Thumbnails
  const mainImg = document.getElementById('detailMainImg');
  mainImg.src = prop.images[0];
  const thumbsContainer = document.getElementById('detailThumbnails');
  thumbsContainer.innerHTML = prop.images.map((img, idx) => `
    <button onclick="document.getElementById('detailMainImg').src='${img}'" class="w-12 h-9 rounded overflow-hidden border-2 border-white/80 hover:border-brand-gold shrink-0 transition">
      <img src="${img}" class="w-full h-full object-cover">
    </button>
  `).join('');

  // Tags
  document.getElementById('detailTags').innerHTML = prop.tags.map(t => `
    <span class="text-xs bg-amber-50 text-amber-800 border border-amber-200 px-2.5 py-1 rounded-md font-semibold">#${t}</span>
  `).join('');

  // 12 Legal Mandatory Disclosures
  document.getElementById('detailTypeVal').textContent = prop.category;
  document.getElementById('detailTransVal').textContent = prop.transactionType;
  document.getElementById('detailAddressVal').textContent = prop.addressMasked;
  document.getElementById('detailAreaVal').textContent = `전용 ${prop.exclusiveArea}㎡ / 공급 ${prop.supplyArea}㎡`;
  document.getElementById('detailFloorVal').textContent = prop.floor;
  document.getElementById('detailRoomsVal').textContent = `방 ${prop.rooms}개 / 욕실 ${prop.bathrooms}개`;
  document.getElementById('detailDirVal').textContent = prop.direction;
  document.getElementById('detailApprovalVal').textContent = prop.approvalDate;
  document.getElementById('detailParkingVal').textContent = prop.parking;
  document.getElementById('detailMoveInVal').textContent = prop.moveInDate;
  document.getElementById('detailMaintTotalVal').textContent = prop.maintenanceFee;
  document.getElementById('detailMaintDetailsVal').textContent = `[세부비목] ${prop.maintenanceDetails}`;

  // Description
  document.getElementById('detailDesc').textContent = prop.description;

  // Direct Call & SMS buttons
  const callBtn = document.getElementById('detailCallBtn');
  callBtn.href = `tel:${prop.agent.phone}`;

  const smsBtn = document.getElementById('detailSmsBtn');
  const smsBody = encodeURIComponent(`안녕하세요 대표님, 홈페이지에서 [${prop.title}] 매물 보고 문의드립니다. 통화 가능하신가요?`);
  smsBtn.href = `sms:${prop.agent.phone}?body=${smsBody}`;

  modal.classList.remove('hidden');
  document.body.style.overflow = 'hidden';

  if (window.lucide) lucide.createIcons();
}

function closePropertyModal() {
  const modal = document.getElementById('propertyDetailModal');
  if (modal) {
    modal.classList.add('hidden');
    document.body.style.overflow = '';
  }
}

function shareCurrentProperty() {
  navigator.clipboard.writeText(window.location.href).then(() => {
    showToast('매물 링크가 클립보드에 복사되었습니다.');
  }).catch(() => {
    showToast('매물 링크를 복사했습니다.');
  });
}

// ----------------------------------------------------
// FAVORITES (찜한 매물)
// ----------------------------------------------------
function toggleFavorite(e, propId) {
  e.stopPropagation();
  const idx = state.favorites.indexOf(propId);
  if (idx > -1) {
    state.favorites.splice(idx, 1);
    showToast('관심 매물에서 삭제되었습니다.');
  } else {
    state.favorites.push(propId);
    showToast('관심 매물에 추가되었습니다.');
  }
  localStorage.setItem('jinjuqueen_favs', JSON.stringify(state.favorites));
  updateFavBadge();
  renderProperties();
}

function updateFavBadge() {
  const badge = document.getElementById('favCountBadge');
  if (!badge) return;
  const count = state.favorites.length;
  badge.textContent = count;
  badge.classList.toggle('hidden', count === 0);
}

function openFavoritesModal() {
  const modal = document.getElementById('favoritesModal');
  const container = document.getElementById('favoritesListContainer');
  if (!modal || !container) return;

  const favProps = PROPERTIES_DATA.filter(p => state.favorites.includes(p.id));

  if (favProps.length === 0) {
    container.innerHTML = `
      <div class="text-center py-10 text-slate-500 text-xs">
        <i data-lucide="heart-off" class="w-8 h-8 mx-auto text-slate-300 mb-2"></i>
        아직 찜한 관심 매물이 없습니다.<br>마음에 드는 매물의 하트 아이콘을 눌러보세요.
      </div>
    `;
  } else {
    container.innerHTML = favProps.map(prop => `
      <div class="flex items-center gap-3 p-3 bg-slate-50 rounded-xl border border-slate-200">
        <img src="${prop.images[0]}" class="w-16 h-14 rounded-lg object-cover">
        <div class="flex-1 min-w-0">
          <div class="text-xs font-bold text-slate-900 truncate">${prop.title}</div>
          <div class="text-xs font-extrabold text-amber-600 mt-0.5">${prop.priceFormatted}</div>
          <div class="text-[11px] text-slate-400">${prop.floor} · 전용 ${prop.exclusiveArea}㎡</div>
        </div>
        <button onclick="openPropertyModal('${prop.id}'); closeFavoritesModal();" class="px-3 py-1.5 bg-brand-navy text-white text-xs font-bold rounded-lg shrink-0">
          보기
        </button>
      </div>
    `).join('');
  }

  modal.classList.remove('hidden');
  document.body.style.overflow = 'hidden';
  if (window.lucide) lucide.createIcons();
}

function closeFavoritesModal() {
  const modal = document.getElementById('favoritesModal');
  if (modal) {
    modal.classList.add('hidden');
    document.body.style.overflow = '';
  }
}

// ----------------------------------------------------
// MEDIA SECTION (YOUTUBE & NAVER BLOG)
// ----------------------------------------------------
function renderMediaSection() {
  const ytContainer = document.getElementById('youtubeVideosContainer');
  const blogContainer = document.getElementById('blogPostsContainer');

  if (ytContainer && typeof YOUTUBE_VIDEOS !== 'undefined') {
    ytContainer.innerHTML = YOUTUBE_VIDEOS.map(video => `
      <a href="${video.url}" target="_blank" rel="noopener noreferrer" 
         class="group bg-slate-800/90 hover:bg-slate-800 rounded-2xl p-3 border border-slate-700/80 hover:border-rose-500/60 transition flex flex-col sm:flex-row gap-3.5 block">
        <div class="relative sm:w-44 aspect-video rounded-xl overflow-hidden bg-slate-950 shrink-0">
          <img src="${video.thumbnail}" alt="${video.title}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300">
          <div class="absolute inset-0 bg-black/30 flex items-center justify-center group-hover:bg-black/10 transition">
            <div class="w-9 h-9 rounded-full bg-rose-600/90 text-white flex items-center justify-center shadow-lg group-hover:scale-110 transition">
              <i data-lucide="play" class="w-4 h-4 fill-white ml-0.5"></i>
            </div>
          </div>
          <span class="absolute bottom-1.5 right-1.5 bg-black/80 text-white text-[10px] font-bold px-1.5 py-0.5 rounded">
            ${video.duration}
          </span>
        </div>
        <div class="flex-1 flex flex-col justify-between py-1">
          <div>
            <h4 class="text-xs sm:text-sm font-bold text-white group-hover:text-rose-400 transition line-clamp-2 leading-snug">
              ${video.title}
            </h4>
            <p class="text-[11px] text-slate-400 mt-1 line-clamp-2 leading-relaxed">
              ${video.desc}
            </p>
          </div>
          <div class="flex items-center justify-between text-[10px] text-slate-400 mt-2">
            <span class="text-rose-400 font-semibold flex items-center gap-1">
              <i data-lucide="youtube" class="w-3 h-3"></i> 진주퀸 유튜브
            </span>
            <span>조회수 ${video.views}</span>
          </div>
        </div>
      </a>
    `).join('');
  }

  if (blogContainer && typeof BLOG_POSTS !== 'undefined') {
    blogContainer.innerHTML = BLOG_POSTS.map(post => `
      <a href="${post.url}" target="_blank" rel="noopener noreferrer" 
         class="group bg-slate-800/90 hover:bg-slate-800 rounded-2xl p-4 border border-slate-700/80 hover:border-emerald-500/60 transition flex flex-col justify-between block space-y-2">
        <div>
          <div class="flex items-center justify-between text-[11px] mb-1">
            <span class="text-emerald-400 font-bold bg-emerald-950/80 px-2 py-0.5 rounded border border-emerald-800/60">${post.category}</span>
            <span class="text-slate-400">${post.date}</span>
          </div>
          <h4 class="text-xs sm:text-sm font-bold text-white group-hover:text-emerald-400 transition line-clamp-1 leading-snug">
            ${post.title}
          </h4>
          <p class="text-[11px] text-slate-400 mt-1 line-clamp-2 leading-relaxed">
            ${post.desc}
          </p>
        </div>
        <div class="flex items-center justify-between text-[10px] text-slate-400 pt-2 border-t border-slate-700/40">
          <span class="text-slate-300 font-medium">네이버 블로그에서 전문 읽기</span>
          <i data-lucide="external-link" class="w-3 h-3 text-emerald-400"></i>
        </div>
      </a>
    `).join('');
  }
}

// ----------------------------------------------------
// REAL ESTATE NEWS BOARD (Live from GitHub Database /api/board)
// ----------------------------------------------------
let currentNewsCategory = 'ALL';
let liveNewsData = null;

async function loadLiveNews() {
  try {
    const res = await fetch('/api/board?t=' + Date.now());
    if (res.ok) {
      const data = await res.json();
      if (data.posts && Array.isArray(data.posts)) {
        liveNewsData = data.posts;
        renderNews();
        return;
      }
    }
    // Fallback to static data/board.json
    const fileRes = await fetch('data/board.json?t=' + Date.now());
    if (fileRes.ok) {
      liveNewsData = await fileRes.json();
      renderNews();
      return;
    }
  } catch (err) {
    // If running offline, fall back to initial NEWS_DATA
  }
  liveNewsData = typeof NEWS_DATA !== 'undefined' ? NEWS_DATA : [];
  renderNews();
}

function filterNews(cat) {
  currentNewsCategory = cat;
  document.querySelectorAll('#newsCategoryFilter .news-cat-btn').forEach(btn => {
    const isCur = btn.textContent.trim() === (cat === 'ALL' ? '전체' : cat);
    btn.classList.toggle('active', isCur);
    btn.classList.toggle('bg-white', isCur);
    btn.classList.toggle('text-brand-navy', isCur);
    btn.classList.toggle('shadow-sm', isCur);
  });
  renderNews();
}

function renderNews() {
  const container = document.getElementById('newsGrid');
  if (!container) return;

  const dataset = liveNewsData || (typeof NEWS_DATA !== 'undefined' ? NEWS_DATA : []);

  const list = dataset.filter(item => {
    if (currentNewsCategory !== 'ALL' && item.category !== currentNewsCategory) return false;
    return true;
  });

  if (list.length === 0) {
    container.innerHTML = `
      <div class="col-span-full bg-slate-50 rounded-2xl p-8 text-center text-slate-400 text-xs">
        해당 카테고리에 등록된 소식이 없습니다.
      </div>
    `;
    return;
  }

  container.innerHTML = list.map(item => `
    <article onclick="openNewsModal('${item.id}')" class="bg-slate-50 hover:bg-white rounded-2xl p-5 border border-slate-200 hover:border-amber-300 transition-all duration-200 cursor-pointer flex flex-col justify-between group shadow-sm hover:shadow-md">
      <div>
        <div class="flex items-center justify-between text-xs mb-3">
          <span class="font-bold text-amber-800 bg-amber-100 px-2.5 py-0.5 rounded-full text-[11px]">${item.category}</span>
          <span class="text-slate-400 text-[11px]">${item.date}</span>
        </div>
        <h4 class="font-bold text-slate-900 group-hover:text-amber-700 transition leading-snug text-sm sm:text-base mb-2 line-clamp-2">
          ${item.title}
        </h4>
        <p class="text-xs text-slate-500 leading-relaxed line-clamp-3">
          ${(item.summary || "").replace(/[#*`_~>\[\]]/g, "").trim()}
        </p>
      </div>
      <div class="pt-4 mt-4 border-t border-slate-200/60 flex items-center justify-between text-[11px] text-slate-400">
        <span class="flex items-center gap-1.5 font-bold text-slate-700">
          <img src="images/ceo-square.jpg?v=7" class="w-4 h-4 rounded-full object-cover border border-brand-gold/60">
          ${item.author || '황선숙 대표'}
        </span>
        <span class="text-amber-800 font-bold flex items-center gap-0.5 group-hover:translate-x-1 transition">
          칼럼 읽기 <i data-lucide="arrow-right" class="w-3 h-3 text-amber-600"></i>
        </span>
      </div>
    </article>
  `).join('');

  if (window.lucide) lucide.createIcons();
}

function openNewsModal(newsId) {
  const dataset = liveNewsData || (typeof NEWS_DATA !== 'undefined' ? NEWS_DATA : []);
  const item = dataset.find(n => n.id === newsId);
  if (!item) return;

  const modal = document.getElementById('newsModal');
  if (!modal) return;

  document.getElementById('newsModalCategory').textContent = item.category;
  document.getElementById('newsModalTitle').textContent = item.title;
  document.getElementById('newsModalDate').textContent = item.date;
  document.getElementById('newsModalAuthor').textContent = `${item.author || '황선숙 대표'} · 조회수 ${item.views || 0}`;
  
  const bodyEl = document.getElementById('newsModalBody');
  if (bodyEl) {
    if (window.marked && typeof window.marked.parse === 'function') {
      try {
        window.marked.setOptions({ breaks: true, gfm: true });
        bodyEl.innerHTML = window.marked.parse(item.content || '');
      } catch (err) {
        bodyEl.innerHTML = (item.content || '').replace(/\n/g, '<br>');
      }
    } else {
      bodyEl.innerHTML = (item.content || '').replace(/\n/g, '<br>');
    }
  }

  modal.classList.remove('hidden');
  document.body.style.overflow = 'hidden';
  if (window.lucide) lucide.createIcons();
}

function closeNewsModal() {
  const modal = document.getElementById('newsModal');
  if (modal) {
    modal.classList.add('hidden');
    document.body.style.overflow = '';
  }
}

// ----------------------------------------------------
// OWNER LISTING REQUEST FORM (집주인 매물 내놓기)
// ----------------------------------------------------
function openListingModal() {
  const modal = document.getElementById('listingModal');
  if (modal) {
    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
  }
}

function closeListingModal() {
  const modal = document.getElementById('listingModal');
  if (modal) {
    modal.classList.add('hidden');
    document.body.style.overflow = '';
  }
}

function handleListingSubmit(e) {
  e.preventDefault();
  const type = document.getElementById('reqPropType').value;
  const trans = document.getElementById('reqTransType').value;
  const price = document.getElementById('reqPrice').value;
  const address = document.getElementById('reqAddress').value;
  const name = document.getElementById('reqName').value;
  const phone = document.getElementById('reqPhone').value;

  closeListingModal();
  showToast(`[접수완료] ${name} 고객님의 ${address} (${type}/${trans}) 매물의뢰가 성공적으로 접수되었습니다. 황선숙 대표가 곧 연락드리겠습니다.`);
  
  // Reset form
  e.target.reset();
}

// ----------------------------------------------------
// TOAST NOTIFICATION UTILITY
// ----------------------------------------------------
function showToast(message) {
  const toast = document.getElementById('toastNotification');
  const msgEl = document.getElementById('toastMessage');
  if (!toast || !msgEl) return;

  msgEl.textContent = message;
  toast.classList.remove('opacity-0', 'translate-y-4', 'pointer-events-none');
  toast.classList.add('opacity-100', 'translate-y-0');

  setTimeout(() => {
    toast.classList.add('opacity-0', 'translate-y-4', 'pointer-events-none');
    toast.classList.remove('opacity-100', 'translate-y-0');
  }, 3500);
}



// ----------------------------------------------------
// TRANSACTION STATUS FILTER & SOLD MODAL (거래완료 시스템)
// ----------------------------------------------------
function toggleStatusFilter() {
  const btn = document.getElementById('statusFilterBtn');
  const dot = document.getElementById('statusDot');
  const txt = document.getElementById('statusFilterText');

  if (state.statusFilter === 'ALL') {
    state.statusFilter = 'ACTIVE';
    if (dot) dot.className = 'w-2 h-2 rounded-full bg-emerald-500';
    if (txt) txt.textContent = '진행중 매물만';
    if (btn) btn.className = 'px-3 py-1.5 rounded-lg bg-emerald-50 text-emerald-900 border border-emerald-300 hover:bg-emerald-100 transition flex items-center gap-1.5 font-bold';
    showToast('현재 진행 중인 실매물만 표시합니다.');
  } else if (state.statusFilter === 'ACTIVE') {
    state.statusFilter = 'SOLD';
    if (dot) dot.className = 'w-2 h-2 rounded-full bg-rose-500';
    if (txt) txt.textContent = '거래완료 실적만';
    if (btn) btn.className = 'px-3 py-1.5 rounded-lg bg-rose-50 text-rose-900 border border-rose-300 hover:bg-rose-100 transition flex items-center gap-1.5 font-bold';
    showToast('진주퀸에서 성사시킨 거래완료 매물 실적을 표시합니다.');
  } else {
    state.statusFilter = 'ALL';
    if (dot) dot.className = 'w-2 h-2 rounded-full bg-slate-400';
    if (txt) txt.textContent = '전체 매물 보기';
    if (btn) btn.className = 'px-3 py-1.5 rounded-lg bg-slate-100 text-slate-700 border border-slate-300 hover:bg-slate-200 transition flex items-center gap-1.5 font-bold';
    showToast('전체 매물(진행중 + 거래완료)을 표시합니다.');
  }

  updateFilterDisplay();
  renderProperties();
  updateMapMarkers();
}

function openSoldNoticeModal(propId) {
  const prop = PROPERTIES_DATA.find(p => p.id === propId);
  const modal = document.getElementById('soldNoticeModal');
  const titleEl = document.getElementById('soldModalTitle');

  if (titleEl && prop) {
    titleEl.textContent = prop.title;
  }
  if (modal) {
    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
    if (window.lucide) lucide.createIcons();
  }
}

function closeSoldNoticeModal() {
  const modal = document.getElementById('soldNoticeModal');
  if (modal) {
    modal.classList.add('hidden');
    document.body.style.overflow = '';
  }
}
