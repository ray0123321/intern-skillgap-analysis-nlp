// Main Application JavaScript - SkillGap.AI
document.addEventListener('DOMContentLoaded', () => {
  let appData = null;
  let selectedIntern = null;

  // Chart instances
  let overviewClusterChart = null;
  let overviewDeficienciesChart = null;
  let clustersScatterChart = null;
  let internRadarChart = null;
  let playgroundRadarChart = null;

  // Color Palette for Clusters
  const clusterColors = [
    { bg: 'rgba(99, 102, 241, 0.7)', border: '#6366f1', glow: 'rgba(99, 102, 241, 0.2)' },
    { bg: 'rgba(16, 185, 129, 0.7)', border: '#10b981', glow: 'rgba(16, 185, 129, 0.2)' },
    { bg: 'rgba(6, 182, 212, 0.7)', border: '#06b6d4', glow: 'rgba(6, 182, 212, 0.2)' },
    { bg: 'rgba(245, 158, 11, 0.7)', border: '#f59e0b', glow: 'rgba(245, 158, 11, 0.2)' },
    { bg: 'rgba(239, 68, 68, 0.7)', border: '#ef4444', glow: 'rgba(239, 68, 68, 0.2)' },
    { bg: 'rgba(139, 92, 246, 0.7)', border: '#8b5cf6', glow: 'rgba(139, 92, 246, 0.2)' }
  ];

  // 1. Fetch Analysis Results JSON
  fetchData();

  async function fetchData() {
    try {
      const response = await fetch('data/analysis_results.json');
      if (!response.ok) throw new Error('Network response was not ok');
      appData = await response.json();
      console.log('App Data Loaded:', appData);
      
      initApp();
    } catch (err) {
      console.error('Failed to load analysis data:', err);
    }
  }

  function initApp() {
    setupNavigation();
    renderGlobalStats();
    renderOverviewCharts();
    renderClusterCards();
    renderClustersScatterPlot();
    populateClusterDeepDive();
    initInternExplorer();
    setupPlayground();
    setupExport();
  }

  // 2. Tab Navigation Setup
  function setupNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    const tabPages = document.querySelectorAll('.tab-page');

    const headers = {
      overview: { title: 'Executive Skill Gap Overview', sub: 'AI-powered analytics aligning intern skillsets with real-time industry demands.' },
      clusters: { title: 'Industry Job Clusters (2D PCA Projection)', sub: 'Visualization of latent industry role groupings via TF-IDF vectorization and K-Means.' },
      interns: { title: 'Intern Skill Gap Explorer', sub: 'Inspect individual intern proficiency radar charts against target cluster benchmarks.' },
      roadmaps: { title: 'Personalized Training Roadmaps', sub: 'Targeted course modules, milestone steps, and hands-on capstone projects.' },
      playground: { title: 'Live Resume & Skill Evaluator', sub: 'Test custom candidate resume profiles or skill lists in real-time.' }
    };

    navItems.forEach(item => {
      item.addEventListener('click', (e) => {
        e.preventDefault();
        const tab = item.getAttribute('data-tab');

        navItems.forEach(i => i.classList.remove('active'));
        tabPages.forEach(p => p.classList.remove('active'));

        item.classList.add('active');
        document.getElementById(`tab-${tab}`).classList.add('active');

        if (headers[tab]) {
          document.getElementById('page-title').innerText = headers[tab].title;
          document.getElementById('page-subtitle').innerText = headers[tab].sub;
        }

        // Resize charts on tab visibility change
        if (tab === 'clusters' && clustersScatterChart) clustersScatterChart.resize();
        if (tab === 'interns' && internRadarChart) internRadarChart.resize();
        if (tab === 'overview') {
          if (overviewClusterChart) overviewClusterChart.resize();
          if (overviewDeficienciesChart) overviewDeficienciesChart.resize();
        }
      });
    });
  }

  // 3. Global Stats Rendering
  function renderGlobalStats() {
    const stats = appData.global_stats;
    document.getElementById('stat-jobs').innerText = stats.total_jobs;
    document.getElementById('stat-interns').innerText = stats.total_interns;
    document.getElementById('stat-readiness').innerText = `${stats.avg_readiness_score}%`;
    document.getElementById('model-silhouette-tag').innerText = `Silhouette: ${stats.silhouette_score}`;

    if (stats.top_missing_skills && stats.top_missing_skills.length > 0) {
      const topGap = stats.top_missing_skills[0];
      document.getElementById('stat-top-gap').innerText = topGap.skill;
      document.getElementById('stat-top-gap-sub').innerText = `${topGap.affected_interns}/${stats.total_interns} Interns Deficient`;
    }
  }

  // 4. Overview Charts
  function renderOverviewCharts() {
    const clusters = appData.clusters;
    const labels = clusters.map(c => c.name);
    const counts = clusters.map(c => c.job_count);

    // Cluster Distribution Doughnut Chart
    const ctxCluster = document.getElementById('overviewClusterChart').getContext('2d');
    if (overviewClusterChart) overviewClusterChart.destroy();
    overviewClusterChart = new Chart(ctxCluster, {
      type: 'doughnut',
      data: {
        labels: labels,
        datasets: [{
          data: counts,
          backgroundColor: clusterColors.map(c => c.bg),
          borderColor: clusterColors.map(c => c.border),
          borderWidth: 1.5
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'right', labels: { color: '#94a3b8', font: { family: 'Inter', size: 12 } } }
        }
      }
    });

    // Top Deficiencies Bar Chart
    const topGaps = appData.global_stats.top_missing_skills;
    const gapLabels = topGaps.map(g => g.skill);
    const gapCounts = topGaps.map(g => g.affected_interns);

    const ctxGap = document.getElementById('overviewDeficienciesChart').getContext('2d');
    if (overviewDeficienciesChart) overviewDeficienciesChart.destroy();
    overviewDeficienciesChart = new Chart(ctxGap, {
      type: 'bar',
      data: {
        labels: gapLabels,
        datasets: [{
          label: 'Affected Interns',
          data: gapCounts,
          backgroundColor: 'rgba(239, 68, 68, 0.65)',
          borderColor: '#ef4444',
          borderWidth: 1.5,
          borderRadius: 6
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false }
        },
        scales: {
          x: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' } },
          y: { ticks: { color: '#f8fafc', font: { weight: '600' } }, grid: { display: false } }
        }
      }
    });
  }

  // 5. Cluster Cards List
  function renderClusterCards() {
    const container = document.getElementById('clusters-cards-grid');
    container.innerHTML = '';

    appData.clusters.forEach((c, idx) => {
      const colTheme = clusterColors[idx % clusterColors.length];
      const tags = c.top_keywords.map(kw => `<span class="kw-tag">${kw.word}</span>`).join('');

      const cardHtml = `
        <div class="cluster-card" style="border-top: 3px solid ${colTheme.border}">
          <div class="cluster-card-header">
            <span class="cluster-name">${c.name}</span>
            <span class="cluster-count">${c.job_count} Jobs</span>
          </div>
          <div class="keyword-tags">
            ${tags}
          </div>
        </div>
      `;
      container.insertAdjacentHTML('beforeend', cardHtml);
    });
  }

  // 6. 2D Scatter Plot
  function renderClustersScatterPlot() {
    const datasets = [];

    appData.clusters.forEach((c, idx) => {
      const col = clusterColors[idx % clusterColors.length];
      const points = appData.job_points_2d.filter(p => p.cluster_id === c.cluster_id);

      datasets.push({
        label: c.name,
        data: points.map(p => ({ x: p.x, y: p.y, title: p.title, job_id: p.job_id })),
        backgroundColor: col.bg,
        borderColor: col.border,
        borderWidth: 1,
        pointRadius: 6,
        pointHoverRadius: 9
      });

      // Centroid point marker
      datasets.push({
        label: `${c.name} Centroid`,
        data: [{ x: c.centroid_x, y: c.centroid_y, title: `${c.name} Centroid`, job_id: `CENTROID_${c.cluster_id}` }],
        backgroundColor: '#ffffff',
        borderColor: col.border,
        borderWidth: 3,
        pointRadius: 12,
        pointStyle: 'rectRot'
      });
    });

    const ctx = document.getElementById('clustersScatterChart').getContext('2d');
    if (clustersScatterChart) clustersScatterChart.destroy();

    clustersScatterChart = new Chart(ctx, {
      type: 'scatter',
      data: { datasets: datasets },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
            labels: {
              color: '#94a3b8',
              font: { family: 'Inter', size: 11 },
              filter: item => !item.text.includes('Centroid')
            }
          },
          tooltip: {
            callbacks: {
              label: (context) => {
                const pt = context.raw;
                return `${pt.title} (X: ${pt.x}, Y: ${pt.y})`;
              }
            }
          }
        },
        scales: {
          x: {
            title: { display: true, text: 'PCA Component 1 (TF-IDF Variance)', color: '#64748b' },
            ticks: { color: '#94a3b8' },
            grid: { color: 'rgba(255,255,255,0.05)' }
          },
          y: {
            title: { display: true, text: 'PCA Component 2 (TF-IDF Variance)', color: '#64748b' },
            ticks: { color: '#94a3b8' },
            grid: { color: 'rgba(255,255,255,0.05)' }
          }
        }
      }
    });
  }

  // 7. Cluster Deep Dive Dropdown
  function populateClusterDeepDive() {
    const select = document.getElementById('select-cluster-deepdive');
    select.innerHTML = '';

    appData.clusters.forEach(c => {
      const opt = document.createElement('option');
      opt.value = c.cluster_id;
      opt.innerText = c.name;
      select.appendChild(opt);
    });

    select.addEventListener('change', (e) => {
      renderClusterDetail(parseInt(e.target.value));
    });

    if (appData.clusters.length > 0) {
      renderClusterDetail(appData.clusters[0].cluster_id);
    }
  }

  function renderClusterDetail(clusterId) {
    const c = appData.clusters.find(item => item.cluster_id === clusterId);
    if (!c) return;

    const box = document.getElementById('cluster-detail-box');
    const kwRows = c.top_keywords.map(kw => `
      <div style="display:flex; justify-content:space-between; margin-bottom:0.4rem; font-size:0.85rem;">
        <span style="color:#f8fafc; font-weight:600;">${kw.word}</span>
        <span style="color:#6366f1; font-family:'JetBrains Mono';">${kw.tfidf_weight}</span>
      </div>
    `).join('');

    box.innerHTML = `
      <h4 style="color:#a5b4fc; font-size:1.05rem; margin-bottom:0.5rem;">${c.name}</h4>
      <p style="font-size:0.8rem; color:#94a3b8; margin-bottom:1rem;">Total Jobs: ${c.job_count} | Centroid 2D: (${c.centroid_x}, ${c.centroid_y})</p>
      <h5 style="font-size:0.85rem; color:#64748b; margin-bottom:0.6rem; text-transform:uppercase;">Top TF-IDF Keyword Weights</h5>
      <div style="background:var(--bg-input); padding:0.85rem; border-radius:var(--radius-sm);">
        ${kwRows}
      </div>
    `;
  }

  // 8. Intern Gap Explorer
  function initInternExplorer() {
    const searchInput = document.getElementById('intern-search-input');
    const domainFilter = document.getElementById('intern-domain-filter');

    // Populate Domain Filter Options
    const domains = [...new Set(appData.interns.map(i => i.target_domain))];
    domains.forEach(d => {
      const opt = document.createElement('option');
      opt.value = d;
      opt.innerText = d;
      domainFilter.appendChild(opt);
    });

    searchInput.addEventListener('input', filterInternList);
    domainFilter.addEventListener('change', filterInternList);

    renderInternList(appData.interns);

    if (appData.interns.length > 0) {
      selectIntern(appData.interns[0]);
    }
  }

  function filterInternList() {
    const q = document.getElementById('intern-search-input').value.toLowerCase();
    const domain = document.getElementById('intern-domain-filter').value;

    const filtered = appData.interns.filter(i => {
      const matchesSearch = i.name.toLowerCase().includes(q) || 
                            i.target_domain.toLowerCase().includes(q) ||
                            Object.keys(i.current_skills).some(s => s.toLowerCase().includes(q));
      const matchesDomain = (domain === 'ALL') || (i.target_domain === domain);
      return matchesSearch && matchesDomain;
    });

    renderInternList(filtered);
  }

  function renderInternList(list) {
    const container = document.getElementById('intern-list-container');
    container.innerHTML = '';

    if (list.length === 0) {
      container.innerHTML = '<p style="color:#64748b; font-size:0.85rem; padding:1rem;">No interns found.</p>';
      return;
    }

    list.forEach(i => {
      const scoreClass = i.readiness_score >= 60 ? 'high' : (i.readiness_score >= 35 ? 'med' : 'low');
      const isSelected = selectedIntern && selectedIntern.intern_id === i.intern_id;

      const itemHtml = `
        <div class="intern-item ${isSelected ? 'active' : ''}" data-id="${i.intern_id}">
          <div class="intern-item-info">
            <h4>${i.name}</h4>
            <span>${i.target_domain}</span>
          </div>
          <span class="score-badge ${scoreClass}">${i.readiness_score}%</span>
        </div>
      `;
      container.insertAdjacentHTML('beforeend', itemHtml);
    });

    // Add click event listeners
    container.querySelectorAll('.intern-item').forEach(el => {
      el.addEventListener('click', () => {
        const id = el.getAttribute('data-id');
        const internObj = appData.interns.find(item => item.intern_id === id);
        if (internObj) {
          container.querySelectorAll('.intern-item').forEach(x => x.classList.remove('active'));
          el.classList.add('active');
          selectIntern(internObj);
        }
      });
    });
  }

  function selectIntern(intern) {
    selectedIntern = intern;
    document.getElementById('intern-detail-name').innerText = intern.name;
    document.getElementById('intern-detail-meta').innerText = `${intern.email} • Target: ${intern.target_domain} (Assigned Cluster: ${intern.assigned_cluster_name})`;
    document.getElementById('intern-detail-score').innerText = `${intern.readiness_score}%`;

    // Render Radar Chart
    renderInternRadarChart(intern);

    // Render Gaps List
    renderInternGapsList(intern);

    // Setup Roadmap Button Click
    const btnRoadmap = document.getElementById('btn-view-intern-roadmap');
    btnRoadmap.onclick = () => {
      renderTrainingRoadmap(intern);
      document.querySelector('[data-tab="roadmaps"]').click();
    };
  }

  function renderInternRadarChart(intern) {
    const labels = intern.radar_benchmark.map(b => b.skill);
    const internLevels = intern.radar_benchmark.map(b => b.intern_level);
    const benchLevels = intern.radar_benchmark.map(b => b.benchmark_level);

    const ctx = document.getElementById('internRadarChart').getContext('2d');
    if (internRadarChart) internRadarChart.destroy();

    internRadarChart = new Chart(ctx, {
      type: 'radar',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Intern Current Level',
            data: internLevels,
            backgroundColor: 'rgba(99, 102, 241, 0.25)',
            borderColor: '#6366f1',
            borderWidth: 2,
            pointBackgroundColor: '#6366f1'
          },
          {
            label: 'Industry Benchmark',
            data: benchLevels,
            backgroundColor: 'rgba(16, 185, 129, 0.15)',
            borderColor: '#10b981',
            borderWidth: 2,
            borderDash: [4, 4],
            pointBackgroundColor: '#10b981'
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          r: {
            angleLines: { color: 'rgba(255, 255, 255, 0.1)' },
            grid: { color: 'rgba(255, 255, 255, 0.1)' },
            pointLabels: { color: '#f8fafc', font: { family: 'Inter', size: 11, weight: '600' } },
            ticks: { display: false, max: 5, min: 0 }
          }
        },
        plugins: {
          legend: { position: 'top', labels: { color: '#94a3b8' } }
        }
      }
    });
  }

  function renderInternGapsList(intern) {
    const container = document.getElementById('intern-gaps-list');
    container.innerHTML = '';

    const allGaps = [
      ...intern.missing_skills.map(g => ({ ...g, type: 'hard' })),
      ...intern.soft_gaps.map(g => ({ ...g, type: 'soft' }))
    ];

    if (allGaps.length === 0) {
      container.innerHTML = '<p style="color:#10b981; font-size:0.85rem;">No critical skill gaps identified! Candidate meets target benchmarks.</p>';
      return;
    }

    allGaps.forEach(g => {
      const isHard = g.type === 'hard';
      const gapHtml = `
        <div class="gap-item ${isHard ? '' : 'soft'}">
          <div>
            <div class="gap-skill-title">${g.skill}</div>
            <div class="gap-levels">Current: Level ${g.current_level} / Required: Level ${g.required_level}</div>
          </div>
          <span class="gap-badge ${isHard ? 'hard' : 'soft'}">${isHard ? 'Missing Skill' : 'Proficiency Upgrade'}</span>
        </div>
      `;
      container.insertAdjacentHTML('beforeend', gapHtml);
    });
  }

  // 9. Training Roadmap Tab Rendering
  function renderTrainingRoadmap(intern) {
    document.getElementById('roadmap-intern-title').innerHTML = `<i class="fa-solid fa-graduation-cap"></i> Tailored Training Roadmap: ${intern.name}`;
    document.getElementById('roadmap-intern-sub').innerText = `Target Domain: ${intern.target_domain} • Readiness Score: ${intern.readiness_score}%`;

    const pillsContainer = document.getElementById('roadmap-meta-pills');
    const totalHours = intern.training_roadmap.reduce((acc, curr) => acc + curr.duration_hours, 0);

    pillsContainer.innerHTML = `
      <span class="step-tag" style="background:var(--primary-light); color:#a5b4fc;"><i class="fa-solid fa-clock"></i> Est. ${totalHours} Hours</span>
      <span class="step-tag" style="background:rgba(16, 185, 129, 0.2); color:var(--accent-emerald);"><i class="fa-solid fa-list-check"></i> ${intern.training_roadmap.length} Modules</span>
    `;

    const container = document.getElementById('timeline-steps-container');
    container.innerHTML = '';

    if (intern.training_roadmap.length === 0) {
      container.innerHTML = '<p style="color:#64748b;">No training modules required. Intern possesses all core skills!</p>';
      return;
    }

    intern.training_roadmap.forEach(step => {
      const stepHtml = `
        <div class="timeline-step" data-step="${step.step}">
          <div class="step-header">
            <div class="step-title-group">
              <h4>${step.course_title}</h4>
              <span>Provider: ${step.provider} • Target Skill: <strong>${step.target_skill}</strong></span>
            </div>
            <div class="step-tags">
              <span class="step-tag"><i class="fa-solid fa-clock"></i> ${step.duration_hours}h</span>
              <span class="step-tag"><i class="fa-solid fa-signal"></i> ${step.difficulty}</span>
            </div>
          </div>
          <p class="step-description">${step.description}</p>
          <div class="step-project-box">
            <i class="fa-solid fa-code"></i> <strong>Hands-on Capstone Project:</strong> ${step.project_name}
          </div>
        </div>
      `;
      container.insertAdjacentHTML('beforeend', stepHtml);
    });
  }

  // 10. Live Resume & Skill Evaluator Playground
  function setupPlayground() {
    const form = document.getElementById('playground-form');
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      runPlaygroundAnalysis();
    });
  }

  function runPlaygroundAnalysis() {
    const name = document.getElementById('pg-candidate-name').value || 'Custom Candidate';
    const targetDomain = document.getElementById('pg-target-domain').value;
    const text = document.getElementById('pg-resume-text').value.toLowerCase();

    if (!text.trim()) {
      alert('Please enter resume text or skill keywords to evaluate.');
      return;
    }

    // Target domain cluster benchmark skills
    const targetCluster = appData.clusters.find(c => c.name === targetDomain) || appData.clusters[0];
    const topKw = targetCluster.top_keywords.slice(0, 7);

    const radarLabels = topKw.map(k => k.word);
    const benchLevels = topKw.map(k => Math.min(5, Math.max(2, Math.round(k.tfidf_weight * 15))));
    const candidateLevels = [];
    const gaps = [];

    topKw.forEach((k, idx) => {
      const word = k.word.toLowerCase();
      let level = 0;
      if (text.includes(word)) {
        level = 3; // basic/intermediate match
        if (text.includes(`expert ${word}`) || text.includes(`advanced ${word}`) || text.includes(`senior ${word}`)) {
          level = 5;
        }
      }
      candidateLevels.push(level);

      const required = benchLevels[idx];
      if (level === 0) {
        gaps.push({ skill: k.word, type: 'Missing Skill', level: 0, required: required });
      } else if (level < required) {
        gaps.push({ skill: k.word, type: 'Proficiency Upgrade', level: level, required: required });
      }
    });

    const totalBench = benchLevels.reduce((a, b) => a + b, 0);
    const totalCand = candidateLevels.reduce((a, b, idx) => a + Math.min(b, benchLevels[idx]), 0);
    const score = Math.round((totalCand / totalBench) * 100);

    // Hide placeholder, show results
    document.getElementById('pg-placeholder').classList.add('hidden');
    document.getElementById('pg-results-container').classList.remove('hidden');
    document.getElementById('pg-readiness-score').innerText = `${score}%`;

    // Render Playground Radar Chart
    const ctx = document.getElementById('playgroundRadarChart').getContext('2d');
    if (playgroundRadarChart) playgroundRadarChart.destroy();

    playgroundRadarChart = new Chart(ctx, {
      type: 'radar',
      data: {
        labels: radarLabels,
        datasets: [
          {
            label: `${name} Level`,
            data: candidateLevels,
            backgroundColor: 'rgba(6, 182, 212, 0.25)',
            borderColor: '#06b6d4',
            borderWidth: 2,
            pointBackgroundColor: '#06b6d4'
          },
          {
            label: `${targetDomain} Benchmark`,
            data: benchLevels,
            backgroundColor: 'rgba(16, 185, 129, 0.15)',
            borderColor: '#10b981',
            borderWidth: 2,
            borderDash: [4, 4],
            pointBackgroundColor: '#10b981'
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          r: {
            angleLines: { color: 'rgba(255, 255, 255, 0.1)' },
            grid: { color: 'rgba(255, 255, 255, 0.1)' },
            pointLabels: { color: '#f8fafc', font: { family: 'Inter', size: 11 } },
            ticks: { display: false, max: 5, min: 0 }
          }
        },
        plugins: {
          legend: { position: 'top', labels: { color: '#94a3b8' } }
        }
      }
    });

    // Render Recommendations
    const listContainer = document.getElementById('pg-recommendations-list');
    listContainer.innerHTML = '';

    if (gaps.length === 0) {
      listContainer.innerHTML = '<p style="color:#10b981;">No gaps identified! Candidate fully satisfies role benchmark.</p>';
      return;
    }

    gaps.forEach(g => {
      const courseMatch = appData.courses_catalog.find(c => c.skill_name.toLowerCase() === g.skill.toLowerCase()) || {
        title: `Applied ${g.skill} Mastering Course`,
        duration_hours: 20,
        provider: 'Tech Learning Hub'
      };

      const gapHtml = `
        <div class="gap-item ${g.level === 0 ? '' : 'soft'}">
          <div>
            <div class="gap-skill-title">${g.skill} - ${courseMatch.title}</div>
            <div class="gap-levels">Provider: ${courseMatch.provider} • Duration: ${courseMatch.duration_hours}h</div>
          </div>
          <span class="gap-badge ${g.level === 0 ? 'hard' : 'soft'}">${g.type}</span>
        </div>
      `;
      listContainer.insertAdjacentHTML('beforeend', gapHtml);
    });
  }

  // 11. Export Functionality
  function setupExport() {
    document.getElementById('btn-export-report').addEventListener('click', () => {
      const jsonStr = JSON.stringify(appData, null, 2);
      const blob = new Blob([jsonStr], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `SkillGap_Analysis_Report_${new Date().toISOString().slice(0,10)}.json`;
      a.click();
      URL.revokeObjectURL(url);
    });

    document.getElementById('btn-re-run-pipeline').addEventListener('click', () => {
      fetchData();
      alert('Data reloaded from latest pipeline analysis!');
    });
  }
});
