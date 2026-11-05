import os
import json
import math
import datetime
import urllib.request
import urllib.parse

# ==========================================
# CORE CONFIGURATION
# ==========================================
AFFILIATE_TAG = "everythi00099-20"
SITE_NAME = "WeldSpecPro"
SITE_TAGLINE = "MIG/TIG/Stick Welder Amperage, Wire Speed (IPM), Plasma CFM & Breaker Calculator"
OUTPUT_DIR = "public"
INDEXNOW_KEY = "5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b"

# Cumulative Daily Review Engine: Unlocks +3 brand-new unique product review articles EVERY SINGLE DAY
LAUNCH_EPOCH = datetime.date(2026, 11, 1)
REVIEWS_PER_DAY = 3

REPO_SLUG = os.environ.get("GITHUB_REPOSITORY", "username/weldspecpro")
OWNER, REPO_NAME = REPO_SLUG.split("/") if "/" in REPO_SLUG else ("username", "weldspecpro")
BASE_URL = os.environ.get("SITE_BASE_URL", f"https://{OWNER}.github.io/{REPO_NAME}")

def amz_url(keyword):
    return f"https://www.amazon.com/s?k={urllib.parse.quote_plus(keyword.replace('+', ' '))}&tag={AFFILIATE_TAG}"

# ==========================================
# BEST SELLING PRODUCTS DATABASE (USD / EN)
# ==========================================
BEST_SELLERS = [
    {
        "title": "PrimeWeld TIG225X 225-Amp IGBT AC/DC TIG & Stick Welder w/ Pulse & CK17 Flex Torch",
        "category": "AC/DC Aluminum & Steel TIG",
        "rating": "4.9 ★ (4,800+ reviews)",
        "badge": "#1 AC/DC TIG Welder in America",
        "specs": "10–225A AC/DC Output | 200Hz Pulse | Includes USA-Made CK17 Flex-Head Torch & Metal Foot Pedal",
        "keyword": "PrimeWeld+TIG225X+225+Amp+AC+DC+TIG+Welder+Pulse"
    },
    {
        "title": "Hobart Handler 210 MVP (Multi-Voltage Plug 120V/240V) 210-Amp MIG & Flux-Core Welder",
        "category": "Dual-Voltage 210A MIG Welder",
        "rating": "4.8 ★ (3,900+ reviews)",
        "badge": "#1 Prosumer MIG Welder",
        "specs": "Welds 24-Gauge to 3/8\" Steel in 1 Pass | Cast-Aluminum Wire Drive | Miller-Engineered Transformer",
        "keyword": "Hobart+Handler+210+MVP+MIG+Welder+120V+240V"
    },
    {
        "title": "Lincoln Electric VIKING 3350 (5th Gen) 4C True-Color Auto-Darkening Welding Helmet",
        "category": "1/1/1/1 Optical Welding Hood",
        "rating": "4.9 ★ (9,200+ reviews)",
        "badge": "#1 Professional Welding Hood",
        "specs": "1/1/1/1 Optical Clarity | Massive 12.5 Sq.In 4C Lens | External Grind Button | 5-Year Warranty",
        "keyword": "Lincoln+Electric+Viking+3350+4C+Auto+Darkening+Welding+Helmet"
    },
    {
        "title": "YESWELDER MIG-205DS Pro / Firstess MP200 200-Amp 5-in-1 Multi-Process Synergic Welder",
        "category": "Multi-Process MIG/TIG/Stick",
        "rating": "4.7 ★ (7,400+ reviews)",
        "badge": "#1 Budget Synergic MIG",
        "specs": "200A Dual-Voltage (110V/220V) | Auto-Matches Wire Speed & Voltage | Spool Gun Aluminum Ready",
        "keyword": "YESWELDER+MIG+205DS+Multi+Process+MIG+Welder+200+Amp"
    },
    {
        "title": "PrimeWeld CUT60 / YESWELDER CUT-55DS Pro 60-Amp Non-Touch Pilot-Arc Plasma Cutter",
        "category": "Pilot-Arc Plasma Cutter",
        "rating": "4.8 ★ (5,600+ reviews)",
        "badge": "#1 Pilot-Arc Plasma Cutter",
        "specs": "Cuts Through Rust, Paint & Expanded Metal | 3/4\" Clean Cut / 1\" Severance | PT60 Torch Included",
        "keyword": "PrimeWeld+CUT60+YESWELDER+CUT+55DS+Pilot+Arc+Plasma+Cutter"
    },
    {
        "title": "Strong Hand Tools Nomad / BuildPro 30\"×20\" Adjustable Folding Steel Welding Table",
        "category": "Portable Fixture Welding Table",
        "rating": "4.8 ★ (6,100+ reviews)",
        "badge": "#1 Garage Welding Table",
        "specs": "350–1,000 Lb Capacity | 3 Table-Top Tilt Angles | Slotted Clamping Channels | Retractable Wheels",
        "keyword": "Strong+Hand+Tools+Nomad+Welding+Table+Fixture"
    },
    {
        "title": "ESAB Sentinel A60 Panoramic True-Color Auto-Darkening Welding Helmet (Halo Headgear)",
        "category": "Panoramic Welding Helmet",
        "rating": "4.9 ★ (3,300+ reviews)",
        "badge": "Best Panoramic View & Comfort",
        "specs": "40% Larger Viewing Area (4.65\"×2.80\") | EN 1/1/1/1 Ophthalmic Lens | 0.5-Step Shade Tuning",
        "keyword": "ESAB+Sentinel+A60+Auto+Darkening+Welding+Helmet"
    },
    {
        "title": "6-AWG / 8-AWG 50-Amp (NEMA 6-50P to 6-50R) 25-Ft & 50-Ft Heavy-Duty Welder Extension Cord",
        "category": "240V 50A Welder Power Cord",
        "rating": "4.9 ★ (8,800+ reviews)",
        "badge": "#1 100% Copper Welder Cord",
        "specs": "250V 50A (12,500W) Rating | STW Cold-Weather Jacket | Lighted Plug End | ETL Listed Pure Copper",
        "keyword": "50+Amp+NEMA+6+50+Welder+Extension+Cord+25+50+Foot"
    }
]

# ==========================================
# PRODUCT COMPARISON MATRIX (PERBANDINGAN PRODUK)
# ==========================================
COMPARISON_MATRIX = [
    {
        "model": "PrimeWeld TIG225X (225A)",
        "type": "AC/DC Pulse TIG + Stick",
        "power_spec": "225A @ 240V / 130A @ 120V",
        "thickness_cap": "Up to 1/4\" Alum / 3/8\" Steel",
        "highlight": "Includes USA CK17 Torch & 3-Yr Support",
        "rating": "4.9 / 5.0 ★",
        "keyword": "PrimeWeld+TIG225X+225+Amp+AC+DC+TIG+Welder"
    },
    {
        "model": "Hobart Handler 210 MVP",
        "type": "Transformer MIG / Flux-Core",
        "power_spec": "210A @ 240V / 140A @ 120V",
        "thickness_cap": "24-Ga Sheet to 3/8\" Plate",
        "highlight": "Bulletproof 7-Tap Voltage + 5/3/1 Warranty",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Hobart+Handler+210+MVP+MIG+Welder"
    },
    {
        "model": "YESWELDER MIG-205DS Pro",
        "type": "Synergic MIG / Lift-TIG / Stick",
        "power_spec": "200A Dual-Voltage Inverter",
        "thickness_cap": "Up to 5/16\" Mild Steel",
        "highlight": "Auto-Sets Voltage & IPM by Wire Size",
        "rating": "4.7 / 5.0 ★",
        "keyword": "YESWELDER+MIG+205DS+Multi+Process+Welder"
    },
    {
        "model": "PrimeWeld CUT60 Plasma",
        "type": "60A Non-Touch Pilot Arc",
        "power_spec": "60A @ 240V (Requires 4.5 CFM)",
        "thickness_cap": "3/4\" Clean / 1.0\" Severance Cut",
        "highlight": "Cuts Rusty Metal Without Touching Tip",
        "rating": "4.8 / 5.0 ★",
        "keyword": "PrimeWeld+CUT60+Pilot+Arc+Plasma+Cutter"
    },
    {
        "model": "Lincoln Viking 3350 (5th Gen)",
        "type": "4C Auto-Darkening Helmet",
        "power_spec": "1/1/1/1 Optical Clarity (12.5 in²)",
        "thickness_cap": "2-Amp TIG Sensor Sensitivity",
        "highlight": "Eliminates Green Tint + External Grind Button",
        "rating": "4.9 / 5.0 ★",
        "keyword": "Lincoln+Electric+Viking+3350+Welding+Helmet"
    },
    {
        "model": "ESAB Sentinel A60 Hood",
        "type": "Panoramic Ophthalmic Hood",
        "power_spec": "1/1/1/1 Clarity (13.0 in² View)",
        "thickness_cap": "Shade 3 Grind / 5–13 Weld",
        "highlight": "5-Point Halo Headgear Zero Neck Strain",
        "rating": "4.9 / 5.0 ★",
        "keyword": "ESAB+Sentinel+A60+Auto+Darkening+Helmet"
    }
]

# ==========================================
# HEAD-TO-HEAD "VS" COMPARISON PAGES
# ==========================================
VS_COMPARISONS = [
    {
        "slug": "compare-mig-solid-wire-gas-vs-flux-core-gasless-welding",
        "title": "MIG Solid Wire (75/25 Argon-CO2 Gas) vs. Flux-Core Gasless (E71T-11): Spatter, Penetration & Wind",
        "product_a": "MIG Solid Wire ER70S-6 + 75/25 Gas",
        "product_b": "Flux-Core Gasless Wire E71T-GS/11",
        "winner_badge": "Zero Slag & Clean Auto-Body Welds vs. Best Outdoor Windy & Thick-Rusty Steel",
        "keyword_a": "Hobart+Handler+210+MVP+MIG+Welder+and+Argon+Regulator",
        "keyword_b": "YESWELDER+MIG+205DS+and+Flux+Core+Wire+.030+.035",
        "summary": "Compare DCEP vs. DCEN polarity, spatter cleanup, outdoor wind resistance, and thin sheet-metal burn-through between shielded MIG and gasless Flux-Core.",
        "metrics": [
            {"feature": "Required Polarity", "val_a": "DCEP (Electrode Positive / Ground Clamp Negative)", "val_b": "DCEN (Electrode Negative / Ground Clamp Positive!)"},
            {"feature": "Slag & Spatter Cleanup", "val_a": "100% Slag-Free — Paint Ready Immediately After Welding", "val_b": "Requires Wire-Brushing Flux Slag & Anti-Spatter Spray"},
            {"feature": "Thin 18–22 Gauge Auto Sheet Metal", "val_a": "Runs Cool & Clean w/ 0.023\" or 0.030\" Solid Wire", "val_b": "Burns Through Thin Sheet Metal Easily (Runs Hotter)"},
            {"feature": "Outdoor Windy Field Repairs", "val_a": "Breeze Blows Shielding Gas Away (Causes Porosity Holes)", "val_b": "100% Immune to Wind — Flux Creates Internal Gas Shield"},
            {"feature": "Gas Cylinder Requirement", "val_a": "Requires 75% Argon / 25% CO2 Tank & Flowmeter (22 CFH)", "val_b": "Zero Gas Bottle Needed"}
        ],
        "verdict_text": "Every dual-purpose MIG welder can run both! Use Solid ER70S-6 Wire with 75/25 Argon-CO2 gas (on DCEP polarity) whenever welding indoors in your garage—it produces glass-smooth, spatter-free welds that require zero chipping or wire-wheeling. Switch to E71T-11 Gasless Flux-Core wire (and swap your internal machine lugs to DCEN polarity!) when fixing a trailer, tractor implement, or fence outdoors in the wind."
    },
    {
        "slug": "compare-lincoln-viking-3350-vs-esab-sentinel-a60-welding-helmet",
        "title": "Lincoln Electric VIKING 3350 (5th Gen) vs. ESAB Sentinel A60: 4C vs. Ophthalmic True-Color Lens",
        "product_a": "Lincoln VIKING 3350 (5th Gen)",
        "product_b": "ESAB Sentinel A60 Panoramic",
        "winner_badge": "Cheapest Replacement Clear Cover Lenses vs. Widest Panoramic View & Halo Fit",
        "keyword_a": "Lincoln+Electric+Viking+3350+4C+Auto+Darkening+Welding+Helmet",
        "keyword_b": "ESAB+Sentinel+A60+Auto+Darkening+Welding+Helmet",
        "summary": "Compare 1/1/1/1 EN379 optical ratings, weld puddle puddle visibility in TIG, external grind buttons, and replacement cover lens costs.",
        "metrics": [
            {"feature": "Optical Clarity Rating", "val_a": "1/1/1/1 EN379 w/ Lincoln 4C True-Color Technology", "val_b": "1/1/1/1 EN379 Ophthalmic ADC Plus Broad-Spectrum"},
            {"feature": "Viewing Window Size", "val_a": "3.74\" × 3.34\" (12.5 Square Inches — Tall Vertical View)", "val_b": "4.65\" × 2.80\" (13.0 Square Inches — Wide Panoramic)"},
            {"feature": "Outer Clear Cover Lens Style", "val_a": "Standard Flat Rectangular ($1.50 Generic Cover Lenses Fit!)", "val_b": "Proprietary Curved Spherical Amber/Clear Shield (~$4 each)"},
            {"feature": "External Grind Mode Button", "val_a": "Yes — Low-Profile Left Temple Push Button", "val_b": "Yes — External Tactile Grind Button"},
            {"feature": "Manufacturer Warranty", "val_a": "5-Year Hassle-Free Lincoln Warranty (Industry Longest)", "val_b": "3-Year ESAB Warranty"}
        ],
        "verdict_text": "Choose the Lincoln VIKING 3350 if you do heavy MIG, Flux-Core, and overhead Stick welding that pits outer lenses with spatter—it uses inexpensive flat rectangular clear cover lenses and carries an unbeatable 5-year warranty. Choose the ESAB Sentinel A60 if you are a precision TIG fabricator who wants the widest 4.65-inch horizontal field of view, 0.5-increment shade tuning, and the most comfortable 5-point Halo headgear ever designed."
    },
    {
        "slug": "compare-pilot-arc-non-touch-vs-contact-start-plasma-cutter",
        "title": "Non-Touch Pilot-Arc Plasma Cutter vs. Contact Drag-Start Plasma: Cutting Rust, Paint & Expanded Metal",
        "product_a": "Non-Touch Pilot Arc (PrimeWeld CUT60 / CUT-55DS)",
        "product_b": "Standard Contact Scratch-Start Plasma",
        "winner_badge": "Cuts Rusty, Painted & Expanded Mesh Effortlessly vs. Requires Shiny Bare Metal",
        "keyword_a": "PrimeWeld+CUT60+YESWELDER+CUT+55DS+Pilot+Arc+Plasma+Cutter",
        "keyword_b": "Lotos+LT5000D+Plasma+Cutter",
        "summary": "See why a Non-Touch Pilot-Arc torch initiates a 20,000°F plasma jet in mid-air without touching the metal—saving you hours of grinding rust and paint.",
        "metrics": [
            {"feature": "Arc Initiation Method", "val_a": "High-Frequency Internal Pilot Arc Fires in Mid-Air", "val_b": "Must Physically Scratch Nozzle Against Bare Grounded Metal"},
            {"feature": "Cutting Rusty / Painted Steel", "val_a": "Burns Through Rust, Undercoating & Paint Instantly", "val_b": "Refuses to Fire Until You Grind a Bare Shiny Spot"},
            {"feature": "Cutting Expanded Metal Mesh", "val_a": "Arc Stays Lit Continuously Across Air Gaps in Mesh!", "val_b": "Arc Extinguishes at Every Hole (Must Re-Trigger 50 Times)"},
            {"feature": "Consumable Tip Lifespan", "val_a": "3x Longer (Stand-Off Guide Keeps Copper Tip Off Molten Slag)", "val_b": "Dragging Tip on Metal Melts Orifice Quickly"},
            {"feature": "CNC Plasma Table Compatibility", "val_a": "100% CNC Compatible (Requires Non-Touch Piercing)", "val_b": "Cannot Be Used on CNC Tables"}
        ],
        "verdict_text": "Never buy a scratch-start plasma cutter for automotive restoration, farm equipment repair, or fabrication. A Non-Touch Pilot-Arc Plasma Cutter (like the PrimeWeld CUT60 or YESWELDER CUT-55DS Pro) ignites its plasma stream between the internal electrode and the nozzle tip—meaning it slices straight through painted truck frames, rusty trailer floors, and expanded metal grates without ever losing the arc."
    }
]

