import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';

// -------------------------------------------------------------
// Sample Receipts Database
// -------------------------------------------------------------
const SAMPLE_RECEIPTS = {
    sample_1: {
        id: "sample_1",
        name: "Sample 1: Urgent Electronics (REC-2026-8891)",
        order_id: "REC-2026-8891",
        customer: "Alex Morgan",
        store_name: "CODEX RETAIL STORE #402",
        purchase_date: "2026-08-27",
        total: 404.96,
        subtotal: 374.97,
        items: [
            { name: "Sony WH-1000XM5 Headphones", sku: "ELEC-9012", category: "Consumer Electronics & Gadgets", qty: 1, unit_price: 349.99, total_price: 349.99, condition: "New / Factory Sealed", policy_days: 30, warranty_days: 365 },
            { name: "Anker Powerline USB-C Cable 6ft", sku: "ACC-3312", category: "Consumer Electronics & Gadgets", qty: 1, unit_price: 19.99, total_price: 19.99, condition: "New", policy_days: 30, warranty_days: 365 },
            { name: "Microfiber Screen Cleaning Kit [CLEARANCE]", sku: "CLR-0041", category: "Final Sale & Clearance Items", qty: 1, unit_price: 4.99, total_price: 4.99, condition: "Final Sale - Non Refundable", policy_days: 0, warranty_days: 0 }
        ],
        raw_text: `========================================
            CODEX RETAIL STORE #402
       100 Innovation Way, Tech District
           Tel: (555) 019-2834
========================================
RECEIPT / ORDER ID: REC-2026-8891
CUSTOMER: Alex Morgan
DATE OF PURCHASE: 2026-08-27
CASHIER: Marcus T. (Terminal 4)
PAYMENT: Visa ending in 4102

ITEMS PURCHASED:
----------------------------------------
Item: Sony WH-1000XM5 Noise Canceling Headphones
SKU: ELEC-9012
Category: Consumer Electronics & Gadgets
Qty: 1
Unit Price: $349.99
Total: $349.99
Condition: New / Factory Sealed
Serial Number: SN-SNY-998241

Item: Anker Powerline USB-C Braided Cable 6ft
SKU: ACC-3312
Category: Consumer Electronics & Gadgets
Qty: 1
Unit Price: $19.99
Total: $19.99
Condition: New

Item: Microfiber Screen Cleaning Kit [CLEARANCE / FINAL SALE]
SKU: CLR-0041
Category: Final Sale & Clearance Items
Qty: 1
Unit Price: $4.99
Total: $4.99
Condition: Final Sale - Non Refundable
----------------------------------------
SUBTOTAL:       $374.97
SALES TAX (8%):  $29.99
TOTAL CHARGE:   $404.96
========================================`
    },
    sample_2: {
        id: "sample_2",
        name: "Sample 2: Mixed Apparel & Goods (REC-2026-9042)",
        order_id: "REC-2026-9042",
        customer: "Sarah Chen",
        store_name: "CODEX FLAGSHIP STORE #101",
        purchase_date: "2026-09-10",
        total: 396.24,
        subtotal: 363.94,
        items: [
            { name: "Patagonia Torrentshell 3L Rain Jacket (Black / M)", sku: "APP-1120", category: "Apparel, Clothing & Footwear", qty: 1, unit_price: 179.00, total_price: 179.00, condition: "New with tags attached", policy_days: 30, warranty_days: 90 },
            { name: "Nike Air Zoom Pegasus 40 Running Shoes (Size 10)", sku: "APP-5541", category: "Apparel, Clothing & Footwear", qty: 1, unit_price: 139.99, total_price: 139.99, condition: "New in original shoebox", policy_days: 30, warranty_days: 90 },
            { name: "Hydro Flask 32oz Insulated Water Bottle", sku: "HOME-7721", category: "Home & Kitchen Appliances", qty: 1, unit_price: 44.95, total_price: 44.95, condition: "New", policy_days: 45, warranty_days: 730 }
        ],
        raw_text: `========================================
           CODEX FLAGSHIP STORE #101
         500 Fifth Avenue, New York, NY
========================================
RECEIPT / ORDER ID: REC-2026-9042
CUSTOMER: Sarah Chen
DATE OF PURCHASE: 2026-09-10
----------------------------------------
Item: Patagonia Torrentshell 3L Rain Jacket
SKU: APP-1120
Qty: 1 | Price: $179.00
Item: Nike Air Zoom Pegasus 40 Running Shoes
SKU: APP-5541
Qty: 1 | Price: $139.99
Item: Hydro Flask 32oz Insulated Bottle
SKU: HOME-7721
Qty: 1 | Price: $44.95
----------------------------------------
TOTAL CHARGE:   $396.24`
    },
    sample_3: {
        id: "sample_3",
        name: "Sample 3: Expiring Winter Apparel (REC-2026-7734)",
        order_id: "REC-2026-7734",
        customer: "Jordan Lee",
        store_name: "CODEX DOWNTOWN #205",
        purchase_date: "2026-08-25",
        total: 183.35,
        subtotal: 168.99,
        items: [
            { name: "Merino Wool Crewneck Winter Sweater (Navy / L)", sku: "APP-8840", category: "Apparel, Clothing & Footwear", qty: 1, unit_price: 89.00, total_price: 89.00, condition: "New with tags attached", policy_days: 30, warranty_days: 90 },
            { name: "Soundcore Wireless Noise Isolating Earbuds", sku: "ELEC-4411", category: "Consumer Electronics & Gadgets", qty: 1, unit_price: 79.99, total_price: 79.99, condition: "New / Factory Sealed", policy_days: 30, warranty_days: 365 }
        ],
        raw_text: `========================================
             CODEX DOWNTOWN #205
         250 Market St, San Francisco, CA
========================================
RECEIPT / ORDER ID: REC-2026-7734
CUSTOMER: Jordan Lee
DATE OF PURCHASE: 2026-08-25
----------------------------------------
Item: Merino Wool Crewneck Winter Sweater
SKU: APP-8840 | Qty: 1 | Price: $89.00
Item: Soundcore Wireless Noise Isolating Earbuds
SKU: ELEC-4411 | Qty: 1 | Price: $79.99
TOTAL CHARGE:   $183.35`
    },
    sample_4: {
        id: "sample_4",
        name: "Sample 4: Shopkeeper Store Invoice (ORD-9912)",
        order_id: "ORD-9912",
        customer: "Tabish",
        store_name: "ABC Superstore #44",
        purchase_date: "2026-09-10",
        total: 428.74,
        subtotal: 396.99,
        items: [
            { name: "Apple AirPods Pro 2", sku: "ELEC-2001", category: "Consumer Electronics & Gadgets", qty: 1, unit_price: 249.00, total_price: 249.00, condition: "New", policy_days: 30, warranty_days: 365 },
            { name: "Levi's Denim Jacket", sku: "APP-3002", category: "Apparel, Clothing & Footwear", qty: 1, unit_price: 89.00, total_price: 89.00, condition: "New", policy_days: 30, warranty_days: 90 },
            { name: "Coffee Maker Blender", sku: "HOME-4003", category: "Home & Kitchen Appliances", qty: 1, unit_price: 49.00, total_price: 49.00, condition: "New", policy_days: 45, warranty_days: 730 },
            { name: "Clearout Phone Case [Clearance]", sku: "CLR-5004", category: "Final Sale & Clearance Items", qty: 1, unit_price: 9.99, total_price: 9.99, condition: "Final Sale", policy_days: 0, warranty_days: 0 }
        ],
        raw_text: `ABC Superstore #44\nOrder: ORD-9912\nDate: 2026-09-10\nCustomer: Tabish\n1. Apple AirPods Pro 2 - $249.00\n2. Levi's Denim Jacket - $89.00\n3. Coffee Maker Blender - $49.00\n4. Clearout Phone Case [Clearance] - $9.99\nSubtotal: $396.99\nTotal: $428.74`
    },
    sample_5: {
        id: "sample_5",
        name: "Sample 5: ABC Mart POS Invoice (20230922-001234)",
        order_id: "20230922-001234",
        customer: "Jane D.",
        store_name: "ABC MART – ONLINE STORE",
        purchase_date: "2026-09-18",
        total: 182.65,
        subtotal: 168.73,
        items: [
            { name: "Wireless Mouse", sku: "ELEC-110", category: "Consumer Electronics & Gadgets", qty: 1, unit_price: 24.99, total_price: 24.99, condition: "New", policy_days: 30, warranty_days: 365 },
            { name: "USB-C Hub", sku: "ELEC-111", category: "Consumer Electronics & Gadgets", qty: 2, unit_price: 15.50, total_price: 31.00, condition: "New", policy_days: 30, warranty_days: 365 },
            { name: "Laptop Sleeve", sku: "ACC-112", category: "Consumer Electronics & Gadgets", qty: 1, unit_price: 32.75, total_price: 32.75, condition: "New", policy_days: 30, warranty_days: 365 },
            { name: "500 GB SSD", sku: "ELEC-113", category: "Consumer Electronics & Gadgets", qty: 1, unit_price: 79.99, total_price: 79.99, condition: "New", policy_days: 30, warranty_days: 365 }
        ],
        raw_text: `ABC MART – ONLINE STORE\nReceipt #: 20230922-001234\nDate: 22 Sep 2026\n| 1. Wireless Mouse 1 $24.99 $24.99 |\n| 2. USB-C Hub 2 $15.50 $31.00 |\n| 3. Laptop Sleeve 1 $32.75 $32.75 |\n| 4. 500 GB SSD 1 $79.99 $79.99 |\nTOTAL DUE: $182.65`
    }
};

