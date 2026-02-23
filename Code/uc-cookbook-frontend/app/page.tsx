'use client';

import { useEffect, useState } from 'react';
import { RecipeCard } from '@/components/RecipeCard';
import { RecipeFilters } from '@/components/RecipeFilters';
import { getRecipes } from '@/lib/api';
import type { Recipe } from '@/lib/types';
import { Loader2, ChefHat } from 'lucide-react';
import { Button } from '@/components/ui/button';
import Link from 'next/link';

export default function HomePage() {
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState({
    search: '',
    tag: '',
    difficulty: '',
  });

  useEffect(() => {
    fetchRecipes();
  }, [filters]);

  const fetchRecipes = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const params: any = {};
      if (filters.search) params.search = filters.search;
      if (filters.tag && filters.tag !== 'all') params.tag = filters.tag;
      if (filters.difficulty && filters.difficulty !== 'all') params.difficulty = filters.difficulty;
      
      const data = await getRecipes(params);
      setRecipes(data.recipes || []);
    } catch (err: any) {
      setError(err.message || 'Failed to load recipes');
      console.error('Error fetching recipes:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container py-8 md:py-12">
      {/* Hero Section */}
      <div className="text-center mb-12">
        <h1 className="text-4xl md:text-5xl font-bold tracking-tight mb-4">
          Discover Delicious Recipes
        </h1>
        <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
          Explore recipes shared by UC students, save your favorites, and contribute your own culinary creations.
        </p>
      </div>

      {/* Filters */}
      <div className="mb-8">
        <RecipeFilters onFilterChange={setFilters} />
      </div>

      {/* Loading State */}
      {loading && (
        <div className="flex justify-center items-center py-20">
          <Loader2 className="h-8 w-8 animate-spin text-primary" />
        </div>
      )}

      {/* Error State */}
      {error && !loading && (
        <div className="text-center py-12">
          <div className="bg-destructive/10 text-destructive rounded-lg p-6 max-w-md mx-auto">
            <p className="font-medium">Error loading recipes</p>
            <p className="text-sm mt-1">{error}</p>
            <Button onClick={fetchRecipes} variant="outline" className="mt-4">
              Try Again
            </Button>
          </div>
        </div>
      )}

      {/* Empty State */}
      {!loading && !error && recipes.length === 0 && (
        <div className="text-center py-20">
          <div className="flex justify-center mb-4">
            <div className="rounded-full bg-muted p-6">
              <ChefHat className="h-12 w-12 text-muted-foreground" />
            </div>
          </div>
          <h2 className="text-2xl font-semibold mb-2">No recipes found</h2>
          <p className="text-muted-foreground mb-6 max-w-md mx-auto">
            {filters.search || filters.tag || filters.difficulty
              ? 'Try adjusting your filters to find more recipes.'
              : 'Be the first to share a recipe with the UC community!'}
          </p>
          <Link href="/recipes/contribute">
            <Button size="lg">
              <ChefHat className="mr-2 h-5 w-5" />
              Contribute a Recipe
            </Button>
          </Link>
        </div>
      )}

      {/* Recipe Grid */}
      {!loading && !error && recipes.length > 0 && (
        <>
          <div className="mb-4 text-sm text-muted-foreground">
            Found {recipes.length} recipe{recipes.length !== 1 ? 's' : ''}
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {recipes.map((recipe) => (
              <RecipeCard key={recipe.id} recipe={recipe} />
            ))}
          </div>
        </>
      )}
    </div>
  );
}
