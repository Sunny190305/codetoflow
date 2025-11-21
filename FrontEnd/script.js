// Helper script to update API endpoint
// Replace YOUR_BACKEND_URL with your actual Render backend URL

const API_URL = window.location.hostname === 'localhost'
  ? 'http://127.0.0.1:5000'
  : 'https://codetoflow-backend.onrender.com'; // Production backend URL

// Initialize Lucide Icons
lucide.createIcons();

// Theme Toggle Logic
const themeToggle = document.getElementById('themeToggle');
const html = document.documentElement;

// Check for saved theme preference
if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
  html.classList.add('dark');
} else {
  html.classList.remove('dark');
}

themeToggle.addEventListener('click', () => {
  html.classList.toggle('dark');
  if (html.classList.contains('dark')) {
    localStorage.theme = 'dark';
  } else {
    localStorage.theme = 'light';
  }
});

// Custom Cursor Logic
const cursor = document.getElementById('cursor');
const cursorDot = document.getElementById('cursor-dot');

document.addEventListener('mousemove', (e) => {
  cursor.style.transform = `translate(${e.clientX - 12}px, ${e.clientY - 12}px)`;
  cursorDot.style.transform = `translate(${e.clientX - 4}px, ${e.clientY - 4}px)`;
});

// Hover effects for cursor
const hoverables = document.querySelectorAll('button, select, textarea, a');

hoverables.forEach(el => {
  el.addEventListener('mouseenter', () => {
    cursor.classList.add('scale-150', 'border-secondary');
    cursor.classList.remove('border-primary');
  });
  el.addEventListener('mouseleave', () => {
    cursor.classList.remove('scale-150', 'border-secondary');
    cursor.classList.add('border-primary');
  });
});

// Mermaid Initialization
mermaid.initialize({
  startOnLoad: false,
  theme: html.classList.contains('dark') ? 'dark' : 'default',
  securityLevel: 'loose',
});

// Generate Flowchart
document.getElementById("generateBtn").addEventListener("click", async () => {
  const code = document.getElementById("codeInput").value;
  const language = document.getElementById("languageSelect").value;
  const generateBtn = document.getElementById("generateBtn");

  // Loading State
  const originalBtnText = generateBtn.innerHTML;
  generateBtn.innerHTML = '<i data-lucide="loader-2" class="w-5 h-5 animate-spin"></i> Generating...';
  lucide.createIcons();
  generateBtn.disabled = true;

  try {
    const response = await fetch(`${API_URL}/parse`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ code, language }),
    });

    const data = await response.json();

    if (data.error) {
      document.getElementById("flowchart").innerHTML = `
        <div class="text-red-500 flex flex-col items-center">
          <i data-lucide="alert-circle" class="w-8 h-8 mb-2"></i>
          <p>Error: ${data.error}</p>
        </div>
      `;
      lucide.createIcons();
      return;
    }

    const { nodes, edges } = data;

    let mermaidCode = "graph LR;\n";
    nodes.forEach((node) => {
      const label = node.label.replace(/"/g, "");
      mermaidCode += `${node.id}["${label}"]\n`;
    });

    edges.forEach((edge) => {
      mermaidCode += `${edge.from} --> ${edge.to}\n`;
    });

    const chartContainer = document.getElementById("flowchart");
    chartContainer.innerHTML = ""; // Clear previous chart

    const mermaidDiv = document.createElement("div");
    mermaidDiv.className = "mermaid w-full h-full flex justify-center items-center";
    mermaidDiv.textContent = mermaidCode;

    chartContainer.appendChild(mermaidDiv);

    // Re-initialize mermaid with current theme
    mermaid.initialize({
      startOnLoad: false,
      theme: html.classList.contains('dark') ? 'dark' : 'default',
    });

    await mermaid.init(undefined, mermaidDiv);

  } catch (error) {
    console.error(error);
    document.getElementById("flowchart").innerHTML = `
      <div class="text-red-500 flex flex-col items-center">
        <i data-lucide="alert-triangle" class="w-8 h-8 mb-2"></i>
        <p>Failed to connect to server.</p>
      </div>
    `;
    lucide.createIcons();
  } finally {
    generateBtn.innerHTML = originalBtnText;
    generateBtn.disabled = false;
    lucide.createIcons();
  }
});

// Export as PNG
document.getElementById("exportBtn").addEventListener("click", () => {
  const chart = document.querySelector("#flowchart .mermaid");

  if (!chart) {
    alert("Please generate a flowchart first.");
    return;
  }

  html2canvas(chart, {
    backgroundColor: html.classList.contains('dark') ? '#1e293b' : '#ffffff'
  }).then((canvas) => {
    const link = document.createElement("a");
    link.download = "flowchart.png";
    link.href = canvas.toDataURL("image/png");
    link.click();
  });
});