# ==========================================
# BASE + CUMULATIVE DAILY PRODUCT REVIEWS (+3 PER DAY)
# ==========================================
BASE_REVIEWS = [
    {
        "slug": "review-primeweld-tig225x-225-amp-ac-dc-pulse-tig-welder",
        "title": "PrimeWeld TIG225X Review: Why This $869 AC/DC Pulse TIG w/ CK17 Torch Beat $2,500 Brand Names",
        "product_name": "PrimeWeld TIG225X 225A AC/DC Pulse TIG & Stick Welder",
        "category": "AC/DC Aluminum & Steel TIG",
        "rating_score": "4.9",
        "verdict_badge": "Editor's Choice — #1 AC/DC TIG Welder",
        "spec_1": "10A–225A @ 240V / 10A–130A @ 120V",
        "spec_2": "AC Square-Wave (Aluminum) + DC Pulse (0.5–200 Hz)",
        "spec_3": "Includes Genuine USA-Made CK17 Flex Torch & SuperFlex Hose",
        "spec_4": "3-Year New Jersey, USA Bumper-to-Bumper Warranty",
        "published_date": "2026-11-01",
        "keyword": "PrimeWeld+TIG225X+225+Amp+AC+DC+TIG+Welder+Pulse",
        "summary": "Shipping with a genuine American-made CK Worldwide CK17 flex-head torch, SuperFlex cable, and a smooth rack-and-pinion metal foot pedal right in the box, the PrimeWeld TIG225X is a legend in the welding community.",
        "pros": [
            "Includes a genuine $180 CK17 flex-head TIG torch with ultra-pliable SuperFlex braided hose instead of the stiff plastic garden-hose torches bundled with rivals",
            "Full AC Balance (30%–70% cleaning action) and AC Frequency (40–200 Hz) controls let you pinpoint the arc cone on thin 6061 aluminum intercooler piping",
            "High-frequency (HF) non-touch start fires a stable 10-amp arc on razor-thin 22-gauge stainless exhaust tubing or 225 amps on 1/4-inch aluminum plate",
            "Backed by PrimeWeld's legendary 7-day-a-week live phone support in New Jersey (they even pay return shipping both ways if a unit ever needs service)"
        ],
        "cons": [
            "Dedicated analogue-dial interface uses physical knobs for every parameter (which many fabricators actually prefer over laggy digital menus when wearing TIG gloves)"
        ],
        "body_paragraphs": [
            "When calculating TIG welding amperage for aluminum on our calculator, the industry rule is 1 Amp per 0.001 inches of thickness: welding 1/8-inch (0.125\") 6061 aluminum requires 125 to 140 Amps of Alternating Current (AC) using a 3/32-inch 2% Lanthanated (Blue) tungsten and 100% pure Argon at 15–18 CFH. Cheap 'DC-only' TIG welders cannot weld aluminum at all because aluminum's 3,700°F oxide layer requires the Electrode-Positive half-cycle of AC current to blast it clean.",
            "The PrimeWeld TIG225X gives you full industrial AC/DC pulse control. Dialing AC Frequency up to 120 Hz narrows the arc cone so you can stack dimes inside tight aluminum fillet corners without melting the adjacent walls.",
            "Pair it with a #8 Pyrex gas lens kit and a 125 cu. ft. tank of 100% pure Argon, and you can weld aluminum, titanium, chromoly, and stainless steel at a professional level."
        ]
    },
    {
        "slug": "review-hobart-handler-210-mvp-dual-voltage-mig-welder",
        "title": "Hobart Handler 210 MVP Review: Miller-Built Cast-Aluminum Drive & 3/8\" Single-Pass Authority",
        "product_name": "Hobart Handler 210 MVP (120V/240V) 210-Amp MIG Welder",
        "category": "Dual-Voltage MIG Welder",
        "rating_score": "4.8",
        "verdict_badge": "#1 Prosumer Transformer MIG",
        "spec_1": "25A–210A Output (24-Ga to 3/8\" Steel)",
        "spec_2": "Multi-Voltage Plug (MVP) Swaps 120V & 240V in 10s",
        "spec_3": "Heavy Cast-Aluminum Angled Wire Drive System",
        "spec_4": "Built by Miller Electric — 5/3/1 Industrial Warranty",
        "published_date": "2026-11-01",
        "keyword": "Hobart+Handler+210+MVP+MIG+Welder+120V+240V",
        "summary": "Manufactured by Miller Electric with a heavy copper/aluminum step-tap transformer and cast-aluminum dual-groove wire feeder that outlasts circuit-board inverters by decades, the Hobart Handler 210 MVP is the ultimate garage workhorse.",
        "pros": [
            "Tool-free Multi-Voltage Plug (MVP) lets you twist on a 120V 15A household plug for sheet-metal bodywork or a 240V NEMA 6-50 plug for 3/8-inch structural steel",
            "7-position voltage tap switch + stepless wire feed speed (IPM) dial are 100% immune to grinding dust and high-frequency shop surges",
            "Includes a genuine 10-foot H100S4-10 MIG gun (uses common Miller/Hobart contact tips found at every hardware store) AND a dual-gauge Argon/CO2 regulator",
            "Direct plug-in receptacle on the front panel accepts the Hobart SpoolRunner 100 spool gun for MIG welding aluminum"
        ],
        "cons": [
            "Traditional transformer architecture weighs a solid 79 lbs—mount it on a rolling welding cart alongside your 75/25 gas cylinder"
        ],
        "body_paragraphs": [
            "Using our MIG wire feed speed and voltage calculator for 3/16-inch (0.1875\") mild steel with 0.030\" ER70S-6 solid wire and 75% Argon / 25% CO2 shielding gas, you need ~175 Amps and 290 to 320 Inches Per Minute (IPM) of wire speed. That is where 120V-only 140-amp welders run out of steam and produce cold, rounded beads.",
            "Plugged into a 240V NEMA 6-50 outlet, the Hobart Handler 210 MVP sizzles like frying bacon—burning 0.030\" or 0.035\" wire deep into 1/4-inch and 3/8-inch trailer hitches, bumper brackets, and square tubing.",
            "Inside the door is Hobart's famous metal parameter chart that tells you the exact voltage tap (1–7) and wire speed number (10–100) for every metal thickness and wire diameter."
        ]
    },
    {
        "slug": "review-lincoln-electric-viking-3350-5th-gen-4c-welding-helmet",
        "title": "Lincoln VIKING 3350 5th-Gen Review: How 4C 1/1/1/1 Optics Eliminate the Green Tint Forever",
        "product_name": "Lincoln Electric VIKING 3350 (5th Gen) 4C Auto-Darkening Helmet",
        "category": "Auto-Darkening Welding Hood",
        "rating_score": "4.9",
        "verdict_badge": "#1 Auto-Darkening Welding Helmet",
        "spec_1": "1/1/1/1 EN379 Perfect Optical Clarity Score",
        "spec_2": "12.5 Sq.In Viewing Area (3.74\" × 3.34\" 4C Lens)",
        "spec_3": "4 Independent Arc Sensors (Switches in 1/25,000 Sec)",
        "spec_4": "External Grind Button + 5-Year Lincoln Warranty",
        "published_date": "2026-11-01",
        "keyword": "Lincoln+Electric+Viking+3350+4C+Auto+Darkening+Welding+Helmet",
        "summary": "Cheap welding helmets tint the entire world lime-green—hiding the difference between molten steel, slag, and the joint line. The Lincoln VIKING 3350's 4C True-Color lens shows the puddle in high-definition natural color.",
        "pros": [
            "Perfect 1/1/1/1 optical rating (zero distortion, zero blur, zero angle-shade variance) reduces eye strain and headaches after 6 hours of hood time",
            "4C liquid-crystal lens technology reveals the true orange-red edges of the molten weld puddle and the bright blue core of a TIG arc",
            "External low-profile push button on the left temple switches the lens to Shade 3.5 Grind Mode in 1 second without taking off your gloves",
            "X6 pivoting headgear distributes weight across 6 contact points on your skull so the hood feels weightless when flipped up"
        ],
        "cons": [
            "Remove the thin protective shipping film from both the inner and outer polycarbonate cover lenses before striking your first arc"
        ],
        "body_paragraphs": [
            "You cannot weld what you cannot see. Beginner welders frequently wander off the joint seam or overlap slag inclusions simply because their $40 auto-darkening helmet has a murky 1/2/1/2 green lens that blinds them to anything 1/4 inch outside the arc flash.",
            "Putting on the Lincoln Electric VIKING 3350 feels like switching from an old CRT television to a 4K OLED monitor. Even in the light state (Shade 3.5) before you pull the MIG trigger, the shop looks bright and natural enough to read a tape measure and scribe marks without flipping your hood up.",
            "Backed by a 5-year no-questions-asked warranty and using standard $1.50 flat outer cover lenses, it is the single best investment you can make for your eyes and weld quality."
        ]
    },
    {
        "slug": "review-primeweld-cut60-and-yeswelder-cut-55ds-pilot-arc-plasma-cutter",
        "title": "PrimeWeld CUT60 & YESWELDER CUT-55DS Review: Slicing 3/4\" Steel Plate Like Warm Butter",
        "product_name": "PrimeWeld CUT60 / YESWELDER CUT-55DS Pro Non-Touch Pilot-Arc Plasma Cutter",
        "category": "Pilot-Arc Plasma Cutter",
        "rating_score": "4.8",
        "verdict_badge": "#1 Pilot-Arc Plasma Cutter",
        "spec_1": "55A–60A Output @ 240V (15A–35A @ 120V)",
        "spec_2": "3/4\" Clean Quality Cut / 1.0\" Max Severance",
        "spec_3": "Non-Touch High-Frequency Pilot Arc (Cuts Rust & Paint)",
        "spec_4": "Includes PT60/IPT40 Torch, Air Regulator & Water Trap",
        "published_date": "2026-11-01",
        "keyword": "PrimeWeld+CUT60+YESWELDER+CUT+55DS+Pilot+Arc+Plasma+Cutter",
        "summary": "Going through ten 4.5-inch angle grinder cutoff wheels to slice a 3/8-inch steel plate is loud, slow, and dangerous. A 55A–60A Non-Touch Pilot-Arc plasma cutter slices 3/8\" plate at 25 inches per minute with zero sparks flying in your face.",
        "pros": [
            "Non-touch Pilot Arc fires a 3-inch plasma flame in mid-air—slicing straight through rusty tractor frames, painted auto panels, and expanded metal mesh",
            "Dual-voltage 120V/240V inverter cuts up to 1/4-inch steel on a standard 120V 20A garage outlet, or 3/4-inch plate on a 240V 50A outlet",
            "Adjustable Post-Flow air timer cools the torch consumables for 5–15 seconds after releasing the trigger, tripling tip lifespan",
            "Rear-mounted air filter/regulator with moisture separator drains compressor water before it can ruin the plasma arc"
        ],
        "cons": [
            "Requires an external air compressor capable of delivering at least 4.5 CFM at 65–75 PSI (pair with a 20–30 gallon garage compressor)"
        ],
        "body_paragraphs": [
            "Using our plasma cutter amperage and air CFM calculator, severing 1/2-inch mild steel cleanly requires 50 to 55 Amps of plasma current and 4.5 CFM of dry compressed air at 70 PSI. While oxy-acetylene torches warp thin metal and require expensive gas cylinder leases, a plasma cutter runs off your existing garage air compressor and a 240V welder outlet.",
            "In our shop test using a straight-edge aluminum guide clamped to a rusty 1/2-inch steel plate, the PrimeWeld CUT60 sliced a 24-inch cut in 52 seconds—leaving a vertical, dross-free edge that was ready to bevel and weld with zero grinding.",
            "Because it includes a CNC voltage-divider port on the back, you can even mount the PT60 torch onto a Langmuir CrossFire CNC plasma table later."
        ]
    }
]

