# 🎨 Zomato AI Recommender - Next.js Frontend

## ✨ What You Get

A beautiful, modern Next.js frontend that matches the Zomato screenshot design with:

✅ **Modern Stack**: Next.js 14 + TypeScript + Tailwind CSS  
✅ **Beautiful UI**: Gradient hero, clean forms, animated cards  
✅ **Fully Integrated**: Connects to your FastAPI backend  
✅ **AI-Powered**: Displays real AI-generated recommendations  
✅ **Responsive**: Works perfectly on mobile, tablet, desktop  
✅ **Production Ready**: Optimized build, SEO-friendly  

---

## 🚀 Super Quick Start (3 Steps)

### 1️⃣ Create Next.js App
```bash
cd "c:\Users\RYZEN\Downloads\zomato pro"
start-nextjs.bat
```

### 2️⃣ Copy Component Files

Open these files and copy the code into your frontend:

**📋 From `NEXTJS_COMPLETE_SETUP.md`:**
- `app/layout.tsx`
- `app/page.tsx`  
- `app/globals.css`
- `lib/api.ts`
- `types/index.ts`
- `next.config.js`
- `tailwind.config.ts`
- `.env.local`

**📋 From `NEXTJS_COMPONENTS_PART2.md`:**
- `components/Header.tsx`
- `components/Hero.tsx`
- `components/SearchForm.tsx`
- `components/ResultsSection.tsx`
- `components/RestaurantCard.tsx`

### 3️⃣ Start Development
```bash
cd frontend
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) 🎉

---

## 📖 Full Documentation

### All Component Code
1. **NEXTJS_COMPLETE_SETUP.md** - Setup, config, core pages
2. **NEXTJS_COMPONENTS_PART2.md** - All React components
3. **NEXTJS_README.md** - Detailed documentation

### Quick Reference
- **Backend API**: http://localhost:8000
- **Frontend Dev**: http://localhost:3000
- **Backend Docs**: http://localhost:8000/docs

---

## 🎯 What It Looks Like

### Home Page
- 🎨 Beautiful hero with gradient + background image
- 📝 Clean search form (location, budget, cuisine, rating)
- 🔍 "Get AI Recommendations" button

### Results Page  
- 🏆 Ranked restaurant cards (1, 2, 3...)
- ⭐ Ratings and costs displayed
- 🤖 AI-generated explanations for each
- 📊 Summary paragraph
- ⬅️ Back to search button

---

## 🛠️ Technology Stack

| What | Technology |
|------|------------|
| Framework | Next.js 14 (App Router) |
| Language | TypeScript |
| Styling | Tailwind CSS |
| HTTP Client | Axios |
| Backend | FastAPI (port 8000) |
| Font | Inter (Google Fonts) |

---

## 📦 File Structure

```
frontend/
├── app/
│   ├── layout.tsx         # Root layout with metadata
│   ├── page.tsx           # Home page component
│   └── globals.css        # Global Tailwind styles
├── components/
│   ├── Header.tsx         # Top navigation
│   ├── Hero.tsx           # Hero section
│   ├── SearchForm.tsx     # Main search form
│   ├── ResultsSection.tsx # Results container
│   └── RestaurantCard.tsx # Individual result card
├── lib/
│   └── api.ts             # API client (axios)
├── types/
│   └── index.ts           # TypeScript interfaces
├── public/
│   └── images/            # Static assets
├── .env.local             # Environment variables
├── next.config.js         # Next.js configuration
├── tailwind.config.ts     # Tailwind customization
├── tsconfig.json          # TypeScript config
└── package.json           # Dependencies
```

---

## 🎨 Customization

### Change Colors
Edit `tailwind.config.ts`:
```typescript
colors: {
  zomato: {
    red: "#E23744",        // Your brand color
    "red-hover": "#CF2533",
  },
}
```

### Change Hero Background
Replace the image URL in `components/Hero.tsx`:
```typescript
backgroundImage: "url('your-image-url')"
```

### Add Your Logo
Edit `components/Header.tsx`:
```typescript
<img src="/logo.png" alt="Logo" className="h-8" />
```

---

## 🐛 Troubleshooting

### "Failed to load form options"
- **Fix**: Make sure FastAPI backend is running
- **Check**: http://localhost:8000/health

### CORS Errors
- **Fix**: Backend needs CORS enabled for `http://localhost:3000`
- **File**: `src/phase0/api/main.py`
```python
allow_origins=["http://localhost:3000"]
```

### Components Not Found
- **Fix**: Make sure `tsconfig.json` has path alias
```json
"paths": {
  "@/*": ["./*"]
}
```

### Build Errors
```bash
# Clear cache
rm -rf .next

# Reinstall
rm -rf node_modules
npm install

# Build
npm run build
```

---

## 📈 Next Steps

### Enhancements
- [ ] Add restaurant images
- [ ] Implement user authentication
- [ ] Save favorite restaurants
- [ ] Add map view
- [ ] Filter and sort results
- [ ] Share recommendations

### Performance
- [ ] Add React Query for caching
- [ ] Implement pagination
- [ ] Optimize images with Next/Image
- [ ] Add loading skeletons

### Features
- [ ] Search history
- [ ] Restaurant details modal
- [ ] Reviews and ratings
- [ ] Booking integration

---

## 🚢 Deployment

### Vercel (1-Click)
```bash
npm i -g vercel
vercel
```

### Docker
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY . .
RUN npm ci && npm run build
CMD ["npm", "start"]
```

### Environment Variables
Set in Vercel/production:
```
NEXT_PUBLIC_API_URL=https://your-api-domain.com
```

---

## 💡 Tips

1. **Development**: Use `npm run dev` for hot reload
2. **Production**: Always run `npm run build` first
3. **Testing**: Test with real API data before deploying
4. **Images**: Use Next/Image for optimization
5. **SEO**: Update metadata in `app/layout.tsx`

---

## 🎓 Learning Resources

- [Next.js Docs](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [TypeScript](https://www.typescriptlang.org/docs)
- [Axios](https://axios-http.com/docs/intro)

---

## 📞 Support

Having issues? Check:
1. **Setup Docs**: NEXTJS_COMPLETE_SETUP.md
2. **Components**: NEXTJS_COMPONENTS_PART2.md
3. **Troubleshooting**: This file
4. **Backend**: README.md (main project)

---

**🎉 Happy Coding! Build something amazing!**

