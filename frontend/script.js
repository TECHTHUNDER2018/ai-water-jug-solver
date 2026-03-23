let currentStep = 0;
let solutionPath = [];
let capacities = [];
let autoPlayInterval = null;
let currentSpeed = 1;

// Three.js Globals
let scene, camera, renderer, controls;
let jugs3D = []; // { group, waterMesh, targetVol, maxCap }

// DOM
const solveBtn = document.getElementById('solveBtn');
const resetBtn = document.getElementById('resetBtn');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const playBtn = document.getElementById('playBtn');
const speedSlider = document.getElementById('speedSlider');
const speedVal = document.getElementById('speedVal');
const stepCounter = document.getElementById('stepCounter');
const progressFill = document.getElementById('progressFill');
const actionTitle = document.getElementById('actionTitle');
const actionDetails = document.getElementById('actionDetails');
const historyLog = document.getElementById('historyLog');

// Initialize 3D Scene
function init3D() {
    const container = document.getElementById('three-container');
    scene = new THREE.Scene();
    scene.background = null; 
    
    camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
    camera.position.set(0, 5, 20);
    
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    container.innerHTML = '';
    container.appendChild(renderer.domElement);
    
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
    scene.add(ambientLight);
    
    const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
    dirLight.position.set(10, 20, 10);
    scene.add(dirLight);
    
    const pointLight = new THREE.PointLight(0x38bdf8, 1, 50);
    pointLight.position.set(0, 10, 0);
    scene.add(pointLight);

    const grid = new THREE.GridHelper(50, 50, 0x334155, 0x1e293b);
    grid.position.y = -3;
    scene.add(grid);
    
    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.maxPolarAngle = Math.PI / 2 + 0.1; 
    
    window.addEventListener('resize', onWindowResize);
    
    capacities = document.getElementById('capacities').value.split(',').map(Number);
    setupJugs3D();

    animate3D();
}

function onWindowResize() {
    const container = document.getElementById('three-container');
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
}

function animate3D() {
    requestAnimationFrame(animate3D);
    controls.update();
    renderer.render(scene, camera);
}

function setupJugs3D() {
    jugs3D.forEach(j => scene.remove(j.group));
    jugs3D = [];
    
    const maxCap = Math.max(...capacities);
    const spacing = 4.5;
    const startX = -((capacities.length - 1) * spacing) / 2;
    
    const glassMaterial = new THREE.MeshPhysicalMaterial({
        color: 0xffffff,
        metalness: 0.1,
        roughness: 0.05,
        transparent: true,
        opacity: 0.15,
        transmission: 0.9,
        ior: 1.5,
        side: THREE.DoubleSide
    });

    const waterMaterial = new THREE.MeshPhysicalMaterial({
        color: 0x0ea5e9,
        metalness: 0.1,
        roughness: 0.2,
        transparent: true,
        opacity: 0.85,
        transmission: 0.6,
        ior: 1.33
    });

    capacities.forEach((cap, idx) => {
        const height = (cap / maxCap) * 8; 
        const radius = 1.3;
        
        const group = new THREE.Group();
        group.position.x = startX + idx * spacing;
        group.position.y = -3 + height / 2; 
        
        const geoGlass = new THREE.CylinderGeometry(radius, radius, height, 32);
        const glass = new THREE.Mesh(geoGlass, glassMaterial);
        
        const geoWater = new THREE.CylinderGeometry(radius - 0.05, radius - 0.05, height, 32);
        geoWater.translate(0, height/2, 0); 
        const water = new THREE.Mesh(geoWater, waterMaterial);
        water.position.y = -height/2;
        water.scale.y = 0.0001; 
        
        const canvas = document.createElement('canvas');
        canvas.width = 256;
        canvas.height = 128;
        const ctx = canvas.getContext('2d');
        ctx.fillStyle = '#ffffff';
        ctx.font = 'Bold 40px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(`Jug ${idx}`, 128, 50);
        ctx.font = '24px Arial';
        ctx.fillStyle = '#94a3b8';
        ctx.fillText(`Capacity: ${cap}`, 128, 90);
        
        const tex = new THREE.CanvasTexture(canvas);
        const spriteMat = new THREE.SpriteMaterial({ map: tex });
        const sprite = new THREE.Sprite(spriteMat);
        sprite.position.y = height / 2 + 1;
        sprite.scale.set(3, 1.5, 1);
        
        group.add(glass);
        group.add(water);
        group.add(sprite);
        scene.add(group);
        
        jugs3D.push({ group, water, height, cap, waterMesh: water });
    });

    if (camera) {
        gsap.to(camera.position, {
            x: 0,
            y: 5,
            z: maxCap + capacities.length * 2,
            duration: 2,
            ease: "power3.inOut"
        });
    }
}

