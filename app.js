// Application State
const appState = {
    currentPage: 'transliterasi',
    manuscriptPage: 1,
    totalPages: 20,
    rdfData: []
};

// RDF Data - Sample data from the TTL file
const rdfData = [
    {
        uri: "http://example.org/jawa#kalimat_1",
        latin: "Ikanang dhanurdhara kabéh,",
        terjemahan: "Semua pemanah bersatu dalam baktinya."
    },
    {
        uri: "http://example.org/jawa#kalimat_2",
        latin: "Kapwa ya bhakti ri sira pranata matwang,",
        terjemahan: "Mereka semua setia kepada pemimpin mereka."
    },
    {
        uri: "http://example.org/jawa#kalimat_3",
        latin: "Kadi mawwata yasa lana,",
        terjemahan: "Seperti cahaya kemuliaan."
    },
    {
        uri: "http://example.org/jawa#kalimat_4",
        latin: "Rupanyanagong ta kirtti nira.",
        terjemahan: "Wajahnya mengagungkan kehormatannya."
    },
    {
        uri: "http://example.org/jawa#kalimat_5",
        latin: "Prajurit-prajurité sané masanjata panah sami,",
        terjemahan: "Para prajurit semuanya bersenjata panah."
    },
    {
        uri: "http://example.org/jawa#kalimat_6",
        latin: "Maka sami bhakti ring Ida nungkul ngalap kasor,",
        terjemahan: "Mereka berbakti kepada pemimpin mereka, tunduk dalam ketulusan."
    },
    {
        uri: "http://example.org/jawa#kalimat_7",
        latin: "Sekadi pacang ngawewehin kawibuhan Ida satata,",
        terjemahan: "Seolah senantiasa menambah kebesarannya."
    },
    {
        uri: "http://example.org/jawa#kalimat_8",
        latin: "Pakantenannya agung wantah kertin Idane.",
        terjemahan: "Kebesarannya sungguh agung dalam kehormatan."
    }
];

// DOM Elements
const elements = {
    sidebar: document.getElementById('sidebar'),
    sidebarToggle: document.getElementById('sidebarToggle'),
    navItems: document.querySelectorAll('.nav-item'),
    pages: document.querySelectorAll('.page'),
    
    // Manuscript viewer elements
    pageTitle: document.getElementById('page-title'),
    manuscriptImage: document.getElementById('manuscript-image'),
    imagePlaceholder: document.getElementById('image-placeholder'),
    prevPageBtn: document.getElementById('prev-page'),
    nextPageBtn: document.getElementById('next-page'),
    pageInput: document.getElementById('page-input'),
    transliterationContent: document.getElementById('transliteration-content'),
    
    // Search elements
    searchInput: document.getElementById('search-input'),
    searchBtn: document.getElementById('search-btn'),
    searchResults: document.getElementById('search-results')
};

// Initialize Application
function initApp() {
    setupEventListeners();
    updateManuscriptPage();
    showPage('transliterasi');
}

// Event Listeners
function setupEventListeners() {
    // Sidebar toggle for mobile
    elements.sidebarToggle.addEventListener('click', toggleSidebar);
    
    // Navigation items
    elements.navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            const page = e.currentTarget.dataset.page;
            showPage(page);
        });
    });
    
    // Manuscript navigation
    elements.prevPageBtn.addEventListener('click', () => navigateManuscript(-1));
    elements.nextPageBtn.addEventListener('click', () => navigateManuscript(1));
    elements.pageInput.addEventListener('change', (e) => {
        const page = parseInt(e.target.value);
        if (page >= 1 && page <= appState.totalPages) {
            appState.manuscriptPage = page;
            updateManuscriptPage();
        }
    });
    
    // Search functionality
    elements.searchBtn.addEventListener('click', performSearch);
    elements.searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            performSearch();
        }
    });
    
    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', (e) => {
        if (window.innerWidth <= 768 && 
            !elements.sidebar.contains(e.target) && 
            !elements.sidebarToggle.contains(e.target) &&
            elements.sidebar.classList.contains('open')) {
            toggleSidebar();
        }
    });
    
    // Handle window resize
    window.addEventListener('resize', () => {
        if (window.innerWidth > 768) {
            elements.sidebar.classList.remove('open');
        }
    });
}

// Navigation Functions
function toggleSidebar() {
    elements.sidebar.classList.toggle('open');
}

function showPage(pageId) {
    // Update navigation state
    elements.navItems.forEach(item => {
        item.classList.remove('active');
        if (item.dataset.page === pageId) {
            item.classList.add('active');
        }
    });
    
    // Show selected page
    elements.pages.forEach(page => {
        page.classList.remove('active');
        if (page.id === `${pageId}-page`) {
            page.classList.add('active');
        }
    });
    
    appState.currentPage = pageId;
    
    // Close sidebar on mobile after navigation
    if (window.innerWidth <= 768) {
        elements.sidebar.classList.remove('open');
    }
}

