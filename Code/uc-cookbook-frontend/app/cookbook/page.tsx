'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth';
import { getCookbook, removeRecipeFromCookbook } from '@/lib/api';
import type { CookbookRecipe } from '@/lib/types';
import { RecipeCard } from '@/components/RecipeCard';
import { Button } from '@/components/ui/button';
import { Loader2, BookOpen, Trash2 } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';

export default function CookbookPage() {
  const router = useRouter();
  const { isAuthenticated, loading: authLoading } = useAuth();
  const [cookbookRecipes, setCookbookRecipes] = useState<CookbookRecipe[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [removing, setRemoving] = useState<number | null>(null);

  // Redirect if not authenticated
  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/auth/login');
    }
  }, [authLoading, isAuthenticated, router]);

  useEffect(() => {
    if (isAuthenticated) {
      fetchCookbook();
    }
  }, [isAuthenticated]);

  const fetchCookbook = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getCookbook();
      setCookbookRecipes(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load cookbook');
      console.error('Error fetching cookbook:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleRemove = async (recipeId: number) => {
    if (!confirm('Remove this recipe from your cookbook?')) return;

    try {
      setRemoving(recipeId);
      await removeRecipeFromCookbook(recipeId);
      setCookbookRecipes((prev) => prev.filter((item) => item.recipe_id !== recipeId));
    } catch (err: any) {
      alert(err.message || 'Failed to remove recipe');
      console.error('Error removing recipe:', err);
    } finally {
      setRemoving(null);
    }
  };

  if (authLoading || (loading && cookbookRecipes.length === 0)) {
    return (
      <div className="container py-12 flex justify-center items-center min-h-[60vh]">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="container py-8 md:py-12">
      <div className="mb-8">
        <h1 className="text-4xl font-bold tracking-tight mb-2">My Cookbook</h1>
        <p className="text-muted-foreground">
          Your personal collection of saved recipes
        </p>
      </div>

      {/* Error State */}
      {error && (
        <div className="bg-destructive/10 text-destructive rounded-lg p-6 mb-6">
          <p className="font-medium">Error loading cookbook</p>
          <p className="text-sm mt-1">{error}</p>
          <Button onClick={fetchCookbook} variant="outline" className="mt-4">
            Try Again
          </Button>
        </div>
      )}

      {/* Empty State */}
      {!loading && !error && cookbookRecipes.length === 0 && (
        <div className="text-center py-20">
          <div className="flex justify-center mb-4">
            <div className="rounded-full bg-muted p-6">
              <BookOpen className="h-12 w-12 text-muted-foreground" />
            </div>
          </div>
          <h2 className="text-2xl font-semibold mb-2">Your cookbook is empty</h2>
          <p className="text-muted-foreground mb-6 max-w-md mx-auto">
            Start saving recipes you love to build your personal collection!
          </p>
          <Button onClick={() => router.push('/')} size="lg">
            Browse Recipes
          </Button>
        </div>
      )}

      {/* Recipe Grid with Remove Buttons */}
      {!loading && !error && cookbookRecipes.length > 0 && (
        <>
          <div className="mb-4 text-sm text-muted-foreground">
            {cookbookRecipes.length} saved recipe{cookbookRecipes.length !== 1 ? 's' : ''}
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {cookbookRecipes.map((item) => (
              <div key={item.id} className="relative group">
                <RecipeCard recipe={item.recipe} />
                <div className="absolute top-4 right-4 z-10">
                  <Button
                    variant="destructive"
                    size="icon"
                    onClick={(e) => {
                      e.preventDefault();
                      handleRemove(item.recipe_id);
                    }}
                    disabled={removing === item.recipe_id}
                    className="shadow-lg opacity-0 group-hover:opacity-100 transition-opacity"
                  >
                    {removing === item.recipe_id ? (
                      <Loader2 className="h-4 w-4 animate-spin" />
                    ) : (
                      <Trash2 className="h-4 w-4" />
                    )}
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