const MOCK_ORDERS = [
    { id: "ORD-1001", customer: "Alex Morgan", date: "2026-09-18", status: "Delivered", carrier: "FedEx", tracking: "FX-9823411029", items: "Sony WH-1000XM5 Headphones (x1), USB-C Charging Cable (x2)", address: "742 Evergreen Terrace, Springfield, IL" },
    { id: "ORD-1002", customer: "Alex Morgan", date: "2026-09-19", status: "Shipped", carrier: "UPS", tracking: "UPS-1Z999999999", items: "Patagonia Torrentshell Jacket (x1, Black/M)", address: "742 Evergreen Terrace, Springfield, IL" },
    { id: "ORD-1003", customer: "Sarah Chen", date: "2026-09-20", status: "Out for Delivery", carrier: "USPS", tracking: "9400111899562534", items: "Espresso Machine Pro (x1)", address: "100 Tech Boulevard, San Jose, CA" },
    { id: "ORD-1004", customer: "Jordan Lee", date: "2026-09-21", status: "Processing", carrier: "Standard Post", tracking: "PENDING", items: "Nike Air Zoom Pegasus 40 (x1, Size 10.5)", address: "456 Oak Avenue, Austin, TX" },
    { id: "ORD-1005", customer: "Emily Davis", date: "2026-09-15", status: "Delivered", carrier: "DHL", tracking: "DHL-549102834", items: "Apple iPad Air M2 (x1), Apple Pencil Pro (x1)", address: "12 Maple Drive, Seattle, WA" },
    { id: "ORD-1006", customer: "David Miller", date: "2026-09-12", status: "Cancelled", carrier: "N/A", tracking: "N/A", items: "4K Gaming Monitor 27-inch (x1)", address: "88 Beacon St, Boston, MA" }
];

// Current benchmark date in CODEX system
const CURRENT_DATE = (() => {
    const now = new Date();
    return new Date(Date.UTC(now.getFullYear(), now.getMonth(), now.getDate()));
})();

// Application State

let activeReceipt = SAMPLE_RECEIPTS.sample_1;

// Automatically load the built-in sample receipt into the CODEX backend
syncActiveReceiptToBackend();

let urgentItems = [];

let chartStyle = "bar"; // bar, line, area

let activeChartType = "velocity"; // velocity, returns, warranty

// -------------------------------------------------------------
// Deterministic Calculations
// -------------------------------------------------------------
function addDays(dateStr, days) {
    const d = new Date(dateStr + "T00:00:00Z");
    d.setUTCDate(d.getUTCDate() + days);
    return d.toISOString().split("T")[0];
}

function calculateAnalysis(receipt) {
    const pDate = new Date(receipt.purchase_date + "T00:00:00Z");
    const processedItems = receipt.items.map(item => {
        let returnDeadline = addDays(receipt.purchase_date, item.policy_days);
        let deadlineDate = new Date(returnDeadline + "T00:00:00Z");
        let diffMs = deadlineDate.getTime() - CURRENT_DATE.getTime();
        let daysRemaining = Math.round(diffMs / (1000 * 60 * 60 * 24));

        let returnStatus = "ACTIVE";
        let isUrgent = false;

        if (item.policy_days === 0 || item.category.toLowerCase().includes("final sale")) {
            returnStatus = "NON_RETURNABLE_FINAL_SALE";
            daysRemaining = 0;
        } else if (daysRemaining < 0) {
            returnStatus = "EXPIRED";
        } else if (daysRemaining <= 7) {
            returnStatus = "EXPIRING_SOON";
            isUrgent = true;
        }

        let warrantyDeadline = addDays(receipt.purchase_date, item.warranty_days);
        let wDate = new Date(warrantyDeadline + "T00:00:00Z");
        let wDiffMs = wDate.getTime() - CURRENT_DATE.getTime();
        let wDaysRemaining = Math.max(0, Math.round(wDiffMs / (1000 * 60 * 60 * 24)));
        let warrantyStatus = item.warranty_days === 0 ? "NO_WARRANTY" : (wDaysRemaining > 0 ? "ACTIVE" : "EXPIRED");

        return {
            ...item,
            return_deadline: returnDeadline,
            return_days_remaining: daysRemaining,
            return_status: returnStatus,
            is_urgent: isUrgent,
            warranty_deadline: warrantyDeadline,
            warranty_days_remaining: wDaysRemaining,
            warranty_status: warrantyStatus
        };
    });

    const urgent = processedItems.filter(i => i.is_urgent);
    return { items: processedItems, urgent };
}

// -------------------------------------------------------------
// 1. Three.js Background Scene (Cinematic Ambient Galaxy)
// -------------------------------------------------------------
let bgRenderer, bgScene, bgCamera;
let bgParticles, bgLines, bgGyros = [], bgCrystals = [];
let mouseX = 0, mouseY = 0, targetMouseX = 0, targetMouseY = 0;

function initCinematicBackground() {
    const canvas = document.getElementById("cinematicCanvas");
    if (!canvas) return;

    bgRenderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: "high-performance" });
    bgRenderer.setSize(window.innerWidth, window.innerHeight);
    bgRenderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));

    bgScene = new THREE.Scene();
    bgScene.fog = new THREE.FogExp2(0x060913, 0.038);

    bgCamera = new THREE.PerspectiveCamera(52, window.innerWidth / window.innerHeight, 0.1, 1000);
    bgCamera.position.set(0, 0, 14);

    // Lighting
    bgScene.add(new THREE.AmbientLight(0xffffff, 0.75));
    const light1 = new THREE.PointLight(0x38bdf8, 3.8, 35);
    light1.position.set(-6, 5, 8);
    bgScene.add(light1);
    const light2 = new THREE.PointLight(0x818cf8, 3.4, 35);
    light2.position.set(7, -4, 6);
    bgScene.add(light2);

    // Constellation particles
    const count = 260;
    const positions = new Float32Array(count * 3);
    const velocities = [];
    for (let i = 0; i < count; i++) {
        positions[i * 3] = (Math.random() - 0.5) * 36;
        positions[i * 3 + 1] = (Math.random() - 0.5) * 24;
        positions[i * 3 + 2] = (Math.random() - 0.5) * 30;
        velocities.push({
            x: (Math.random() - 0.5) * 0.012,
            y: (Math.random() - 0.5) * 0.012,
            z: (Math.random() - 0.5) * 0.012
        });
    }
    const pGeo = new THREE.BufferGeometry();
    pGeo.setAttribute("position", new THREE.BufferAttribute(positions, 3));
    const pMat = new THREE.PointsMaterial({ size: 0.16, color: 0x38bdf8, transparent: true, opacity: 0.85 });
    bgParticles = new THREE.Points(pGeo, pMat);
    bgParticles.userData.velocities = velocities;
    bgScene.add(bgParticles);

    // Laser Connection Lines
    const maxConn = 140;
    const linePos = new Float32Array(maxConn * 6);
    const lineGeo = new THREE.BufferGeometry();
    lineGeo.setAttribute("position", new THREE.BufferAttribute(linePos, 3));
    bgLines = new THREE.LineSegments(lineGeo, new THREE.LineBasicMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.22, blending: THREE.AdditiveBlending }));
    bgScene.add(bgLines);

    // Concentric Gyroscopes
    const gyroGroup = new THREE.Group();
    bgScene.add(gyroGroup);
    gyroGroup.position.set(0, 0, -2);
    const r1 = new THREE.Mesh(new THREE.RingGeometry(4.2, 4.26, 80), new THREE.MeshBasicMaterial({ color: 0x38bdf8, side: THREE.DoubleSide, transparent: true, opacity: 0.45 }));
    const r2 = new THREE.Mesh(new THREE.RingGeometry(3.6, 3.65, 80), new THREE.MeshBasicMaterial({ color: 0x818cf8, side: THREE.DoubleSide, transparent: true, opacity: 0.4 }));
    r2.rotation.x = Math.PI / 3;
    const r3 = new THREE.Mesh(new THREE.RingGeometry(2.9, 2.94, 80), new THREE.MeshBasicMaterial({ color: 0xc084fc, side: THREE.DoubleSide, transparent: true, opacity: 0.35 }));
    r3.rotation.y = Math.PI / 4;
    gyroGroup.add(r1, r2, r3);
    bgGyros = [r1, r2, r3];

    // Floating Wireframe Crystals
    const ico = new THREE.Mesh(new THREE.IcosahedronGeometry(1.6, 1), new THREE.MeshBasicMaterial({ color: 0x38bdf8, wireframe: true, transparent: true, opacity: 0.35 }));
    ico.position.set(-6.5, 2.5, -4);
    const oct = new THREE.Mesh(new THREE.OctahedronGeometry(1.4, 0), new THREE.MeshBasicMaterial({ color: 0x818cf8, wireframe: true, transparent: true, opacity: 0.32 }));
    oct.position.set(7.2, -2.8, -5);
    bgScene.add(ico, oct);
    bgCrystals = [ico, oct];

    window.addEventListener("mousemove", (e) => {
        targetMouseX = (e.clientX / window.innerWidth - 0.5) * 2;
        targetMouseY = (e.clientY / window.innerHeight - 0.5) * 2;
    });

    animateCinematicBg();
}

