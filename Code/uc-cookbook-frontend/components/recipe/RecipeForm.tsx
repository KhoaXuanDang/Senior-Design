'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
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
import type { Recipe, User } from '@/lib/types';

export const recipeSchema = z.object({
  title: z.string().min(3, 'Title must be at least 3 characters').max(100),
  description: z.string().min(10, 'Description must be at least 10 characters').max(500),
  ingredients: z.array(z.string().min(1)).min(1, 'At least one ingredient is required'),
  steps: z.array(z.string().min(1)).min(1, 'At least one step is required'),
  tags: z.array(z.string()).min(1, 'At least one tag is required'),
  time_minutes: z.number().min(1, 'Time must be at least 1 minute').max(1440),
  difficulty: z.enum(['easy', 'medium', 'hard']),
  image_url: z.string().url('Must be a valid URL').optional().or(z.literal('')),
  is_published: z.boolean(),
  visibility: z.enum(['public', 'private']),
});

export type RecipeFormValidated = z.infer<typeof recipeSchema>;

export function recipeToFormSnapshot(r: Recipe) {
  return {
    title: r.title,
    description: r.description,
    ingredients: r.ingredients?.length ? [...r.ingredients] : [''],
    steps: r.steps?.length ? [...r.steps] : [''],
    tags: (r.tags || []).join(', '),
    time_minutes: String(r.time_minutes),
    difficulty: r.difficulty,
    image_url: r.image_url || '',
    is_published: r.is_published,
    visibility: r.visibility as 'public' | 'private',
  };
}

type FormState = {
  title: string;
  description: string;
  ingredients: string[];
  steps: string[];
  tags: string;
  time_minutes: string;
  difficulty: string;
  image_url: string;
  is_published: boolean;
  visibility: 'public' | 'private';
};

const emptyForm = (): FormState => ({
  title: '',
  description: '',
  ingredients: [''],
  steps: [''],
  tags: '',
  time_minutes: '',
  difficulty: '',
  image_url: '',
  is_published: false,
  visibility: 'public',
});

export function RecipeForm(props: {
  heading: string;
  subheading: string;
  submitLabel: string;
  submittingLabel: string;
  initialSnapshot?: FormState | null;
  onSubmitValidated: (data: RecipeFormValidated) => Promise<void>;
  setUser: (u: User | null) => void;
  submitErrorContext?: string;
}) {
  const router = useRouter();
  const {
    heading,
    subheading,
    submitLabel,
    submittingLabel,
    initialSnapshot,
    onSubmitValidated,
    setUser,
    submitErrorContext = 'recipe',
  } = props;

  const [submitting, setSubmitting] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [formData, setFormData] = useState<FormState>(emptyForm);

  useEffect(() => {
    if (initialSnapshot) {
      setFormData({
        ...emptyForm(),
        ...initialSnapshot,
        ingredients:
          initialSnapshot.ingredients?.length > 0 ? initialSnapshot.ingredients : [''],
        steps: initialSnapshot.steps?.length > 0 ? initialSnapshot.steps : [''],
      });
    }
  }, [initialSnapshot]);

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
      const dataToValidate = {
        title: formData.title,
        description: formData.description,
        ingredients: formData.ingredients.filter((i) => i.trim() !== ''),
        steps: formData.steps.filter((s) => s.trim() !== ''),
        tags: formData.tags.split(',').map((t) => t.trim()).filter((t) => t !== ''),
        time_minutes: Number(formData.time_minutes),
        difficulty: formData.difficulty as 'easy' | 'medium' | 'hard',
        image_url: formData.image_url || undefined,
        is_published: formData.is_published,
        visibility: formData.visibility,
      };

      const validatedData = recipeSchema.parse(dataToValidate);

      setSubmitting(true);
      await onSubmitValidated(validatedData);
    } catch (err: unknown) {
      if (err instanceof z.ZodError) {
        const fieldErrors: Record<string, string> = {};
        err.errors.forEach((error) => {
          const path = error.path.join('.');
          fieldErrors[path] = error.message;
        });
        setErrors(fieldErrors);
      } else {
        const anyErr = err as { status?: number; message?: string };
        if (anyErr.status === 401 || anyErr.message?.includes('Could not validate credentials')) {
          setUser(null);
          setErrors({
            submit: `Your session has expired. Please log in again to ${submitErrorContext}.`,
          });
          setTimeout(() => router.push('/auth/login'), 2000);
        } else {
          setErrors({ submit: anyErr.message || 'Something went wrong' });
        }
      }
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="container py-8 md:py-12 max-w-3xl">
      <div className="mb-8">
        <h1 className="text-4xl font-bold tracking-tight mb-2">{heading}</h1>
        <p className="text-muted-foreground">{subheading}</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
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

        <Card>
          <CardHeader>
            <CardTitle>Recipe Details</CardTitle>
            <CardDescription>Time, difficulty, tags, and publishing</CardDescription>
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
                <Select
                  value={formData.difficulty}
                  onValueChange={(value) => setFormData({ ...formData, difficulty: value })}
                >
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

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="visibility">Visibility</Label>
                <Select
                  value={formData.visibility}
                  onValueChange={(value: 'public' | 'private') =>
                    setFormData({ ...formData, visibility: value })
                  }
                >
                  <SelectTrigger id="visibility">
                    <SelectValue placeholder="Select visibility" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="public">Public</SelectItem>
                    <SelectItem value="private">Private</SelectItem>
                  </SelectContent>
                </Select>
                {errors.visibility && <p className="text-sm text-destructive">{errors.visibility}</p>}
              </div>

              <div className="space-y-2">
                <Label>Publish Status</Label>
                <Button
                  type="button"
                  variant={formData.is_published ? 'default' : 'outline'}
                  className="w-full"
                  onClick={() => setFormData({ ...formData, is_published: !formData.is_published })}
                >
                  {formData.is_published ? 'Published' : 'Draft'}
                </Button>
                <p className="text-xs text-muted-foreground">Draft recipes are only visible to you.</p>
              </div>
            </div>
          </CardContent>
        </Card>

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
            <Button type="button" variant="outline" onClick={handleAddIngredient} className="w-full">
              <PlusCircle className="h-4 w-4 mr-2" />
              Add Ingredient
            </Button>
            {errors.ingredients && <p className="text-sm text-destructive">{errors.ingredients}</p>}
          </CardContent>
        </Card>

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
            <Button type="button" variant="outline" onClick={handleAddStep} className="w-full">
              <PlusCircle className="h-4 w-4 mr-2" />
              Add Step
            </Button>
            {errors.steps && <p className="text-sm text-destructive">{errors.steps}</p>}
          </CardContent>
        </Card>

        {errors.submit && (
          <div className="bg-destructive/10 text-destructive rounded-lg p-4">{errors.submit}</div>
        )}

        <div className="flex gap-3">
          <Button type="submit" size="lg" disabled={submitting} className="flex-1">
            {submitting ? (
              <>
                <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                {submittingLabel}
              </>
            ) : (
              submitLabel
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
