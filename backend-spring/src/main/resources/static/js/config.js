/* ══════════════════════════════════════
   MASTER CONFIGURATION & 3 BANTS
══════════════════════════════════════ */
export const CATEGORIES = [
  {
    id: 'Workwear',
    name: 'İş Geyimi (Workwear)',
    code: 'Bant 1',
    color: '#4f80ff',
    iconSvg: '<svg viewBox="0 0 24 24"><path d="M20.38 3.46L16 2a4 4 0 0 1-8 0L3.62 3.46a2 2 0 0 0-1.34 2.23l.58 3.47a1 1 0 0 0 .99.84H6v10c0 1.1.9 2 2 2h8a2 2 0 0 0 2-2V10h2.15a1 1 0 0 0 .99-.84l.58-3.47a2 2 0 0 0-1.34-2.23z"/></svg>',
    products: [
      { id: 'kitel', name: 'Kitel / Tunic', easyRate: 150, hardRate: 100 },
      { id: 'salvar', name: 'Şalvar / Trousers', easyRate: 200, hardRate: 150 },
      { id: 'godekce', name: 'Gödəkcə / Jacket', easyRate: 120, hardRate: 80 },
      { id: 'polo', name: 'Polo T-Shirt', easyRate: 400, hardRate: 300 },
      { id: 'onluk', name: 'Önlük / Apron', easyRate: 1000, hardRate: 1000 },
      { id: 'papaq', name: 'Papaq / Cap', easyRate: 1000, hardRate: 500 }
    ],
    stages: [
      { id: 'dizayn', name: 'Dizayn & Sifariş' },
      { id: 'material', name: 'Material Təchizatı' },
      { id: 'kesim', name: 'Kəsim' },
      { id: 'tikis', name: 'Tikiş' },
      { id: 'hazir', name: 'Hazır Məhsul' }
    ]
  },
  {
    id: 'Underwear-boxer',
    name: 'Alt Geyim (Underwear)',
    code: 'Bant 2',
    color: '#34d399',
    iconSvg: '<svg viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="2"/><path d="M4 10h16M10 4v16"/></svg>',
    products: [
      { id: 'boxer', name: 'Boxer Şort', easyRate: 1200, hardRate: 1000 },
      { id: 'mayka', name: 'Mayka / Köynək', easyRate: 2400, hardRate: 2000 }
    ],
    stages: [
      { id: 'dizayn', name: 'Dizayn & Sifariş' },
      { id: 'material', name: 'Material Təchizatı' },
      { id: 'kesim', name: 'Kəsim' },
      { id: 'tikis', name: 'Tikiş' },
      { id: 'hazir', name: 'Hazır Məhsul' }
    ]
  },
  {
    id: 'Socks',
    name: 'Corab İstehsalatı (Socks)',
    code: 'Bant 3',
    color: '#38bdf8',
    iconSvg: '<svg viewBox="0 0 24 24"><path d="M8 2h8v8l4 6a4 4 0 0 1-4 4H8a4 4 0 0 1-4-4l4-6V2z"/></svg>',
    products: [
      { id: 'qis_corabi', name: 'Qış Corabı (Qalın)', easyRate: 300, hardRate: 200 },
      { id: 'idman_corabi', name: 'İkili İdman Corabı', easyRate: 400, hardRate: 300 },
      { id: 'qadin_corabi', name: 'Qadın Corabı', easyRate: 500, hardRate: 400 }
    ],
    stages: [
      { id: 'material', name: 'Material Təchizatı' },
      { id: 'horgu', name: 'Hörgü (Knitting)' },
      { id: 'tikis', name: 'Tikiş (Toe-closing)' },
      { id: 'forma', name: 'Forma (Boarding)' },
      { id: 'hazir', name: 'Paket & Anbar' }
    ]
  }
];