let bgClock = 0;
function animateCinematicBg() {
    requestAnimationFrame(animateCinematicBg);
    bgClock += 0.012;

    mouseX += (targetMouseX - mouseX) * 0.05;
    mouseY += (targetMouseY - mouseY) * 0.05;

    bgCamera.position.x = Math.sin(bgClock * 0.22) * 2.8 + mouseX * 2.2;
    bgCamera.position.y = Math.cos(bgClock * 0.17) * 1.5 - mouseY * 1.8;
    bgCamera.position.z = 13.5 + Math.sin(bgClock * 0.14) * 1.5;
    bgCamera.lookAt(0, 0, 0);

    // Particles & line updates
    const pos = bgParticles.geometry.attributes.position.array;
    const vels = bgParticles.userData.velocities;
    for (let i = 0; i < vels.length; i++) {
        pos[i * 3] += vels[i].x;
        pos[i * 3 + 1] += vels[i].y;
        pos[i * 3 + 2] += vels[i].z;
        if (Math.abs(pos[i * 3]) > 18) vels[i].x *= -1;
        if (Math.abs(pos[i * 3 + 1]) > 12) vels[i].y *= -1;
        if (Math.abs(pos[i * 3 + 2]) > 15) vels[i].z *= -1;
    }
    bgParticles.geometry.attributes.position.needsUpdate = true;

    // Gyro rotations
    if (bgGyros.length === 3) {
        bgGyros[0].rotation.z += 0.004;
        bgGyros[1].rotation.y += 0.007;
        bgGyros[2].rotation.x += 0.009;
    }

    bgCrystals.forEach(c => {
        c.rotation.x += 0.005;
        c.rotation.y += 0.008;
    });

    bgRenderer.render(bgScene, bgCamera);
}

// -------------------------------------------------------------
// 2. Three.js Interactive 3D / 4D Parcel Digital Twin Scene
// -------------------------------------------------------------
let twinRenderer, twinScene, twinCamera, twinControls;
let parcelMesh, statusRimLight, stageRing1, stageRing2, laserMesh, tesseractLines, waveGrid;
let show4D = true;
let isLaserActive = false;
let laserProgress = 0;
let timeWarpSpeed = 1.0;
let isWireframe = false;
let twinRaycaster, twinPointer;
let twinPointerDown = null;
let selectedTwinItemIndex = null;
let scanSequence = 0;

// 4D Geometry Definition
const vertices4D = [];
for (let i = 0; i < 16; i++) {
    vertices4D.push([
        (i & 1 ? 1 : -1) * 0.8,
        (i & 2 ? 1 : -1) * 0.8,
        (i & 4 ? 1 : -1) * 0.8,
        (i & 8 ? 1 : -1) * 0.8
    ]);
}
const edges4D = [];
for (let i = 0; i < 16; i++) {
    for (let j = i + 1; j < 16; j++) {
        let diff = 0;
        for (let k = 0; k < 4; k++) if (vertices4D[i][k] !== vertices4D[j][k]) diff++;
        if (diff === 1) edges4D.push([i, j]);
    }
}

function project4Dto3D(v4, aXW, aYW, aZW, scale) {
    let x = v4[0], y = v4[1], z = v4[2], w = v4[3];
    let x1 = x * Math.cos(aXW) - w * Math.sin(aXW);
    let w1 = x * Math.sin(aXW) + w * Math.cos(aXW);
    let y1 = y * Math.cos(aYW) - w1 * Math.sin(aYW);
    let w2 = y * Math.sin(aYW) + w1 * Math.cos(aYW);
    let z1 = z * Math.cos(aZW) - w2 * Math.sin(aZW);
    let w3 = z * Math.sin(aZW) + w2 * Math.cos(aZW);
    const p = 1.0 / (2.6 - w3);
    return [x1 * p * scale, y1 * p * scale + 0.35, z1 * p * scale];
}

function initTwinScene() {
    const container = document.getElementById("twinBox");
    const canvas = document.getElementById("twinCanvas");
    if (!container || !canvas) return;

    const width = container.clientWidth;
    const height = container.clientHeight || 420;

    twinRenderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
    twinRenderer.setSize(width, height);
    twinRenderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    twinScene = new THREE.Scene();
    twinCamera = new THREE.PerspectiveCamera(45, width / height, 0.1, 100);
    twinCamera.position.set(4.2, 2.8, 5.0);

    twinControls = new OrbitControls(twinCamera, canvas);
    twinControls.enableDamping = true;
    twinControls.dampingFactor = 0.05;
    twinControls.target.set(0, 0.4, 0);

    // Stage Pedestal
    const pedestalGeo = new THREE.CylinderGeometry(2.4, 2.6, 0.18, 48);
    const pedestalMat = new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.3, metalness: 0.8 });
    const pedestal = new THREE.Mesh(pedestalGeo, pedestalMat);
    pedestal.position.y = -0.7;
    twinScene.add(pedestal);

    // Concentric Stage LED Rings
    stageRing1 = new THREE.Mesh(new THREE.RingGeometry(2.35, 2.45, 64), new THREE.MeshBasicMaterial({ color: 0x38bdf8, side: THREE.DoubleSide }));
    stageRing1.rotation.x = Math.PI / 2;
    stageRing1.position.y = -0.6;
    stageRing1.userData.action = "return";
    twinScene.add(stageRing1);

    stageRing2 = new THREE.Mesh(new THREE.RingGeometry(1.6, 1.66, 64), new THREE.MeshBasicMaterial({ color: 0x10b981, side: THREE.DoubleSide }));
    stageRing2.rotation.x = Math.PI / 2;
    stageRing2.position.y = -0.605;
    stageRing2.userData.action = "warranty";
    twinScene.add(stageRing2);

    // -----------------------------------------------------------
    // Realistic 3D Shipping Parcel
    // -----------------------------------------------------------
    // The parcel keeps the existing holographic/animated behavior,
    // but now visually reads as a real cardboard ecommerce package.
    const parcelGeo = new THREE.BoxGeometry(1.7, 1.12, 1.38);
    const parcelMat = new THREE.MeshStandardMaterial({
        color: 0x9a6636,
        roughness: 0.78,
        metalness: 0.04,
        emissive: 0x082f49,
        emissiveIntensity: 0.055
    });
    parcelMesh = new THREE.Mesh(parcelGeo, parcelMat);
    parcelMesh.position.y = 0.35;
    parcelMesh.userData.action = "order";
    twinScene.add(parcelMesh);

    // Cardboard edge seams — makes the object read as a shipping carton.
    const parcelEdges = new THREE.LineSegments(
        new THREE.EdgesGeometry(parcelGeo),
        new THREE.LineBasicMaterial({
            color: 0x5f3b20,
            transparent: true,
            opacity: 0.75
        })
    );
    parcelEdges.scale.set(1.002, 1.002, 1.002);
    parcelMesh.add(parcelEdges);

    // Brown packing tape across the top.
    const tapeMat = new THREE.MeshStandardMaterial({
        color: 0xd6b46a,
        roughness: 0.58,
        metalness: 0.02
    });

    const topTape = new THREE.Mesh(
        new THREE.BoxGeometry(0.34, 0.018, 1.40),
        tapeMat
    );
    topTape.position.set(0, 0.569, 0);
    parcelMesh.add(topTape);

    // Second short tape strip crossing the main tape, like a sealed parcel.
    const crossTape = new THREE.Mesh(
        new THREE.BoxGeometry(1.68, 0.019, 0.28),
        tapeMat
    );
    crossTape.position.set(0, 0.571, 0);
    parcelMesh.add(crossTape);

    // Create a real-looking shipping label as a canvas texture.
    const labelCanvas = document.createElement("canvas");
    labelCanvas.width = 640;
    labelCanvas.height = 360;
    const labelCtx = labelCanvas.getContext("2d");

    if (labelCtx) {
        labelCtx.fillStyle = "#f4f1e8";
        labelCtx.fillRect(0, 0, 640, 360);

        labelCtx.strokeStyle = "#202020";
        labelCtx.lineWidth = 8;
        labelCtx.strokeRect(8, 8, 624, 344);

        labelCtx.fillStyle = "#111827";
        labelCtx.font = "bold 34px Arial";
        labelCtx.fillText("CODEX RETAIL", 28, 55);

        labelCtx.font = "bold 22px monospace";
        labelCtx.fillText(`ORDER: ${activeReceipt.order_id}`, 28, 94);

        labelCtx.font = "18px Arial";
        labelCtx.fillText(`SHIP TO: ${activeReceipt.customer}`, 28, 124);
        labelCtx.fillText("DIGITAL TWIN VERIFIED", 28, 151);

        // Barcode-like shipping graphic.
        let x = 28;
        const barcodeSeed = String(activeReceipt.order_id || "CODEX-001");
        for (let i = 0; i < 72; i++) {
            const code = barcodeSeed.charCodeAt(i % barcodeSeed.length);
            const barWidth = (code % 3) + 2;
            const gap = (code % 2) + 2;
            labelCtx.fillStyle = i % 7 === 0 ? "#111827" : "#252525";
            labelCtx.fillRect(x, 178, barWidth, 105);
            x += barWidth + gap;
            if (x > 610) break;
        }

        labelCtx.font = "bold 18px monospace";
        labelCtx.fillStyle = "#111827";
        labelCtx.fillText(String(activeReceipt.order_id), 28, 315);

        labelCtx.font = "bold 16px Arial";
        labelCtx.fillText("HANDLE WITH CARE", 405, 320);
    }

    const labelTexture = new THREE.CanvasTexture(labelCanvas);
    labelTexture.colorSpace = THREE.SRGBColorSpace;
    labelTexture.anisotropy = Math.min(twinRenderer.capabilities.getMaxAnisotropy(), 8);

    const labelMat = new THREE.MeshStandardMaterial({
        map: labelTexture,
        roughness: 0.82,
        metalness: 0.0,
        emissive: 0x082f49,
        emissiveIntensity: 0.025
    });

    // Front shipping label.
    const frontLabel = new THREE.Mesh(
        new THREE.PlaneGeometry(0.98, 0.55),
        labelMat
    );
    frontLabel.position.set(0.18, 0.35, 0.696);
    parcelMesh.add(frontLabel);

    // Small "FRAGILE" marker on the side.
    const fragileMat = new THREE.MeshStandardMaterial({
        color: 0xd94841,
        roughness: 0.7,
        metalness: 0.0
    });
    const fragileSticker = new THREE.Mesh(
        new THREE.PlaneGeometry(0.34, 0.22),
        fragileMat
    );
    fragileSticker.position.set(-0.82, 0.42, 0.02);
    fragileSticker.rotation.y = -Math.PI / 2;
    parcelMesh.add(fragileSticker);

    // Subtle cyan hologram outline around the parcel, preserving the
    // futuristic CODEX look without making the parcel look metallic.
    const holoEdges = new THREE.LineSegments(
        new THREE.EdgesGeometry(new THREE.BoxGeometry(1.76, 1.18, 1.44)),
        new THREE.LineBasicMaterial({
            color: 0x38bdf8,
            transparent: true,
            opacity: 0.28
        })
    );
    parcelMesh.add(holoEdges);

    // Status Rim Light
    statusRimLight = new THREE.PointLight(0xef4444, 3.5, 12);
    statusRimLight.position.set(0, 1.2, 0);
    twinScene.add(statusRimLight);

    // Ambient & Key light
    twinScene.add(new THREE.AmbientLight(0xffffff, 0.8));
    const dirLight = new THREE.DirectionalLight(0xffffff, 1.5);
    dirLight.position.set(5, 8, 4);
    twinScene.add(dirLight);

    // Laser Scan Beam
    const laserGeo = new THREE.RingGeometry(0.1, 1.4, 32);
    const laserMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8, side: THREE.DoubleSide, transparent: true, opacity: 0 });
    laserMesh = new THREE.Mesh(laserGeo, laserMat);
    laserMesh.rotation.x = Math.PI / 2;
    twinScene.add(laserMesh);

    // 4D Tesseract Lines
    const tessGeo = new THREE.BufferGeometry();
    const tessPos = new Float32Array(edges4D.length * 2 * 3);
    tessGeo.setAttribute("position", new THREE.BufferAttribute(tessPos, 3));
    tesseractLines = new THREE.LineSegments(tessGeo, new THREE.LineBasicMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.75 }));
    twinScene.add(tesseractLines);

    // 4D Riemannian Wave Grid
    const gridW = 5.0;
    const gridDivs = 20;
    const gridGeo = new THREE.PlaneGeometry(gridW, gridW, gridDivs, gridDivs);
    gridGeo.rotateX(-Math.PI / 2);
    const gridMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8, wireframe: true, transparent: true, opacity: 0.35 });
    waveGrid = new THREE.Mesh(gridGeo, gridMat);
    waveGrid.position.y = -0.68;
    twinScene.add(waveGrid);

    twinRaycaster = new THREE.Raycaster();
    twinPointer = new THREE.Vector2();

    attachTwinInteractions(canvas);

    updateTwinStatus();
    animateTwinScene();

    window.addEventListener("resize", () => {
        if (!container) return;
        const w = container.clientWidth;
        const h = container.clientHeight || 420;
        twinCamera.aspect = w / h;
        twinCamera.updateProjectionMatrix();
        twinRenderer.setSize(w, h);
    });
}

