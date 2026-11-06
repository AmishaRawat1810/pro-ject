#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "🚀 Bootstrapping Modular Tracker MVP Frontend..."

# 1. Scaffold Vite Project (React + TypeScript)
npm create vite@latest tracker-frontend -- --template react-ts
cd tracker-frontend

# 2. Install Core MVP Dependencies
echo "📦 Installing core dependencies..."
# React Flow for the canvas, Zustand for state management, Lucide for UI icons
npm install reactflow zustand lucide-react 
# Utility libraries for handling Tailwind classes efficiently
npm install clsx tailwind-merge

# 3. Install and Configure Tailwind CSS
echo "🎨 Setting up Tailwind CSS..."
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Overwrite tailwind.config.js for React files
cat <<EOT > tailwind.config.js
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
EOT

# Overwrite index.css with Tailwind directives
cat <<EOT > src/index.css
@tailwind base;
@tailwind components;
@tailwind utilities;

html, body, #root {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
  overflow: hidden; /* Prevents scrollbars, letting React Flow handle panning */
}
EOT

# 4. Scaffold the MVP Directory Architecture
echo "📂 Creating strict MVP folder structure..."

# Delete default Vite boilerplate files
rm src/App.css src/assets/react.svg

# Create directories mapping exactly to your Plan.md
mkdir -p src/{api,components/{canvas,sidebar,templates,trackers,ui},store,types,utils}

# --- Canvas Engine (React Flow) ---
touch src/components/canvas/Workspace.tsx
touch src/components/canvas/HabitTrackerNode.tsx

# --- UI & Menus ---
touch src/components/sidebar/ToolMenu.tsx
touch src/components/templates/CanvaDrawer.tsx
touch src/components/templates/TemplateGrid.tsx

# --- Tracker Widgets ---
touch src/components/trackers/DailyWeeklyTracker.tsx
touch src/components/trackers/ThisMonthView.tsx

# --- State Management (Zustand Strict Separation) ---
touch src/store/useLayoutStore.ts   # For React Flow X/Y coordinates
touch src/store/useHabitStore.ts    # For actual habit data and checkmarks

# --- Types & Interfaces ---
touch src/types/canvas.d.ts
touch src/types/habits.d.ts
touch src/types/api.d.ts

# --- Utils & API ---
touch src/utils/debounce.ts         # For debouncing backend saves
touch src/utils/storage.ts          # For localStorage sync
touch src/api/client.ts             # Axios/Fetch setup for .NET backend

echo "✅ Frontend setup complete!"
echo "➡️  Next steps: cd tracker-frontend && npm run dev"