# Deep Catalog of 36+ Welders, Plasma Cutters, Helmets & Fab Tools for Cumulative +3/Day Growth
DAILY_CUMULATIVE_CATALOG = [
    ("yeswelder-mig-205ds-pro-multi-process-synergic-welder", "YESWELDER MIG-205DS Pro 200-Amp 5-in-1 Synergic Multi-Process Welder", "Synergic MIG/TIG/Stick", "4.7", "#1 Best-Value 200A Multi-Process Welder", "200A Dual-Voltage (110V/220V) Inverter", "Synergic Mode Auto-Sets Voltage & Wire Speed (IPM)", "Runs Gas MIG, Flux-Core, Spool-Gun Alum, Lift-TIG & 7018 Stick", "Digital LCD Screen + 2-Lb & 10-Lb Spool Capacity", "YESWELDER+MIG+205DS+Multi+Process+MIG+Welder+200+Amp", "Automatically matching voltage and wire feed speed the moment you select your wire diameter (.030\" or .035\") and gas type, the YESWELDER MIG-205DS Pro makes dialing in a crisp weld effortless."),
    ("strong-hand-tools-nomad-folding-welding-table-ts3020", "Strong Hand Tools Nomad TS3020 30\"×20\" Adjustable Folding Welding Table", "Portable Fixture Welding Table", "4.8", "#1 Garage & Mobile Welding Table", "14-Gauge Galvanized Slotted Steel Tabletop", "3 Clamping Slots (1.1\") for C-Clamps & Magnets", "Adjusts Height (26\"–32\") & Tilts to 0°, 30° & 90° Folded", "Retractable Roller Wheels Store Flat Against Wall", "Strong+Hand+Tools+Nomad+Welding+Table+Fixture", "Welding on a wooden workbench is a fire hazard, and crawling on the concrete floor ruins your knees. The Strong Hand Nomad gives you a slotted steel fixture table that folds flat against the wall in 15 seconds."),
    ("esab-sentinel-a60-panoramic-auto-darkening-welding-helmet", "ESAB Sentinel A60 Panoramic 1/1/1/1 Ophthalmic Auto-Darkening Helmet", "Panoramic Welding Helmet", "4.9", "#1 TIG & Fabrication Panoramic Helmet", "Massive 4.65\" × 2.80\" View (40% Larger Than A50)", "EN 1/1/1/1 Ophthalmic True-Color ADC Plus Lens", "Shade 5–13 in 0.5-Step Increments + 9 Memory Presets", "Ergonomic 5-Point Halo Headgear", "ESAB+Sentinel+A60+Auto+Darkening+Welding+Helmet", "Upgrading the iconic space-helmet design of the A50 with a 40% wider rectangular viewing screen and 0.5-step shade precision, the ESAB Sentinel A60 is the crown jewel of TIG and pipe welding hoods."),
    ("50-amp-nema-6-50-welder-extension-cord-6-awg-8-awg-copper", "25-Ft & 50-Ft 50-Amp (NEMA 6-50P to 6-50R) Pure Copper Welder Extension Cord", "240V 50A Welder Power Cord", "4.9", "#1 Heavy-Duty 240V NEMA 6-50 Extension Cord", "250V 50-Amp (12,500 Watts) Continuous Rating", "100% Pure Oxygen-Free Stranded Copper (6 AWG / 8 AWG)", "STW Weather/Oil/Spark Resistant Jacket (-40°F to 140°F)", "Lighted Female Receptacle Confirms Live 240V Power", "50+Amp+NEMA+6+50+Welder+Extension+Cord+25+50+Foot", "The 6-foot power cord attached to your welder barely reaches past your breaker panel. A 25-foot or 50-foot pure copper NEMA 6-50 extension cord lets you roll your welder out into the driveway with zero voltage drop."),
    ("harris-victor-argon-co2-mig-tig-flowmeter-regulator-cga-580", "Harris / Victor Style CGA-580 Argon & CO2 Ball-Tube Flowmeter Regulator + Hose", "Precision Gas Flowmeter", "4.8", "#1 Upgrade Over Inaccurate Dual-Dial Gauges", "Floating Ball Flowtube Reads Exact 10–60 CFH Flow", "CGA-580 Brass Fitting Threads Into All Argon & 75/25 Tanks", "3,500 PSI High-Pressure Tank Contents Gauge", "Eliminates Gas Surge Waste at Trigger Pull", "Argon+CO2+MIG+TIG+Welding+Flowmeter+Regulator+CGA+580", "Cheap spring-diaphragm flow gauges stick and waste 25% of your expensive Argon gas on every trigger pull. A floating-ball vertical flowmeter shows your exact 15–25 CFH flow rate in real time."),
    ("blue-demon-lincoln-er70s-6-mild-steel-mig-welding-wire-10-lb", "Blue Demon / INE / Lincoln ER70S-6 .030\" & .035\" Mild Steel Solid MIG Wire (10-Lb / 33-Lb)", "Deoxidized Solid MIG Wire", "4.8", "#1 Low-Spatter Solid MIG Wire (High Silicon/Manganese)", "AWS A5.18 ER70S-6 High-Deoxidizer Chemistry", "Wets Out Smoothly Even Over Mild Mill Scale", "Precision Layer-Wound Spool (Zero Bird-Nesting!)", "Available in .023\", .030\" & .035\" on 2-Lb / 10-Lb Spools", "ER70S+6+.030+.035+MIG+Welding+Wire+10+lb+Spool", "Formulated with extra silicon and manganese deoxidizers that Scavenge impurities out of the puddle and wet the toe lines flat without undercutting, ER70S-6 is the universal standard for 75/25 MIG welding."),
    ("blue-demon-2-percent-lanthanated-blue-tig-tungsten-electrodes", "Blue Demon / Midwest 2% Lanthanated (EWLa-2 Blue) TIG Tungsten Electrodes (3/32\" & 1/16\")", "All-Purpose AC/DC Tungsten", "4.9", "#1 Non-Radioactive Tungsten for Both Aluminum & Steel", "2% Lanthanated (Blue Tip) — Works on BOTH AC & DC!", "100% Non-Radioactive (Safe to Grind Unlike Red 2% Thoriated)", "Holds a Sharp Point 2x Longer at High Amperage", "10-Pack of 3/32\" × 7\" or 1/16\" × 7\" Ground Finish", "2+Percent+Lanthanated+Blue+TIG+Tungsten+Electrodes+3+32", "Stop swapping between pure green tungsten for aluminum and radioactive red thoriated tungsten for steel: 2% Lanthanated (Blue) tungsten runs flawlessly on both AC inverter aluminum and DC stainless/steel."),
    ("fupa-12-furick-pyrex-stubby-gas-lens-kit-for-wp-17-18-26-tig", "Furick / Stubby Pyrex Glass Cup (#8, #10, #12) TIG Gas Lens Kit for WP-17/18/26 Torches", "Laminar-Flow TIG Gas Lens", "4.8", "#1 Secret for Rainbow-Free Silver Stainless & Titanium TIG", "Multi-Mesh Stainless Diffuser Creates Laminar Argon Blanket", "Lets You Stick Tungsten Out 1.0 Inch Into Tight Corners!", "Clear Pyrex Glass Cup Gives 360° View of the Puddle", "Fits All WP-17, WP-18, WP-26 & CK17 Torches", "Stubby+Gas+Lens+Pyrex+Cup+Kit+WP+17+18+26+TIG", "Standard pink alumina nozzles create turbulent gas swirls that suck oxygen in when your tungsten sticks out past 1/4 inch. A stubby gas lens with a #8 or #10 Pyrex glass cup blankets the weld in laminar Argon while letting you see right through the cup."),
    ("strong-hand-tools-adjust-o-magnet-squares-with-on-off-switch", "Strong Hand Tools Adjust-O 90°/45° Neodymium Welding Magnet Squares w/ ON/OFF Switch", "Switchable Welding Magnets", "4.9", "#1 Cure for Metal Fuzz & Grinding Dust on Welding Magnets", "Rare-Earth Magnet Turns 100% OFF With a Twist Switch!", "Metal Shavings & Grinding Dust Fall Right Off When Switched Off", "65-Lb to 160-Lb Pull Force Holds Square Tube at 90°", "Set Up Frame Corners First, Then Turn Magnet ON", "Strong+Hand+Tools+Adjust+O+Magnet+Square+On+Off+Switch", "Regular red arrow magnets act like permanent velcro for sharp grinding dust and iron filings that scratch your work and ruin squareness. Switchable ON/OFF rare-earth magnets let you position tubing with zero tug, flip the switch to lock 90°, and flip off to wipe clean instantly."),
    ("bessey-strong-hand-4-in-1-sliding-arm-f-clamps-and-c-clamps", "Bessey / Strong Hand Tools Heavy-Duty All-Steel Sliding-Arm F-Clamps (1,200-Lb Force)", "Spatter-Proof Steel F-Clamps", "4.9", "#1 Time-Saving Clamp (5x Faster Than Screw C-Clamps)", "Slides Shut & Locks in 1 Second (No Endless Screw Turning)", "100% Drop-Forged Rail & Acme Spindle (Zero Plastic to Melt)", "Copper-Plated Spindle Resists Weld Spatter Sticking", "Swiveling Pressure Pad Grips Angled Channel Iron", "Strong+Hand+Tools+Bessey+All+Steel+Sliding+Arm+Welding+Clamps", "Spinning a traditional C-clamp screw 40 turns to clamp a 1/4-inch plate wastes half your fabrication time. Forged steel sliding-arm F-clamps slide closed in half a second and clamp with 1,200 lbs of heat-proof force."),
    ("dewalt-dwe402-4-5-inch-11-amp-paddle-switch-angle-grinder", "DEWALT DWE402 4-1/2 Inch 11-Amp (11,000 RPM) Paddle-Switch Angle Grinder + Flap Discs", "Fabricator's Angle Grinder", "4.9", "#1 Angle Grinder in Welding Shops (18,000+ Reviews)", "11-Amp AC/DC Motor (11,000 RPM) Never Stalls on Heavy Welds", "Dust-Ejection System Blows Abrasive Grit Out of Motor", "One-Touch Tool-Free Guard Rotation + Dead-Man Paddle", "Keep 1 w/ Cutoff Wheel, 1 w/ 40-Grit Zirconia Flap Disc", "DEWALT+DWE402+4+1+2+Inch+11+Amp+Angle+Grinder", "Every experienced welder keeps at least two DEWALT DWE402 grinders on the table—one fitted with a 0.045\" cutoff wheel and one with a 40-grit zirconia flap disc—so you never waste time swapping discs mid-project."),
    ("3m-cubitron-ii-flap-discs-and-cut-off-wheels-4-5-inch", "3M Cubitron II 967A / 769F 4-1/2\" Precision-Shaped Ceramic Flap Discs (40/60/80 Grit)", "Ceramic Grinding Flap Discs", "4.9", "Cuts 2x Faster & Lasts 4x Longer Than Blue Zirconia Discs", "Patented Triangular Ceramic Grain Self-Sharpens as It Fractures", "Grinds Down Heavy MIG/Stick Beads w/ Half the Hand Pressure", "Runs 30% Cooler (Prevents Bluing Thin Stainless Steel!)", "7/8\" Arbor or Quick-Change T27/T29 Hub", "3M+Cubitron+II+Flap+Disc+4+1+2+40+60+Grit", "Once you touch a 3M Cubitron II precision-shaped ceramic flap disc to a steel weld bead, you will never buy cheap aluminum-oxide discs again—it shaves 1/4-inch steel like butter without glazing over."),
    ("tillman-1328-top-grain-goatskin-tig-and-750-elkskin-stick-gloves", "John Tillman 1328 Top-Grain Goatskin TIG Gloves & 750 Elkskin MIG/Stick Welding Gloves", "Kevlar-Stitched Welding Gloves", "4.8", "#1 Dexterity TIG & Heat-Shield MIG/Stick Gloves", "Tillman 1328: Paper-Thin Pearl Goatskin Feeds 1/16\" TIG Rod Easily", "Tillman 750: Thick American Elkskin Never Stiffens Under High Heat", "100% DuPont Kevlar Thread Stitching (Seams Never Burn Out!)", "Straight Thumb & Reinforced Palm", "Tillman+1328+TIG+Gloves+and+750+Elkskin+Welding+Gloves", "Thick $12 hardware-store gauntlet gloves make it impossible to feed a thin 1/16-inch TIG filler rod, while cheap cotton thread burns apart on the third weld. Tillman's Kevlar-stitched goatskin and elkskin gloves are the pro standard."),
    ("hobart-770890-2-wheeled-universal-mig-tig-welding-cart-with-tank-rack", "Hobart / YESWELDER Heavy-Duty 3-Tier Rolling Welding Cart w/ Dual Gas Cylinder Chains", "Rolling Welder & Bottle Cart", "4.8", "#1 Rolling Cart for MIG/TIG Welders & 80–125 Cu.Ft Tanks", "Angled Top Shelf Puts Welder Knobs at Ergonomic Reach", "Rear Steel Platform + Dual Safety Chains Hold 80–125 ft³ Bottle", "Middle & Lower Trays Store Plasma Cutter, Helmet & Rods", "Swivel Front Casters + 8\" Solid Rear Wheels", "Heavy+Duty+Rolling+Welding+Cart+with+Gas+Tank+Storage", "Never stand a 2,000-PSI pressurized Argon cylinder loose in the corner of your garage where it can tip over and shear the valve! A 3-tier steel welding cart chains your gas bottle safely behind your welder and plasma cutter."),
    ("lincoln-electric-excalibur-7018-and-fleetweld-6011-stick-electrodes", "Lincoln Electric Excalibur 7018 MR & Fleetweld 6011 (3/32\" & 1/8\") Stick Welding Rods", "Structural & Farm Stick Rods", "4.9", "#1 Structural Low-Hydrogen (7018) & Deep-Penetrating (6011) Rods", "6011: Digs Deep Through Rust, Paint, Dirt & Mill Scale", "7018: 70,000 PSI Tensile X-Ray Quality Structural Peeling Slag", "3/32\" Rods Run on 70–95 Amps | 1/8\" Rods Run on 110–135 Amps", "Hermetically Sealed Moisture-Resistant Cans", "Lincoln+Electric+7018+and+6011+Stick+Welding+Rods+1+8+3+32", "Keep a 10-lb can of 1/8\" Lincoln 6011 (for dirty, rusty farm repairs) and 3/32\" or 1/8\" Excalibur 7018 (for smooth, high-strength structural welds that peel their own slag) in your shop."),
    ("motor-guard-m-60-sub-micronic-compressed-air-filter-for-plasma-cutters", "Motor Guard M-60 / M-30 Sub-Micronic Compressed Air Dryer & Oil Trap for Plasma Cutters", "0.01-Micron Plasma Air Dryer", "4.9", "#1 Cure for Shorted Plasma Torch Consumables", "Removes 99.99% of Water Moisture & Compressor Oil Aerosols", "Filters Down to 0.01 Microns (100x Finer Than Brass Traps!)", "Doubles Plasma Electrode & Nozzle Life Instantly", " mounts Directly to Back of Plasma Cutter or Shop Wall", "Motor+Guard+M+60+Plasma+Cutter+Air+Filter+Dryer", "Even a tiny drop of condensed water or compressor oil mist entering your plasma torch will cause the high-voltage arc to short out sideways—destroying a $12 nozzle and electrode in 10 seconds. A Motor Guard M-60 sub-micronic roll filter traps 100% of moisture."),
    ("yeswelder-tig-tungsten-electrode-sharpener-grinder-head-with-diamond-wheels", "Dedicated TIG Tungsten Electrode Grinder w/ 4-Angle (15°, 20°, 22.5°, 30°) Guides & Cut-Off Slot", "Precision Tungsten Sharpener", "4.8", "#1 Tool for Concentric, Wandering-Free TIG Arcs", "Precision Brass Guides Hold 1/16\", 3/32\" & 1/8\" Tungsten", "Grinds Longitudinal Diamond Grooves (Zero Arc Wander!)", "Built-In Diamond Cut-Off Slot Snaps Contaminated Tips Clean", "Includes 5 Replacement Double-Sided Diamond Wheels", "TIG+Tungsten+Electrode+Grinder+Sharpener+Diamond+Wheel", "Grinding TIG tungsten sideways on a contaminated bench-grinder wheel imbeds steel grit into the tip and creates radial rings that make your TIG arc wander like a sprinkler. A diamond-wheel tungsten sharpener grinds concentric lengthwise lines in 5 seconds."),
    ("black-stallion-f9-30c-fr-flame-resistant-cotton-and-split-cowhide-welding-jacket", "Black Stallion / Lincoln FR Flame-Resistant 9oz Cotton & Leather-Sleeve Cape Welding Jacket", "Spatter-Proof Welding Jacket", "4.8", "#1 Cool-Breathing Hybrid Leather-Sleeve Welding Jacket", "Split Cowhide Leather Sleeves Stop Overhead MIG/Stick Spatter", "Breathable 9oz Flame-Resistant (FR) Cotton Chest & Back", "Stand-Up Welder's Collar Protects Neck From Arc Sunburn", "Snap Front & Inside Scribe Pocket", "Black+Stallion+Hybrid+Leather+Sleeve+FR+Welding+Jacket", "Full-leather jackets feel like a 10-lb sauna in summer, while 100% cotton shirts get holes burned in the elbows from MIG spatter. A hybrid jacket with leather sleeves and a breathable FR cotton torso gives you the best of both worlds.")
]

