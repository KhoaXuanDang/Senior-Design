# UC Cookbook - Frontend

A modern, microservice-based web application for University of Cincinnati students to discover, share, and save delicious recipes.

## 🚀 Features

- **Browse Recipes**: Explore a grid of recipe cards with search and filter functionality
- **Recipe Details**: View complete recipe information including ingredients, steps, and metadata
- **Contribute Recipes**: Share your own recipes with the UC community (authenticated users)
- **My Cookbook**: Save your favorite recipes to a personal collection (authenticated users)
- **Authentication**: Secure login and registration with token-based auth

## 🛠️ Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui
- **Icons**: lucide-react
- **Validation**: Zod
- **Authentication**: Token-based auth with httpOnly cookies

## 📋 Prerequisites

- Node.js 18+ and npm
- Backend API running on port **8000** (the default frontend uses a Next.js **proxy** at `/api` → `http://127.0.0.1:8000`; override with `NEXT_PUBLIC_API_BASE_URL` if needed)

## 🔧 Installation

1. **Navigate to the project directory**:
   ```bash
   cd uc-cookbook-frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Configure environment variables** (optional):
   
   By default, API requests go to **`/api`** on the Next server, which rewrites to the backend. To call the backend directly, create `.env.local`:
   ```
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
   ```
   If the backend is not at `127.0.0.1:8000`, set `BACKEND_INTERNAL_URL` for the proxy (see `next.config.js`).

## 🚀 Running the Application

### Development Mode

```bash
npm run dev
```

The application will be available at [http://localhost:3000](http://localhost:3000).

### Production Build

```bash
npm run build
npm start
```

## 📁 Project Structure

```
uc-cookbook-frontend/
├── app/                          # Next.js App Router pages
│   ├── auth/                     # Authentication pages
│   │   ├── login/
│   │   └── register/
│   ├── cookbook/                 # My Cookbook page
│   ├── recipes/                  # Recipe pages
│   │   ├── [id]/                 # Recipe detail page (dynamic route)
│   │   └── contribute/           # Contribute recipe page
│   ├── layout.tsx                # Root layout with Navbar & Footer
│   ├── page.tsx                  # Homepage (browse recipes)
│   └── globals.css               # Global styles
├── components/                   # React components
│   ├── ui/                       # shadcn/ui components
│   ├── Footer.tsx
│   ├── Navbar.tsx
│   ├── RecipeCard.tsx
│   └── RecipeFilters.tsx
├── lib/                          # Utilities and helpers
│   ├── api.ts                    # API client
│   ├── auth.ts                   # Auth helpers
│   ├── types.ts                  # TypeScript type definitions
│   └── utils.ts                  # Utility functions
├── public/                       # Static assets
├── .env.local                    # Environment variables
├── components.json               # shadcn/ui configuration
├── next.config.js                # Next.js configuration
├── package.json                  # Dependencies and scripts
├── tailwind.config.ts            # Tailwind CSS configuration
└── tsconfig.json                 # TypeScript configuration
```

## 🎨 Design Philosophy

The UI is inspired by Airbnb's design principles:
- **Clean whitespace**: Generous spacing for breathing room
- **Card-based layouts**: Recipe cards with subtle shadows and borders
- **Strong typography**: Clear hierarchy with Inter font
- **Warm neutrals**: Comfortable, inviting color palette
- **Responsive grids**: Adapts seamlessly from mobile to desktop

## 🔌 API Integration

The frontend integrates with the backend API at `http://localhost:8000`. Key endpoints:

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `POST /auth/logout` - Logout user

### Recipes
- `GET /recipes` - List recipes (with optional filters)
- `GET /recipes/:id` - Get recipe details
- `POST /recipes` - Create new recipe (authenticated)

### Cookbook
- `GET /cookbook` - Get saved recipes (authenticated)
- `POST /cookbook/:recipe_id` - Save recipe to cookbook (authenticated)
- `DELETE /cookbook/:recipe_id` - Remove recipe from cookbook (authenticated)

## 🎯 Key Pages

### Homepage (`/`)
- Browse all recipes with search and filters
- Filter by tag, difficulty, or search query
- Empty state prompts users to contribute the first recipe

### Recipe Detail (`/recipes/[id]`)
- Full recipe information with hero image
- Ingredients list and step-by-step instructions
- Save to cookbook button (authenticated users)
- Recipe metadata (author, time, difficulty, tags)

### Contribute Recipe (`/recipes/contribute`)
- Multi-section form with validation
- Dynamic ingredient and step inputs
- Client-side validation with Zod
- Authenticated users only

### My Cookbook (`/cookbook`)
- Personal collection of saved recipes
- Remove recipes from collection
- Authenticated users only

### Login/Register (`/auth/login`, `/auth/register`)
- Secure authentication forms
- Form validation with Zod
- Error handling and loading states

## 🔐 Authentication Flow

1. User logs in or registers via `/auth/login` or `/auth/register`
2. Backend returns user data and sets httpOnly cookie
3. Frontend stores user data in localStorage
4. All API requests include credentials (cookies sent automatically)
5. Protected routes check authentication status and redirect if needed

## 🧪 Error Handling

- **Loading states**: Spinners and skeleton screens
- **Error states**: User-friendly error messages
- **Empty states**: Helpful prompts when no data exists
- **Form validation**: Real-time validation with clear error messages

## 📱 Responsive Design

The application is fully responsive:
- **Mobile**: Single column layout, touch-friendly buttons
- **Tablet**: Two-column recipe grid
- **Desktop**: Three-column recipe grid, sticky filters

## 🎨 Customization

### Change API URL
Edit `.env.local`:
```
NEXT_PUBLIC_API_BASE_URL=https://your-backend-url.com
```

### Modify Theme
Edit `app/globals.css` to change CSS variables:
```css
:root {
  --primary: 0 72% 51%;  /* Change primary color */
  --radius: 0.5rem;       /* Change border radius */
}
```

### Add New Components
Use shadcn/ui CLI to add more components:
```bash
npx shadcn-ui@latest add [component-name]
```

## 📝 Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint

## 🤝 Contributing

1. Ensure the backend API is running
2. Make your changes
3. Test thoroughly across different screen sizes
4. Follow the existing code style and component patterns

## 📄 License

This project is part of the UC Senior Design Capstone project.

## 🙋 Support

For issues or questions, please contact the development team.

---

Built with ❤️ for University of Cincinnati students
