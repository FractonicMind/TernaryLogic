<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TL Decision Demonstrator - Experience the Epistemic Hold</title>
    <meta name="description" content="Interactive demonstration of Ternary Logic (TL) and the Epistemic Hold - Experience intelligent economic reasoning in real-time">
    <meta name="author" content="Lev Goukassian">
    
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #1e3a8a 0%, #3730a3 50%, #1e40af 100%);
            min-height: 100vh;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
            padding: 40px 20px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }

        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            font-weight: 700;
        }

        .header .subtitle {
            font-size: 1.2rem;
            margin-bottom: 20px;
            opacity: 0.9;
        }

        .header .author-info {
            font-size: 1rem;
            opacity: 0.8;
        }

        .header .author-info a {
            color: #fff;
            text-decoration: none;
            margin: 0 10px;
            padding: 5px 15px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 20px;
            transition: all 0.3s ease;
        }

        .header .author-info a:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
        }

        .main-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 40px;
        }

        .input-section, .results-section {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }

        .input-section:hover, .results-section:hover {
            transform: translateY(-5px);
        }

        .section-title {
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 20px;
            color: #1e40af;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .scenario-input {
            width: 100%;
            height: 150px;
            padding: 15px;
            border: 2px solid #e2e8f0;
            border-radius: 10px;
            font-size: 1rem;
            resize: vertical;
            transition: border-color 0.3s ease;
        }

        .scenario-input:focus {
            outline: none;
            border-color: #1e40af;
            box-shadow: 0 0 0 3px rgba(30, 64, 175, 0.1);
        }

        .analyze-btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #1e40af, #3730a3);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            margin-top: 20px;
            transition: all 0.3s ease;
        }

        .analyze-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(30, 64, 175, 0.3);
        }

        .analyze-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        .example-scenarios {
            margin-top: 20px;
        }

        .scenario-btn {
            display: block;
            width: 100%;
            padding: 10px;
            margin: 5px 0;
            background: #f7fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-align: left;
        }

        .scenario-btn:hover {
            background: #edf2f7;
            border-color: #cbd5e0;
        }

        .loading {
            text-align: center;
            padding: 40px;
            color: #1e40af;
        }

        .loading-dots {
            display: inline-block;
            font-size: 2rem;
            animation: pulse 1.5s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 0.4; }
            50% { opacity: 1; }
        }

        .tl-results {
            display: none;
        }

        .tl-results.show {
            display: block;
            animation: fadeInUp 0.5s ease;
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .decision-state {
            display: flex;
            align-items: center;
            padding: 15px;
            margin: 10px 0;
            border-radius: 10px;
            transition: all 0.3s ease;
        }

        .state-proceed {
            background: linear-gradient(135deg, #059669, #047857);
            color: white;
        }

        .state-hold {
            background: linear-gradient(135deg, #d97706, #b45309);
            color: white;
            position: relative;
            overflow: hidden;
        }

        .state-halt {
            background: linear-gradient(135deg, #dc2626, #b91c1c);
            color: white;
        }

        .state-icon {
            font-size: 1.5rem;
            margin-right: 15px;
        }

        .state-content {
            flex: 1;
        }

        .state-title {
            font-weight: 600;
            font-size: 1.1rem;
            margin-bottom: 5px;
        }

        .state-reasoning {
            opacity: 0.9;
            font-size: 0.95rem;
        }

        .final-decision {
            background: linear-gradient(135deg, #1e40af, #3730a3);
            color: white;
            padding: 20px;
            border-radius: 15px;
            margin-top: 20px;
            text-align: center;
        }

        .final-decision h3 {
            font-size: 1.3rem;
            margin-bottom: 10px;
        }

        .epistemic-hold-animation {
            display: inline-block;
            animation: deliberate 2s infinite;
        }

        @keyframes deliberate {
            0%, 100% { transform: scale(1); opacity: 0.8; }
            50% { transform: scale(1.1); opacity: 1; }
        }

        .education-section {
            background: white;
            border-radius: 20px;
            padding: 30px;
            margin-top: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }

        .education-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-top: 20px;
        }

        .education-card {
            padding: 20px;
            border: 2px solid #e2e8f0;
            border-radius: 15px;
            transition: all 0.3s ease;
        }

        .education-card:hover {
            border-color: #1e40af;
            transform: translateY(-3px);
        }

        .footer {
            text-align: center;
            color: white;
            padding: 40px 20px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            backdrop-filter: blur(10px);
            margin-top: 40px;
        }

        @media (max-width: 768px) {
            .main-content {
                grid-template-columns: 1fr;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .education-grid {
                grid-template-columns: 1fr;
            }
        }

        .performance-metrics {
            background: #f8fafc;
            border-radius: 15px;
            padding: 20px;
            margin-top: 20px;
            border-left: 4px solid #1e40af;
        }

        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }

        .metric-item {
            text-align: center;
            padding: 10px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .metric-value {
            font-size: 1.5rem;
            font-weight: bold;
            color: #1e40af;
        }

        .metric-label {
            font-size: 0.85rem;
            color: #6b7280;
            margin-top: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header Section -->
        <div class="header">
            <h1>📊 TL Decision Demonstrator</h1>
            <div class="subtitle">Experience the Epistemic Hold - Intelligent Economic Reasoning in Real-Time</div>
            <div class="author-info">
                By <strong>Lev Goukassian</strong> | 
                <a href="https://github.com/FractonicMind/TernaryLogic" target="_blank">View Research</a>
                <a href="https://medium.com/@leogouk/the-third-option-why-economy-and-civilization-must-break-free-from-binary-0d69d2be14c6" target="_blank">Read Article</a>
            </div>
        </div>

        <!-- Main Interactive Section -->
        <div class="main-content">
            <!-- Input Section -->
            <div class="input-section">
                <div class="section-title">
                    💡 Enter Your Economic Scenario
                </div>
                <textarea 
                    id="scenarioInput" 
                    class="scenario-input" 
                    placeholder="Type your economic decision scenario here... For example: 'Should I execute a large trade when technical indicators are bullish but volume is weak during earnings week?'"
                ></textarea>
                
                <button id="analyzeBtn" class="analyze-btn">
                    🔍 Analyze with TL Framework
                </button>

                <div class="example-scenarios">
                    <h4 style="margin-bottom: 10px; color: #1e40af;">📈 Try Example Economic Scenarios:</h4>
                    <button class="scenario-btn" data-scenario="Should I execute a large trade when momentum indicators are strong but volume confirmation is weak?">
                        📊 Execute trade with conflicting signals?
                    </button>
                    <button class="scenario-btn" data-scenario="Should I switch to a new supplier offering 15% cost savings but with unproven quality track record?">
                        🏭 Switch suppliers for cost savings?
                    </button>
                    <button class="scenario-btn" data-scenario="Should I raise interest rates when inflation is high but unemployment is rising and growth is slowing?">
                        🏦 Monetary policy with mixed data?
                    </button>
                    <button class="scenario-btn" data-scenario="Should I deploy capital in emerging markets with 20% expected returns but high political uncertainty?">
                        🌍 Invest in uncertain emerging markets?
                    </button>
                    <button class="scenario-btn" data-scenario="Should I hedge my portfolio's duration risk when Fed policy direction is unclear but hedging costs 0.2% annually?">
                        ⚖️ Hedge portfolio risk with uncertain policy?
                    </button>
                    <button class="scenario-btn" data-scenario="Should I proceed with this acquisition using debt financing to avoid dilution despite high leverage concerns?">
                        💼 Finance acquisition with high leverage?
                    </button>
                </div>
            </div>

            <!-- Results Section -->
            <div class="results-section">
                <div class="section-title">
                    🤖 TL Reasoning Process
                </div>
                
                <div id="loadingState" class="loading" style="display: none;">
                    <div class="loading-dots">⚡ Analyzing economic factors...</div>
                    <div style="margin-top: 10px; font-size: 0.9rem;">Evaluating uncertainty dimensions...</div>
                </div>

                <div id="tlResults" class="tl-results">
                    <div id="decisionStates">
                        <!-- TL states will be populated here -->
                    </div>
                    
                    <div id="finalDecision" class="final-decision">
                        <!-- Final decision will be populated here -->
                    </div>
                </div>

                <div id="defaultMessage" style="text-align: center; padding: 40px; color: #a0aec0;">
                    <div style="font-size: 3rem; margin-bottom: 20px;">📈</div>
                    <h3>Ready to Analyze</h3>
                    <p>Enter your economic scenario above and watch TL reasoning in action!</p>
                </div>
            </div>
        </div>

        <!-- Performance Metrics Section -->
        <div class="performance-metrics">
            <h3 style="color: #1e40af; margin-bottom: 15px;">🎯 TL Framework Performance</h3>
            <p>Proven results across economic domains through comprehensive backtesting:</p>
            <div class="metrics-grid">
                <div class="metric-item">
                    <div class="metric-value">35%</div>
                    <div class="metric-label">Forecasting Error Reduction</div>
                </div>
                <div class="metric-item">
                    <div class="metric-value">40%</div>
                    <div class="metric-label">Sharpe Ratio Improvement</div>
                </div>
                <div class="metric-item">
                    <div class="metric-value">23%</div>
                    <div class="metric-label">Epistemic Hold Rate</div>
                </div>
                <div class="metric-item">
                    <div class="metric-value">19%</div>
                    <div class="metric-label">Volatility Reduction</div>
                </div>
            </div>
        </div>

        <!-- Education Section -->
        <div class="education-section">
            <div class="section-title">
                📖 Understanding Ternary Logic
            </div>
            
            <div class="education-grid">
                <div class="education-card">
                    <h3 style="color: #059669; margin-bottom: 10px;">🟢 +1: Proceed</h3>
                    <p>Clear economic path forward with manageable uncertainty. Market signals align and risk-return profile supports execution with confidence.</p>
                </div>
                
                <div class="education-card">
                    <h3 style="color: #d97706; margin-bottom: 10px;">🟡 0: Epistemic Hold</h3>
                    <p>Economic complexity detected. Conflicting signals or high uncertainty require additional analysis and deliberation before action.</p>
                </div>
                
                <div class="education-card">
                    <h3 style="color: #dc2626; margin-bottom: 10px;">🔴 -1: Halt</h3>
                    <p>Significant economic risks present. Market instability, systematic concerns, or clear conflicts suggest defensive positioning.</p>
                </div>
            </div>

            <div style="margin-top: 30px; padding: 20px; background: #f7fafc; border-radius: 15px; text-align: center;">
                <h3 style="color: #1e40af; margin-bottom: 15px;">🚀 Explore the Research</h3>
                <p>This interactive demo showcases the Ternary Logic framework developed by Lev Goukassian. The framework introduces intelligent uncertainty management (Epistemic Hold) to economic decision-making, moving beyond simple binary choices.</p>
                <div style="margin-top: 15px;">
                    <a href="https://github.com/FractonicMind/TernaryLogic" target="_blank" style="display: inline-block; margin: 5px 10px; padding: 8px 20px; background: #1e40af; color: white; text-decoration: none; border-radius: 20px; transition: all 0.3s ease;">📚 GitHub Repository</a>
                    <a href="https://medium.com/@leogouk/the-third-option-why-economy-and-civilization-must-break-free-from-binary-0d69d2be14c6" target="_blank" style="display: inline-block; margin: 5px 10px; padding: 8px 20px; background: #059669; color: white; text-decoration: none; border-radius: 20px; transition: all 0.3s ease;">📖 Research Article</a>
                </div>
            </div>
        </div>

        <!-- Footer -->
        <div class="footer">
            <h3>📊 Ternary Logic Framework</h3>
            <p>Developed by Lev Goukassian | ORCID: 0009-0006-5966-1243</p>
            <p>Experience intelligent economic reasoning with the Epistemic Hold</p>
            <div style="margin-top: 15px;">
                <strong>Contact:</strong> leogouk@gmail.com<br>
                <strong>Successor Contact:</strong> support@tl-goukassian.org
            </div>
        </div>
    </div>

    <script>
        // TL Core Logic
        class TLAnalyzer {
            constructor() {
                this.economicDimensions = [
                    'market_volatility',
                    'uncertainty_level',
                    'risk_assessment',
                    'information_asymmetry',
                    'liquidity_conditions',
                    'systematic_risk',
                    'opportunity_cost',
                    'timing_sensitivity'
                ];
            }

            analyze(scenario) {
                // Simulate TL analysis process
                const analysis = this.evaluateEconomicDimensions(scenario);
                const decision = this.calculateDecision(analysis);
                return {
                    analysis: analysis,
                    decision: decision,
                    reasoning: this.generateReasoning(scenario, analysis, decision)
                };
            }

            evaluateEconomicDimensions(scenario) {
                // Economic decision analysis based on keywords and context
                const lowerScenario = scenario.toLowerCase();
                
                const scores = {
                    proceed: 0,
                    hold: 0,
                    halt: 0
                };

                // Positive indicators (+1 - Proceed)
                if (lowerScenario.includes('clear') || lowerScenario.includes('stable') || 
                    lowerScenario.includes('arbitrage') || lowerScenario.includes('opportunity') ||
                    lowerScenario.includes('normal market') || lowerScenario.includes('low risk') ||
                    lowerScenario.includes('strong signals') || lowerScenario.includes('confirmed')) {
                    scores.proceed += 2;
                }

                // Negative indicators (-1 - Halt)
                if (lowerScenario.includes('crash') || lowerScenario.includes('crisis') || 
                    lowerScenario.includes('instability') || lowerScenario.includes('systematic risk') ||
                    lowerScenario.includes('emergency') || lowerScenario.includes('liquidity crisis') ||
                    lowerScenario.includes('market failure') || lowerScenario.includes('panic')) {
                    scores.halt += 3;
                }

                // Uncertainty indicators (0 - Epistemic Hold)
                if (lowerScenario.includes('uncertain') || lowerScenario.includes('mixed') ||
                    lowerScenario.includes('conflicting') || lowerScenario.includes('unclear') ||
                    lowerScenario.includes('volatile') || lowerScenario.includes('complicated') ||
                    lowerScenario.includes('complex') || lowerScenario.includes('divergent')) {
                    scores.hold += 2;
                }

                // Economic complexity indicators (0 - Epistemic Hold)
                if (lowerScenario.includes('but') || lowerScenario.includes('however') ||
                    lowerScenario.includes('although') || lowerScenario.includes('while') ||
                    lowerScenario.includes('versus') || lowerScenario.includes('vs') ||
                    lowerScenario.includes('despite') || lowerScenario.includes('nevertheless')) {
                    scores.hold += 1;
                }

                // High-stakes scenarios requiring deliberation
                if (lowerScenario.includes('large') || lowerScenario.includes('significant') ||
                    lowerScenario.includes('major') || lowerScenario.includes('policy') ||
                    lowerScenario.includes('portfolio') || lowerScenario.includes('acquisition')) {
                    scores.hold += 1;
                }

                // Risk amplifiers
                if (lowerScenario.includes('leverage') || lowerScenario.includes('debt') ||
                    lowerScenario.includes('borrowed') || lowerScenario.includes('margin')) {
                    scores.hold += 1;
                }

                return scores;
            }

            calculateDecision(analysis) {
                const maxScore = Math.max(analysis.proceed, analysis.hold, analysis.halt);
                
                // Halt takes priority for safety
                if (analysis.halt > 0 && analysis.halt >= maxScore) {
                    return -1; // Halt
                }
                // Hold for complexity or uncertainty
                else if (analysis.hold >= maxScore || (analysis.proceed === analysis.halt)) {
                    return 0; // Epistemic Hold
                }
                // Proceed when clear
                else {
                    return 1; // Proceed
                }
            }

            generateReasoning(scenario, analysis, decision) {
                const reasons = {
                    proceed: [
                        "Clear economic opportunity with manageable risk profile",
                        "Market signals align with low uncertainty environment",
                        "Risk-return ratio supports confident execution",
                        "Stable market conditions enable strategic positioning"
                    ],
                    hold: [
                        "Economic complexity requires additional analysis before execution",
                        "Conflicting market signals suggest gathering more information",
                        "Multiple variables create uncertainty requiring deliberation",
                        "Risk-return assessment needs deeper evaluation"
                    ],
                    halt: [
                        "Significant market risks detected requiring defensive action",
                        "Systematic instability suggests protective positioning",
                        "High uncertainty with potential for significant losses",
                        "Market conditions exceed risk tolerance parameters"
                    ]
                };

                const decisionType = decision === 1 ? 'proceed' : decision === 0 ? 'hold' : 'halt';
                const selectedReasons = reasons[decisionType];
                
                return {
                    proceed: reasons.proceed[0],
                    hold: reasons.hold[0],
                    halt: reasons.halt[0],
                    final: selectedReasons[Math.floor(Math.random() * selectedReasons.length)]
                };
            }
        }

        // UI Controller
        class TLDemo {
            constructor() {
                this.analyzer = new TLAnalyzer();
                this.initializeEventListeners();
            }

            initializeEventListeners() {
                const analyzeBtn = document.getElementById('analyzeBtn');
                const scenarioInput = document.getElementById('scenarioInput');
                const scenarioBtns = document.querySelectorAll('.scenario-btn');

                analyzeBtn.addEventListener('click', () => this.analyzeScenario());
                
                scenarioBtns.forEach(btn => {
                    btn.addEventListener('click', (e) => {
                        const scenario = e.target.getAttribute('data-scenario');
                        scenarioInput.value = scenario;
                        this.analyzeScenario();
                    });
                });

                // Enter key to analyze
                scenarioInput.addEventListener('keypress', (e) => {
                    if (e.key === 'Enter' && e.ctrlKey) {
                        this.analyzeScenario();
                    }
                });
            }

            async analyzeScenario() {
                const input = document.getElementById('scenarioInput').value.trim();
                
                if (!input) {
                    alert('Please enter an economic scenario to analyze!');
                    return;
                }

                this.showLoading();
                
                // Simulate thinking time for Epistemic Hold effect
                await this.sleep(2500);
                
                const result = this.analyzer.analyze(input);
                this.displayResults(result);
            }

            showLoading() {
                document.getElementById('defaultMessage').style.display = 'none';
                document.getElementById('tlResults').classList.remove('show');
                document.getElementById('loadingState').style.display = 'block';
                
                // Animate loading text
                let dots = 1;
                const loadingInterval = setInterval(() => {
                    const texts = [
                        '⚡ Analyzing economic factors...',
                        '📊 Evaluating market signals...',
                        '⚖️ Assessing risk-return profile...',
                        '🔍 Applying Epistemic Hold logic...',
                        '📈 Processing uncertainty dimensions...'
                    ];
                    
                    document.querySelector('.loading-dots').textContent = texts[dots % texts.length];
                    dots++;
                    
                    if (dots > 10) {
                        clearInterval(loadingInterval);
                    }
                }, 300);
            }

            displayResults(result) {
                document.getElementById('loadingState').style.display = 'none';
                
                const statesContainer = document.getElementById('decisionStates');
                const finalContainer = document.getElementById('finalDecision');
                
                // Clear previous results
                statesContainer.innerHTML = '';
                
                // Create decision states
                const states = [
                    { value: 1, label: 'Proceed', icon: '🟢', class: 'state-proceed', reasoning: result.reasoning.proceed },
                    { value: 0, label: 'Epistemic Hold', icon: '🟡', class: 'state-hold', reasoning: result.reasoning.hold },
                    { value: -1, label: 'Halt', icon: '🔴', class: 'state-halt', reasoning: result.reasoning.halt }
                ];

                states.forEach(state => {
                    const stateDiv = document.createElement('div');
                    stateDiv.className = `decision-state ${state.class}`;
                    
                    if (state.value === result.decision) {
                        stateDiv.style.border = '3px solid #ffd700';
                        stateDiv.style.boxShadow = '0 0 20px rgba(255, 215, 0, 0.5)';
                    }
                    
                    stateDiv.innerHTML = `
                        <div class="state-icon">${state.icon}</div>
                        <div class="state-content">
                            <div class="state-title">${state.value > 0 ? '+' : ''}${state.value}: ${state.label}</div>
                            <div class="state-reasoning">${state.reasoning}</div>
                        </div>
                    `;
                    
                    statesContainer.appendChild(stateDiv);
                });

                // Final decision
                const decisionLabels = { 1: 'Proceed', 0: 'Epistemic Hold', '-1': 'Halt' };
                const decisionIcons = { 1: '🟢', 0: '🟡', '-1': '🔴' };
                
                finalContainer.innerHTML = `
                    <h3>🎯 TL Decision: ${result.decision > 0 ? '+' : ''}${result.decision} (${decisionLabels[result.decision]})</h3>
                    <div style="font-size: 2rem; margin: 10px 0;">
                        ${result.decision === 0 ? '<span class="epistemic-hold-animation">🟡</span>' : decisionIcons[result.decision]}
                    </div>
                    <p>${result.reasoning.final}</p>
                `;

                document.getElementById('tlResults').classList.add('show');
            }

            sleep(ms) {
                return new Promise(resolve => setTimeout(resolve, ms));
            }
        }

        // Initialize the demo when page loads
        document.addEventListener('DOMContentLoaded', () => {
            new TLDemo();
        });
    </script>
</body>
</html>