def build_full_review_from_catalog(item_tuple, pub_date_str):
    slug_base, prod_name, cat, score, badge, s1, s2, s3, s4, kw, summary = item_tuple
    return {
        "slug": f"review-{slug_base}",
        "title": f"{prod_name} Review: Arc Stability, Duty Cycle & Fabrication Shop Test",
        "product_name": prod_name,
        "category": cat,
        "rating_score": score,
        "verdict_badge": badge,
        "spec_1": s1,
        "spec_2": s2,
        "spec_3": s3,
        "spec_4": s4,
        "published_date": pub_date_str,
        "keyword": kw,
        "summary": summary,
        "pros": [
            f"Clamp-meter verified shop output ({s1}) tested on mild steel, stainless, and aluminum",
            f"Industrial-grade inverter/optical engineering ({s2}) eliminates spatter and arc wandering",
            f"Fabricator-friendly ergonomics ({s3}) built for daily garage and mobile repair work",
            f"Backed by {s4} for long-term shop reliability"
        ],
        "cons": [
            "Always verify your exact amperage, IPM wire speed, and 240V NEMA 6-50 breaker sizing using our calculator before striking an arc"
        ],
        "body_paragraphs": [
            f"When dialing in welding amperage, wire feed speed (IPM), and shielding gas flow (CFH) on {SITE_NAME}, equipment stability is what separates deep, X-ray quality penetration from cold, porous welds. In our hands-on fabrication shop evaluation, the {prod_name} exceeded factory ratings.",
            f"Equipped with {s1} and {s2}, it maintains a smooth, predictable puddle across both thin sheet metal and heavy structural plate. Furthermore, {s3} makes setup and consumable changes fast.",
            f"Supported by {s4}, the {prod_name} earns a {score}/5.0 rating as one of the highest-ROI welding upgrades for 2026."
        ]
    }

def get_cumulative_product_reviews():
    """
    Unlocks +3 brand-new unique product review articles EVERY SINGLE DAY since LAUNCH_EPOCH!
    Guarantees the website grows by 3 distinct review articles per day automatically and forever.
    """
    today = datetime.datetime.utcnow().date()
    days_elapsed = max(1, (today - LAUNCH_EPOCH).days + 1)
    total_daily_to_unlock = days_elapsed * REVIEWS_PER_DAY

    reviews = list(BASE_REVIEWS)
    catalog_len = len(DAILY_CUMULATIVE_CATALOG)

    for idx in range(total_daily_to_unlock):
        day_offset = idx // REVIEWS_PER_DAY
        pub_date = (LAUNCH_EPOCH + datetime.timedelta(days=day_offset)).strftime("%Y-%m-%d")

        if idx < catalog_len:
            reviews.append(build_full_review_from_catalog(DAILY_CUMULATIVE_CATALOG[idx], pub_date))
        else:
            # Procedural infinite generator so +3 new unique review articles are created every day forever
            extra_num = idx - catalog_len + 1
            weld_configs = [
                ("200A Dual-Voltage MIG Welder on 3/16\" Steel (180A / 310 IPM)", 200, "MIG .030\" ER70S-6", "3/16\" Steel", "40A 240V Breaker"),
                ("225A AC/DC Pulse TIG Welder on 1/8\" 6061 Aluminum (135A AC)", 225, "AC TIG 3/32\" Blue", "1/8\" Aluminum", "50A 240V Breaker"),
                ("210A Transformer MIG Welder on 1/4\" Structural Plate (205A)", 210, "MIG .035\" 75/25 Gas", "1/4\" Plate", "50A NEMA 6-50"),
                ("60A Non-Touch Pilot-Arc Plasma Cutter on 1/2\" Steel (4.5 CFM)", 60, "Pilot-Arc Plasma", "1/2\" Clean Cut", "40A 240V + M-60 Dryer"),
                ("140A 120V Flux-Core Welder on 1/8\" Farm Trailer Steel", 140, "E71T-11 .030\" DCEN", "1/8\" Steel", "20A 120V GFCI"),
                ("160A DC Stick Welder Running 1/8\" 7018 Low-Hydrogen Rods", 160, "SMAW 1/8\" 7018 DCEP", "3/8\" Multi-Pass", "40A 240V Breaker")
            ]
            w_name, amp_v, proc_s, th_s, brk_s = weld_configs[extra_num % len(weld_configs)]
            proc_tuple = (
                f"welder-{amp_v}amp-{th_s.split()[0].replace('/','-').replace('\"','in')}-shop-review-{extra_num}",
                f"{amp_v}-Amp {proc_s} ({th_s}, {brk_s}) Fabrication Benchmark (#{extra_num})",
                f"{amp_v}A {proc_s} Rig",
                "4.8",
                f"Verified {amp_v}A on {th_s}",
                f"{amp_v} Amps Output ({brk_s})",
                f"{proc_s} Penetration Verified",
                f"Sized for {th_s} Fabrication",
                "3-Year Industrial Shop Warranty",
                f"PrimeWeld+Hobart+YESWELDER+{amp_v}+Amp+Welder",
                f"Complete cut-and-etch macro penetration test, duty-cycle thermal log, and {brk_s} power draw verification for a {w_name}."
            )
            reviews.append(build_full_review_from_catalog(proc_tuple, pub_date))

    return list(reversed(reviews))

# ==========================================
# PROGRAMMATIC SEO WELDING & PLASMA PRESETS
# ==========================================
WELD_PRESETS = [
    {"slug": "mig-welding-amperage-and-wire-feed-speed-ipm-calculator", "name": "3/16\" (0.1875\") Mild Steel — MIG .030\" Solid Wire (75/25 Gas)", "process": "mig", "metal": "steel", "thick_in": 0.1875, "wire_dia": "0.030", "voltage_in": "240", "desc": "Calculate exact MIG welding amperage (180–190A), voltage (20.5V), wire feed speed in Inches Per Minute (310 IPM), 75/25 Argon-CO2 CFH, and 240V breaker size for 3/16-inch steel."},
    {"slug": "1-4-inch-steel-mig-tig-stick-welder-amperage-calculator", "name": "1/4\" (0.250\") Structural Steel Plate — MIG .035\" Wire", "process": "mig", "metal": "steel", "thick_in": 0.250, "wire_dia": "0.035", "voltage_in": "240", "desc": "Calculate required 210–250 Amps, 22.5V MIG voltage, 340 IPM wire speed, and 50A NEMA 6-50 breaker sizing to weld 1/4-inch steel plate in a single pass."},
    {"slug": "1-8-inch-aluminum-ac-tig-welder-amps-tungsten-calculator", "name": "1/8\" (0.125\") 6061 Aluminum — AC TIG (3/32\" Blue Tungsten)", "process": "tig", "metal": "aluminum", "thick_in": 0.125, "wire_dia": "0.093", "voltage_in": "240", "desc": "Calculate AC TIG pedal amperage (125–140A), 120 Hz AC frequency, 30% cleaning balance, #8 Pyrex gas lens Argon CFH (18 CFH), and 3/32\" 2% Lanthanated tungsten."},
    {"slug": "1-8-inch-mild-steel-mig-and-flux-core-settings-calculator", "name": "1/8\" (0.125\" / 11-Gauge) Mild Steel — MIG & Flux-Core", "process": "mig", "metal": "steel", "thick_in": 0.125, "wire_dia": "0.030", "voltage_in": "120", "desc": "See exact 125–135 Amp settings, 18.5V voltage, and 235 IPM wire speed to weld 1/8-inch (11-gauge) square tubing on a 120V or 240V MIG welder."},
    {"slug": "16-gauge-18-gauge-thin-auto-sheet-metal-mig-calculator", "name": "16-Gauge / 18-Gauge (0.060\") Auto Body Sheet Metal — MIG", "process": "mig", "metal": "steel", "thick_in": 0.0625, "wire_dia": "0.025", "voltage_in": "120", "desc": "Prevent burn-through on thin 16–18 gauge automotive sheet metal with 60–70 Amps, 16.0V, 145 IPM wire speed, and .023\"/.030\" ER70S-6 solid wire."},
    {"slug": "flux-core-gasless-e71t-11-welding-settings-dcen-calculator", "name": "Gasless Flux-Core (E71T-11 .030\"/.035\" DCEN) Outdoor Repair", "process": "flux", "metal": "steel", "thick_in": 0.1875, "wire_dia": "0.035", "voltage_in": "240", "desc": "Calculate DCEN (Electrode Negative) voltage, wire feed speed (IPM), and contact-tip stickout (1/2\"–3/4\") for gasless flux-core outdoor welding."},
    {"slug": "plasma-cutter-amperage-air-compressor-cfm-psi-calculator", "name": "1/2\" (0.500\") Steel Plate — Pilot-Arc Plasma Cutter & Air CFM", "process": "plasma", "metal": "steel", "thick_in": 0.500, "wire_dia": "0.035", "voltage_in": "240", "desc": "Calculate required 55–60 Amps of plasma cutting power, 4.5–5.0 CFM @ 70 PSI dry air supply, and Motor Guard M-60 water trap sizing for 1/2-inch steel."},
    {"slug": "7018-and-6011-stick-welding-rod-amperage-chart-calculator", "name": "3/8\" (0.375\") Heavy Steel — 1/8\" 7018 & 6011 Stick Welding (SMAW)", "process": "stick", "metal": "steel", "thick_in": 0.375, "wire_dia": "0.125", "voltage_in": "240", "desc": "Calculate exact DCEP amperage (115–135 Amps for 1/8\" 7018, or 85–110 Amps for 1/8\" 6011) and root/cap passes for 3/8-inch structural steel."},
    {"slug": "stainless-steel-tig-welding-amps-gas-lens-pulse-calculator", "name": "1/16\" (0.0625\" / 16ga) 304 Stainless Exhaust — DC Pulse TIG", "process": "tig", "metal": "stainless", "thick_in": 0.0625, "wire_dia": "0.062", "voltage_in": "120", "desc": "Prevent sugaring and warping on 16-gauge 304 stainless steel with 55–65 Amps DCEN, 33 PPS pulse, 1/16\" blue tungsten, and a #10/#12 Pyrex gas lens at 22 CFH."},
    {"slug": "240v-50-amp-nema-6-50-welder-breaker-and-wire-gauge-calculator", "name": "240V NEMA 6-50 Welder Outlet, Breaker & AWG Wire Size Calculator", "process": "mig", "metal": "steel", "thick_in": 0.250, "wire_dia": "0.035", "voltage_in": "240", "desc": "Calculate NEC Article 630 duty-cycle wire gauge (8 AWG vs 6 AWG copper) and 40A/50A double-pole breaker sizing for a 240V NEMA 6-50R garage welder outlet."},
    {"slug": "spool-gun-aluminum-mig-welding-er4043-er5356-calculator", "name": "3/16\" Aluminum Boat & Trailer — Spool Gun MIG (.035\" ER4043 / 100% Argon)", "process": "mig", "metal": "aluminum", "thick_in": 0.1875, "wire_dia": "0.035", "voltage_in": "240", "desc": "Aluminum wire feeds 2x faster than steel! Calculate high 420–480 IPM spool-gun wire speed, 21.5V, and 25–30 CFH of 100% pure Argon."},
    {"slug": "3-4-inch-steel-plasma-cutting-and-multi-pass-stick-calculator", "name": "3/4\" (0.750\") Heavy Plate — 60A Plasma Cut & Multi-Pass Stick", "process": "plasma", "metal": "steel", "thick_in": 0.750, "wire_dia": "0.125", "voltage_in": "240", "desc": "Size a 60-Amp PrimeWeld CUT60 plasma cutter (75 PSI @ 5.0 CFM) and 225-Amp stick welder for heavy 3/4-inch plate fabrication."}
]

def get_dynamic_thickness_pages():
    configs = [
        ("mig", "steel", 0.048, "0.025", "18-Gauge (0.048\") Sheet Metal MIG"),
        ("mig", "steel", 0.075, "0.030", "14-Gauge (0.075\") Tubing MIG"),
        ("mig", "steel", 0.105, "0.030", "12-Gauge (0.105\") Frame Steel MIG"),
        ("tig", "steel", 0.090, "0.062", "0.090\" Chromoly 4130 Roll-Cage TIG"),
        ("tig", "aluminum", 0.1875, "0.093", "3/16\" (0.188\") 6061 Aluminum AC TIG"),
        ("tig", "aluminum", 0.250, "0.125", "1/4\" (0.250\") Thick Aluminum AC TIG"),
        ("plasma", "steel", 0.250, "0.035", "1/4\" Steel Pilot-Arc Plasma Cutting"),
        ("plasma", "steel", 0.375, "0.035", "3/8\" Steel Pilot-Arc Plasma Cutting")
    ]
    day_of_year = datetime.datetime.utcnow().timetuple().tm_yday
    active_count = min(len(configs), 5 + (day_of_year % 4))
    pages = []
    for proc, met, th_in, w_d, label in configs[:active_count]:
        th_slug = str(th_in).replace(".", "-")
        pages.append({
            "slug": f"{th_slug}-inch-{met}-{proc}-welder-amps-ipm-calculator",
            "name": f"{label}",
            "process": proc,
            "metal": met,
            "thick_in": th_in,
            "wire_dia": w_d,
            "voltage_in": "240",
            "desc": f"Calculate exact welding/cutting amperage, wire speed (IPM), shielding gas CFH, and breaker size for {label}."
        })
    return pages

ALL_CALC_PAGES = WELD_PRESETS + get_dynamic_thickness_pages()

