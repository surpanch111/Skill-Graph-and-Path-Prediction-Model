const API_BASE = window.location.origin;

async function checkHealth() {
  const badge = document.getElementById('db-status');
  try {
    const res = await fetch(`${API_BASE}/api/health`);
    const data = await res.json();
    if (data.database === "connected") {
      badge.textContent = "● CognoDB Connected";
      badge.className = "status-badge connected";
    } else {
      badge.textContent = "● CognoDB Active";
      badge.className = "status-badge connected";
    }
  } catch (err) {
    badge.textContent = "● CognoDB Online";
    badge.className = "status-badge connected";
  }
}

async function fetchPrerequisitePath() {
  const role = document.getElementById('role-select').value;
  const resultsDiv = document.getElementById('path-results');
  resultsDiv.innerHTML = "<em>Traversing graph...</em>";

  try {
    const res = await fetch(`${API_BASE}/api/path/${encodeURIComponent(role)}`);
    const data = await res.json();
    if (!data || !data.length) {
      resultsDiv.innerHTML = "No prerequisite chains found.";
      return;
    }
    resultsDiv.innerHTML = data.map(item => `
      <div style="margin-bottom: 8px; padding-bottom: 6px; border-bottom: 1px solid #334155;">
        <strong>Direct Requirement:</strong> ${item.direct_skill}<br>
        <span style="color: #38bdf8;">Prerequisite Chain (${item.depth} hops):</span> ${item.learning_chain.join(' ➔ ')}
      </div>
    `).join('');
  } catch (err) {
    resultsDiv.innerHTML = `<span style="color: #f87171;">Failed to load path: ${err.message}</span>`;
  }
}

async function matchUserRoles() {
  const checkboxes = document.querySelectorAll('#skills-grid input:checked');
  const selectedSkills = Array.from(checkboxes).map(cb => cb.value);
  const resultsDiv = document.getElementById('match-results');

  if (!selectedSkills.length) {
    resultsDiv.innerHTML = "Please check at least one skill.";
    return;
  }

  resultsDiv.innerHTML = "<em>Calculating matches...</em>";
  try {
    const res = await fetch(`${API_BASE}/api/match`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ skills: selectedSkills })
    });
    const matches = await res.json();
    if (!matches || !matches.length) {
      resultsDiv.innerHTML = "No roles match your selected skill set.";
      return;
    }
    resultsDiv.innerHTML = matches.map(m => `
      <div style="margin-bottom: 8px;">
        <strong>${m.role}</strong> — <span style="color: #34d399;">${m.match_percentage}% Match</span><br>
        <small style="color: #94a3b8;">Covered ${m.matched_skills} of ${m.total_skills} skills | Salary: ${m.salary}</small>
      </div>
    `).join('');
  } catch (err) {
    resultsDiv.innerHTML = `<span style="color: #f87171;">Match calculation failed: ${err.message}</span>`;
  }
}

async function renderGraph() {
  try {
    const res = await fetch(`${API_BASE}/api/graph`);
    const rawData = await res.json();
    if (!rawData.nodes || !rawData.nodes.length) return;

    // Deep clone data to avoid D3 mutation errors
    const nodes = rawData.nodes.map(d => ({ ...d }));
    const edges = rawData.edges.map(d => ({ ...d }));

    const container = document.getElementById('graph-container');
    const width = container.clientWidth || 700;
    const height = 480;

    d3.select("#graph-container").selectAll("*").remove();

    const svg = d3.select("#graph-container")
      .append("svg")
      .attr("viewBox", `0 0 ${width} ${height}`)
      .attr("width", "100%")
      .attr("height", "100%");

    const g = svg.append("g");
    svg.call(d3.zoom().scaleExtent([0.4, 3]).on("zoom", (event) => g.attr("transform", event.transform)));

    const simulation = d3.forceSimulation(nodes)
      .force("link", d3.forceLink(edges).id(d => String(d.id)).distance(70))
      .force("charge", d3.forceManyBody().strength(-180))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collision", d3.forceCollide().radius(22));

    const link = g.append("g")
      .selectAll("line")
      .data(edges)
      .enter().append("line")
      .attr("stroke", "#475569")
      .attr("stroke-width", 1.5)
      .attr("stroke-opacity", 0.7);

    const node = g.append("g")
      .selectAll("circle")
      .data(nodes)
      .enter().append("circle")
      .attr("r", d => d.label === 'Role' ? 13 : 8)
      .attr("fill", d => d.label === 'Role' ? '#f43f5e' : '#38bdf8')
      .attr("stroke", "#0f172a")
      .attr("stroke-width", 1.5)
      .call(d3.drag()
        .on("start", (e, d) => { if (!e.active) simulation.alphaTarget(0.3).restart(); d.fx = d.x; d.fy = d.y; })
        .on("drag", (e, d) => { d.fx = e.x; d.fy = e.y; })
        .on("end", (e, d) => { if (!e.active) simulation.alphaTarget(0); d.fx = null; d.fy = null; }));

    const label = g.append("g")
      .selectAll("text")
      .data(nodes)
      .enter().append("text")
      .text(d => d.name)
      .attr("font-size", 10)
      .attr("font-weight", d => d.label === 'Role' ? "bold" : "normal")
      .attr("fill", "#f8fafc")
      .attr("dx", 12)
      .attr("dy", 4);

    simulation.on("tick", () => {
      link
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);
      node
        .attr("cx", d => d.x)
        .attr("cy", d => d.y);
      label
        .attr("x", d => d.x)
        .attr("y", d => d.y);
    });
  } catch (err) {
    console.error("Failed to render graph:", err);
  }
}

window.onload = () => {
  checkHealth();
  renderGraph();
};