function updateTwinStatus() {
    if (!statusRimLight) return;
    const isUrgent = urgentItems.length > 0;
    const col = isUrgent ? 0xef4444 : 0x10b981;
    statusRimLight.color.setHex(col);
    stageRing2.material.color.setHex(col);

    const badge = document.getElementById("twinBadge");
    const orderEl = document.getElementById("twinOrder");
    if (orderEl) orderEl.innerText = activeReceipt.order_id;
    if (badge) {
        if (isUrgent) {
            badge.className = "twin-hud-badge urgent";
            const dueToday = urgentItems.filter(i => i.return_days_remaining === 0).length;
            badge.innerText = dueToday > 0
                ? `⚠️ ALERT: ${dueToday} ITEM(S) DUE TODAY`
                : `⚠️ ALERT: ${urgentItems.length} ITEM(S) EXPIRING SOON`;
        } else {
            badge.className = "twin-hud-badge safe";
            badge.innerText = "✅ ALL RETURN WINDOWS SAFE";
        }
    }
}

let twinClock = 0;
function animateTwinScene() {
    requestAnimationFrame(animateTwinScene);
    twinClock += 0.015 * timeWarpSpeed;

    // Parcel Floating & Rotation
    if (parcelMesh) {
        parcelMesh.position.y = 0.35 + Math.sin(twinClock * 1.5) * 0.06;
        parcelMesh.rotation.y += 0.008 * timeWarpSpeed;
    }

    // 4D Tesseract Rotation
    if (show4D && tesseractLines) {
        tesseractLines.visible = true;
        const aXW = twinClock * 0.45;
        const aYW = twinClock * 0.35;
        const aZW = twinClock * 0.28;
        const scale = 2.1;

        const projected = [];
        for (let i = 0; i < 16; i++) {
            projected.push(project4Dto3D(vertices4D[i], aXW, aYW, aZW, scale));
        }

        const posAttr = tesseractLines.geometry.attributes.position;
        let ptr = 0;
        for (let e = 0; e < edges4D.length; e++) {
            const pA = projected[edges4D[e][0]];
            const pB = projected[edges4D[e][1]];
            posAttr.setXYZ(ptr++, pA[0], pA[1], pA[2]);
            posAttr.setXYZ(ptr++, pB[0], pB[1], pB[2]);
        }
        posAttr.needsUpdate = true;
    } else if (tesseractLines) {
        tesseractLines.visible = false;
    }

    // 4D Spacetime Ripple Grid
    if (show4D && waveGrid) {
        waveGrid.visible = true;
        const pos = waveGrid.geometry.attributes.position;
        for (let i = 0; i < pos.count; i++) {
            const vx = pos.getX(i);
            const vz = pos.getZ(i);
            const dist = Math.sqrt(vx * vx + vz * vz);
            const waveY = Math.sin(vx * 0.35 + twinClock * 1.2) * Math.cos(vz * 0.35 + twinClock * 0.9) * 0.15 +
                Math.sin(dist * 0.5 - twinClock * 1.8) * 0.1;
            pos.setY(i, waveY);
        }
        pos.needsUpdate = true;
    } else if (waveGrid) {
        waveGrid.visible = false;
    }

    // Laser Scan
    if (isLaserActive && laserMesh) {
        laserProgress += 0.04;
        laserMesh.position.y = Math.sin(laserProgress * 2.5) * 0.7 + 0.35;
        laserMesh.material.opacity = 0.85;
        if (laserProgress > Math.PI * 2) {
            isLaserActive = false;
            laserMesh.material.opacity = 0;
            handleLaserScanComplete();
        }
    }

    twinControls.update();
    twinRenderer.render(twinScene, twinCamera);
}

// -------------------------------------------------------------
// 3. Functional 3D Order Twin Interactions
// -------------------------------------------------------------
function getTwinAnalysis() {
    return calculateAnalysis(activeReceipt);
}

