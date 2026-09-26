"""
Commercial Design 3D & 4D Animation Component for CODEX Order & Warranty Assistant.
Renders an interactive Three.js Commercial Retail Studio Showroom:
- Sleek commercial showroom floor with dynamic studio lighting and reflective halo rings
- 4D Hyper-Dimensional Continuum Grid & Tesseract wireframe projection
- Interactive 3D Retail Parcel with dynamic status illumination (urgent alert vs active safe)
- Laser Scan telemetry beam and commercial interactive HUD controls
"""

def render_3d_order_animation(
    order_id: str = "CODEX-HUB",
    customer_name: str = "Shopper",
    is_urgent: bool = False,
    urgent_count: int = 0,
    total_items: int = 1,
    height: int = 400
) -> str:
    """
    Generates an HTML/JS snippet with Three.js, OrbitControls, and Commercial Studio 3D/4D procedural geometries.
    Runs 100% in browser WebGL with zero external asset dependencies.
    """
    glow_color = "#EF4444" if is_urgent else "#10B981"
    glow_hex = "0xef4444" if is_urgent else "0x10b981"
    status_text = f"⚠️ ALERT: {urgent_count} ITEM(S) EXPIRING SOON" if is_urgent else "✅ ALL RETURN WINDOWS SAFE"
    badge_bg = "rgba(239, 68, 68, 0.22)" if is_urgent else "rgba(16, 185, 129, 0.22)"
    badge_border = "#EF4444" if is_urgent else "#10B981"

    html_code = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                overflow: hidden;
                /* Commercial Studio Luxury Gradient Animation */
                background: radial-gradient(ellipse at 50% 40%, rgba(2, 132, 199, 0.25) 0%, rgba(15, 23, 42, 0.95) 65%),
                            radial-gradient(circle at 80% 15%, rgba(124, 58, 237, 0.28) 0%, transparent 55%),
                            radial-gradient(circle at 20% 85%, rgba(16, 185, 129, 0.20) 0%, transparent 55%),
                            linear-gradient(180deg, #070b14 0%, #0b1120 50%, #0f172a 100%);
                background-size: 200% 200%;
                animation: commercialStudioSweep 16s ease-in-out infinite alternate;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace;
                color: #e2e8f0;
                width: 100%;
                height: {height}px;
                position: relative;
                border-radius: 14px;
                border: 1px solid rgba(56, 189, 248, 0.35);
                box-shadow: 0 16px 40px rgba(0, 0, 0, 0.65), inset 0 1px 0 rgba(255, 255, 255, 0.1);
            }}

            @keyframes commercialStudioSweep {{
                0% {{ background-position: 0% 0%; }}
                50% {{ background-position: 100% 100%; }}
                100% {{ background-position: 0% 100%; }}
            }}

            #canvas-container {{
                width: 100%;
                height: 100%;
                display: block;
            }}
            .hud-overlay {{
                position: absolute;
                top: 14px;
                left: 16px;
                pointer-events: none;
                z-index: 10;
            }}
            .hud-title {{
                font-size: 11px;
                font-weight: 800;
                letter-spacing: 0.1em;
                text-transform: uppercase;
                color: #38bdf8;
                display: flex;
                align-items: center;
                gap: 6px;
                font-family: monospace;
            }}
            .hud-order {{
                font-size: 18px;
                font-weight: 800;
                color: #f8fafc;
                margin-top: 2px;
                text-shadow: 0 2px 10px rgba(0,0,0,0.5);
            }}
            .hud-badge {{
                display: inline-block;
                margin-top: 6px;
                padding: 4px 10px;
                border-radius: 6px;
                background: {badge_bg};
                border: 1px solid {badge_border};
                color: {glow_color};
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 0.04em;
                text-transform: uppercase;
                box-shadow: 0 0 14px {glow_color}55;
            }}
            .badge-commercial {{
                display: inline-block;
                margin-left: 8px;
                padding: 3px 8px;
                border-radius: 999px;
                background: rgba(56, 189, 248, 0.2);
                border: 1px solid #38bdf8;
                color: #7dd3fc;
                font-size: 10px;
                font-weight: 800;
                letter-spacing: 0.06em;
                font-family: monospace;
            }}
            .controls-hint {{
                position: absolute;
                bottom: 12px;
                right: 16px;
                font-size: 10px;
                color: #94a3b8;
                pointer-events: none;
                background: rgba(15, 23, 42, 0.85);
                padding: 4px 12px;
                border-radius: 6px;
                border: 1px solid rgba(56, 189, 248, 0.25);
                font-family: monospace;
            }}
            .hud-buttons {{
                position: absolute;
                bottom: 12px;
                left: 16px;
                display: flex;
                gap: 8px;
                z-index: 10;
                flex-wrap: wrap;
            }}
            .hud-btn {{
                background: rgba(15, 23, 42, 0.9);
                border: 1px solid rgba(56, 189, 248, 0.35);
                color: #cbd5e1;
                font-size: 11px;
                font-weight: 600;
                padding: 6px 12px;
                border-radius: 8px;
                cursor: pointer;
                transition: all 0.2s;
                backdrop-filter: blur(12px);
                font-family: monospace;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            }}
            .hud-btn:hover {{
                background: rgba(2, 132, 199, 0.35);
                border-color: #38bdf8;
                color: #fff;
                box-shadow: 0 0 16px rgba(56, 189, 248, 0.45);
                transform: translateY(-1px);
            }}
            .hud-btn.active {{
                background: rgba(2, 132, 199, 0.4);
                border-color: #38bdf8;
                color: #f0fdf4;
            }}
        </style>
        <!-- Load Three.js and OrbitControls -->
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    </head>
    <body>
        <div class="hud-overlay">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;flex-wrap:wrap;">
                <span class="hud-title"><span>🛍️</span> COMMERCIAL 4D SHOWROOM • RETAIL STUDIO</span>
                <span class="badge-commercial">STUDIO GRADE</span>
            </div>
            <div class="hud-order">{order_id} <span style="font-size:12px;font-weight:400;color:#94a3b8;">({total_items} items • {customer_name})</span></div>
            <div class="hud-badge">{status_text}</div>
        </div>

        <div class="hud-buttons">
            <button class="hud-btn active" id="btn-4d">🌀 4D Continuum Grid: ON</button>
            <button class="hud-btn" id="btn-scan">⚡ Laser Scan</button>
            <button class="hud-btn" id="btn-speed">Speed: 1x</button>
            <button class="hud-btn" id="btn-wireframe">Wireframe</button>
            <button class="hud-btn" id="btn-reset">Reset View</button>
        </div>

        <div class="controls-hint">🖱️ Left-drag: Orbit Showroom | Scroll: Zoom</div>
        <div id="canvas-container"></div>

        <script>
            const container = document.getElementById('canvas-container');
            const width = window.innerWidth;
            const height = {height};

            // Scene, Camera, Renderer
            const scene = new THREE.Scene();
            scene.fog = new THREE.FogExp2(0x070b14, 0.035);

            const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
            camera.position.set(4.2, 2.8, 5.0);

            const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
            renderer.setSize(width, height);
            renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
            renderer.shadowMap.enabled = true;
            renderer.shadowMap.type = THREE.PCFSoftShadowMap;
            container.appendChild(renderer.domElement);

            // Controls
            const controls = new THREE.OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;
            controls.dampingFactor = 0.05;
            controls.maxPolarAngle = Math.PI / 2 + 0.1;
            controls.minDistance = 2.0;
            controls.maxDistance = 14.0;
            controls.target.set(0, 0.4, 0);

            // Lighting (Commercial Studio 3-Point Light Rig)
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.75);
            scene.add(ambientLight);

            // Key Light (Warm White)
            const keyLight = new THREE.DirectionalLight(0xfff8ee, 1.4);
            keyLight.position.set(5, 8, 4);
            keyLight.castShadow = true;
            keyLight.shadow.mapSize.width = 1024;
            keyLight.shadow.mapSize.height = 1024;
            scene.add(keyLight);

            // Fill Light (Cool Commercial Cyan)
            const fillLight = new THREE.DirectionalLight(0x38bdf8, 0.8);
            fillLight.position.set(-6, 3, -4);
            scene.add(fillLight);

            // Status Accent Light
            const statusColor = {glow_hex};
            const statusLight = new THREE.PointLight(statusColor, 2.8, 9);
            statusLight.position.set(0, 2.0, 0);
            scene.add(statusLight);

            // Luxury Violet Floor Accent Light
            const violetLight = new THREE.PointLight(0x7c3aed, 2.2, 10);
            violetLight.position.set(0, -0.6, 0);
            scene.add(violetLight);

            // ========================================================
            // 🏢 1. COMMERCIAL REFLECTIVE STUDIO FLOOR & PEDESTAL
            // ========================================================
            // Circular Pedestal Stage
            const stageGeo = new THREE.CylinderGeometry(1.8, 1.9, 0.12, 64);
            const stageMat = new THREE.MeshStandardMaterial({{
                color: 0x0f172a,
                roughness: 0.25,
                metalness: 0.85
            }});
            const stageMesh = new THREE.Mesh(stageGeo, stageMat);
            stageMesh.position.y = -0.65;
            stageMesh.receiveShadow = true;
            scene.add(stageMesh);

            // Concentric Glowing LED Halo Rings on Floor
            const ringGeo1 = new THREE.RingGeometry(1.82, 1.88, 64);
            const ringMat1 = new THREE.MeshBasicMaterial({{
                color: statusColor,
                side: THREE.DoubleSide,
                transparent: true,
                opacity: 0.8
            }});
            const ringMesh1 = new THREE.Mesh(ringGeo1, ringMat1);
            ringMesh1.rotation.x = -Math.PI / 2;
            ringMesh1.position.y = -0.63;
            scene.add(ringMesh1);

            const ringGeo2 = new THREE.RingGeometry(2.3, 2.34, 64);
            const ringMat2 = new THREE.MeshBasicMaterial({{
                color: 0x38bdf8,
                side: THREE.DoubleSide,
                transparent: true,
                opacity: 0.45
            }});
            const ringMesh2 = new THREE.Mesh(ringGeo2, ringMat2);
            ringMesh2.rotation.x = -Math.PI / 2;
            ringMesh2.position.y = -0.64;
            scene.add(ringMesh2);

            // ========================================================
            // 🌀 2. COMMERCIAL 4D SPACETIME RIPPLE GRID
            // ========================================================
            const gridW = 22, gridH = 22, gridSegs = 36;
            const waveGridGeo = new THREE.PlaneGeometry(gridW, gridH, gridSegs, gridSegs);
            waveGridGeo.rotateX(-Math.PI / 2);
            const waveGridMat = new THREE.MeshBasicMaterial({{
                color: 0x0284c7,
                wireframe: true,
                transparent: true,
                opacity: 0.35
            }});
            const waveGridMesh = new THREE.Mesh(waveGridGeo, waveGridMat);
            waveGridMesh.position.y = -0.72;
            scene.add(waveGridMesh);

            // ========================================================
            // 🌀 3. MATHEMATICAL 4D TESSERACT HYPERCUBE BACKGROUND
            // ========================================================
            const vertices4D = [];
            for (let x = -1; x <= 1; x += 2) {{
                for (let y = -1; y <= 1; y += 2) {{
                    for (let z = -1; z <= 1; z += 2) {{
                        for (let w = -1; w <= 1; w += 2) {{
                            vertices4D.push([x, y, z, w]);
                        }}
                    }}
                }}
            }}

            const edges4D = [];
            for (let i = 0; i < 16; i++) {{
                for (let j = i + 1; j < 16; j++) {{
                    let diff = 0;
                    for (let k = 0; k < 4; k++) {{
                        if (vertices4D[i][k] !== vertices4D[j][k]) diff++;
                    }}
                    if (diff === 1) edges4D.push([i, j]);
                }}
            }}

            const tesseractGroup = new THREE.Group();
            scene.add(tesseractGroup);

            const tesseractLinesGeo = new THREE.BufferGeometry();
            const linePositions = new Float32Array(edges4D.length * 2 * 3);
            tesseractLinesGeo.setAttribute('position', new THREE.BufferAttribute(linePositions, 3));
            const tesseractLinesMat = new THREE.LineBasicMaterial({{
                color: 0x38bdf8,
                transparent: true,
                opacity: 0.55
            }});
            const tesseractLines = new THREE.LineSegments(tesseractLinesGeo, tesseractLinesMat);
            tesseractGroup.add(tesseractLines);

            // 16 Vertex Spheres
            const vertexSpheres = [];
            const sphereGeo = new THREE.SphereGeometry(0.04, 10, 10);
            const sphereMat = new THREE.MeshBasicMaterial({{ color: 0x38bdf8, transparent: true, opacity: 0.85 }});
            for (let i = 0; i < 16; i++) {{
                const sp = new THREE.Mesh(sphereGeo, sphereMat);
                tesseractGroup.add(sp);
                vertexSpheres.push(sp);
            }}

            // ========================================================
            // 📦 4. CENTRAL COMMERCIAL PRODUCT PARCEL & DUAL RINGS
            // ========================================================
            const mainGroup = new THREE.Group();
            scene.add(mainGroup);

            // Cardboard Box
            const boxGeo = new THREE.BoxGeometry(1.5, 1.2, 1.3);
            const boxMat = new THREE.MeshStandardMaterial({{
                color: 0xd4a373,
                roughness: 0.5,
                metalness: 0.15
            }});
            const boxMesh = new THREE.Mesh(boxGeo, boxMat);
            boxMesh.castShadow = true;
            mainGroup.add(boxMesh);

            // Branding Ribbon Tape
            const tapeMat = new THREE.MeshStandardMaterial({{
                color: 0x0f172a,
                roughness: 0.25,
                metalness: 0.6
            }});
            mainGroup.add(new THREE.Mesh(new THREE.BoxGeometry(0.28, 1.21, 1.31), tapeMat));
            mainGroup.add(new THREE.Mesh(new THREE.BoxGeometry(1.51, 1.21, 0.28), tapeMat));

            // Dual Rotating Warranty Shield Rings
            const shieldOrbitGroup = new THREE.Group();
            mainGroup.add(shieldOrbitGroup);

            const torGeo1 = new THREE.TorusGeometry(1.35, 0.035, 16, 100);
            const torMat1 = new THREE.MeshStandardMaterial({{
                color: statusColor,
                emissive: statusColor,
                emissiveIntensity: 0.7,
                roughness: 0.2,
                metalness: 0.9
            }});
            const torMesh1 = new THREE.Mesh(torGeo1, torMat1);
            torMesh1.rotation.x = Math.PI / 3;
            shieldOrbitGroup.add(torMesh1);

            const torGeo2 = new THREE.TorusGeometry(1.5, 0.025, 16, 100);
            const torMat2 = new THREE.MeshStandardMaterial({{
                color: 0x38bdf8,
                emissive: 0x38bdf8,
                emissiveIntensity: 0.5,
                roughness: 0.2,
                metalness: 0.9
            }});
            const torMesh2 = new THREE.Mesh(torGeo2, torMat2);
            torMesh2.rotation.y = Math.PI / 2.3;
            shieldOrbitGroup.add(torMesh2);

            // Hexagon Security Badge
            const badgeMesh = new THREE.Mesh(
                new THREE.CylinderGeometry(0.22, 0.22, 0.06, 6),
                new THREE.MeshStandardMaterial({{
                    color: 0x0f172a,
                    emissive: statusColor,
                    emissiveIntensity: 0.5,
                    roughness: 0.2,
                    metalness: 0.95
                }})
            );
            badgeMesh.position.set(1.35, 0, 0);
            badgeMesh.rotation.z = Math.PI / 2;
            shieldOrbitGroup.add(badgeMesh);

            // ========================================================
            // ✨ 5. COMMERCIAL AMBIENT DUST / PARTICLES
            // ========================================================
            const particleCount = 200;
            const particleGeo = new THREE.BufferGeometry();
            const particlePos = new Float32Array(particleCount * 3);
            for (let i = 0; i < particleCount * 3; i += 3) {{
                particlePos[i] = (Math.random() - 0.5) * 8;
                particlePos[i + 1] = (Math.random() - 0.5) * 4 + 0.5;
                particlePos[i + 2] = (Math.random() - 0.5) * 8;
            }}
            particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePos, 3));
            const particleMat = new THREE.PointsMaterial({{
                color: 0x38bdf8,
                size: 0.045,
                transparent: true,
                opacity: 0.65
            }});
            const particleSystem = new THREE.Points(particleGeo, particleMat);
            scene.add(particleSystem);

            // ========================================================
            // ⚡ LASER SCAN TELEMETRY BEAM
            // ========================================================
            let isLaserActive = false;
            let laserProgress = 0;
            const laserPlaneGeo = new THREE.PlaneGeometry(2.4, 0.05);
            const laserPlaneMat = new THREE.MeshBasicMaterial({{
                color: 0x38bdf8,
                side: THREE.DoubleSide,
                transparent: true,
                opacity: 0
            }});
            const laserMesh = new THREE.Mesh(laserPlaneGeo, laserPlaneMat);
            laserMesh.rotation.x = -Math.PI / 2;
            scene.add(laserMesh);

            // ========================================================
            // 🕹️ INTERACTIVE BUTTONS
            // ========================================================
            let show4D = true;
            let isWireframe = false;
            let rotSpeedMult = 1.0;
            const speeds = [1.0, 2.0, 0.0, 0.5];
            let speedIdx = 0;

            document.getElementById('btn-4d').addEventListener('click', () => {{
                show4D = !show4D;
                tesseractGroup.visible = show4D;
                waveGridMesh.visible = show4D;
                document.getElementById('btn-4d').classList.toggle('active', show4D);
                document.getElementById('btn-4d').textContent = show4D ? '🌀 4D Continuum Grid: ON' : '🌀 4D Continuum Grid: OFF';
            }});

            document.getElementById('btn-speed').addEventListener('click', () => {{
                speedIdx = (speedIdx + 1) % speeds.length;
                rotSpeedMult = speeds[speedIdx];
                document.getElementById('btn-speed').textContent = `Speed: ${{rotSpeedMult}}x`;
            }});

            document.getElementById('btn-wireframe').addEventListener('click', () => {{
                isWireframe = !isWireframe;
                boxMat.wireframe = isWireframe;
                tapeMat.wireframe = isWireframe;
                torMat1.wireframe = isWireframe;
                torMat2.wireframe = isWireframe;
                document.getElementById('btn-wireframe').style.borderColor = isWireframe ? '{glow_color}' : '';
            }});

            document.getElementById('btn-scan').addEventListener('click', () => {{
                isLaserActive = true;
                laserProgress = 0;
                document.getElementById('btn-scan').style.borderColor = '#38bdf8';
                document.getElementById('btn-scan').style.color = '#38bdf8';
                setTimeout(() => {{
                    document.getElementById('btn-scan').style.borderColor = '';
                    document.getElementById('btn-scan').style.color = '';
                }}, 2200);
            }});

            document.getElementById('btn-reset').addEventListener('click', () => {{
                camera.position.set(4.2, 2.8, 5.0);
                controls.target.set(0, 0.4, 0);
                controls.update();
            }});

            // 4D Projection Math
            function project4Dto3D(v4, aXW, aYW, aZW, scale) {{
                let x = v4[0], y = v4[1], z = v4[2], w = v4[3];
                let x1 = x * Math.cos(aXW) - w * Math.sin(aXW);
                let w1 = x * Math.sin(aXW) + w * Math.cos(aXW);
                let y1 = y * Math.cos(aYW) - w1 * Math.sin(aYW);
                let w2 = y * Math.sin(aYW) + w1 * Math.cos(aYW);
                let z1 = z * Math.cos(aZW) - w2 * Math.sin(aZW);
                let w3 = z * Math.sin(aZW) + w2 * Math.cos(aZW);

                const perspective = 1.0 / (2.5 - w3);
                return [x1 * perspective * scale, y1 * perspective * scale + 0.35, z1 * perspective * scale];
            }}

            // Animation Loop
            let clock = new THREE.Clock();
            function animate() {{
                requestAnimationFrame(animate);
                const t = clock.getElapsedTime() * (rotSpeedMult === 0 ? 0.05 : rotSpeedMult);

                // 1. 4D Tesseract Rotation
                if (show4D) {{
                    const aXW = t * 0.45;
                    const aYW = t * 0.35;
                    const aZW = t * 0.28;
                    const scale = 2.1;

                    const projected3D = [];
                    for (let i = 0; i < 16; i++) {{
                        const p3 = project4Dto3D(vertices4D[i], aXW, aYW, aZW, scale);
                        projected3D.push(p3);
                        vertexSpheres[i].position.set(p3[0], p3[1], p3[2]);
                    }}

                    const lineAttr = tesseractLinesGeo.attributes.position;
                    let ptr = 0;
                    for (let e = 0; e < edges4D.length; e++) {{
                        const pA = projected3D[edges4D[e][0]];
                        const pB = projected3D[edges4D[e][1]];
                        lineAttr.setXYZ(ptr++, pA[0], pA[1], pA[2]);
                        lineAttr.setXYZ(ptr++, pB[0], pB[1], pB[2]);
                    }}
                    lineAttr.needsUpdate = true;
                }}

                // 2. 4D Spacetime Ripple Grid
                if (show4D) {{
                    const posAttr = waveGridGeo.attributes.position;
                    for (let i = 0; i < posAttr.count; i++) {{
                        const vx = posAttr.getX(i);
                        const vz = posAttr.getZ(i);
                        const dist = Math.sqrt(vx * vx + vz * vz);
                        const waveY = Math.sin(vx * 0.35 + t * 1.2) * Math.cos(vz * 0.35 + t * 0.9) * 0.25 +
                                      Math.sin(dist * 0.5 - t * 1.8) * 0.18 - 0.72;
                        posAttr.setY(i, waveY);
                    }}
                    posAttr.needsUpdate = true;
                }}

                // 3. Laser Scan
                if (isLaserActive) {{
                    laserProgress += 0.04;
                    laserMesh.position.y = Math.sin(laserProgress * 2.5) * 0.7 + 0.3;
                    laserMesh.material.opacity = 0.85;
                    if (laserProgress > Math.PI * 2.2) {{
                        isLaserActive = false;
                        laserMesh.material.opacity = 0;
                    }}
                }}

                // 4. Smooth Floating Bob & Rotations
                mainGroup.position.y = Math.sin(t * 1.6) * 0.07 + 0.32;
                mainGroup.rotation.y += 0.007 * rotSpeedMult;
                shieldOrbitGroup.rotation.y += 0.018 * rotSpeedMult;
                shieldOrbitGroup.rotation.z = Math.sin(t * 1.1) * 0.18;

                // Pulsing Studio Lights
                statusLight.intensity = Math.sin(t * 2.8) * 0.4 + 2.4;
                ringMesh1.material.opacity = Math.sin(t * 2.5) * 0.2 + 0.7;

                // Ambient dust drift
                particleSystem.rotation.y = t * 0.02;

                controls.update();
                renderer.render(scene, camera);
            }}

            animate();

            // Resize Handler
            window.addEventListener('resize', () => {{
                const newW = window.innerWidth;
                const newH = {height};
                camera.aspect = newW / newH;
                camera.updateProjectionMatrix();
                renderer.setSize(newW, newH);
            }});
        </script>
    </body>
    </html>
    """
    return html_code


def render_cinematic_3d_background() -> str:
    """
    Generates a full-screen, GPU-accelerated 3D Cinematic Background using Three.js:
    - 3D Celestial Neural Starfield & dynamic holographic laser lattice
    - 3 Concentric cinematic orbital gyroscopes with iridescence
    - Floating 3D wireframe polyhedra crystals drifting in spacetime
    - Autonomous cinematic camera glide along a 3D Lissajous trajectory
    - Interactive cursor parallax inertia and chromatic lighting flares
    """
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        html, body {
            width: 100%;
            height: 100%;
            overflow: hidden;
            background: transparent !important;
        }
        #cinematicCanvas {
            width: 100%;
            height: 100%;
            display: block;
            position: absolute;
            top: 0;
            left: 0;
        }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
    <canvas id="cinematicCanvas"></canvas>

    <script>
        // Auto-pin iframe to fixed full viewport
        try {
            if (window.frameElement) {
                const fe = window.frameElement;
                fe.style.position = 'fixed';
                fe.style.top = '0';
                fe.style.left = '0';
                fe.style.width = '100vw';
                fe.style.height = '100vh';
                fe.style.zIndex = '0';
                fe.style.pointerEvents = 'none';
                fe.style.border = 'none';
                fe.style.opacity = '0.88';
                if (fe.parentElement) {
                    fe.parentElement.style.position = 'fixed';
                    fe.parentElement.style.top = '0';
                    fe.parentElement.style.left = '0';
                    fe.parentElement.style.width = '100vw';
                    fe.parentElement.style.height = '100vh';
                    fe.parentElement.style.zIndex = '0';
                    fe.parentElement.style.pointerEvents = 'none';
                }
            }
        } catch(e) {}

        const canvas = document.getElementById("cinematicCanvas");
        const renderer = new THREE.WebGLRenderer({
            canvas: canvas,
            antialias: true,
            alpha: true,
            powerPreference: "high-performance"
        });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));

        const scene = new THREE.Scene();
        scene.fog = new THREE.FogExp2(0x060913, 0.038);

        const camera = new THREE.PerspectiveCamera(52, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(0, 0, 14);

        // Lighting Rig
        const ambient = new THREE.AmbientLight(0xffffff, 0.75);
        scene.add(ambient);

        const cyanLight = new THREE.PointLight(0x38bdf8, 3.8, 35);
        cyanLight.position.set(-6, 5, 8);
        scene.add(cyanLight);

        const violetLight = new THREE.PointLight(0x818cf8, 3.4, 35);
        violetLight.position.set(7, -4, 6);
        scene.add(violetLight);

        const magentaLight = new THREE.PointLight(0xf472b6, 2.8, 30);
        magentaLight.position.set(0, 7, -4);
        scene.add(magentaLight);

        // 1. Constellation Starfield & Laser Lattice
        const particleCount = 260;
        const positions = new Float32Array(particleCount * 3);
        const velocities = [];
        const pColors = new Float32Array(particleCount * 3);

        const colorPalette = [
            new THREE.Color(0x38bdf8),
            new THREE.Color(0x818cf8),
            new THREE.Color(0xc084fc),
            new THREE.Color(0x34d399),
            new THREE.Color(0x60a5fa)
        ];

        for (let i = 0; i < particleCount; i++) {
            const i3 = i * 3;
            positions[i3] = (Math.random() - 0.5) * 36;
            positions[i3 + 1] = (Math.random() - 0.5) * 24;
            positions[i3 + 2] = (Math.random() - 0.5) * 30;

            velocities.push({
                x: (Math.random() - 0.5) * 0.012,
                y: (Math.random() - 0.5) * 0.012,
                z: (Math.random() - 0.5) * 0.012
            });

            const col = colorPalette[i % colorPalette.length];
            pColors[i3] = col.r;
            pColors[i3 + 1] = col.g;
            pColors[i3 + 2] = col.b;
        }

        const pGeo = new THREE.BufferGeometry();
        pGeo.setAttribute("position", new THREE.BufferAttribute(positions, 3));
        pGeo.setAttribute("color", new THREE.BufferAttribute(pColors, 3));

        const pMat = new THREE.PointsMaterial({
            size: 0.16,
            vertexColors: true,
            transparent: true,
            opacity: 0.85
        });
        const pMesh = new THREE.Points(pGeo, pMat);
        scene.add(pMesh);

        // Laser Connection Lines
        const maxConnections = 140;
        const linePositions = new Float32Array(maxConnections * 2 * 3);
        const lineGeo = new THREE.BufferGeometry();
        lineGeo.setAttribute("position", new THREE.BufferAttribute(linePositions, 3));
        const lineMat = new THREE.LineBasicMaterial({
            color: 0x38bdf8,
            transparent: true,
            opacity: 0.22,
            blending: THREE.AdditiveBlending
        });
        const lineMesh = new THREE.LineSegments(lineGeo, lineMat);
        scene.add(lineMesh);

        // 2. Cinematic 3D Floating Gyroscopes (Concentric Rings)
        const gyroGroup = new THREE.Group();
        scene.add(gyroGroup);
        gyroGroup.position.set(0, 0, -2);

        const r1 = new THREE.Mesh(
            new THREE.RingGeometry(4.2, 4.26, 80),
            new THREE.MeshBasicMaterial({ color: 0x38bdf8, side: THREE.DoubleSide, transparent: true, opacity: 0.45 })
        );
        gyroGroup.add(r1);

        const r2 = new THREE.Mesh(
            new THREE.RingGeometry(3.6, 3.65, 80),
            new THREE.MeshBasicMaterial({ color: 0x818cf8, side: THREE.DoubleSide, transparent: true, opacity: 0.4 })
        );
        r2.rotation.x = Math.PI / 3;
        gyroGroup.add(r2);

        const r3 = new THREE.Mesh(
            new THREE.RingGeometry(2.9, 2.94, 80),
            new THREE.MeshBasicMaterial({ color: 0xc084fc, side: THREE.DoubleSide, transparent: true, opacity: 0.35 })
        );
        r3.rotation.y = Math.PI / 4;
        gyroGroup.add(r3);

        // 3. Floating 3D Wireframe Polyhedra
        const crystalGroup = new THREE.Group();
        scene.add(crystalGroup);

        const icoGeo = new THREE.IcosahedronGeometry(1.6, 1);
        const icoMat = new THREE.MeshBasicMaterial({
            color: 0x38bdf8,
            wireframe: true,
            transparent: true,
            opacity: 0.35
        });
        const icoMesh = new THREE.Mesh(icoGeo, icoMat);
        icoMesh.position.set(-6.5, 2.5, -4);
        crystalGroup.add(icoMesh);

        const octGeo = new THREE.OctahedronGeometry(1.4, 0);
        const octMat = new THREE.MeshBasicMaterial({
            color: 0x818cf8,
            wireframe: true,
            transparent: true,
            opacity: 0.32
        });
        const octMesh = new THREE.Mesh(octGeo, octMat);
        octMesh.position.set(7.2, -2.8, -5);
        crystalGroup.add(octMesh);

        const torGeo = new THREE.TorusGeometry(1.2, 0.08, 16, 60);
        const torMat = new THREE.MeshBasicMaterial({
            color: 0xf472b6,
            transparent: true,
            opacity: 0.35
        });
        const torMesh = new THREE.Mesh(torGeo, torMat);
        torMesh.position.set(-4.5, -3.5, -3);
        crystalGroup.add(torMesh);

        // Mouse Interaction Parallax
        let mouseX = 0, mouseY = 0;
        let targetMouseX = 0, targetMouseY = 0;

        window.addEventListener("mousemove", (e) => {
            targetMouseX = (e.clientX / window.innerWidth - 0.5) * 2;
            targetMouseY = (e.clientY / window.innerHeight - 0.5) * 2;
        });

        // Cinematic Animation Loop
        let clock = 0;
        function animate() {
            requestAnimationFrame(animate);
            clock += 0.012;

            mouseX += (targetMouseX - mouseX) * 0.05;
            mouseY += (targetMouseY - mouseY) * 0.05;

            // Autonomous Cinematic Camera Glide (3D Lissajous trajectory + mouse tilt)
            camera.position.x = Math.sin(clock * 0.22) * 2.8 + mouseX * 2.2;
            camera.position.y = Math.cos(clock * 0.17) * 1.5 - mouseY * 1.8;
            camera.position.z = 13.5 + Math.sin(clock * 0.14) * 1.5;
            camera.lookAt(0, 0, 0);

            // Update Particles & Connections
            const pos = pGeo.attributes.position.array;
            let lineIdx = 0;
            const distThreshold = 4.0;

            for (let i = 0; i < particleCount; i++) {
                const i3 = i * 3;
                pos[i3] += velocities[i].x;
                pos[i3 + 1] += velocities[i].y;
                pos[i3 + 2] += velocities[i].z;

                // Bounds bounce
                if (Math.abs(pos[i3]) > 18) velocities[i].x *= -1;
                if (Math.abs(pos[i3 + 1]) > 12) velocities[i].y *= -1;
                if (Math.abs(pos[i3 + 2]) > 15) velocities[i].z *= -1;

                // Dynamic Lattice Connections
                if (lineIdx < maxConnections) {
                    for (let j = i + 1; j < Math.min(i + 14, particleCount); j++) {
                        const j3 = j * 3;
                        const dx = pos[i3] - pos[j3];
                        const dy = pos[i3 + 1] - pos[j3 + 1];
                        const dz = pos[i3 + 2] - pos[j3 + 2];
                        const dist = Math.sqrt(dx * dx + dy * dy + dz * dz);

                        if (dist < distThreshold && lineIdx < maxConnections) {
                            const l6 = lineIdx * 6;
                            linePositions[l6] = pos[i3];
                            linePositions[l6 + 1] = pos[i3 + 1];
                            linePositions[l6 + 2] = pos[i3 + 2];
                            linePositions[l6 + 3] = pos[j3];
                            linePositions[l6 + 4] = pos[j3 + 1];
                            linePositions[l6 + 5] = pos[j3 + 2];
                            lineIdx++;
                        }
                    }
                }
            }
            pGeo.attributes.position.needsUpdate = true;
            lineGeo.attributes.position.needsUpdate = true;
            lineMesh.geometry.setDrawRange(0, lineIdx * 2);

            // Gyroscope Rotations
            r1.rotation.z += 0.004;
            r2.rotation.y += 0.007;
            r3.rotation.x += 0.009;

            // Crystal Tumbling
            icoMesh.rotation.x += 0.005;
            icoMesh.rotation.y += 0.008;
            octMesh.rotation.y -= 0.006;
            octMesh.rotation.z += 0.007;
            torMesh.rotation.x += 0.008;
            torMesh.rotation.y += 0.004;

            // Light pulsing
            cyanLight.intensity = 3.2 + Math.sin(clock * 1.5) * 0.8;
            violetLight.intensity = 3.0 + Math.cos(clock * 1.8) * 0.7;

            renderer.render(scene, camera);
        }
        animate();

        window.addEventListener("resize", () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });
    </script>
</body>
</html>
"""