// Manuscript Navigation
function navigateManuscript(direction) {
    const newPage = appState.manuscriptPage + direction;
    if (newPage >= 1 && newPage <= appState.totalPages) {
        appState.manuscriptPage = newPage;
        updateManuscriptPage();
    }
}

function updateManuscriptPage() {
    const page = appState.manuscriptPage;
    
    // Update page title
    elements.pageTitle.textContent = `Tampilan Naskah Halaman ${page}`;
    
    // Update image
    const imagePath = `images/page_${page}.png`;
    elements.manuscriptImage.src = imagePath;
    elements.manuscriptImage.alt = `Halaman naskah ${page}`;
    
    // Handle image load error
    elements.manuscriptImage.onerror = () => {
        elements.manuscriptImage.style.display = 'none';
        elements.imagePlaceholder.style.display = 'block';
        elements.imagePlaceholder.innerHTML = `<p>Gambar halaman ${page} tidak tersedia</p>`;
    };
    
    elements.manuscriptImage.onload = () => {
        elements.manuscriptImage.style.display = 'block';
        elements.imagePlaceholder.style.display = 'none';
    };
    
    // Update pagination controls
    elements.prevPageBtn.disabled = page === 1;
    elements.nextPageBtn.disabled = page === appState.totalPages;
    elements.pageInput.value = page;
    
    // Update transliteration content
    updateTransliterationContent(page);
}

function updateTransliterationContent(page) {
    if (page === 3) {
        // Show RDF data for page 3
        const content = rdfData.map(item => `
            <div class="transliteration-item">
                <div class="latin"><strong>Latin:</strong> <em>${item.latin}</em></div>
                <div class="translation"><strong>Terjemahan:</strong> ${item.terjemahan}</div>
            </div>
        `).join('');
        
        elements.transliterationContent.innerHTML = content;
    } else {
        elements.transliterationContent.innerHTML = `
            <div class="content-message">
                <p>Data transliterasi untuk halaman ${page} belum tersedia.</p>
                <p>Silakan pilih halaman 3 untuk melihat contoh data yang tersedia.</p>
            </div>
        `;
    }
}

// Search Functionality
function performSearch() {
    const query = elements.searchInput.value.trim().toLowerCase();
    
    if (!query) {
        elements.searchResults.innerHTML = `
            <div class="search-placeholder">
                <p>Masukkan kata kunci untuk memulai pencarian</p>
            </div>
        `;
        return;
    }
    
    // Filter RDF data based on search query
    const results = rdfData.filter(item => 
        item.latin.toLowerCase().includes(query) || 
        item.terjemahan.toLowerCase().includes(query)
    );
    
    if (results.length === 0) {
        elements.searchResults.innerHTML = `
            <div class="search-placeholder">
                <p>Tidak ada hasil ditemukan untuk "${query}"</p>
                <p>Coba gunakan kata kunci yang berbeda</p>
            </div>
        `;
        return;
    }
    
    // Display search results with highlighting
    const resultsHTML = results.map(item => {
        const highlightedLatin = highlightText(item.latin, query);
        const highlightedTranslation = highlightText(item.terjemahan, query);
        
        return `
            <div class="search-result">
                <div class="latin"><strong>Latin:</strong> <em>${highlightedLatin}</em></div>
                <div class="translation"><strong>Terjemahan:</strong> ${highlightedTranslation}</div>
            </div>
        `;
    }).join('');
    
    elements.searchResults.innerHTML = `
        <div style="margin-bottom: 1rem;">
            <p><strong>${results.length}</strong> hasil ditemukan untuk "<strong>${query}</strong>"</p>
        </div>
        ${resultsHTML}
    `;
}

function highlightText(text, query) {
    if (!query) return text;
    
    const regex = new RegExp(`(${escapeRegExp(query)})`, 'gi');
    return text.replace(regex, '<span class="highlight">$1</span>');
}

function escapeRegExp(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

// Utility Functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', initApp);

// Add keyboard navigation support
document.addEventListener('keydown', (e) => {
    // Only handle keyboard navigation when not typing in inputs
    if (e.target.tagName === 'INPUT') return;
    
    switch(e.key) {
        case 'ArrowLeft':
            if (appState.currentPage === 'transliterasi' && appState.manuscriptPage > 1) {
                navigateManuscript(-1);
                e.preventDefault();
            }
            break;
        case 'ArrowRight':
            if (appState.currentPage === 'transliterasi' && appState.manuscriptPage < appState.totalPages) {
                navigateManuscript(1);
                e.preventDefault();
            }
            break;
        case '/':
            if (appState.currentPage === 'pencarian') {
                elements.searchInput.focus();
                e.preventDefault();
            }
            break;
    }
});