function escapeHtml(value) {
    return String(value ?? "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function formatStatus(status) {
    return String(status || "UNKNOWN")
        .replaceAll("_", " ")
        .toLowerCase()
        .replace(/\b\w/g, c => c.toUpperCase());
}

function getOrderLifecycleStatus() {
    const matching = MOCK_ORDERS.find(o =>
        o.customer?.toLowerCase() === activeReceipt.customer?.toLowerCase()
    );
    return matching || {
        id: activeReceipt.order_id,
        customer: activeReceipt.customer,
        date: activeReceipt.purchase_date,
        status: "Delivered",
        carrier: "CODEX Logistics",
        tracking: "DIGITAL-TWIN",
        items: activeReceipt.items.map(i => `${i.name} (x${i.qty || 1})`).join(", "),
        address: "Order address available in receipt / order system"
    };
}

function ensureTwinOverlay() {
    let overlay = document.getElementById("codexTwinOverlay");
    if (overlay) return overlay;

    overlay = document.createElement("div");
    overlay.id = "codexTwinOverlay";
    overlay.style.cssText = `
    position:fixed;inset:0;z-index:9999;display:none;align-items:center;justify-content:center;
    padding:24px;background:rgba(2,6,23,.72);backdrop-filter:blur(8px);
  `;

    overlay.innerHTML = `
    <div id="codexTwinModal" style="
      width:min(760px,92vw);max-height:86vh;overflow:auto;
      background:linear-gradient(180deg,rgba(15,23,42,.98),rgba(2,6,23,.98));
      border:1px solid rgba(56,189,248,.32);border-radius:18px;
      box-shadow:0 25px 80px rgba(0,0,0,.55),0 0 40px rgba(56,189,248,.08);
      color:#e2e8f0;font-family:inherit;
    ">
      <div id="codexTwinModalBody"></div>
    </div>
  `;

    document.body.appendChild(overlay);
    overlay.addEventListener("click", (e) => {
        if (e.target === overlay) closeTwinOverlay();
    });

    return overlay;
}

function showTwinOverlay(title, bodyHtml, accent = "#38bdf8") {
    const overlay = ensureTwinOverlay();
    const body = document.getElementById("codexTwinModalBody");
    if (!body) return;

    body.innerHTML = `
    <div style="display:flex;align-items:center;justify-content:space-between;gap:16px;padding:18px 20px;border-bottom:1px solid rgba(255,255,255,.08);">
      <div>
        <div style="font-size:10px;letter-spacing:1.4px;color:${accent};font-family:'DM Mono',monospace;text-transform:uppercase;">CODEX DIGITAL TWIN</div>
        <div style="font-size:20px;font-weight:800;margin-top:4px;color:#fff;">${title}</div>
      </div>
      <button id="codexTwinClose" style="border:1px solid rgba(255,255,255,.12);background:rgba(255,255,255,.05);color:#cbd5e1;border-radius:10px;padding:8px 11px;cursor:pointer;font-size:16px;">✕</button>
    </div>
    <div style="padding:20px;">${bodyHtml}</div>
  `;

    overlay.style.display = "flex";
    document.getElementById("codexTwinClose")?.addEventListener("click", closeTwinOverlay);
}

function closeTwinOverlay() {
    const overlay = document.getElementById("codexTwinOverlay");
    if (overlay) overlay.style.display = "none";
}

function showOrderTwinDetails() {
    const analysis = getTwinAnalysis();
    const order = getOrderLifecycleStatus();
    const items = analysis.items.map((item, index) => `
    <div data-twin-item-index="${index}" style="display:grid;grid-template-columns:1fr auto;gap:12px;padding:13px 0;border-bottom:1px solid rgba(255,255,255,.07);">
      <div>
        <div style="font-weight:750;color:#fff;">${index + 1}. ${escapeHtml(item.name)}</div>
        <div style="font-size:11px;color:#94a3b8;margin-top:4px;">SKU ${escapeHtml(item.sku)} · ${escapeHtml(item.category)}</div>
      </div>
      <div style="text-align:right;">
        <div style="font-family:'DM Mono',monospace;color:#38bdf8;">$${Number(item.total_price || 0).toFixed(2)}</div>
        <div style="font-size:10px;color:#94a3b8;margin-top:4px;">${formatStatus(item.return_status)}</div>
      </div>
    </div>
  `).join("");

    showTwinOverlay("Order Digital Twin", `
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:18px;">
      <div style="padding:12px;border:1px solid rgba(56,189,248,.16);border-radius:12px;background:rgba(56,189,248,.04);">
        <div style="font-size:10px;color:#64748b;text-transform:uppercase;">Order</div>
        <div style="font-family:'DM Mono',monospace;color:#38bdf8;margin-top:4px;">${escapeHtml(activeReceipt.order_id)}</div>
      </div>
      <div style="padding:12px;border:1px solid rgba(56,189,248,.16);border-radius:12px;background:rgba(56,189,248,.04);">
        <div style="font-size:10px;color:#64748b;text-transform:uppercase;">Customer</div>
        <div style="color:#fff;margin-top:4px;font-weight:700;">${escapeHtml(activeReceipt.customer)}</div>
      </div>
      <div style="padding:12px;border:1px solid rgba(56,189,248,.16);border-radius:12px;background:rgba(56,189,248,.04);">
        <div style="font-size:10px;color:#64748b;text-transform:uppercase;">Total</div>
        <div style="color:#fff;margin-top:4px;font-weight:700;">$${Number(activeReceipt.total || 0).toFixed(2)}</div>
      </div>
    </div>

    <div style="padding:14px;border-radius:12px;background:rgba(16,185,129,.06);border:1px solid rgba(16,185,129,.18);margin-bottom:18px;">
      <div style="font-size:10px;color:#10b981;text-transform:uppercase;letter-spacing:1px;">Live order lifecycle</div>
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:12px;">
        ${["Ordered", "Shipped", "In Transit", "Delivered"].map((stage) => {
        const current = order.status?.toLowerCase() || "delivered";
        const rank = { ordered: 1, processing: 1, shipped: 2, "out for delivery": 3, "in transit": 3, delivered: 4, cancelled: 0 }[current] ?? 4;
        const stageRank = { Ordered: 1, Shipped: 2, "In Transit": 3, Delivered: 4 }[stage];
        const active = stageRank <= rank && current !== "cancelled";
        return `<div style="text-align:center;font-size:10px;color:${active ? '#e2e8f0' : '#64748b'};">
            <div style="width:22px;height:22px;margin:auto;border-radius:50%;display:flex;align-items:center;justify-content:center;border:1px solid ${active ? '#10b981' : 'rgba(255,255,255,.12)'};background:${active ? 'rgba(16,185,129,.16)' : 'rgba(255,255,255,.03)'};">${active ? '✓' : '·'}</div>
            <div style="margin-top:6px;">${stage}</div>
          </div>`;
    }).join("")}
      </div>
      <div style="margin-top:12px;font-size:11px;color:#94a3b8;">Status: <strong style="color:#fff;">${escapeHtml(order.status)}</strong> · ${escapeHtml(order.carrier)} · ${escapeHtml(order.tracking)}</div>
    </div>

    <div style="font-size:11px;letter-spacing:1px;color:#64748b;text-transform:uppercase;margin-bottom:4px;">Receipt-linked items</div>
    <div>${items}</div>
  `);
}

function showReturnTwinDetails() {
    const analysis = getTwinAnalysis();
    const rows = analysis.items.map(item => {
        let statusColor = "#10b981";
        if (item.return_status === "EXPIRING_SOON") statusColor = "#ef4444";
        if (item.return_status === "NON_RETURNABLE_FINAL_SALE" || item.return_status === "EXPIRED") statusColor = "#f59e0b";
        return `
      <div style="padding:12px 0;border-bottom:1px solid rgba(255,255,255,.07);">
        <div style="display:flex;justify-content:space-between;gap:10px;">
          <strong style="color:#fff;">${escapeHtml(item.name)}</strong>
          <span style="color:${statusColor};font-family:'DM Mono',monospace;font-size:11px;">${formatStatus(item.return_status)}</span>
        </div>
        <div style="font-size:11px;color:#94a3b8;margin-top:5px;">Policy: ${item.policy_days} days · Deadline: <code>${escapeHtml(item.return_deadline)}</code> · Remaining: ${item.return_days_remaining} day(s)</div>
      </div>
    `;
    }).join("");

    showTwinOverlay("Return Status Scan", `
    <div style="padding:13px;border-radius:12px;background:rgba(239,68,68,.06);border:1px solid rgba(239,68,68,.18);margin-bottom:16px;">
      <div style="font-size:11px;color:#fca5a5;">The outer 3D ring is linked to the active receipt's return-policy calculations.</div>
    </div>
    ${rows}
  `, "#ef4444");
}

function showWarrantyTwinDetails() {
    const analysis = getTwinAnalysis();
    const rows = analysis.items.map(item => {
        const active = item.warranty_status === "ACTIVE";
        return `
      <div style="padding:12px 0;border-bottom:1px solid rgba(255,255,255,.07);">
        <div style="display:flex;justify-content:space-between;gap:10px;">
          <strong style="color:#fff;">${escapeHtml(item.name)}</strong>
          <span style="color:${active ? '#38bdf8' : '#f59e0b'};font-family:'DM Mono',monospace;font-size:11px;">${escapeHtml(item.warranty_status)}</span>
        </div>
        <div style="font-size:11px;color:#94a3b8;margin-top:5px;">Coverage: ${item.warranty_days} days · Expiry: <code>${escapeHtml(item.warranty_deadline)}</code> · Remaining: ${item.warranty_days_remaining} day(s)</div>
      </div>
    `;
    }).join("");

    showTwinOverlay("Warranty Ring", `
    <div style="padding:13px;border-radius:12px;background:rgba(56,189,248,.06);border:1px solid rgba(56,189,248,.18);margin-bottom:16px;">
      <div style="font-size:11px;color:#bae6fd;">The inner 3D ring is linked to warranty coverage from the active receipt.</div>
    </div>
    ${rows}
  `, "#38bdf8");
}

async function handleLaserScanComplete() {
    scanSequence += 1;
    const analysis = getTwinAnalysis();
    const scanRows = analysis.items.map((item, index) => `
    <div style="display:flex;align-items:center;gap:12px;padding:10px 0;border-bottom:1px solid rgba(255,255,255,.07);">
      <div style="width:24px;height:24px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:rgba(56,189,248,.12);border:1px solid rgba(56,189,248,.3);color:#38bdf8;font-size:11px;">${index + 1}</div>
      <div style="flex:1;">
        <div style="color:#fff;font-weight:700;">${escapeHtml(item.name)}</div>
        <div style="color:#94a3b8;font-size:10px;margin-top:3px;">SKU ${escapeHtml(item.sku)} · Return ${escapeHtml(item.return_deadline)} · Warranty ${escapeHtml(item.warranty_deadline)}</div>
      </div>
      <div style="color:#10b981;font-family:'DM Mono',monospace;font-size:10px;">MATCHED</div>
    </div>
  `).join("");

    showTwinOverlay("Laser Scan Complete", `
    <div style="display:flex;align-items:center;gap:10px;padding:13px;border-radius:12px;background:rgba(16,185,129,.06);border:1px solid rgba(16,185,129,.18);margin-bottom:16px;">
      <span style="font-size:20px;">✓</span>
      <div>
        <div style="font-weight:800;color:#fff;">Receipt identity verified</div>
        <div style="font-size:11px;color:#94a3b8;margin-top:3px;">Order ${escapeHtml(activeReceipt.order_id)} · ${analysis.items.length} item(s) mapped into the digital twin.</div>
      </div>
    </div>
    ${scanRows}
    <div id="codexScanAgentResult" style="margin-top:16px;padding:12px;border-radius:12px;background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.07);font-size:11px;color:#94a3b8;">CODEX agent validation: checking receipt + policy context…</div>
  `);

    // Use the real backend agent after the visual scan, so this interaction also exercises RAG/tool orchestration.
    try {
        const response = await fetch("http://localhost:8000/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                message: `Run a concise verification for order ${activeReceipt.order_id}. Using the active receipt and internal store policy, summarize the return and warranty status for every purchased item.`
            })
        });
        const data = await response.json();
        const result = document.getElementById("codexScanAgentResult");
        if (result) {
            result.innerHTML = `<strong style="color:#38bdf8;">CODEX agent:</strong><br>${escapeHtml(data.response || "No validation response received.")}`;
        }
    } catch (error) {
        const result = document.getElementById("codexScanAgentResult");
        if (result) {
            result.innerHTML = `<strong style="color:#f59e0b;">Agent validation unavailable:</strong> ${escapeHtml(error.message)}`;
        }
    }
}

