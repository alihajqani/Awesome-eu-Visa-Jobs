const companiesUrl = 'data/companies.json';
const grid = document.getElementById('company-grid');
const countLabel = document.getElementById('count-label');
const searchInput = document.getElementById('searchInput');
const visaFilter = document.getElementById('visaFilter');
const remoteFilter = document.getElementById('remoteFilter');

let allCompanies = [];

// 1. Fetch Data
async function fetchCompanies() {
    try {
        const response = await fetch(companiesUrl);
        allCompanies = await response.json();
        renderCompanies(allCompanies);
    } catch (error) {
        console.error('Error fetching data:', error);
        grid.innerHTML = '<p>Error loading data. Please try again later.</p>';
    }
}

// 2. Render Cards
function renderCompanies(companies) {
    grid.innerHTML = ''; // Clear existing
    countLabel.textContent = `Showing ${companies.length} companies`;

    if (companies.length === 0) {
        grid.innerHTML = '<p style="text-align:center; width:100%;">No companies match your filters.</p>';
        return;
    }

    companies.forEach(company => {
        const card = document.createElement('div');
        card.className = 'card';

        // Visa Badge Logic
        let visaClass = 'yes';
        let visaText = 'Visa Sponsored';
        if (company.visa_sponsorship === 'NO') {
            visaClass = 'no';
            visaText = 'No Visa';
        } else if (company.visa_sponsorship === 'SENIOR_ONLY') {
            visaClass = 'senior';
            visaText = 'Senior Visa';
        }

        // Location formatting
        const locationText = company.locations.map(l => `${l.city}, ${l.country} ${l.is_hq ? '(HQ)' : ''}`).join(' | ');

        // Tech Stack Tags
        const techHtml = company.tech_stack 
            ? company.tech_stack.map(tech => `<span class="tech-tag">${tech}</span>`).join('') 
            : '';

        card.innerHTML = `
            <div class="card-header">
                <h2>${company.name}</h2>
                <span class="badge ${visaClass}">${visaText}</span>
            </div>
            <div class="details">
                <p>📍 ${locationText}</p>
                <p>🏠 Remote: <strong>${company.remote_policy.replace('_', ' ')}</strong></p>
            </div>
            <div class="tech-stack">
                ${techHtml}
            </div>
            <a href="${company.careers_url}" target="_blank" class="apply-btn">View Careers →</a>
        `;
        grid.appendChild(card);
    });
}

// 3. Filter Logic
function filterData() {
    const query = searchInput.value.toLowerCase();
    const visaVal = visaFilter.value;
    const remoteVal = remoteFilter.value;

    const filtered = allCompanies.filter(company => {
        // Search Filter (Name, Tech, Location)
        const matchesSearch = 
            company.name.toLowerCase().includes(query) ||
            (company.tech_stack && company.tech_stack.some(t => t.toLowerCase().includes(query))) ||
            company.locations.some(l => l.country.toLowerCase().includes(query) || l.city.toLowerCase().includes(query));

        // Dropdown Filters
        const matchesVisa = visaVal === 'all' || company.visa_sponsorship === visaVal;
        const matchesRemote = remoteVal === 'all' || company.remote_policy === remoteVal;

        return matchesSearch && matchesVisa && matchesRemote;
    });

    renderCompanies(filtered);
}

// Event Listeners
searchInput.addEventListener('input', filterData);
visaFilter.addEventListener('change', filterData);
remoteFilter.addEventListener('change', filterData);

// Init
fetchCompanies();