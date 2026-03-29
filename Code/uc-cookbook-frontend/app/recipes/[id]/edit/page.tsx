'use client';

import { useEffect, useMemo, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth';
import { getRecipeById, updateRecipe } from '@/lib/api';
import { RecipeForm, recipeToFormSnapshot } from '@/components/recipe/RecipeForm';
import { Loader2 } from 'lucide-react';
import type { Recipe } from '@/lib/types';
import { Button } from '@/components/ui/button';

export default function EditRecipePage() {
  const params = useParams();
  const router = useRouter();
  const { isAuthenticated, loading: authLoading, user, setUser } = useAuth();
  const [recipe, setRecipe] = useState<Recipe | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const id = Number(params.id);

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/auth/login');
      return;
    }
  }, [authLoading, isAuthenticated, router]);

  useEffect(() => {
    if (authLoading || !isAuthenticated || !user || Number.isNaN(id)) return;

    let cancelled = false;

    (async () => {
      try {
        setLoading(true);
        setLoadError(null);
        const r = await getRecipeById(id);
        if (cancelled) return;
        if (r.author_id !== user.id) {
          setLoadError('You can only edit your own recipes.');
          setRecipe(null);
          return;
        }
        setRecipe(r);
      } catch (e: unknown) {
        if (!cancelled) {
          const msg = e instanceof Error ? e.message : 'Failed to load recipe';
          setLoadError(msg);
          setRecipe(null);
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();

    return () => {
      cancelled = true;
    };
  }, [authLoading, isAuthenticated, user, id]);

  const formSnapshot = useMemo(
    () => (recipe ? recipeToFormSnapshot(recipe) : null),
    [recipe]
  );

  if (authLoading || (loading && !loadError)) {
    return (
      <div className="container py-12 flex justify-center items-center min-h-[60vh]">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  if (loadError) {
    return (
      <div className="container py-12 max-w-lg mx-auto text-center">
        <p className="text-destructive mb-4">{loadError}</p>
        <Button variant="outline" onClick={() => router.push('/')}>
          Back to Browse
        </Button>
      </div>
    );
  }

  if (!recipe) {
    return null;
  }

  return (
    <RecipeForm
      heading="Edit recipe"
      subheading="Update your recipe details and save changes"
      submitLabel="Save changes"
      submittingLabel="Saving..."
      initialSnapshot={formSnapshot!}
      setUser={setUser}
      submitErrorContext="edit this recipe"
      onSubmitValidated={async (data) => {
        await updateRecipe(id, {
          title: data.title,
          description: data.description,
          ingredients: data.ingredients,
          steps: data.steps,
          tags: data.tags,
          time_minutes: data.time_minutes,
          difficulty: data.difficulty,
          image_url: data.image_url,
          is_published: data.is_published,
          visibility: data.visibility,
        });
        router.push(`/recipes/${id}`);
      }}
    />
  );
}