setTimeout(init3D, 100);

solveBtn.addEventListener('click', async () => {
    let rawCaps = document.getElementById('capacities').value.split(',').map(n => Number(n.trim()));
    let rawStarts = document.getElementById('startVolumes').value.split(',').map(n => Number(n.trim()));
    const target = Number(document.getElementById('target').value);
    const alg = document.getElementById('algorithm').value;
    const kVal = Number(document.getElementById('k').value);

    // Auto-sync startVolumes length to match capacities length so it doesn't crash
    while(rawStarts.length < rawCaps.length) rawStarts.push(0);
    rawStarts = rawStarts.slice(0, rawCaps.length);
    document.getElementById('startVolumes').value = rawStarts.join(',');

    capacities = rawCaps;
    setupJugs3D();

    try {
        solveBtn.disabled = true;
        solveBtn.innerHTML = 'Computing...';
        
        document.getElementById('metricsPanel').style.opacity = '1';

        const res = await fetch('/api/solve', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                capacities: rawCaps,
                start_volumes: rawStarts,
                target: target,
                algorithm: alg,
                k: kVal
            })
        });

        if (!res.ok) throw new Error('API Error');

        const data = await res.json();
        solutionPath = data.path;
        
        solutionPath.unshift({
            action: "Initial State",
            volumes: rawStarts
        });

        displayMetrics(data.metrics);
        populateHistory();
        
        currentStep = 0;
        renderStep();
        
        const hasPath = solutionPath.length > 1;
        prevBtn.disabled = true;
        nextBtn.disabled = !hasPath;
        playBtn.disabled = !hasPath;
        
        if (!hasPath) {
            actionTitle.textContent = "No Path Found";
            actionTitle.style.color = "#ef4444";
            actionDetails.textContent = "The target is unreachable with these parameters.";
            
            // Move water up slightly and drop it to signify failure visually
            jugs3D.forEach(j => {
                gsap.to(j.waterMesh.scale, { y: 0.05, duration: 0.3, yoyo: true, repeat: 1 });
            });
        }

    } catch (err) {
        alert(err.message);
    } finally {
        solveBtn.disabled = false;
        solveBtn.innerHTML = 'Run Simulation';
    }
});

resetBtn.addEventListener('click', () => {
    if(autoPlayInterval) stopAutoPlay();
    solutionPath = [];
    currentStep = 0;
    
    actionTitle.textContent = "Ready to Solve";
    actionTitle.style.color = "#fca5a5";
    actionDetails.textContent = "Configure parameters and press Run Simulation.";
    
    document.getElementById('metricsPanel').style.opacity = '0.3';
    historyLog.innerHTML = '<li class="empty-log">Log will populate when solving...</li>';
    
    prevBtn.disabled = true;
    nextBtn.disabled = true;
    playBtn.disabled = true;
    stepCounter.textContent = "Step: 0 / 0";
    progressFill.style.width = "0%";
    
    jugs3D.forEach(j => {
        gsap.to(j.waterMesh.scale, { y: 0.0001, duration: 1 });
    });
});

