const services = [
    { name: 'ubs', port: 5000 },
    { name: 'das', port: 8000 },
    { name: 'dis', port: 8001 }
];

async function checkHealth() {
    for (const svc of services) {
        const indicator = document.querySelector(`#card-${svc.name} .indicator`);
        try {
            // This works because Nginx proxies /api/svc to the correct backend
            const response = await fetch(`/api/${svc.name}/health`);
            if (response.ok) {
                indicator.textContent = "● Online";
                indicator.className = "indicator online";
            } else {
                throw new Error();
            }
        } catch (error) {
            indicator.textContent = "○ Offline";
            indicator.className = "indicator offline";
        }
    }
}

function triggerIngest(source) {
    fetch(`/api/dis/ingest/${source}`)
        .then(res => res.json())
        .then(data => alert(`Ingest Started: ${data.message}`))
        .catch(err => console.error("Ingest failed", err));
}

// Initial check and set interval
checkHealth();
setInterval(checkHealth, 10000);