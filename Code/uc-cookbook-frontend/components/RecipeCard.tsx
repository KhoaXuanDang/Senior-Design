'use client';

import Image from 'next/image';
import Link from 'next/link';
import { Clock, ChefHat, User } from 'lucide-react';
import { Card, CardContent, CardFooter, CardHeader } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import type { Recipe } from '@/lib/types';

interface RecipeCardProps {
  recipe: Recipe;
}

export function RecipeCard({ recipe }: RecipeCardProps) {
  const difficultyColors = {
    easy: 'bg-green-100 text-green-800 hover:bg-green-200',
    medium: 'bg-yellow-100 text-yellow-800 hover:bg-yellow-200',
    hard: 'bg-red-100 text-red-800 hover:bg-red-200',
  };

  return (
    <Link href={`/recipes/${recipe.id}`}>
      <Card className="h-full overflow-hidden transition-all hover:shadow-lg group cursor-pointer">
        <div className="relative w-full h-48 bg-muted overflow-hidden">
          {recipe.image_url ? (
            <Image
              src={recipe.image_url}
              alt={recipe.title}
              fill
              className="object-cover transition-transform group-hover:scale-105"
              sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-primary/10 to-primary/5">
              <ChefHat className="h-16 w-16 text-primary/40" />
            </div>
          )}
        </div>
        
        <CardHeader className="pb-3">
          <h3 className="font-semibold text-lg line-clamp-2 group-hover:text-primary transition-colors">
            {recipe.title}
          </h3>
          <p className="text-sm text-muted-foreground line-clamp-2 mt-1">
            {recipe.description}
          </p>
        </CardHeader>
        
        <CardContent className="pb-3">
          <div className="flex flex-wrap gap-1.5">
            {recipe.tags.slice(0, 3).map((tag) => (
              <Badge key={tag} variant="secondary" className="text-xs">
                {tag}
              </Badge>
            ))}
            {recipe.tags.length > 3 && (
              <Badge variant="secondary" className="text-xs">
                +{recipe.tags.length - 3}
              </Badge>
            )}
          </div>
        </CardContent>
        
        <CardFooter className="flex items-center justify-between text-sm text-muted-foreground pt-3 border-t">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-1">
              <Clock className="h-4 w-4" />
              <span>{recipe.time_minutes} min</span>
            </div>
            <Badge variant="outline" className={difficultyColors[recipe.difficulty]}>
              {recipe.difficulty}
            </Badge>
          </div>
          {recipe.author && (
            <div className="flex items-center gap-1">
              <User className="h-4 w-4" />
              <span className="text-xs">{recipe.author.username}</span>
            </div>
          )}
        </CardFooter>
      </Card>
    </Link>
  );
}