function startLaserScan() {
    isLaserActive = true;
    laserProgress = 0;
    selectedTwinItemIndex = null;
    if (laserMesh) {
        laserMesh.material.opacity = 0.85;
        laserMesh.scale.set(1, 1, 1);
    }
}

function attachTwinInteractions(canvas) {
    if (!canvas) return;

    const isInteractiveTarget = (object) => {
        let current = object;
        while (current) {
            if (current.userData?.action) return current;
            current = current.parent;
        }
        return null;
    };

    canvas.addEventListener("pointerdown", (event) => {
        twinPointerDown = { x: event.clientX, y: event.clientY };
    });

    canvas.addEventListener("pointerup", (event) => {
        if (!twinPointerDown || !twinRaycaster || !twinPointer || !twinCamera) return;
        const dx = event.clientX - twinPointerDown.x;
        const dy = event.clientY - twinPointerDown.y;
        twinPointerDown = null;

        // Ignore camera orbit drags; only treat a small pointer movement as a click.
        if ((dx * dx + dy * dy) > 36) return;

        const rect = canvas.getBoundingClientRect();
        twinPointer.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
        twinPointer.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

        twinRaycaster.setFromCamera(twinPointer, twinCamera);
        const hits = twinRaycaster.intersectObjects(
            [parcelMesh, stageRing1, stageRing2].filter(Boolean),
            false
        );

        if (!hits.length) return;
        const target = isInteractiveTarget(hits[0].object);
        const action = target?.userData?.action;

        if (action === "order") showOrderTwinDetails();
        else if (action === "return") showReturnTwinDetails();
        else if (action === "warranty") showWarrantyTwinDetails();
    });

    canvas.addEventListener("mousemove", (event) => {
        if (!twinRaycaster || !twinPointer || !twinCamera) return;
        const rect = canvas.getBoundingClientRect();
        twinPointer.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
        twinPointer.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
        twinRaycaster.setFromCamera(twinPointer, twinCamera);
        const hits = twinRaycaster.intersectObjects(
            [parcelMesh, stageRing1, stageRing2].filter(Boolean),
            false
        );
        canvas.style.cursor = hits.length ? "pointer" : "grab";
    });
}

// -------------------------------------------------------------
// 4. UI Rendering & Interaction
// -------------------------------------------------------------
function renderUI() {
    const analysis = calculateAnalysis(activeReceipt);
    urgentItems = analysis.urgent;

    // 1. Alert Banner
    const alertContainer = document.getElementById("alertBannerContainer");
    if (alertContainer) {
        if (urgentItems.length > 0) {
            alertContainer.innerHTML = `
        <div class="alert-banner urgent">
          <div class="alert-title">🚨 PROACTIVE ALERT: ${urgentItems.length} ITEM(S) EXPIRING SOON (&lt; 7 DAYS REMAINING)</div>
          The return window for these items is closing rapidly. Act promptly to request refund or exchange before deadlines elapse.
        </div>
      `;
        } else {
            alertContainer.innerHTML = `
        <div class="alert-banner safe">
          ✅ <strong>All Return Windows Active:</strong> No items on this receipt have return windows expiring within 7 days.
        </div>
      `;
        }
    }

    // 2. Active Receipt Status HUD in Sidebar
    const activeHud = document.getElementById("activeReceiptHud");
    if (activeHud) {
        activeHud.innerHTML = `
      <div class="active-receipt-title">● ACTIVE INGESTED RECEIPT</div>
      <div class="active-receipt-name">${activeReceipt.name}</div>
      <div class="active-receipt-meta">Order: <strong>${activeReceipt.order_id}</strong> | Items: <strong>${activeReceipt.items.length}</strong></div>
      <div class="active-receipt-meta">Customer: <strong>${activeReceipt.customer}</strong></div>
    `;
    }

    // 3. Key Metrics
    document.getElementById("mOrderId").innerText = activeReceipt.order_id;
    document.getElementById("mCustomer").innerText = activeReceipt.customer;
    document.getElementById("mStore").innerText = (activeReceipt.store_name || "CODEX Retail").slice(0, 22);
    document.getElementById("mDate").innerText = activeReceipt.purchase_date;
    document.getElementById("mTotal").innerText = `$${activeReceipt.total.toFixed(2)}`;

    // 4. Itemized Coverage List
    const itemizedList = document.getElementById("itemizedList");
    if (itemizedList) {
        itemizedList.innerHTML = analysis.items.map((it, idx) => {
            let badgeHtml = "";
            if (it.return_status === "EXPIRING_SOON") {
                badgeHtml = `<span class="status-badge-urgent">⚠️ Expiring Soon (${it.return_days_remaining}d left)</span>`;
            } else if (it.return_status === "NON_RETURNABLE_FINAL_SALE") {
                badgeHtml = `<span class="status-badge-final">❌ Final Sale (Non-Returnable)</span>`;
            } else if (it.return_status === "EXPIRED") {
                badgeHtml = `<span class="status-badge-final">❌ Expired</span>`;
            } else {
                const zeroDayText = it.return_days_remaining === 0 ? "⚠️ Due Today (0d left)" : `✅ Active (${it.return_days_remaining}d left)`;
                const zeroDayClass = it.return_days_remaining === 0 ? "status-badge-urgent" : "status-badge-active";
                badgeHtml = `<span class="${zeroDayClass}">${zeroDayText}</span>`;
            }

            return `
        <div class="item-row">
          <div>
            <div style="font-weight:700;font-size:14px;color:#fff;">${idx + 1}. ${it.name}</div>
            <div style="font-size:11px;color:#94a3b8;margin-top:2px;">
              📁 Category: <code>${it.category}</code> | 🏷️ SKU: <code>${it.sku}</code>
            </div>
            <div style="font-size:11px;color:#cbd5e1;margin-top:2px;">
              🔢 Qty: ${it.qty} | 💵 Unit Price: $${it.unit_price.toFixed(2)} | 💰 Total: $${it.total_price.toFixed(2)}
            </div>
          </div>
          <div>
            <div style="font-size:11px;color:#94a3b8;margin-bottom:4px;">Return Window:</div>
            ${badgeHtml}
            <div style="font-size:10px;color:#94a3b8;margin-top:4px;">Policy: ${it.policy_days}d | Deadline: <code>${it.return_deadline}</code></div>
          </div>
          <div>
            <div style="font-size:11px;color:#94a3b8;margin-bottom:4px;">Warranty Coverage:</div>
            <div style="font-weight:700;font-size:12px;color:#38bdf8;font-family:'DM Mono',monospace;">${it.warranty_status}</div>
            <div style="font-size:10px;color:#94a3b8;margin-top:4px;">Remaining: ${it.warranty_days_remaining}d | Expiry: <code>${it.warranty_deadline}</code></div>
          </div>
        </div>
      `;
        }).join("");
    }

    // 5. Raw Text View
    const rawCode = document.getElementById("rawReceiptCode");
    if (rawCode) rawCode.innerText = activeReceipt.raw_text;

    // 6. Update 3D Twin HUD
    updateTwinStatus();

    // 7. Render 5.6 Tera Chart
    renderChart();
}

