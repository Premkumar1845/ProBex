<p align="center">
  <img src="https://img.shields.io/badge/Algorand-000000?style=for-the-badge&logo=algorand&logoColor=white" alt="Algorand" />
  <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React" />
  <img src="https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white" alt="Vite" />
  <img src="https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white" alt="Supabase" />
</p>

<h1 align="center">ProBex - Prediction Markets on Algorand</h1>

<p align="center">
  <strong>Trustless parimutuel prediction markets built entirely on Algorand.</strong><br/>
  Bet on real-world outcomes. Get paid in ALGO. No intermediaries.
</p>

<p align="center">
  <a href="https://probex-nine.vercel.app"><img src="https://img.shields.io/badge/Live%20Demo-probex--nine.vercel.app-00e5b0?style=for-the-badge&logo=vercel&logoColor=white" alt="Live Demo" /></a>
</p>

<p align="center">
  <a href="#features">Features</a> &bull;
  <a href="#architecture">Architecture</a> &bull;
  <a href="#tech-stack">Tech Stack</a> &bull;
  <a href="#project-structure">Project Structure</a> &bull;
  <a href="#getting-started">Getting Started</a> &bull;
  <a href="#smart-contract">Smart Contract</a> &bull;
  <a href="#frontend">Frontend</a> &bull;
  <a href="#deployment">Deployment</a> &bull;
  <a href="#testing">Testing</a> &bull;
  <a href="#license">License</a>
</p>

---

## Overview

**ProBex** is a decentralized prediction market platform where users stake ALGO on binary outcomes (YES/NO) using a parimutuel betting model. The entire settlement logic lives on-chain via an Algorand smart contract — there is no backend server, no database for market logic, and no trusted third party handling funds.

Winners receive automatic payouts proportional to their stake from the combined pool. The platform supports 36 prediction questions across six categories: Crypto, Politics, War & Conflict, Business, Tech, and Sports.

> **Status**: Proof of Concept deployed on Algorand TestNet (App ID: `758007912`)

---

## Features