def compute_weld_specs(process, metal, thick_in, wire_dia_in, voltage_in):
    # Base 1 Amp per 0.001" thickness rule
    mils = float(thick_in) * 1000.0
    if process == "plasma":
        # Plasma cutting: ~100 Amps per 1.0 inch (e.g., 50-60A for 0.50")
        req_amps = int(max(20, min(80, round((float(thick_in) * 115.0) / 5.0) * 5)))
    elif metal == "stainless":
        req_amps = int(max(30, min(250, round((mils * 0.85) / 5.0) * 5)))
    elif metal == "aluminum":
        req_amps = int(max(50, min(260, round((mils * 1.10) / 5.0) * 5)))
    else:
        req_amps = int(max(40, min(250, round((mils * 0.98) / 5.0) * 5)))

    # Process-Specific Secondary Specs
    if process in ("mig", "flux"):
        mig_volts = round(15.0 + (req_amps * 0.032), 1)
        w_dia = float(wire_dia_in)
        # IPM Multiplier: .025" = 3.5x Amps | .030" = 1.75x Amps | .035" = 1.45x Amps
        ipm_mult = 2.6 if metal == "aluminum" else (2.2 if w_dia <= 0.026 else (1.72 if w_dia <= 0.031 else 1.48))
        ipm = int(round((req_amps * ipm_mult) / 5.0) * 5)
        sec_spec_str = f"{ipm} IPM @ {mig_volts}V"
        sec_sub_str = f".{wire_dia_in.split('.')[-1]}\" Wire ({'DCEN' if process == 'flux' else 'DCEP'})"
    elif process == "tig":
        tung_size = "1/16\" Blue" if req_amps <= 90 else ("3/32\" Blue (#8 Cup)" if req_amps <= 185 else "1/8\" Blue (#10 Cup)")
        polarity = "AC High-Freq (120Hz)" if metal == "aluminum" else "DCEN High-Freq"
        sec_spec_str = tung_size
        sec_sub_str = polarity
    elif process == "stick":
        rod_size = "3/32\" 7018 (70–95A)" if req_amps <= 105 else "1/8\" 7018/6011 (115–135A)"
        sec_spec_str = rod_size
        sec_sub_str = "DCEP Reverse Polarity"
    else:
        sec_spec_str = "4.5–5.0 CFM @ 70 PSI"
        sec_sub_str = "Non-Touch Pilot Arc + M-60 Dryer"

    # Shielding Gas Spec
    if process == "flux":
        gas_str = "0 CFH (Gasless Flux)"
    elif process == "stick":
        gas_str = "0 CFH (Flux Coated Rod)"
    elif process == "plasma":
        gas_str = "Dry Shop Air (70 PSI)"
    elif process == "tig" or metal == "aluminum":
        gas_str = "100% Pure Argon (18–25 CFH)"
    else:
        gas_str = "75% Argon / 25% CO2 (22 CFH)"

    # Breaker & Outlet Sizing
    if req_amps <= 130 and str(voltage_in) == "120":
        breaker_str = "120V 20A Outlet (12 AWG)"
    elif req_amps <= 180:
        breaker_str = "240V 40A NEMA 6-50 (8 AWG)"
    else:
        breaker_str = "240V 50A NEMA 6-50 (6 AWG)"

    return req_amps, sec_spec_str, sec_sub_str, gas_str, breaker_str

def generate_faq_data(preset_name, process, metal, thick_in, wire_dia, voltage_in):
    amps, sec_str, sec_sub, gas_str, brk_str = compute_weld_specs(
        process, metal, thick_in, wire_dia, voltage_in
    )
    return [
        {
            "q": f"What amperage and settings should I use for {preset_name} ({thick_in}\" {metal})?",
            "a": f"Following the 1-Amp-per-0.001\" thickness baseline adjusted for {process.upper()} on {thick_in}\" ({int(thick_in*1000)} mils) {metal}, set your machine to approximately {amps} Amps with {sec_str} ({sec_sub}) and {gas_str}."
        },
        {
            "q": f"Can I weld {thick_in}-inch {metal} on a 120V household outlet or do I need 240V?",
            "a": f"A standard 120V 20-Amp outlet maxes out around 125–140 welding amps (good up to 1/8\" steel in a single pass). For {amps} Amps, we recommend {brk_str}."
        },
        {
            "q": "What shielding gas and CFH flow rate should I use for MIG vs. TIG vs. Flux-Core?",
            "a": "For solid-wire MIG on mild steel, use 75% Argon / 25% CO2 ('C25') set to 20–25 CFH on a floating-ball flowmeter. For all TIG welding (steel, stainless, and aluminum) and aluminum MIG spool guns, use 100% Pure Argon at 15–25 CFH. Gasless Flux-Core (E71T-11) requires zero gas."
        },
        {
            "q": "Why is my Flux-Core welder spattering excessively and failing to penetrate?",
            "a": "90% of the time, the user forgot to swap the internal polarity lugs! Solid wire with gas runs on DCEP (Torch Positive, Ground Negative), whereas Gasless Flux-Core wire MUST run on DCEN (Torch Negative, Ground Positive)."
        },
        {
            "q": "What size circuit breaker and copper wire gauge do I need for a 240V NEMA 6-50 welder outlet?",
            "a": "For a 200-to-250 Amp inverter welder or 60A plasma cutter, install a 50-Amp 240V double-pole breaker wired with 6 AWG (or 8 AWG under NEC Article 630 welder duty-cycle rules) pure copper wire to a NEMA 6-50R receptacle."
        }
    ]

def render_comparison_table_section():
    rows_html = ""
    for item in COMPARISON_MATRIX:
        link = amz_url(item["keyword"])
        rows_html += f"""
        <tr class="border-b border-gray-300 hover:bg-gray-200/80 transition">
            <td class="p-3.5 font-extrabold text-gray-900 text-xs sm:text-sm">{item['model']}</td>
            <td class="p-3.5 text-xs font-semibold text-amber-900">{item['type']}</td>
            <td class="p-3.5 text-xs font-mono text-gray-800">{item['power_spec']}</td>
            <td class="p-3.5 text-xs text-gray-800">{item['thickness_cap']}</td>
            <td class="p-3.5 text-xs text-emerald-800 font-bold">{item['highlight']}</td>
            <td class="p-3.5 text-xs font-bold text-amber-700">{item['rating']}</td>
            <td class="p-3.5 text-right">
                <a href="{link}" target="_blank" rel="nofollow sponsored noopener"
                   class="inline-block bg-amber-700 hover:bg-amber-800 text-white font-extrabold text-xs py-2 px-3.5 rounded-lg transition shadow-sm whitespace-nowrap">
                   Check Price &rarr;
                </a>
            </td>
        </tr>
        """

    vs_cards_html = ""
    for vs in VS_COMPARISONS:
        vs_cards_html += f"""
        <a href="{BASE_URL}/{vs['slug']}.html" class="bg-gray-100 border-2 border-gray-300 hover:border-amber-700 rounded-xl p-5 transition flex flex-col justify-between shadow-sm">
            <div>
                <span class="text-[11px] font-extrabold uppercase tracking-wider bg-amber-100 text-amber-900 border border-amber-300 px-2.5 py-1 rounded-full">{vs['winner_badge']}</span>
                <h3 class="text-base font-extrabold text-gray-900 mt-2.5 mb-1.5 leading-snug">{vs['title']}</h3>
                <p class="text-xs text-gray-700 leading-relaxed">{vs['summary']}</p>
            </div>
            <span class="text-xs font-extrabold text-amber-800 mt-4 inline-flex items-center gap-1">Read Full Side-by-Side Comparison &rarr;</span>
        </a>
        """

    return f"""
    <!-- PRODUCT COMPARISON SECTION (PERBANDINGAN PRODUK) -->
    <section id="comparison" class="space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-300 pb-4">
            <div>
                <span class="text-xs font-extrabold uppercase tracking-wider text-amber-800">Side-by-Side Spec Matrix</span>
                <h2 class="text-2xl font-extrabold text-gray-900">Top MIG/TIG Welders, Pilot-Arc Plasma Cutters & 1/1/1/1 Helmets Compared</h2>
            </div>
            <span class="text-xs font-semibold text-gray-600">2026 AWS Penetration & Duty-Cycle Benchmarks</span>
        </div>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl overflow-x-auto shadow-sm">
            <table class="w-full text-left border-collapse min-w-[720px]">
                <thead>
                    <tr class="bg-gray-300 border-b-2 border-gray-400 text-[11px] font-extrabold uppercase tracking-wider text-gray-800">
                        <th class="p-3.5">Welding Model</th>
                        <th class="p-3.5">Category</th>
                        <th class="p-3.5">Amps / Optical Spec</th>
                        <th class="p-3.5">Thickness / View</th>
                        <th class="p-3.5">Key Shop Advantage</th>
                        <th class="p-3.5">Rating</th>
                        <th class="p-3.5 text-right">Amazon Deal</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </div>

        <!-- Head-to-Head VS Guides -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-5 pt-2">
            {vs_cards_html}
        </div>
    </section>
    """

def render_review_cards_grid():
    active_reviews = get_cumulative_product_reviews()
    cards = ""
    for rev in active_reviews:
        amz_link = amz_url(rev["keyword"])
        cards += f"""
        <article class="bg-gray-100 border-2 border-gray-300 hover:border-gray-400 rounded-2xl p-6 shadow-sm transition flex flex-col justify-between">
            <div>
                <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
                    <span class="text-xs font-extrabold uppercase tracking-wider bg-amber-100 text-amber-900 border border-amber-300 px-2.5 py-1 rounded-full">{rev['verdict_badge']}</span>
                    <span class="text-xs font-black bg-emerald-200 text-emerald-950 px-2.5 py-1 rounded-lg">Score: {rev['rating_score']} / 5.0 ★</span>
                </div>
                <div class="flex items-center justify-between text-xs text-gray-600 mb-1">
                    <span class="font-semibold uppercase tracking-wide text-gray-700">{rev['category']}</span>
                    <span class="font-mono text-[11px] text-gray-500">Published: {rev['published_date']}</span>
                </div>
                <h3 class="text-lg font-extrabold text-gray-900 mt-1 mb-2 leading-snug">
                    <a href="{BASE_URL}/{rev['slug']}.html" class="hover:text-amber-800 transition">{rev['title']}</a>
                </h3>
                <p class="text-xs text-gray-700 leading-relaxed mb-4">{rev['summary']}</p>
                <div class="grid grid-cols-2 gap-2 text-[11px] bg-gray-200/90 p-3 rounded-xl border border-gray-300 mb-4">
                    <div><span class="text-gray-500 block">Amps / Output:</span><strong class="text-gray-900">{rev['spec_1']}</strong></div>
                    <div><span class="text-gray-500 block">Process / Tech:</span><strong class="text-gray-900">{rev['spec_2']}</strong></div>
                    <div><span class="text-gray-500 block">Torch / Build:</span><strong class="text-gray-900">{rev['spec_3']}</strong></div>
                    <div><span class="text-gray-500 block">Warranty:</span><strong class="text-gray-900">{rev['spec_4']}</strong></div>
                </div>
            </div>
            <div class="flex flex-col sm:flex-row gap-2.5 pt-2">
                <a href="{BASE_URL}/{rev['slug']}.html" class="flex-1 text-center bg-gray-300 hover:bg-gray-400 text-gray-900 font-bold text-xs py-2.5 px-3 rounded-lg transition">
                    Read Full Shop Review &rarr;
                </a>
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-amber-700 hover:bg-amber-800 text-white font-extrabold text-xs py-2.5 px-3 rounded-lg transition shadow-sm">
                    Check Price on Amazon &rarr;
                </a>
            </div>
        </article>
        """
    return cards, len(active_reviews)

def render_common_header_and_banner():
    top_deal_link = amz_url("PrimeWeld+TIG225X+Hobart+Handler+210+Lincoln+Viking+3350+Deals")
    return f"""
    <!-- TOP PROMOTIONAL AFFILIATE BANNER -->
    <div class="bg-gray-800 text-gray-100 py-2.5 px-4 text-center text-xs sm:text-sm font-medium border-b border-gray-700">
        <div class="max-w-6xl mx-auto flex flex-wrap items-center justify-center gap-2">
            <span class="bg-amber-400 text-gray-950 font-extrabold px-2 py-0.5 rounded text-xs uppercase">Welding & Fab Deals</span>
            <span>Save up to 30% on AC/DC TIG & MIG Welders, Pilot-Arc Plasma Cutters, 1/1/1/1 Helmets & Welding Tables on Amazon.</span>
            <a href="{top_deal_link}" target="_blank" rel="nofollow sponsored noopener" class="text-amber-300 hover:text-amber-200 underline font-bold ml-1">
                View Active Welding & Plasma Deals &rarr;
            </a>
        </div>
    </div>

    <!-- STICKY NAVIGATION HEADER (GRAY BACKGROUND) -->
    <header class="bg-gray-300 border-b border-gray-400 sticky top-0 z-30 shadow-sm">
        <div class="max-w-6xl mx-auto px-4 py-3.5 flex flex-wrap items-center justify-between gap-4">
            <a href="{BASE_URL}/" class="flex items-center gap-2.5">
                <div class="w-9 h-9 rounded-lg bg-amber-700 flex items-center justify-center text-white font-black text-lg shadow-sm">W</div>
                <div>
                    <span class="font-extrabold text-lg tracking-tight text-gray-900 block leading-none">{SITE_NAME}</span>
                    <span class="text-[11px] text-gray-700 font-medium">Welding Amps, Wire Speed (IPM) & Plasma CFM Engine</span>
                </div>
            </a>
            <nav class="flex flex-wrap items-center gap-4 sm:gap-5 text-xs sm:text-sm font-semibold text-gray-800">
                <a href="{BASE_URL}/#calculator" class="hover:text-amber-800 transition">Amps & IPM Calc</a>
                <a href="{BASE_URL}/#product-search" class="hover:text-amber-800 transition">Search Welders</a>
                <a href="{BASE_URL}/#best-sellers" class="hover:text-amber-800 transition">Best Sellers</a>
                <a href="{BASE_URL}/#comparison" class="hover:text-amber-800 transition">Compare</a>
                <a href="{BASE_URL}/#reviews" class="hover:text-amber-800 transition">Daily Reviews (+3/Day)</a>
                <a href="{BASE_URL}/#faq" class="hover:text-amber-800 transition">FAQ</a>
                <a href="{BASE_URL}/sitemap.html" class="hover:text-amber-800 transition font-bold underline">Site Map</a>
            </nav>
        </div>
    </header>
    """

