# Zomato AI Recommender - Next.js Frontend

This is a modern Next.js frontend that matches the design from the screenshot and connects to the existing FastAPI backend.

## 🚀 Quick Setup

### Option 1: Automated Setup (Recommended)
```bash
# Run the setup script
setup-nextjs.bat

# Wait for installation to complete
cd frontend

# Copy all component files from the nextjs-components folder
# (Files will be created in the next step)

# Start development server
npm run dev
```

### Option 2: Manual Setup
```bash
# Create Next.js app
npx create-next-app@latest frontend --typescript --tailwind --app --no-src-dir --import-alias "@/*"

cd frontend

# Install dependencies
npm install axios

# Create folder structure
mkdir components lib types public/images

# Copy all files from nextjs-components folder
# Start development server
npm run dev
```

## 📁 Project Structure

```
frontend/
├── app/
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Home page
│   └── globals.css         # Global styles
├── components/
│   ├── Header.tsx          # Navigation header
│   ├── Hero.tsx            # Hero section
│   ├── SearchForm.tsx      # Search form
│   ├── ResultsSection.tsx  # Results display
│   └── RestaurantCard.tsx  # Individual result card
├── lib/
│   └── api.ts              # API client
├── types/
│   └── index.ts            # TypeScript types
├── public/
│   └── images/             # Static images
├── next.config.js          # Next.js config
├── tailwind.config.ts      # Tailwind config
├── tsconfig.json           # TypeScript config
└── package.json            # Dependencies
```

## 🎨 Features

### Design Highlights
- ✅ Matches the Zomato screenshot design
- ✅ Modern gradient hero section
- ✅ Clean, intuitive search form
- ✅ Responsive design (mobile-first)
- ✅ Smooth animations and transitions
- ✅ Loading states and error handling

### Functionality
- ✅ Connects to FastAPI backend (localhost:8000)
- ✅ Dynamic dropdowns (cities, cuisines, budgets from API)
- ✅ AI-powered restaurant recommendations
- ✅ Real-time search with loading indicators
- ✅ Beautiful result cards with ratings and costs
- ✅ TypeScript for type safety
- ✅ Tailwind CSS for styling

## 🔧 Configuration

### Backend Connection
The frontend connects to your FastAPI backend at `http://localhost:8000`.

**File: `.env.local`**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### API Proxy (Optional)
For production, you can use Next.js API routes as a proxy:

**File: `next.config.js`**
```javascript
async rewrites() {
  return [
    {
      source: '/api/:path*',
      destination: 'http://localhost:8000/:path*',
    },
  ];
}
```

## 🎯 Usage

### Development
```bash
cd frontend
npm run dev
```
Open [http://localhost:3000](http://localhost:3000)

### Production Build
```bash
npm run build
npm start
```

### Linting
```bash
npm run lint
```

## 🔗 API Integration

The frontend connects to these backend endpoints:

- `GET /meta/cities` - Get available cities
- `GET /meta/cuisines` - Get available cuisines
- `GET /meta/budgets` - Get budget options
- `POST /recommend` - Get AI recommendations

## 🎨 Customization

### Colors
Edit `tailwind.config.ts` to customize the color scheme:

```typescript
colors: {
  zomato: {
    red: "#E23744",           // Main red color
    "red-hover": "#CF2533",   // Hover state
    dark: "#1C1C1C",          // Dark text
  },
}
```

### Hero Background
Replace `public/images/hero-bg.jpg` with your own background image.

### Fonts
The app uses Inter font from Google Fonts. Change in `app/layout.tsx`:

```typescript
import { Inter, Poppins } from "next/font/google";
const poppins = Poppins({ subsets: ["latin"], weight: ["400", "600", "700"] });
```

## 📱 Responsive Design

The frontend is fully responsive with breakpoints:
- Mobile: < 640px
- Tablet: 640px - 1024px  
- Desktop: > 1024px

## 🐛 Troubleshooting

### CORS Errors
If you see CORS errors, ensure the FastAPI backend has CORS middleware enabled:

```python
# In src/phase0/api/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add Next.js URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### API Connection Failed
1. Make sure FastAPI server is running: `http://localhost:8000`
2. Check `.env.local` has correct API URL
3. Verify CORS is enabled on backend

### Build Errors
```bash
# Clear Next.js cache
rm -rf .next

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Try building again
npm run build
```

## 🚢 Deployment

### Vercel (Recommended)
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Docker
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

## 📚 Tech Stack

- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **HTTP Client:** Axios
- **Fonts:** Google Fonts (Inter)
- **Icons:** Heroicons (inline SVG)

## 🎉 Next Steps

1. **Enhance UI:**
   - Add restaurant images
   - Implement favorite/bookmark feature
   - Add user reviews section

2. **Add Features:**
   - User authentication
   - Search history
   - Map view with locations
   - Filter and sort options

3. **Performance:**
   - Add caching with React Query
   - Implement infinite scroll
   - Optimize images with Next/Image

4. **Analytics:**
   - Add Google Analytics
   - Track user interactions
   - A/B testing for recommendations

## 📄 License

Same as the main project.

---

**Made with ❤️ for better dining experiences**