- **Fully On-Chain Settlement** — All bets, resolutions, and payouts are executed through Algorand smart contracts with zero off-chain dependencies.
- **Parimutuel Betting Model** — No fixed odds. The payout ratio is determined by the total pool and the winning side's share, ensuring fair and dynamic pricing.
- **Pera Wallet Integration** — Seamless mobile wallet connection via `@txnlab/use-wallet-react` with QR code scanning support.
- **Wallet-First Authentication Flow** — Users must connect their Pera Wallet before accessing sign-in or sign-up, ensuring every account is linked to a verified Algorand address.
- **Supabase Auth** — Email/password authentication with duplicate account detection and automatic wallet address linking on signup.
- **36 Prediction Markets** — Curated questions across six categories with real-time pool tracking and percentage displays.
- **Admin Oracle Resolution** — The contract deployer can resolve markets by declaring a winning outcome, triggering the payout phase.
- **Automatic Winner Payouts** — Winners call `claim_winnings()` to receive their proportional share via an inner payment transaction.
- **Dark / Light Theme** — Full theme switcher with CSS custom properties for a polished user experience.
- **Responsive Design** — Fully responsive across desktop, tablet, and mobile with adaptive grid layouts, collapsing navigation, and touch-friendly interactions.
- **Market Analytics Dashboard** — Interactive charts (Recharts) showing probability trends, volume history, sentiment analysis, and order book visualization.
- **TestNet Explorer Integration** — Direct links to Lora Explorer for verifying transactions and contract state on-chain.

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                        USER (Browser)                        │
│                                                              │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────────┐ │
│  │ Landing Page │→ │  Auth Page   │→ │     Dashboard       │ │
│  │  (Connect    │  │  (Sign In /  │  │  (Bet / Resolve /   │ │
│  │   Wallet)    │  │   Sign Up)   │  │     Claim)          │ │
│  └─────────────┘  └──────────────┘  └─────────────────────┘ │
│         │                │                     │             │
│         ▼                ▼                     ▼             │
│    Pera Wallet      Supabase Auth      algosdk Transactions  │
└──────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                    ALGORAND BLOCKCHAIN                        │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │              ProbexContract (AVM v11)                   │  │
│  │                                                        │  │
│  │  Global State:                                         │  │
│  │    total_yes_pool | total_no_pool                      │  │
│  │    market_resolved | winning_outcome                   │  │
│  │                                                        │  │
│  │  Local State (per user):                               │  │
│  │    bet_amount | bet_outcome | claimed                  │  │
│  │                                                        │  │
│  │  Methods:                                              │  │
│  │    bet(outcome, payment) → stake ALGO on YES/NO        │  │
│  │    resolve_market(outcome) → admin declares winner     │  │
│  │    claim_winnings() → winners withdraw proportional $  │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Smart Contracts | Algorand Python (Puya) | On-chain betting logic compiled to AVM bytecode |
| Compiler | PuyaPy v5.7.1 | Compiles Algorand Python to TEAL |
| Frontend Framework | React 18 + TypeScript | Single-page application |
| Build Tool | Vite 5 | Fast HMR development and optimized production builds |
| Blockchain SDK | algosdk v3 | Transaction construction, signing, and submission |
| Wallet | @txnlab/use-wallet-react v4 | Pera Wallet connection and transaction signing |
| Authentication | Supabase | Email/password auth with PostgreSQL user storage |
| Charts | Recharts v3 | Interactive market analytics and visualizations |
| Animations | Framer Motion v12 | Smooth page transitions and micro-interactions |
| Styling | Custom CSS | Dark/light themes with CSS variables and glassmorphism |
| Testing | Pytest | 10 integration tests covering the full contract lifecycle |
| Toolchain | AlgoKit CLI | Project scaffolding, compilation, deployment, and testing |

---

## Project Structure

```
ProBex/
├── README.md                          # This file
├── AGENTS.md                          # AI agent instructions for Algorand development
├── .vscode/
│   └── mcp.json                       # MCP server configuration (Kappa + VibeKit)
├── .github/
│   ├── copilot-instructions.md        # GitHub Copilot context
│   └── skills/                        # AlgoKit agent skill definitions
│
└── ProBex/                            # AlgoKit workspace root
    ├── .algokit.toml                  # Workspace configuration
    ├── ProBex.code-workspace          # VS Code multi-root workspace
    │
    └── projects/
        ├── ProBex-contracts/          # Smart contract project (Python)
        │   ├── pyproject.toml         # Python dependencies (Poetry)
        │   ├── poetry.lock            # Locked dependency versions
        │   ├── smart_contracts/
        │   │   ├── __main__.py        # Build & deploy orchestrator
        │   │   └── probex_contract/
        │   │       ├── contract.py    # THE SMART CONTRACT (95 lines)
        │   │       └── deploy_config.py
        │   ├── smart_contracts/artifacts/probex_contract/
        │   │   ├── ProbexContract.approval.teal
        │   │   ├── ProbexContract.clear.teal
        │   │   ├── ProbexContract.arc56.json
        │   │   └── probex_contract_client.py
        │   └── tests/
        │       ├── conftest.py        # Pytest fixtures
        │       └── test_probex_contract.py  # 10 integration tests
        │
        └── ProBex-frontend/           # React frontend project
            ├── package.json           # Node.js dependencies
            ├── vite.config.ts         # Vite build configuration
            ├── index.html             # Entry HTML
            ├── src/
            │   ├── main.tsx           # App entry point
            │   ├── App.tsx            # Router + WalletProvider setup
            │   ├── Home.tsx           # Main betting interface (36 markets)
            │   ├── pages/
            │   │   ├── LandingPage.tsx    # Animated hero + wallet connect
            │   │   ├── AuthPage.tsx       # Login/Signup with Supabase
            │   │   └── DashboardPage.tsx  # Protected dashboard with tabs
            │   ├── components/
            │   │   ├── ConnectWallet.tsx   # Pera Wallet connection modal
            │   │   ├── MarketAnalytics.tsx # Charts and market data
            │   │   ├── NavButtons.tsx      # Navigation buttons
            │   │   └── ErrorBoundary.tsx   # React error boundary
            │   ├── contracts/
            │   │   └── ProbexContract.ts   # Auto-generated typed client
            │   ├── hooks/
            │   │   └── useAuth.ts         # Supabase auth session hook
            │   ├── utils/
            │   │   ├── probexClient.ts    # Algorand client utilities
            │   │   ├── supabase.ts        # Supabase client initialization
            │   │   └── network/
            │   │       └── getAlgoClientConfigs.ts
            │   └── styles/
            │       └── App.css            # Full responsive stylesheet
            └── public/
                └── robots.txt
```