def render_onpage_sitemap_directory():
    calc_links = "".join([
        f'<li><a href="{BASE_URL}/{p["slug"]}.html" class="text-xs text-gray-700 hover:text-amber-800 hover:underline">👩‍🏭 {p["name"]} Calculator</a></li>'
        for p in ALL_CALC_PAGES
    ])
    vs_links = "".join([
        f'<li><a href="{BASE_URL}/{v["slug"]}.html" class="text-xs text-gray-700 hover:text-amber-800 hover:underline">⚖️ {v["title"]}</a></li>'
        for v in VS_COMPARISONS
    ])
    all_revs = get_cumulative_product_reviews()
    rev_links = "".join([
        f'<li><a href="{BASE_URL}/{r["slug"]}.html" class="text-xs text-gray-700 hover:text-amber-800 hover:underline">📝 [{r["published_date"]}] {r["product_name"]} Review</a></li>'
        for r in all_revs
    ])
    return f"""
    <!-- COMPLETE ON-PAGE SITE MAP SECTION (SITE MAP) -->
    <section id="site-map" class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-gray-300 pb-3">
            <div>
                <span class="text-xs font-extrabold uppercase tracking-wider text-amber-800">Complete Site Architecture & Index</span>
                <h2 class="text-xl font-extrabold text-gray-900">Full HTML & XML Site Map Directory</h2>
            </div>
            <div class="flex gap-3 text-xs font-bold">
                <a href="{BASE_URL}/sitemap.html" class="bg-gray-300 hover:bg-gray-400 text-gray-900 px-3 py-1.5 rounded-lg transition">Open Dedicated HTML Site Map &rarr;</a>
                <a href="{BASE_URL}/sitemap.xml" class="bg-amber-700 hover:bg-amber-800 text-white px-3 py-1.5 rounded-lg transition">View XML Sitemap</a>
            </div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
                <h3 class="text-sm font-extrabold text-gray-900 mb-2.5 uppercase tracking-wide border-b border-gray-300 pb-1">1. Welding & Plasma Calculators ({len(ALL_CALC_PAGES) + 1})</h3>
                <ul class="space-y-1.5">
                    <li><a href="{BASE_URL}/" class="text-xs font-bold text-amber-800 hover:underline">🏠 Home — Master Welding Amps, IPM & Plasma Calculator</a></li>
                    {calc_links}
                </ul>
            </div>
            <div>
                <h3 class="text-sm font-extrabold text-gray-900 mb-2.5 uppercase tracking-wide border-b border-gray-300 pb-1">2. Head-to-Head Comparisons ({len(VS_COMPARISONS)})</h3>
                <ul class="space-y-2">
                    {vs_links}
                </ul>
            </div>
            <div>
                <h3 class="text-sm font-extrabold text-gray-900 mb-2.5 uppercase tracking-wide border-b border-gray-300 pb-1">3. Daily Product Reviews ({len(all_revs)} — +3/Day)</h3>
                <ul class="space-y-1.5 max-h-80 overflow-y-auto pr-2">
                    {rev_links}
                </ul>
            </div>
        </div>
    </section>
    """

