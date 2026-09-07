document.addEventListener('DOMContentLoaded', () => {
    // ---------------------------------------------------------
    // 1. Navigation & Tab Switching
    // ---------------------------------------------------------
    const navItems = document.querySelectorAll('.nav-item');
    const tabContents = document.querySelectorAll('.tab-content');
    const pageTitle = document.getElementById('page-title');
    const pageSubtitle = document.getElementById('page-subtitle');

    const tabHeaders = {
        'tab-executive': {
            title: 'Executive Summary Dashboard',
            subtitle: 'Bio-statistical analysis of menstrual phase & PCOD impacts on daily work performance'
        },
        'tab-phase': {
            title: 'Cycle Phase Deep-Dive Analytics',
            subtitle: 'Comparative metrics across Menstrual, Follicular, Ovulation, and Luteal phases'
        },
        'tab-tracker': {
            title: 'Period & PCOD Health Tracker Module',
            subtitle: 'Log period delays, cycle irregularity, PCOD symptoms, and view personalized wellness guidance'
        },
        'tab-factors': {
            title: 'Productivity Drivers & EDA Findings',
            subtitle: 'Scatter regression and correlation analysis of lifestyle & physical factors'
        },
        'tab-predictor': {
            title: 'Machine Learning Productivity Engine',
            subtitle: 'Real-time daily score prediction simulator powered by Random Forest Regression'
        }
    };

    navItems.forEach(item => {
        item.addEventListener('click', () => {
            const targetTab = item.getAttribute('data-tab');

            navItems.forEach(n => n.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            item.classList.add('active');
            const targetEl = document.getElementById(targetTab);
            if (targetEl) targetEl.classList.add('active');

            if (tabHeaders[targetTab]) {
                pageTitle.textContent = tabHeaders[targetTab].title;
                if (pageSubtitle) pageSubtitle.textContent = tabHeaders[targetTab].subtitle;
            }
        });
    });

    // ---------------------------------------------------------
    // 2. Chart.js Global Configuration
    // ---------------------------------------------------------
    Chart.defaults.color = '#94a3b8';
    Chart.defaults.font.family = 'Plus Jakarta Sans, sans-serif';
    Chart.defaults.borderColor = 'rgba(255, 255, 255, 0.08)';

    const phaseColors = {
        'Menstrual': '#e63946',
        'Follicular': '#457b9d',
        'Ovulation': '#2a9d8f',
        'Luteal': '#e76f51'
    };

    // ---------------------------------------------------------
    // 3. Tab 1 & 2 Charts
    // ---------------------------------------------------------
    const ctxPhaseProd = document.getElementById('chart-phase-productivity');
    if (ctxPhaseProd) {
        new Chart(ctxPhaseProd, {
            type: 'bar',
            data: {
                labels: ['Menstrual Phase', 'Follicular Phase', 'Ovulation Phase', 'Luteal Phase'],
                datasets: [{
                    label: 'Avg Productivity Score',
                    data: [44.2, 71.5, 75.8, 55.4],
                    backgroundColor: [phaseColors['Menstrual'], phaseColors['Follicular'], phaseColors['Ovulation'], phaseColors['Luteal']],
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: { y: { beginAtZero: true, max: 100 } }
            }
        });
    }

    const ctxPcodImp = document.getElementById('chart-pcod-impact');
    if (ctxPcodImp) {
        new Chart(ctxPcodImp, {
            type: 'bar',
            data: {
                labels: ['Non-PCOD Cohort', 'Diagnosed PCOD Cohort'],
                datasets: [
                    {
                        label: 'Productivity Score',
                        data: [64.8, 52.4],
                        backgroundColor: '#2a9d8f',
                        borderRadius: 6
                    },
                    {
                        label: 'Stress Index (1-10)',
                        data: [4.6, 7.2],
                        backgroundColor: '#e63946',
                        borderRadius: 6
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: { y: { beginAtZero: true, max: 100 } }
            }
        });
    }

    const ctxPhaseStress = document.getElementById('chart-phase-stress');
    if (ctxPhaseStress) {
        new Chart(ctxPhaseStress, {
            type: 'bar',
            data: {
                labels: ['Menstrual', 'Follicular', 'Ovulation', 'Luteal'],
                datasets: [{
                    label: 'Avg Stress Index',
                    data: [6.8, 4.4, 3.9, 6.1],
                    backgroundColor: '#e76f51',
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: { y: { beginAtZero: true, max: 10 } }
            }
        });
    }

    const ctxPhaseMood = document.getElementById('chart-phase-mood');
    if (ctxPhaseMood) {
        new Chart(ctxPhaseMood, {
            type: 'bar',
            data: {
                labels: ['Menstrual', 'Follicular', 'Ovulation', 'Luteal'],
                datasets: [{
                    label: 'Avg Mood Score',
                    data: [4.6, 7.2, 8.3, 5.4],
                    backgroundColor: '#8b5cf6',
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: { y: { beginAtZero: true, max: 10 } }
            }
        });
    }

    const ctxPhaseEP = document.getElementById('chart-phase-energy-pain');
    if (ctxPhaseEP) {
        new Chart(ctxPhaseEP, {
            type: 'bar',
            data: {
                labels: ['Menstrual', 'Follicular', 'Ovulation', 'Luteal'],
                datasets: [
                    { label: 'Energy Level', data: [3.9, 7.4, 8.6, 5.2], backgroundColor: '#2a9d8f', borderRadius: 6 },
                    { label: 'Pain Level', data: [7.2, 2.3, 2.0, 4.2], backgroundColor: '#e63946', borderRadius: 6 }
                ]
            },
            options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true, max: 10 } } }
        });
    }

    const ctxDelayProd = document.getElementById('chart-delay-productivity');
    if (ctxDelayProd) {
        const delayDays = [0, 5, 10, 15, 20, 25, 30];
        const scores = [72.5, 68.2, 63.4, 57.8, 51.2, 45.0, 38.4];
        new Chart(ctxDelayProd, {
            type: 'line',
            data: {
                labels: delayDays.map(d => `${d}d Late`),
                datasets: [{
                    label: 'Productivity Score',
                    data: scores,
                    borderColor: '#e63946',
                    backgroundColor: 'rgba(230, 57, 70, 0.15)',
                    fill: true,
                    tension: 0.3,
                    pointRadius: 5
                }]
            },
            options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true, max: 100 } } }
        });
    }

    // ---------------------------------------------------------
    // 4. Tab 3 EDA Charts
    // ---------------------------------------------------------
    const ctxSleepProd = document.getElementById('chart-sleep-productivity');
    if (ctxSleepProd) {
        new Chart(ctxSleepProd, {
            type: 'line',
            data: {
                labels: ['4 hrs', '5 hrs', '6 hrs', '7 hrs', '8 hrs', '9 hrs', '10 hrs'],
                datasets: [{ label: 'Productivity Score', data: [39.5, 48.2, 58.0, 67.5, 77.2, 84.8, 90.1], borderColor: '#2a9d8f', backgroundColor: 'rgba(42, 157, 143, 0.15)', fill: true, tension: 0.3 }]
            },
            options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true, max: 100 } } }
        });
    }

    const ctxStressProd = document.getElementById('chart-stress-productivity');
    if (ctxStressProd) {
        new Chart(ctxStressProd, {
            type: 'line',
            data: {
                labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(s => `Lvl ${s}`),
                datasets: [{ label: 'Productivity Score', data: [86.2, 82.0, 77.4, 71.0, 63.2, 55.6, 47.8, 39.2, 30.5, 22.0], borderColor: '#e76f51', backgroundColor: 'rgba(231, 111, 81, 0.15)', fill: true, tension: 0.3 }]
            },
            options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true, max: 100 } } }
        });
    }

    const ctxPainProd = document.getElementById('chart-pain-productivity');
    if (ctxPainProd) {
        new Chart(ctxPainProd, {
            type: 'bar',
            data: {
                labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(p => `Pain ${p}`),
                datasets: [{ label: 'Productivity Score', data: [83.5, 79.4, 74.8, 69.2, 62.0, 53.8, 44.5, 36.2, 27.8, 19.5], backgroundColor: '#e63946', borderRadius: 6 }]
            },
            options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true, max: 100 } } }
        });
    }

    const ctxCorr = document.getElementById('chart-correlation');
    if (ctxCorr) {
        new Chart(ctxCorr, {
            type: 'bar',
            data: {
                labels: ['Health Score', 'Sleep Hours', 'Cycle Phase', 'Energy Level', 'Pain Level', 'Period Delay', 'Hormonal Imbalance'],
                datasets: [{ label: 'Correlation (r)', data: [0.94, 0.42, 0.28, 0.81, -0.45, -0.38, -0.41], backgroundColor: ctx => ctx.raw >= 0 ? '#2a9d8f' : '#e63946', borderRadius: 6 }]
            },
            options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false, scales: { x: { min: -1.0, max: 1.0 } } }
        });
    }

    // ---------------------------------------------------------
    // 5. Tab 3: Period & PCOD Health Tracker Logic
    // ---------------------------------------------------------
    const trackPcod = document.getElementById('track-pcod');
    const trackCycleLen = document.getElementById('track-cycle-len');
    const trackDelayDays = document.getElementById('track-delay-days');
    const trackHormonal = document.getElementById('track-hormonal');

    const valCycleLen = document.getElementById('val-cycle-len');
    const valDelayDays = document.getElementById('val-delay-days');
    const valHormonal = document.getElementById('val-hormonal');

    const trackerScoreEl = document.getElementById('tracker-score');
    const trackerRing = document.getElementById('tracker-ring');
    const trackerTier = document.getElementById('tracker-tier');
    const trackerRecList = document.getElementById('tracker-rec-list');

    function updateTracker() {
        const pcod = trackPcod.value;
        const cycleLen = parseInt(trackCycleLen.value);
        const delay = parseInt(trackDelayDays.value);
        const hormonal = parseInt(trackHormonal.value);

        if (valCycleLen) valCycleLen.textContent = `${cycleLen} Days`;
        if (valDelayDays) valDelayDays.textContent = `${delay} Days Late`;
        if (valHormonal) valHormonal.textContent = `${hormonal} / 10`;

        // Calculate PCOD Health Risk Index (0 - 100)
        let riskScore = 20.0 + (delay * 1.5) + (hormonal * 4.2);
        if (pcod === 'Yes') riskScore += 22.0;
        if (cycleLen > 35) riskScore += (cycleLen - 35) * 0.8;
        riskScore = Math.min(Math.max(riskScore, 10.0), 100.0);

        if (trackerScoreEl) trackerScoreEl.textContent = riskScore.toFixed(1);

        if (trackerRing) {
            const circumference = 477.5;
            const offset = circumference - (riskScore / 100) * circumference;
            trackerRing.style.strokeDashoffset = offset;
            if (riskScore >= 70) trackerRing.style.stroke = '#e63946';
            else if (riskScore >= 45) trackerRing.style.stroke = '#e76f51';
            else trackerRing.style.stroke = '#2a9d8f';
        }

        if (trackerTier) {
            let recs = [];
            if (riskScore >= 70) {
                trackerTier.textContent = 'High PCOD & Cycle Irregularity Risk';
                trackerTier.className = 'score-tier tier-low';
                recs.push(`<strong>PCOD Alert:</strong> Significant cycle delay (${delay}d late) and high hormonal imbalance. Focus on anti-inflammatory diet (Omega-3s, Zinc) and stress mitigation.`);
                recs.push(`<strong>Workplace Strategy:</strong> Request flex remote work or asynchronous scheduling to manage physical discomfort and fatigue.`);
            } else if (riskScore >= 45) {
                trackerTier.textContent = 'Moderate Cycle Delay / Irregularity';
                trackerTier.className = 'score-tier tier-moderate';
                recs.push(`<strong>Cycle Guidance:</strong> Mild delay detected. Maintain steady hydration, light yoga, and 7.5+ hours of sleep.`);
            } else {
                trackerTier.textContent = 'Regular & Balanced Cycle';
                trackerTier.className = 'score-tier tier-optimal';
                recs.push(`<strong>Optimal Health:</strong> Cycle length (${cycleLen}d) is balanced. Keep up regular wellness routines.`);
            }
            if (trackerRecList) trackerRecList.innerHTML = recs.map(r => `<li>${r}</li>`).join('');
        }
    }

    [trackPcod, trackCycleLen, trackDelayDays, trackHormonal].forEach(el => {
        if (el) el.addEventListener('input', updateTracker);
    });

    ['sym-cramps', 'sym-bloating', 'sym-fatigue', 'sym-acne', 'sym-mood'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.addEventListener('change', updateTracker);
    });

    updateTracker();

    // ---------------------------------------------------------
    // 6. Tab 5: ML Prediction Engine Simulator
    // ---------------------------------------------------------
    const simPhase = document.getElementById('sim-phase');
    const simPcod = document.getElementById('sim-pcod');
    const simDelay = document.getElementById('sim-delay');
    const simSleep = document.getElementById('sim-sleep');
    const simStress = document.getElementById('sim-stress');
    const simPain = document.getElementById('sim-pain');
    const simMood = document.getElementById('sim-mood');
    const simEnergy = document.getElementById('sim-energy');

    const valSimDelay = document.getElementById('val-sim-delay');
    const valSleep = document.getElementById('val-sleep');
    const valStress = document.getElementById('val-stress');
    const valPain = document.getElementById('val-pain');
    const valMood = document.getElementById('val-mood');
    const valEnergy = document.getElementById('val-energy');

    const predictedScoreEl = document.getElementById('predicted-score');
    const scoreRing = document.getElementById('score-ring');
    const scoreTier = document.getElementById('score-tier');
    const recList = document.getElementById('rec-list');

    const phaseOffsets = { 'Menstrual': -4.5, 'Follicular': 3.5, 'Ovulation': 6.0, 'Luteal': -2.0 };

    function updateSimulator() {
        if (!simPhase) return;
        const phase = simPhase.value;
        const pcod = simPcod ? simPcod.value : 'No';
        const delay = simDelay ? parseInt(simDelay.value) : 0;
        const sleep = parseFloat(simSleep.value);
        const stress = parseInt(simStress.value);
        const pain = parseInt(simPain.value);
        const mood = parseInt(simMood.value);
        const energy = parseInt(simEnergy.value);

        if (valSimDelay) valSimDelay.textContent = `${delay} Days Late`;
        if (valSleep) valSleep.textContent = `${sleep} hrs`;
        if (valStress) valStress.textContent = `${stress} / 10`;
        if (valPain) valPain.textContent = `${pain} / 10`;
        if (valMood) valMood.textContent = `${mood} / 10`;
        if (valEnergy) valEnergy.textContent = `${energy} / 10`;

        const offset = phaseOffsets[phase] || 0;
        const pcodPen = (pcod === 'Yes') ? -3.8 : 0.0;
        const delayPen = -0.18 * delay;

        let score = 12.0 + (4.00 * energy) + (3.75 * sleep) + (2.50 * mood) - (2.35 * stress) - (2.00 * pain) + offset + pcodPen + delayPen;
        score = Math.min(Math.max(score, 10.0), 100.0);
        score = Math.round(score * 10) / 10;

        if (predictedScoreEl) predictedScoreEl.textContent = score.toFixed(1);

        if (scoreRing) {
            const circumference = 477.5;
            const offsetRing = circumference - (score / 100) * circumference;
            scoreRing.style.strokeDashoffset = offsetRing;
            if (score >= 75) scoreRing.style.stroke = '#10b981';
            else if (score >= 50) scoreRing.style.stroke = '#f59e0b';
            else scoreRing.style.stroke = '#f43f5e';
        }

        if (scoreTier) {
            scoreTier.className = 'score-tier';
            let recs = [];
            if (score >= 75) {
                scoreTier.textContent = 'High Productivity Output';
                scoreTier.classList.add('tier-optimal');
                recs.push(`<strong>Peak Output:</strong> Optimal day for strategic presentations and high-stakes problem solving.`);
            } else if (score >= 50) {
                scoreTier.textContent = 'Moderate Performance Output';
                scoreTier.classList.add('tier-moderate');
                recs.push(`<strong>Balanced Focus:</strong> Ideal for routine coding, documentation, and structured team reviews.`);
            } else {
                scoreTier.textContent = 'Low Energy / Flex Need';
                scoreTier.classList.add('tier-low');
                recs.push(`<strong>Flex Day Recommended:</strong> Consider remote flex day, lighter workloads, and pain management.`);
            }

            if (pcod === 'Yes') {
                recs.push(`<strong>PCOD Condition Note:</strong> Diagnosed PCOD is applying a -3.8 pt baseline output penalty. Maintain low-GI nutrition and stress reduction.`);
            }
            if (delay > 7) {
                recs.push(`<strong>Period Delay Warning:</strong> ${delay} days late. Period delay penalty is reducing output by -${(delay * 0.18).toFixed(1)} points.`);
            }

            if (recList) recList.innerHTML = recs.map(r => `<li>${r}</li>`).join('');
        }
    }

    [simPhase, simPcod, simDelay, simSleep, simStress, simPain, simMood, simEnergy].forEach(el => {
        if (el) el.addEventListener('input', updateSimulator);
    });

    updateSimulator();
});