---

## Getting Started

### Prerequisites

- [Node.js](https://nodejs.org/) >= 20.0
- [Python](https://python.org/) >= 3.12
- [AlgoKit CLI](https://github.com/algorandfoundation/algokit-cli)
- [Poetry](https://python-poetry.org/) (Python package manager)
- [Pera Wallet](https://perawallet.app/) mobile app (for TestNet transactions)

### 1. Clone the Repository

```bash
git clone https://github.com/Premkumar1845/ProBex.git
cd ProBex
```

### 2. Smart Contract Setup

```bash
cd ProBex/projects/ProBex-contracts

# Install Python dependencies
poetry install

# Start local Algorand network (optional, for local testing)
algokit localnet start

# Build the smart contract
algokit project run build

# Run tests
algokit project run test
```

### 3. Frontend Setup

```bash
cd ProBex/projects/ProBex-frontend

# Install Node.js dependencies
npm install

# Configure environment variables
cp .env.template .env
# Edit .env with your Algorand node and Supabase credentials

# Start development server
npm run dev
```

The application will be available at `http://localhost:5173/`.

### 4. Environment Variables

Create a `.env` file in the frontend project with the following:

```env
VITE_ALGOD_SERVER=https://testnet-api.algonode.cloud
VITE_ALGOD_PORT=
VITE_ALGOD_TOKEN=
VITE_ALGOD_NETWORK=testnet
VITE_INDEXER_SERVER=https://testnet-idx.algonode.cloud
VITE_INDEXER_PORT=
VITE_INDEXER_TOKEN=
VITE_APP_ID=758007912
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

---

## Smart Contract

The core of ProBex is a single Algorand Python smart contract implementing a **parimutuel betting pool**.

### How It Works

1. **Betting Phase** — Users call `bet("yes", payment)` or `bet("no", payment)` to stake ALGO. Each user can only bet once per market. The payment is sent to the contract's escrow address.

2. **Resolution Phase** — The contract creator (admin oracle) calls `resolve_market("yes")` or `resolve_market("no")` to declare the winning outcome.

3. **Claim Phase** — Winners call `claim_winnings()` to receive their proportional payout. The formula is:

```
payout = (user_bet_amount * total_pool) / winning_pool
```

For example, if the total pool is 10 ALGO, you bet 2 ALGO on YES, and YES wins with a 5 ALGO pool, your payout is `(2 * 10) / 5 = 4 ALGO`.

### Contract Methods

| Method | Access | Description |
|--------|--------|-------------|
| `bet(outcome, payment)` | Anyone | Stake ALGO on YES or NO. Requires opt-in. |
| `resolve_market(outcome)` | Creator only | Declare the winning outcome. Irreversible. |
| `claim_winnings()` | Winners only | Withdraw proportional payout from the pool. |

### Security Properties

- One bet per user per market (enforced on-chain)
- Only the contract creator can resolve the market
- Double-claim prevention via local state flag
- Payment verification ensures funds go to the contract escrow
- Payout uses inner transactions with fee pooling

---

## Frontend

### User Flow

```
Connect Pera Wallet → Sign In / Sign Up → Dashboard → Place Bets → Claim Winnings
```

1. **Landing Page** — Users must first connect their Pera Wallet. Only after a successful wallet connection do the authentication options appear.

2. **Auth Page** — Email/password login or signup via Supabase. The wallet address is automatically linked to the user's profile. Duplicate accounts are detected and the user is redirected to login.

3. **Dashboard** — Protected route requiring both wallet connection and authentication. Contains two tabs:
   - **Live Contract** — The main betting interface with 36 prediction markets, pool visualizations, and transaction submission.
   - **All Markets + Analytics** — Market listing with category filtering, probability charts, volume history, sentiment indicators, and order book visualization.

### Key Design Decisions

- **Wallet-first flow**: Ensures every user interaction is tied to a verified Algorand address before any authentication occurs.
- **No backend**: All market data is fetched directly from the Algorand blockchain via `algosdk`. User authentication is handled by Supabase.
- **Atomic transaction groups**: Bets are submitted as 3-transaction atomic groups (fee payment + bet payment + app call with opt-in).
- **Responsive design**: Fully adaptive layouts using CSS media queries at 768px and 400px breakpoints.

---

## Testing

The smart contract includes 10 comprehensive integration tests:

| Test | Description |
|------|-------------|
| `test_basic_parimutuel_yes_wins` | 2 ALGO YES + 1 ALGO NO, YES wins, payout = 3 ALGO |
| `test_no_side_wins` | 1 ALGO YES + 2 ALGO NO, NO wins, payout = 3 ALGO |
| `test_proportional_split_multiple_winners` | 3 winners with proportional payouts |
| `test_loser_cannot_claim` | Loser's claim attempt is rejected |
| `test_double_claim_rejected` | Double-claim prevention works |
| `test_no_bet_after_resolve` | Betting after resolution is blocked |
| `test_only_creator_can_resolve` | Non-creator resolution attempt is rejected |
| `test_double_bet_rejected` | Same user cannot bet twice |
| `test_invalid_outcome_rejected` | Invalid outcome string is rejected |
| `test_claim_before_resolve_rejected` | Pre-resolution claim attempt is rejected |

Run all tests:

```bash
cd ProBex/projects/ProBex-contracts
poetry run pytest -v
```

---

## Deployment

### TestNet Deployment

The contract is currently deployed on Algorand TestNet:

- **App ID**: `758007912`
- **Explorer**: [View on Lora](https://lora.algokit.io/testnet/application/758007912)

### Frontend Deployment

The frontend is live on Vercel:

- **Live URL**: [https://probex-nine.vercel.app](https://probex-nine.vercel.app)

### Deploy Your Own Instance

```bash
cd ProBex/projects/ProBex-contracts

# Set up deployer account
export DEPLOYER_MNEMONIC="your 25-word mnemonic"

# Deploy to TestNet
algokit project deploy testnet
```

---

## Development Commands

| Command | Description |
|---------|-------------|
| `algokit localnet start` | Start local Algorand network |
| `algokit localnet stop` | Stop local network |
| `algokit localnet reset` | Reset local network state |
| `algokit project run build` | Compile contracts and generate typed clients |
| `algokit project run test` | Run all integration tests |
| `npm run dev` | Start frontend development server |
| `npm run build` | Production build of frontend |

---

## Built With

This project was to demonstrate the feasibility of trustless prediction markets on Algorand. It leverages the [AlgoKit](https://developer.algorand.org/algokit/) fullstack development toolkit and the [Puya compiler](https://github.com/algorandfoundation/puya) for writing smart contracts in Python.

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">
  <strong>ProBex</strong> — Trade the Future. Price Reality.<br/>
  Built on <a href="https://algorand.com">Algorand</a>
</p>
