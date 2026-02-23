'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth';
import { createRecipe } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { PlusCircle, Trash2, Loader2 } from 'lucide-react';
import { z } from 'zod';

const recipeSchema = z.object({
  title: z.string().min(3, 'Title must be at least 3 characters').max(100),
  description: z.string().min(10, 'Description must be at least 10 characters').max(500),
  ingredients: z.array(z.string().min(1)).min(1, 'At least one ingredient is required'),
  steps: z.array(z.string().min(1)).min(1, 'At least one step is required'),
  tags: z.array(z.string()).min(1, 'At least one tag is required'),
  time_minutes: z.number().min(1, 'Time must be at least 1 minute').max(1440),
  difficulty: z.enum(['easy', 'medium', 'hard']),
  image_url: z.string().url('Must be a valid URL').optional().or(z.literal('')),
});

export default function ContributeRecipePage() {
  const router = useRouter();
  const { isAuthenticated, loading: authLoading, setUser } = useAuth();
  const [submitting, setSubmitting] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});

  const [formData, setFormData] = useState({
    title: '',
    description: '',
    ingredients: [''],
    steps: [''],
    tags: '',
    time_minutes: '',
    difficulty: '',
    image_url: '',
  });

  // Redirect if not authenticated
  if (!authLoading && !isAuthenticated) {
    router.push('/auth/login');
    return null;
  }

  const handleAddIngredient = () => {
    setFormData((prev) => ({
      ...prev,
      ingredients: [...prev.ingredients, ''],
    }));
  };

  const handleRemoveIngredient = (index: number) => {
    setFormData((prev) => ({
      ...prev,
      ingredients: prev.ingredients.filter((_, i) => i !== index),
    }));
  };

  const handleIngredientChange = (index: number, value: string) => {
    setFormData((prev) => {
      const newIngredients = [...prev.ingredients];
      newIngredients[index] = value;
      return { ...prev, ingredients: newIngredients };
    });
  };

  const handleAddStep = () => {
    setFormData((prev) => ({
      ...prev,
      steps: [...prev.steps, ''],
    }));
  };

  const handleRemoveStep = (index: number) => {
    setFormData((prev) => ({
      ...prev,
      steps: prev.steps.filter((_, i) => i !== index),
    }));
  };

  const handleStepChange = (index: number, value: string) => {
    setFormData((prev) => {
      const newSteps = [...prev.steps];
      newSteps[index] = value;
      return { ...prev, steps: newSteps };
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrors({});

    try {
      // Prepare data for validation
      const dataToValidate = {
        title: formData.title,
        description: formData.description,
        ingredients: formData.ingredients.filter((i) => i.trim() !== ''),
        steps: formData.steps.filter((s) => s.trim() !== ''),
        tags: formData.tags.split(',').map((t) => t.trim()).filter((t) => t !== ''),
        time_minutes: Number(formData.time_minutes),
        difficulty: formData.difficulty as 'easy' | 'medium' | 'hard',
        image_url: formData.image_url || undefined,
      };

      // Validate with Zod
      const validatedData = recipeSchema.parse(dataToValidate);

      setSubmitting(true);

      // Submit to API
      const newRecipe = await createRecipe(validatedData);

      // Redirect to the new recipe page
      router.push(`/recipes/${newRecipe.id}`);
    } catch (err: any) {
      if (err instanceof z.ZodError) {
        const fieldErrors: Record<string, string> = {};
        err.errors.forEach((error) => {
          const path = error.path.join('.');
          fieldErrors[path] = error.message;
        });
        setErrors(fieldErrors);
      } else {
        // If it's a 401 error (unauthorized), clear auth and redirect to login
        if (err.status === 401 || err.message?.includes('Could not validate credentials')) {
          setUser(null);
          setErrors({ submit: 'Your session has expired. Please log in again to contribute recipes.' });
          setTimeout(() => {
            router.push('/auth/login');
          }, 2000);
        } else {
          setErrors({ submit: err.message || 'Failed to create recipe' });
        }
      }
      setSubmitting(false);
    }
  };

  if (authLoading) {
    return (
      <div className="container py-12 flex justify-center items-center min-h-[60vh]">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  return (
    <div className="container py-8 md:py-12 max-w-3xl">
      <div className="mb-8">
        <h1 className="text-4xl font-bold tracking-tight mb-2">Contribute a Recipe</h1>
        <p className="text-muted-foreground">
          Share your favorite recipe with the UC community
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Basic Info */}
        <Card>
          <CardHeader>
            <CardTitle>Basic Information</CardTitle>
            <CardDescription>Give your recipe a name and description</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="title">Title *</Label>
              <Input
                id="title"
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                placeholder="e.g., Classic Chocolate Chip Cookies"
              />
              {errors.title && <p className="text-sm text-destructive">{errors.title}</p>}
            </div>

            <div className="space-y-2">
              <Label htmlFor="description">Description *</Label>
              <Textarea
                id="description"
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                placeholder="Brief description of your recipe..."
                rows={3}
              />
              {errors.description && <p className="text-sm text-destructive">{errors.description}</p>}
            </div>

            <div className="space-y-2">
              <Label htmlFor="image_url">Image URL (optional)</Label>
              <Input
                id="image_url"
                type="url"
                value={formData.image_url}
                onChange={(e) => setFormData({ ...formData, image_url: e.target.value })}
                placeholder="https://example.com/image.jpg"
              />
              {errors.image_url && <p className="text-sm text-destructive">{errors.image_url}</p>}
            </div>
          </CardContent>
        </Card>

        {/* Recipe Details */}
        <Card>
          <CardHeader>
            <CardTitle>Recipe Details</CardTitle>
            <CardDescription>Time, difficulty, and tags</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="time_minutes">Time (minutes) *</Label>
                <Input
                  id="time_minutes"
                  type="number"
                  min="1"
                  value={formData.time_minutes}
                  onChange={(e) => setFormData({ ...formData, time_minutes: e.target.value })}
                  placeholder="30"
                />
                {errors.time_minutes && <p className="text-sm text-destructive">{errors.time_minutes}</p>}
              </div>

              <div className="space-y-2">
                <Label htmlFor="difficulty">Difficulty *</Label>
                <Select value={formData.difficulty} onValueChange={(value) => setFormData({ ...formData, difficulty: value })}>
                  <SelectTrigger id="difficulty">
                    <SelectValue placeholder="Select difficulty" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="easy">Easy</SelectItem>
                    <SelectItem value="medium">Medium</SelectItem>
                    <SelectItem value="hard">Hard</SelectItem>
                  </SelectContent>
                </Select>
                {errors.difficulty && <p className="text-sm text-destructive">{errors.difficulty}</p>}
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="tags">Tags * (comma-separated)</Label>
              <Input
                id="tags"
                value={formData.tags}
                onChange={(e) => setFormData({ ...formData, tags: e.target.value })}
                placeholder="e.g., dessert, quick, vegetarian"
              />
              <p className="text-xs text-muted-foreground">Separate tags with commas</p>
              {errors.tags && <p className="text-sm text-destructive">{errors.tags}</p>}
            </div>
          </CardContent>
        </Card>

        {/* Ingredients */}
        <Card>
          <CardHeader>
            <CardTitle>Ingredients</CardTitle>
            <CardDescription>List all ingredients needed</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            {formData.ingredients.map((ingredient, index) => (
              <div key={index} className="flex gap-2">
                <Input
                  value={ingredient}
                  onChange={(e) => handleIngredientChange(index, e.target.value)}
                  placeholder={`Ingredient ${index + 1}`}
                />
                {formData.ingredients.length > 1 && (
                  <Button
                    type="button"
                    variant="outline"
                    size="icon"
                    onClick={() => handleRemoveIngredient(index)}
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                )}
              </div>
            ))}
            <Button
              type="button"
              variant="outline"
              onClick={handleAddIngredient}
              className="w-full"
            >
              <PlusCircle className="h-4 w-4 mr-2" />
              Add Ingredient
            </Button>
            {errors.ingredients && <p className="text-sm text-destructive">{errors.ingredients}</p>}
          </CardContent>
        </Card>

        {/* Steps */}
        <Card>
          <CardHeader>
            <CardTitle>Instructions</CardTitle>
            <CardDescription>Step-by-step cooking instructions</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            {formData.steps.map((step, index) => (
              <div key={index} className="flex gap-2">
                <div className="flex-shrink-0 flex items-center justify-center w-8 h-8 rounded-full bg-primary text-primary-foreground font-semibold text-sm mt-1">
                  {index + 1}
                </div>
                <Textarea
                  value={step}
                  onChange={(e) => handleStepChange(index, e.target.value)}
                  placeholder={`Step ${index + 1}`}
                  rows={2}
                  className="flex-1"
                />
                {formData.steps.length > 1 && (
                  <Button
                    type="button"
                    variant="outline"
                    size="icon"
                    onClick={() => handleRemoveStep(index)}
                    className="flex-shrink-0 mt-1"
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                )}
              </div>
            ))}
            <Button
              type="button"
              variant="outline"
              onClick={handleAddStep}
              className="w-full"
            >
              <PlusCircle className="h-4 w-4 mr-2" />
              Add Step
            </Button>
            {errors.steps && <p className="text-sm text-destructive">{errors.steps}</p>}
          </CardContent>
        </Card>

        {/* Submit */}
        {errors.submit && (
          <div className="bg-destructive/10 text-destructive rounded-lg p-4">
            {errors.submit}
          </div>
        )}

        <div className="flex gap-3">
          <Button type="submit" size="lg" disabled={submitting} className="flex-1">
            {submitting ? (
              <>
                <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                Creating Recipe...
              </>
            ) : (
              'Create Recipe'
            )}
          </Button>
          <Button
            type="button"
            variant="outline"
            size="lg"
            onClick={() => router.back()}
            disabled={submitting}
          >
            Cancel
          </Button>
        </div>
      </form>
    </div>
  );
}