function displayMetrics(metrics) {
    document.getElementById('m-time').textContent = metrics.execution_time_ms.toFixed(2) + ' ms';
    document.getElementById('m-mem').textContent = metrics.peak_memory_kb.toFixed(2) + ' KB';
    document.getElementById('m-nodes').textContent = metrics.nodes_expanded;
    
    const cEl = document.getElementById('m-cost');
    cEl.textContent = metrics.solution_cost;
    cEl.style.color = metrics.solution_cost === -1 ? '#ef4444' : '#38bdf8';
    
    document.getElementById('m-bstar').textContent = metrics.effective_branching_factor.toFixed(2);
    
    const aEl = document.getElementById('m-adm');
    aEl.textContent = metrics.heuristic_admissible ? 'Yes' : 'No';
    aEl.style.color = metrics.heuristic_admissible ? '#86efac' : '#fca5a5';
}

function populateHistory() {
    historyLog.innerHTML = '';
    if(solutionPath.length <= 1 && document.getElementById('m-cost').textContent === '-1') {
        historyLog.innerHTML = '<li class="empty-log">Search complete. Target is physically impossible.</li>';
        return;
    }
    
    solutionPath.forEach((step, idx) => {
        const li = document.createElement('li');
        li.id = `log-item-${idx}`;
        li.innerHTML = `<span class="step-num">Step ${idx}</span><strong>${step.action}</strong><br>Vols: [${step.volumes.join(', ')}]`;
        historyLog.appendChild(li);
    });
}

function renderStep() {
    if (solutionPath.length === 0) return;
    
    const step = solutionPath[currentStep];
    
    actionTitle.textContent = step.action;
    actionTitle.style.color = "#38bdf8";
    actionDetails.textContent = `Current Volumes: [${step.volumes.join(', ')}]`;
    
    stepCounter.textContent = `Step: ${currentStep} / ${solutionPath.length > 1 ? solutionPath.length - 1 : 0}`;
    const pct = solutionPath.length > 1 ? (currentStep / (solutionPath.length - 1)) * 100 : 0;
    progressFill.style.width = `${pct}%`;
    
    step.volumes.forEach((vol, idx) => {
        const targetScale = Math.max(0.0001, vol / capacities[idx]);
        gsap.to(jugs3D[idx].waterMesh.scale, {
            y: targetScale,
            duration: 0.8 / currentSpeed,
            ease: "back.out(1.2)"
        });
    });
    
    document.querySelectorAll('.history-list li').forEach(li => li.classList.remove('active'));
    const activeLi = document.getElementById(`log-item-${currentStep}`);
    if(activeLi) {
        activeLi.classList.add('active');
        activeLi.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
    
    prevBtn.disabled = currentStep === 0;
    nextBtn.disabled = currentStep === solutionPath.length - 1 || solutionPath.length <= 1;
}

speedSlider.addEventListener('input', (e) => {
    currentSpeed = e.target.value;
    speedVal.textContent = currentSpeed + 'x';
    if(autoPlayInterval) {
        stopAutoPlay();
        startAutoPlay();
    }
});

prevBtn.addEventListener('click', () => {
    if (currentStep > 0) {
        currentStep--;
        renderStep();
    }
    stopAutoPlay();
});

nextBtn.addEventListener('click', () => {
    if (currentStep < solutionPath.length - 1) {
        currentStep++;
        renderStep();
    }
    stopAutoPlay();
});

function startAutoPlay() {
    playBtn.innerHTML = '⏸ Pause';
    autoPlayInterval = setInterval(() => {
        if (currentStep < solutionPath.length - 1) {
            currentStep++;
            renderStep();
        } else {
            stopAutoPlay();
        }
    }, 1500 / currentSpeed);
}

function stopAutoPlay() {
    if(autoPlayInterval) {
        clearInterval(autoPlayInterval);
        autoPlayInterval = null;
    }
    playBtn.innerHTML = '▶ Auto Play';
}

playBtn.addEventListener('click', () => {
    if (autoPlayInterval) {
        stopAutoPlay();
    } else {
        if (currentStep === solutionPath.length - 1) {
            currentStep = 0;
        }
        startAutoPlay();
    }
});