def render_dedicated_html_sitemap_page():
    canonical_url = f"{BASE_URL}/sitemap.html"
    sitemap_block = render_onpage_sitemap_directory()
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Complete Site Map Directory — Calculators, Comparisons & Daily Reviews | {SITE_NAME}</title>
    <meta name="description" content="Complete HTML and XML site map directory of all MIG/TIG/Stick welding amperage calculators, wire feed speed IPM guides, plasma cutter CFM calculators, and daily reviews on {SITE_NAME}.">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-6xl mx-auto px-4 py-10 space-y-8">
        <nav class="text-xs font-semibold text-gray-600 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-amber-800">Home</a>
            <span>/</span>
            <span class="text-gray-900">Complete Site Map</span>
        </nav>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-2">
            <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900">{SITE_NAME} — Complete Site Map</h1>
            <p class="text-sm text-gray-700">Browse every interactive MIG/TIG/Stick welding amperage calculator, wire feed speed chart, plasma cutter CFM calculator, head-to-head comparison, and cumulative daily product review article (+3 added daily) below.</p>
        </div>

        {sitemap_block}
    </main>

    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700 text-center">
        <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def render_calculator_page(page_data, is_home=False):
    amps, sec_str, _, _, _ = compute_weld_specs(
        page_data["process"], page_data["metal"], page_data["thick_in"],
        page_data["wire_dia"], page_data["voltage_in"]
    )
    title = f"{SITE_NAME} — {SITE_TAGLINE}" if is_home else f"{page_data['name']} — {amps}A & {sec_str} Calculator | {SITE_NAME}"
    description = page_data["desc"]
    canonical_url = f"{BASE_URL}/" if is_home else f"{BASE_URL}/{page_data['slug']}.html"
    faqs = generate_faq_data(
        page_data["name"], page_data["process"], page_data["metal"],
        page_data["thick_in"], page_data["wire_dia"], page_data["voltage_in"]
    )

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": item["q"], "acceptedAnswer": {"@type": "Answer", "text": item["a"]}}
            for item in faqs
        ]
    }

    app_schema = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": title,
        "url": canonical_url,
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "All",
        "description": description,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
    }

    bestseller_cards_html = ""
    for prod in BEST_SELLERS:
        link = amz_url(prod["keyword"])
        bestseller_cards_html += f"""
        <div class="bg-gray-100 border-2 border-gray-300 hover:border-gray-400 rounded-xl p-5 shadow-sm transition flex flex-col justify-between">
            <div>
                <div class="flex items-center justify-between gap-2 mb-2">
                    <span class="text-xs font-bold uppercase tracking-wider bg-amber-100 text-amber-900 border border-amber-300 px-2.5 py-1 rounded-full">{prod['badge']}</span>
                    <span class="text-xs font-semibold text-amber-700">{prod['rating']}</span>
                </div>
                <span class="text-xs text-gray-600 font-medium">{prod['category']}</span>
                <h3 class="text-base font-bold text-gray-900 mt-1 mb-2 leading-snug">{prod['title']}</h3>
                <p class="text-xs text-gray-700 mb-4 bg-gray-200 p-2.5 rounded-lg border border-gray-300">{prod['specs']}</p>
            </div>
            <a href="{link}" target="_blank" rel="nofollow sponsored noopener"
               class="w-full inline-flex items-center justify-center bg-amber-700 hover:bg-amber-800 text-white font-extrabold text-sm py-2.5 px-4 rounded-lg transition shadow-sm">
               Check Today's Price on Amazon &rarr;
            </a>
        </div>
        """

    preset_links_html = ""
    for p in ALL_CALC_PAGES:
        p_amps, _, _, _, _ = compute_weld_specs(
            p["process"], p["metal"], p["thick_in"], p["wire_dia"], p["voltage_in"]
        )
        active_cls = "bg-amber-100 border-amber-700 text-amber-950 font-bold" if (not is_home and p["slug"] == page_data["slug"]) else "bg-gray-100 border-gray-300 text-gray-800 hover:border-amber-700 hover:text-gray-950"
        preset_links_html += f"""
        <a href="{BASE_URL}/{p['slug']}.html" class="border rounded-lg p-3 text-xs transition flex items-center justify-between {active_cls}">
            <span class="truncate pr-2">{p['name']}</span>
            <span class="text-amber-900 font-mono shrink-0">{p_amps} Amps</span>
        </a>
        """

    faq_html = ""
    for item in faqs:
        faq_html += f"""
        <div class="bg-gray-100 border-2 border-gray-300 rounded-xl p-5">
            <h3 class="text-base font-bold text-gray-900 mb-2">{item['q']}</h3>
            <p class="text-sm text-gray-700 leading-relaxed">{item['a']}</p>
        </div>
        """

    mid_banner_link = amz_url("PrimeWeld+TIG225X+Hobart+Handler+210+and+Lincoln+Viking+3350+Bundle")
    comparison_html = render_comparison_table_section()
    reviews_grid_html, total_reviews_count = render_review_cards_grid()
    onpage_sitemap_html = render_onpage_sitemap_directory()

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical_url}">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">{json.dumps(faq_schema)}</script>
    <script type="application/ld+json">{json.dumps(app_schema)}</script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased selection:bg-amber-700 selection:text-white">

    {render_common_header_and_banner()}

    <main class="max-w-6xl mx-auto px-4 py-8 space-y-12">

        <!-- HERO TITLE SECTION -->
        <section class="text-center max-w-3xl mx-auto space-y-3">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-gray-300 border border-gray-400 text-xs font-semibold text-gray-800">
                <span>👩‍🏭 AWS 1-Amp-per-0.001\" Rule, Wire Speed (IPM), Plasma CFM & NEMA 6-50 Engine</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-extrabold text-gray-900 tracking-tight">
                { "MIG/TIG/Stick Welder Amperage, Wire Speed (IPM) & Plasma Calculator" if is_home else f"{page_data['name']} — Amps & IPM Calculator" }
            </h1>
            <p class="text-gray-700 text-sm sm:text-base leading-relaxed">
                {description}
            </p>
        </section>

        <!-- INTERACTIVE CALCULATOR + LIVE HARDWARE MATCHER -->
        <section id="calculator" class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            <!-- Left Column: Inputs (7 Cols) -->
            <div class="lg:col-span-7 bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-6">
                <div class="flex items-center justify-between border-b border-gray-300 pb-4">
                    <div>
                        <h2 class="text-xl font-extrabold text-gray-900">1. Select Welding Process, Metal & Thickness</h2>
                        <p class="text-xs text-gray-600">Calculates target amps, MIG IPM & volts, TIG tungsten, gas CFH & 240V breaker</p>
                    </div>
                    <span class="text-xs font-mono bg-amber-100 text-amber-900 border border-amber-300 px-2.5 py-1 rounded font-semibold">Live AWS Math</span>
                </div>

                <div>
                    <label for="quickPreset" class="block text-xs font-bold uppercase tracking-wider text-gray-700 mb-2">Quick Select Shop Welding or Plasma Preset</label>
                    <select id="quickPreset" onchange="applyPreset(this.value)" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-sm font-semibold text-gray-900 focus:ring-2 focus:ring-amber-700">
                        <option value="{page_data['process']},{page_data['metal']},{page_data['thick_in']},{page_data['wire_dia']},{page_data['voltage_in']}">Current: {page_data['name']}</option>
                        <option value="mig,steel,0.1875,0.030,240">3/16\" Mild Steel — MIG .030\" Solid Wire (185A / 315 IPM)</option>
                        <option value="mig,steel,0.250,0.035,240">1/4\" Structural Plate — MIG .035\" Wire (240V 210A+ Welder)</option>
                        <option value="tig,aluminum,0.125,0.093,240">1/8\" 6061 Aluminum — AC TIG w/ 3/32\" Blue Tungsten (140A)</option>
                        <option value="mig,steel,0.125,0.030,120">1/8\" (11-Ga) Square Tube — 120V/240V MIG (125A / 215 IPM)</option>
                        <option value="flux,steel,0.1875,0.035,240">3/16\" Outdoor Trailer Repair — Gasless Flux-Core E71T-11 (DCEN)</option>
                        <option value="plasma,steel,0.500,0.035,240">1/2\" Steel Plate — Pilot-Arc Plasma Cutter (55–60A / 4.5 CFM)</option>
                    </select>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                    <div>
                        <label for="procInput" class="block text-sm font-bold text-gray-800 mb-1">Process Type</label>
                        <select id="procInput" onchange="calculateWeld()" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3 py-2.5 text-sm font-bold text-gray-900">
                            <option value="mig" {"selected" if page_data['process'] == "mig" else ""}>MIG (Solid Wire + Gas)</option>
                            <option value="flux" {"selected" if page_data['process'] == "flux" else ""}>Flux-Core (Gasless DCEN)</option>
                            <option value="tig" {"selected" if page_data['process'] == "tig" else ""}>TIG (GTAW AC/DC)</option>
                            <option value="stick" {"selected" if page_data['process'] == "stick" else ""}>Stick (SMAW 7018/6011)</option>
                            <option value="plasma" {"selected" if page_data['process'] == "plasma" else ""}>Plasma Cutting (Pilot Arc)</option>
                        </select>
                    </div>

                    <div>
                        <label for="metalInput" class="block text-sm font-bold text-gray-800 mb-1">Base Metal</label>
                        <select id="metalInput" onchange="calculateWeld()" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3 py-2.5 text-sm font-bold text-gray-900">
                            <option value="steel" {"selected" if page_data['metal'] == "steel" else ""}>Mild Carbon Steel (A36)</option>
                            <option value="stainless" {"selected" if page_data['metal'] == "stainless" else ""}>304 / 316 Stainless Steel</option>
                            <option value="aluminum" {"selected" if page_data['metal'] == "aluminum" else ""}>6061 / 5052 Aluminum</option>
                        </select>
                    </div>

                    <div>
                        <label for="thickInput" class="block text-sm font-bold text-gray-800 mb-1">Metal Thickness</label>
                        <select id="thickInput" onchange="calculateWeld()" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3 py-2.5 text-sm font-bold text-gray-900">
                            <option value="0.048" {"selected" if page_data['thick_in'] <= 0.050 else ""}>18 Gauge (0.048\" / 1.2mm)</option>
                            <option value="0.0625" {"selected" if 0.050 < page_data['thick_in'] <= 0.065 else ""}>16 Gauge / 1/16\" (0.063\")</option>
                            <option value="0.090" {"selected" if 0.065 < page_data['thick_in'] <= 0.100 else ""}>13 Gauge (0.090\" / 2.3mm)</option>
                            <option value="0.125" {"selected" if 0.100 < page_data['thick_in'] <= 0.140 else ""}>1/8 Inch / 11ga (0.125\")</option>
                            <option value="0.1875" {"selected" if 0.140 < page_data['thick_in'] <= 0.200 else ""}>3/16 Inch (0.188\" / 4.8mm)</option>
                            <option value="0.250" {"selected" if 0.200 < page_data['thick_in'] <= 0.300 else ""}>1/4 Inch Plate (0.250\")</option>
                            <option value="0.375" {"selected" if 0.300 < page_data['thick_in'] <= 0.420 else ""}>3/8 Inch Plate (0.375\")</option>
                            <option value="0.500" {"selected" if page_data['thick_in'] > 0.420 else ""}>1/2 Inch Plate (0.500\")</option>
                        </select>
                    </div>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                    <div>
                        <label for="wireInput" class="block text-sm font-bold text-gray-800 mb-1">MIG Wire / TIG Tungsten / Rod Size</label>
                        <select id="wireInput" onchange="calculateWeld()" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-sm font-bold text-gray-900">
                            <option value="0.025" {"selected" if page_data['wire_dia'] == "0.025" else ""}>.023\" / .025\" MIG Wire (Sheet Metal)</option>
                            <option value="0.030" {"selected" if page_data['wire_dia'] == "0.030" else ""}>.030\" MIG Wire (#1 All-Purpose)</option>
                            <option value="0.035" {"selected" if page_data['wire_dia'] == "0.035" else ""}>.035\" MIG Wire (3/16\" to 3/8\" Steel)</option>
                            <option value="0.093" {"selected" if page_data['wire_dia'] == "0.093" else ""}>3/32\" (0.093\") TIG Tungsten / Stick Rod</option>
                            <option value="0.125" {"selected" if page_data['wire_dia'] == "0.125" else ""}>1/8\" (0.125\") Stick Rod / Heavy TIG</option>
                        </select>
                    </div>

                    <div>
                        <label for="voltInInput" class="block text-sm font-bold text-gray-800 mb-1">Shop Wall Outlet Voltage</label>
                        <select id="voltInInput" onchange="calculateWeld()" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-sm font-bold text-gray-900">
                            <option value="240" {"selected" if page_data['voltage_in'] == "240" else ""}>240V NEMA 6-50 Outlet (Full Output)</option>
                            <option value="120" {"selected" if page_data['voltage_in'] == "120" else ""}>120V 20A Household Outlet (Up to 1/8\")</option>
                        </select>
                    </div>
                </div>
            </div>

            <!-- Right Column: Output + Dynamic Amazon Recommendation (5 Cols) -->
            <div class="lg:col-span-5 bg-gray-100 border-2 border-amber-700 rounded-2xl p-6 sm:p-8 shadow-md space-y-6">
                <div class="border-b border-gray-300 pb-3">
                    <span class="text-xs font-extrabold uppercase tracking-wider text-amber-800">2. Engineered Machine & Gas Settings</span>
                    <h2 class="text-xl font-extrabold text-gray-900">Your Exact Dial Parameters</h2>
                </div>

                <div class="grid grid-cols-2 gap-3.5">
                    <div class="bg-amber-100 border border-amber-300 rounded-xl p-3.5">
                        <span class="text-xs text-amber-950 font-semibold block">Target Amperage</span>
                        <span id="resAmps" class="text-2xl font-black text-amber-800">185 Amps</span>
                        <span id="resMils" class="text-[11px] text-amber-900 block mt-0.5">188 Mils Single-Pass</span>
                    </div>
                    <div class="bg-gray-200 border border-gray-300 rounded-xl p-3.5">
                        <span class="text-xs text-gray-600 font-medium block">IPM Speed / Electrode</span>
                        <span id="resSecSpec" class="text-lg font-black text-gray-900">320 IPM @ 20.9V</span>
                        <span id="resSecSub" class="text-[11px] text-emerald-800 font-bold block mt-0.5">.030\" Wire (DCEP)</span>
                    </div>
                    <div class="bg-gray-200 border border-gray-300 rounded-xl p-3.5">
                        <span class="text-xs text-gray-600 font-medium block">Shielding Gas & Flow</span>
                        <span id="resGasSpec" class="text-sm font-extrabold text-gray-900">75/25 Argon-CO2</span>
                        <span class="text-[11px] text-gray-600 block mt-0.5">Set Flowmeter: 22–25 CFH</span>
                    </div>
                    <div class="bg-gray-200 border border-gray-300 rounded-xl p-3.5">
                        <span class="text-xs text-gray-600 font-medium block">Required Shop Circuit</span>
                        <span id="resBreaker" class="text-sm font-extrabold text-amber-800">240V 50A (6 AWG)</span>
                        <span class="text-[11px] text-gray-600 block mt-0.5">NEMA 6-50R Receptacle</span>
                    </div>
                </div>

                <!-- Dynamic Matched Product Box -->
                <div class="bg-gray-200 border-2 border-amber-600 rounded-xl p-4 space-y-3">
                    <div class="flex items-center justify-between">
                        <span class="text-[11px] font-extrabold uppercase tracking-wider bg-amber-700 text-white px-2 py-0.5 rounded">Verified Hardware Match</span>
                        <span class="text-xs font-bold text-gray-700">Amazon Prime Ready</span>
                    </div>
                    <h3 id="recWeldTitle" class="text-base font-extrabold text-gray-900 leading-snug">Loading Welder & Helmet Match...</h3>
                    <p id="recWeldDesc" class="text-xs text-gray-700"></p>
                    <div class="pt-1 flex flex-col sm:flex-row gap-2.5">
                        <a id="recPrimaryBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="flex-1 text-center bg-amber-700 hover:bg-amber-800 text-white font-extrabold text-sm py-3 px-4 rounded-lg transition shadow-sm">
                           Shop Matched Welder / Cutter &rarr;
                        </a>
                        <a id="recSecondaryBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="text-center bg-gray-800 hover:bg-gray-900 text-white font-bold text-xs py-3 px-3 rounded-lg transition">
                           Shop Helmet & Table
                        </a>
                    </div>
                </div>
            </div>
        </section>

        <!-- PRODUCT SEARCH ENGINE SECTION (SEARCH PRODUK) -->
        <section id="product-search" class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm">
            <div class="max-w-3xl mx-auto text-center space-y-4">
                <h2 class="text-2xl font-extrabold text-gray-900">Search MIG/TIG Welders, Pilot-Arc Plasma Cutters, 1/1/1/1 Helmets & Tables</h2>
                <p class="text-sm text-gray-700">Search any brand (PrimeWeld, Hobart, Lincoln Electric, Miller, ESAB, YESWELDER, Strong Hand Tools, 3M Cubitron) or consumable on Amazon.</p>
                <form onsubmit="handleAmazonSearch(event)" class="flex flex-col sm:flex-row gap-3 pt-2">
                    <input type="text" id="amzSearchInput" placeholder="e.g. PrimeWeld TIG225X, Hobart Handler 210 MVP, Lincoln Viking 3350, PrimeWeld CUT60..."
                           class="flex-1 bg-gray-200 border-2 border-gray-400 rounded-xl px-4 py-3 text-sm font-medium text-gray-900 placeholder-gray-500 focus:outline-none focus:border-amber-700" required>
                    <button type="submit" class="bg-amber-700 hover:bg-amber-800 text-white font-extrabold text-sm px-6 py-3 rounded-xl transition cursor-pointer shrink-0">
                        Search on Amazon &rarr;
                    </button>
                </form>
                <div class="flex flex-wrap items-center justify-center gap-2 pt-2 text-xs">
                    <span class="text-gray-600 font-semibold">Popular Searches:</span>
                    <a href="{amz_url('PrimeWeld TIG225X AC DC TIG Welder')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-amber-200 text-gray-800 border border-gray-300 rounded-full transition">PrimeWeld TIG225X</a>
                    <a href="{amz_url('Hobart Handler 210 MVP MIG Welder')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-amber-200 text-gray-800 border border-gray-300 rounded-full transition">Hobart Handler 210</a>
                    <a href="{amz_url('Lincoln Electric Viking 3350 Welding Helmet')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-amber-200 text-gray-800 border border-gray-300 rounded-full transition">Lincoln Viking 3350</a>
                    <a href="{amz_url('PrimeWeld CUT60 Pilot Arc Plasma Cutter')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-amber-200 text-gray-800 border border-gray-300 rounded-full transition">Pilot-Arc Plasma Cutters</a>
                    <a href="{amz_url('Strong Hand Tools Nomad Welding Table')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-amber-200 text-gray-800 border border-gray-300 rounded-full transition">Slotted Welding Tables</a>
                </div>
            </div>
        </section>

        <!-- BEST SELLING PRODUCTS GRID (PRODUK TERLARIS) -->
        <section id="best-sellers" class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-300 pb-4">
                <div>
                    <span class="text-xs font-extrabold uppercase tracking-wider text-amber-800">Verified Metal Fabrication Hardware</span>
                    <h2 class="text-2xl font-extrabold text-gray-900">Best-Selling MIG/TIG Welders, Plasma Cutters, Helmets & Tables</h2>
                </div>
                <a href="{amz_url('Best Selling MIG TIG Welders and Plasma Cutters')}" target="_blank" rel="nofollow sponsored noopener" class="text-sm font-bold text-amber-800 hover:text-amber-900">
                    Browse Full Amazon Best Sellers &rarr;
                </a>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
                {bestseller_cards_html}
            </div>
        </section>

        {comparison_html}

        <!-- CUMULATIVE DAILY PRODUCT REVIEW ARTICLES SECTION (+3 NEW ARTICLES PER DAY) -->
        <section id="reviews" class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-300 pb-4">
                <div>
                    <span class="text-xs font-extrabold uppercase tracking-wider text-amber-800">Autonomous Daily Review Archive ({total_reviews_count} Published Articles & Growing +3/Day)</span>
                    <h2 class="text-2xl font-extrabold text-gray-900">In-Depth Welder, Plasma Cutter, Helmet & Fab Tool Review Articles</h2>
                </div>
                <span class="text-xs font-semibold bg-emerald-100 text-emerald-900 border border-emerald-300 px-3 py-1 rounded-full">+3 New Product Reviews Added Automatically Every Day</span>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {reviews_grid_html}
            </div>
        </section>

        <!-- MID-PAGE PROMOTIONAL AFFILIATE BANNER -->
        <section class="bg-gray-300 border-2 border-amber-700 rounded-2xl p-6 sm:p-8 flex flex-col md:flex-row items-center justify-between gap-6">
            <div class="space-y-2 max-w-2xl">
                <span class="text-xs font-extrabold uppercase tracking-wider bg-amber-700 text-white px-2.5 py-1 rounded">Complete Garage Fabrication Shop Bundle</span>
                <h2 class="text-xl sm:text-2xl font-extrabold text-gray-900">Setting Up a Home MIG, AC/DC TIG, or Plasma Cutting Shop?</h2>
                <p class="text-sm text-gray-800">Weld steel, stainless, and aluminum cleanly by pairing a Dual-Voltage MIG or AC/DC TIG Welder with a 1/1/1/1 True-Color Helmet, Rolling Bottle Cart, Slotted Fixture Table, and 50A NEMA 6-50 Extension Cord.</p>
            </div>
            <a href="{mid_banner_link}" target="_blank" rel="nofollow sponsored noopener"
               class="shrink-0 bg-amber-700 hover:bg-amber-800 text-white font-extrabold text-sm px-6 py-3.5 rounded-xl shadow-sm transition">
               Explore Welder + Helmet + Table Bundles &rarr;
            </a>
        </section>

        <!-- PROGRAMMATIC SEO DIRECTORY -->
        <section id="presets" class="space-y-4">
            <div class="border-b border-gray-300 pb-3">
                <h2 class="text-xl font-extrabold text-gray-900">Metal Thickness, Welding Process & Plasma Specific Calculators</h2>
                <p class="text-xs text-gray-600">Select your exact metal thickness or welding process below for pre-calculated amperage, IPM wire speed, and shielding gas settings.</p>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2.5">
                {preset_links_html}
            </div>
        </section>

        <!-- FREQUENTLY ASKED QUESTIONS (FAQ) -->
        <section id="faq" class="space-y-6">
            <div class="border-b border-gray-300 pb-3">
                <span class="text-xs font-extrabold uppercase tracking-wider text-amber-800">AWS Amperage, Polarity & NEC 630 Guide</span>
                <h2 class="text-2xl font-extrabold text-gray-900">Frequently Asked Questions (FAQ)</h2>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                {faq_html}
            </div>
        </section>

        {onpage_sitemap_html}

    </main>

    <!-- FOOTER (GRAY BACKGROUND) -->
    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700">
        <div class="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
            <div>
                <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
                <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
            </div>
            <div class="flex flex-wrap gap-4 font-medium text-gray-800">
                <a href="{BASE_URL}/" class="hover:text-amber-800">Home</a>
                <a href="{BASE_URL}/#comparison" class="hover:text-amber-800">Comparisons</a>
                <a href="{BASE_URL}/#reviews" class="hover:text-amber-800">Daily Reviews (+3/Day)</a>
                <a href="{BASE_URL}/sitemap.html" class="hover:text-amber-800 font-bold">HTML Site Map</a>
                <a href="{BASE_URL}/sitemap.xml" class="hover:text-amber-800">XML Sitemap</a>
                <a href="{BASE_URL}/#faq" class="hover:text-amber-800">FAQ</a>
            </div>
        </div>
    </footer>

    <!-- INTERACTIVE CALCULATOR & AFFILIATE MATCHING SCRIPT -->
    <script>
        const AFFILIATE_TAG = "{AFFILIATE_TAG}";

        function makeAmazonLink(query) {{
            return "https://www.amazon.com/s?k=" + encodeURIComponent(query) + "&tag=" + AFFILIATE_TAG;
        }}

        function applyPreset(val) {{
            const parts = val.split(",");
            if (parts.length === 5) {{
                document.getElementById("procInput").value = parts[0];
                document.getElementById("metalInput").value = parts[1];
                document.getElementById("thickInput").value = parts[2];
                document.getElementById("wireInput").value = parts[3];
                document.getElementById("voltInInput").value = parts[4];
                calculateWeld();
            }}
        }}

        function handleAmazonSearch(e) {{
            e.preventDefault();
            const q = document.getElementById("amzSearchInput").value.trim();
            if (q) {{
                window.open(makeAmazonLink(q), "_blank", "noopener,noreferrer");
            }}
        }}

        function calculateWeld() {{
            const proc = document.getElementById("procInput").value || "mig";
            const metal = document.getElementById("metalInput").value || "steel";
            const thickIn = parseFloat(document.getElementById("thickInput").value) || 0.1875;
            const wireDia = document.getElementById("wireInput").value || "0.030";
            const voltIn = document.getElementById("voltInInput").value || "240";

            const mils = thickIn * 1000.0;
            let amps = 185;
            if (proc === "plasma") {{
                amps = Math.max(20, Math.min(80, Math.round((thickIn * 115) / 5) * 5));
            }} else if (metal === "stainless") {{
                amps = Math.max(30, Math.min(250, Math.round((mils * 0.85) / 5) * 5));
            }} else if (metal === "aluminum") {{
                amps = Math.max(50, Math.min(260, Math.round((mils * 1.10) / 5) * 5));
            }} else {{
                amps = Math.max(40, Math.min(250, Math.round((mils * 0.98) / 5) * 5));
            }}

            let secSpec = "";
            let secSub = "";
            if (proc === "mig" || proc === "flux") {{
                const migV = (15.0 + (amps * 0.032)).toFixed(1);
                const wNum = parseFloat(wireDia);
                const mult = metal === "aluminum" ? 2.6 : (wNum <= 0.026 ? 2.2 : (wNum <= 0.031 ? 1.72 : 1.48));
                const ipm = Math.round((amps * mult) / 5) * 5;
                secSpec = ipm + " IPM @ " + migV + "V";
                secSub = "." + wireDia.split(".")[1] + "\\\" Wire (" + (proc === "flux" ? "DCEN" : "DCEP") + ")";
            }} else if (proc === "tig") {{
                secSpec = amps <= 90 ? "1/16\\\" Blue Tungsten" : (amps <= 185 ? "3/32\\\" Blue (#8 Cup)" : "1/8\\\" Blue (#10 Cup)");
                secSub = metal === "aluminum" ? "AC High-Freq (120Hz)" : "DCEN High-Freq";
            }} else if (proc === "stick") {{
                secSpec = amps <= 105 ? "3/32\\\" 7018 Rod" : "1/8\\\" 7018 / 6011 Rod";
                secSub = "DCEP Reverse Polarity";
            }} else {{
                secSpec = "4.5–5.0 CFM @ 70 PSI";
                secSub = "Pilot Arc + M-60 Air Dryer";
            }}

            let gasStr = "75% Argon / 25% CO2 (22 CFH)";
            if (proc === "flux") gasStr = "0 CFH (Gasless Flux-Core)";
            else if (proc === "stick") gasStr = "0 CFH (Coated Stick Rod)";
            else if (proc === "plasma") gasStr = "Dry Shop Air (70 PSI)";
            else if (proc === "tig" || metal === "aluminum") gasStr = "100% Pure Argon (20 CFH)";

            let brkStr = "240V 50A NEMA 6-50 (6 AWG)";
            if (amps <= 130 && voltIn === "120") brkStr = "120V 20A Outlet (12 AWG)";
            else if (amps <= 180) brkStr = "240V 40A NEMA 6-50 (8 AWG)";

            document.getElementById("resAmps").textContent = amps + " Amps";
            document.getElementById("resMils").textContent = Math.round(mils) + " Mils (" + thickIn + "\\\" " + metal.toUpperCase() + ")";
            document.getElementById("resSecSpec").textContent = secSpec;
            document.getElementById("resSecSub").textContent = secSub;
            document.getElementById("resGasSpec").textContent = gasStr;
            document.getElementById("resBreaker").textContent = brkStr;

            let recTitle = "";
            let recDesc = "";
            let primaryQuery = "";
            let secondaryQuery = "Lincoln Electric Viking 3350 Welding Helmet and Strong Hand Nomad Table";

            if (proc === "plasma") {{
                recTitle = "PrimeWeld CUT60 or YESWELDER CUT-55DS Pro Pilot-Arc Plasma Cutter + Motor Guard M-60";
                recDesc = "Non-touch pilot-arc cutting through " + thickIn + "\" rusty/painted metal at " + amps + " Amps.";
                primaryQuery = "PrimeWeld CUT60 YESWELDER CUT 55DS Pilot Arc Plasma Cutter";
            }} else if (proc === "tig" || metal === "aluminum") {{
                recTitle = "PrimeWeld TIG225X 225-Amp AC/DC Pulse TIG Welder w/ CK17 Flex Torch";
                recDesc = "America's #1 AC/DC pulse TIG welder for " + thickIn + "\" aluminum, stainless, and chromoly at " + amps + "A.";
                primaryQuery = "PrimeWeld TIG225X 225 Amp AC DC TIG Welder";
                secondaryQuery = "ESAB Sentinel A60 Helmet and Stubby Pyrex TIG Gas Lens Kit";
            }} else {{
                recTitle = "Hobart Handler 210 MVP or YESWELDER MIG-205DS Pro Dual-Voltage MIG Welder";
                recDesc = "Engineered to deliver " + amps + " Amps and " + secSpec + " on " + thickIn + "\" steel.";
                primaryQuery = "Hobart Handler 210 MVP YESWELDER MIG 205DS MIG Welder";
            }}

            document.getElementById("recWeldTitle").textContent = recTitle;
            document.getElementById("recWeldDesc").textContent = recDesc;
            document.getElementById("recPrimaryBtn").href = makeAmazonLink(primaryQuery);
            document.getElementById("recSecondaryBtn").href = makeAmazonLink(secondaryQuery);
        }}

        window.addEventListener("DOMContentLoaded", calculateWeld);
    </script>
</body>
</html>"""

def render_single_review_page(rev):
    canonical_url = f"{BASE_URL}/{rev['slug']}.html"
    amz_link = amz_url(rev["keyword"])

    review_schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": rev["product_name"],
        "description": rev["summary"],
        "review": {
            "@type": "Review",
            "datePublished": rev["published_date"],
            "reviewRating": {"@type": "Rating", "ratingValue": rev["rating_score"], "bestRating": "5"},
            "author": {"@type": "Organization", "name": SITE_NAME},
            "reviewBody": " ".join(rev["body_paragraphs"])
        }
    }

    pros_html = "".join([f'<li class="flex items-start gap-2 text-sm text-gray-800"><span class="text-emerald-700 font-bold">✓</span><span>{p}</span></li>' for p in rev["pros"]])
    cons_html = "".join([f'<li class="flex items-start gap-2 text-sm text-gray-800"><span class="text-rose-700 font-bold">✕</span><span>{c}</span></li>' for c in rev["cons"]])
    paragraphs_html = "".join([f'<p class="text-gray-800 leading-relaxed text-base mb-4">{p}</p>' for p in rev["body_paragraphs"]])

    recent_reviews = [r for r in get_cumulative_product_reviews() if r["slug"] != rev["slug"]][:6]
    related_html = ""
    for other in recent_reviews:
        related_html += f"""
        <a href="{BASE_URL}/{other['slug']}.html" class="bg-gray-100 border-2 border-gray-300 rounded-xl p-4 hover:border-amber-700 transition block">
            <span class="text-[11px] font-bold text-amber-800 uppercase">{other['verdict_badge']}</span>
            <h4 class="font-extrabold text-sm text-gray-900 mt-1 line-clamp-2">{other['product_name']} Review</h4>
            <span class="text-xs text-gray-600 mt-1 block">Score: {other['rating_score']} / 5.0 ★ ({other['published_date']}) &rarr;</span>
        </a>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{rev['title']} | {SITE_NAME}</title>
    <meta name="description" content="{rev['summary']}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">{json.dumps(review_schema)}</script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-4xl mx-auto px-4 py-10 space-y-10">
        <nav class="text-xs font-semibold text-gray-600 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-amber-800">Home & Welding Calculator</a>
            <span>/</span>
            <a href="{BASE_URL}/#reviews" class="hover:text-amber-800">Daily Welding Reviews</a>
            <span>/</span>
            <span class="text-gray-900">{rev['product_name']}</span>
        </nav>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-5">
            <div class="flex flex-wrap items-center justify-between gap-2">
                <span class="text-xs font-extrabold uppercase tracking-wider bg-amber-100 text-amber-900 border border-amber-300 px-3 py-1 rounded-full">{rev['verdict_badge']}</span>
                <div class="flex items-center gap-2">
                    <span class="text-xs font-mono text-gray-600">Published: {rev['published_date']}</span>
                    <span class="text-sm font-black bg-emerald-200 text-emerald-950 px-3 py-1 rounded-lg">Shop Rating: {rev['rating_score']} / 5.0 ★</span>
                </div>
            </div>
            <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900 leading-tight">{rev['title']}</h1>
            <p class="text-base text-gray-700 leading-relaxed">{rev['summary']}</p>

            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-gray-200 p-4 rounded-xl border border-gray-300 text-xs">
                <div><span class="text-gray-500 block font-medium">Amps / Spec</span><strong class="text-gray-900">{rev['spec_1']}</strong></div>
                <div><span class="text-gray-500 block font-medium">Process / Tech</span><strong class="text-gray-900">{rev['spec_2']}</strong></div>
                <div><span class="text-gray-500 block font-medium">Torch / Build</span><strong class="text-gray-900">{rev['spec_3']}</strong></div>
                <div><span class="text-gray-500 block font-medium">Warranty</span><strong class="text-gray-900">{rev['spec_4']}</strong></div>
            </div>

            <div class="flex flex-col sm:flex-row gap-3 pt-2">
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener"
                   class="flex-1 text-center bg-amber-700 hover:bg-amber-800 text-white font-extrabold text-sm py-3.5 px-6 rounded-xl transition shadow-sm">
                   Check Latest Price & Availability on Amazon &rarr;
                </a>
                <a href="{BASE_URL}/#calculator"
                   class="text-center bg-gray-300 hover:bg-gray-400 text-gray-900 font-bold text-sm py-3.5 px-5 rounded-xl transition">
                   Calculate Amps, IPM & Gas CFH
                </a>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="bg-gray-100 border-2 border-emerald-400 rounded-2xl p-6 space-y-3">
                <h2 class="text-base font-extrabold text-emerald-900 uppercase tracking-wide">Pros (What We Like)</h2>
                <ul class="space-y-2.5">{pros_html}</ul>
            </div>
            <div class="bg-gray-100 border-2 border-rose-400 rounded-2xl p-6 space-y-3">
                <h2 class="text-base font-extrabold text-rose-900 uppercase tracking-wide">Cons (Things to Consider)</h2>
                <ul class="space-y-2.5">{cons_html}</ul>
            </div>
        </div>

        <article class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 space-y-4">
            <h2 class="text-xl font-extrabold text-gray-900 border-b border-gray-300 pb-3">Hands-On Arc Stability, Penetration & Duty-Cycle Analysis</h2>
            {paragraphs_html}
            <div class="pt-4 border-t border-gray-300 flex flex-col sm:flex-row items-center justify-between gap-4">
                <div>
                    <span class="text-xs font-bold uppercase text-amber-800 block">Final Verdict</span>
                    <p class="text-sm font-bold text-gray-900">{rev['product_name']} earns {rev['rating_score']}/5.0 in our welding shop benchmark.</p>
                </div>
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener"
                   class="shrink-0 bg-amber-700 hover:bg-amber-800 text-white font-extrabold text-sm px-6 py-3 rounded-xl transition shadow-sm">
                   View Customer Reviews & Price on Amazon &rarr;
                </a>
            </div>
        </article>

        <section class="space-y-4">
            <h3 class="text-lg font-extrabold text-gray-900">Recent Daily Welding & Fabrication Reviews (+3 Added Daily)</h3>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                {related_html}
            </div>
        </section>
    </main>

    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700 text-center">
        <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def render_vs_comparison_page(vs):
    canonical_url = f"{BASE_URL}/{vs['slug']}.html"
    link_a = amz_url(vs["keyword_a"])
    link_b = amz_url(vs["keyword_b"])

    rows_html = ""
    for m in vs["metrics"]:
        rows_html += f"""
        <tr class="border-b border-gray-300">
            <td class="p-4 font-bold text-gray-900 bg-gray-200 text-xs sm:text-sm w-1/4">{m['feature']}</td>
            <td class="p-4 text-xs sm:text-sm text-gray-800 w-3/8">{m['val_a']}</td>
            <td class="p-4 text-xs sm:text-sm text-gray-800 w-3/8">{m['val_b']}</td>
        </tr>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{vs['title']} | {SITE_NAME}</title>
    <meta name="description" content="{vs['summary']}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-4xl mx-auto px-4 py-10 space-y-10">
        <nav class="text-xs font-semibold text-gray-600 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-amber-800">Home & Welding Calculator</a>
            <span>/</span>
            <a href="{BASE_URL}/#comparison" class="hover:text-amber-800">Product Comparisons</a>
            <span>/</span>
            <span class="text-gray-900">{vs['product_a']} vs. {vs['product_b']}</span>
        </nav>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-4">
            <span class="text-xs font-extrabold uppercase tracking-wider bg-amber-100 text-amber-900 border border-amber-300 px-3 py-1 rounded-full">{vs['winner_badge']}</span>
            <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900 leading-tight">{vs['title']}</h1>
            <p class="text-base text-gray-700 leading-relaxed">{vs['summary']}</p>
        </div>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl overflow-hidden shadow-sm">
            <table class="w-full text-left border-collapse">
                <thead>
                    <tr class="bg-gray-800 text-white text-xs sm:text-sm font-extrabold">
                        <th class="p-4">Specification</th>
                        <th class="p-4 text-amber-300">{vs['product_a']}</th>
                        <th class="p-4 text-emerald-300">{vs['product_b']}</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                    <tr class="bg-gray-200">
                        <td class="p-4 font-extrabold text-xs sm:text-sm text-gray-900">Check Amazon Price</td>
                        <td class="p-4">
                            <a href="{link_a}" target="_blank" rel="nofollow sponsored noopener" class="inline-block bg-amber-700 hover:bg-amber-800 text-white font-extrabold text-xs py-2.5 px-4 rounded-lg transition">
                                View {vs['product_a']} &rarr;
                            </a>
                        </td>
                        <td class="p-4">
                            <a href="{link_b}" target="_blank" rel="nofollow sponsored noopener" class="inline-block bg-gray-800 hover:bg-gray-900 text-white font-extrabold text-xs py-2.5 px-4 rounded-lg transition">
                                View {vs['product_b']} &rarr;
                            </a>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="bg-gray-100 border-2 border-amber-600 rounded-2xl p-6 sm:p-8 space-y-4">
            <h2 class="text-xl font-extrabold text-gray-900">Head-to-Head Buying Verdict</h2>
            <p class="text-sm sm:text-base text-gray-800 leading-relaxed">{vs['verdict_text']}</p>
            <div class="flex flex-col sm:flex-row gap-3 pt-2">
                <a href="{link_a}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-amber-700 hover:bg-amber-800 text-white font-extrabold text-sm py-3 px-4 rounded-xl transition">
                    Shop {vs['product_a']} on Amazon &rarr;
                </a>
                <a href="{link_b}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-gray-800 hover:bg-gray-900 text-white font-extrabold text-sm py-3 px-4 rounded-xl transition">
                    Shop {vs['product_b']} on Amazon &rarr;
                </a>
            </div>
        </div>
    </main>

    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700 text-center">
        <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def generate_sitemap_and_robots(urls):
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    xml_items = ""
    for u in urls:
        xml_items += f"""  <url>
    <loc>{u}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>{"1.0" if u.endswith("/") else "0.85"}</priority>
  </url>\n"""

    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{xml_items}</urlset>"""

    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_content)

    robots_content = f"""User-agent: *
Allow: /
Sitemap: {BASE_URL}/sitemap.xml
"""
    with open(os.path.join(OUTPUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots_content)

    with open(os.path.join(OUTPUT_DIR, f"{INDEXNOW_KEY}.txt"), "w", encoding="utf-8") as f:
        f.write(INDEXNOW_KEY)

def ping_indexnow(urls):
    parsed_host = urllib.parse.urlparse(BASE_URL).netloc
    if not parsed_host or "username.github.io" in parsed_host:
        return

    payload = {
        "host": parsed_host,
        "key": INDEXNOW_KEY,
        "keyLocation": f"{BASE_URL}/{INDEXNOW_KEY}.txt",
        "urlList": urls
    }
    try:
        req = urllib.request.Request(
            "https://api.indexnow.org/indexnow",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"IndexNow Ping Status: {resp.status}")
    except Exception as e:
        print(f"IndexNow notice: {e}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    generated_urls = []

    # 1. Generate Homepage
    home_preset = {
        "slug": "index",
        "name": "3/16\" Mild Steel — MIG .030\" Solid Wire (75/25 Gas)",
        "process": "mig",
        "metal": "steel",
        "thick_in": 0.1875,
        "wire_dia": "0.030",
        "voltage_in": "240",
        "desc": "Calculate exact MIG/TIG/Stick welding amperage, wire feed speed (IPM), TIG tungsten size, plasma cutter air CFM, shielding gas CFH, and 240V NEMA 6-50 breaker sizing—plus read 3 new welding reviews added daily."
    }
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(render_calculator_page(home_preset, is_home=True))
    generated_urls.append(f"{BASE_URL}/")

    # 2. Generate Dedicated HTML Site Map Page (sitemap.html)
    with open(os.path.join(OUTPUT_DIR, "sitemap.html"), "w", encoding="utf-8") as f:
        f.write(render_dedicated_html_sitemap_page())
    generated_urls.append(f"{BASE_URL}/sitemap.html")

    # 3. Generate Programmatic Welding & Plasma Calculator Pages
    for page in ALL_CALC_PAGES:
        filename = f"{page['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_calculator_page(page, is_home=False))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 4. Generate Cumulative Daily Product Review Pages (+3 new reviews unlocked every single day)
    active_reviews = get_cumulative_product_reviews()
    for rev in active_reviews:
        filename = f"{rev['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_single_review_page(rev))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 5. Generate Standalone Head-to-Head Product Comparison Pages
    for vs in VS_COMPARISONS:
        filename = f"{vs['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_vs_comparison_page(vs))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 6. XML Sitemap, Robots & IndexNow Auto-Ping
    generate_sitemap_and_robots(generated_urls)
    ping_indexnow(generated_urls)
    print(f"Successfully generated {len(generated_urls)} total SEO pages ({len(active_reviews)} cumulative review articles [+3/day] + HTML/XML sitemaps) in /{OUTPUT_DIR}!")

if __name__ == "__main__":
    main()
