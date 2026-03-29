'use client';

import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth';
import { createRecipe } from '@/lib/api';
import { RecipeForm } from '@/components/recipe/RecipeForm';
import { Loader2 } from 'lucide-react';

export default function ContributeRecipePage() {
  const router = useRouter();
  const { isAuthenticated, loading: authLoading, setUser } = useAuth();

  if (!authLoading && !isAuthenticated) {
    router.push('/auth/login');
    return null;
  }

  if (authLoading) {
    return (
      <div className="container py-12 flex justify-center items-center min-h-[60vh]">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  return (
    <RecipeForm
      heading="Contribute a Recipe"
      subheading="Share your favorite recipe with the UC community"
      submitLabel="Create Recipe"
      submittingLabel="Creating Recipe..."
      setUser={setUser}
      submitErrorContext="contribute recipes"
      onSubmitValidated={async (data) => {
        const newRecipe = await createRecipe(data);
        router.push(`/recipes/${newRecipe.id}`);
      }}
    />
  );
}