// -------------------------------------------------------------
// 4. 5.6 Tera ChartGPT Canvas Renderer
// -------------------------------------------------------------
function renderChart() {
    const canvas = document.getElementById("chartCanvas");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    const width = canvas.clientWidth;
    const height = canvas.clientHeight || 220;
    canvas.width = width;
    canvas.height = height;

    ctx.clearRect(0, 0, width, height);

    // Background grid
    ctx.strokeStyle = "rgba(255, 255, 255, 0.05)";
    ctx.lineWidth = 1;
    for (let y = 30; y < height - 20; y += 40) {
        ctx.beginPath();
        ctx.moveTo(40, y);
        ctx.lineTo(width - 20, y);
        ctx.stroke();
    }

    let labels = [], data = [], colors = [];
    if (activeChartType === "velocity") {
        labels = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Today"];
        data = [120, 180, 240, 310, 280, 390, 440];
        colors = ["#38bdf8", "#38bdf8", "#38bdf8", "#38bdf8", "#38bdf8", "#38bdf8", "#10b981"];
        document.getElementById("chartTitle").innerText = "📈 7-Day Revenue Velocity & Sales Projections";
    } else if (activeChartType === "returns") {
        const analysis = calculateAnalysis(activeReceipt);
        labels = analysis.items.map(i => i.name.slice(0, 14) + "...");
        data = analysis.items.map(i => Math.max(0, i.return_days_remaining));
        colors = analysis.items.map(i => i.is_urgent ? "#ef4444" : "#10b981");
        document.getElementById("chartTitle").innerText = "⏳ Return Window Days Remaining Radar";
    } else {
        const analysis = calculateAnalysis(activeReceipt);
        labels = analysis.items.map(i => i.name.slice(0, 14) + "...");
        data = analysis.items.map(i => i.warranty_days_remaining);
        colors = ["#818cf8", "#38bdf8", "#c084fc", "#34d399"];
        document.getElementById("chartTitle").innerText = "🛡️ 365-Day Warranty Horizon Coverage";
    }

    const maxVal = Math.max(...data, 10);
    const chartW = width - 70;
    const chartH = height - 60;
    const barW = Math.min(50, chartW / (data.length * 1.6));

    if (chartStyle === "bar") {
        data.forEach((val, i) => {
            const h = (val / maxVal) * chartH;
            const x = 50 + (i * (chartW / data.length)) + ((chartW / data.length - barW) / 2);
            const y = height - 30 - h;

            const grad = ctx.createLinearGradient(0, y, 0, y + h);
            grad.addColorStop(0, colors[i % colors.length]);
            grad.addColorStop(1, "rgba(15, 23, 42, 0.4)");

            ctx.fillStyle = grad;
            ctx.beginPath();
            ctx.roundRect(x, y, barW, h, [4, 4, 0, 0]);
            ctx.fill();

            // Label
            ctx.fillStyle = "#94a3b8";
            ctx.font = "10px DM Mono";
            ctx.textAlign = "center";
            ctx.fillText(labels[i], x + barW / 2, height - 12);

            // Value
            ctx.fillStyle = "#fff";
            ctx.fillText(val, x + barW / 2, y - 6);
        });
    } else if (chartStyle === "line" || chartStyle === "area") {
        ctx.beginPath();
        const points = [];
        data.forEach((val, i) => {
            const x = 50 + (i * (chartW / (data.length - 1 || 1)));
            const y = height - 30 - ((val / maxVal) * chartH);
            points.push({ x, y, val, label: labels[i] });
            if (i === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        });

        if (chartStyle === "area") {
            ctx.lineTo(points[points.length - 1].x, height - 30);
            ctx.lineTo(points[0].x, height - 30);
            ctx.closePath();
            const areaGrad = ctx.createLinearGradient(0, 0, 0, height);
            areaGrad.addColorStop(0, "rgba(56, 189, 248, 0.35)");
            areaGrad.addColorStop(1, "rgba(56, 189, 248, 0.0)");
            ctx.fillStyle = areaGrad;
            ctx.fill();
        }

        ctx.strokeStyle = "#38bdf8";
        ctx.lineWidth = 3;
        ctx.stroke();

        points.forEach(p => {
            ctx.fillStyle = "#0284c7";
            ctx.beginPath();
            ctx.arc(p.x, p.y, 5, 0, Math.PI * 2);
            ctx.fill();
            ctx.strokeStyle = "#fff";
            ctx.lineWidth = 2;
            ctx.stroke();

            ctx.fillStyle = "#fff";
            ctx.font = "10px DM Mono";
            ctx.textAlign = "center";
            ctx.fillText(p.val, p.x, p.y - 10);
            ctx.fillStyle = "#94a3b8";
            ctx.fillText(p.label, p.x, height - 12);
        });
    }
}

// -------------------------------------------------------------
// 5. Google ✦ Gemini Search & AI Overview Cockpit
// -------------------------------------------------------------
function executeSearch(query) {
    const q = query.trim().toLowerCase();
    const resultsCard = document.getElementById("aiOverviewPanel");
    if (!resultsCard) return;

    const analysis = calculateAnalysis(activeReceipt);

    let directAnswer = "";
    let matchedProds = [];
    let sources = [
        { icon: "🏪", domain: "codex-retail.store", title: "CODEX Store Policy §2.1", snippet: "Electronics 30-day window, Apparel 30-day window, Final Sale strictly non-returnable." },
        { icon: "🧾", domain: "receipt.internal", title: `Order ${activeReceipt.order_id}`, snippet: `Ingested ${analysis.items.length} items purchased on ${activeReceipt.purchase_date}.` },
        { icon: "🚚", domain: "fedex.com", title: "Carrier Logistics Database", snippet: "Deterministic live tracking milestones for ORD shipments." }
    ];
    let paa = [
        "What restocking fee applies to opened electronics at CODEX?",
        "Can I return final-sale clearance items for store credit?",
        "How do I track an in-transit order with tracking number?"
    ];

    // Specific query matching
    if (q.includes("ord-") || q.includes("track") || q.includes("status")) {
        const foundOrder = MOCK_ORDERS.find(o => q.includes(o.id.toLowerCase())) || MOCK_ORDERS[0];
        directAnswer = `Order <strong>${foundOrder.id}</strong> for <strong>${foundOrder.customer}</strong> is currently <strong>${foundOrder.status}</strong> via <strong>${foundOrder.carrier}</strong> (Tracking: <code>${foundOrder.tracking}</code>). Shipping destination: ${foundOrder.address}.`;
        matchedProds = [
            { name: foundOrder.items, sku: foundOrder.id, unit_price: 299.99, qty: 1, return_status: foundOrder.status, return_days_remaining: 5, return_deadline: "2026-09-26", warranty_deadline: "2027-08-27" }
        ];
    } else if (q.includes("sony") || q.includes("headphone")) {
        const item = analysis.items.find(i => i.name.toLowerCase().includes("sony")) || analysis.items[0];
        directAnswer = `The <strong>${item.name}</strong> must be returned by <strong>${item.return_deadline}</strong> (<strong>${item.return_days_remaining} days remaining</strong>). Active warranty coverage continues until <strong>${item.warranty_deadline}</strong>.`;
        matchedProds = [item];
    } else if (q.includes("cable") || q.includes("anker")) {
        const item = analysis.items.find(i => i.name.toLowerCase().includes("anker")) || analysis.items[1];
        directAnswer = `The <strong>${item.name}</strong> has <strong>${item.return_days_remaining} days remaining</strong> for return (Deadline: <strong>${item.return_deadline}</strong>). SKU: <code>${item.sku}</code>, Price: $${item.unit_price.toFixed(2)}.`;
        matchedProds = [item];
    } else if (q.includes("final") || q.includes("clean") || q.includes("kit")) {
        directAnswer = `Final Sale items are <strong>strictly non-returnable and non-refundable</strong> per CODEX Store Policy §2.4. Return window is 0 days.`;
        matchedProds = analysis.items.filter(i => i.policy_days === 0);
    } else {
        // Default: full product breakdown
        directAnswer = `On Order <strong>${activeReceipt.order_id}</strong>, you purchased <strong>${analysis.items.length} items</strong> totaling <strong>$${activeReceipt.total.toFixed(2)}</strong> on ${activeReceipt.purchase_date}. ${urgentItems.length > 0 ? `⚠️ <strong>${urgentItems.length} item(s) have an urgent return window expiring soon!</strong>` : 'All return windows are active.'}`;
        matchedProds = analysis.items;
    }

    // Populate Panel
    document.getElementById("resQueryText").innerText = `"${query}"`;
    document.getElementById("directAnswerText").innerHTML = directAnswer;

    const srcGrid = document.getElementById("citationsGrid");
    if (srcGrid) {
        srcGrid.innerHTML = sources.map(s => `
      <div class="citation-card">
        <div class="citation-domain"><span>${s.icon}</span> <strong>${s.domain}</strong></div>
        <div class="citation-title">${s.title}</div>
        <div class="citation-snippet">${s.snippet}</div>
      </div>
    `).join("");
    }

    const prodGrid = document.getElementById("verifiedProductsGrid");
    if (prodGrid) {
        prodGrid.innerHTML = matchedProds.map(p => {
            let bClass = p.is_urgent ? "status-badge-urgent" : (p.return_days_remaining === 0 ? "status-badge-final" : "status-badge-active");
            let bText = p.is_urgent ? `⚠️ EXPIRING SOON (${p.return_days_remaining}d left)` : (p.return_days_remaining === 0 ? "❌ Final Sale" : `✅ Active (${p.return_days_remaining}d left)`);
            return `
        <div class="prod-detail-card">
          <div class="prod-detail-name">${p.name}</div>
          <span class="${bClass}">${bText}</span>
          <div style="font-size:11px;color:#94a3b8;margin-top:8px;display:flex;justify-content:space-between;">
            <span>SKU: <code>${p.sku}</code></span>
            <span><strong>$${(p.unit_price || 0).toFixed(2)}</strong> (x${p.qty || 1})</span>
          </div>
          <div style="font-size:11px;color:#cbd5e1;margin-top:4px;display:flex;justify-content:space-between;">
            <span>Deadline: <code>${p.return_deadline || 'N/A'}</code></span>
            <span style="color:#38bdf8;">Warranty: <code>${p.warranty_deadline || 'N/A'}</code></span>
          </div>
        </div>
      `;
        }).join("");
    }

    const paaRow = document.getElementById("paaRow");
    if (paaRow) {
        paaRow.innerHTML = paa.map(p => `
      <button class="cockpit-chip paa-btn" data-q="${p}">✦ ${p}</button>
    `).join("");
        document.querySelectorAll(".paa-btn").forEach(btn => {
            btn.addEventListener("click", () => {
                const qText = btn.getAttribute("data-q");
                document.getElementById("cockpitInput").value = qText;
                executeSearch(qText);
            });
        });
    }

    resultsCard.classList.add("active");
    resultsCard.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

// -------------------------------------------------------------
// 6. Event Listeners & Initialization
// -------------------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
    initCinematicBackground();
    initTwinScene();
    renderUI();

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape") closeTwinOverlay();
    });

    // Sample Receipt Buttons
    document.querySelectorAll(".sample-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            document.querySelectorAll(".sample-btn").forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            const sKey = btn.getAttribute("data-sample");
            if (SAMPLE_RECEIPTS[sKey]) {
                activeReceipt = SAMPLE_RECEIPTS[sKey];
                renderUI();
                syncActiveReceiptToBackend();
            }
        });
    });

    // File Upload Dropzone
    const dropzone = document.getElementById("fileDropzone");
    const fileInput = document.getElementById("fileInput");
    if (dropzone && fileInput) {
        dropzone.addEventListener("click", () => fileInput.click());
        fileInput.addEventListener("change", (e) => {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (evt) => {
                    const content = evt.target.result;
                    parseUploadedReceipt(file.name, content);
                };
                reader.readAsText(file);
            }
        });
    }

    // Paste Text Form
    const pasteBtn = document.getElementById("pasteSubmitBtn");
    if (pasteBtn) {
        pasteBtn.addEventListener("click", () => {
            const text = document.getElementById("pasteArea").value.trim();
            if (text) {
                parseUploadedReceipt("Pasted Receipt", text);

            }
        });
    }

    // Reset Button
    const resetBtn = document.getElementById("resetReceiptBtn");
    if (resetBtn) {
        resetBtn.addEventListener("click", () => {
            activeReceipt = SAMPLE_RECEIPTS.sample_1;
            document.querySelectorAll(".sample-btn").forEach(b => b.classList.remove("active"));
            document.querySelector('[data-sample="sample_1"]')?.classList.add("active");
            renderUI();
            syncActiveReceiptToBackend();
        });
    }

    // 3D Twin HUD Controls
    document.getElementById("btnToggle4D")?.addEventListener("click", (e) => {
        show4D = !show4D;
        e.target.classList.toggle("active", show4D);
        e.target.innerText = show4D ? "🌀 4D Tesseract [ON]" : "🌀 4D Tesseract [OFF]";
    });

    document.getElementById("btnLaser")?.addEventListener("click", () => {
        startLaserScan();
    });

    document.getElementById("btnWireframe")?.addEventListener("click", (e) => {
        isWireframe = !isWireframe;
        if (parcelMesh) parcelMesh.material.wireframe = isWireframe;
        e.target.classList.toggle("active", isWireframe);
    });

    document.getElementById("btnTimeWarp")?.addEventListener("click", (e) => {
        if (timeWarpSpeed === 1.0) timeWarpSpeed = 2.0;
        else if (timeWarpSpeed === 2.0) timeWarpSpeed = 4.0;
        else if (timeWarpSpeed === 4.0) timeWarpSpeed = 0.5;
        else timeWarpSpeed = 1.0;
        e.target.innerText = `⏱️ Time-Warp [${timeWarpSpeed}x]`;
    });

    document.getElementById("btnResetCamera")?.addEventListener("click", () => {
        if (twinCamera && twinControls) {
            twinCamera.position.set(4.2, 2.8, 5.0);
            twinControls.target.set(0, 0.4, 0);
            twinControls.update();
        }
    });

    // Search Cockpit Form
    const searchForm = document.getElementById("cockpitSearchForm");
    if (searchForm) {
        searchForm.addEventListener("submit", (e) => {
            e.preventDefault();
            const val = document.getElementById("cockpitInput").value.trim();
            if (val) executeSearch(val);
        });
    }

    // Suggestion Chips
    document.querySelectorAll(".cockpit-chip[data-q]").forEach(chip => {
        chip.addEventListener("click", () => {
            const q = chip.getAttribute("data-q");
            document.getElementById("cockpitInput").value = q;
            executeSearch(q);
        });
    });

    // Clear Results
    document.getElementById("btnClearResults")?.addEventListener("click", () => {
        document.getElementById("aiOverviewPanel")?.classList.remove("active");
    });

    // Chart Type & Style Switchers
    document.querySelectorAll(".chart-type-btn").forEach(b => {
        b.addEventListener("click", () => {
            document.querySelectorAll(".chart-type-btn").forEach(x => x.classList.remove("active"));
            b.classList.add("active");
            activeChartType = b.getAttribute("data-type");
            renderChart();
        });
    });

    document.querySelectorAll(".chart-style-btn").forEach(b => {
        b.addEventListener("click", () => {
            document.querySelectorAll(".chart-style-btn").forEach(x => x.classList.remove("active"));
            b.classList.add("active");
            chartStyle = b.getAttribute("data-style");
            renderChart();
        });
    });

    // Expanders
    document.querySelectorAll(".cyber-expander-header").forEach(h => {
        h.addEventListener("click", () => {
            h.parentElement.classList.toggle("open");
        });
    });

    // Chat Console
    const chatForm = document.getElementById("chatForm");

    if (chatForm) {
        chatForm.addEventListener("submit", async (e) => {
            e.preventDefault();

            const input = document.getElementById("chatInput");
            const msg = input.value.trim();

            if (!msg) return;

            input.value = "";
            appendChatMessage("user", msg);

            // Create a unique thinking message for THIS question
            const thinkingId = "codex-thinking-" + Date.now();

            appendChatMessage(
                "assistant",
                `<span id="${thinkingId}" class="codex-thinking">
        <span class="thinking-dot"></span>
        <span class="thinking-dot"></span>
        <span class="thinking-dot"></span>
        <span class="thinking-text">CODEX is thinking</span>
      </span>`
            );

            const thinkingElement = document.getElementById(thinkingId);
            const thinkingBubble = thinkingElement
                ? thinkingElement.closest(".message")
                : null;

            try {
                // Give the backend a maximum of 60 seconds
                const controller = new AbortController();
                const timeout = setTimeout(() => controller.abort(), 60000);

                const response = await fetch("http://localhost:8000/chat", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        message: msg
                    }),
                    signal: controller.signal
                });

                clearTimeout(timeout);

                const data = await response.json();

                if (!response.ok) {
                    throw new Error(data.detail || "API request failed");
                }

                // Convert basic Markdown formatting to HTML
                const formattedResponse = String(data.response || "")
                    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
                    .replace(/\n/g, "<br>");

                // Replace THIS question's thinking message
                if (thinkingBubble) {
                    thinkingBubble.innerHTML = formattedResponse;
                } else {
                    appendChatMessage("assistant", formattedResponse);
                }

            } catch (error) {

                let errorMessage = error.message;

                if (error.name === "AbortError") {
                    errorMessage =
                        "CODEX took too long to respond. Please try the question again.";
                }

                if (thinkingBubble) {
                    thinkingBubble.innerHTML =
                        `<strong>CODEX connection error:</strong><br>${errorMessage}`;
                } else {
                    appendChatMessage(
                        "assistant",
                        `<strong>CODEX connection error:</strong><br>${errorMessage}`
                    );
                }
            }
        });
    }

    // Populate Mock Orders Table
    const ordersTableBody = document.getElementById("ordersTableBody");
    if (ordersTableBody) {
        ordersTableBody.innerHTML = MOCK_ORDERS.map(o => `
      <tr style="border-bottom:1px solid rgba(255,255,255,0.06);">
        <td style="padding:6px 8px;font-family:'DM Mono',monospace;color:#38bdf8;">${o.id}</td>
        <td style="padding:6px 8px;">${o.customer}</td>
        <td style="padding:6px 8px;"><span class="status-badge-active">${o.status}</span></td>
        <td style="padding:6px 8px;">${o.carrier}</td>
        <td style="padding:6px 8px;font-family:'DM Mono',monospace;font-size:10px;">${o.tracking}</td>
      </tr>
    `).join("");
    }
});


