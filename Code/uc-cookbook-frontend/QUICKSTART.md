# UC Cookbook Frontend - Quick Start Guide

## 📦 What's Included

A complete, production-ready Next.js 14 frontend application with:

✅ **Full Feature Set**:
- Browse recipes with search and filters
- Recipe detail pages with save functionality
- Contribute new recipes (authenticated)
- Personal cookbook for saved recipes
- Login and registration pages

✅ **Modern Tech Stack**:
- Next.js 14 (App Router) + TypeScript
- shadcn/ui + Tailwind CSS
- Zod validation
- Token-based authentication
- Airbnb-inspired design

✅ **Complete API Integration**:
- Typed API client for all backend endpoints
- Error handling and loading states
- Empty state UX

## 🚀 Get Started (3 Steps)

### 1. Install Dependencies
```bash
cd Senior-Design/Code/uc-cookbook-frontend
npm install
```

### 2. Start Development Server
```bash
npm run dev
```

### 3. Open in Browser
Navigate to [http://localhost:3000](http://localhost:3000)

## ⚙️ Configuration

By default the app calls **`/api/...`** on the Next dev server; Next **proxies** those requests to the FastAPI backend (`http://127.0.0.1:8000`). That avoids browser connection issues to port 8000. Start **both** the backend and `npm run dev`.

Optional `.env.local` overrides:

```
# Talk to the backend directly instead of the proxy (advanced)
# NEXT_PUBLIC_API_BASE_URL=http://localhost:8000

# Where Next should proxy /api when the backend is not on 127.0.0.1:8000 (e.g. Docker)
# BACKEND_INTERNAL_URL=http://127.0.0.1:8000
```

## 📁 Project Structure

```
uc-cookbook-frontend/
├── app/                    # Pages (Next.js App Router)
│   ├── page.tsx           # Homepage (browse recipes)
│   ├── recipes/
│   │   ├── [id]/          # Recipe detail
│   │   └── contribute/    # Create recipe
│   ├── cookbook/          # Saved recipes
│   └── auth/              # Login/Register
├── components/            # React components
│   ├── ui/               # shadcn/ui components
│   ├── Navbar.tsx
│   ├── Footer.tsx
│   ├── RecipeCard.tsx
│   └── RecipeFilters.tsx
├── lib/                   # Utilities
│   ├── api.ts            # API client
│   ├── auth.ts           # Auth helpers
│   └── types.ts          # TypeScript types
└── README.md             # Full documentation
```

## 🎯 Key Features

### Browse Recipes (Homepage)
- Grid of recipe cards with images
- Search by title/description
- Filter by tag and difficulty
- Responsive 1/2/3 column layout

### Recipe Details
- Full recipe with ingredients and steps
- Save to cookbook (authenticated)
- Author info and metadata

### Contribute Recipe
- Multi-section form with validation
- Dynamic ingredient/step inputs
- Image URL support
- Zod schema validation

### My Cookbook
- Personal saved recipes
- Remove from collection
- Empty state with CTA

### Authentication
- Login and registration forms
- Client-side validation
- Token-based auth with httpOnly cookies

## 🎨 Design Features

- **Airbnb-inspired**: Clean, card-based layout
- **Fully responsive**: Mobile, tablet, desktop
- **Loading states**: Spinners for async operations
- **Error handling**: User-friendly error messages
- **Empty states**: Helpful CTAs when no data

## 📡 API Endpoints Used

- `GET /health`
- `POST /auth/register`, `/auth/login`, `/auth/logout`
- `GET /recipes` (with filters), `GET /recipes/:id`, `POST /recipes`
- `GET /cookbook`, `POST /cookbook/:id`, `DELETE /cookbook/:id`

## ✅ Ready to Run

All files are created and configured. Just run:

```bash
npm install && npm run dev
```

## 📚 Need More Info?

See [README.md](README.md) for comprehensive documentation including:
- Detailed feature descriptions
- API integration details
- Customization guide
- Component documentation

---

**Note**: Ensure your backend API is running on `http://localhost:8000` before testing the app.
