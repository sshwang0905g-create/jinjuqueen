import re

# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add Status filter buttons in search bar
old_trans = '''          <!-- Transaction Type Pills -->
          <div class="flex items-center gap-1.5 text-xs font-semibold" id="transTypeGroup">
            <button onclick="setTransFilter('ALL')" class="trans-btn px-3 py-1.5 rounded-lg bg-slate-900 text-white transition">전체</button>
            <button onclick="setTransFilter('매매')" class="trans-btn px-3 py-1.5 rounded-lg bg-slate-100 text-slate-600 hover:bg-slate-200 transition">매매</button>
            <button onclick="setTransFilter('전세')" class="trans-btn px-3 py-1.5 rounded-lg bg-slate-100 text-slate-600 hover:bg-slate-200 transition">전세</button>
            <button onclick="setTransFilter('월세')" class="trans-btn px-3 py-1.5 rounded-lg bg-slate-100 text-slate-600 hover:bg-slate-200 transition">월세</button>
          </div>'''

new_trans = '''          <!-- Transaction Type Pills & Status Filter -->
          <div class="flex flex-wrap items-center gap-1.5 text-xs font-semibold" id="transTypeGroup">
            <button onclick="setTransFilter('ALL')" class="trans-btn px-3 py-1.5 rounded-lg bg-slate-900 text-white transition">전체</button>
            <button onclick="setTransFilter('매매')" class="trans-btn px-3 py-1.5 rounded-lg bg-slate-100 text-slate-600 hover:bg-slate-200 transition">매매</button>
            <button onclick="setTransFilter('전세')" class="trans-btn px-3 py-1.5 rounded-lg bg-slate-100 text-slate-600 hover:bg-slate-200 transition">전세</button>
            <button onclick="setTransFilter('월세')" class="trans-btn px-3 py-1.5 rounded-lg bg-slate-100 text-slate-600 hover:bg-slate-200 transition">월세</button>
            <span class="text-slate-300 mx-1">|</span>
            <!-- Status Filter Toggle -->
            <button id="statusFilterBtn" onclick="toggleStatusFilter()" class="px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 border border-slate-300 transition flex items-center gap-1.5 font-bold">
              <span id="statusDot" class="w-2 h-2 rounded-full bg-slate-400"></span>
              <span id="statusFilterText">전체 매물 보기</span>
            </button>
          </div>'''

# Also add Sold Notice Modal into index.html if not present
sold_modal_html = '''
  <!-- Sold Property Alert Modal (거래완료 안내 모달) -->
  <div id="soldNoticeModal" class="fixed inset-0 z-50 bg-slate-950/70 backdrop-blur-md flex items-center justify-center p-4 hidden">
    <div class="bg-white rounded-3xl p-6 sm:p-8 max-w-md w-full shadow-2xl border border-slate-200 text-center relative overflow-hidden animate-in fade-in zoom-in-95 duration-200">
      <div class="w-16 h-16 rounded-full bg-rose-50 border-2 border-rose-500/30 flex items-center justify-center mx-auto mb-4 shadow-inner">
        <i data-lucide="check-check" class="w-8 h-8 text-rose-600"></i>
      </div>
      <div class="inline-block px-3 py-1 rounded-full bg-rose-100 text-rose-800 text-xs font-extrabold mb-2 tracking-wide">
        계약 체결 완료 (거래완료)
      </div>
      <h3 id="soldModalTitle" class="text-lg font-bold text-slate-900 leading-snug mb-2">매물 제목</h3>
      <p class="text-xs text-slate-500 leading-relaxed mb-6">
        본 매물은 고객님의 성원에 힘입어 <strong class="text-slate-800">성공적으로 계약이 체결</strong>되었습니다.<br>
        공인중개사법에 따라 거래 완료된 매물의 세부 정보 열람은 제한됩니다.
      </p>

      <div class="bg-amber-50 rounded-2xl p-4 border border-amber-200 text-left mb-6 space-y-2">
        <div class="text-xs font-bold text-amber-950 flex items-center gap-1.5">
          <i data-lucide="sparkles" class="w-4 h-4 text-amber-600"></i>
          <span>유사한 추천 실매물을 찾으시나요?</span>
        </div>
        <p class="text-[11px] text-amber-900/80 leading-relaxed">
          동일 단지 및 충무공동 혁신도시 내 아직 광고에 나오지 않은 <strong>비공개 신규 매물</strong>을 황선숙 대표가 1:1 맞춤으로 직접 찾아드립니다.
        </p>
      </div>

      <div class="grid grid-cols-2 gap-3">
        <button onclick="closeSoldNoticeModal()" class="py-3 rounded-xl border border-slate-300 text-slate-700 hover:bg-slate-100 text-xs font-bold transition">
          닫기
        </button>
        <a href="tel:010-4670-7248" class="py-3 rounded-xl bg-brand-navy hover:bg-slate-800 text-white text-xs font-bold transition shadow flex items-center justify-center gap-1.5">
          <i data-lucide="phone-call" class="w-3.5 h-3.5 text-brand-gold"></i>
          <span>유사 매물 문의</span>
        </a>
      </div>
    </div>
  </div>
'''

html_norm = html.replace('\r\n', '\n')
old_trans_norm = old_trans.replace('\r\n', '\n')
new_trans_norm = new_trans.replace('\r\n', '\n')

if old_trans_norm in html_norm:
    html_norm = html_norm.replace(old_trans_norm, new_trans_norm)
    print("Replaced transaction buttons with Status toggle in index.html")

if 'id="soldNoticeModal"' not in html_norm:
    # insert before </body>
    html_norm = html_norm.replace('</body>', sold_modal_html + '\n</body>')
    print("Inserted soldNoticeModal into index.html")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_norm)

print("Updated index.html successfully!")