async function syncActiveReceiptToBackend() {
    try {
        const response = await fetch("http://127.0.0.1:8000/load-receipt", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ receipt: activeReceipt.raw_text })
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.detail || "Receipt ingestion failed");
        console.log("CODEX active receipt synced:", data);
        return data;
    } catch (error) {
        console.error("CODEX active receipt sync failed:", error);
        return null;
    }
}

function appendChatMessage(role, text) {
    const list = document.getElementById("chatHistoryList");
    if (!list) return;
    const bubble = document.createElement("div");
    bubble.className = `chat-bubble ${role}`;
    bubble.innerHTML = text;
    list.appendChild(bubble);
    list.scrollTop = list.scrollHeight;
}

function parseUploadedReceipt(name, text) {
    // Simple flexible parser for custom uploaded text
    const lines = text.split("\n");
    let customer = "Shopper";
    let order_id = "REC-UPLOAD-" + Math.floor(Math.random() * 9000 + 1000);
    let total = 0;
    let items = [];

    lines.forEach(l => {
        if (l.toLowerCase().includes("customer:")) customer = l.split(":")[1].trim();
        if (l.toLowerCase().includes("order") && l.includes(":")) order_id = l.split(":")[1].trim();
        if (l.includes("$") && (l.includes("-") || l.includes("|") || l.includes("."))) {
            const match = l.match(/([^$\n]+)\$?(\d+\.\d{2})/);
            if (match) {
                const iName = match[1].replace(/^[|\d.\s-]+/, "").trim();
                const price = parseFloat(match[2]);
                if (iName.length > 2 && price > 0) {
                    items.push({
                        name: iName,
                        sku: "SKU-" + Math.floor(Math.random() * 9000 + 1000),
                        category: iName.toLowerCase().includes("jacket") || iName.toLowerCase().includes("shoe") ? "Apparel, Clothing & Footwear" : "Consumer Electronics & Gadgets",
                        qty: 1,
                        unit_price: price,
                        total_price: price,
                        condition: "Standard",
                        policy_days: 30,
                        warranty_days: 365
                    });
                    total += price;
                }
            }
        }
    });

    if (items.length === 0) {
        items = [
            { name: "General Merchandise Item", sku: "GEN-101", category: "Consumer Electronics & Gadgets", qty: 1, unit_price: 49.99, total_price: 49.99, condition: "Standard", policy_days: 30, warranty_days: 365 }
        ];
        total = 49.99;
    }

    activeReceipt = {
        id: "uploaded",
        name: `📄 ${name}`,
        order_id: order_id,
        customer: customer,
        store_name: "CODEX STORE",
        purchase_date: "2026-09-15",
        total: total,
        subtotal: total,
        items: items,
        raw_text: text
    };

    renderUI();
    syncActiveReceiptToBackend();
}
